from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from flask_mail import Message
from oracledb import DataBase
from oracledb import Pool
from oracledb import DataBasePool
from datetime import timedelta
from datetime import datetime
import uuid
import jwt
from time import time
from flask import render_template,current_app

pool=Pool()
pool.creatpool('webmanager','123456','192.168.71.139/oradb')

# 正常普通用户
class User(UserMixin):
    def __init__(self,username):
        # 创建数据库链接类
        self.db=DataBasePool()
        self.username=username
        self.id=self.get_id()
        self.authenticated=False
        self.active=False
        self.anonymous=False
        self.user_type=self.get_type()

    # 是否已认证
    @property
    def is_authenticated(self):
        return self.authenticated
    
    @is_authenticated.setter
    def is_authenticated(self,temp):
        self.authenticated=temp
    
    # 是否活跃
    @property
    def is_active(self):
        return self.active
    
    @is_active.setter
    def is_active(self,temp):
        self.active=temp
    
    # 是否匿名用户
    @property
    def is_anonymous(self):
        return self.anonymous

    @is_anonymous.setter
    def is_anonymous(self,temp):
        self.anonymous=temp

    # 转换password方法为属性
    @property
    def password(self):
        # password不是可读的属性
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        """
            save user name, id and password hash to database
            保存用户名，id,密码hash到数据库
        """
        self.password_hash = generate_password_hash(password)
        # 获取数据库连接
        self.db.connect(pool)
        dic={}
        dic['username']=self.username
        dic['password']=self.password_hash
        try:
            from session import ALLOWSQLI
            cmdinfo=self.db.modify('update weboracle.users set password=:password where username=:username',dic,ALLOWSQLI=ALLOWSQLI)
            if cmdinfo==1:
                self.db.commit()
                return True
        except:
            self.db.rollback()
        self.db.rollback()

    def verify_password(self, password):
        self.password_hash = self.get_password_hash()
        if self.password_hash is None:
            return False
        result=check_password_hash(self.password_hash, password)
        if result==True:
            try:
                from session import ALLOWSQLI
                self.db.connect(pool)
                creatdata=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dic={}
                dic['last_login_time']=creatdata
                dic['sid']=self.id
                print('rew')
                self.db.modify("update weboracle.users set login_num=login_num+1,last_login_time=to_date(:last_login_time,'yyyy-mm-dd hh24:mi:ss') where sid=:sid",dic,ALLOWSQLI=ALLOWSQLI)
                print('dsadada')
                self.db.commit()
                self.db.close()
                return result
            except IOError:
                return None
            except ValueError:
                return None
            except:
                return None
            return False
        else:
            return False 

    def get_password_hash(self):
        """try to get password hash from file.
        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        try:
            from session import ALLOWSQLI
            self.db.connect(pool)
            dic={}
            dic['username']=self.username
            result=self.db.select('select password from weboracle.users where username=:username',dic,ALLOWSQLI=ALLOWSQLI)
            self.db.close()
            return result[1][0][0]
        except IOError:
            return None
        except ValueError:
            return None
        except:
            return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        # 在斟酌要怎么办
        if self.username is not None:
            try:
                from session import ALLOWSQLI
                self.db.connect(pool)
                dic={}
                dic['username']=self.username
                id=self.db.select('select sid from weboracle.users where username=:username',dic,ALLOWSQLI=ALLOWSQLI )  
                if id[0]!=0:
                    return id[1][0][0]
            except IOError:
                pass
            except ValueError:
                pass
            finally:
                self.db.close()
        return None

    def get_jwt_token(self, expires_in=600):
        """获取JWT令牌"""
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},current_app.config['SECRET_KEY'],algorithm='HS256').encode('utf-8')
    
    def get_type(self):
        try:
            from session import ALLOWSQLI
            self.db.connect(pool)
            dic={}
            dic['username']=self.username
            id=self.db.select('select user_type from weboracle.users where username=:username',dic,ALLOWSQLI=ALLOWSQLI )  
            if id[0]!=0:
                return id[1][0][0]
        except IOError:
            pass
        except ValueError:
            pass
        finally:
            self.db.close()
        return None

    def can(self,permission):

        if self.user_type=="2 ":
            return True
        return False

    @staticmethod
    def verify_jwt_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')['reset_password']
        except Exception as e:
            # print(e)
            return False,1
        return True,user_id

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        用户回调函数
        """
        if not user_id:
            return None
        try:
            from session import ALLOWSQLI
            database=DataBasePool()
            database.connect(pool)
            dic={}
            dic['user_id']=user_id
            result=database.select('select username from weboracle.users where sid=:user_id',dic,ALLOWSQLI=ALLOWSQLI)
            if result[0]==1:
                return User(result[1][0][0])
        except:
            return None
        return None

    @staticmethod
    def register(username,password,email,data_time):
        database=DataBasePool()
        database.connect(pool)
        from session import ALLOWSQLI
        dic={}
        dic['user_name']=username
        result=database.select('select username from weboracle.users where username=:user_name',dic,ALLOWSQLI=ALLOWSQLI)
        if result[0]==0:
            try:
                from session import ALLOWSQLI
                user_id=str(uuid.uuid4()).replace('-','')
                password_hash=generate_password_hash(password)
                dic={}
                dic['sid']=user_id
                dic['username']=username
                dic['password']=password_hash
                dic['user_type']=1
                dic['e_mail']=email
                dic['login_num']=1
                dic['last_login_time']=data_time
                database.modify("insert into weboracle.users (sid,username,password,user_type,e_mail,login_num,last_login_time) values(:sid,:username,:password,:user_type,:e_mail,:login_num,to_date(:last_login_time,'yyyy-mm-dd'))",dic,ALLOWSQLI=ALLOWSQLI)
                database.commit()
                return User(username)
            except Exception:
                return None
            finally:
                database.close()
        return None     

    @staticmethod
    def get_email(email):
        """try to return user_id corresponding User object.
        This method is used by reset_password_request function
        根据用户邮箱查找用户
        """
        if not email:
            return None
        try:
            from session import ALLOWSQLI
            database=DataBasePool()
            database.connect(pool)
            dic={}
            dic['email']=email
            result=database.select('select username from weboracle.users where e_mail=:email',dic,ALLOWSQLI=ALLOWSQLI)
            if result[0]==1:
                return User(result[1][0][0])
        except:
            return None
        return None

# class AnonymousUser(AnonymousUserMixin):
#     def __init__(self):
#         pass

def send_email(to, subject, template, **kwargs):
    from session import mail
    msg = Message(subject,sender='2248607145@qq.com',recipients=[to])#实例化一个Message对象，准备发送邮件，接受者为to
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)#将准备好的模板添加到msg对象上，字典传的参里包括token(即生成的一长串字符串)，链接的组装，页面的渲染在里面用jinja2语法完成
    # msg.body = "testing"
    # msg.html = "<b>testing</b>"
    mail.send(msg) #发射

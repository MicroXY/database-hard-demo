from login_form import LoginForm
from login_form import RegisterForm
from login_form import SecrityForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from user import User,send_email
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
from flask_login import fresh_login_required
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import redirect
from flask import flash,abort
from oracledb import Pool
from oracledb import DataBasePool
import time
import uuid
import os
from datetime import timedelta
from datetime import datetime
import urllib
import re
from flask_mail import Mail
from functools import wraps

ALLOWSQLI=True
# 创建数据库连接池
pool=Pool()
# pool链接数据库
pool.creatpool('webmanager','123456','192.168.71.139/oradb')

# Flask类对象
app = Flask(__name__,static_url_path='')
app.config.update(
    MAIL_SERVER = "smtp.qq.com",
    MAIL_PORT = "587",
    MAIL_USE_TLS = True,
    MAIL_USERNAME = "",
    MAIL_PASSWORD = "",
    
    MAIL_DEFAULT_SENDER = "吉林大学计算机科学与技术学院",#默认发送者

)
# 密钥
app.secret_key = os.urandom(24)
# 核心类用户设置
# use login manager to manage session
login_managers = LoginManager()
login_managers.session_protection = 'strong'
login_managers.login_view = 'login'
login_managers.login_message = '请先登录'
login_managers.refresh_view = 'login'
login_managers.needs_refresh_message = '你需要重新登录'
login_managers.remember_cookie_duration=timedelta(days=1)
login_managers.remember_cookie_httponly=True
# login_managers.user
login_managers.init_app(app=app)
# 实例化flask_mail
mail = Mail(app)
# 这个callback函数用于reload User object，根据session中存储的user id
import logging  # 引入logging模块
import os.path
import time
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
filename = r'C:\Users\MIAO -\Desktop\weboracle2.0\weboracle2.0\weboracle\log.txt'
fh = logging.FileHandler(filename, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
@login_managers.user_loader
def load_user(user_id,is_authenticated=True,is_active=False,is_anonymous=False):
    # flash('回调函数')
    user = User.get(user_id)
    user.is_authenticated=is_authenticated
    user.is_active=is_active
    user.is_anonymous=is_anonymous
    return user

# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def calculate_age(birth_s):
    birth_d = datetime.strptime(birth_s, "%Y/%m/%d")
    today_d = datetime.now()
    birth_t = birth_d.replace(year=today_d.year)
    if today_d > birth_t:
        age = today_d.year - birth_d.year
    else:
        age = today_d.year - birth_d.year - 1
    return age

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            # print(current_user.can(2))
            if not current_user.can(2):
                logger.warning('无管理员权限，无法执行此操作')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(2)(f)
'''
@app.before_request
def before_request():
    #假设是post请求，data为传入的请求参数
    # print(request.url)
    
    if re.search(r"*.html",request.path):
        data =request.json
        for v in data.values():
            v= str(v).lower()
            pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
            r = re.search(pattern,v)
            if r:
                abort(405)
    
    return redirect(request.url)
'''

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user is not None and  current_user.is_authenticated:
        url= request.args.get('next')
        next_url=None
        if url!=None:
            next_url = urllib.parse.unquote(url)
        else:
            next_url=None
        login_user(load_user(current_user.id))
        return redirect( next_url or url_for('index') )  
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(user_name).lower())
        if r:
            logger.warning('username一栏检测到非法输入:'+r.group()+'可能为恶意攻击.')
            abort(405)
            return render_template('login.html', title="登录", form=form)
        r = re.search(pattern, str(password).lower())
        if r:
            logger.warning('password一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('login.html', title="登录", form=form)
        user = User(user_name)
        if user.verify_password(password):
            user.is_authenticated=True
            user.is_active=True
            login_user(user, remember=remember_me)
            url= request.args.get('next')
            next_url=None

            if url!=None:
                next_url = urllib.parse.unquote(url)
            else:
                next_url=None
            return redirect( next_url or url_for('index') )
        else:
            return render_template('login.html', title="登录", form=form,info='用户名或密码错误！')     
    return render_template('login.html', title="登录", form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        # print(user_name)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        creatdata=datetime.now().strftime("%Y-%m-%d")
        #print(email)
        #print(creatdata)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(user_name).lower())
        if r:
            logger.warning('user_name一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('register.html', title="注册", form=form)
        r = re.search(pattern, str(password).lower())
        if r:
            logger.warning('password一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('register.html', title="注册", form=form)
        r = re.search(pattern, str(email).lower())
        if r:
            logger.warning('email一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('register.html', title="注册", form=form)
        r = re.search(pattern, str(creatdata).lower())
        if r:
            logger.warning('creatdata一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('register.html', title="注册", form=form)
        user=User.register(user_name,password,email,creatdata)
        if user is not None :
            user.is_active=True
            user.is_authenticated=True
            user.is_anonymous=False
            login_user(user)
            return redirect( request.args.get('next') or url_for('index'))
        else:
            return render_template('register.html', title="注册", form=form,info='用户名不可用!')    
    return render_template('register.html', title="注册", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    form=SecrityForm()
    keys= request.args.get('search')
    '''
    pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
    r = re.search(pattern, str(keys).lower())
    if r:
        logger.warning('keys一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
        abort(405)
        return render_template('index.html', title="注册", form=form)
    '''
    if keys!=None:
        try:
            db=DataBasePool()
            db.connect(pool)
            #results = db.select("select company_id,brief_introduce,upload_time,time_of_end,workplace,salary,job_title,sid from weboracle.company_info WHERE brief_introduce like :pattern OR workplace like :pattern OR salary like :pattern OR job_title like :pattern OR to_char(time_of_end,'yyyy-mm-dd') like :pattern OR to_char(upload_time,'yyyy-mm-dd hh24:mi:ss') like :pattern order by upload_time desc",)
            ll=[]
            d = {}
            # #keys='aa%\' OR \'aa\' like \'%a'
            # print(keys)
            # '''以下方式存在注入漏洞'''
            # sql="select company_id,brief_introduce,upload_time,time_of_end,workplace,salary,job_title,sid from weboracle.company_info WHERE brief_introduce like '%"+keys+"%' OR workplace like '%"+keys+"%' OR salary like '%"+keys+"%' OR job_title like '%"+keys+"%' OR to_char(time_of_end,'yyyy-mm-dd') like '%"+keys+"%' OR to_char(upload_time,'yyyy-mm-dd hh24:mi:ss') like '%"+keys+"%' order by upload_time desc"
            # print(sql)
            # results=db.select(sql,None)
            # '''以下方式不存在漏洞'''
            d["pattern"] = '%' + keys + '%'
            print(d)
            results=db.select("select company_id,brief_introduce,upload_time,time_of_end,workplace,salary,job_title,sid from weboracle.company_info WHERE brief_introduce like :pattern OR workplace like :pattern OR salary like :pattern OR job_title like :pattern OR to_char(time_of_end,'yyyy-mm-dd') like :pattern OR to_char(upload_time,'yyyy-mm-dd hh24:mi:ss') like :pattern order by upload_time desc",d,ALLOWSQLI=ALLOWSQLI)

            # print(results)
            for item in results[1]:
                dic={}
                dic["company_id"]=item[0]
                dic["brief_introduce"]=item[1]
                dic["upload_time"]=item[2]
                dic["time_of_end"]=item[3]
                dic["workplace"]=item[4]
                dic["salary"]=item[5]
                dic["job_title"]=item[6]
                dic["sid"]=item[7]
                ll.append(dic)
            return render_template('index.html',flags=ALLOWSQLI,form=form,index_result=ll,username=current_user.username)
        except:
            return render_template('index.html',flags=ALLOWSQLI,form=form,error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('index.html',flags=ALLOWSQLI,form=form,error='未查询到数据，请刷新重试！',username=current_user.username)
    else:
        try:
            db=DataBasePool()
            db.connect(pool)
            ll=[]
            results=db.select("select company_id,brief_introduce,upload_time,time_of_end,workplace,salary,job_title,sid from weboracle.company_info order by upload_time desc",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["company_id"]=item[0]
                dic["brief_introduce"]=item[1]
                dic["upload_time"]=item[2]
                dic["time_of_end"]=item[3]
                dic["workplace"]=item[4]
                dic["salary"]=item[5]
                dic["job_title"]=item[6]
                dic["sid"]=item[7]
                ll.append(dic)
            return render_template('index.html',flags=ALLOWSQLI,form=form,index_result=ll,username=current_user.username)
        except:
            return render_template('index.html',flags=ALLOWSQLI,form=form,error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('index.html',flags=ALLOWSQLI,form=form,error='未查询到数据，请刷新重试！',username=current_user.username)
    


# @login_required
# @app.route('/')
@app.route('/reset_password',methods=['GET','POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        #验证密码是否为登录状态，如果是，则终止重置密码
        return redirect(url_for('index'))
    form=SecrityForm()
    if form.validate_on_submit():
        email = request.form.get('email', None)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(email).lower())
        if r:
            logger.warning('email一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('reset_password.html', form=form)
        user = User.get_email(email)
        if user:
            #如果用户存在
            token = user.get_jwt_token()
            #调用User模块中的generate_reset_token函数生成验证信息
            send_email(email,'重置密码','mail',token=token,username=user.username)
            #调用send_email函数，渲染邮件内容之后发送重置密码邮件
        return render_template('reset_password.html',form=form,info="重置密码邮件已发送，请注意查收")
    return render_template('reset_password.html',form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    form=SecrityForm()
    if form.validate_on_submit():
        password=request.form.get('password', None)
        tokens=request.form.get('token', None)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(password).lower())
        if r:
            logger.warning('password一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('password_reset.html', form=form,token=token)
        r = re.search(pattern, str(tokens).lower())
        if r:
            logger.warning('tokens一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('password_reset.html', form=form, token=token)
        if User.verify_jwt_token(bytes(tokens.encode('utf-8')))[0]==True:
            user = User.get(User.verify_jwt_token(bytes( tokens.encode('utf-8') ))[1])
            if user is None:
                return render_template('password_reset.html',form=form,token=token,info="密码重置失败,用户不存在")  
            user.password=password              
            return redirect(url_for('login'))
            # else:
            #     return render_template('password_reset.html',form=form,token=token,info="密码重置失败")
        return render_template('password_reset.html',form=form,token=token,info="你是不是来盗号的?????")    
    return render_template('password_reset.html',form=form,token=token)

@app.route('/job_wanted')
@login_required
def job_wanted():
    form=SecrityForm()
    keys= request.args.get('search')
    pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
    r = re.search(pattern, str(keys).lower())
    if r:
        logger.warning('keys一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
        abort(405)
        return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,username=current_user.username)
    if keys!=None:
        try:
            db=DataBasePool()
            db.connect(pool)
            d={}
            d["pattern"]='%'+keys+'%'
            ll=[]
            results=db.select("select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,job_wanted,salary,job_time,to_char(time_of_graduation,'yyyy-mm-dd') from weboracle.student_info WHERE name like :pattern OR sex like :pattern OR education_background like :pattern OR school_of_graduation like :pattern OR to_char(birth_time,'yyyy-mm-dd') like :pattern OR job_wanted like :pattern OR salary like :pattern OR job_time like :pattern OR to_char(time_of_graduation,'yyyy-mm-dd') like :pattern order by salary desc",d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["stu_id"]=item[0]
                dic["name"]=item[1]
                if str(item[2])=="man   " or str(item[2])=="男    ":
                    dic["sex"]='男' 
                else:
                    dic["sex"]='女'
                dic["birth_time"]=str(calculate_age(item[3]))+'岁'
                dic["education_background"]=item[4]
                dic["school_of_graduation"]=item[5]
                dic["job_wanted"]=item[6]
                dic["salary"]=item[7]
                dic["job_time"]=item[8]
                dic["time_of_graduation"]=item[9]
                ll.append(dic)
            return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,job_result=ll,username=current_user.username)
        except:
            return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,error='未查询到数据，请刷新重试！',username=current_user.username)
    else:
        try:
            db=DataBasePool()
            db.connect(pool)
            ll=[]
            results=db.select("select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,job_wanted,salary,job_time,to_char(time_of_graduation,'yyyy-mm-dd') from weboracle.student_info order by salary desc",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["stu_id"]=item[0]
                dic["name"]=item[1]
                if str(item[2])=="man   " or str(item[2])=="男    ":
                    dic["sex"]='男'
                else:
                    dic["sex"]='女'
                dic["birth_time"]=str(calculate_age(item[3]))+'岁'
                dic["education_background"]=item[4]
                dic["school_of_graduation"]=item[5]
                dic["job_wanted"]=item[6]
                dic["salary"]=item[7]
                dic["job_time"]=item[8]
                dic["time_of_graduation"]=item[9]
                ll.append(dic)
            return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,job_result=ll,username=current_user.username)
        except:
            return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('job_wanted.html',flags=ALLOWSQLI,form=form,error='未查询到数据，请刷新重试！',username=current_user.username)

# @app.route('/')
@app.route('/info_modification',methods=['GET','POST'])
@login_required
def info_modification(): 
    form = SecrityForm()
    if form.validate_on_submit():
        db=DataBasePool()
        db.connect(pool)
        try:
            store_id=str(uuid.uuid4()).replace('-','')
            name = request.form.get('val-name', None)
            sex = request.form.get('val-sex', None)
            birth_time = request.form.get('birth_time', None)
            education_background = request.form.get('val-education_background', None)
            time_of_graduation = request.form.get('time_of_graduation', None)
            school_of_graduation = request.form.get('val-school_of_graduation', None)
            major = request.form.get('val-major', None)
            phone_number = request.form.get('val-phone_number', None)
            job_wanted = request.form.get('val-job_wanted', None)
            job_time = request.form.get('val-job_time', None)
            salary = request.form.get('val-salary', None)
            suggestions = request.form.get('val-suggestions', None)
            pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
            r = re.search(pattern, str(name).lower())
            if r:
                logger.warning('name一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form,username=current_user.username)
            r = re.search(pattern, str(sex).lower())
            if r:
                logger.warning('sex一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(birth_time).lower())
            if r:
                logger.warning('birth_time一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(education_background).lower())
            if r:
                logger.warning('education_background一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(time_of_graduation).lower())
            if r:
                logger.warning('time_of_graduation一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(school_of_graduation).lower())
            if r:
                logger.warning('school_of_graduation一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(major).lower())
            if r:
                logger.warning('major一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(phone_number).lower())
            if r:
                logger.warning('phone_number一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(job_wanted).lower())
            if r:
                logger.warning('job_wanted一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(job_time).lower())
            if r:
                logger.warning('job_time一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(salary).lower())
            if r:
                logger.warning('salary一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(suggestions).lower())
            if r:
                logger.warning('suggestions一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            dic={}
            dic["stu_id"]=store_id
            dic["name"]=name
            dic["sex"]=sex
            dic["birth_time"]=birth_time
            dic["education_background"]=education_background
            dic["school_of_graduation"]=school_of_graduation
            dic["time_of_graduation"]=time_of_graduation
            dic["major"]=major
            dic["resume"]=suggestions
            dic["phone_number"]=phone_number
            dic["job_time"]=job_time
            dic["job_wanted"]=job_wanted
            dic["salary"]=salary
            dic["sid"]=current_user.id
            
            for value in dic.values():
                # print(value)
                if value=='':
                    return render_template('info_modification.html',flags=ALLOWSQLI,form=form,error='所有表格都为必填项，请重新填写！',username=current_user.username)
            if is_number(phone_number)==False:
                return render_template('info_modification.html',flags=ALLOWSQLI,form=form,error='电话号码格式错误，请重新填写！',username=current_user.username)
            db.modify("insert into weboracle.student_info (stu_id,name,sex,birth_time,education_background,time_of_graduation,school_of_graduation,major,resume,phone_number,job_time,job_wanted,salary,sid) values (:stu_id,:name,:sex,to_date(:birth_time,'yyyy-mm-dd'),:education_background,to_date(:time_of_graduation,'yyyy-mm-dd'),:school_of_graduation,:major,:resume,:phone_number,:job_time,:job_wanted,:salary,:sid)",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        except:
            db.rollback()
            return render_template('info_modification.html',flags=ALLOWSQLI,form=form,error='服务器发生错误，请重试！',username=current_user.username)
        finally:
            db.close()
        return render_template('info_modification.html',flags=ALLOWSQLI, form=form,info='发布成功!',username=current_user.username)     
    return render_template('info_modification.html',flags=ALLOWSQLI, form=form,username=current_user.username)

# @app.route('/')
@app.route('/manager_info',methods=['GET','POST'])
@login_required
@admin_required
def manager_info():
    form=SecrityForm()
    db=DataBasePool()
    db.connect(pool)
    if form.validate_on_submit():
        if request.form.get('delete',None)!=None:
            dic = {}
            type_pk = request.form.get('pk', None)
            dic['stu_id'] = type_pk
            db.modify("delete from weboracle.student_info where stu_id=:stu_id", dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
            ll = []
            results = db.select(
                "select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info ",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic = {}
                dic["stu_id"] = item[0]
                dic["name"] = item[1]
                if str(item[2]) == "man   " or str(item[2]) == "男    ":
                    dic["sex"] = '男'
                else:
                    dic["sex"] = '女'
                dic["birth_time"] = item[3]
                dic["education_background"] = item[4]
                dic["school_of_graduation"] = item[5]
                dic["time_of_graduation"] = item[6]
                dic["major"] = item[7]
                dic["resume"] = item[8]
                dic["phone_number"] = item[9]
                dic["job_time"] = item[10]
                dic["job_wanted"] = item[11]
                dic["salary"] = item[12]
                ll.append(dic)
            return render_template('manager_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info', manager_info_result=ll,
                                       error='删除成功！',username=current_user.username)
        return render_template('manager_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',username=current_user.username)
    else:
        try:
            ll=[]
            results=db.select("select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info ",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["stu_id"]=item[0]
                dic["name"]=item[1]
                if str(item[2])=="man   " or str(item[2])=="男    ":
                    dic["sex"]='男'
                else:
                    dic["sex"]='女'
                dic["birth_time"]=item[3]
                dic["education_background"]=item[4]
                dic["school_of_graduation"]=item[5]
                dic["time_of_graduation"]=item[6]
                dic["major"]=item[7]
                dic["resume"]=item[8]
                dic["phone_number"]=item[9]
                dic["job_time"]=item[10]
                dic["job_wanted"]=item[11]
                dic["salary"]=item[12]
                ll.append(dic)
            
            return render_template('manager_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',manager_info_result=ll,username=current_user.username)
        except:
            return render_template('manager_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('manager_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',error='未查询到数据，请刷新重试！',username=current_user.username)

@app.route('/manager_user',methods=['GET','POST'])
@login_required
@admin_required
def manager_user():
    form=SecrityForm()
    db = DataBasePool()
    db.connect(pool)
    if form.validate_on_submit():
        if request.form.get('delete',None)!=None:
            dic = {}
            type_pk = request.form.get('pk', None)
            dic['sid'] = type_pk
            results = db.select("select user_type from weboracle.users where sid=:sid", dic)
            if len(results[1])!=0:
                if int(results[1][0][0])!=1:
                    # print(type(results[1][0][0]))
                    logger.warning('无权限删除管理员信息')
                    abort(403)
                    return render_template('manager_user.html',flags=ALLOWSQLI, form=form, URL='/manager_user',username=current_user.username)
                db.modify("delete from weboracle.users where sid=:sid", dic)
                db.modify("delete from weboracle.student_info where sid=:sid", dic)
                db.modify("delete from weboracle.company_info where sid=:sid", dic)
                db.commit()
                ll = []
                results = db.select(
                    "select sid,username,user_type,E_mail,login_num,last_login_time from weboracle.users order by last_login_time desc")
                for item in results[1]:
                    dic = {}
                    dic["sid"] = item[0]
                    dic["username"] = item[1]
                    dic["user_type"] = item[2]
                    dic["Email"] = item[3]
                    dic["login_num"] = item[4]
                    dic["last_login_time"] = item[5]
                    ll.append(dic)
                return render_template('manager_user.html',flags=ALLOWSQLI, form=form, URL='/manager_user', manager_user_result=ll,
                                       error='删除成功',username=current_user.username)
            else:
                ll = []
                results = db.select(
                    "select sid,username,user_type,E_mail,login_num,last_login_time from weboracle.users order by last_login_time desc")
                for item in results[1]:
                    dic = {}
                    dic["sid"] = item[0]
                    dic["username"] = item[1]
                    dic["user_type"] = item[2]
                    dic["Email"] = item[3]
                    dic["login_num"] = item[4]
                    dic["last_login_time"] = item[5]
                    ll.append(dic)
                return render_template('manager_user.html',flags=ALLOWSQLI, form=form, URL='/manager_user', manager_user_result=ll,
                                       error='删除成功', username=current_user.username)
        type_name  = request.form.get('name', None)
        type_value   = request.form.get('value', None)
        type_pk   = request.form.get('pk', None)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(type_name).lower())
        if r:
            logger.warning('type_name一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',username=current_user.username)
        r = re.search(pattern, str(type_value).lower())
        if r:
            logger.warning('type_value一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',username=current_user.username)
        r = re.search(pattern, str(type_pk).lower())
        if r:
            logger.warning('type_pk一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',username=current_user.username)
        dic={}
        dic['sid']=type_pk
        dic['value']=type_value
        if type_name=='username':
            db.modify("update weboracle.users set username=:value where sid=:sid",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='user_type':
            db.modify("update weboracle.users set user_type=:value where sid=:sid",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='EMail':
            db.modify("update weboracle.users set e_mail=:value where sid=:sid",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        else :
            return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',error='未知错误',username=current_user.username)
        return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',error='修改成功',username=current_user.username)

    else:
        try:
            ll=[]
            results=db.select("select sid,username,user_type,E_mail,login_num,last_login_time from weboracle.users order by last_login_time desc",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["sid"]=item[0]
                dic["username"]=item[1]
                dic["user_type"]=item[2]
                dic["Email"]=item[3]
                dic["login_num"]=item[4]
                dic["last_login_time"]=item[5]
                ll.append(dic)
            return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',manager_user_result=ll,username=current_user.username)
        except:
            return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('manager_user.html',flags=ALLOWSQLI,form=form,URL='/manager_user',error='未查询到数据，请刷新重试！',username=current_user.username)

@app.route('/modify_self_info',methods=['GET','POST'])
@login_required
def modify_self_info():
    form=SecrityForm()
    db = DataBasePool()
    db.connect(pool)
    keys=request.form.get('search',None)
    if keys != None:
        try:
            ll = []
            d = {}
            # print(keys)
            d["sid"]=current_user.id
            # '''以下方式存在注入漏洞'''
            # #05%') OR ('ab' like '%a
            # '''
            # sql = "select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info where sid=:sid AND (stu_id like '%" + keys + "%' OR name like '%" + keys + "%' OR sex like '%" + keys + "%' OR to_char(birth_time,'yyyy/mm/dd') like '%" + keys + "%' OR education_background like '%" + keys + "%' OR school_of_graduation like '%" + keys+ "%' OR to_char(time_of_graduation,'yyyy-mm-dd') like '%" + keys+ "%' OR major like '%" + keys+ "%' OR resume like '%" + keys+ "%' OR phone_number like '%"+ keys+ "%' OR job_time like '%"+ keys+ "%' OR job_wanted like '%"+ keys + "%' OR salary like '%"+ keys + "%') order by stu_id desc"
            # print(sql)
            # results = db.select(sql, d)
            # '''
            # '''以下方式不存在漏洞'''
            d["pattern"] = '%' + keys + '%'
            results=db.select("select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info where sid=:sid AND ( stu_id like :pattern OR name like :pattern OR sex like :pattern OR to_char(birth_time,'yyyy/mm/dd') like :pattern OR education_background like :pattern OR school_of_graduation like :pattern OR to_char(time_of_graduation,'yyyy-mm-dd') like :pattern OR major like :pattern OR resume like :pattern OR phone_number like :pattern OR job_time like :pattern OR job_wanted like :pattern OR salary like :pattern) order by stu_id desc",d,ALLOWSQLI=ALLOWSQLI)

            # print(results)
            for item in results[1]:
                dic = {}
                dic["stu_id"] = item[0]
                dic["name"] = item[1]
                if str(item[2]) == "man   " or str(item[2]) == "男    ":
                    dic["sex"] = '男'
                else:
                    # print(str(item[2])+"?")
                    dic["sex"] = '女'
                dic["birth_time"] = item[3]
                dic["education_background"] = item[4]
                dic["school_of_graduation"] = item[5]
                dic["time_of_graduation"] = item[6]
                dic["major"] = item[7]
                dic["resume"] = item[8]
                dic["phone_number"] = item[9]
                dic["job_time"] = item[10]
                dic["job_wanted"] = item[11]
                dic["salary"] = item[12]
                ll.append(dic)
            return render_template('modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info',
                                   modify_self_info_result=ll, username=current_user.username)
        except:
            return render_template('modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info',
                                   error="服务器发生错误", username=current_user.username)
        finally:
            db.close()
        return render_template('modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info',
                               error="为查询到数据", username=current_user.username)
    if form.validate_on_submit():
        if request.form.get('delete',None)!=None:
            dic = {}
            type_pk = request.form.get('pk', None)
            dic['stu_id'] = type_pk
            db.modify("delete from weboracle.student_info where stu_id=:stu_id", dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
            ll=[]
            d={}
            d['sid']=current_user.id
            results=db.select("select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info where sid=:sid",d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["stu_id"]=item[0]
                dic["name"]=item[1]
                if str(item[2])=="man   " or str(item[2])=="男    ":
                    dic["sex"]='男'
                else:
                    dic["sex"]='女'
                dic["birth_time"]=item[3]
                dic["education_background"]=item[4]
                dic["school_of_graduation"]=item[5]
                dic["time_of_graduation"]=item[6]
                dic["major"]=item[7]
                dic["resume"]=item[8]
                dic["phone_number"]=item[9]
                dic["job_time"]=item[10]
                dic["job_wanted"]=item[11]
                dic["salary"]=item[12]
                ll.append(dic)
            return render_template('modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info',
                                   modify_self_info_result=ll, username=current_user.username)
        # None=request.form.get('delete', None)
        type_name  = request.form.get('name', None)
        type_value   = request.form.get('value', None)
        type_pk   = request.form.get('pk', None)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(type_name).lower())
        if r:
            logger.warning('type_name一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',username=current_user.username)
        r = re.search(pattern, str(type_value).lower())
        if r:
            logger.warning('type_value一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info',username=current_user.username)
        r = re.search(pattern, str(type_pk).lower())
        if r:
            logger.warning('type_pk一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/modify_self_info',username=current_user.username)
        dic={}
        dic['stu_id']=type_pk
        dic['value']=type_value
        # print(dic)
        if type_name=='names':
            db.modify("update weboracle.student_info set name=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='sex':
            db.modify("update weboracle.student_info set sex=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='birth_time':
            db.modify("update weboracle.student_info set birth_time=to_date(:value,'yyyy-mm-dd') where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='education_background':
            db.modify("update weboracle.student_info set education_background=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='time_of_graduation':
            db.modify("update weboracle.student_info set time_of_graduation=to_date(:value,'yyyy-mm-dd') where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='school_of_graduation':
            db.modify("update weboracle.student_info set school_of_graduation=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='major':
            db.modify("update weboracle.student_info set major=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='phone_number':
            db.modify("update weboracle.student_info set phone_number=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='job_wanted':
            db.modify("update weboracle.student_info set job_wanted=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='job_time':
            db.modify("update weboracle.student_info set job_time=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='salary':
            db.modify("update weboracle.student_info set salary=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='resume':
            db.modify("update weboracle.student_info set resume=:value where stu_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        else :
            return render_template('modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',error='未知错误',username=current_user.username)
        return render_template('modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',error='修改成功',username=current_user.username)
    else:
        try:
            db=DataBasePool()
            db.connect(pool)
            ll=[]
            d={}
            d['sid']=current_user.id
            results=db.select("select stu_id,name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info where sid=:sid",d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["stu_id"]=item[0]
                dic["name"]=item[1]
                if str(item[2])=="man   " or str(item[2])=="男    ":
                    dic["sex"]='男'
                else:
                    # print(str(item[2])+"?")
                    dic["sex"]='女'
                dic["birth_time"]=item[3]
                dic["education_background"]=item[4]
                dic["school_of_graduation"]=item[5]
                dic["time_of_graduation"]=item[6]
                dic["major"]=item[7]
                dic["resume"]=item[8]
                dic["phone_number"]=item[9]
                dic["job_time"]=item[10]
                dic["job_wanted"]=item[11]
                dic["salary"]=item[12]
                ll.append(dic)
            
            return render_template('modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',modify_self_info_result=ll,username=current_user.username)
        except:
            return render_template('modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/modify_self_info',error='未查询到数据，请刷新重试！',username=current_user.username)
    

@app.route('/person_resume')
@login_required
def person_resume():
    form=SecrityForm()
    url= request.args.get('jobID')
    pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
    r = re.search(pattern, str(url).lower())
    if r:
        logger.warning('url一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
        abort(405)
        return render_template('person_resume.html',flags=ALLOWSQLI,form=form, username=current_user.username)
    # print(url)
    if url!=None:
        db=DataBasePool()
        db.connect(pool)
        try:
            ll=[]
            d={}
            d['stu_id']=url
            results=db.select("select name,sex,to_char(birth_time,'yyyy/mm/dd'),education_background,school_of_graduation,to_char(time_of_graduation,'yyyy-mm-dd'),major,resume,phone_number,job_time,job_wanted,salary from weboracle.student_info where stu_id=:stu_id",d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["name"]=item[0]
                if str(item[1])=="man   ":
                    dic["sex"]='男'
                else:
                    # print(str(item[2])+"?")
                    dic["sex"]='女'
                dic["birth_time"]=str(calculate_age(item[2]))+'岁'
                dic["education_background"]=item[3]
                dic["school_of_graduation"]=item[4]
                dic["time_of_graduation"]=item[5]
                dic["major"]=item[6]
                dic["resume"]=item[7]
                dic["phone_number"]=item[8]
                dic["job_time"]=item[9]
                dic["job_wanted"]=item[10]
                dic["salary"]=item[11]
                ll.append(dic)
            return render_template('person_resume.html',flags=ALLOWSQLI,form=form,person_resume_result=ll, username=current_user.username)
        except:
            return render_template('person_resume.html',flags=ALLOWSQLI,form=form,error='服务器发送错误，请重试！', username=current_user.username)
        finally:
            db.close()
        return render_template('person_resume.html',flags=ALLOWSQLI,form=form,error='服务器发送错误，请重试！', username=current_user.username)
    else: 
        return render_template('person_resume.html',flags=ALLOWSQLI,form=form,error='没有查询到结果，请返回重试', username=current_user.username)

@app.route('/company_resume')
@login_required
def company_resume():
    form=SecrityForm()
    url= request.args.get('comID')
    pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
    r = re.search(pattern, str(url).lower())
    if r:
        logger.warning('url一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
        abort(405)
        return render_template('company_resume.html',flags=ALLOWSQLI,form=form, username=current_user.username)
    # print(url)
    if url!=None:
        db=DataBasePool()
        db.connect(pool)
        try:
            ll=[]
            d={}
            d['company_id']=url
            results=db.select("select name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info where company_id=:company_id",d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["name"]=item[0]
                dic["brief_introduce"]=item[1]
                dic["address"]=item[2]
                dic["contact_person"]=item[3]
                dic["phone_number"]=item[4]
                dic["person_num"]=item[5]
                dic["requirement"]=item[6]
                dic["time_of_end"]=item[7]
                dic["workplace"]=item[8]
                dic["salary"]=item[9]
                dic["job_title"]=item[10]

                ll.append(dic)
            return render_template('company_resume.html',flags=ALLOWSQLI,form=form,company_resume_result=ll, username=current_user.username)
        except:
            return render_template('company_resume.html',flags=ALLOWSQLI,form=form,error='服务器发送错误，请重试！', username=current_user.username)
        finally:
            db.close()
        return render_template('company_resume.html',flags=ALLOWSQLI,form=form,error='服务器发送错误，请重试！', username=current_user.username)
    else: 
        return render_template('company_resume.html',flags=ALLOWSQLI,form=form,error='没有查询到结果，请返回重试', username=current_user.username)


@app.route('/company_modify_self_info',methods=['GET','POST'])
@login_required
def company_modify_self_info():
    form=SecrityForm()
    db = DataBasePool()
    db.connect(pool)
    keys = request.form.get('search', None)
    if keys != None:
        try:
            ll = []
            d = {}
            d["sid"] = current_user.id
            # '''以下方式存在注入漏洞'''
            # # 05%') OR ('ab' like '%a


            # sql="select company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info where sid=:sid AND ( company_id like '%" + keys + "%' OR name like '%" + keys + "%' OR brief_introduce like '%" + keys + "%' OR address like '%" + keys + "%' OR contact_person like '%" + keys + "%' OR phone_number like '%" + keys + "%' OR person_num like '%" + keys + "%' OR requirement like '%" + keys + "%' OR time_of_end like '%" + keys + "%' OR workplace like '%" + keys + "%' OR salary like '%" + keys + "%' OR job_title like '%" + keys + "%') order by company_id desc"
            # # print(sql)
            # results = db.select(sql, d)

            # '''以下方式不存在漏洞'''
            
            d["pattern"] = '%' + keys + '%'
            results = db.select(
                "select company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info where sid=:sid AND ( company_id like :pattern OR name like :pattern OR brief_introduce like :pattern OR address like :pattern OR contact_person like :pattern OR phone_number like :pattern OR person_num like :pattern OR requirement like :pattern OR time_of_end like :pattern OR workplace like :pattern OR salary like :pattern OR job_title like :pattern) order by company_id desc",
                d,ALLOWSQLI=ALLOWSQLI)
            
            # print(results)
            for item in results[1]:
                dic = {}
                dic["company_id"] = item[0]
                dic["name"] = item[1]
                dic["brief_introduce"] = item[2]
                dic["address"] = item[3]
                dic["contact_person"] = item[4]
                dic["phone_number"] = item[5]
                dic["person_num"] = item[6]
                dic["requirement"] = item[7]
                dic["time_of_end"] = item[8]
                dic["workplace"] = item[9]
                dic["salary"] = item[10]
                dic["job_title"] = item[11]
                ll.append(dic)
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/company_modify_self_info',
                                   company_modify_self_info_result=ll, username=current_user.username)
        except:
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/company_modify_self_info',
                                   error="服务器发生错误", username=current_user.username)
        finally:
            db.close()
        return render_template('company_modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/company_modify_self_info',
                               error="为查询到数据", username=current_user.username)
    if form.validate_on_submit():
        if request.form.get('delete',None)!=None:
            dic = {}
            type_pk = request.form.get('pk', None)
            dic['company_id'] = type_pk
            db.modify("delete from weboracle.company_info where company_id=:company_id", dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
            ll = []
            d = {}
            d['sid'] = current_user.id
            results = db.select(
                "select company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info where sid=:sid order by time_of_end desc",
                d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic = {}
                dic["company_id"] = item[0]
                dic["name"] = item[1]
                dic["brief_introduce"] = item[2]
                dic["address"] = item[3]
                dic["contact_person"] = item[4]
                dic["phone_number"] = item[5]
                dic["person_num"] = item[6]
                dic["requirement"] = item[7]
                dic["time_of_end"] = item[8]
                dic["workplace"] = item[9]
                dic["salary"] = item[10]
                dic["job_title"] = item[11]
                ll.append(dic)
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI, form=form, URL='/company_modify_self_info',
                                   company_modify_self_info_result=ll, username=current_user.username)
        type_name  = request.form.get('name', None)
        type_value   = request.form.get('value', None)
        type_pk   = request.form.get('pk', None)
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, str(type_name).lower())
        if r:
            logger.warning('type_name一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',username=current_user.username)
        r = re.search(pattern, str(type_value).lower())
        if r:
            logger.warning('type_value一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',username=current_user.username)
        r = re.search(pattern, str(type_pk).lower())
        if r:
            logger.warning('type_pk一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
            abort(405)
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',username=current_user.username)
        dic={}
        dic['stu_id']=type_pk
        dic['value']=type_value
        if type_name=='company_name':
            db.modify("update weboracle.company_info set name=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='brief_introduce':
            db.modify("update weboracle.company_info set brief_introduce=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='address':
            db.modify("update weboracle.company_info set address=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='job_type':
            db.modify("update weboracle.company_info set job_title=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='company_dob':
            db.modify("update weboracle.company_info set time_of_end=to_date(:value,'yyyy-mm-dd') where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='workplace':
            db.modify("update weboracle.company_info set workplace=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='company_salary':
            db.modify("update weboracle.company_info set salary=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='contact_person':
            db.modify("update weboracle.company_info set contact_person=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='company_phone_number':
            db.modify("update weboracle.company_info set phone_number=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='person_num':
            db.modify("update weboracle.company_info set person_num=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        elif type_name=='company_comments':
            db.modify("update weboracle.company_info set requirement=:value where company_id=:stu_id",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        else :
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='未知错误',username=current_user.username)
        return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='修改成功',username=current_user.username)
    else:
        try:
            db=DataBasePool()
            db.connect(pool)
            ll=[]
            d={}
            d['sid']=current_user.id
            results=db.select("select company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info where sid=:sid order by time_of_end desc",d,ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["company_id"]=item[0]
                dic["name"]=item[1]
                dic["brief_introduce"]=item[2]
                dic["address"]=item[3]
                dic["contact_person"]=item[4]
                dic["phone_number"]=item[5]
                dic["person_num"]=item[6]
                dic["requirement"]=item[7]
                dic["time_of_end"]=item[8]
                dic["workplace"]=item[9]
                dic["salary"]=item[10]
                dic["job_title"]=item[11]
                ll.append(dic)
            
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',company_modify_self_info_result=ll,username=current_user.username)
        except:
            return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('company_modify_self_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='未查询到数据，请刷新重试！',username=current_user.username)
    

@app.route('/company_manager_info',methods=['GET','POST'])
@login_required
@admin_required
def company_manager_info():
    form=SecrityForm()
    db=DataBasePool()
    db.connect(pool)
    if form.validate_on_submit():
        if request.form.get('delete',None)!=None:
            dic = {}
            type_pk = request.form.get('pk', None)
            dic['company_id'] = type_pk
            db.modify("delete from weboracle.company_info where company_id=:company_id", dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
            ll = []
            results = db.select(
                "select company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info order by time_of_end desc",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic = {}
                dic["company_id"] = item[0]
                dic["name"] = item[1]
                dic["brief_introduce"] = item[2]
                dic["address"] = item[3]
                dic["contact_person"] = item[4]
                dic["phone_number"] = item[5]
                dic["person_num"] = item[6]
                dic["requirement"] = item[7]
                dic["time_of_end"] = item[8]
                dic["workplace"] = item[9]
                dic["salary"] = item[10]
                dic["job_title"] = item[11]
                ll.append(dic)
            return render_template('company_manager_info.html',flags=ALLOWSQLI, form=form, URL='/company_modify_self_info',
                                   error='删除成功',company_manager_info_result=ll, username=current_user.username)
        return render_template('company_manager_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='成功',username=current_user.username)
    else:
        try:

            ll=[]
            results=db.select("select company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,time_of_end,workplace,salary,job_title from weboracle.company_info order by time_of_end desc",ALLOWSQLI=ALLOWSQLI)
            for item in results[1]:
                dic={}
                dic["company_id"]=item[0]
                dic["name"]=item[1]
                dic["brief_introduce"]=item[2]
                dic["address"]=item[3]
                dic["contact_person"]=item[4]
                dic["phone_number"]=item[5]
                dic["person_num"]=item[6]
                dic["requirement"]=item[7]
                dic["time_of_end"]=item[8]
                dic["workplace"]=item[9]
                dic["salary"]=item[10]
                dic["job_title"]=item[11]

                ll.append(dic)
            
            return render_template('company_manager_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',company_manager_info_result=ll,username=current_user.username)
        except:
            return render_template('company_manager_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='服务器发生错误！！！',username=current_user.username)
        finally:
            db.close()
        return render_template('company_manager_info.html',flags=ALLOWSQLI,form=form,URL='/company_modify_self_info',error='未查询到数据，请刷新重试！',username=current_user.username)
    



@app.route('/company_info_modification',methods=['GET','POST'])
@login_required
def company_info_modification():
    form = SecrityForm()
    if form.validate_on_submit():
        db=DataBasePool()
        db.connect(pool)
        try:
            store_id=str(uuid.uuid4()).replace('-','')
            company_name = request.form.get('val-company_name', None)
            brief_introduce = request.form.get('val-brief_introduce', None)
            address = request.form.get('val-address', None)
            job_type = request.form.get('val-job_type', None)
            time_of_end = request.form.get('time_of_end', None)
            workplace = request.form.get('val-workplace', None)
            company_salary = request.form.get('val-company_salary', None)
            contact_person = request.form.get('val-contact_person', None)
            phone_number = request.form.get('val-phone_number', None)
            person_num = request.form.get('val-person_num', None)
            company_suggestions = request.form.get('val-company_suggestions', None)
            pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
            r = re.search(pattern, str(company_name).lower())
            if r:
                logger.warning('company_name一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form,username=current_user.username)
            r = re.search(pattern, str(brief_introduce).lower())
            if r:
                logger.warning('brief_introduce一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(address).lower())
            if r:
                logger.warning('address一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(job_type).lower())
            if r:
                logger.warning('job_type一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(time_of_end).lower())
            if r:
                logger.warning('time_of_end一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(workplace).lower())
            if r:
                logger.warning('workplace一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(company_salary).lower())
            if r:
                logger.warning('company_salary一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(contact_person).lower())
            if r:
                logger.warning('contact_person一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(phone_number).lower())
            if r:
                logger.warning('phone_number一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(person_num).lower())
            if r:
                logger.warning('person_num一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            r = re.search(pattern, str(company_suggestions).lower())
            if r:
                logger.warning('company_suggestions一栏检测到非法输入:' + r.group() + '可能为恶意攻击.')
                abort(405)
                return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form, username=current_user.username)
            dic={}
            dic["company_id"]=store_id
            dic["name"]=company_name
            dic["brief_introduce"]=brief_introduce
            dic["address"]=address
            dic["contact_person"]=contact_person
            dic["phone_number"]=phone_number
            dic["person_num"]=person_num
            dic["requirement"]=company_suggestions
            dic["upload_time"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dic["time_of_end"]=time_of_end
            dic["workplace"]=workplace
            dic["salary"]=company_salary
            dic["job_title"]=job_type
            dic["sid"]=current_user.id
            
            for value in dic.values():
                # print(value)
                if value=='':
                    return render_template('company_info_modification.html',flags=ALLOWSQLI,form=form,error='所有表格都为必填项，请重新填写！',username=current_user.username)
            if is_number(phone_number)==False:
                return render_template('company_info_modification.html',flags=ALLOWSQLI,form=form,error='电话号码格式错误，请重新填写！',username=current_user.username)
            if is_number(person_num)==False:
                return render_template('company_info_modification.html',flags=ALLOWSQLI,form=form,error='人数不是整数，请重新填写！',username=current_user.username)

            db.modify("insert into weboracle.company_info (company_id,name,brief_introduce,address,contact_person,phone_number,person_num,requirement,upload_time,time_of_end,workplace,salary,job_title,sid)values(:company_id,:name,:brief_introduce,:address,:contact_person,:phone_number,:person_num,:requirement,to_date(:upload_time,'yyyy-mm-dd hh24:mi:ss'),to_date(:time_of_end,'yyyy-mm-dd'),:workplace,:salary,:job_title,:sid)",dic,ALLOWSQLI=ALLOWSQLI)
            db.commit()
        except:
            db.rollback()
            return render_template('company_info_modification.html',flags=ALLOWSQLI,form=form,error='服务器发生错误，请重试！',username=current_user.username)
        finally:
            db.close()
        return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form,info='发布成功!',username=current_user.username)     
    return render_template('company_info_modification.html',flags=ALLOWSQLI, form=form,username=current_user.username)

@app.route('/manager_sql/<flags>',methods=['GET','POST'])
@login_required
@admin_required
def manager_sql(flags):
    global ALLOWSQLI
    print('a'+flags+'a')
    if flags=='False':
        ALLOWSQLI=False
    elif flags=='True':
        print(1536)
        ALLOWSQLI=True
    else:
        pass
    return redirect(url_for('index'))


if __name__ == "__main__":

    app.run(host='0.0.0.0',port=80,debug=True)

# from werkzeug.security import generate_password_hash
# from werkzeug.security import check_password_hash
# from flask_login import UserMixin
from oracledb import DataBase
from oracledb import Pool
from oracledb import DataBasePool
import uuid


pool=Pool()
pool.creatpool('webmanager','123456','192.168.137.135/oradb')
username='admin'
password='admin'
db=DataBasePool()
# 获取数据库连接
db.connect(pool)
cmdinfo=db.select("select * from weboracle.users")
for item in cmdinfo[1]:
    print(list(item))
cmdinfo=db.modify("delete weboracle.users where sid='1'")
db.commit()
print(cmdinfo)
# print([0])
# dic={}
# dic['username']=username
# d={}
# d['username']=username
# dic['password']=password
# db.modify("insert into users values('22','mxq','999','1')")
# temp_id=db.select('select password from users where username=:username',d)
# print(temp_id[1][0][0])
# cmdinfo=db.modify('update users set password=:password where username=:username',dic)
# db.commit()
# print(cmdinfo)

# import uuid
# u4=
# print(len(u4))
# print(type(u4))
# u41=u4
# print(u41)
# print(len(u41))
# print(unicode(uuid.uuid4()))

# import os
# print(type(os.urandom(24)))

# @app.route('/')
# @app.route('/main')
# @login_required
# def main():
#     return render_template('main.html', username=current_user.username)
# from werkzeug.security import generate_password_hash
# s=generate_password_hash('456')
# print(s)
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,BooleanField,PasswordField,SelectField,DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,EqualTo,Length,Regexp,NumberRange,Email,InputRequired

from oracledb import Pool
from oracledb import DataBasePool

# 创建数据库连接池
pool=Pool()
# pool链接数据库
pool.creatpool('webmanager','123456','192.168.71.139/oradb')

# 定义的表单类需要继承自flaskfrom
class LoginForm(FlaskForm):
    # ,Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'username must have only letters, numbers dots or underscores')
    username = StringField('用户名',validators=[DataRequired(),Length(1, 40)])
    password = PasswordField('密码',validators=[DataRequired(),Length(1, 40)])
    remember_me =BooleanField('记住我' ,default=False)
    # vail = RecaptchaField()
# 在wtf当中，每个域代表就是html中的元素，
# 比如StringField代表的是<input type="text">元素，
# 当然wtf的域还定义了一些特定功能，比如validators，
# 可以通过validators来对这个域的数据做检查，详细请参考wtf教程。

class RegisterForm(FlaskForm):
    email = StringField('邮箱',validators=[Email(message="邮箱格式不正确")])# message:错误提示信息
    username = StringField('用户名',validators=[InputRequired(message="您未输入")])
    password = PasswordField('密码',validators=[Length(min=6, max=12, message="密码长度必须为6至12位")])
   
    confirm_password = PasswordField('确认密码',validators=[EqualTo('password',message="两次密码输入必须一致")])

# 建库表单

# class BuildWarehouseForm(FlaskForm):
#     id = StringField('编号：' ,validators=[DataRequired()])
#     name = StringField('名称：' ,validators=[DataRequired()])
#     types = StringField('种类：' ,validators=[DataRequired()])
#     unit = StringField('单位：' ,validators=[DataRequired()])
#     company = StringField('厂商：' ,validators=[DataRequired()])

class SecrityForm(FlaskForm):
    pass

# class SalesDataEntry(FlaskForm):
#     def query_id():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select  identifier from stock ')
#             print(result)
#             # distinct
#             l=[]
#             for item in result[1]:
#                 l.append(item[0])
#             print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def query_name():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select name from stock ')
#             print(result)
#             l=[]
#             for item in result[1]:
#                 l.append(item[0])
#             print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def get_pk(obj):
#         return obj

#     ids = QuerySelectField(label= '编号：' ,validators=[DataRequired()],query_factory=query_id,get_pk=get_pk)
#     name = QuerySelectField(label='名称：' ,validators=[DataRequired()],query_factory=query_name,get_pk=get_pk)
#     unit = SelectField(label='单位：' ,validators=[DataRequired()],choices=[('kg','千克'),('bao','包'),('ping','瓶'),('dai','袋'),('ge','个'),('ban','版')])
#     number = StringField(label='数量：' ,validators=[DataRequired()])
#     price = StringField(label='单价：' ,validators=[DataRequired()])

# class InputInStorage(FlaskForm):
#     def query_id():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select identifier from store ')
#             # print(result)
#             l=[]
#             for item in result[1]:
#                 l.append(item[0])
#             print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def query_name():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select name from store ')
#             # print(result)
#             l=[]
#             for item in result[1]:
#                 l.append(item[0])
#             print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def get_pk(obj):
#         return obj

#     id =  QuerySelectField(label= '编号：' ,validators=[DataRequired()],query_factory=query_id,get_pk=get_pk)
#     name = QuerySelectField(label='名称：' ,validators=[DataRequired()],query_factory=query_name,get_pk=get_pk)
#     number = StringField(label='数量：' ,validators=[DataRequired()])
#     price = StringField(label='单价：' ,validators=[DataRequired()])
#     car_id = StringField(label='车号：',validators=[DataRequired()])

# class QuerySalesData(FlaskForm):
#     def query_id():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select identifier from salasdata ')
#             # print(result)
#             l=[]
#             for item in result[1][0]:
#                 l.append(item)
#             # print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def query_name():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select name from salasdata ')
#             # print(result)
#             l=[]
#             for item in result[1][0]:
#                 l.append(item)
#             # print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def query_company():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select distinct company from store ')
#             # print(result)
#             l=[]
#             for item in result[1][0]:
#                 l.append(item)
#             # print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def get_pk(obj):
#         return obj
    
#     id = QuerySelectField(label= '编号：' ,validators=[DataRequired()],query_factory=query_id,get_pk=get_pk)
#     name = QuerySelectField(label='名称：' ,validators=[DataRequired()],query_factory=query_name,get_pk=get_pk)
#     company =  QuerySelectField(label='公司：' ,validators=[DataRequired()],query_factory=query_company,get_pk=get_pk)
    
    
# class QueryStockInData(FlaskForm):
#     def query_id():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select identifier from buydata ')
#             # print(result)
#             l=[]
#             for item in result[1][0]:
#                 l.append(item)
#             # print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def query_name():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select name from buydata ')
#             # print(result)
#             l=[]
#             for item in result[1][0]:
#                 l.append(item)
#             # print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def query_car_id():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select carid from buydata ')
#             # print(result)
#             l=[]
#             for item in result[1][0]:
#                 l.append(item)
#             # print(l)
#             return l
#         except:
#             return ['服务器发生错误']

#     def get_pk(obj):
#         return obj

#     id = QuerySelectField(label='编号：' ,validators=[DataRequired()],query_factory=query_id,get_pk=get_pk)
#     name = QuerySelectField(label='名称：' ,validators=[DataRequired()],query_factory=query_name,get_pk=get_pk)
#     car_id =  QuerySelectField(label='车号：' ,validators=[DataRequired()],query_factory=query_car_id,get_pk=get_pk)

# class SalesReport(FlaskForm):
#     def query_id():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result1=database.select('select distinct identifier from salasdata ')
#             result2=database.select('select distinct identifier from buydata ')
#             # print(result)
#             l=set(result1[1][0]+result2[1][0])
#             # print(l)
#             return list(l)
#         except:
#             return ['服务器发生错误']

#     def query_name():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result1=database.select('select distinct name from salasdata ')
#             result2=database.select('select distinct name from buydata ')            # print(result)
#             l=set(result1[1][0]+result2[1][0])
#             return list(l)
#         except:
#             return ['服务器发生错误']

#     def query_company():
#         try:
#             database=DataBasePool()
#             database.connect(pool)
#             result=database.select('select distinct company from store ')
#             return list(result[1][0])
#         except:
#             return ['服务器发生错误']

#     def get_pk(obj):
#         return obj

#     id = QuerySelectField(label='编号：' ,validators=[DataRequired()],query_factory=query_id,get_pk=get_pk)
#     name = QuerySelectField(label='名称：' ,validators=[DataRequired()],query_factory=query_name,get_pk=get_pk)
#     company =QuerySelectField(label='公司：' ,validators=[DataRequired()],query_factory=query_company,get_pk=get_pk)
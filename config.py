host = "127.0.0.1"
port = "3306"
database = "ii"
username = "root"
password = "123456"
DB = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(username,password,host,port,database)
SQLALCHEMY_DATABASE_URI = DB

#设置数据库追踪信息,压制警告
SQLALCHEMY_TRACK_MODIFICATIONS = True


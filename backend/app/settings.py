# DB_FILE = 'test.db'
# DB_STRING = 'sqlite:///' + DB_FILE
import os

# DB_NAME = 'test'
DB_NAME = os.environ['DB_NAME']
# DB_USER = 'user'
DB_USER = 'root'
# DB_PASSWORD = 'asdqwe123'
DB_PASSWORD = os.environ['DB_PASS']
# DB_HOST = 'localhost'
DB_HOST = 'mysql'
DB_STRING = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME

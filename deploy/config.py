#coding:utf-8
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

DEBUG                = os.getenv('debug', default=True)

JSON_AS_ASCII        = os.getenv('json_as_ascii',default=False)
SECRET_KEY           = os.environ.get('secret_key') or 'nobody knows the password'
PER_PAGE             = os.getenv('per_page', default=10)

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True

IMAGE_UPLOAD_DIR = 'static/upload/'
UPLOAD_FOLDER = os.path.join(base_dir, 'app/static/upload/')

MAIL_SERVER          = os.getenv('mail_smtp',default='smtp.163.com')
MAIL_PORT            = os.getenv('mail_port',default=465)
MAIL_USE_SSL         = os.getenv('mail_use_ssl', default=True)
MAIL_USERNAME        = os.getenv('mail_user', default='weeklyreport.com')
MAIL_PASSWORD        = os.getenv('mail_pass', default='email_pass')

WR_MAIL_SUBJECT_PREFIX = '[WeeklyReport]'
WR_MAIL_SENDER       = os.getenv('mail_sender',default='weeklyreport <weeklyreport@163.com>')
DEPARTMENTS          = os.getenv('department', default='技术部,销售部').split(",")

DEFAULT_TITLE        = os.getenv('default_title', default="")
DEFAULT_CONTENT      = os.getenv('default_content', default="## 一、上周计划完成情况:\n\n- [x] DONE `Ctrl+J`\n\n## 二、计划外工作:\n\n## 三、重要问题:\n\n## 四、个人小结:\n\n## 五、下周计划:\n\n- [ ] TODO `Ctrl+Shift+J`\n\n")

DB_NAME = os.getenv("db_name", default='weeklyreport')
DB_USER = os.getenv("db_user", default='postgres')
DB_HOST = os.getenv("db_host", default='localhost')
DB_PORT = os.getenv("db_port", default='5432')
DB_PASS = os.getenv("db_pass", default='postgres')

# SQLALCHEMY_DATABASE_URI = 'postgresql://'+dbuser+':'+dbpass+'@'+dbhost+':'+dbport+'/'+dbname
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'wr_prd.sqlite')

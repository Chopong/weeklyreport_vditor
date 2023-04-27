import sys
import os
import time
import psycopg2
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logging.info("Checking if table 'django_migrations' exists.")
logging.info("If you want to skip this, just set the environment var")
logging.info("TAIGA_SKIP_DB_CHECK=True on docker-compose.yml on <backend> service.")

dbname = os.getenv("db_name", default='weeklyreport')
dbuser = os.getenv("db_user", default='postgres')
dbhost = os.getenv("db_host", default='localhost')
dbport = os.getenv("db_port", default='5432')
dbpass = os.getenv("db_pass", default='postgres')

CONNECTION_STRING = "dbname='{}' user='{}' host='{}' port='{}' password='{}'".format(
    dbname,
    dbuser,
    dbhost,
    dbport,
    dbpass
)
CONNECTION_STRING_SYS = "dbname='{}' user='{}' host='{}' port='{}' password='{}'".format(
    "postgres",
    dbuser,
    dbhost,
    dbport,
    dbpass
)
LIMIT_RETRIES = 5
SLEEP_INTERVAL = 5

def postgres_create_database(connection_string, dbname):
    try:
        connection = psycopg2.connect(connection_string)
        logging.warning("------------> Postgres login success.")
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{}'".format(dbname))
        if cursor.fetchone()[0]:
            try:
                cursor.execute('CREATE DATABASE {};'.format(dbname))
            except Exception as e:
                logging.warning('------------> {}'.format(e))
                cursor.execute("ROLLBACK")   #如果数据错误，执行回滚操作
                cursor.execute('CREATE DATABASE {};'.format(dbname))
            logging.warning("------------> Create {} success.".format(dbname))
        else:
            logging.warning("------------> DB: {} exsis.".format(dbname))
        cursor.close()
        connection.commit()
        connection.close()
    except psycopg2.OperationalError as e:
        logging.warning("------------> Err: {}".format(e))
        logging.warning("------------> Please check postgres user and pass.")
        return "Err"
    return "OK"

def postgres_connection(connection_string, retry_counter=1):
    try:
        connection = psycopg2.connect(connection_string)
    except psycopg2.OperationalError as e:
        if retry_counter > LIMIT_RETRIES:
            logging.error("CAN'T CONNECT TO POSTGRES")
            logging.error("Check your connection settings.")
            logging.error("Or increase (in docker-compose.yml):")
            logging.error(
                "TAIGA_DB_CHECK_SLEEP_INTERVAL / TAIGA_DB_CHECK_LIMIT_RETRIES."
            )
            logging.error("Exception messsage: {}".format(e))
            sys.exit(1)
        else:
            logging.warning("Can't connect to Postgres. Will try again...")
            time.sleep(SLEEP_INTERVAL)
            retry_counter += 1
            return postgres_connection(connection_string, retry_counter)
    return connection

postgres_create_database(CONNECTION_STRING_SYS, dbname)
cursor = postgres_connection(CONNECTION_STRING).cursor()
cursor.execute(
    "select exists(select * from information_schema.tables where table_name=%s)",
    ('users',)
)
if not cursor.fetchone()[0]:
    logging.info("So, it seems like it's the first time you run the <backend>")
    logging.info("service for taiga. Will try to:")
    logging.info("1) migrate DB; 2) load initial data; 3) compilemessages")
    print('missing_flask_users')

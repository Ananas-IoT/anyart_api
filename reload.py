import shutil
import mysql.connector
from mysql.connector import Error
from subprocess import call
import environ
from anyart_api.settings import DEV

# Initializing .devenv
env = environ.Env()
ENV_PATH = './anyart_api/.env'
environ.Env.read_env(ENV_PATH)

env_dict = { 
    'DATABASE_PASSWORD': 'DATABASE_PASSWORD', 
    'DATABASE_USER': 'DATABASE_USER', 
    'DATABASE_HOST': 'DATABASE_HOST', 
    'DATABASE_NAME': 'DATABASE_NAME'
}

if DEV:
    for key, value in env_dict.items():
        env_dict[key] = f'DEV_{value}'

# DB constants
DB_HOST = env(env_dict['DATABASE_HOST'])
DB_USER = env(env_dict['DATABASE_USER'])
DB_NAME = env(env_dict['DATABASE_NAME'])
DB_PASSWORD = env(env_dict['DATABASE_PASSWORD'])

# removing existing migration files
remove_dirs = ['authorization/migrations', 'workload/migrations', 'approval/migrations']
for remove_dir in remove_dirs:
    shutil.rmtree(remove_dir, ignore_errors=True)

# recreate db
my_SQL_connection = mysql.connector.connect(host=DB_HOST,
                                            user=DB_USER,
                                            database=DB_NAME,
                                            password=DB_PASSWORD)
sql_query = 'DROP DATABASE IF EXISTS anyart_db; CREATE DATABASE anyart_db;'
cursor = my_SQL_connection.cursor()
cursor.execute(sql_query)
cursor.close()

if my_SQL_connection.is_connected():
    my_SQL_connection.close()


# makemigrations
apps = ['authorization', 'workload', 'approval']
for app in apps:
    call(['python', 'manage.py', 'makemigrations', app])

# migrate
call(['python', 'manage.py', 'migrate'])

# loaddata
call(['python', 'manage.py', 'loaddata', 'authorization.json'])
call(['python', 'manage.py', 'loaddata', 'workload.json'])
call(['python', 'manage.py', 'loaddata', 'auth_group.json'])
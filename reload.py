import shutil
import mysql.connector
from mysql.connector import Error
from subprocess import call


remove_dirs = ['authorization/migrations', 'workload/migrations', 'approval/migrations']
for remove_dir in remove_dirs:
    shutil.rmtree(remove_dir, ignore_errors=True)

# recreate db
my_SQL_connection = mysql.connector.connect(host='localhost',
                                            user='admin',
                                            password='admin')
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
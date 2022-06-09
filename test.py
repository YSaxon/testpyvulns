import shlex
import subprocess
import sqlalchemy
def lookup_via_sqlalchemy(username):
    engine = sqlalchemy.create_engine('postgresql://scott:tiger@localhost/test')
    connection = engine.connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM users where username = '{username}'")
        result = cursor.fetchone()
    connection.close()
    return result

import sqlite3
def lookup_via_sqlite(username):
    db = sqlite3.connect(':memory:')
    cursor=db.execute(f"SELECT * FROM users where name = '{username}'")
    result=cursor.fetchone()
    return result


#fastapi webserver

from fastapi import FastAPI
fastapi_app = FastAPI()
@fastapi_app.get("/sqli/{username}")
def sqli_fastapi(username: str):
    a=lookup_via_sqlalchemy(username)
    b=lookup_via_sqlite(username)
    return a+"\n"+b

from fastapi import FastAPI
@fastapi_app.get("/xss/{xss}")
def xss_fastapi(xss: str):
    return "<script>"+xss+"</script>"

import os
@fastapi_app.get("/cmd/{cmd}")
def cmd_fastapi(cmd: str):
    a=os.system(cmd)
    b=subprocess.check_output(shlex.split(cmd))
    return a+"\n"+b


#flask webserver

from flask import Flask
flask_app = Flask(__name__)
@flask_app.route("/sqli/<username>")
def sqli_flask(username):
    a=lookup_via_sqlalchemy(username)
    b=lookup_via_sqlite(username)
    return a+"\n"+b

@flask_app.route("/xss/<xss>")
def xss_flask(xss):
    return "<script>"+xss+"</script>"

@flask_app.route("/cmd/<cmd>")
def cmd_flask(cmd):
    a=os.system(cmd)
    b=subprocess.check_output(shlex.split(cmd))
    return a+"\n"+b


# django webserver

import sys
from django.conf import settings
from django.urls import path
from django.core.management import execute_from_command_line
from django.http import HttpRequest, HttpResponse

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=sys.modules[__name__],
)

def sqli_django(request,username):
    a=lookup_via_sqlalchemy(username)
    b=lookup_via_sqlite(username)
    return a+"\n"+b

def xss_django(request,xss):
    return "<script>"+xss+"</script>"

def cmd_django(request,cmd):
    a=os.system(cmd)
    b=subprocess.check_output(shlex.split(cmd))
    return a+"\n"+b

urlpatterns = [
    path('sqli/<str:username>/', sqli_django),
    path('xss/<str:xss>/', xss_django),
    path('cmd/<str:cmd>/', cmd_django),
]


from hashlib import md5
def check_password(password: str):
    return md5(password.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
    flask_app.run()
    check_password("test")
    
    

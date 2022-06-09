import html
import os
import shlex
import sqlite3
import subprocess
import sys
import django
from django.conf import settings
from django.urls import include, path
from django.core.management import execute_from_command_line
from django.http import HttpRequest, HttpResponse
import sqlalchemy

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=sys.modules[__name__],
    SECRET_KEY='thisisthesecretkey',
)

def sqli_django(request,username):
    engine = sqlalchemy.create_engine('postgresql://scott:tiger@localhost/test')
    connection = engine.connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM users where username = '{username}'") #DOESNT CATCH!
        resulta = cursor.fetchone()
    connection.close()
    db = sqlite3.connect(':memory:')
    cursor=db.execute(f"SELECT * FROM users where name = '{username}'") #DOESNT CATCH!
    resultb=cursor.fetchone()
    db.close()
    return HttpResponse(html.escape(resulta+"\n"+resultb)) #WOULD CATCH XSS ONLY NOT SQLI

def xss_django(request,xss):
    return HttpResponse("<script>"+xss+"</script>") #DOESNT CATCH!

def cmd_django(request,cmd):
    a=os.system(cmd) #DOESNT CATCH!
    b=subprocess.check_output(shlex.split(cmd)) #DOESNT CATCH!
    return HttpResponse(f"{a}\n{b}")

urlpatterns = [
    path('sqli/<str:username>', sqli_django),
    path('xss/<str:xss>', xss_django),
    path('cmd/<str:cmd>', cmd_django),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
    
    
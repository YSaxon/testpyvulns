import html
import shlex
import sqlite3
import subprocess
import sqlalchemy
from fastapi import FastAPI
app = FastAPI()
@app.get("/sqli/{username}")
def sqli_fastapi(username: str):
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
    return html.escape(resulta+"\n"+resultb) #CATCHES XSS WITHOUT ESCAPE BUT NOT SQLI!

#this one is protected against by fastapi by default
# @app.get("/xss/{xss}")
# def xss_fastapi(xss: str):
#     return "<script>"+xss+"</script>"


import os
@app.get("/cmd/{cmd}")
def cmd_fastapi(cmd: str):
    a=os.system(cmd) #DOESNT CATCH!
    b=subprocess.check_output(shlex.split(cmd)) #DOESNT CATCH!
    return f"{a}\n{b}"
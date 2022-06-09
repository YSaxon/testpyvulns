import html
import os
import shlex
import sqlite3
import subprocess
from flask import Flask
import sqlalchemy
flask_app = Flask(__name__)
@flask_app.route("/sqli/<username>")
def sqli_flask(username):
    engine = sqlalchemy.create_engine('postgresql://scott:tiger@localhost/test')
    connection = engine.connect()
    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT * FROM users where username = '{username}'") #CATCHES
        resulta = cursor.fetchone()
    connection.close()
    db = sqlite3.connect(':memory:')
    cursor=db.execute(f"SELECT * FROM users where name = '{username}'") #DOES NOT CATCH!
    resultb=cursor.fetchone()
    db.close()
    return html.escape(resulta+"\n"+resultb)

@flask_app.route("/xss/<xss>")
def xss_flask(xss):
    return "<script>"+xss+"</script>" #CATCHES

@flask_app.route("/cmd/<cmd>")
def cmd_flask(cmd):
    a="" #os.system(cmd) #CATCHES
    b=subprocess.check_output(shlex.split(cmd)) #DOES NOT CATCH!
    return html.escape(a+"\n"+b)
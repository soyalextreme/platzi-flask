from flask import Flask, request, make_response, redirect, render_template, session, flash, url_for
import  unittest

from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users

app = create_app()


@app.route("/")
def index():
    user_ip = request.remote_addr
    res = make_response(redirect("/hello"))
    session["user_ip"] = user_ip
    return res


@app.route('/hello')
def hello():
    user_ip = session.get("user_ip")
    ctx = {"user_ip": user_ip, "username": None}
    return render_template("hello.html", **ctx)


@app.route('/error/fatal')
def error_fatal():
    raise(Exception('500 error'))
    

@app.cli.command()
def tests():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)



@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def server_down(error):
    return render_template('500.html', error=error)

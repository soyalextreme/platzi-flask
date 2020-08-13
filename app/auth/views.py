from flask import render_template, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user
from . import auth
from app.forms import LoginForm, RegisterForm
from app.firestore_service import get_user, put_user
from app.models import UserData, UserModel

@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    context = {
        "login_form" : login_form, 
        "username": None
    }
    if login_form.validate_on_submit(): 
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()["password"]

            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user) 
                flash("Iniciando sesion correctamente")
                return redirect(url_for("app.home"))
            else:
                flash("Informacion no coincide")
        else:
            flash("El usuario no existe")
    return render_template("login.html", **context)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Regresa pronto")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    context = {
        "username": None,
        "register_form": register_form
    }
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data
        c_password = register_form.c_password.data
        # verifiando las contrasenas
        if c_password != password:
            flash("Las contrasenas no coinciden")
        else:
            # revisando que exista el usuario
            user_doc = get_user(username)
            if user_doc.to_dict() is None:
                password_hash = generate_password_hash(password)
                user_data = UserData(username, password_hash)
                put_user(user_data)
                user = UserModel(user_data)
                login_user(user)
                flash(f"Bienvenido {username}")
                return redirect(url_for("app.home"))
            else:
                flash("El usuario ya existe")
    return render_template("register.html", **context)
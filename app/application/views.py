from flask import render_template, session, redirect, url_for, flash
from flask_login import current_user

from . import application 
from app.firestore_service import get_todos, put_todos, update_todo, delete_todo


from flask_login import login_required
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm


@application.route("/home", methods=["GET", "POST"])
@login_required
def home():
    username = current_user.id
    todos = get_todos(username)
    todo_form = TodoForm()
    delete_todo_form = DeleteTodoForm()
    update_todo_form = UpdateTodoForm()
    context = {
        "username": username,  
        "todos": todos,
        "todo_form": todo_form,
        "delete_todo_form": delete_todo_form,
        "update_todo_form": update_todo_form
    }
    if todo_form.validate_on_submit():
        put_todos(user_id=username, description=todo_form.description.data)
        flash("TODO registrada con exito")
        return redirect(url_for("app.home")) 

    return render_template("app/home.html", **context)


@application.route("/todo/delete/<todo_id>", methods=["POST"])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)
    return redirect(url_for("app.home"))


@application.route("/todo/update/<todo_id>/<int:done>", methods=["POST"])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id, todo_id, done)    
    return redirect(url_for("app.home"))


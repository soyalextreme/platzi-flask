import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)


db = firestore.client()


def get_users():
    return db.collection("users").get()

def get_user(user_id):
    # siempre usamos el meotod get por que si no solo trae uuna ref
    return db.collection("users").document(user_id).get()

def put_user(user_data):
    user_ref = db.collection("users").document(user_data.username)
    user_ref.set({"password": user_data.password})
    

# TODOS implementation
def get_todos(user_id):
    return db.collection("users").document(user_id).collection("todos").get()


def put_todos(user_id, description):
    todos_collection_ref = db.collection("users").document(user_id).collection("todos")
    todos_collection_ref.add({"description": description, "done": False})

def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    # todo_ref = db.collection("users").document(user_id).collection("todos").document(todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    # cast de numero a bool
    done = bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({"done": not done})

def _get_todo_ref(user_id, todo_id):
    return db.document(f"users/{user_id}/todos/{todo_id}")
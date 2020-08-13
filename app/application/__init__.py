
from flask import Blueprint

application = Blueprint("app", __name__, url_prefix="/app")


from . import views
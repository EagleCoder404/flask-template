from flask import Blueprint

bp = Blueprint("user_management", __name__, url_prefix="/user_management")

from flaskapp.user_management import routes
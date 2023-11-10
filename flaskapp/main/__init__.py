from flask import Blueprint, render_template
from flask_login import login_required
from flask_login import current_user

bp = Blueprint("main", __name__)


@bp.get("/")
@login_required
def index():
    return render_template("main/index.html")

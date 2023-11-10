from flask_login import LoginManager
from .service import get_user_by_id

login_manager = LoginManager()

login_manager.login_view = "user_management.login"

@login_manager.user_loader
def load_user(id: int):
    return get_user_by_id(id)

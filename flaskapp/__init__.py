from flask import Flask
from flaskapp.logger_config import *


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("flaskapp.config.DevelopmentConfig")

    from .sqlite_database import db
    db.init_app(app)

    from flaskapp.migration_config import migrate
    migrate.init_app(app, db)

    from flaskapp.mongo_database import mdb
    mdb.init_app(app)

    from flaskapp.user_management.auth import login_manager
    login_manager.init_app(app)

    from .user_management import bp as user_bp
    from .main import bp as main_bp
    from .blog import bp as blog_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp)


    return app

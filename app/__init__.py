from flask import Flask
from flask_login import LoginManager

from config import config
from app.models import db

login_manager = LoginManager()
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))


def create_app(environment_name=None):
    app = Flask(__name__)

    env_name = environment_name or "development"
    if env_name not in config:
        env_name = "default"

    app.config.from_object(config[env_name])
    db.init_app(app)
    login_manager.init_app(app)

    @app.route("/")
    def index():
        return "FocusFlow is running successfully."

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app

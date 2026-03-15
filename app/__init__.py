from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from app.config import Config, BASE_DIR

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    mail.init_app(app)

    from app.models import User, Admin
    from app.auth import auth_bp
    from app.main_routes import main_bp
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(main_bp, url_prefix="/")

    @login_manager.user_loader
    def load_user(id_str):
        if id_str.startswith("admin:"):
            return Admin.get_by_id_for_login(id_str)
        return User.get_by_id_for_login(id_str)

    with app.app_context():
<<<<<<< HEAD
=======
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
            instance_dir = BASE_DIR / "instance"
            instance_dir.mkdir(exist_ok=True)
>>>>>>> 2b75912e0ee3f30fc96cb1654973892719c3de21
        db.create_all()
        if Admin.query.filter_by(username="admin").first() is None:
            admin = Admin(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    return app

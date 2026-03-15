from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    occupation = db.Column(db.String(120), nullable=True)
    income = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return f"user:{self.id}"

    @staticmethod
    def get_by_id_for_login(id_str):
        if not id_str or not id_str.startswith("user:"):
            return None
        try:
            uid = int(id_str.split(":", 1)[1])
            return User.query.get(uid)
        except (ValueError, IndexError):
            return None


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return f"admin:{self.id}"

    @staticmethod
    def get_by_id_for_login(id_str):
        if not id_str or not id_str.startswith("admin:"):
            return None
        try:
            uid = int(id_str.split(":", 1)[1])
            return Admin.query.get(uid)
        except (ValueError, IndexError):
            return None


class OtpToken(db.Model):
    __tablename__ = "otp_tokens"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    otp = db.Column(db.String(10), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() >= self.expires_at

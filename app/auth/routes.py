import random
import string
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.auth import auth_bp
from app.config import Config
from app.models import User, Admin, OtpToken
from app.send_email import send_email as send_email_smtp


def generate_otp(length=6):
    return "".join(random.choices(string.digits, k=length))


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        email = (request.form.get("email") or "").strip().lower()
        age = request.form.get("age")
        occupation = (request.form.get("occupation") or "").strip()
        income = request.form.get("income")

        if not username or not password or not email:
            flash("Username, password and email are required.", "error")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("register.html")

        try:
            age = int(age) if age else None
        except ValueError:
            age = None
        try:
            income = float(income) if income else None
        except ValueError:
            income = None

        user = User(
            username=username,
            email=email,
            age=age,
            occupation=occupation or None,
            income=income,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("login.html")


@auth_bp.route("/login/request-otp", methods=["POST"])
def request_otp():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    username = (request.form.get("username") or "").strip()
    if not username:
        flash("Username is required.", "error")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No account found with this username.", "error")
        return redirect(url_for("auth.login"))
    # Send OTP to the user's registered email only
    email = user.email
    OtpToken.query.filter_by(email=email).delete()
    otp = generate_otp(Config.OTP_LENGTH)
    expires_at = datetime.utcnow() + timedelta(minutes=Config.OTP_EXPIRE_MINUTES)
    otp_token = OtpToken(email=email, otp=otp, expires_at=expires_at)
    db.session.add(otp_token)
    db.session.commit()

    mail_user = (current_app.config.get("MAIL_USERNAME") or "").strip()
    mail_pass = current_app.config.get("MAIL_PASSWORD") or ""
    if not mail_user or not mail_pass:
        flash("OTP cannot be sent. Mail is not configured. Please contact the administrator.", "error")
        return redirect(url_for("auth.login"))

    ok, err = send_email_smtp(
        to_email=email,
        subject="Your login OTP - Govt Schemes Advisor",
        body=f"Your one-time password is: {otp}\n\nThis OTP is for the application GOVT SCHEME ADVISOR.\nIt is valid for {Config.OTP_EXPIRE_MINUTES} minutes.\n\nIf you did not request this, please ignore this email.",
        mail_username=mail_user,
        mail_password=mail_pass,
        mail_server=current_app.config.get("MAIL_SERVER") or "smtp.gmail.com",
        mail_port=int(current_app.config.get("MAIL_PORT") or 587),
    )
    if not ok:
        flash(f"OTP could not be sent to your email: {err}", "error")
        return redirect(url_for("auth.login"))

    flash("OTP sent to your registered email. Check your inbox (and spam) and enter it below.", "success")
    return redirect(url_for("auth.verify_otp", email=email, username=username))


@auth_bp.route("/login/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    email = request.args.get("email") or request.form.get("email") or ""
    username = request.args.get("username") or request.form.get("username") or ""
    if not email or not username:
        flash("Session expired. Please start login again.", "error")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        otp_entered = (request.form.get("otp") or "").strip()
        if not otp_entered:
            flash("Please enter the OTP.", "error")
            return render_template("verify_otp.html", email=email, username=username)
        token = OtpToken.query.filter_by(email=email).order_by(OtpToken.expires_at.desc()).first()
        if not token or token.is_expired():
            flash("OTP expired. Please request a new one.", "error")
            return redirect(url_for("auth.login"))
        if token.otp != otp_entered:
            flash("Invalid OTP.", "error")
            return render_template("verify_otp.html", email=email, username=username)
        user = User.query.filter_by(username=username, email=email).first()
        if not user:
            flash("Account not found. Please try again.", "error")
            return redirect(url_for("auth.login"))
        OtpToken.query.filter_by(email=email).delete()
        db.session.commit()
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("verify_otp.html", email=email, username=username)


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("admin_login.html")
        admin = Admin.query.filter_by(username=username).first()
        if not admin or not admin.check_password(password):
            flash("Invalid admin credentials.", "error")
            return render_template("admin_login.html")
        login_user(admin)
        flash("Admin logged in successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("admin_login.html")


# Dashboard moved to main_bp


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/test-email", methods=["GET", "POST"])
def test_email():
    """Send a test email to check if mail config works. Use this to debug OTP not received."""
    mail_configured = bool(
        (current_app.config.get("MAIL_USERNAME") or "").strip()
        and current_app.config.get("MAIL_PASSWORD")
    )
    mail_user = (current_app.config.get("MAIL_USERNAME") or "").strip()
    hint = ""
    if request.method == "POST":
        to_email = (request.form.get("email") or "").strip().lower()
        if not to_email:
            flash("Enter an email address.", "error")
            return render_template("test_email.html", mail_configured=mail_configured, mail_user=mail_user, hint=hint)
        if not mail_configured:
            flash("Mail is not configured. Add MAIL_USERNAME and MAIL_PASSWORD to .env in the project folder.", "error")
            return render_template("test_email.html", mail_configured=mail_configured, mail_user=mail_user, hint=hint)
        ok, err = send_email_smtp(
            to_email=to_email,
            subject="Test email - Govt Schemes Advisor",
            body="If you got this, OTP emails will work. Check your spam folder if OTP doesn't arrive.",
            mail_username=mail_user,
            mail_password=current_app.config.get("MAIL_PASSWORD") or "",
            mail_server=current_app.config.get("MAIL_SERVER") or "smtp.gmail.com",
            mail_port=int(current_app.config.get("MAIL_PORT") or 587),
        )
        if ok:
            flash(f"Test email sent to {to_email}. Check inbox and spam.", "success")
        else:
            hint = err
            flash("Send failed. See error below.", "error")
    return render_template("test_email.html", mail_configured=mail_configured, mail_user=mail_user, hint=hint)

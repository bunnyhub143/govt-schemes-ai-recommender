"""
Send email using smtplib (works reliably with Gmail App Password).
Use this for OTP and test emails instead of Flask-Mail.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body, mail_username, mail_password, mail_server="smtp.gmail.com", mail_port=587):
    """
    Send a plain-text email. Returns (True, None) on success, (False, error_message) on failure.
    For Gmail: use App Password (https://myaccount.google.com/apppasswords), not your normal password.
    """
    if not mail_username or not mail_password:
        return False, "MAIL_USERNAME and MAIL_PASSWORD must be set in .env"
    mail_password = mail_password.strip().replace(" ", "")  # App passwords sometimes pasted with spaces
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = mail_username
        msg["To"] = to_email
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(mail_server, mail_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mail_username, mail_password)
            server.sendmail(mail_username, [to_email], msg.as_string())
        return True, None
    except smtplib.SMTPAuthenticationError as e:
        return False, "Gmail login failed. Use an App Password (not your normal password). See: https://myaccount.google.com/apppasswords - " + str(e)
    except smtplib.SMTPRecipientsRefused as e:
        return False, "Invalid recipient: " + str(e)
    except smtplib.SMTPException as e:
        return False, "SMTP error: " + str(e)
    except Exception as e:
        return False, str(e)

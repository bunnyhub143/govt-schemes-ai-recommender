import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv_manual(env_path):
    """Load .env by reading file (avoids path/order issues with dotenv)."""
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key, value = key.strip(), value.strip().strip('"').strip("'")
                    if key:
                        os.environ[key] = value
    except Exception:
        pass


# Load .env from project root (folder containing run.py / app/)
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    _load_dotenv_manual(_env_file)
else:
    # Also try current working directory (e.g. if run from IDE)
    _load_dotenv_manual(Path(os.getcwd()) / ".env")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + str(BASE_DIR / "instance" / "schemes.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail (for OTP) - set in env or .env
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.gmail.com"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or ""
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or ""
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or MAIL_USERNAME

    OTP_EXPIRE_MINUTES = 10
    OTP_LENGTH = 6

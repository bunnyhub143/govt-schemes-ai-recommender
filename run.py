"""
Run the AI Govt Schemes Advisor app.
Create virtualenv, install requirements, then: python run.py
To send OTP to registered email: create .env with MAIL_USERNAME and MAIL_PASSWORD (see SETUP_EMAIL.md).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (same folder as run.py) so mail config is always found
_project_root = Path(__file__).resolve().parent
load_dotenv(_project_root / ".env")

from app import create_app

app = create_app()

if __name__ == "__main__":
    mail_ok = bool((app.config.get("MAIL_USERNAME") or "").strip() and app.config.get("MAIL_PASSWORD"))
    print("Mail configured for OTP:", "YES" if mail_ok else "NO (add .env with MAIL_USERNAME and MAIL_PASSWORD)")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

# AI Govt Schemes Advisor – Auth Setup

## What’s implemented

- **User registration** – Username, password, email, age, occupation, income  
- **User login** – Username + email → OTP sent to email → user enters OTP to log in  
- **Admin login** – Username + password (default: `admin` / `admin123`)  
- **Dashboard** – After login, user or admin sees a simple dashboard  

## How to run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   python run.py
   ```
   Open http://127.0.0.1:5000

3. **Email (OTP)**  
   For “Send OTP to Email” to work, set mail settings. Copy `.env.example` to `.env` and set:
   - `MAIL_USERNAME` – e.g. your Gmail
   - `MAIL_PASSWORD` – Gmail “App password” (not your normal password)

   Without these, registration and admin login still work; only OTP sending will fail.

## Pages

| URL            | Description                    |
|----------------|--------------------------------|
| `/register`    | New user sign up               |
| `/login`       | User login (username + email → OTP) |
| `/admin/login` | Admin login (username + password)   |
| `/dashboard`   | After login (requires login)   |
| `/logout`      | Log out                        |

## Default admin

- **Username:** `admin`  
- **Password:** `admin123`  

Change this in production.

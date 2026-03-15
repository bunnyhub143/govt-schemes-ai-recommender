# Send OTP to Registered Email (Gmail)

Right now the app says **"Mail not configured"** because it doesn't have your email credentials. Follow these steps to send OTP to the user's registered email (e.g. bunny143256a@gmail.com).

---

## Step 1: Turn on 2-Step Verification (Gmail)

1. Open [Google Account](https://myaccount.google.com/) → **Security**.
2. Under "How you sign in to Google", click **2-Step Verification**.
3. Turn it **On** and complete the steps.

---

## Step 2: Create an App Password

1. In the same **Security** page, open **2-Step Verification**.
2. Scroll to **App passwords** (or go to [App passwords](https://myaccount.google.com/apppasswords)).
3. Select app: **Mail**, device: **Other** (type "Govt Schemes Advisor").
4. Click **Generate**.
5. Copy the **16-character password** (e.g. `abcd efgh ijkl mnop`). You'll use it in Step 3 (no spaces).

---

## Step 3: Create `.env` in the project folder

1. Open the project folder:  
   `c:\Users\VAMSHI\OneDrive\Documents\3-2\schemes project`

2. Copy the file **`.env.example`** and paste it in the same folder.

3. Rename the copy to **`.env`** (exactly, no .example).

4. Open **`.env`** in Notepad or Cursor and set:

   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=bunny143256a@gmail.com
   MAIL_PASSWORD=abcdefghijklmnop
   MAIL_DEFAULT_SENDER=bunny143256a@gmail.com
   ```

   - **MAIL_USERNAME** = the Gmail address that will *send* the OTP (can be the same as the user's registered mail or another Gmail).
   - **MAIL_PASSWORD** = the **App Password** from Step 2 (16 letters, no spaces).

5. Save the file.

---

## Step 4: Restart the app

1. Stop the running server (Ctrl+C in the terminal).
2. Start it again:
   ```bash
   python run.py
   ```
3. Try **Login** → enter username → **Send OTP to Registered Email**.

The OTP will be sent to the user's **registered email** (the one they used when they registered). Check that inbox (and spam folder) for the 6-digit code.

---

## If it still doesn’t send

- Make sure **.env** is in the same folder as **run.py** (project root).
- Make sure you’re using an **App Password**, not your normal Gmail password.
- If you see an error message on the page, it will usually say what went wrong (e.g. wrong password, less secure app).

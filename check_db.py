"""Quick script to view all PostgreSQL table records."""
import psycopg2

conn = psycopg2.connect("postgresql://postgres:501%40Bunny@localhost:5432/schemes_db")
cur = conn.cursor()

# Show users
cur.execute("SELECT id, username, email, age, occupation, income, created_at FROM users")
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
print(f"--- USERS ({len(rows)} records) ---")
print("Columns:", cols)
for row in rows:
    print(row)

# Show admins
cur.execute("SELECT id, username FROM admins")
rows = cur.fetchall()
print(f"\n--- ADMINS ({len(rows)} records) ---")
for row in rows:
    print(row)

# Show otp_tokens
cur.execute("SELECT id, email, otp, expires_at FROM otp_tokens")
rows = cur.fetchall()
print(f"\n--- OTP_TOKENS ({len(rows)} records) ---")
for row in rows:
    print(row)

conn.close()

import psycopg2

DATABASE_URL = "postgresql://postgres:serfglobalauth@db.uyanofddigzsbpxarrci.supabase.co:5432/postgres"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to the database successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)

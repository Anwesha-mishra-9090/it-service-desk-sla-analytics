import psycopg2
from urllib.parse import quote_plus

# Test with your password
password = "Badal@143"

try:
    # Try with encoded password
    encoded_password = quote_plus(password)
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password=password,  # Use the actual password, not encoded
        database="service_desk"
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure PostgreSQL is running")
    print("2. Check if password 'Badal@143' is correct")
    print("3. Verify database 'service_desk' exists in pgAdmin4")
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 50)
print("Testing IT Service Desk Database Connection")
print("=" * 50)

try:
    # Connect to database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'service_desk')
    )
    
    cursor = conn.cursor()
    
    # Test 1: Check connection
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ Connected to: {version[0][:50]}...")
    
    # Test 2: Check tickets table
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_name = 'tickets'
    """)
    table_exists = cursor.fetchone()[0]
    if table_exists:
        print("✅ Tickets table exists")
    else:
        print("❌ Tickets table not found")
    
    # Test 3: Count tickets
    cursor.execute("SELECT COUNT(*) FROM tickets")
    ticket_count = cursor.fetchone()[0]
    print(f"✅ Total tickets in database: {ticket_count}")
    
    # Test 4: Get sample tickets
    if ticket_count > 0:
        cursor.execute("""
            SELECT id, title, status, priority 
            FROM tickets 
            LIMIT 3
        """)
        tickets = cursor.fetchall()
        print("\n📋 Sample tickets:")
        for ticket in tickets:
            print(f"   - Ticket #{ticket[0]}: {ticket[1]} [{ticket[2]}] Priority: {ticket[3]}")
    
    conn.close()
    print("\n" + "=" * 50)
    print("✅ Database is ready! You can run the application.")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if PostgreSQL is running")
    print("2. Verify .env file credentials")
    print("3. Make sure database 'service_desk' exists")
import requests
import json

print("Testing Dashboard API...")

try:
    # Test dashboard stats
    response = requests.get('http://localhost:5000/api/dashboard/stats')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Dashboard API Working!")
        print(f"Total Tickets: {data.get('summary', {}).get('total_tickets', 0)}")
        print(f"Open Tickets: {data.get('summary', {}).get('open_tickets', 0)}")
        print(f"SLA Compliance: {data.get('sla_metrics', {}).get('compliance_rate', 0)}%")
    else:
        print(f"\n❌ Error: {response.text}")
        
except Exception as e:
    print(f"\n❌ Connection Error: {e}")
    print("Make sure the app is running on http://localhost:5000")
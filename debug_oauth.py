import os
import requests
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

print("=== RAW OAUTH DIAGNOSTIC ===")

# 1. Get Variables
u = os.getenv("SF_USERNAME")
p = os.getenv("SF_PASSWORD")
t = os.getenv("SF_TOKEN")
ck = os.getenv("SF_CONSUMER_KEY")
cs = os.getenv("SF_CONSUMER_SECRET")

# 2. Check for "Poison" Characters (Spaces/Quotes)
print(f"Username: '{u}'")
print(f"Consumer Key Length: {len(ck) if ck else 'None'}")
print(f"Consumer Secret Length: {len(cs) if cs else 'None'}")

if ck and (ck.startswith('"') or ck.startswith("'")):
    print("ERROR: Your Consumer Key in .env has quotes! Remove them.")
if cs and (cs.startswith('"') or cs.startswith("'")):
    print("ERROR: Your Consumer Secret in .env has quotes! Remove them.")

# 3. Attempt Raw Login
login_url = "https://login.salesforce.com/services/oauth2/token"
payload = {
    "grant_type": "password",
    "client_id": ck,
    "client_secret": cs,
    "username": u,
    "password": p + t  # Concatenate Password + Token
}

print("\nSending Request to Salesforce...")
response = requests.post(login_url, data=payload)

# 4. Analyze Result
if response.status_code == 200:
    print("\nSUCCESS! We got an Access Token.")
    print("This proves your Keys and Password are correct.")
    print("The issue is inside the simple-salesforce library or usage.")
else:
    print(f"\nFAILED (Status {response.status_code})")
    print(f"Response: {response.text}")
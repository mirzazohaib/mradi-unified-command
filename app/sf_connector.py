import os
import requests
from simple_salesforce import Salesforce
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

def get_skysec_connection():
    """
    Establishes a secure connection using a 'Manual Override' OAuth handshake.
    """
    print("[INFO] SkySec Uplink: Initiating Manual OAuth 2.0 Handshake...")

    # ---------------------------------------------------------
    # STEP 1: Get the Token manually (Since we know this works)
    # ---------------------------------------------------------
    login_url = "https://login.salesforce.com/services/oauth2/token"
    
    payload = {
        "grant_type": "password",
        "client_id": os.getenv("SF_CONSUMER_KEY"),
        "client_secret": os.getenv("SF_CONSUMER_SECRET"),
        "username": os.getenv("SF_USERNAME"),
        "password": os.getenv("SF_PASSWORD") + os.getenv("SF_TOKEN")
    }

    try:
        response = requests.post(login_url, data=payload)
        auth_data = response.json()
        
        if response.status_code != 200:
            print(f"\n[CRITICAL] Auth Request Failed: {auth_data}")
            return None
            
        access_token = auth_data.get('access_token')
        instance_url = auth_data.get('instance_url')
        
        print(f"[INFO] Access Token Acquired. Instance: {instance_url}")

        # ---------------------------------------------------------
        # STEP 2: Inject Token into Simple-Salesforce
        # ---------------------------------------------------------
        sf = Salesforce(
            instance_url=instance_url,
            session_id=access_token
        )
        return sf

    except Exception as e:
        print(f"[ERROR] Connection failed during handshake: {e}")
        return None

if __name__ == "__main__":
    # Test the connection
    sf = get_skysec_connection()
    
    if sf:
        print("[SUCCESS] Connected to SkySec Database.")
        
        # Query the mission
        query = """
        SELECT Id, Name, Region__c, Readiness_Status__c, Assigned_Asset__r.Name 
        FROM Demo_Mission__c
        LIMIT 5
        """
        
        try:
            results = sf.query(query)
            print(f"\n[SEARCH] Found {results['totalSize']} Active Mission(s):")
            
            for record in results['records']:
                # Safe fetching of related object data
                asset_info = record.get('Assigned_Asset__r')
                asset_name = asset_info['Name'] if asset_info else "Unassigned"
                
                print(f"   -----------------------------")
                print(f"   Mission: {record['Name']}")
                print(f"   Region:  {record['Region__c']}")
                print(f"   Status:  {record['Readiness_Status__c']}")
                print(f"   Asset:   {asset_name}")
                
        except Exception as e:
            print(f"[ERROR] Query Error: {e}")
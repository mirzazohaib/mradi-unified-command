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
    # Debug: Print loaded variables (First 2 chars only for security)
    # print(f"DEBUG: User={os.getenv('SF_USERNAME')[:2]}***")
    
    login_url = "https://login.salesforce.com/services/oauth2/token"
    
    # SAFEGUARD: Handle None values if .env is not loading correctly
    password = os.getenv("SF_PASSWORD") or ""
    token = os.getenv("SF_TOKEN") or ""
    consumer_key = os.getenv("SF_CONSUMER_KEY") or ""
    consumer_secret = os.getenv("SF_CONSUMER_SECRET") or ""
    username = os.getenv("SF_USERNAME") or ""

    payload = {
        "grant_type": "password",
        "client_id": consumer_key,
        "client_secret": consumer_secret,
        "username": username,
        "password": password + token 
    }

    try:
        response = requests.post(login_url, data=payload)
        auth_data = response.json()
        
        if response.status_code != 200:
            print(f"\n[CRITICAL] Auth Request Failed: {auth_data}")
            return None
            
        access_token = auth_data.get('access_token')
        instance_url = auth_data.get('instance_url')
        
        # Inject Token into Simple-Salesforce
        sf = Salesforce(
            instance_url=instance_url,
            session_id=access_token
        )
        return sf

    except Exception as e:
        print(f"[ERROR] Connection failed during handshake: {e}")
        return None

def get_active_missions():
    """
    Connects to Salesforce, fetches missions, and returns them as a clean list.
    """
    sf = get_skysec_connection()
    if not sf:
        # Return an empty list instead of crashing if connection fails
        return []

    query = """
    SELECT Id, Name, Region__c, Readiness_Status__c, Assigned_Asset__r.Name 
    FROM Demo_Mission__c
    LIMIT 10
    """
    
    try:
        results = sf.query(query)
        formatted_missions = []
        
        for record in results['records']:
            asset_info = record.get('Assigned_Asset__r')
            asset_name = asset_info['Name'] if asset_info else "Unassigned"
            
            formatted_missions.append({
                "id": record['Id'],
                "mission_name": record['Name'],
                "region": record['Region__c'],
                "status": record['Readiness_Status__c'],
                "asset": asset_name
            })
            
        return formatted_missions

    except Exception as e:
        print(f"[ERROR] fetching missions: {e}")
        return []

if __name__ == "__main__":
    # Test locally
    print("Testing Mission Fetch...")
    missions = get_active_missions()
    print(f"Found {len(missions)} missions")

def update_mission_status_in_sf(mission_id: str, new_status: str):
    """
    Connects to Salesforce and updates the Readiness_Status__c of a mission.
    """
    sf = get_skysec_connection()
    if not sf:
        return False

    try:
        # Use simple-salesforce to update the specific record
        sf.Demo_Mission__c.update(mission_id, {
            'Readiness_Status__c': new_status
        })
        return True
    except Exception as e:
        print(f"[ERROR] updating mission {mission_id}: {e}")
        return False
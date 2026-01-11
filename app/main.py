from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

# Internal module imports
from app.sf_connector import get_active_missions, update_mission_status_in_sf
from app.risk_engine import calculate_risk_score  # MRADI-5
from app.audit_logger import log_transaction       # MRADI-6

app = FastAPI(title="SkySec Unified Command API", version="1.0")

# Pydantic model for the update request body
class StatusUpdate(BaseModel):
    status: str

@app.get("/")
def read_root():
    return {"message": "SkySec Uplink Online. System Ready."}

# UPDATED: Added Risk Scoring and Audit Logging (MRADI-5 & MRADI-6)
@app.get("/api/missions")
def read_missions(region: Optional[str] = Query(None, description="Filter missions by region")):
    print(f"API Request received: Fetching missions for region: {region or 'All'}")
    
    # 1. Fetch raw data from Salesforce
    data = get_active_missions()
    
    # 2. Filter by region if requested
    if region:
        data = [m for m in data if m['region'].lower() == region.lower()]
    
    # 3. Enrich data with Risk Intelligence and Log actions
    for mission in data:
        # Calculate risk (Complexity is mocked at 3 for this sprint)
        risk_assessment = calculate_risk_score(mission['status'], complexity=3)
        
        # Inject the assessment into the mission object
        mission['risk_assessment'] = risk_assessment
        
        # Log the transaction for audit compliance (MRADI-6)
        log_transaction(
            action="RISK_CALCULATION",
            mission_id=mission['id'],
            details=f"Score: {risk_assessment['score']} | Level: {risk_assessment['risk_level']}"
        )
        
    return {"count": len(data), "missions": data}

# PATCH endpoint to update status (MRADI-4)
@app.patch("/api/missions/{mission_id}")
def update_mission(mission_id: str, update: StatusUpdate):
    success = update_mission_status_in_sf(mission_id, update.status)
    
    if not success:
        # Log failed update attempt
        log_transaction("UPDATE_FAILED", mission_id, f"Attempted status: {update.status}")
        raise HTTPException(status_code=500, detail="Failed to update Salesforce record")
    
    # Log successful update
    log_transaction("UPDATE_SUCCESS", mission_id, f"New status: {update.status}")
    
    return {"status": "success", "mission_id": mission_id, "new_status": update.status}
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.sf_connector import get_active_missions, update_mission_status_in_sf

app = FastAPI(title="SkySec Unified Command API", version="1.0")

# Pydantic model for the update request body
class StatusUpdate(BaseModel):
    status: str

@app.get("/")
def read_root():
    return {"message": "SkySec Uplink Online. System Ready."}

# UPDATED: Added optional region filtering (MRADI-3)
@app.get("/api/missions")
def read_missions(region: Optional[str] = Query(None, description="Filter missions by region")):
    print(f"API Request received: Fetching missions for region: {region or 'All'}")
    data = get_active_missions()
    
    if region:
        # Filter the list based on the region parameter
        data = [m for m in data if m['region'].lower() == region.lower()]
        
    return {"count": len(data), "missions": data}

# NEW: PATCH endpoint to update status (MRADI-4)
@app.patch("/api/missions/{mission_id}")
def update_mission(mission_id: str, update: StatusUpdate):
    success = update_mission_status_in_sf(mission_id, update.status)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update Salesforce record")
    
    return {"status": "success", "mission_id": mission_id, "new_status": update.status}
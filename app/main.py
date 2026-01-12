from fastapi import FastAPI, Query, HTTPException, Header # SECURITY: Header required for auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from pydantic import BaseModel

# Internal module imports
from app.sf_connector import get_active_missions, update_mission_status_in_sf
from app.risk_engine import calculate_risk_score   
from app.audit_logger import log_transaction       # GOVERNANCE: Audit capability
from app.system_monitor import get_system_health, toggle_service_status

app = FastAPI(title="SkySec Unified Command API", version="1.3")

# 1. VISUALIZATION LAYER
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- PYDANTIC MODELS (Data Validation) ---
class StatusUpdate(BaseModel):
    status: str

class ServiceControl(BaseModel):
    service_name: str
    active: bool

# 2. ENTRY POINT
@app.get("/")
async def read_root():
    return FileResponse('app/static/index.html')

# ==========================================
# STRATEGIC LAYER (Salesforce Missions)
# ==========================================
@app.get("/api/missions")
def read_missions(region: Optional[str] = Query(None)):
    data = get_active_missions()
    if region:
        data = [m for m in data if m['region'].lower() == region.lower()]
    
    for mission in data:
        # INTELLIGENCE: Dynamic risk calculation
        risk_assessment = calculate_risk_score(mission['status'], complexity=3)
        mission['risk_assessment'] = risk_assessment
        
        # GOVERNANCE: Log access to mission data
        log_transaction("RISK_CALCULATION", mission['id'], f"Score: {risk_assessment['score']}")
        
    return {"count": len(data), "missions": data}

@app.patch("/api/missions/{mission_id}")
def update_mission(mission_id: str, update: StatusUpdate):
    success = update_mission_status_in_sf(mission_id, update.status)
    if not success:
        log_transaction("UPDATE_FAILED", mission_id, f"Target: {update.status}")
        raise HTTPException(status_code=500, detail="Salesforce Update Failed")
    
    log_transaction("UPDATE_SUCCESS", mission_id, f"New status: {update.status}")
    return {"status": "success"}

# ==========================================
# OPERATIONAL LAYER (Telemetry & Sim)
# ==========================================

@app.get("/api/system/status")
def read_system_status():
    """Provides real-time telemetry for the HUD."""
    return get_system_health()

@app.post("/api/system/control")
def control_service(
    cmd: ServiceControl, 
    x_demo_key: str = Header(None) # SECURITY: Require API Key via Header
):
    """
    Simulate service failures. Protected by Header Auth.
    """
    # 1. SECURITY CHECK
    if x_demo_key != "ALLOW_SIM":
        log_transaction("SECURITY_ALERT", "SYSTEM", "Unauthorized control attempt")
        raise HTTPException(status_code=403, detail="Unauthorized: Invalid Key")

    # 2. EXECUTE
    success = toggle_service_status(cmd.service_name, cmd.active)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # 3. AUDIT LOG (GOVERNANCE)
    # Critical: Record who changed the system state and when.
    action = "SERVICE_RESTORED" if cmd.active else "SERVICE_OUTAGE_SIMULATED"
    log_transaction(action, "SYSTEM_OP", f"Manual toggle of {cmd.service_name}")
        
    return {"success": success, "new_state": "ONLINE" if cmd.active else "OFFLINE"}
import psutil
import time

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================

# SYSTEMS ENG: Explicit flag to signal we are in a Simulation/Training environment.
DEMO_MODE = True 

# SAFETY INTERLOCK: Prevent accidental deployment to Production.
# If this code is ever deployed with DEMO_MODE=False, it will crash intentionally
# because it lacks the Secure Service Discovery required for Live Ops.
assert DEMO_MODE is True, "CRITICAL ERROR: Live mode requires secure service discovery."

# THRESHOLDS & TUNING
# Defined as constants to prevent "magic numbers" deep in the logic.
CPU_CRITICAL_THRESHOLD = 90
MEMORY_CRITICAL_THRESHOLD = 95
DEBOUNCE_LIMIT = 3  # Seconds of sustained load required to trigger alert

# ==========================================
# STATE TRACKING (Global Mutable State)
# ==========================================

# NOTE: Registry simulates external service discovery (Consul/K8s).
service_registry = {
    "MCx Core": {"status": "ONLINE", "critical": True},       
    "Video Gateway": {"status": "ONLINE", "critical": False}, 
    "Secure Uplink": {"status": "ONLINE", "critical": True}   
}

# GOVERNANCE: Provenance Tracking
# We track specific variables to detect state changes.
_last_readiness = "READY"
_last_cause = "System Startup" # Critical: Tracks the *reason* for the state

_transition_log = {
    "from": "INIT",
    "to": "READY",
    "cause": "System Startup",
    "timestamp": time.strftime("%H:%M:%SZ", time.gmtime())
}

# SYSTEMS ENG: Debounce Counters (Anti-Flap Logic)
_cpu_breach_count = 0
_mem_breach_count = 0

def get_system_health():
    """
    Aggregates Hardware Telemetry, Simulated Service Status, and State Provenance.
    """
    global _last_readiness, _last_cause, _transition_log, _cpu_breach_count, _mem_breach_count
    
    # 1. Acquire Hardware Telemetry (Real-time)
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    
    # 2. Analyze Service Health (Smart Logic)
    current_readiness = "READY"
    failed_critical = []
    failed_degraded = []

    for name, data in service_registry.items():
        if data["status"] != "ONLINE":
            if data["critical"]:
                failed_critical.append(name)
                current_readiness = "NOT_READY"
            else:
                failed_degraded.append(name)
                # If only non-critical services are down, we are DEGRADED 
                if current_readiness != "NOT_READY":
                    current_readiness = "DEGRADED"

    # 3. Hardware Checks (With Debounce Logic)
    # SYSTEMS ENG: Rolling counts prevent transient spikes (1s) from triggering alerts.
    
    # CPU Logic
    if cpu > CPU_CRITICAL_THRESHOLD:
        _cpu_breach_count += 1
    else:
        _cpu_breach_count = 0 
        
    if _cpu_breach_count >= DEBOUNCE_LIMIT:
        failed_degraded.append(f"CPU Critical ({cpu}%)")
        if current_readiness != "NOT_READY":
            current_readiness = "DEGRADED"

    # RAM Logic
    if memory > MEMORY_CRITICAL_THRESHOLD:
        _mem_breach_count += 1
    else:
        _mem_breach_count = 0
        
    if _mem_breach_count >= DEBOUNCE_LIMIT:
        failed_degraded.append(f"RAM Critical ({memory}%)")
        if current_readiness != "NOT_READY":
            current_readiness = "DEGRADED"

    # 4. DETERMINE CAUSE STRING
    # We calculate this BEFORE checking for transitions.
    # This ensures we catch changes like "MCx Down" -> "Secure Link Down" (both are Red).
    current_cause = "Unknown"
    
    if current_readiness == "NOT_READY":
        if failed_critical:
            current_cause = f"{failed_critical[0]} unavailable"
            if len(failed_critical) > 1:
                current_cause = "Multiple Critical Failures"
        else:
            current_cause = "Critical Failure"
            
    elif current_readiness == "DEGRADED":
        if failed_degraded:
            current_cause = f"{failed_degraded[0]} unavailable"
        else:
            current_cause = "Performance Degraded"
            
    elif current_readiness == "READY":
        current_cause = "All Systems Nominal"

    # 5. PROVENANCE LOGIC (State Transition Detection)
    # Update log if Readiness Level changes OR if the Root Cause changes.
    if current_readiness != _last_readiness or current_cause != _last_cause:
        
        _transition_log = {
            "from": _last_readiness,
            "to": current_readiness,
            "cause": current_cause,
            "timestamp": time.strftime("%H:%M:%SZ", time.gmtime())
        }
        
        # Update State Memory
        _last_readiness = current_readiness
        _last_cause = current_cause

    # Flatten reasons for the Dashboard UI list
    all_reasons = [f"{x} unavailable" for x in failed_critical] + \
                  [f"{x} unavailable" for x in failed_degraded]

    return {
        "mode": "SIMULATION", 
        "hardware": {
            "cpu_usage": cpu,
            "memory_usage": memory,
        },
        "services": service_registry,
        "readiness": current_readiness,
        "readiness_reasons": all_reasons,
        "last_transition": _transition_log,
        # GOVERNANCE: Use UTC (gmtime) for global audit consistency
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def toggle_service_status(service_name: str, active: bool):
    """
    Simulation Tool: Allows the dashboard to intentionally break/fix a service.
    """
    if service_name in service_registry:
        service_registry[service_name]["status"] = "ONLINE" if active else "OFFLINE"
        return True
    return False
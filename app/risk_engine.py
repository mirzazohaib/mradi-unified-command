def calculate_risk_score(readiness_status: str, complexity: int) -> dict:
    """
    MRADI-5: Composite Risk Scoring logic.
    Returns a score (0-100) and a risk category.
    """
    # Base score based on status
    status_weights = {
        "READY": 10,
        "DEGRADED": 50,
        "NOT_READY": 90
    }
    
    base_score = status_weights.get(readiness_status.upper(), 100)
    
    # Adjust for complexity (example: 1-5 scale)
    # Formula: $Score = (Base \times 0.7) + (Complexity \times 6)$
    final_score = (base_score * 0.7) + (complexity * 6)
    
    # Ensure score stays within 0-100
    final_score = min(max(final_score, 0), 100)
    
    if final_score > 70:
        level = "CRITICAL"
    elif final_score > 40:
        level = "ELEVATED"
    else:
        level = "LOW"
        
    return {
        "score": round(final_score, 2),
        "risk_level": level
    }
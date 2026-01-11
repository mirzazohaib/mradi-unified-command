import sys
import os
# Ensure we can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.risk_engine import calculate_risk_score

def test_risk_ready_low_complexity():
    """Scenario: Ready Mission, Simple Asset -> Should be LOW risk"""
    result = calculate_risk_score("READY", complexity=1)
    
    # Math: (10 * 0.7) + (1 * 6) = 7 + 6 = 13.0
    assert result["score"] == 13.0
    assert result["risk_level"] == "LOW"

def test_risk_not_ready_critical():
    """Scenario: Not Ready Mission -> Should be CRITICAL risk (Safety Policy)"""
    result = calculate_risk_score("NOT_READY", complexity=3)
    
    # Math: (90 * 0.7) + (3 * 6) = 63 + 18 = 81.0
    assert result["score"] > 70
    assert result["risk_level"] == "CRITICAL"

def test_risk_high_complexity_bump():
    """Scenario: Ready but High Complexity (5) -> Should be higher, but still manageable"""
    result = calculate_risk_score("READY", complexity=5)
    
    # Math: (10 * 0.7) + (5 * 6) = 7 + 30 = 37.0
    assert result["score"] == 37.0
    # 37 is < 40, so it is still LOW
    assert result["risk_level"] == "LOW"
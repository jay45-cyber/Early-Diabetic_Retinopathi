"""Clinical risk formatting, recommendation mapping, and safety disclaimers."""
from typing import Dict, Any

CLINICAL_DISCLAIMER = (
    "RESEARCH SCREENING-SUPPORT PROTOTYPE ONLY: "
    "This AI system is an academic research prototype. It does not diagnose diabetes "
    "or replace laboratory testing (HbA1c / FPG) or clinical evaluation by a physician."
)


def format_screening_output(
    calibrated_probability: float,
    threshold_low_risk: float = 0.35,
    threshold_high_risk: float = 0.65
) -> Dict[str, Any]:
    """Map calibrated probability score to clinical triage recommendation bands."""
    prob_percent = round(calibrated_probability * 100.0, 1)

    if calibrated_probability < threshold_low_risk:
        risk_category = "Low Risk"
        recommendation = "Standard annual health review and regular ocular screening."
        urgency = "Routine"
    elif calibrated_probability < threshold_high_risk:
        risk_category = "Moderate Risk"
        recommendation = "Primary care clinical review; consider baseline fasting plasma glucose check within 3 months."
        urgency = "Moderate"
    else:
        risk_category = "High Risk"
        recommendation = "Priority referral to Primary Health Center (PHC) for confirmatory venous HbA1c testing."
        urgency = "Priority"

    return {
        "calibrated_risk_score": prob_percent,
        "risk_category": risk_category,
        "triage_urgency": urgency,
        "clinical_recommendation": recommendation,
        "disclaimer": CLINICAL_DISCLAIMER
    }


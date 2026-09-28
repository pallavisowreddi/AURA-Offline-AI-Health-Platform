# -*- coding: utf-8 -*-
"""
AURA Symptom Awareness Service
Educational symptom correlation without medical diagnosis.
Adheres strictly to WHO / medical guidelines: educational awareness, no probabilistic diagnosis.
"""
from core import database

def analyze_symptoms_for_awareness(symptom_ids_or_names, user_notes="", lang="en"):
    """
    Correlates a list of reported symptoms with the local disease knowledge base.
    Returns:
    - matched_conditions: list of potential associated conditions (with key facts)
    - general_guidance: educational care information
    - warning_signs: warning signs to watch out for
    - when_to_seek_care: medical trigger criteria
    """
    all_diseases = database.get_all_diseases()
    
    # Normalize input symptoms
    input_terms = [s.lower().strip() for s in symptom_ids_or_names if s.strip()]
    if user_notes:
        input_terms.extend([w.lower().strip() for w in user_notes.replace(",", " ").split() if len(w) > 3])

    matched_conditions = []

    for d in all_diseases:
        raw = d.get("raw", {})
        common_symptoms = [cs.lower() for cs in raw.get("common_symptoms", [])]
        matched_symptoms = []

        for term in input_terms:
            for cs in common_symptoms:
                if term in cs or cs in term:
                    if cs not in matched_symptoms:
                        matched_symptoms.append(cs)

        if matched_symptoms:
            matched_conditions.append({
                "id": d["id"],
                "name": d["name"],
                "category": d["category"],
                "matched_symptoms": matched_symptoms,
                "match_count": len(matched_symptoms),
                "overview": d["overview"],
                "warning_signs": raw.get("warning_signs", []),
                "when_to_seek_help": raw.get("when_to_seek_medical_help", ""),
                "prevention": raw.get("prevention", [])[:3]
            })

    # Sort conditions by number of matching symptoms
    matched_conditions.sort(key=lambda x: x["match_count"], reverse=True)
    top_matches = matched_conditions[:4]

    # Educational narrative
    disclaimer = (
        "Educational information only. This tool provides health-awareness information "
        "and DOES NOT diagnose diseases. A physical examination and clinical laboratory testing "
        "by a qualified doctor are necessary for an accurate diagnosis."
    )

    return {
        "status": "success",
        "input_symptoms": symptom_ids_or_names,
        "possible_conditions": top_matches,
        "disclaimer": disclaimer,
        "summary": f"These symptoms may occur in several conditions, including {', '.join([c['name'] for c in top_matches])}." if top_matches else "No direct matches found in our local database for this symptom combination."
    }

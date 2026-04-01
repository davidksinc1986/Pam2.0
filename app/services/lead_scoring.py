def score_lead(source: str, stage: str, summary: str) -> float:
    score = 35.0
    if source.lower() in {"facebook", "instagram", "meta"}:
        score += 20
    if stage in {"Contacted", "Qualified"}:
        score += 15
    text = summary.lower()
    if any(token in text for token in ["presupuesto", "comprar", "demo", "precio"]):
        score += 20
    if any(token in text for token in ["no", "sin interés", "después"]):
        score -= 10
    return max(0.0, min(score, 100.0))

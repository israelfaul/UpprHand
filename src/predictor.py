WEIGHTS = {
    "opponent_quality": 0.30,
    "punch_efficiency": 0.20,
    "recent_form": 0.15,
    "power": 0.15,
    "weight_class_fit": 0.10,
    "pedigree": 0.05,
    "age_prime": 0.05,
}


def calculate_score(fighter):
    total = 0

    for category, weight in WEIGHTS.items():
        total += fighter["scores"][category] * weight

    return total


def predict_matchup(fighter_a, fighter_b):
    score_a = calculate_score(fighter_a)
    score_b = calculate_score(fighter_b)

    total_score = score_a + score_b

    probability_a = round((score_a / total_score) * 100, 1)
    probability_b = round((score_b / total_score) * 100, 1)

    return {
        fighter_a["name"]: probability_a,
        fighter_b["name"]: probability_b,
        "raw_scores": {
            fighter_a["name"]: round(score_a, 2),
            fighter_b["name"]: round(score_b, 2),
        },
    }
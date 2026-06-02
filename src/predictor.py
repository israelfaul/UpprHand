from scoring import build_scores

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
    scores = build_scores(fighter)
    total = 0

    for category, weight in WEIGHTS.items():
        total += scores[category] * weight

    return total


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


def compare_categories(fighter_a, fighter_b):
    advantages_a = []
    advantages_b = []

    for category in WEIGHTS:
        
        
        scores_a = build_scores(fighter_a)
        scores_b = build_scores(fighter_b)

        score_a = scores_a[category]
        score_b = scores_b[category]

        difference = round(abs(score_a - score_b), 1)

        if score_a > score_b:
            advantages_a.append((category, difference))
        elif score_b > score_a:
            advantages_b.append((category, difference))

    advantages_a.sort(key=lambda x: x[1], reverse=True)
    advantages_b.sort(key=lambda x: x[1], reverse=True)

    return advantages_a[:3], advantages_b[:3]


def predict_matchup(fighter_a, fighter_b):
    score_a = calculate_score(fighter_a)
    score_b = calculate_score(fighter_b)

    total_score = score_a + score_b

    probability_a = round((score_a / total_score) * 100, 1)
    probability_b = round((score_b / total_score) * 100, 1)

    advantages_a, advantages_b = compare_categories(
        fighter_a,
        fighter_b
    )

    return {
        "probabilities": {
            fighter_a["name"]: probability_a,
            fighter_b["name"]: probability_b
        },
        "raw_scores": {
            fighter_a["name"]: round(score_a, 2),
            fighter_b["name"]: round(score_b, 2)
        },
        "advantages": {
            fighter_a["name"]: advantages_a,
            fighter_b["name"]: advantages_b
        }
    }
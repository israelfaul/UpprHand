from src.scoring import build_scores

BASE_RATING = 1000

CATEGORY_WEIGHTS = {
    "opponent_quality": 1.8,
    "punch_efficiency": 1.5,
    "recent_form": 1.3,
    "power": 1.2,
    "weight_class_fit": 0.9,
    "pedigree": 0.7,
    "age_prime": 0.6,
}

CATEGORY_BASELINE = 70


def calculate_rating(fighter):
    scores = build_scores(fighter)
    rating = BASE_RATING

    for category, weight in CATEGORY_WEIGHTS.items():
        rating += (scores[category] - CATEGORY_BASELINE) * weight

    return round(rating, 2)


def calculate_probability(rating_a, rating_b):
    probability_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    probability_b = 1 - probability_a

    return round(probability_a * 100, 1), round(probability_b * 100, 1)


def compare_categories(fighter_a, fighter_b):
    scores_a = build_scores(fighter_a)
    scores_b = build_scores(fighter_b)

    advantages_a = []
    advantages_b = []

    for category in CATEGORY_WEIGHTS:
        difference = round(abs(scores_a[category] - scores_b[category]), 1)

        if scores_a[category] > scores_b[category]:
            advantages_a.append((category, difference))
        elif scores_b[category] > scores_a[category]:
            advantages_b.append((category, difference))

    advantages_a.sort(key=lambda x: x[1], reverse=True)
    advantages_b.sort(key=lambda x: x[1], reverse=True)

    return advantages_a[:3], advantages_b[:3]


def predict_matchup(fighter_a, fighter_b):
    rating_a = calculate_rating(fighter_a)
    rating_b = calculate_rating(fighter_b)

    probability_a, probability_b = calculate_probability(rating_a, rating_b)

    advantages_a, advantages_b = compare_categories(fighter_a, fighter_b)

    return {
        "probabilities": {
            fighter_a["name"]: probability_a,
            fighter_b["name"]: probability_b
        },
        "raw_scores": {
            fighter_a["name"]: rating_a,
            fighter_b["name"]: rating_b
        },
        "advantages": {
            fighter_a["name"]: advantages_a,
            fighter_b["name"]: advantages_b
        }
    }
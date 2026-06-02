def calculate_ko_percentage(fighter):
    if fighter["wins"] == 0:
        return 0

    return round((fighter["kos"] / fighter["wins"]) * 100, 1)


def calculate_age_prime_score(fighter):
    age = fighter["age"]

    if 24 <= age <= 30:
        return 95
    elif 21 <= age <= 23:
        return 88
    elif 31 <= age <= 34:
        return 82
    elif 35 <= age <= 37:
        return 70
    else:
        return 60


def build_scores(fighter):
    scores = fighter["scores"].copy()

    scores["power"] = calculate_ko_percentage(fighter)
    scores["age_prime"] = calculate_age_prime_score(fighter)

    return scores
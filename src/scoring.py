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


def calculate_opponent_score(opponent):
    total_fights = opponent["wins"] + opponent["losses"] + opponent["draws"]

    if total_fights == 0:
        return 0

    win_percentage = (opponent["wins"] / total_fights) * 100
    ko_percentage = 0

    if opponent["wins"] > 0:
        ko_percentage = (opponent["kos"] / opponent["wins"]) * 100

    score = (win_percentage * 0.60) + (ko_percentage * 0.20)

    if opponent["ranked"]:
        score += 10

    if opponent["former_champion"]:
        score += 10

    return min(round(score, 1), 100)


def calculate_opponent_quality_score(fighter):
    opponents = fighter.get("opponents", [])

    if not opponents:
        return fighter["scores"].get("opponent_quality", 0)

    opponent_scores = []

    for opponent in opponents:
        opponent_scores.append(calculate_opponent_score(opponent))

    return round(sum(opponent_scores) / len(opponent_scores), 1)


def build_scores(fighter):
    scores = fighter["scores"].copy()

    scores["power"] = calculate_ko_percentage(fighter)
    scores["age_prime"] = calculate_age_prime_score(fighter)
    scores["opponent_quality"] = calculate_opponent_quality_score(fighter)

    return scores
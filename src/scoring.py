def calculate_ko_percentage(fighter):
    if fighter["wins"] == 0:
        return 0

    return round((fighter["kos"] / fighter["wins"]) * 100, 1)


def build_scores(fighter):
    scores = fighter["scores"].copy()

    scores["power"] = calculate_ko_percentage(fighter)

    return scores
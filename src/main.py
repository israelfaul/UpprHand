import json
from predictor import predict_matchup


def load_fighters():
    with open("data/fighters.json", "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    fighters = load_fighters()

    fighter_a = fighters[0]
    fighter_b = fighters[1]

    prediction = predict_matchup(fighter_a, fighter_b)

    print("\nUpprHand Prediction")
    print("-------------------\n")

    for fighter, probability in prediction["probabilities"].items():
        print(f"{fighter}: {probability}%")

    print("\nRaw Scores:")
    for fighter, score in prediction["raw_scores"].items():
        print(f"{fighter}: {score}")

    print("\nBiggest Advantages\n")

    for fighter, advantages in prediction["advantages"].items():
        print(f"{fighter}")

        for category, diff in advantages:
            print(f"  + {category} (+{diff})")

        print()


if __name__ == "__main__":
    main()
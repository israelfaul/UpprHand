import json
from predictor import predict_matchup


def load_fighters():
    with open("data/fighters.json", "r", encoding="utf-8") as file:
        return json.load(file)


def find_fighter(fighters, name):
    name = name.lower().strip()

    for fighter in fighters:
        fighter_name = fighter["name"].lower()

        if name == fighter_name or name in fighter_name:
            return fighter

    return None


def display_fighters(fighters):
    print("\nAvailable Fighters")
    print("------------------")

    for fighter in fighters:
        print(f"- {fighter['name']}")

def save_prediction(prediction, fighter_a, fighter_b):
    result = {
        "fighter_a": fighter_a["name"],
        "fighter_b": fighter_b["name"],
        "prediction": prediction
    }

    with open("results/predictions.json", "r", encoding="utf-8") as file:
        predictions = json.load(file)

    predictions.append(result)

    with open("results/predictions.json", "w", encoding="utf-8") as file:
        json.dump(predictions, file, indent=4)

def main():
    fighters = load_fighters()

    display_fighters(fighters)

    fighter_a_name = input("\nEnter first fighter: ")
    fighter_b_name = input("Enter second fighter: ")

    fighter_a = find_fighter(fighters, fighter_a_name)
    fighter_b = find_fighter(fighters, fighter_b_name)

    if fighter_a is None or fighter_b is None:
        print("\nError: One or both fighters were not found.")
        return

    prediction = predict_matchup(fighter_a, fighter_b)
    
    save_prediction(prediction, fighter_a, fighter_b)

    print("\nUpprHand Prediction")
    print("-------------------\n")

    for fighter, probability in prediction["probabilities"].items():
        print(f"{fighter}: {probability}%")

    winner = max(
        prediction["probabilities"],
        key=prediction["probabilities"].get
    )

    winner_probability = prediction["probabilities"][winner]

    print(f"\nProjected Edge: {winner} with {winner_probability}%")

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
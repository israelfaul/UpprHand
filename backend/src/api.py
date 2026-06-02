import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.predictor import predict_matchup

app = FastAPI(title="UpprHand API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/")
def root():
    return {"message": "UpprHand API is running"}


@app.get("/fighters")
def get_fighters():
    fighters = load_fighters()

    return [
        {
            "name": fighter["name"],
            "record": fighter["record"],
            "weight_class": fighter["weight_class"],
            "stance": fighter["stance"]
        }
        for fighter in fighters
    ]


@app.get("/predict")
def predict(fighter_a: str, fighter_b: str):
    fighters = load_fighters()

    first_fighter = find_fighter(fighters, fighter_a)
    second_fighter = find_fighter(fighters, fighter_b)

    if first_fighter is None or second_fighter is None:
        raise HTTPException(status_code=404, detail="One or both fighters were not found.")

    return predict_matchup(first_fighter, second_fighter)
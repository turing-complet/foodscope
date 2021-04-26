import pandas as pd


def _get_compounds(name: str):
    df = pd.read_csv("foodb_2020_04_07_csv/Compound.csv")
    return df.loc[df["name"].str.contains(name, case=False), :]


def get_foods(compound: str):
    compounds = _get_compounds(compound)
    ids = compounds.id
    df = pd.read_csv("foodb_2020_04_07_csv/Content.csv")
    foods = pd.read_csv("foodb_2020_04_07_csv/Food.csv")
    food_id = df.loc[df["source_id"].isin(ids), "food_id"]
    return foods.loc[foods["id"].isin(food_id), :]

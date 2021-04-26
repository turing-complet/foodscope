import pandas as pd


def _get_compounds(name: str):
    df = pd.read_csv("foodb_2020_04_07_csv/Compound.csv", usecols=["id", "name"])
    return df.loc[df["name"].str.contains(name, case=False), :]


def get_foods(compound: str):
    compounds = _get_compounds(compound)
    ids = compounds.id
    df = pd.read_csv(
        "foodb_2020_04_07_csv/Content.csv",
        usecols=["id", "food_id", "source_id", "source_type"],
    )
    foods = pd.read_csv("foodb_2020_04_07_csv/Food.csv", usecols=["id", "name"])
    food_id = df.loc[
        df["source_id"].isin(ids) & (df["source_type"] == "Compound"), "food_id"
    ]
    return foods.loc[foods["id"].isin(food_id), :]

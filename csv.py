import pandas as pd


def _get_compounds(name: str):
    df = pd.read_csv("foodb_2020_04_07_csv/Compound.csv", usecols=["id", "name"])
    df = df.loc[df["name"].str.contains(name, case=False), :]
    return df.rename(columns={"id": "compound_id"})


def get_foods(compound: str):
    compounds = _get_compounds(compound)
    ids = compounds.compound_id
    cols = [
        "id",
        "food_id",
        "source_id",
        "source_type",
        "orig_content",
        "orig_min",
        "orig_max",
    ]
    df = pd.read_csv(
        "foodb_2020_04_07_csv/Content.csv",
        usecols=cols,
    )
    mask = df["source_id"].isin(ids) & (df["source_type"] == "Compound")
    df = df.loc[mask, :]

    foods = pd.read_csv("foodb_2020_04_07_csv/Food.csv", usecols=["id", "name"])
    foods.rename(columns={"id": "food_id"}, inplace=True)
    merged = pd.merge(df, foods, on="food_id")
    return merged

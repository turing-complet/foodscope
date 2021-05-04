import pandas as pd


def get_nutrients():
    df = pd.read_csv("foodb_2020_04_07_csv/Nutrient.csv", usecols=["id", "name"])
    df.rename(columns={"id": "nutrient_id"}, inplace=True)
    return df


def get_compounds():
    df = pd.read_csv("foodb_2020_04_07_csv/Compound.csv", usecols=["id", "name"])
    df.rename(columns={"id": "compound_id"}, inplace=True)
    return df


def select_compound(name: str):
    df = get_compounds()
    return df.loc[df.name.str.contains(name, case=False), :]


def get_foods():
    foods = pd.read_csv("foodb_2020_04_07_csv/Food.csv", usecols=["id", "name"])
    foods.rename(columns={"id": "food_id"}, inplace=True)
    return foods


def select_food(food: str):
    foods = get_foods()
    return foods.loc[foods.name.str.contains(food, case=False), :]


def get_content(cols=None):
    cols = (
        cols
        if cols is not None
        else [
            "id",
            "food_id",
            "source_id",
            "source_type",
            "orig_content",
            "orig_min",
            "orig_max",
        ]
    )
    df = pd.read_csv("foodb_2020_04_07_csv/Content.csv", usecols=cols)
    return df


def foods_by_compound(compound: str):
    compounds = select_compound(compound)
    ids = compounds.compound_id

    df = get_content()
    mask = df["source_id"].isin(ids) & (df["source_type"] == "Compound")
    df = df.loc[mask, :]
    df.rename(columns={"source_id": "compound_id"}, inplace=True)

    foods = get_foods()
    merged = pd.merge(df, foods, on="food_id")
    merged.rename(columns={"source_id": "compound_id"}, inplace=True)
    return pd.merge(merged, compounds, on="compound_id")


# probably need outer join if source is both
def composition(food: str, source=None):
    if source is None:
        source = ("Compound", "Nutrient")
    food = select_food(food)
    df = get_content(cols=["source_id", "source_type", "food_id"])
    df = pd.merge(df, food, on="food_id")
    result = pd.DataFrame()
    if "Compound" in source:
        compound = get_compounds()
        result = result.append(
            pd.merge(df[df.source_type == "Compound"], compound, left_on="source_id", right_on="compound_id")
        )
    if "Nutrient" in source:
        nutrient = get_nutrients()
        result.append(
            pd.merge(df[df.source_type == "Nutrient"], nutrient, left_on="source_id", right_on="nutrient_id")
        )
    return df


def get_health_effects(food: str):
    pass

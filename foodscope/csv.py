from pathlib import Path

import pandas as pd

_csv_dir = Path(Path(__file__).parent.parent, "foodb_2020_04_07_csv")


def load(filename, cols):
    return pd.read_csv(f"{_csv_dir}/{filename}", usecols=cols)


def get_nutrients():
    df = load("Nutrient.csv", cols=["id", "name"])
    df.rename(columns={"id": "nutrient_id"}, inplace=True)
    return df


def get_compounds():
    df = load("Compound.csv", cols=["id", "name"])
    df.rename(columns={"id": "compound_id"}, inplace=True)
    return df


def select_compound(name: str):
    df = get_compounds()
    return df.loc[df.name.str.contains(name, case=False), :]


def get_foods():
    foods = load("Food.csv", cols=["id", "name"])
    foods.rename(columns={"id": "food_id"}, inplace=True)
    return foods


def select_food(food: str):
    foods = get_foods()
    return foods.loc[foods.name.str.contains(food, case=False), :]


def get_health_effects():
    df = load("HealthEffect.csv", cols=["id", "name", "description"])
    df.rename(columns={"id": "health_effect_id"}, inplace=True)
    return df


def get_compounds_health_effects():
    df = load(
        "CompoundsHealthEffect.csv", cols=["id", "compound_id", "health_effect_id"]
    )
    return df


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
    df = load("Content.csv", cols=cols)
    return df


def filter_content(df=None, source_type=None, cols=None):
    df = get_content(cols) if df is None else df
    if source_type not in ("Nutrient", "Compound"):
        raise ValueError(f"Invalid source_type={source_type}")
    return df.loc[df.source_type == source_type, :]


def foods_by_compound(compound: str):
    compounds = select_compound(compound)
    ids = compounds.compound_id

    df = filter_content(source_type="Compound")
    mask = df["source_id"].isin(ids)
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
            pd.merge(
                filter_content(df, "Compound"),
                compound,
                left_on="source_id",
                right_on="compound_id",
            )
        )
    if "Nutrient" in source:
        nutrient = get_nutrients()
        result = result.append(
            pd.merge(
                filter_content(df, "Nutrient"),
                nutrient,
                left_on="source_id",
                right_on="nutrient_id",
            )
        )
    return result


def health_effects(food: str):
    df = filter_content(source_type="Compound")
    result = pd.merge(select_food(food), df, on="food_id")
    result = pd.merge(
        result, get_compounds(), left_on="source_id", right_on="compound_id"
    )
    result = pd.merge(result, get_compounds_health_effects(), on="compound_id")
    return pd.merge(result, get_health_effects(), on="health_effect_id")

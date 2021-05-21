from pathlib import Path

import pandas as pd

# pd.set_option("display.max_rows", None)
_csv_dir = Path(Path(__file__).parent.parent, "v2020_04_07")


class Table:
    _filename = None
    _cols = None
    _rename = None

    def __new__(cls, cols=None):
        if cols is None:
            cols = cls._cols
        elif cols == "all":
            cols = None
        df = load(cls._filename, cols)
        if cls._rename is not None:
            df.rename(columns=cls._rename, inplace=True)
        return df


class Nutrient(Table):
    _filename = "Nutrient.csv"
    _cols = ["id", "name"]
    _rename = {"id": "nutrient_id"}


class Compound(Table):
    _filename = "Compound.csv"
    _cols = ["id", "name"]
    _rename = {"id": "compound_id"}


class Food(Table):
    _filename = "Food.csv"
    _cols = ["id", "name"]
    _rename = {"id": "food_id"}


class CompoundsHealthEffect(Table):
    _filename = "CompoundsHealthEffect.csv"
    _cols = ["id", "compound_id", "health_effect_id"]


class HealthEffect(Table):
    _filename = "HealthEffect.csv"
    _cols = ["id", "name", "description"]
    _rename = {"id": "health_effect_id"}


class Content(Table):
    _filename = "Content.csv"


def load(filename, cols=None):
    return pd.read_csv(Path(_csv_dir, filename), usecols=cols)


def select_compound(name: str):
    df = Compound()
    return df.loc[df.name.str.contains(name, case=False), :]


def select_food(food: str):
    foods = Food()
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

    foods = Food()
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
        compound = Compound()
        result = result.append(
            pd.merge(
                filter_content(df, "Compound"),
                compound,
                left_on="source_id",
                right_on="compound_id",
            )
        )
    if "Nutrient" in source:
        nutrient = Nutrient()
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
    result = pd.merge(result, Compound(), left_on="source_id", right_on="compound_id")
    result = pd.merge(result, CompoundsHealthEffect(), on="compound_id")
    return pd.merge(result, HealthEffect(), on="health_effect_id")

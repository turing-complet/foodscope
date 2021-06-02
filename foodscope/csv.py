from pathlib import Path

import pandas as pd

_csv_dir = Path(Path(__file__).parent.parent, "v2020_04_07")


class Table(pd.DataFrame):
    _filename = None
    _cols = None
    _rename = None

    def __init__(self, cols=None):
        if cols is None:
            cols = self._cols
        elif cols == "all":
            cols = None
        df = load(self._filename, cols)
        if self._rename is not None:
            df.rename(columns=self._rename, inplace=True)
        super().__init__(df)

    def select(self, name):
        return self.loc[self.name.str.contains(name, case=False), :]


class Nutrient(Table):
    _filename = "Nutrient.csv"
    _cols = ["id", "name"]
    _rename = {"id": "nutrient_id"}


class Compound(Table):
    _filename = "Compound.csv"
    _cols = ["id", "name"]
    _rename = {"id": "compound_id"}

    def equiv(self, group):
        return self.loc[self.name.str.contains("|".join(group))]

    def health_effects(self, group):
        result = self.equiv(group)
        result = pd.merge(result, CompoundsHealthEffect(), on="compound_id")
        return pd.merge(result, HealthEffect(), on="health_effect_id")


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
    _cols = [
        "id",
        "food_id",
        "source_id",
        "source_type",
        "orig_content",
        "orig_min",
        "orig_max",
    ]


def load(filename, cols=None):
    return pd.read_csv(Path(_csv_dir, filename), usecols=cols)


def filter_content(df=None, source_type=None, cols=None):
    df = Content(cols) if df is None else df
    if source_type not in ("Nutrient", "Compound"):
        raise ValueError(f"Invalid source_type={source_type}")
    return df.loc[df.source_type == source_type, :]


def foods_by_compound(compound: str):
    compounds = Compound().select(compound)
    ids = compounds.compound_id

    df = filter_content(source_type="Compound")
    mask = df["source_id"].isin(ids)
    df = df.loc[mask, :]
    df.rename(columns={"source_id": "compound_id"}, inplace=True)

    merged = pd.merge(df, Food(), on="food_id")
    return pd.merge(merged, compounds, on="compound_id")


# probably need outer join if source is both
def composition(food: str, source=None):
    if source is None:
        source = ("Compound", "Nutrient")

    df = Content(cols=["source_id", "source_type", "food_id"])
    df = pd.merge(df, Food().select(food), on="food_id")
    result = pd.DataFrame()
    if "Compound" in source:
        result = result.append(
            pd.merge(
                filter_content(df, "Compound"),
                Compound(),
                left_on="source_id",
                right_on="compound_id",
            )
        )
    if "Nutrient" in source:
        result = result.append(
            pd.merge(
                filter_content(df, "Nutrient"),
                Nutrient(),
                left_on="source_id",
                right_on="nutrient_id",
            )
        )
    return result


def health_effects(food: str):
    df = filter_content(source_type="Compound")
    result = pd.merge(Food().select(food), df, on="food_id")
    result = pd.merge(result, Compound(), left_on="source_id", right_on="compound_id")
    result = pd.merge(result, CompoundsHealthEffect(), on="compound_id")
    return pd.merge(result, HealthEffect(), on="health_effect_id")

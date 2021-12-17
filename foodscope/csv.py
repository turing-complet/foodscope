import logging
from pathlib import Path

import pandas as pd
import numexpr

from foodscope.mappings import expand_greeks

_log = logging.getLogger(__name__)
_csv_dir = Path(Path(__file__).parent.parent, "v2020_04_07")


def lazy_property(fn):
    attr = f"_lazy_{fn.__name__}"

    @property
    def _lazy(self):
        if not hasattr(self, attr):
            setattr(self, attr, fn(self))
        return getattr(self, attr)

    return _lazy


class FooDb:
    def __init__(self) -> None:
        self.food = Food()
        self.compound = Compound()
        self.nutrient = Nutrient()
        self.health_effect = HealthEffect()
        self.compounds_health_effect = CompoundsHealthEffect()
        self._content = None

    @lazy_property
    def content(self):
        return Content()

    def foods_by_compound(self, compound: str):
        _log.warn("Use Food.by_compound instead")
        return self.food.by_compound(compound)

    def health_effects(self, food: str):
        df = filter_content(source_type="Compound")
        result = pd.merge(self.food.select(food), df, on="food_id")
        result = pd.merge(
            result, self.compound.df, left_on="source_id", right_on="compound_id"
        )
        result = pd.merge(result, self.compounds_health_effect.df, on="compound_id")
        return pd.merge(result, self.health_effect.df, on="health_effect_id")

    def composition(self, food: str, source=None):
        if source is None:
            source = ("Compound", "Nutrient")

        df = Content(cols=["source_id", "source_type", "food_id"]).df
        df = pd.merge(df, self.food.select(food), on="food_id")
        result = pd.DataFrame()
        if "Compound" in source:
            result = result.append(
                pd.merge(
                    filter_content(df, source_type="Compound"),
                    self.compound.df,
                    left_on="source_id",
                    right_on="compound_id",
                )
            )
        if "Nutrient" in source:
            result = result.append(
                pd.merge(
                    filter_content(df, source_type="Nutrient"),
                    self.nutrient.df,
                    left_on="source_id",
                    right_on="nutrient_id",
                )
            )
        return result


class Table:
    _filename = None
    _cols = None
    _rename = None

    def __init__(self, cols=None):
        if cols is None:
            cols = self._cols
        elif cols == "all":
            cols = None
        self.df: pd.DataFrame = load(self._filename, cols)
        if self._rename is not None:
            self.df.rename(columns=self._rename, inplace=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(shape={self.df.shape}, cols={list(self.df.columns)})"

    def select(self, name):
        if isinstance(name, str):
            _log.info("Expanding greeks")
            name = expand_greeks(name)
        if not isinstance(name, (list, tuple, set)):
            raise TypeError("group should be iterable")
        return self.df.loc[self.df.name.str.contains("|".join(name), case=False)]


class EntityTable(Table):
    _id = None

    def by_id(self, row_id):
        return self.df.loc[self.df.get(self._id) == row_id, :]


class Nutrient(EntityTable):
    _filename = "Nutrient.csv"
    _cols = ["id", "name"]
    _rename = {"id": "nutrient_id"}
    _id = "nutrient_id"


class Compound(EntityTable):
    _filename = "Compound.csv"
    _cols = ["id", "name"]
    _rename = {"id": "compound_id"}
    _id = "compound_id"

    def health_effects(self, group):
        result = self.select(group)
        result = pd.merge(result, CompoundsHealthEffect().df, on="compound_id")
        return pd.merge(result, HealthEffect().df, on="health_effect_id")


class Food(EntityTable):
    _filename = "Food.csv"
    _cols = ["id", "name"]
    _rename = {"id": "food_id"}
    _id = "food_id"

    def by_compound(self, name):
        compounds = DB.compound.select(name)
        ids = compounds.compound_id
        df = filter_content(DB.content.df, source_type="Compound")
        mask = df["source_id"].isin(ids)
        df = df.loc[mask, :]
        df.rename(columns={"source_id": "compound_id"}, inplace=True)

        merged = pd.merge(df, self.df, on="food_id")
        return pd.merge(merged, compounds, on="compound_id")

    def subtract(self, name, threshold=None):
        ids = DB.compound.select(name).compound_id
        content = DB.content.df
        mask = content["source_id"].isin(ids)
        content = content.loc[mask, :]
        content = filter_content(content, source_type="Compound", floor=threshold)
        filtered_ids = content.food_id.unique()

        orig = set(self.df.name)
        self.df = self.df.loc[~self.df.food_id.isin(filtered_ids)]
        new = set(self.df.name)
        print(f"Removed = {sorted(orig-new)}")
        return self


class HealthEffect(EntityTable):
    _filename = "HealthEffect.csv"
    _cols = ["id", "name", "description"]
    _rename = {"id": "health_effect_id"}
    _id = "health_effect_id"


class CompoundsHealthEffect(Table):
    _filename = "CompoundsHealthEffect.csv"
    _cols = ["id", "compound_id", "health_effect_id"]


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


def filter_content(df=None, source_type=None, cols=None, floor=None):
    df = Content(cols).df if df is None else df
    if source_type not in ("Nutrient", "Compound"):
        raise ValueError(f"Invalid source_type={source_type}")
    query = "source_type == @source_type"
    if floor is not None:
        query += " & (orig_content > @floor"
        query += " | orig_min > @floor"
        query += " | orig_max > @floor)"
        query += " | @pd.isna([orig_content, orig_min, orig_max]).all()"
    return df.query(query, engine="python")


def foods_by_compound(compound: str):
    return DB.foods_by_compound(compound)


def health_effects(food: str):
    return DB.health_effects(food)


# probably need outer join if source is both
def composition(food: str, source=None):
    return DB.composition(food, source)


DB = FooDb()

import logging
from pathlib import Path

import pandas as pd

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
            result, self.compound, left_on="source_id", right_on="compound_id"
        )
        result = pd.merge(result, self.compounds_health_effect, on="compound_id")
        return pd.merge(result, self.health_effect, on="health_effect_id")

    def composition(self, food: str, source=None):
        if source is None:
            source = ("Compound", "Nutrient")

        df = Content(cols=["source_id", "source_type", "food_id"])
        df = pd.merge(df, self.food.select(food), on="food_id")
        result = pd.DataFrame()
        if "Compound" in source:
            result = result.append(
                pd.merge(
                    filter_content(df, "Compound"),
                    self.compound,
                    left_on="source_id",
                    right_on="compound_id",
                )
            )
        if "Nutrient" in source:
            result = result.append(
                pd.merge(
                    filter_content(df, "Nutrient"),
                    self.nutrient,
                    left_on="source_id",
                    right_on="nutrient_id",
                )
            )
        return result


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
        matches = expand_greeks(name)
        return self.equiv(matches)

    def equiv(self, group):
        if isinstance(group, str):
            _log.warn("Use .select() instead")
            group = [group]
        if not isinstance(group, (list, tuple, set)):
            raise TypeError("group should be iterable")
        return self.loc[self.name.str.contains("|".join(group), case=False)]


class EntityTable(Table):
    def by_id(self, row_id):
        return self.loc[self.get(self._id) == row_id, :]


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
        result = self.equiv(group)
        result = pd.merge(result, CompoundsHealthEffect(), on="compound_id")
        return pd.merge(result, HealthEffect(), on="health_effect_id")


class Food(EntityTable):
    _filename = "Food.csv"
    _cols = ["id", "name"]
    _rename = {"id": "food_id"}
    _id = "food_id"

    def by_compound(self, name):
        compounds = DB.compound.select(name)
        ids = compounds.compound_id
        df = filter_content(DB.content, source_type="Compound")
        mask = df["source_id"].isin(ids)
        df = df.loc[mask, :]
        df.rename(columns={"source_id": "compound_id"}, inplace=True)

        merged = pd.merge(df, self, on="food_id")
        return pd.merge(merged, compounds, on="compound_id")

    def subtract(self, name):
        compounds = DB.compound.select(name)
        ids = compounds.compound_id
        df = filter_content(DB.content, source_type="Compound")
        mask = df["source_id"].isin(ids)
        filtered_ids = df.loc[~mask, :].food_id
        return self.loc[self.food_id.isin(filtered_ids)]


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


def filter_content(df=None, source_type=None, cols=None):
    df = Content(cols) if df is None else df
    if source_type not in ("Nutrient", "Compound"):
        raise ValueError(f"Invalid source_type={source_type}")
    return df.loc[df.source_type == source_type, :]


def foods_by_compound(compound: str):
    return DB.foods_by_compound(compound)


def health_effects(food: str):
    return DB.health_effects(food)


# probably need outer join if source is both
def composition(food: str, source=None):
    return DB.composition(food, source)


DB = FooDb()

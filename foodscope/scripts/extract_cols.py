import foodscope as fs

cols = {}


def _cols(df):
    return list(df.columns.values)


# global view
db = fs.FooDb()
df = db.food.select("milk")
cols["food"] = _cols(df)


# case insensitive match across permutations
df = db.compound.select(fs.expand_greeks("beta-carotene"))
cols["compound"] = _cols(df)


# base data frames
nutrient = fs.Nutrient()
food = fs.Food()
compound = fs.Compound()

# unfiltered
nutrient = fs.Nutrient(cols="all")
cols["nutrient"] = _cols(df)


# simple filters
food.select("chicken")
nutrient.select("protein")
df = fs.filter_content(source_type="Nutrient")
cols["content_by_nutrient"] = _cols(df)

# fancy stuff
fs.foods_by_compound("sulf")
fs.composition("apple")
df = fs.health_effects("artichoke")
cols["health_effects"] = _cols(df)

# compounds
c = fs.Compound()
c.select(fs.vitamin_a)
df = c.health_effects(fs.vitamin_a)
cols["compound_health_effects"] = _cols(df)

print(cols)

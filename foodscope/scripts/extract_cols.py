import foodscope as fs

cols = {}


def _cols(df):
    return list(df.columns)


df = fs.Food(cols="all").df
cols["food"] = _cols(df)

df = fs.Compound(cols="all").df
cols["compound"] = _cols(df)


df = fs.Nutrient(cols="all").df
cols["nutrient"] = _cols(df)

df = fs.HealthEffect(cols="all").df
cols["health_effect"] = _cols(df)

df = fs.CompoundsHealthEffect(cols="all").df
cols["compounds_health_effect"] = _cols(df)

df = fs.Content(cols="all").df
cols["content_by_nutrient"] = _cols(df)

# fancy stuff
df = fs.foods_by_compound("sulf")
cols["foods_by_compound"] = _cols(df)

df = fs.composition("apple")
cols["fs.composition"] = _cols(df)

df = fs.health_effects("artichoke")
cols["fs.health_effects"] = _cols(df)


df = fs.Compound().health_effects(fs.vitamin_a)
cols["compound.health_effects"] = _cols(df)

print(cols)

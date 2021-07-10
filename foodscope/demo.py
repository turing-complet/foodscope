import foodscope as fs

# global view
db = fs.FooDb()
db.food.select("milk")

# case insensitive match across permutations
db.compound.equiv(fs.expand_greeks("beta-carotene"))

# base data frames
nutrient = fs.Nutrient()
food = fs.Food()
compound = fs.Compound()

# unfiltered
nutrient = fs.Nutrient(cols="all")

# simple filters
food.select("chicken")
nutrient.select("protein")
fs.filter_content(source_type="Nutrient")

# fancy stuff
fs.foods_by_compound("sulf")
fs.composition("apple")
fs.health_effects("artichoke")

# compounds
c = fs.Compound()
c.equiv(fs.vitamin_a)
c.health_effects(fs.vitamin_a)

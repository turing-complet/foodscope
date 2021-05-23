import foodscope as fs

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

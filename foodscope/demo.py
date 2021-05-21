import foodscope as fs

# base data frames
nutrient = fs.Nutrient()
food = fs.Food()
compound = fs.Compound()

# simple filters
fs.select_food("chicken")
fs.filter_content(source_type="Nutrient")

# fancy stuff
fs.foods_by_compound("sulf")
fs.composition("apple")
fs.health_effects("artichoke")

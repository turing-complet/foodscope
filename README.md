# foodscope

A closer look at food, based on data from [foodb](https://foodb.ca/)

Download the database (also available
[here](https://foodscope.blob.core.windows.net/data/foodb_2020_4_7_csv.tar.gz))
```
curl https://foodb.ca/public/system/downloads/foodb_2020_4_7_csv.tar.gz -O
tar xf foodb_2020_4_7_csv.tar.gz
```

Usage (see [demo](foodscope/demo.py))

```python
import foodscope as fs

# global view
db = fs.FooDb()
db.food.select("milk")

# case insensitive match across permutations
db.compound.select(fs.expand_greeks("beta-carotene"))

# automatically expand
db.compound.select("beta-carotene")

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
c.select(fs.vitamin_a)
c.health_effects(fs.vitamin_a)
```

https://foodb.ca/compounds/FDB003717#references

## TODO
- Bin foods by nutrient (quartiles)
- get health effects of a given meal
- preprocess data to minimize file size, or import to postgres?
- fuzzy vs exact match - could use global option?
- ask foodb about nan cols
- use CompoundSynonym.csv
- convert to hdf5
- filter against config file with compounds of interest
- check compound list for capital greek letters
- cache results from complex functions
- add aliases for other vitamins
- untangle circular references

look up health effects of garlic and compare with
this [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4417560/)

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

# base data frames
food = fs.Food()
compound = fs.Compound()

# unfiltered
nutrient = fs.Nutrient(cols="all")

#simple filters
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

# misc
fs.expand_greeks("beta-Carotene")
```

https://foodb.ca/compounds/FDB003717#references

## TODO
- Gluten free, dairy free, low beta carotene, low vitamin A, low sulfur
- Bin foods by nutrient (quartiles)
- get health effects of a given meal
- preprocess data to minimize file size, or import to postgres?
- cache base data frames in memory
- unit test with df.head() as mock
- compounds contain greek β AND regular "beta"
- fuzzy vs exact match - could use global option?
- ask foodb about nan cols
- use CompoundSynonym.csv
- convert to hdf5
- filter against config file with compounds of interest
- allow passing compound_id, food_id, etc


Content.csv seems to have food_id in (554, 678) which are missing from Food.csv
repro:
- step through foods_by_compound('L-Ascorbic acid')
- compare df to merged

look up health effects of garlic and compare with
this [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4417560/)

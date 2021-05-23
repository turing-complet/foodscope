# foodscope

A closer look at food, based on data from [foodb](https://foodb.ca/)

Download the database
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
```

https://foodb.ca/compounds/FDB003717#references

## TODO
- Gluten free, dairy free, low beta carotene, low vitamin A, low sulfur
- Bin foods by nutrient (quartiles)
- get health effects of a given meal
- preprocess data to minimize file size, or import to postgres?
- cache base data frames in memory
- backup dataset
- unit test with df.head() as mock
- compounds contain greek β AND regular "beta"
- fuzzy vs exact match
- gzip csv and store in s3/blob
- ask foodb about nan cols

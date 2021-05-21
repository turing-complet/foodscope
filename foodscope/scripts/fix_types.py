import pandas as pd
from pathlib import Path

from foodscope.csv import load, _csv_dir

files = [
    "Nutrient",
    "Compound",
    "Food",
    "HealthEffect",
    "CompoundsHealthEffect",
    "Content",
]


def get_stats(threshold=10, show_all=False):
    for f in files:
        df = load(f"{f}.csv")
        print(f"BEGIN stats for {f}")
        print("---------------------------------------")
        for c in df.columns:
            vc = df.loc[:, c].value_counts(dropna=False)
            if len(vc) > threshold:
                if show_all:
                    print(f"Discarding {f}.{c}, size={len(vc)}")
                    print()
                continue
            print(f"Value counts for {c}")
            print(vc)
            print()
        print(f"END stats for {f}")
        print("---------------------------------------")


def drop_nan():
    for f in files:
        df = load(f"{f}.csv")
        df.dropna(axis=1, how="all", inplace=True)
        df.to_csv(Path(_csv_dir, f"{f}.v1.csv"), index=False)

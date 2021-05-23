import shutil
from pathlib import Path

from foodscope.csv import _csv_dir, load

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
        fname = f"{f}.csv"
        new_fname = f"{f}.v1.csv"
        df = load(fname)
        df2 = df.dropna(axis=1, how="all")
        try:
            df.compare(df2)
            print(f"No change in {f}")
        except ValueError:
            print(f"{fname} -> {new_fname}")
            shutil.move(Path(_csv_dir, fname), Path(_csv_dir, new_fname))
            df2.to_csv(Path(_csv_dir, fname), index=False)

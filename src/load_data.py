from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path("data/MachineLearningCVE")


def load_all(cache="data/clean.pkl", refresh=False):
    """Load all CICIDS2017 CSVs, clean them, and cache the result."""
    cache = Path(cache)
    if cache.exists() and not refresh:
        return pd.read_pickle(cache)

    frames = []
    for path in sorted(DATA_DIR.glob("*.csv")):
        df = pd.read_csv(path, encoding="latin-1")
        df.columns = df.columns.str.strip()
        df["Label"] = (df["Label"].str.strip()
                       .str.replace(r"[^\x20-\x7E]", "-", regex=True))
        df = df.replace([np.inf, -np.inf], np.nan).dropna()

        features = df.columns.difference(["Label"])
        df[features] = df[features].astype("float32")
        df["Day"] = path.name.split("-")[0]
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=df.columns.difference(["Day"]))
    df["is_attack"] = (df["Label"] != "BENIGN").astype("int8")

    cache.parent.mkdir(exist_ok=True)
    df.to_pickle(cache)
    return df
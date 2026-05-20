"""Label and OneHot encoding for categorical features."""
import pickle
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


def encode_categoricals(
    df: pd.DataFrame,
    categorical_cols: list[str],
    fit: bool = True,
    encoders: dict | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Encode categorical columns using LabelEncoder per column."""
    df = df.copy()
    encoders = encoders or {}

    for col in categorical_cols:
        if col not in df.columns:
            continue
        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            le = encoders[col]
            df[col] = df[col].astype(str).map(
                {cls: i for i, cls in enumerate(le.classes_)}
            ).fillna(-1).astype(int)

    return df, encoders


def save_encoders(encoders: dict, path: Path) -> None:
    with open(path, "wb") as f:
        pickle.dump(encoders, f)


def load_encoders(path: Path) -> dict:
    with open(path, "rb") as f:
        return pickle.load(f)

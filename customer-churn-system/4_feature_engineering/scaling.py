"""StandardScaler for numeric features."""
import pickle
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_features(
    X: pd.DataFrame,
    fit: bool = True,
    scaler: StandardScaler | None = None,
) -> tuple[pd.DataFrame, StandardScaler]:
    """Scale numeric feature matrix."""
    scaler = scaler or StandardScaler()
    if fit:
        scaled = scaler.fit_transform(X)
    else:
        scaled = scaler.transform(X)
    return pd.DataFrame(scaled, columns=X.columns, index=X.index), scaler


def save_scaler(scaler: StandardScaler, path: Path) -> None:
    with open(path, "wb") as f:
        pickle.dump(scaler, f)


def load_scaler(path: Path) -> StandardScaler:
    with open(path, "rb") as f:
        return pickle.load(f)

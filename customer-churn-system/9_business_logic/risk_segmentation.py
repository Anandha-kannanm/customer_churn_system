"""Customer risk segmentation: High / Medium / Low."""
import pandas as pd


def segment_risk(churn_probabilities: pd.Series) -> pd.Series:
    """Assign risk segment labels based on churn probability."""
    return churn_probabilities.apply(_segment_single)


def _segment_single(proba: float) -> str:
    if proba >= 0.7:
        return "High"
    if proba >= 0.4:
        return "Medium"
    return "Low"


def segment_dataframe(df: pd.DataFrame, proba_col: str = "churn_probability") -> pd.DataFrame:
    """Add risk_segment column to dataframe."""
    df = df.copy()
    df["risk_segment"] = segment_risk(df[proba_col])
    return df


def segment_summary(df: pd.DataFrame, proba_col: str = "churn_probability") -> dict:
    """Return count and percentage per risk segment."""
    segmented = segment_dataframe(df, proba_col)
    counts = segmented["risk_segment"].value_counts().to_dict()
    total = len(segmented)
    return {
        segment: {"count": count, "pct": round(count / total * 100, 2)}
        for segment, count in counts.items()
    }

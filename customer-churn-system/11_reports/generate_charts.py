"""Generate report charts from processed data."""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "12_config"))
import config

df = pd.read_csv(config.PROCESSED_DATA_PATH)
config.CHARTS_DIR.mkdir(parents=True, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.countplot(data=df, x="Churn", ax=axes[0])
axes[0].set_title("Churn Distribution")
axes[0].set_xticklabels(["Retained", "Churned"])

df.groupby("Contract")["Churn"].mean().plot(kind="bar", ax=axes[1], color="steelblue")
axes[1].set_title("Churn Rate by Contract")
axes[1].set_ylabel("Churn Rate")

plt.tight_layout()
plt.savefig(config.CHARTS_DIR / "churn_overview.png", dpi=150)
plt.close()
print(f"Saved chart to {config.CHARTS_DIR / 'churn_overview.png'}")

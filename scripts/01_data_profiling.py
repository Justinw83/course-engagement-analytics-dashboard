import os
from pathlib import Path
import pandas as pd
import numpy as np

##### Load the Data #####

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Data file
DATA_PATH = ROOT_DIR / "data" / "raw" / "student_data.csv"

df = pd.read_csv(DATA_PATH)

quality_report = pd.DataFrame({
    "Metric": [
        "Row Count",
        "Column Count",
        "Duplicate Rows",
        "Missing Quiz Scores",
        "Missing Completion Rates",
        "Invalid Quiz Scores (>100)",
        "Invalid Completion Rates (>100)",
        "Invalid Quiz Scores (<0)",
        "Invalid Completion Rates (<0)",
        "Negative Time Spent"
    ],
    "Value": [
        len(df),
        len(df.columns),
        df.duplicated().sum(),
        df["QuizScores"].isna().sum(),
        df["CompletionRate"].isna().sum(),
        (df["QuizScores"] > 100).sum(),
        (df["CompletionRate"] > 100).sum(),
        (df["QuizScores"] < 0).sum(),
        (df["CompletionRate"] < 0).sum(),
        (df["TimeSpentOnCourse"] < 0).sum()
    ]
})

quality_report.to_csv(
    ROOT_DIR / "outputs" / "quality_report.csv",
    index=False
)

print(quality_report)

summary_stats = df.describe()

summary_stats.to_csv(
    ROOT_DIR / "outputs" / "summary_statistics.csv"
)

print(summary_stats)
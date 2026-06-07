import pandas as pd
import numpy as np
from pathlib import Path

##### Load the Data #####

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Data file
DATA_PATH = ROOT_DIR / "data" / "raw" / "student_data.csv"

df = pd.read_csv(DATA_PATH)

# Remove duplicates
df = df.drop_duplicates()

# Standardize category names
df["CourseCategory"] = (
    df["CourseCategory"]
    .str.strip() # Remove any extra leading or trailing whitespace
    .str.title() # Capitalize first letter and lowercase all others
)

# Fix invalid quiz scores
df.loc[
    (df["QuizScores"] > 100) |
    (df["QuizScores"] < 0),
    "QuizScores"
] = np.nan # Replace with null

# Fill quiz scores using category median
df["QuizScores"] = (
    df.groupby("CourseCategory")["QuizScores"]
      .transform(
          lambda x: x.fillna(x.median())
      )
)

# Fix invalid completion rates
df.loc[
    (df["CompletionRate"] > 100) |
    (df["CompletionRate"] < 0),
    "CompletionRate"
] = np.nan # Replace with null

# Fill completion rates with  median
df["CompletionRate"] = (
    df.groupby("CourseCategory")["CompletionRate"]
      .transform(
          lambda x: x.fillna(x.median())
      )
)

# Fix negative time spent
df.loc[
    df["TimeSpentOnCourse"] < 0,
    "TimeSpentOnCourse"
] = np.nan # Replace with null

# Fill time spent with median
df["TimeSpentOnCourse"] = (
    df.groupby("CourseCategory")["TimeSpentOnCourse"]
      .transform(
          lambda x: x.fillna(x.median())
      )
)

# Remove duplicates
df = df.drop_duplicates()

df.to_csv(
    ROOT_DIR / "data" / "clean" / "student_data_clean.csv",
    index=False
)

print("Cleaning complete.")
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# VACCINATION DATA ANALYTICS
# STEP 4: ADVANCED DATA CLEANING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


datasets = {
    "Coverage": "coverage-data.xlsx",
    "Incidence Rate": "incidence-rate-data.xlsx",
    "Reported Cases": "reported-cases-data.xlsx",
    "Vaccine Introduction": "vaccine-introduction-data.xlsx",
    "Vaccine Schedule": "vaccine-schedule-data.xlsx"
}


# ============================================================
# COMMON CLEANING
# ============================================================

def clean_common(df):

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove extra spaces from column names
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )

    # Clean text columns
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        # Convert empty strings to missing values
        df[column] = df[column].replace(
            ["", "NA", "N/A", "NULL", "NONE"],
            pd.NA
        )

    # Convert YEAR to numeric
    if "YEAR" in df.columns:

        df["YEAR"] = pd.to_numeric(
            df["YEAR"],
            errors="coerce"
        )

        # Keep realistic years only
        df.loc[
            ~df["YEAR"].between(1900, 2100),
            "YEAR"
        ] = np.nan

        df["YEAR"] = df["YEAR"].astype("Int64")

    return df


# ============================================================
# COVERAGE CLEANING
# ============================================================

def clean_coverage(df):

    numeric_columns = [
        "TARGET_NUMBER",
        "DOSES",
        "COVERAGE"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Negative doses are invalid
    if "DOSES" in df.columns:

        df.loc[
            df["DOSES"] < 0,
            "DOSES"
        ] = np.nan

    # Coverage should normally be between 0 and 100
    if "COVERAGE" in df.columns:

        df.loc[
            (df["COVERAGE"] < 0) |
            (df["COVERAGE"] > 100),
            "COVERAGE"
        ] = np.nan

    return df


# ============================================================
# INCIDENCE RATE CLEANING
# ============================================================

def clean_incidence(df):

    if "DENOMINATOR" in df.columns:

        df["DENOMINATOR"] = pd.to_numeric(
            df["DENOMINATOR"],
            errors="coerce"
        )

        df.loc[
            df["DENOMINATOR"] < 0,
            "DENOMINATOR"
        ] = np.nan

    if "INCIDENCE_RATE" in df.columns:

        df["INCIDENCE_RATE"] = pd.to_numeric(
            df["INCIDENCE_RATE"],
            errors="coerce"
        )

        df.loc[
            df["INCIDENCE_RATE"] < 0,
            "INCIDENCE_RATE"
        ] = np.nan

    return df


# ============================================================
# REPORTED CASES CLEANING
# ============================================================

def clean_cases(df):

    if "CASES" in df.columns:

        df["CASES"] = pd.to_numeric(
            df["CASES"],
            errors="coerce"
        )

        df.loc[
            df["CASES"] < 0,
            "CASES"
        ] = np.nan

    return df


# ============================================================
# VACCINE INTRODUCTION CLEANING
# ============================================================

def clean_introduction(df):

    # No aggressive imputation.
    # Missing descriptive information is preserved.

    return df


# ============================================================
# VACCINE SCHEDULE CLEANING
# ============================================================

def clean_schedule(df):

    numeric_columns = [
        "SCHEDULEROUNDS",
        "TARGETPOP",
        "GEOAREA",
        "AGEADMINISTERED"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Negative values are invalid
    for column in numeric_columns:

        if column in df.columns:

            df.loc[
                df[column] < 0,
                column
            ] = np.nan

    return df


# ============================================================
# PROCESS DATASETS
# ============================================================

cleaned_results = {}

for name, filename in datasets.items():

    print("\n" + "=" * 80)
    print(f"CLEANING: {name}")
    print("=" * 80)

    input_file = RAW_DIR / filename

    df = pd.read_excel(input_file)

    original_rows = len(df)

    # Common cleaning
    df = clean_common(df)

    # Dataset-specific cleaning
    if name == "Coverage":

        df = clean_coverage(df)

    elif name == "Incidence Rate":

        df = clean_incidence(df)

    elif name == "Reported Cases":

        df = clean_cases(df)

    elif name == "Vaccine Introduction":

        df = clean_introduction(df)

    elif name == "Vaccine Schedule":

        df = clean_schedule(df)

    # Remove rows where YEAR is missing
    if "YEAR" in df.columns:

        df = df.dropna(
            subset=["YEAR"]
        )

    # Remove duplicate rows
    duplicate_count = df.duplicated().sum()

    df = df.drop_duplicates()

    # Save cleaned dataset
    output_name = (
        filename
        .replace(".xlsx", "_cleaned.csv")
    )

    output_file = CLEAN_DIR / output_name

    df.to_csv(
        output_file,
        index=False
    )

    cleaned_results[name] = {
        "Original Rows": original_rows,
        "Cleaned Rows": len(df),
        "Duplicates Removed": duplicate_count,
        "Missing Cells": int(df.isna().sum().sum()),
        "Output": str(output_file)
    }

    print(f"Original rows       : {original_rows:,}")
    print(f"Cleaned rows        : {len(df):,}")
    print(f"Duplicates removed  : {duplicate_count:,}")
    print(
        f"Missing cells       : "
        f"{df.isna().sum().sum():,}"
    )
    print(f"Saved to            : {output_file}")


# ============================================================
# CLEANING SUMMARY
# ============================================================

summary = pd.DataFrame(
    cleaned_results
).T.reset_index()

summary = summary.rename(
    columns={"index": "Dataset"}
)

summary.to_csv(
    CLEAN_DIR / "cleaning_summary.csv",
    index=False
)


print("\n")
print("=" * 80)
print("ADVANCED DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 80)

print("\nCleaned files are available in:")
print(CLEAN_DIR)

print("\nGenerated files:")

for file in CLEAN_DIR.iterdir():

    print(" -", file.name)
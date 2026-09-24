import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# VACCINATION DATA ANALYTICS
# STEP 5: ADVANCED EXPLORATORY DATA ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CLEAN_DIR = BASE_DIR / "data" / "cleaned"
EDA_DIR = BASE_DIR / "data" / "eda"

# Create EDA folders
EDA_DIR.mkdir(parents=True, exist_ok=True)
(EDA_DIR / "figures").mkdir(parents=True, exist_ok=True)


# ============================================================
# DATASETS
# ============================================================

datasets = {
    "Coverage": "coverage-data_cleaned.csv",
    "Incidence Rate": "incidence-rate-data_cleaned.csv",
    "Reported Cases": "reported-cases-data_cleaned.csv",
    "Vaccine Introduction": "vaccine-introduction-data_cleaned.csv",
    "Vaccine Schedule": "vaccine-schedule-data_cleaned.csv"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_plot(filename):
    """
    Save the current matplotlib figure.
    """
    plt.tight_layout()

    path = EDA_DIR / "figures" / filename

    plt.savefig(
        path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


def find_column(df, possible_names):
    """
    Find the first matching column.
    """

    for name in possible_names:

        if name in df.columns:
            return name

    return None


def numeric_summary(df, dataset_name):
    """
    Generate descriptive statistics for numeric columns.
    """

    numeric_df = df.select_dtypes(
        include=np.number
    )

    if numeric_df.empty:
        return

    summary = numeric_df.describe().T

    summary["missing_values"] = numeric_df.isna().sum()

    summary["missing_percentage"] = (
        numeric_df.isna().mean() * 100
    )

    summary.to_csv(
        EDA_DIR /
        f"{dataset_name.lower().replace(' ', '_')}_numeric_summary.csv"
    )


# ============================================================
# LOAD DATA
# ============================================================

data = {}

print("\n" + "=" * 80)
print("LOADING CLEANED DATASETS")
print("=" * 80)

for name, filename in datasets.items():

    path = CLEAN_DIR / filename

    df = pd.read_csv(path)

    data[name] = df

    print(
        f"{name:<25} "
        f"{len(df):>10,} rows | "
        f"{len(df.columns):>3} columns"
    )


# ============================================================
# 1. DATASET OVERVIEW
# ============================================================

overview = []

for name, df in data.items():

    overview.append({
        "Dataset": name,
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing_Cells": int(df.isna().sum().sum()),
        "Duplicate_Rows": int(df.duplicated().sum())
    })

overview_df = pd.DataFrame(overview)

overview_df.to_csv(
    EDA_DIR / "eda_dataset_overview.csv",
    index=False
)


# ============================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 80)
print("DESCRIPTIVE STATISTICS")
print("=" * 80)

for name, df in data.items():

    print(f"\n{name}")

    numeric_summary(
        df,
        name
    )


# ============================================================
# 3. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("MISSING VALUE ANALYSIS")
print("=" * 80)

missing_records = []

for name, df in data.items():

    for column in df.columns:

        count = int(df[column].isna().sum())

        percentage = (
            count / len(df) * 100
            if len(df) > 0
            else 0
        )

        missing_records.append({
            "Dataset": name,
            "Column": column,
            "Missing_Count": count,
            "Missing_Percentage": round(
                percentage,
                2
            )
        })

missing_df = pd.DataFrame(
    missing_records
)

missing_df.to_csv(
    EDA_DIR / "missing_value_analysis.csv",
    index=False
)


# ============================================================
# 4. COVERAGE ANALYSIS
# ============================================================

coverage = data["Coverage"].copy()

print("\n" + "=" * 80)
print("COVERAGE ANALYSIS")
print("=" * 80)


year_col = find_column(
    coverage,
    ["YEAR"]
)

coverage_col = find_column(
    coverage,
    ["COVERAGE"]
)

name_col = find_column(
    coverage,
    ["NAME", "COUNTRYNAME", "COUNTRY"]
)

antigen_col = find_column(
    coverage,
    ["ANTIGEN", "VACCINECODE"]
)


# ------------------------------------------------------------
# 4A. YEAR-WISE COVERAGE
# ------------------------------------------------------------

if year_col and coverage_col:

    year_coverage = (
        coverage
        .dropna(subset=[year_col, coverage_col])
        .groupby(year_col)[coverage_col]
        .mean()
        .reset_index()
    )

    year_coverage.columns = [
        "YEAR",
        "AVERAGE_COVERAGE"
    ]

    year_coverage.to_csv(
        EDA_DIR / "year_wise_coverage.csv",
        index=False
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        year_coverage["YEAR"],
        year_coverage["AVERAGE_COVERAGE"],
        marker="o"
    )

    plt.title(
        "Average Vaccination Coverage by Year"
    )

    plt.xlabel("Year")
    plt.ylabel("Average Coverage (%)")

    plt.grid(True, alpha=0.3)

    save_plot(
        "01_year_wise_average_coverage.png"
    )


# ------------------------------------------------------------
# 4B. VACCINE-WISE COVERAGE
# ------------------------------------------------------------

if antigen_col and coverage_col:

    vaccine_coverage = (
        coverage
        .dropna(subset=[antigen_col, coverage_col])
        .groupby(antigen_col)[coverage_col]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    vaccine_coverage.columns = [
        "Vaccine",
        "Average_Coverage"
    ]

    vaccine_coverage.to_csv(
        EDA_DIR / "top_vaccines_by_coverage.csv",
        index=False
    )

    plt.figure(figsize=(11, 6))

    plt.bar(
        vaccine_coverage["Vaccine"].astype(str),
        vaccine_coverage["Average_Coverage"]
    )

    plt.title(
        "Top Vaccines by Average Coverage"
    )

    plt.xlabel("Vaccine")
    plt.ylabel("Average Coverage (%)")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "02_vaccine_coverage.png"
    )


# ------------------------------------------------------------
# 4C. COUNTRY-WISE COVERAGE
# ------------------------------------------------------------

if name_col and coverage_col:

    country_coverage = (
        coverage
        .dropna(subset=[name_col, coverage_col])
        .groupby(name_col)[coverage_col]
        .agg(
            Average_Coverage="mean",
            Records="count"
        )
        .sort_values(
            "Average_Coverage",
            ascending=False
        )
    )

    country_coverage = (
        country_coverage
        .head(20)
        .reset_index()
    )

    country_coverage.to_csv(
        EDA_DIR / "top_countries_by_coverage.csv",
        index=False
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        country_coverage[name_col].astype(str),
        country_coverage["Average_Coverage"]
    )

    plt.title(
        "Top Countries by Average Vaccination Coverage"
    )

    plt.xlabel("Average Coverage (%)")
    plt.ylabel("Country")

    plt.gca().invert_yaxis()

    save_plot(
        "03_top_countries_coverage.png"
    )


# ============================================================
# 5. INCIDENCE RATE ANALYSIS
# ============================================================

incidence = data["Incidence Rate"].copy()

print("\n" + "=" * 80)
print("INCIDENCE RATE ANALYSIS")
print("=" * 80)


year_col = find_column(
    incidence,
    ["YEAR"]
)

rate_col = find_column(
    incidence,
    ["INCIDENCE_RATE"]
)

disease_col = find_column(
    incidence,
    ["DISEASE"]
)


# ------------------------------------------------------------
# 5A. YEAR-WISE INCIDENCE
# ------------------------------------------------------------

if year_col and rate_col:

    incidence_year = (
        incidence
        .dropna(subset=[year_col, rate_col])
        .groupby(year_col)[rate_col]
        .mean()
        .reset_index()
    )

    incidence_year.columns = [
        "YEAR",
        "AVERAGE_INCIDENCE_RATE"
    ]

    incidence_year.to_csv(
        EDA_DIR / "year_wise_incidence_rate.csv",
        index=False
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        incidence_year["YEAR"],
        incidence_year["AVERAGE_INCIDENCE_RATE"],
        marker="o"
    )

    plt.title(
        "Average Disease Incidence Rate by Year"
    )

    plt.xlabel("Year")
    plt.ylabel("Incidence Rate")

    plt.grid(True, alpha=0.3)

    save_plot(
        "04_year_wise_incidence_rate.png"
    )


# ------------------------------------------------------------
# 5B. DISEASE-WISE INCIDENCE
# ------------------------------------------------------------

if disease_col and rate_col:

    disease_incidence = (
        incidence
        .dropna(subset=[disease_col, rate_col])
        .groupby(disease_col)[rate_col]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    disease_incidence.columns = [
        "Disease",
        "Average_Incidence_Rate"
    ]

    disease_incidence.to_csv(
        EDA_DIR / "top_diseases_by_incidence.csv",
        index=False
    )

    plt.figure(figsize=(11, 6))

    plt.bar(
        disease_incidence["Disease"].astype(str),
        disease_incidence["Average_Incidence_Rate"]
    )

    plt.title(
        "Diseases with Highest Average Incidence Rate"
    )

    plt.xlabel("Disease")
    plt.ylabel("Average Incidence Rate")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "05_disease_incidence.png"
    )


# ============================================================
# 6. REPORTED CASES ANALYSIS
# ============================================================

cases = data["Reported Cases"].copy()

print("\n" + "=" * 80)
print("REPORTED CASES ANALYSIS")
print("=" * 80)


year_col = find_column(
    cases,
    ["YEAR"]
)

cases_col = find_column(
    cases,
    ["CASES"]
)

disease_col = find_column(
    cases,
    ["DISEASE"]
)


# ------------------------------------------------------------
# 6A. YEAR-WISE CASES
# ------------------------------------------------------------

if year_col and cases_col:

    year_cases = (
        cases
        .dropna(subset=[year_col, cases_col])
        .groupby(year_col)[cases_col]
        .sum()
        .reset_index()
    )

    year_cases.columns = [
        "YEAR",
        "TOTAL_CASES"
    ]

    year_cases.to_csv(
        EDA_DIR / "year_wise_reported_cases.csv",
        index=False
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        year_cases["YEAR"],
        year_cases["TOTAL_CASES"],
        marker="o"
    )

    plt.title(
        "Reported Vaccination-Related Cases by Year"
    )

    plt.xlabel("Year")
    plt.ylabel("Total Cases")

    plt.grid(True, alpha=0.3)

    save_plot(
        "06_year_wise_reported_cases.png"
    )


# ------------------------------------------------------------
# 6B. DISEASE-WISE CASES
# ------------------------------------------------------------

if disease_col and cases_col:

    disease_cases = (
        cases
        .dropna(subset=[disease_col, cases_col])
        .groupby(disease_col)[cases_col]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    disease_cases.columns = [
        "Disease",
        "Total_Cases"
    ]

    disease_cases.to_csv(
        EDA_DIR / "top_diseases_by_cases.csv",
        index=False
    )

    plt.figure(figsize=(11, 6))

    plt.bar(
        disease_cases["Disease"].astype(str),
        disease_cases["Total_Cases"]
    )

    plt.title(
        "Diseases with Highest Reported Cases"
    )

    plt.xlabel("Disease")
    plt.ylabel("Total Cases")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "07_disease_reported_cases.png"
    )


# ============================================================
# 7. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("CORRELATION ANALYSIS")
print("=" * 80)

correlation_records = []

for name, df in data.items():

    numeric_df = df.select_dtypes(
        include=np.number
    )

    if numeric_df.shape[1] >= 2:

        corr = numeric_df.corr()

        output_name = (
            name.lower()
            .replace(" ", "_")
            + "_correlation.csv"
        )

        corr.to_csv(
            EDA_DIR / output_name
        )

        for column1 in corr.columns:

            for column2 in corr.columns:

                if column1 < column2:

                    correlation_records.append({
                        "Dataset": name,
                        "Variable_1": column1,
                        "Variable_2": column2,
                        "Correlation": corr.loc[
                            column1,
                            column2
                        ]
                    })


correlation_df = pd.DataFrame(
    correlation_records
)

if not correlation_df.empty:

    correlation_df.to_csv(
        EDA_DIR / "all_correlations.csv",
        index=False
    )


# ============================================================
# 8. OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("OUTLIER ANALYSIS")
print("=" * 80)

outlier_records = []

for name, df in data.items():

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = (
            (series < lower_bound) |
            (series > upper_bound)
        )

        count = int(outliers.sum())

        outlier_records.append({
            "Dataset": name,
            "Column": column,
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "Lower_Bound": lower_bound,
            "Upper_Bound": upper_bound,
            "Outlier_Count": count,
            "Outlier_Percentage": (
                count / len(series) * 100
            )
        })


outlier_df = pd.DataFrame(
    outlier_records
)

outlier_df.to_csv(
    EDA_DIR / "outlier_analysis.csv",
    index=False
)


# ============================================================
# 9. DATASET SIZE VISUALIZATION
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    overview_df["Dataset"],
    overview_df["Rows"]
)

plt.title(
    "Dataset Size Comparison"
)

plt.xlabel("Dataset")
plt.ylabel("Number of Rows")

plt.xticks(
    rotation=30,
    ha="right"
)

save_plot(
    "08_dataset_size_comparison.png"
)


# ============================================================
# 10. MISSING VALUE VISUALIZATION
# ============================================================

missing_plot = (
    missing_df
    .sort_values(
        "Missing_Percentage",
        ascending=False
    )
    .head(20)
)

plt.figure(figsize=(12, 7))

labels = (
    missing_plot["Dataset"]
    + " - "
    + missing_plot["Column"]
)

plt.barh(
    labels,
    missing_plot["Missing_Percentage"]
)

plt.title(
    "Top Missing-Value Fields"
)

plt.xlabel(
    "Missing Values (%)"
)

plt.ylabel(
    "Dataset - Column"
)

plt.gca().invert_yaxis()

save_plot(
    "09_missing_value_analysis.png"
)


# ============================================================
# 11. FINAL EDA SUMMARY
# ============================================================

summary = {
    "Total_Datasets": len(data),
    "Total_Rows": sum(
        len(df)
        for df in data.values()
    ),
    "Total_Missing_Cells": sum(
        int(df.isna().sum().sum())
        for df in data.values()
    ),
    "Total_Duplicate_Rows": sum(
        int(df.duplicated().sum())
        for df in data.values()
    ),
    "Generated_At": pd.Timestamp.now()
}

summary_df = pd.DataFrame(
    [summary]
)

summary_df.to_csv(
    EDA_DIR / "advanced_eda_summary.csv",
    index=False
)


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n")
print("=" * 80)
print("ADVANCED EDA COMPLETED SUCCESSFULLY")
print("=" * 80)

print("\nEDA files saved in:")
print(EDA_DIR)

print("\nFigures saved in:")
print(EDA_DIR / "figures")

print("\nGenerated analysis includes:")
print("1. Dataset overview")
print("2. Descriptive statistics")
print("3. Missing-value analysis")
print("4. Year-wise vaccination coverage")
print("5. Vaccine-wise coverage")
print("6. Country-wise coverage")
print("7. Incidence-rate trends")
print("8. Disease-wise incidence")
print("9. Reported cases trends")
print("10. Disease-wise reported cases")
print("11. Correlation analysis")
print("12. IQR-based outlier analysis")
print("13. Dataset-size visualization")
print("14. Missing-value visualization")

print("\n" + "=" * 80)
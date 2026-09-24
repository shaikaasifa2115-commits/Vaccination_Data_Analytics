import pandas as pd
from pathlib import Path

# ============================================================
# VACCINATION DATA ANALYTICS PROJECT
# STEP 1: ADVANCED DATA PROFILING & QUALITY ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("       VACCINATION DATA ANALYTICS - DATA PROFILING")
print("=" * 80)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

# Create cleaned folder if it doesn't exist
CLEANED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. DATASET FILES
# ============================================================

datasets = {
    "Coverage": "coverage-data.xlsx",
    "Incidence Rate": "incidence-rate-data.xlsx",
    "Reported Cases": "reported-cases-data.xlsx",
    "Vaccine Introduction": "vaccine-introduction-data.xlsx",
    "Vaccine Schedule": "vaccine-schedule-data.xlsx"
}


# ============================================================
# 3. STORAGE FOR DATA QUALITY RESULTS
# ============================================================

dataframes = {}

quality_reports = []


# ============================================================
# 4. FUNCTION TO PROFILE DATASET
# ============================================================

def profile_dataset(dataset_name, filename):

    file_path = RAW_DIR / filename

    print("\n" + "=" * 80)
    print(f"DATASET: {dataset_name}")
    print("=" * 80)

    # --------------------------------------------------------
    # Check whether file exists
    # --------------------------------------------------------

    if not file_path.exists():

        print(f"ERROR: File not found:")
        print(file_path)

        return None

    # --------------------------------------------------------
    # Load Excel file
    # --------------------------------------------------------

    print("\nLoading dataset...")

    df = pd.read_excel(file_path)

    print("Dataset loaded successfully.")


    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    rows = df.shape[0]
    columns = df.shape[1]

    print(f"\nNumber of Rows    : {rows:,}")
    print(f"Number of Columns : {columns}")


    # --------------------------------------------------------
    # Column information
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("COLUMN INFORMATION")
    print("-" * 60)

    for column in df.columns:

        print(
            f"{column} | "
            f"Type: {df[column].dtype} | "
            f"Unique: {df[column].nunique(dropna=True):,}"
        )


    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("MISSING VALUE ANALYSIS")
    print("-" * 60)

    missing_count = df.isna().sum()

    missing_percentage = (
        df.isna().mean() * 100
    ).round(2)

    missing_data = pd.DataFrame({

        "Column": df.columns,

        "Missing_Count": missing_count.values,

        "Missing_Percentage": missing_percentage.values

    })

    missing_data = missing_data[
        missing_data["Missing_Count"] > 0
    ]

    if missing_data.empty:

        print("No missing values found.")

    else:

        print(missing_data.to_string(index=False))


    # --------------------------------------------------------
    # Duplicate analysis
    # --------------------------------------------------------

    duplicate_count = df.duplicated().sum()

    print("\n" + "-" * 60)
    print("DUPLICATE ANALYSIS")
    print("-" * 60)

    print(f"Duplicate Rows: {duplicate_count:,}")


    # --------------------------------------------------------
    # Numerical analysis
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) > 0:

        print("\n" + "-" * 60)
        print("NUMERICAL SUMMARY")
        print("-" * 60)

        print(
            df[numeric_columns]
            .describe()
            .round(2)
            .to_string()
        )


    # --------------------------------------------------------
    # Generate quality report for every column
    # --------------------------------------------------------

    for column in df.columns:

        quality_reports.append({

            "Dataset": dataset_name,

            "Column": column,

            "Data_Type": str(
                df[column].dtype
            ),

            "Total_Rows": len(df),

            "Missing_Count": int(
                df[column].isna().sum()
            ),

            "Missing_Percentage": round(
                df[column].isna().mean() * 100,
                2
            ),

            "Unique_Values": int(
                df[column].nunique(
                    dropna=True
                )
            ),

            "Duplicate_Rows_In_Dataset": int(
                duplicate_count
            )

        })


    # --------------------------------------------------------
    # Display sample data
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("FIRST 5 RECORDS")
    print("-" * 60)

    print(
        df.head()
        .to_string(index=False)
    )


    # --------------------------------------------------------
    # Store dataframe
    # --------------------------------------------------------

    dataframes[dataset_name] = df

    return df


# ============================================================
# 5. PROFILE ALL DATASETS
# ============================================================

for dataset_name, filename in datasets.items():

    try:

        profile_dataset(
            dataset_name,
            filename
        )

    except Exception as error:

        print("\nERROR PROCESSING DATASET")
        print(f"Dataset: {dataset_name}")
        print(f"Error: {error}")


# ============================================================
# 6. CREATE DATA QUALITY REPORT
# ============================================================

print("\n" + "=" * 80)
print("CREATING DATA QUALITY REPORT")
print("=" * 80)


if quality_reports:

    quality_report_df = pd.DataFrame(
        quality_reports
    )

    report_path = (
        CLEANED_DIR /
        "data_quality_report.csv"
    )

    quality_report_df.to_csv(
        report_path,
        index=False
    )

    print(
        "\nData quality report created successfully:"
    )

    print(report_path)

else:

    print(
        "\nNo quality report was generated."
    )


# ============================================================
# 7. CREATE DATASET SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("DATASET SUMMARY")
print("=" * 80)


summary = []


for dataset_name, df in dataframes.items():

    summary.append({

        "Dataset": dataset_name,

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Duplicate_Rows": int(
            df.duplicated().sum()
        ),

        "Total_Missing_Values": int(
            df.isna().sum().sum()
        )

    })


summary_df = pd.DataFrame(summary)


summary_path = (
    CLEANED_DIR /
    "dataset_summary.csv"
)


summary_df.to_csv(
    summary_path,
    index=False
)


print("\nDataset summary:")

print(
    summary_df.to_string(
        index=False
    )
)


# ============================================================
# 8. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 80)
print("DATA PROFILING COMPLETED SUCCESSFULLY")
print("=" * 80)

print("\nGenerated files:")

print(
    "1. data/cleaned/data_quality_report.csv"
)

print(
    "2. data/cleaned/dataset_summary.csv"
)

print("\nNext step: Advanced data validation and cleaning.")
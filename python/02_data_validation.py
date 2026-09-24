import pandas as pd
from pathlib import Path

# ============================================================
# VACCINATION DATA ANALYTICS PROJECT
# STEP 2: ADVANCED DATA VALIDATION
# ============================================================

print("\n" + "=" * 80)
print("        ADVANCED DATA VALIDATION")
print("=" * 80)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

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
# 3. VALIDATION RESULTS
# ============================================================

validation_results = []


# ============================================================
# 4. HELPER FUNCTION
# ============================================================

def add_result(dataset, check, status, details):

    validation_results.append({
        "Dataset": dataset,
        "Validation_Check": check,
        "Status": status,
        "Details": details
    })


# ============================================================
# 5. VALIDATE EACH DATASET
# ============================================================

for dataset_name, filename in datasets.items():

    print("\n" + "=" * 80)
    print(f"VALIDATING: {dataset_name}")
    print("=" * 80)

    file_path = RAW_DIR / filename

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not file_path.exists():

        print("ERROR: File not found.")

        add_result(
            dataset_name,
            "File Exists",
            "FAIL",
            f"File not found: {filename}"
        )

        continue

    add_result(
        dataset_name,
        "File Exists",
        "PASS",
        "Dataset file found."
    )


    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    try:

        df = pd.read_excel(file_path)

        print(
            f"Rows: {len(df):,} | "
            f"Columns: {len(df.columns)}"
        )

    except Exception as error:

        add_result(
            dataset_name,
            "File Read",
            "FAIL",
            str(error)
        )

        continue


    # ========================================================
    # CHECK 1 — DUPLICATES
    # ========================================================

    duplicates = df.duplicated().sum()

    if duplicates == 0:

        status = "PASS"
        details = "No duplicate rows found."

    else:

        status = "WARNING"
        details = f"{duplicates:,} duplicate rows found."

    add_result(
        dataset_name,
        "Duplicate Rows",
        status,
        details
    )


    # ========================================================
    # CHECK 2 — MISSING VALUES
    # ========================================================

    missing_total = df.isna().sum().sum()

    missing_percentage = (
        missing_total /
        (df.shape[0] * df.shape[1])
    ) * 100

    if missing_total == 0:

        status = "PASS"

    elif missing_percentage < 5:

        status = "WARNING"

    else:

        status = "REVIEW"

    details = (
        f"{missing_total:,} missing cells "
        f"({missing_percentage:.2f}%)."
    )

    add_result(
        dataset_name,
        "Missing Values",
        status,
        details
    )


    # ========================================================
    # CHECK 3 — YEAR VALIDATION
    # ========================================================

    if "YEAR" in df.columns:

        year_numeric = pd.to_numeric(
            df["YEAR"],
            errors="coerce"
        )

        invalid_years = (
            year_numeric.isna().sum()
        )

        out_of_range_years = (
            (year_numeric < 1900) |
            (year_numeric > 2100)
        ).sum()

        if invalid_years == 0 and out_of_range_years == 0:

            status = "PASS"

            details = (
                f"Valid year values. "
                f"Range: {year_numeric.min():.0f} - "
                f"{year_numeric.max():.0f}."
            )

        else:

            status = "REVIEW"

            details = (
                f"Invalid/missing years: "
                f"{invalid_years:,}; "
                f"out-of-range years: "
                f"{out_of_range_years:,}."
            )

        add_result(
            dataset_name,
            "Year Validation",
            status,
            details
        )


    # ========================================================
    # CHECK 4 — COVERAGE VALIDATION
    # ========================================================

    if "COVERAGE" in df.columns:

        coverage = pd.to_numeric(
            df["COVERAGE"],
            errors="coerce"
        )

        invalid_coverage = (
            (coverage < 0) |
            (coverage > 100)
        ).sum()

        if invalid_coverage == 0:

            status = "PASS"

            details = (
                "Coverage values are within "
                "the expected 0-100 range."
            )

        else:

            status = "REVIEW"

            details = (
                f"{invalid_coverage:,} "
                "coverage values outside 0-100."
            )

        add_result(
            dataset_name,
            "Coverage Range",
            status,
            details
        )


    # ========================================================
    # CHECK 5 — NEGATIVE NUMERIC VALUES
    # ========================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    negative_values = 0

    for column in numeric_columns:

        negative_values += (
            df[column] < 0
        ).sum()

    if negative_values == 0:

        status = "PASS"

        details = "No negative numeric values found."

    else:

        status = "REVIEW"

        details = (
            f"{negative_values:,} negative "
            "numeric values found."
        )

    add_result(
        dataset_name,
        "Negative Values",
        status,
        details
    )


    # ========================================================
    # CHECK 6 — EMPTY COLUMNS
    # ========================================================

    empty_columns = [
        column
        for column in df.columns
        if df[column].isna().all()
    ]

    if len(empty_columns) == 0:

        status = "PASS"
        details = "No completely empty columns."

    else:

        status = "REVIEW"
        details = (
            "Empty columns: "
            + ", ".join(empty_columns)
        )

    add_result(
        dataset_name,
        "Empty Columns",
        status,
        details
    )


    # ========================================================
    # CHECK 7 — CONSTANT COLUMNS
    # ========================================================

    constant_columns = [
        column
        for column in df.columns
        if df[column].nunique(dropna=True) <= 1
    ]

    if len(constant_columns) == 0:

        status = "PASS"
        details = "No constant columns found."

    else:

        status = "REVIEW"
        details = (
            "Constant columns: "
            + ", ".join(constant_columns)
        )

    add_result(
        dataset_name,
        "Constant Columns",
        status,
        details
    )


    print("Validation completed.")


# ============================================================
# 6. SAVE VALIDATION REPORT
# ============================================================

validation_df = pd.DataFrame(
    validation_results
)

validation_path = (
    CLEANED_DIR /
    "data_validation_report.csv"
)

validation_df.to_csv(
    validation_path,
    index=False
)


# ============================================================
# 7. DISPLAY SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

print(
    validation_df[
        [
            "Dataset",
            "Validation_Check",
            "Status"
        ]
    ].to_string(index=False)
)


# ============================================================
# 8. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 80)
print("ADVANCED DATA VALIDATION COMPLETED")
print("=" * 80)

print("\nReport saved at:")

print(validation_path)
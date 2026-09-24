import pandas as pd
from pathlib import Path

# ============================================================
# VACCINATION DATA ANALYTICS
# STEP 3: DETAILED DATA DIAGNOSTICS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

datasets = {
    "Coverage": "coverage-data.xlsx",
    "Incidence Rate": "incidence-rate-data.xlsx",
    "Reported Cases": "reported-cases-data.xlsx",
    "Vaccine Introduction": "vaccine-introduction-data.xlsx",
    "Vaccine Schedule": "vaccine-schedule-data.xlsx"
}


def inspect_dataset(name, filename):

    print("\n" + "=" * 80)
    print(f"DATASET: {name}")
    print("=" * 80)

    df = pd.read_excel(RAW_DIR / filename)

    # --------------------------------------------------------
    # Missing values by column
    # --------------------------------------------------------

    print("\nMISSING VALUES BY COLUMN")
    print("-" * 60)

    missing = pd.DataFrame({
        "Missing_Count": df.isna().sum(),
        "Missing_Percentage": (
            df.isna().mean() * 100
        ).round(2)
    })

    missing = missing[
        missing["Missing_Count"] > 0
    ]

    if missing.empty:
        print("No missing values.")

    else:
        print(missing.to_string())


    # --------------------------------------------------------
    # YEAR problems
    # --------------------------------------------------------

    if "YEAR" in df.columns:

        year = pd.to_numeric(
            df["YEAR"],
            errors="coerce"
        )

        invalid_year = df[
            year.isna()
        ]

        print("\nYEAR PROBLEMS")
        print("-" * 60)

        print(
            f"Invalid/missing YEAR records: "
            f"{len(invalid_year)}"
        )

        if len(invalid_year) > 0:
            print(invalid_year.to_string(index=False))


    # --------------------------------------------------------
    # COVERAGE problems
    # --------------------------------------------------------

    if "COVERAGE" in df.columns:

        coverage = pd.to_numeric(
            df["COVERAGE"],
            errors="coerce"
        )

        invalid_coverage = df[
            (coverage < 0) |
            (coverage > 100)
        ]

        print("\nINVALID COVERAGE VALUES")
        print("-" * 60)

        print(
            f"Invalid coverage records: "
            f"{len(invalid_coverage)}"
        )

        if len(invalid_coverage) > 0:

            columns_to_show = [
                column
                for column in [
                    "CODE",
                    "NAME",
                    "YEAR",
                    "ANTIGEN",
                    "COVERAGE_CATEGORY",
                    "TARGET_NUMBER",
                    "DOSES",
                    "COVERAGE"
                ]
                if column in df.columns
            ]

            print(
                invalid_coverage[
                    columns_to_show
                ].head(20).to_string(index=False)
            )


    # --------------------------------------------------------
    # NEGATIVE NUMERIC VALUES
    # --------------------------------------------------------

    print("\nNEGATIVE NUMERIC VALUES")
    print("-" * 60)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    negative_found = False

    for column in numeric_columns:

        negative_rows = df[
            df[column] < 0
        ]

        if len(negative_rows) > 0:

            negative_found = True

            print(
                f"{column}: "
                f"{len(negative_rows)} negative values"
            )

            print(
                negative_rows[
                    [column]
                ].head(10).to_string(index=False)
            )

    if not negative_found:
        print("No negative numeric values.")


    # --------------------------------------------------------
    # DATASET SHAPE
    # --------------------------------------------------------

    print("\nDATASET SIZE")
    print("-" * 60)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")


# ============================================================
# RUN DIAGNOSTICS
# ============================================================

for name, filename in datasets.items():

    try:

        inspect_dataset(
            name,
            filename
        )

    except Exception as error:

        print(
            f"\nERROR processing {name}:"
        )

        print(error)


print("\n" + "=" * 80)
print("DETAILED DIAGNOSTICS COMPLETED")
print("=" * 80)
import os
import click
import pandas as pd
import pandera as pa


@click.command()
@click.option('--input_path', type=str, required=True, help='Path to the raw data file.')
@click.option('--output_path', type=str, required=True, help='Path to save the cleaned data.')
def clean_validate_save_data(input_path, output_path):
    """
    Cleans and validates the raw data, then saves it as a processed file.
    """
    col_names = [
        "id", "age_group", "age", "gender", "weekly_physical_activity",
        "bmi", "blood_glucose_fasting", "diabetic", "oral", "insulin_level"
    ]
    
    data = pd.read_csv(input_path, names=col_names, skiprows=1).drop(columns=["id", "age"])
    data["gender"] = data["gender"].replace({1: "Male", 2: "Female"})
    data["weekly_physical_activity"] = data["weekly_physical_activity"].replace({1: "Yes", 2: "No"})
    data["diabetic"] = data["diabetic"].replace({1: "Yes", 2: "No", 3: "Borderline"})
    data = data[data["weekly_physical_activity"] != 7.0]

    # Validation

    MISSINGNESS_THRESHOLD = 0.2

    schema = pa.DataFrameSchema({
        "age_group": pa.Column(str, pa.Check.isin(["Adult", "Senior"])),
        "gender": pa.Column(str, pa.Check.isin(["Female", "Male"]), nullable=True),
        "weekly_physical_activity": pa.Column(str, pa.Check.isin(["No", "Yes"]), nullable=True),
        "bmi": pa.Column(float, pa.Check.between(14.5, 70.1), nullable=True),
        "blood_glucose_fasting": pa.Column(float, pa.Check.between(63.0, 405.0), nullable=True),
        "diabetic": pa.Column(str, pa.Check.isin(["No", "Yes", "Borderline"]), nullable=True),
        "oral": pa.Column(float, pa.Check.between(40.0, 604.0), nullable=True),
        "insulin_level": pa.Column(float, pa.Check.between(0.14, 102.29), nullable=True)
    }, strict=True,
    checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
        pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        pa.Check(lambda df: df.apply(lambda col: col.isnull().mean() <= MISSINGNESS_THRESHOLD).all(),
            error=f"One or more columns have missing values above {MISSINGNESS_THRESHOLD*100:.1f}% threshold.")
    ]
    )
    
    validated_data = schema.validate(data, lazy=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    validated_data.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    clean_validate_save_data()

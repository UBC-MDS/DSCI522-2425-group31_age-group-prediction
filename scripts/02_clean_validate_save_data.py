import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import click
import pandas as pd
from src.validate_data import validate_data


@click.command()
@click.option('--input_path', type=str, required=True, help='Path to the raw data file.')
@click.option('--output_path', type=str, required=True, help='Path to save the cleaned data.')
def clean_and_save_data(input_path, output_path):
    """
    Cleans the raw data, validates it, and then saves it as a processed file.
    """
    col_names = [
        "id", "age_group", "age", "gender", "weekly_physical_activity",
        "bmi", "blood_glucose_fasting", "diabetic", "oral", "insulin_level"
    ]
    
    # Load the data
    data = pd.read_csv(input_path, names=col_names, skiprows=1).drop(columns=["id", "age"])
    data["gender"] = data["gender"].replace({1: "Male", 2: "Female"})
    data["weekly_physical_activity"] = data["weekly_physical_activity"].replace({1: "Yes", 2: "No"})
    data["diabetic"] = data["diabetic"].replace({1: "Yes", 2: "No", 3: "Borderline"})
    data = data[data["weekly_physical_activity"] != 7.0]

    # Validate the cleaned data using the validation function from validate_data
    validated_data = validate_data(data)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the validated data
    validated_data.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    clean_and_save_data()

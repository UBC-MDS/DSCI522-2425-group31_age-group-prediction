import os
import sys
import pandas as pd
import click
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.second_validate_data import second_validate_data 

@click.command()
@click.option('--data_train_path', type=str, required=True, help='Path to the training data CSV file.')
def simple_eda_with_validation(data_train_path):
    """
    Performs simple EDA and validation checks.
    """
    # Load data
    data_train = pd.read_csv(data_train_path)

    # Basic dataset overview
    print("\nDataset Info:")
    print(data_train.info())
    print("\nDataset Description:")
    print(data_train.describe())

    # Value counts for categorical columns
    for col in ["age_group", "gender", "diabetic", "weekly_physical_activity"]:
        print(f"\nValue Counts for {col}:")
        print(data_train[col].value_counts())

    # Validation checks
    print("\nRunning correlation validation checks...")
    second_validate_data(data_train)

    print("\nSimple EDA and validation completed successfully.")

if __name__ == "__main__":
    simple_eda_with_validation()

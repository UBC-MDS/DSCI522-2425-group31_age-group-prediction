import os
import click
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import set_config

@click.command()
@click.option('--input_path', type=str, required=True, help='Path to the cleaned data file.')
@click.option('--output_dir', type=str, required=True, help='Directory to save the split datasets.')
@click.option('--seed', type=int, required=True, help='Random seed for reproducibility.')
def split_preprocess_data(input_path, output_dir, seed):
    """
    Splits the cleaned data into training and testing datasets and saves them.
    """
    np.random.seed(seed)
    set_config(transform_output="pandas")
    
    # Load data
    data = pd.read_csv(input_path)

    # Split the data
    data_train, data_test = train_test_split(
        data, train_size=0.75, stratify=data["age_group"], random_state=42
    )

    # Save datasets
    train_path = os.path.join(output_dir, "data_train.csv")
    test_path = os.path.join(output_dir, "data_test.csv")
    os.makedirs(output_dir, exist_ok=True)

    data_train.to_csv(train_path, index=False)
    data_test.to_csv(test_path, index=False)

    print(f"Training data saved to {train_path}")
    print(f"Testing data saved to {test_path}")

if __name__ == "__main__":
    split_preprocess_data()

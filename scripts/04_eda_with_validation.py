import pandas as pd
import click
from deepchecks.tabular.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation
from deepchecks.tabular import Dataset

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

    # Correlation validation
    print("\nRunning correlation validation checks...")
    data_train_ds = Dataset(data_train, label="age_group", cat_features=[])

    # Feature-Label Correlation
    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.9)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset=data_train_ds)

    if not check_feat_lab_corr_result.passed_conditions():
        raise ValueError("Feature-Label correlation exceeds the maximum acceptable threshold.")

    # Feature-Feature Correlation
    check_feat_feat_corr = FeatureFeatureCorrelation().add_condition_max_number_of_pairs_above_threshold(threshold=0.92, n_pairs=0)
    check_feat_feat_corr_result = check_feat_feat_corr.run(dataset=data_train_ds)

    if not check_feat_feat_corr_result.passed_conditions():
        raise ValueError("Feature-Feature correlation exceeds the maximum acceptable threshold.")

    print("\nSimple EDA and validation completed successfully.")

if __name__ == "__main__":
    simple_eda_with_validation()

# 07_model_evaluation.py
# author: Dongchun Chen
# date: 2024-12-07

import click
import os
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.write_csv import write_csv


@click.command()
@click.option('--train-data', type=str, help="Path to training data (optional, for reference)")
@click.option('--test-data', type=str, help="Path to test data")
@click.option('--results-to', type=str, help="Path to directory where results will be saved")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(train_data, test_data, results_to, seed):
    """
    Evaluate a Logistic Regression model directly in the script.

    This script integrates preprocessing, model definition, and evaluation into one place.
    It avoids compatibility issues with pre-saved pipelines by rebuilding the pipeline 
    before evaluation.

    Args:
        train_data (str): Path to the CSV file containing the training dataset 
            (optional, for reference).
        test_data (str): Path to the CSV file containing the test dataset. 
            The dataset must include numeric, categorical, and ordinal features, 
            along with the target column `age_group`.
        results_to (str): Directory path where the evaluation results will be saved 
            as CSV files.
        seed (int, optional): Random seed for reproducibility. Defaults to 123.

    Returns:
        None: Saves evaluation results (confusion matrix and classification report) as CSV files.
    """
    np.random.seed(seed)

    # Define feature groups
    numeric_features = ['bmi', 'blood_glucose_fasting', 'oral', 'insulin_level']
    categorical_features = ['weekly_physical_activity', 'gender']
    ordinal_features = ['diabetic']
    drop_features = []

    # Preprocessing pipelines
    numeric_transformer = StandardScaler()
    ordinal_transformer = OrdinalEncoder(categories=[['No', 'Borderline', 'Yes']], dtype=int)
    categorical_transformer = make_pipeline(
        SimpleImputer(strategy='constant', fill_value='missing'),
        OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    )

    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (ordinal_transformer, ordinal_features),
        (categorical_transformer, categorical_features),
        ("drop", drop_features),
    )

    # Define Logistic Regression pipeline
    lgr_classifier = LogisticRegression(max_iter=2000, random_state=seed, class_weight='balanced')
    pipe = make_pipeline(preprocessor, lgr_classifier)

    # Load test data
    data_test = pd.read_csv(test_data)
    target = 'age_group'
    X_test, y_test = data_test.drop(columns=[target]), data_test[target]

    # Reorder and align test data
    expected_features = numeric_features + categorical_features + ordinal_features
    for col in expected_features:
        if col not in X_test.columns:
            print(f"Adding missing column: {col}")
            X_test[col] = 0  # Default value for missing features
    X_test = X_test[expected_features]

    # Fit pipeline (on optional train data, if provided)
    if train_data:
        data_train = pd.read_csv(train_data)
        X_train, y_train = data_train.drop(columns=[target]), data_train[target]
        pipe.fit(X_train, y_train)
    else:
        print("No training data provided. Using default parameters.")

    # Predict on test data
    y_pred_test = pipe.predict(X_test)

    # Evaluate and save results
    cm = confusion_matrix(y_test, y_pred_test)
    cm_df = pd.DataFrame(cm, index=pipe.classes_, columns=pipe.classes_)
    write_csv(cm_df, results_to, "confusion_matrix.csv", index=True)

    report = classification_report(y_test, y_pred_test, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    write_csv(report_df, results_to, "age_model_report.csv", index=True)


if __name__ == '__main__':
    main()

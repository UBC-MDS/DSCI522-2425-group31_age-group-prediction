# 07_model_evaluation.py
# author: Dongchun Chen
# date: 2024-12-07

import click
import os
import sys
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.write_csv import write_csv


@click.command()
@click.option('--model-path', type=str, help="Path to the saved GridSearchCV pipeline (pickle file)")
@click.option('--test-data', type=str, help="Path to test data")
@click.option('--results-to', type=str, help="Path to directory where results will be saved")
def main(model_path, test_data, results_to):
    """
    Evaluate a pre-trained GridSearchCV pipeline.

    Args:
        model_path (str): Path to the saved GridSearchCV object (pickle file).
        test_data (str): Path to the CSV file containing the test dataset. 
            The dataset must include numeric, categorical, and ordinal features, 
            along with the target column `age_group`.
        results_to (str): Directory path where the evaluation results will be saved 
            as CSV files.

    Returns:
        None: Saves evaluation results (confusion matrix and classification report) as CSV files.
    """
    # Load the GridSearchCV object
    with open(model_path, 'rb') as f:
        grid_search = pickle.load(f)

    # Get the best pipeline
    pipe = grid_search.best_estimator_

    # Load test data
    data_test = pd.read_csv(test_data)
    target = 'age_group'
    X_test, y_test = data_test.drop(columns=[target]), data_test[target]

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
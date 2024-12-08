# evaluate_age_group_classifier.py
# author: Dongchun Chen
# date: 2024-12-07

import click
import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
import pickle
from sklearn import set_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.write_csv import write_csv


@click.command()
@click.option('--test-data', type=str, help="Path to test data")
@click.option('--pipeline-from', type=str, help="Path to the trained pipeline object")
@click.option('--results-to', type=str, help="Path to directory where results will be saved")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(test_data, pipeline_from, results_to, seed):
    """
    Evaluate a pre-trained Logistic Regression model on test data.

    This function loads a pre-trained pipeline, uses it to make predictions on the test dataset, 
    and saves the evaluation results, including a confusion matrix and a classification report, 
    as CSV files.

    Args:
        test_data (str): Path to the CSV file containing the test dataset. 
            The dataset must include numeric, categorical, and ordinal features, 
            along with the target column `age_group`. Example: "data/test.csv".
        pipeline_from (str): File path to load the trained pipeline (preprocessor + logistic regression model) 
            in pickle format. Example: "models/model_pipeline.pkl".
        results_to (str): Directory path where the evaluation results will be saved 
            as CSV files. Example: "results/evaluation".
        seed (int, optional): Random seed for reproducibility. Defaults to 123.

    Returns:
        None: This function performs the following side effects:
            - Loads a trained pipeline from `pipeline_from`.
            - Predicts and evaluates on the test data.
            - Saves evaluation results (confusion matrix and classification report) as CSV files 
              to the specified `results_to` directory.
    """
    np.random.seed(seed)
    set_config(transform_output="pandas")
    
    # Load test data
    data_test = pd.read_csv(test_data)
    target = 'age_group'
    X_test, y_test = data_test.drop(columns=[target]), data_test[target]

    # Load the pre-trained pipeline
    with open(pipeline_from, 'rb') as f:
        trained_pipeline = pickle.load(f)
    
    # Predict and evaluate
    y_pred_test = trained_pipeline.predict(X_test)
    cancer_preds = pd.DataFrame({"actual": y_test, "predicted": y_pred_test})
    
    # Save Confusion Matrix as CSV
    confusion_matrix = pd.crosstab(cancer_preds["actual"], cancer_preds["predicted"])
    write_csv(confusion_matrix, results_to, "confusion_matrix.csv", index=True)

    # Save Classification Report as CSV
    report = classification_report(y_test, y_pred_test, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    write_csv(report_df, results_to, "age_model_report.csv", index=True)


if __name__ == '__main__':
    main()

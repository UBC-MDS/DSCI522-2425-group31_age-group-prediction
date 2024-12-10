import click
import os
import numpy as np
import pandas as pd
import altair as alt
import pickle
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split

@click.command()
@click.option('--train-data', type=str, help="Path to training data")
@click.option('--preprocessor-to', type=str, help="Path to save the preprocessor object")
@click.option('--pipeline-to', type=str, help="Path to save the trained pipeline object")
@click.option('--plot-to', type=str, help="Path to save the training plot")
@click.option('--seed', type=int, default=123, help="Random seed")

def main(train_data, preprocessor_to, pipeline_to, plot_to, seed):
    """
    Train and Evaluate a Logistic Regression Model.

    This function preprocesses data, trains a logistic regression model with hyperparameter 
    tuning, and generates visualizations of training and cross-validation scores.

    Args:
        train_data (str): Path to the CSV file containing the training dataset. 
            The dataset must include numeric, categorical, and ordinal features, 
            along with the target column `age_group`. Example: "data/train.csv".
        preprocessor_to (str): File path to save the preprocessing pipeline object 
            (`preprocessor`) in pickle format. Example: "models/preprocessor.pkl".
        pipeline_to (str): File path to save the trained pipeline (preprocessor + 
            logistic regression model) in pickle format. Example: "models/model_pipeline.pkl".
        plot_to (str): File path to save the Altair plot comparing training and cross-validation 
            scores as an HTML file. Example: "results/train_vs_cv_plot.html".
        seed (int, optional): Random seed for reproducibility. Defaults to 123.

    Returns:
        None: This function performs the following side effects:
            - Saves the preprocessing pipeline to `preprocessor_to`.
            - Saves the trained pipeline (preprocessor + model) to `pipeline_to`.
            - Exports an interactive Altair plot to `plot_to`.

    Example:
        main(
            train_data="data/train.csv",
            preprocessor_to="models/preprocessor.pkl",
            pipeline_to="models/model_pipeline.pkl",
            plot_to="results/train_vs_cv_plot.html",
            seed=42
        )
    """
    np.random.seed(seed)
    
    # Load data
    data_train = pd.read_csv(train_data)
    target = 'age_group'
    X_train, y_train = data_train.drop(columns=[target]), data_train[target]

    # Feature categorization
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
    
    # Save preprocessor
    with open(os.path.join(preprocessor_to, "age_prediction_preprocessor.pickle"), 'wb') as f:
        pickle.dump(preprocessor, f)
    
    # Logistic Regression Pipeline
    lgr_classifier = LogisticRegression(max_iter=2000, random_state=seed, class_weight='balanced')
    pipe = make_pipeline(preprocessor, lgr_classifier)
    
    # Hyperparameter tuning
    param_grid = {'logisticregression__C': 10.0 ** np.arange(-6, 6)}
    gs_optimize = GridSearchCV(pipe, param_grid, cv=10, return_train_score=True)
    gs_optimize.fit(X_train, y_train)
    
    # Save the pipeline
    with open(os.path.join(pipeline_to, "age_prediction_model.pickle"), 'wb') as f:
        #save the best estimator
        pickle.dump(gs_optimize.best_estimator_, f)   
    
    # Plot training vs. CV scores
    train_scores = gs_optimize.cv_results_["mean_train_score"]
    cv_scores = gs_optimize.cv_results_["mean_test_score"]
    train_cv_df = pd.concat([
        pd.DataFrame({'C': np.log10(param_grid["logisticregression__C"]),
                      'score': train_scores,
                      'score_type': ['Training'] * len(train_scores)}),
        pd.DataFrame({'C': np.log10(param_grid["logisticregression__C"]),
                      'score': cv_scores,
                      'score_type': ['Cross Validation'] * len(cv_scores)}),
    ])
    plot = alt.Chart(train_cv_df).mark_line().encode(
        x=alt.X('C', title='Hyperparameter C (log10)'),
        y=alt.Y('score', title='Model Score').scale(zero=False),
        color=alt.Color('score_type')
    )
    plot.save(os.path.join(plot_to, "fig_hyperparameter_c.png"),
              scale_factor=2.0)

if __name__ == '__main__':
    main()

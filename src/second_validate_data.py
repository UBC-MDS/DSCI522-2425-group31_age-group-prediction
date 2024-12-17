from deepchecks.tabular.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation
from deepchecks.tabular import Dataset
from deepchecks.core.errors import DeepchecksValueError

def second_validate_data(data_train):
    """
    Validates the input data for correlation issues using predefined checks.

    Parameters
    ----------
    data_train : pandas.DataFrame
        The DataFrame containing the training data to be validated.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If any validation condition is not met, indicating a failure in the checks.    
    """
    # Create Deepchecks Dataset object
    try:
        data_train_ds = Dataset(data_train, label="age_group", cat_features=[])
    except DeepchecksValueError as e:
        raise ValueError(f"Dataset creation failed: {e}")

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

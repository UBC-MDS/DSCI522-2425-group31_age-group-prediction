import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.second_validate_data import second_validate_data 
import pandas as pd
import pandera as pa
import pytest
import numpy as np

# Test data setup
valid_data = pd.DataFrame({
    "age_group": ["Adult", "Senior", "Adult", "Senior", "Adult", "Senior"],
    "gender": ["Female", "Male", "Female", "Male", "Female", "Male"],
    "diabetic": ["No", "Yes", "No", "Yes", "No", "Yes"],
    "weekly_physical_activity": ["Yes", "No", "Yes", "No", "Yes", "No"],
    "bmi": [18.5, 22.0, 28.0, 24.5, 20.0, 30.0],  # More diverse values
    "blood_glucose_fasting": [90.0, 110.0, 95.0, 120.0, 100.0, 105.0],  # More variety
    "oral": [85.0, 170.0, 150.0, 140.0, 160.0, 180.0],  # Spread values further
    "insulin_level": [0.4, 1.3, 2.2, 1.1, 0.5, 1.9]  # Break linear relationships
})

# Case 1: Validate valid data
def test_validate_valid_data():
    """
    Test that valid data passes the validation without raising any errors.
    """
    print("\nCorrelation matrix for valid_data:")
    print(valid_data.select_dtypes(include=["number"]).corr())
    second_validate_data(valid_data)  # No exceptions expected

# 2. Test dataset creation failed
def test_dataset_creation_failed():
    """
    Test that missing the 'age_group' column raises a dataset creation error.
    """
    invalid_data = valid_data.drop("age_group", axis=1)  # Remove required label column
    with pytest.raises(ValueError, match="Dataset creation failed: .*"):
        second_validate_data(invalid_data)

# 3. Test missing required columns
def test_missing_column():
    """
    Test that missing required columns raises an error.
    """
    invalid_data = valid_data.drop("age_group", axis=1)  # Remove the required 'age_group' column
    with pytest.raises(ValueError, match="Dataset creation failed: .*"):
        second_validate_data(invalid_data)

# 4. Test feature-feature correlation failure
def test_feature_feature_correlation():
    """
    Test that features with high inter-correlation raise an error.
    """
    invalid_data = valid_data.copy()
    # Introduce a feature perfectly correlated with another feature
    invalid_data["duplicate_feature"] = invalid_data["bmi"]  # Fully correlated with 'bmi'

    with pytest.raises(ValueError, match="Feature-Feature correlation exceeds the maximum acceptable threshold."):
        second_validate_data(invalid_data)

if __name__ == "__main__":
    pytest.main()
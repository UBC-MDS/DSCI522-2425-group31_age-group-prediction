import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import validate_data 
import pandas as pd
import pandera as pa
import pytest
import numpy as np

# Test data setup
valid_data = pd.DataFrame({
    "age_group": ["Adult", "Senior", "Adult"],
    "gender": ["Female", "Male", "Female"],
    "weekly_physical_activity": ["Yes", "No", "Yes"],
    "bmi": [18.5, 24.9, 30.0],
    "blood_glucose_fasting": [90.0, 120.5, 100.0],
    "diabetic": ["No", "Yes", "No"],
    "oral": [100.0, 200.0, 150.0],
    "insulin_level": [0.14, 50.0, 25.0]
})

# Case 1: Validate valid data
def test_validate_valid_data():
    validated_data = validate_data(valid_data)
    assert not validated_data.empty
    assert validated_data.equals(valid_data)

# Case 2: Duplicate rows
case_duplicate_rows = pd.concat([valid_data, valid_data.iloc[[0]]], ignore_index=True)
def test_duplicate_rows():
    with pytest.raises(pa.errors.SchemaErrors, match="Duplicate rows found"):
        validate_data(case_duplicate_rows)

# Case 3: Missing values exceed threshold
case_high_missingness = valid_data.copy()
case_high_missingness["bmi"] = np.nan  # Introduce missing values exceeding threshold
def test_high_missingness():
    with pytest.raises(pa.errors.SchemaErrors, match="missing values above"):
        validate_data(case_high_missingness)

# Case 4: Empty rows
def test_empty_rows():
    case_empty_rows = pd.concat(
        [valid_data, pd.DataFrame([[None] * len(valid_data.columns)], columns=valid_data.columns).astype(valid_data.dtypes)],
        ignore_index=True
    )
    with pytest.raises(pa.errors.SchemaErrors, match="Empty rows found"):
        validate_data(case_empty_rows)

# Case 5: Values out of range
def test_out_of_range_values():
    case_out_of_range = valid_data.copy()
    case_out_of_range.loc[0, "bmi"] = 80.0  # Out of range
    with pytest.raises(pa.errors.SchemaErrors, match="bmi"):
        validate_data(case_out_of_range)

# Case 6: Invalid category values
def test_invalid_category():
    case_invalid_category = valid_data.copy()
    case_invalid_category.loc[0, "age_group"] = "Child"  # Invalid category
    with pytest.raises(pa.errors.SchemaErrors, match="age_group"):
        validate_data(case_invalid_category)

# Case 7: Missing required columns
def test_missing_column():
    case_missing_column = valid_data.drop("age_group", axis=1)
    with pytest.raises(pa.errors.SchemaErrors, match="age_group"):
        validate_data(case_missing_column)

# Case 8: Wrong data type
def test_wrong_data_type():
    case_wrong_type = valid_data.copy()
    case_wrong_type["bmi"] = "invalid_type"
    with pytest.raises(pa.errors.SchemaErrors, match="bmi"):
        validate_data(case_wrong_type)

# Case 9: All values missing in a column
def test_all_missing_column():
    case_all_missing = valid_data.copy()
    case_all_missing["gender"] = None
    with pytest.raises(pa.errors.SchemaErrors, match="missing values above"):
        validate_data(case_all_missing)

if __name__ == "__main__":
    pytest.main()
import pandas as pd
import pandera as pa

def validate_data(data):
    """
    Validates the input data according to a predefined schema.

    Parameters
    ----------
    data : pandas.DataFrame
        The DataFrame containing raw data that needs to be validated.

    Returns
    -------
    pandas.DataFrame
        The validated DataFrame that conforms to the specified schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not conform to the specified schema.
    """
    MISSINGNESS_THRESHOLD = 0.2

    schema = pa.DataFrameSchema({
        "age_group": pa.Column(str, pa.Check.isin(["Adult", "Senior"])),
        "gender": pa.Column(str, pa.Check.isin(["Female", "Male"]), nullable=True),
        "weekly_physical_activity": pa.Column(str, pa.Check.isin(["No", "Yes"]), nullable=True),
        "bmi": pa.Column(float, pa.Check.between(14.5, 70.1), nullable=True),
        "blood_glucose_fasting": pa.Column(float, pa.Check.between(63.0, 405.0), nullable=True),
        "diabetic": pa.Column(str, pa.Check.isin(["No", "Yes", "Borderline"]), nullable=True),
        "oral": pa.Column(float, pa.Check.between(40.0, 604.0), nullable=True),
        "insulin_level": pa.Column(float, pa.Check.between(0.14, 102.29), nullable=True)
    }, strict=True,
    checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
        pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        pa.Check(lambda df: df.apply(lambda col: col.isnull().mean() <= MISSINGNESS_THRESHOLD).all(),
            error=f"One or more columns have missing values above {MISSINGNESS_THRESHOLD*100:.1f}% threshold.")
    ]
    )

    # Validate data and return validated dataframe
    validated_data = schema.validate(data, lazy=True)
    return validated_data
import os
import sys
import pytest
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.write_csv import write_csv  

@pytest.fixture
def temp_directory(tmp_path):
    """Fixture to provide a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def sample_dataframe():
    """Fixture to provide a sample Pandas DataFrame."""
    data = {
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    }
    return pd.DataFrame(data)

def test_write_csv_valid_input(temp_directory, sample_dataframe):
    """Test that write_csv saves the DataFrame correctly."""
    directory = temp_directory
    filename = "test.csv"

    write_csv(sample_dataframe, str(directory), filename)

    filepath = os.path.join(directory, filename)
    assert os.path.exists(filepath), "CSV file was not created."

    saved_df = pd.read_csv(filepath)
    pd.testing.assert_frame_equal(sample_dataframe.reset_index(drop=True), saved_df, check_dtype=False)

def test_write_csv_invalid_filename_extension(temp_directory, sample_dataframe):
    """Test that write_csv raises ValueError for invalid filename extension."""
    with pytest.raises(ValueError, match="Filename must end with '.csv'"):
        write_csv(sample_dataframe, str(temp_directory), "test.txt")

def test_write_csv_nonexistent_directory(sample_dataframe):
    """Test that write_csv raises FileNotFoundError for a nonexistent directory."""
    with pytest.raises(FileNotFoundError, match="Directory .+ does not exist"):
        write_csv(sample_dataframe, "nonexistent_directory", "test.csv")

def test_write_csv_empty_dataframe(temp_directory):
    """Test that write_csv raises ValueError for an empty DataFrame."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="DataFrame must contain observations"):
        write_csv(empty_df, str(temp_directory), "test.csv")

def test_write_csv_invalid_dataframe(temp_directory):
    """Test that write_csv raises TypeError for invalid DataFrame input."""
    with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
        write_csv("not_a_dataframe", str(temp_directory), "test.csv")

def test_write_csv_with_index(temp_directory, sample_dataframe):
    """Test that write_csv correctly includes the index when specified."""
    directory = temp_directory
    filename = "test_with_index.csv"

    write_csv(sample_dataframe, str(directory), filename, index=True)

    filepath = os.path.join(directory, filename)
    assert os.path.exists(filepath), "CSV file with index was not created."

    saved_df = pd.read_csv(filepath, index_col=0)
    pd.testing.assert_frame_equal(sample_dataframe, saved_df)
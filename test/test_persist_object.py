import os
import sys
import pytest
import pickle
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.persist_object import persist_object  

# This is a simple utility class that implements __eq__ 
# to easily test object equality
class SimpleClass:
    def __init__(self, int_value: int, name_property: str, float_value: float):
        self.int_value = int_value
        self.name_property = name_property
        self.float_value = float_value

    def __eq__(self, other):
        if not isinstance(other, SimpleClass):
            return False
        # Compare all properties for equality
        return (
            self.int_value == other.int_value 
            and self.name_property == other.name_property 
            and self.float_value == other.float_value
        )


@pytest.fixture
def temp_directory(tmp_path):
    """Fixture to provide a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def sample_object():
    """Fixture to create a column transformer"""
    preproc = make_column_transformer(
        (StandardScaler(), []),
        ("drop", []),
    )
    return preproc

@pytest.fixture
def sample_simple_type():
    """Fixture to create an object with simple types"""
    return SimpleClass(522, "Data Science Workflows", 99.99)

def test_persist_simple_valid_input(temp_directory, sample_simple_type):
    """Test that persist_object saves an object with simple data types correctly."""
    directory = temp_directory
    filename = "simple.obj"

    persist_object(sample_simple_type, str(directory), filename)

    filepath = os.path.join(directory, filename)
    assert os.path.exists(filepath), "Simple object was persisted to disk."

    with open(filepath, 'rb') as f:
        read_obj = pickle.load(f)
    assert read_obj == sample_simple_type, "Simple object read differs from one saved"

def test_persist_valid_input(temp_directory, sample_object):
    """Test that persist_object saves the a ColumnTransformer object correctly."""
    directory = temp_directory
    filename = "preproc.obj"

    persist_object(sample_object, str(directory), filename)

    filepath = os.path.join(directory, filename)
    assert os.path.exists(filepath), "Object was persisted to disk."

    with open(filepath, 'rb') as f:
        read_obj = pickle.load(f)
    #check obj
    check_properties = ['remainder', 'sparse_threshold', 'n_jobs',
                        'transformer_weights', 'verbose', 'verbose_feature_names_out']
    for prop in check_properties:
        #print(f'Comparing {read_obj.__dict__[prop]} == {sample_object.__dict__[prop]}')
        assert read_obj.__dict__[prop] == sample_object.__dict__[prop], f"Saved object differs on {prop}"
    #for ct in sample_object.named_transformers_():
    if(len(read_obj.transformers) == len(sample_object.transformers)):
        for pair in zip(read_obj.transformers, sample_object.transformers):
            #print(f"Checking 0: {pair[0][0]} == {pair[1][0]}")
            assert pair[0][0] == pair[1][0], \
                f"Transformer setting different {pair[0][0]} != {pair[1][0]}"
            # for the transformer, we only check if they are of the same class
            assert type(pair[0][1]) == type(pair[1][1]), \
                f"Transformer setting different {pair[0][1]} != {pair[1][1]}"
            assert pair[0][2] == pair[1][2], \
                f"Transformer setting different {pair[0][2]} != {pair[1][2]}"
    else:
        assert len(read_obj.transformers) == len(sample_object.transformers), \
            f"Saved object does not have the same transformers"
        
def test_persist_none(temp_directory):
    """Test that persist_object raises TypeError None is passed"""
    directory = temp_directory
    filename = "None.obj"
    with pytest.raises(TypeError, match = "Input must be an object instance"):
        persist_object(None, str(directory), filename)

def test_persist_invalid_filename(temp_directory, sample_object):
    """Test that persist_object raises ValueError if the filename contains spaces"""
    directory = temp_directory
    filename = "a file name with spaces.obj"
    with pytest.raises(ValueError, match = "The specified value is not valid for a filename"):
        persist_object(sample_object, str(directory), filename)

def test_persist_invalid_filename_withpath(temp_directory, sample_object):
    """Test that persist_object raises ValueError if the filename contains slash or is a path"""
    directory = temp_directory
    filename = "./model/preprocessor.obj"
    with pytest.raises(ValueError, match = "The specified value is not valid for a filename"):
        persist_object(sample_object, str(directory), filename)

        
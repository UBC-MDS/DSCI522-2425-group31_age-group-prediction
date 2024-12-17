import os
import re
import pickle

def persist_object(obj: object, directory: str, filename: str):
    """
    Utility method to save an in-memory object to disk

    Parameters
    ----------
    obj : object
        Object instance to to be saved.
    directory : str
        The directory where the object will be serialized to file.
    filename : str
        The name of the file including the extension, if needed.

    Raises
    ------
    ValueError
        If the filename is not valid, or the object is None.
    FileNotFoundError
        If the specified directory does not exist.
    """
    if not re.match(r'^[a-zA-Z0-9\\.\\-_]+$', filename):
        raise ValueError("The specified value is not valid for a filename")
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} does not exist.")
    if (obj is None):
        raise TypeError("Input must be an object instance")    

    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as fo:
        model = pickle.dump(obj, fo)
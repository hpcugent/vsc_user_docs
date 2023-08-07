import numpy as np


def simplify_modules(data: dict | list | np.ndarray):
    """
    Data is a list of modules.
    It removes the version of the modules and removes the duplicates.

    @param data:
    @return: List of programs.
    """

    if isinstance(data, dict):
        simplified_data = {}
        for cluster in data:
            simplified_data[cluster] = np.unique([entry.split("/")[0] for entry in data[cluster]])
    else:
        simplified_data = np.unique([entry.split("/")[0] for entry in data])

    return simplified_data

import numpy as np


def simplify_modules(data):
    """

    @param modules:
    @return:
    """
    return np.unique([entry.split("/")[0] for entry in data])

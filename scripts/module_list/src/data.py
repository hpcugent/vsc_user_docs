import numpy as np
from .module import avail, swap


def filter_fn_gent_cluster(data: np.ndarray):
    return data[~np.char.endswith(data, ":") &
                ~np.char.startswith(data, "env/")
                ]


def filter_fn_gent_modules(data: np.ndarray):
    """

    @param data:
    @return:
    """
    return data[~np.char.endswith(data, ":") &
                ~np.char.startswith(data, "env/") &
                ~np.char.startswith(data, "cluster/")
                ]


def ugent_clusters():
    return avail(name="cluster/", filter_fn=filter_fn_gent_cluster)


def simplify_modules(data):
    """

    @param modules:
    @return:
    """
    return [entry.split("/")[0] for entry in data]


def data_ugent():
    data = {}
    for cluster in ugent_clusters():
        swap(cluster)
        data[cluster] = simplify_modules(avail(filter_fn=filter_fn_gent_modules))
        break
    return data

import os
import subprocess
from typing import Union, Tuple
from mdutils.mdutils import MdUtils
import numpy as np


# --------------------------------------------------------------------------------------------------------
# Module bash API
# --------------------------------------------------------------------------------------------------------

def module(*args, filter_fn=lambda x: x) -> np.ndarray:
    """
    API to call the module command.

    @param args: Extra arguments for the module command.
    @param filter_fn: Filter function on the ouput.
    @return:
    """
    lmod = os.getenv('LMOD_CMD')
    proc = subprocess.run(
        [lmod, "python", "-t"] + list(args),
        encoding="utf-8",
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    exec(proc.stdout)
    return filter_fn(np.array(proc.stderr.split()))


def module_avail(name: str = "", filter_fn=lambda x: x) -> np.ndarray:
    """
    API to call the module avail command of Lmod.

    @param name: Possible module name.
    @param filter_fn: Filter on the output.
    @return: List of all available modules of name, or all if name is not given.
    """
    return module("avail", name, filter_fn=filter_fn)


def module_swap(name: str) -> None:
    """
    Function to run "module swap" commands.

    @param name: Name of module you want to swap to.
    """
    module("swap", name)


# --------------------------------------------------------------------------------------------------------
# Fetch data
# --------------------------------------------------------------------------------------------------------

def filter_fn_gent_cluster(data: np.ndarray) -> np.ndarray:
    """
    Filter function for output of "module avail" commands on HPC-UGent infrastructure.

    Filters out lines ending with ':' (which are paths to module files),
    and lines starting with 'env/' or 'cluster/default', which are not actually software modules
    @param data: Output
    @return: Filtered output
    """
    return data[~np.char.endswith(data, ":") &
                ~np.char.startswith(data, "env/") &
                ~np.char.startswith(data, "cluster/default")
                ]


def filter_fn_gent_modules(data: np.ndarray) -> np.ndarray:
    """
    Filter function for the output of all modules.
    @param data: Output
    @return: Filtered output
    """
    return data[~np.char.endswith(data, ":") &
                ~np.char.startswith(data, "env/") &
                ~np.char.startswith(data, "cluster/")
                ]


def clusters_ugent() -> np.ndarray:
    """
    Returns all the cluster names of the HPC at UGent.
    @return: cluster names
    """

    return module_avail(name="cluster/", filter_fn=filter_fn_gent_cluster)


def modules_ugent() -> dict:
    """
    Returns all the module names that are installed on the HPC on UGent.
    They are grouped by cluster.
    @return: Dictionary with all the modules per cluster
    """

    data = {}
    for cluster in clusters_ugent():
        module_swap(cluster)
        data[cluster] = module_avail(filter_fn=filter_fn_gent_modules)
    return data


# --------------------------------------------------------------------------------------------------------
# Util functions
# --------------------------------------------------------------------------------------------------------

def simplify_modules(data: Union[dict, list, np.ndarray]) -> Union[dict, list, np.ndarray]:
    """
    Simplify list of modules by removing versions and duplicates.

    @param data: List of modules
    @return: List of programs.
    """

    if isinstance(data, dict):
        simplified_data = {}
        for cluster in data:
            simplified_data[cluster] = np.unique([entry.split("/")[0] for entry in data[cluster]])
    else:
        simplified_data = np.unique([entry.split("/")[0] for entry in data])

    return simplified_data


# --------------------------------------------------------------------------------------------------------
# Generate markdown
# --------------------------------------------------------------------------------------------------------

def generate_table_data(data: dict) -> Tuple[np.ndarray, int, int]:
    """
    Generate data that can be used to construct a MarkDown table.

    @param data: Available data
    @return: Returns tuple (Table data, #col, #row)
    """
    data = simplify_modules(data)
    all_modules = simplify_modules(np.concatenate(list(data.values())))

    final = np.array([" "])
    final = np.append(final, list(data.keys()))

    for package in all_modules:
        final = np.append(final, package)

        for cluster in data:
            final = np.append(final, "X" if package in data[cluster] else " ")

    return final, len(data.keys()) + 1, len(all_modules) + 1


def generate_module_table(data: dict, md_file: MdUtils) -> None:
    """
    Generate the general table of the overview.

    @param data: Dict with all the data. Keys are the cluster names.
    @param md_file: MdUtils object.
    """
    structured, col, row = generate_table_data(data)
    md_file.new_table(columns=col, rows=row, text=list(structured), text_align='center')


def generate_general_overview() -> None:
    """
    Generate the general overview in a markdown file.
    It generates a list of all the available software and indicates on which cluster it is available.
    """
    md_file = MdUtils(file_name='module_overview.md', title='Overview of available modules per cluster')
    data = modules_ugent()
    generate_module_table(data, md_file)
    md_file.create_md_file()


if __name__ == '__main__':
    # Generate the overview
    generate_general_overview()

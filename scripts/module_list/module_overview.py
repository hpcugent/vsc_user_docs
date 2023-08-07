import os
import subprocess
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
    # return module(f"avail {name if name else ''}", filter_fn=filter_fn)
    return module("avail", name, filter_fn=filter_fn)


def module_swap(name: str) -> None:
    """
    API to call swap command of module.

    @param name: Module you want to swap to.
    """
    module("swap", name)


# --------------------------------------------------------------------------------------------------------
# Fetch data
# --------------------------------------------------------------------------------------------------------

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
    return module_avail(name="cluster/", filter_fn=filter_fn_gent_cluster)


def data_ugent():
    data = {}
    for cluster in ugent_clusters():
        module_swap(cluster)
        data[cluster] = module_avail(filter_fn=filter_fn_gent_modules)
    return data


# --------------------------------------------------------------------------------------------------------
# Util functions
# --------------------------------------------------------------------------------------------------------

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


# --------------------------------------------------------------------------------------------------------
# Generate markdown
# --------------------------------------------------------------------------------------------------------

def generate_table_data(data: dict):
    """

    @param data:
    @return:
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
    md_file = MdUtils(file_name='Example_Markdown', title='Overview Moduls')
    data = data_ugent()
    generate_module_table(data, md_file)
    md_file.create_md_file()


if __name__ == '__main__':
    # Generate the overview
    generate_general_overview()

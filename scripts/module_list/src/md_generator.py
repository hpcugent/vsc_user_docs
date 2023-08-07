from mdutils.mdutils import MdUtils
from .data import data_ugent
import numpy as np
import pickle
from .utils import simplify_modules


def generate_table_data(data: dict):
    """
    
    @param data:
    @return:
    """
    all_modules = simplify_modules(np.concatenate(list(data.values())))

    final = np.array([" "])
    final = np.append(final, list(data.keys()))

    for module in all_modules:
        final = np.append(final, module)

        for cluster in data:
            final = np.append(final, "X" if module in data[cluster] else " ")

    return final,  len(data.keys()) + 1, len(all_modules)+1


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

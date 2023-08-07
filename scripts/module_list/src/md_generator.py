from mdutils.mdutils import MdUtils
from .data import data_ugent
import numpy as np


def generate_module_table(data: dict, md_file: MdUtils) -> None:
    """
    Generate the general table of the overview.

    @param data: Dict with all the data. Keys are the cluster names.
    @param md_file: MdUtils object.
    """
    all_modules = np.unique(np.concatenate(list(data.values())))
    md_file.new_table(columns=1, rows=len(all_modules), text=list(all_modules), text_align='center')


def generate_general_overview() -> None:
    """
    Generate the general overview in a markdown file.
    It generates a list of all the available software and indicates on which cluster it is available.
    """
    md_file = MdUtils(file_name='Example_Markdown', title='Overview Moduls')
    data = data_ugent()
    generate_module_table(data, md_file)
    md_file.create_md_file()

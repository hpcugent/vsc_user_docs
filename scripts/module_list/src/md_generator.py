from mdutils.mdutils import MdUtils
from .data import data_ugent
import numpy as np


def generate_module_table(data: dict, md_file: MdUtils) -> None:
    """

    @param data:
    @param md_file:
    """
    all_modules = np.unique(np.concatenate(list(data.values())))
    md_file.new_table(columns=1, rows=len(all_modules), text=all_modules, text_align='center')


def generate_general_overview() -> None:
    """

    @param data:
    """
    md_file = MdUtils(file_name='Example_Markdown', title='Overview Moduls')
    data = data_ugent()
    generate_module_table(data, md_file)
    md_file.create_md_file()

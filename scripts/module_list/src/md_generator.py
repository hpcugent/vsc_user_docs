from mdutils.mdutils import MdUtils


def generate_module_table(data: dict, md_file: MdUtils) -> None:
    """

    @param data:
    @param md_file:
    """
    md_file.new_table(columns=3, rows=2, text=["1", "2", "3", "1", "2", "3"], text_align='center')


def generate_general_overview(data: dict) -> None:
    """

    @param data:
    """
    md_file = MdUtils(file_name='Example_Markdown', title='Overview Moduls')
    generate_module_table(data, md_file)
    md_file.create_md_file()

import pickle
from mdutils.mdutils import MdUtils
from scripts.module_list.module_overview import simplify_modules, generate_table_data, generate_module_table


class TestMarkdown:

    # ---------------------------
    # Class level setup/teardown
    # ---------------------------

    @classmethod
    def setup_class(cls):
        with open('data/data_simple.pickle', 'rb') as handle:
            cls.simple_data = simplify_modules(pickle.load(handle))

        with open('data/data_all.pickle', 'rb') as handle:
            cls.all_data = simplify_modules(pickle.load(handle))

    # ---------------------------
    # Markdown tests
    # ---------------------------

    def test_table_generate_simple(self):
        table_data = generate_table_data(self.simple_data)

    def test_table_generate_all(self):
        table_data = generate_table_data(self.all_data)

    def test_simple(self):
        md_file = MdUtils(file_name='test_simple', title='Overview Modules')
        generate_module_table(self.simple_data, md_file)
        md_file.create_md_file()
        assert True

    def test_all(self):
        md_file = MdUtils(file_name='test_all', title='Overview Modules')
        generate_module_table(self.all_data, md_file)
        md_file.create_md_file()
        assert True

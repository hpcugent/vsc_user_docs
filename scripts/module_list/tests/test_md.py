from mdutils.mdutils import MdUtils
from module_overview import simplify_modules, modules_ugent, generate_table_data, generate_module_table
import os
import numpy as np


class TestMarkdown:
    # ---------------------------
    # Class level setup/teardown
    # ---------------------------

    path = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setup_class(cls):
        os.environ["TESTS_PATH"] = cls.path
        os.environ["LMOD_CMD"] = cls.path + "/data/lmod_mock.sh"
        os.environ["MOCK_FILE_SWAP"] = cls.path + "/data/data_swap_CLUSTER.txt"
        os.environ["MOCK_FILE_AVAIL_CLUSTER"] = cls.path + "/data/data_avail_cluster_simple.txt"

    @classmethod
    def teardown_class(cls):
        if os.path.exists("test_simple.md"):
            os.remove("test_simple.md")

    # ---------------------------
    # Markdown tests
    # ---------------------------

    def test_table_generate_simple(self):
        simple_data = simplify_modules(modules_ugent())
        table_data, col, row = generate_table_data(simple_data)
        all_modules = simplify_modules(np.concatenate(list(simple_data.values())))
        assert col == len(simple_data.keys())+1
        assert row == len(all_modules)+1
        assert len(table_data) == (len(simple_data.keys()) * len(all_modules)) + \
               len(simple_data.keys()) + \
               len(all_modules) + \
               1

    def test_simple(self):
        md_file = MdUtils(file_name='test_simple', title='Overview Modules')
        simple_data = simplify_modules(modules_ugent())
        generate_module_table(simple_data, md_file)
        md_file.create_md_file()
        assert os.path.exists("test_simple.md")

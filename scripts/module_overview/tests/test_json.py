import filecmp
from module_overview import generate_json_overview_data, generate_json_overview, modules_ugent, generate_json_detailed
import os


class TestJSON:
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
        if os.path.exists("json_data.json"):
            os.remove("json_data.json")
            os.remove("json_data_detail.json")

    # ---------------------------
    # Markdown tests
    # ---------------------------

    def test_json_generate_simple(self):
        modules = modules_ugent()
        json_data = generate_json_overview_data(modules)
        assert len(json_data["clusters"]) == 2
        assert len(json_data["modules"]) == 4
        assert list(json_data["clusters"]) == ["cluster/dialga", "cluster/pikachu"]
        assert json_data == {
            'clusters': ["cluster/dialga", "cluster/pikachu"],
            'modules': {
                "Markov": [1, 0],
                "cfd": [1, 1],
                "llm": [0, 1],
                "science": [1, 1]
            }
        }

    def test_json_simple(self):
        modules = modules_ugent()
        generate_json_overview(modules)
        assert os.path.exists("json_data.json")
        assert filecmp.cmp(self.path + "/data/test_json_simple_sol.json", "json_data.json")

    def test_json_detail_simple(self):
        modules = modules_ugent()
        generate_json_detailed(modules)
        assert os.path.exists("json_data_detail.json")
        assert filecmp.cmp(self.path + "/data/test_json_simple_sol_detail.json", "json_data_detail.json")

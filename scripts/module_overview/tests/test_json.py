from module_overview import generate_overview_json_data, generate_json_overview, modules_ugent
import os
import json


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

    # ---------------------------
    # Markdown tests
    # ---------------------------

    def test_json_generate_simple(self):
        modules = modules_ugent()
        json_data = generate_overview_json_data(modules)
        assert len(json_data.keys()) == 3
        assert list(json_data["clusters"]) == ["cluster/dialga", "cluster/pikachu"]
        assert json_data["modules"] == {
                "Markov": [True, False],
                "cfd": [True, True],
                "llm": [False, True],
                "science": [True, True]
            }

    def test_json_simple(self):
        generate_json_overview()
        with open("json_data.json") as json_data:
            data_generated = json.load(json_data)

        with open(self.path + "/data/test_json_simple_sol.json") as json_data:
            data_solution = json.load(json_data)

        assert len(data_generated) == 3
        assert data_generated["modules"] == data_solution["modules"]
        assert data_generated["clusters"] == data_solution["clusters"]

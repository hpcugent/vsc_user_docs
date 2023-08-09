import os
from module_overview import modules_ugent, clusters_ugent, simplify_modules


class TestData:
    # ---------------------------
    # Class level setup/teardown
    # ---------------------------
    path = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setup_class(cls):
        os.environ["LMOD_CMD"] = cls.path + "/data/lmod_mock.sh"

    # ---------------------------
    # Module tests
    # ---------------------------

    def test_data_ugent(self):
        os.environ["MOCK_FILE_AVAIL"] = self.path + "/data/data_avail_simple_pikachu.txt"
        os.environ["MOCK_FILE_AVAIL_CLUSTER"] = self.path + "/data/data_avail_cluster_simple.txt"
        sol = modules_ugent()
        assert len(sol) == 2
        assert len(sol["cluster/dialga"]) == 15
        assert list(simplify_modules(sol["cluster/dialga"])) == ["cfd", "llm", "science"]

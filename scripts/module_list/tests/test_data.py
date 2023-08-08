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
        os.environ["MOCK_FILE_AVAIL"] = self.path + "/data/data_avail_simple.txt"
        os.environ["MOCK_FILE_AVAIL_CLUSTER"] = self.path + "/data/data_avail_cluster_simple.txt"
        sol = modules_ugent()
        assert len(sol) == 2
        assert len(sol["cluster/victini"]) == 15
        assert list(simplify_modules(sol["cluster/victini"])) == ["ABAQUS", "ABINIT", "zstd"]

    def test_clusters_ugent(self):
        os.environ["MOCK_FILE_AVAIL_CLUSTER"] = self.path + "/data/doduo_avail_cluster.txt"
        sol = clusters_ugent()
        assert len(sol) == 8
        assert list(sol) == ['cluster/accelgor', 'cluster/doduo', 'cluster/donphan',
                             'cluster/gallade', 'cluster/joltik', 'cluster/skitty',
                             'cluster/swalot', 'cluster/victini']

    def test_large(self):
        os.environ["MOCK_FILE_AVAIL"] = self.path + "/data/doduo_avail.txt"
        os.environ["MOCK_FILE_AVAIL_CLUSTER"] = self.path + "/data/doduo_avail_cluster.txt"
        sol = modules_ugent()
        assert len(sol) == 8
        assert len(sol["cluster/victini"]) == 5504
        assert len(simplify_modules(sol["cluster/victini"])) == 1391

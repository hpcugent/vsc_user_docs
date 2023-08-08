import os


class TestModule:
    # ---------------------------
    # Class level setup/teardown
    # ---------------------------
    path = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setup_class(cls):
        os.environ["LMOD_CMD"] = cls.path + "data/lmod_mock.sh"

    # ---------------------------
    # Module tests
    # ---------------------------

    def test_avail(self):
        os.environ["MOCK_FILE"] = self.path + "data/mock_avail_0.txt"
        assert True

    def test_swap(self):
        os.environ["MOCK_FILE"] = self.path + "data/mock_swap_0.txt"
        assert True

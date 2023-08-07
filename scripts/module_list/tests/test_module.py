import os

from src.module import avail


# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    os.environ["LMOD_CMD"] = "data/lmod_mock.sh"
    os.environ["TEST"] = "data/test.txt"
    t = avail()

from mdutils import MdUtils
from src.md_generator import generate_general_overview, generate_module_table
from src.data import data_ugent
import pickle
from src.utils import simplify_modules


def main():
    # print(avail(name="Tensorflow", filter_fn=filter_fn_gent))
    print(data_ugent())


def md():
    generate_general_overview()


if __name__ == '__main__':
    md()

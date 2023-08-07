from src.module import avail
from src.md_generator import generate_general_overview
from src.data import filter_fn_gent_modules, data_ugent


def main():
    # print(avail(name="Tensorflow", filter_fn=filter_fn_gent))
    print(data_ugent())


def md():
    generate_general_overview()


if __name__ == '__main__':
    md()

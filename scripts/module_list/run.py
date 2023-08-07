from mdutils import MdUtils
from src.md_generator import generate_general_overview, generate_module_table
from src.data import data_ugent
import pickle


def main():
    # print(avail(name="Tensorflow", filter_fn=filter_fn_gent))
    print(data_ugent())


def md():
    generate_general_overview()


def test_md():
    with open('tests/data.pickle', 'rb') as handle:
        b = pickle.load(handle)

        md_file = MdUtils(file_name='Example_Markdown', title='Overview Moduls')
        generate_module_table(b, md_file)
        md_file.create_md_file()


if __name__ == '__main__':
    md()

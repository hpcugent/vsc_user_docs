import yaml
from jinja2 import Template
from if_mangler import mangle_ifs


# function that let's jinja do its thing to format the files expect for the os-related if-statements
def jinja_parser(filename):
    # Read the YAML file
    with open('..\\..\\mkdocs\\extra\\gent.yml', 'r') as yml_file:
        words_dict = yaml.safe_load(yml_file)

    # Mangle the OS-related if-statements
    mangle_ifs('.\\copies', filename)

    # Read the if-mangled Markdown file
    with open('.\\if_mangled_files\\' + filename, 'r') as md_file:
        md_content = md_file.read()

    # Use Jinja2 to replace the macros
    template = Template(md_content)
    rendered_content = template.render(words_dict)

    # Save the rendered content to a new file
    with open('.\\copies\\' + filename, 'w') as output_file:
        output_file.write(rendered_content)

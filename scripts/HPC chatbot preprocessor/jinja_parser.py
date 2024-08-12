import yaml
from jinja2 import Template, FileSystemLoader, Environment, ChoiceLoader
from if_mangler import mangle_ifs


# function that let's jinja do its thing to format the files expect for the os-related if-statements
def jinja_parser(filename, copy_location):
    # Read the YAML file
    with open('..\\..\\mkdocs\\extra\\gent.yml', 'r') as yml_file:
        words_dict = yaml.safe_load(yml_file)

    # ugly fix for index.md error
    additional_context = {
        'config': {
            'repo_url': 'https://github.com/hpcugent/vsc_user_docs'
        }
    }
    combined_context = {**words_dict, **additional_context}

    # Mangle the OS-related if-statements
    mangle_ifs(copy_location, filename)

    # Use Jinja2 to replace the macros
    template_loader = ChoiceLoader([FileSystemLoader(searchpath='.\\if_mangled_files'), FileSystemLoader(searchpath="..\\..\\mkdocs\\docs\\HPC")])
    templateEnv = Environment(loader=template_loader)
    template = templateEnv.get_template(filename)
    rendered_content = template.render(combined_context)

    # Save the rendered content to a new file
    with open(copy_location, 'w', encoding='utf-8', errors='ignore') as output_file:
        output_file.write(rendered_content)

# Python Virtual Environment Wrapper Script

`vsc-venv` is a script that encapsulates the creation and management of Python virtual environments. 
This avoids multiple issues with the default `venv` included in Python (`python -m venv`).


One issue is that a virtual environment created for one cluster might not work on another. 
Additionally, when activating a virtual environment, 
the same centrally installed modules used during its creation must also be loaded.
The `vsc-venv` command manages multiple virtual environments for different clusters in a transparent way, 
while guaranteeing the same module environment.

Detailed information can be found [here](../../mkdocs/docs/HPC/setting_up_python_virtual_environments.md#vsc-venv-python-virtual-environment-wrapper-script)
This tool is installed on the HPC-UGent clusters via a module. For more information, contact Kenneth Hoste.
from setuptools import setup

setup(
    name="ugent-plugin",
    version="0.0.1",
    entry_points={
        "mkdocs.plugins": [
            "ugent = custom_plugin:UgentPlugin",
        ]
    },
    py_modules=['constants', 'custom_plugin']
)

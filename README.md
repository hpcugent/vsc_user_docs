# UGent HPC - pdf2wiki
<!-- TOC -->
* [UGent HPC - pdf2wiki](#ugent-hpc---pdf2wiki)
  * [Introduction](#introduction)
  * [Requirements](#requirements)
  * [Configuration](#configuration)
  * [Build](#build)
  * [Run website locally](#run-website-locally)
  * [Add new OS](#add-new-os)
  * [Macros](#macros)
    * [Markdown macros](#markdown-macros)
    * [Python macros](#python-macros)
      * [Example](#example)
<!-- TOC -->

## Introduction

UGent HPC currently has user manuals in LaTex. Sources can be found here: https://github.com/hpcugent/vsc_user_docs
Pdf versions can be found here: https://www.ugent.be/hpc/en/support/documentation.htm

There are different variants for each VSC site and for each operating system.

## OS selection

The OS selection is stored in localStorage and kept for , and can be bypassed by going to any index pages (i.e. one without the OS),
and adding the hash `#force_select_OS` (case-sensitive).

## Build

You can use the `build.sh` wrapper script to take of the steps below,
all options including `--help` are passed to the `build.py` tool.

Using `INSTALLDEPS=1 build.sh ...` will first install the dependencies in a subdir `pypkgs`,
and then build the docs. (You typicaly only need to run that once, unless some of the dependencies are updated).

Using `WEBSERVER=1 build.sh ...`, you will first build the docs, and then start a local webserver
that provides the docs (and if supported by the OS, open a new browser tab with the page loaded).

### Dependencies

**Python version 3.6 and greater is required.**

Install requirements by running:

```shell
python -m pip install -r requirements.txt
```

Install custom plugin, which is present in this repository (at least for now):

```shell
python -m pip install -e custom_plugin
```

Install computational macros - Pyton macros:
```shell
python -m pip install -e computational_macros
```

### Build

Usage:

```shell
python build.py [options]
```

Options:

```text
-l, --skip-docs           Build only landing page. Skip building documentation pages.
-d, --skip-landing-page   Build only documentation pages. Skip building landing page.
--ignore-errors           Ignore errors in partial mkdocs builds and continue with build process.
-v                        Enable verbosity.
```

Without options, it will build all documentation defined in [build_config.yml](build_config.yml) and also landing page.

By default, the main build script fails and clean the build directory if any of the partial builds fails.
To override this behaviour and continue even if some documentation will not be built correctly, use the
option `--ignore-errors` described above.

```shell
python build.py
```

In directory `./build/` there will be built landing page called HPC for prettier url and site-OS hierarchy.
According to config, there will be folder structure with documentation content.

### Run website locally

Move to root directory of your static website:

```shell
cd build
```

Run simple HTTP server:

```shell
python -m http.server --cgi 8000
```

Visit `localhost:8000` and start looking around your documentation.


## Configuration

All `.yml` files in the `mkdocs` are supposedly generated and removed if unknown.

Every site has 3 generated configuration yamls in `mkdocs` dir one for each site and OS combination.
Template is in `config/templates` dir named [hpc.template](./config/templates/hpc.template).
Naming convention of generated files is like this: [hpc_Antwerpen_Linux.yml](mkdocs/hpc_Antwerpen_Linux.yml).

Configuration for OS picker utility is generated in `mkdocs` dir one for each site.
Template is in `config/templates` dir named [os_pick.template](./config/templates/os_pick.template).
Naming convention of generated files is like: [os_pick_Antwerpen.yml](mkdocs/os_pick_Antwerpen.yml).

Common constants are defined in [constants.yml](mkdocs/extra/constants.yml).

Configuration for landing page is defined in [landing_page.yml](config/others/landing_page.yml).

Configuration for documentation building script [build.py](build.py) is in [build.yml](config/build.yml).

When editing content, only specific site-OS yaml could be affected.
When adding or removing new site or OS except for site-OS yamls also other yamls are affected.

## Add new OS
You might want to add a new OS or divide Linux to some distros. You need to follow these steps:
0. Let's pretend you want add Arch Linux distro to Gent site.
1. Add the OS in [build.yml](config/build.yml)

In fact, this way you can add anything what you want. The build system will treat it as some OS.

## Macros
### Markdown macros
You can create macros in markdown as mkdocs documentation specifies.
On top of that there is a support for Python macros described in following section.

### Python macros
You can write Python script and use the output as content in the markdown.
This feature is implemented as variable injection. That brings some specific steps to follow.
The restrictions or rules are valid for current version and can vary in the future.
1. All scripts are placed in module [computational_macros](computational_macros) in package [scripts](computational_macros%2Fscripts).
2. Each script should contain exactly one method with the same name as the file. (Of course
   without the `.py` file extension.)
3. The method should return string object with desired output. This will be stored in the variable
   with again the same name. **You have to consider markdown and HTML formatting!**
4. Each script is automatically loaded, so you may want to add some prefix to prevent
   existing variables conflicts, respectively overriding.

You can return anything from Python macro, but it should make sense in context of mkdocs usage.
For example, you can generate some JavaScript code which will provide some interactive stuff in
target document page.

#### Implementation
You can find implementation in [custom_plugin.py](custom_plugin%2Fcustom_plugin.py).
It is single method called `gen_content_from_macros()`

#### Example
See example scripts in folder [scripts](computational_macros%2Fscripts).

See usage in file [account.md](docs%2Fintro-HPC%2Fexamples%2FAntwerpen%2FLinux%2Fintro-HPC%2Faccount.md).<br>
Built page can be access only by knowing its location and that is: `<server_name>/Antwerpen/Linux/intro-HPC/examples/Antwerpen/Linux/intro-HPC/account`

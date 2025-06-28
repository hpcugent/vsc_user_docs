# Chatbot parser

`chatbot_parser.py` is a script that transforms the markdown sourcefiles into a structured directory as input for a chatbot.

## Usage

The script can be ran in a shell environment with the following command:

```shell
python chatbot_parser.py
```

This command has the following possible options:

```shell
chatbot_parser.py [-h] -src SOURCE -dst DESTINATION [-st] [-pl MIN_PARAGRAPH_LENGTH] [-td MAX_TITLE_DEPTH] [-l] [-dd]
```

### Options

#### `h`/`help`

Display the help message

#### `src`/`source`

This is a required option that specifies the source directory of the input files for the script. This location is also used to look for jinja templates when using jinja to parse the source files (such as the `macros` directory within `vsc_user_docs/mkdocs/docs/HPC`).

#### `dst`/`destination`

This is a required option that specifies where the output of the script should be written. The script also generates extra intermediate subdirectories, so subdirectories with the following names shouldn't be present in the destination directory: `parsed_mds`, `copies` and `if_mangled_files`. If any of these pose a problem, the name of the intermediate subdirectory used for the script can be changed in the macros at the top of the script.

#### `st`/`split_on_titles`

Including this option will split the source files based on the titles and subtitles in the markdown text. Not including this option will split the text on paragraphs with a certain minimum length.

#### `pl`/`min_paragraph_length`

This option allows the user to configure the minimum length a paragraph must be. Some deviations from this minimum length are possible (for example at the end of a file). The default value for this minimum paragraph length is 512 tokens. This options only works if `split_on_titles` is not enabled.

#### `td`/`max_title_depth`

This option allows the user to configure the maximum "title depth" (the amount of `#` in front) to be used as borders between sections if `split_on_titles` is enabled. The default value is 4.

#### `l`/`links`

Some of the sourcefiles might contain links. Including this option will retain the links in the plaintext. If this option is not included, the links will be dropped from the plaintext.

#### `dd`/`deep_directories`

Including this option will make the script generate a "deep directory" where every title encountered will be made into a subdirectory of its parent title (So for example a title with three `#`s will be made a subdirectory of the most recent title with two `#`s). This option only works if `split_on_titles` is enabled.

## Generated file structure

The generated directory structure is written as a subdirectory of `parsed_mds`. In `parsed_mds`, two subdirectories can be found: 

- `generic` contains the parts of the markdown sources that were non-OS-specific
- `os_specific` contains the parts of the markdown sources that were OS-specific

Within `os_specific` a further distinction is made for each of the three possible operating systems included in the documentation.

Both the generic and each of the three os-specific directories then contain a directory for each source file. 

If the option `deep_directories` is not enabled, all paragraphs of the source file and their corresponding metadata will be saved in this directory. The (processed) plaintext of the paragraph is written to a `.txt` file and the metadata is written to a `.json` file.

If the option `deep_directories` is enabled, the directory of each source file will contain a subdirectory structure corresponding to the structure of the subtitles at different levels in the source file. Each subtitle in the source file corresponds to a directory nested in the directory of its parent title (So for example a title with three `#`s will be made a subdirectory of the most recent title with two `#`s). 

Finally, each of these subtitle-specific subdirectories contains a `.txt` file with the (processed) plaintext of that section and a `.json` file with the metadata of that section.

## Requirements

- The required Python packages are listed in `requirements.txt`

## Restrictions on source-files

Due to the nature of the script, some restrictions should be taken into account about the markdown files it can use as input.

### Nested if structures

The script uses the if-structures in the source-files to split the documentation into general documentation and os-specific documentation. As such it needs to keep track of which types of if-structures (os-related/non-os-related) it is reading from. When using certain nested if-structures, this will cause problems. The supported nested if-structures are determined by the macros `NON_OS_IF`, `NON_OS_IF_IN_OS_IF`, `OS_IF` and `OS_IF_IN_OS_IF`. So respectively a non-os-related if-structure, a non-os-related if nested in an os-related one, an os-related if-structure and an os-related if-structure nested in another os-related if-structure. All of these are allowed to be nested in an undetermined amount of non-os-related if-structures, but no non-os-related if structures should be nested in them. It is also not allowed to nest any of the allowed structures in more os-related if-structures. 

#### Examples of valid and invalid if-structures

##### Allowed

###### non-os-related in os-related

This is an example of one of the basic allowed if-structures (`NON_OS_IF_IN_OS_IF`)

```
if OS == windows:
  if site == Gent:
    ...
  endif
endif
```

###### os-related in os-related in non-os-related

This is an example of the basic allowed if-structure `OS_IF_IN_OS_IF` nested in a non-os-specific if.

```
if site == Gent:
  if OS == windows:
    ...
  else:
    if OS == Linux:
      ...
    endif
  endif
endif
```

##### Not allowed

###### non-os-related in os-related in os-related

This is an example of a non-os-related if-structure nested in one of the basic allowed if-structures (`OS_IF_IN_OS_IF`).

```
if OS != windows:
  if OS == Linux:
    if site == Gent:
      ...
    endif
  endif
endif
```

This will result in the parser "forgetting" it opened an os-specific if-statement with OS != windows and not properly closing it.

###### os-related in non-os-related in os-related

This is an example of the basic allowed if-structure `OS_IF` (indirectly) nested in an os-specific if-structure.

```
if OS != windows:
  if site == Gent:
    if OS == Linux:
      ...
    endif
  endif
endif
```

This will also result in the parser "forgetting" it opened an os-specific if-statement with OS != windows and not properly closing it.

### Non OS-related if-statements

Due to the way jinja parses the sourcefiles, the script slightly alters non os-specific if-statements as well. It expects if-statements of the following form:

```
{%- if site == gent %}
{% if site != (gent or brussel) %}
```

All spaces and the dash are optional. City names don't need to be fully lowercase since the parser will capitalize them properly anyway.

### html syntax

The input shouldn't contain any html syntax. While some failsafes are in place, the script isn't made with the use case of handling html syntax in mind. 

### Comments

Any comments within the markdown files (for example TODO's) should follow the following syntax:

```
<!--your comment-->
```
 and should be limited to one line.

Comments can be written in such a way that the script will keep them as input for the bot. To do that, the marker `INPUT_FOR_BOT` should be put in front of the content of the comment as such.

```
<!--INPUT_FOR_BOT: your comment for the bot-->
```

This will be reworked to
 
```
your comment for the bot
```

in the final output.

### Long filepaths

Due to the nature of this script, it can generate large directories with very long names if `deep_directories` is enabled. Depending on the operating system, this can cause problems with filepaths being to long, resulting in files not being able to open. A possible fix for this is to make sure the filepath to where the script is located is not too long. Another solution is lowering the `max_title_depth` or disabling `deep_directories`.

### Markdown lists

The parser is made in a way to detect lists and not split them in multiple paragraphs. The kinds of lists it can detect is all lists with denominators `-`, `+`, `*` and list indexed with numbers or letters (one letter per list entry). It can handle  list entries being spread out over multiple lines if there is an indentation of at least two spaces. It can also handle multiple paragraph list entries in this way, as long as the indentation stays.

### Links

Part of the metadata of the parser are links. In order for the links to be built up in the right way, links to external sites should always start with either `https://` or `http://`.

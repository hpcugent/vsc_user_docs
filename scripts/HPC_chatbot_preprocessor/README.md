# Chatbot parser

`chatbot_parser.py` is a script that transforms the markdown sourcefiles into a structured directory as input for a chatbot. 

## Generated file structure

The generated directory structure is written as a subdirectory of `parsed_mds`. In `parsed_mds`, two subdirectories can be found: 

- `generic` contains the parts of the markdown sources that were non-OS-specific
- `os_specific` contains the parts of the markdown sources that were OS-specific

Within `os_specific` a further distinction is made for each of the three possible operating systems included in the documentation.

These subdirectories then contain a subdirectory for each individual markdown sourcefile. In the file specific subdirectories, further divisions are made according to the titles and subtitles found in that markdown sourcefile. 

Finally, each of these subtitle-specific subdirectories contains a `.txt` file with the (processed) plaintext of that section and at the end a reference link to the corresponding part of the documentation website on <docs.hpc.ugent.be>.

## Requirements

- The required Python packages are listed in `requirements.txt`
- [Pandoc](https://pandoc.org/installing.html) must be installed and must be added to the system PATH

## Usage

The script can be ran in a shell environment with the following command:

```shell
python chatbot_parser.py
```

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

### Allowed html syntax

The script contains a list of html syntax keywords it filters out. If more html syntax keywords are used in the future, it suffices to add them to this list to adapt the script to filter them out. The current list is:
```
["pre", "b", "code", "sub", "br", "center", "p", "div", "u", "p", "i", "tt", "a", "t", "span"]
```
The script is also adapted to take into consideration structures like `<a href="link">` and retain the link.

### Markdown comments

Any comments within the markdown files (for example TODO's) should follow the following syntax:

```
<!--your comment-->
```
 and should be limited to one line.

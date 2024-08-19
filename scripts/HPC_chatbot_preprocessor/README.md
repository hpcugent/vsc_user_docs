# Chatbot parser

`chatbot_parser.py` is a script that transforms the markdown sourcefiles into a structured directory for a chatbot to be trained on. 

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

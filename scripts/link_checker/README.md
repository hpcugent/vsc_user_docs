# Link checker

The link checker consists of two parts:
- A bash script that outputs all links from the HTML files in the build directory along with the path to the file containing the link.
- A Python script that reads the output of the bash script and checks the status code of each link.

The Python script will output all links that return a status code other than 200 (OK) along with the path to the file containing the link.

## Usage

```shell
$ ./generate_links_from_build.sh /path/to/mkdocs/build > links.txt
```

```shell
$ python check_links.py [--whitelist <whitelist.txt>] links.txt
```

The script will not check links that are in the whitelist file. The whitelist file should contain one link per line.
# Module list
A script that generates a list of all available lmod modules in markdown.
It also indicates which package is avalaible on each server. 

## Requirements
- Required Python packages are listed in the `requirements.txt`  file.
- Lmod must be available, $LMOD_CMD must specify path to the lmod binary.

## Usage
You can run the script with following command:

```shell
python module_overview.py
```

## Testing
You can run the tests by running the `test.sh` script.
```shell
./test.sh
```

The tests make use of a mocked `$LMOD_CMD` script, you can find it in [tests/data/lmod_mock.sh](tests/data/lmod_mock.sh).

### Write tests
If you want to write more tests and use this script, yuo need to know a few things.

1. The path to the mocked script needs to be set before every test. You can do this in the `setup_class` function.
2. The output of the command `mock avail cluster/` can be put in a .txt file. 
   You need to assign to path to that file to the `MOCK_FILE_AVAIL_CLUSTER` variable.
3. If you want to make use of the swap command, you need to assign the path to the swap files to the `MOCK_FILE_SWAP` variable.
   You need to put `CLUSTER` into the filename, this will me substituted to the actual cluster name it will swap to.
   
   For example:
   ```
   os.environ["MOCK_FILE_SWAP"] = cls.path + "/data/data_swap_CLUSTER.txt"
   ```
   When trying to swap to, for example, the cluster/dialga cluster.
   It will use the data_swap_dialga.txt file as output for the swap command.
   
### Example 
An example of a possible `setup_class` function is given below.
```python
import os

@classmethod
def setup_class(cls):
    os.environ["TESTS_PATH"] = cls.path
    os.environ["LMOD_CMD"] = cls.path + "/data/lmod_mock.sh"
    os.environ["MOCK_FILE_AVAIL_CLUSTER"] = cls.path + "/data/data_avail_cluster_simple.txt"
    os.environ["MOCK_FILE_SWAP"] = cls.path + "/data/data_swap_CLUSTER.txt"
```

This does multiple things:
1. It sets the path to the test file in `$TESTS_PATH`
2. Sets the path to the `lmod_mock.sh` script in `$LMOD_CMD`
3. Sets the output file for the `module avail cluster/` to the `MOCK_FILE_AVAIL_CLUSTER` variable.
   The actual output can be found in the `data/data_avail_cluster_simple.txt` file.
4. Sets the swap files output to the `MOCK_FILE_SWAP` variable.
   Files with swap outut will have the `data/data_swap_CLUSTER.txt`.
   For example, `data/data_swap_dialga.txt` could be a possible file.
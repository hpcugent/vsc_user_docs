# Module overview

A script to generate an table overview of all available module files in MarkDown format,
which indicates on which clusters each module is available.

## Requirements
- Required Python packages are listed in `requirements.txt` and `requirements_tests.txt`
- [Lmod](https://github.com/TACC/Lmod) must be available, and `$LMOD_CMD` must specify the path to the `lmod` binary.


### Creating a virtual environment (optional)

If the required Python packages are not available in your Python setup,
you can easily create a dedicated virtual environment as follows:

```shell
python -m venv module_overview_venv
source module_overview_venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_tests.txt
# to exit the virtual environment, run 'deactivate'
```

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

The tests make use of a mocked `$LMOD_CMD` script, which you can find [here](tests/data/lmod_mock.sh).

### Write tests
If you want to write additional tests and use the script effectively, follow these guidelines:


1. **Setting up mocked Lmod:**

   Before each test, ensure that you set the path to the script that mocks the `lmod` binary.
   This can be done within the setup_class function.
   ```python
   path = os.path.dirname(os.path.realpath(__file__))
   
   @classmethod
   def setup_class(cls):
       os.environ["LMOD_CMD"] = cls.path + "/data/lmod_mock.sh"
   ```

2. **Mocking output of `module avail cluster` command:**

   The output of the command `module avail cluster/` can be put in a `.txt` file. 
   Set the path to this file in the `$MOCK_FILE_AVAIL_CLUSTER` environment variable.
   ```python
   os.environ["MOCK_FILE_AVAIL_CLUSTER"] = path + "/data/data_avail_cluster_simple.txt"
   ```
   
3. **Mocking the `module swap` command:**

   For mocking the `module swap` command, assign the path to the swap files to the `$MOCK_FILE_SWAP` environment variable.
   Ensure that the filename contains the placeholder '`CLUSTER`', 
   which will later be replaced with the actual cluster name when performing the swap.

   ```python
   os.environ["MOCK_FILE_SWAP"] = path + "/data/data_swap_CLUSTER.txt"
   ```
   When trying to swap to, for example, the `cluster/pikachu` cluster,
   it will use the `data_swap_pikachu.txt` file as output for the swap command.
   
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
1. Set the path of the tests folder in `$TESTS_PATH`
2. Set the path to the `lmod_mock.sh` script in the environment variable `$LMOD_CMD`
3. Set the output file for the `module avail cluster/` to the `MOCK_FILE_AVAIL_CLUSTER` variable.
   The actual output can be found in the `data/data_avail_cluster_simple.txt` file.
4. Set the swap files output to the `MOCK_FILE_SWAP` variable.
   Files with swap outut will have the `data/data_swap_CLUSTER.txt`.
   For example, `data/data_swap_pikachu.txt` could be a possible file.
import os
import subprocess
import numpy as np


def module(*args, filter_fn=lambda x: x) -> np.ndarray:
    """
    API to call the module command.

    @param args: Extra arguments for the module command.
    @param filter_fn: Filter function on the ouput.
    @return:
    """
    lmod = os.getenv('LMOD_CMD')
    proc = subprocess.run(
        [lmod, "python", "-t"] + list(args),
        encoding="utf-8",
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL
    )

    return filter_fn(np.array(proc.stderr.split()))


def avail(name: str = "", filter_fn=lambda x: x) -> np.ndarray:
    """
    API to call the module avail command of Lmod.

    @param name: Possible module name.
    @param filter_fn: Filter on the output.
    @return: List of all available modules of name, or all if name is not given.
    """
    # return module(f"avail {name if name else ''}", filter_fn=filter_fn)
    return module("avail", name, filter_fn=filter_fn)


def swap(name: str) -> None:
    """
    API to call swap command of module.

    @param name: Module you want to swap to.
    """
    module("swap", name)

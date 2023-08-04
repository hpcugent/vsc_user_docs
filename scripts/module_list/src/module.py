import os
import subprocess
import numpy as np


def module(*args, filter_fn=lambda x: x) -> np.ndarray:
    """

    @param args:
    @param filter_fn:
    @return:
    """
    lmod = os.getenv('LMOD_CMD')
    proc = subprocess.run(
        [lmod, "python", "-t"] + list(args),
        encoding="utf-8",
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL
    )

    print(proc)

    return filter_fn(np.array(proc.stderr.split()))


def avail(name="", filter_fn=lambda x: x) -> np.ndarray:
    """

    @param name:
    @param filter_fn:
    @return:
    """
    # return module(f"avail {name if name else ''}", filter_fn=filter_fn)
    return module("avail", name, filter_fn=filter_fn)


def swap(name) -> None:
    """

    @param name:
    """
    module("swap", name)

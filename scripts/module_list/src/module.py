import os
import subprocess


def module(*args):
    lmod = os.getenv('LMOD_CMD')
    proc = subprocess.run(
        [lmod, "python", "-t"] + list(args),
        encoding="utf-8",
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL
    )

    return proc.stderr.split()


def avail(name=None):
    return module(f"avail {name if name else ''}")
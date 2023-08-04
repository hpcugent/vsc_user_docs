import os
import subprocess
import re


def module(*args, regex_filter: str = "") -> list:
    lmod = os.getenv('LMOD_CMD')
    proc = subprocess.run(
        [lmod, "python", "-t"] + list(args),
        encoding="utf-8",
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL
    )

    p = re.compile(regex_filter)
    return list(filter(p.match, proc.stderr.split()))


def avail(name=None, regex_filter: str = "") -> list:
    return module(f"avail {name if name else ''}", regex_filter=regex_filter)

def cat_file():
    import os
    import subprocess
    import sys

    cmd = "type" if sys.platform == "win32" else "cat"

    subp = subprocess.run(
        f'{cmd} {os.path.join("computational_macros", "scripts", "cat_file.py")}',
        shell=True,
        capture_output=True,
    )
    return "<pre><code>" + subp.stdout.decode() + "</code></pre>"

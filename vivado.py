#! /usr/bin/env python3

import os
import sys
import shutil
import pathlib
import subprocess
from typing import List


def test_compile(
    project_path: str,
    testbench_only: bool,
    iverilog_path: str,
    iverilog_params: List[str],
):
    assert os.path.exists(project_path)   


def test_run(
    project_path: str, vivado_path: str, files_to_copy: List[str]
) -> str:
    proj_dir = os.path.dirname(project_path)
    tcl_filename = os.path.join(proj_dir, "run.tcl")
    with open(tcl_filename, "w") as fout:
        fout.write("""open_project "%s"
launch_simulation -simset sim_1
exit
""" % repr(os.path.abspath(project_path))[1:-1])

    cwd = os.path.dirname(project_path)

    for filename in files_to_copy:
        with open(filename) as fin:
            data = fin.read()
        with open(os.path.join(cwd, os.path.basename(filename)), "w") as fout:
            fout.write(data)

    result = subprocess.run([vivado_path, "-mode", "batch", "-source", "run.tcl"], cwd=cwd, capture_output=True)

    if len(result.stderr):
        print(result.stderr.decode("utf-8"), file=sys.stderr)
    
    print(result.stdout.decode("utf-8"))

    return "\n".join(
        [
            s  # "".join(s.split())
            for s in filter(
                lambda x: x.startswith("@"), result.stdout.decode("utf-8").split("\n")
            )
        ]
    )

if __name__ == '__main__':
    test_run(*sys.argv[1:])

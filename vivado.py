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
    sim_dir = os.path.join(proj_dir, next(filter(lambda x: x.endswith('.sim'), os.listdir(proj_dir))), 'sim_1', 'behav', 'xsim')

    tcl_filename = os.path.join(proj_dir, "run.tcl")
    with open(tcl_filename, "w") as fout:
        fout.write("""open_project "%s"
launch_simulation -simset sim_1
run all
exit
""" % repr(os.path.abspath(project_path))[1:-1])

    for filename in files_to_copy:
        with open(filename) as fin:
            data = fin.read()
        with open(os.path.join(sim_dir, os.path.basename(filename)), "w") as fout:
            fout.write(data)

    result = subprocess.run([vivado_path, "-mode", "batch", "-source", "run.tcl"], cwd=proj_dir, capture_output=True)

    if len(result.stderr):
        print(result.stderr.decode("utf-8"), file=sys.stderr)

    return result.stdout.decode("utf-8")

if __name__ == '__main__':
    test_run(*sys.argv[1:])

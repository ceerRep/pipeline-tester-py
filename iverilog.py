#! /usr/bin/env python3

import os
import sys
import pathlib
import subprocess
from typing import List


def test_compile(
    testbench_path: str,
    testbench_only: bool,
    iverilog_path: str,
    iverilog_params: List[str],
):
    cwd = os.path.dirname(testbench_path)
    compile_files: List[str] = []

    if testbench_only:
        compile_files.append(testbench_path)
    else:
        compile_files.extend([str(x) for x in pathlib.Path(cwd).rglob("*.v")])
        compile_files.extend([str(x) for x in pathlib.Path(cwd).rglob("*.sv")])
    # print(compile_files)
    
    if os.path.exists(os.path.join(cwd, "a.out")):
        os.remove(os.path.join(cwd, "a.out"))
    
    result = subprocess.run(
        [iverilog_path, *iverilog_params, *compile_files], capture_output=True, cwd=cwd
    )

    if len(result.stderr):
        print(result.stderr.decode("utf-8"), file=sys.stderr)
    
    if not os.path.exists(os.path.join(cwd, "a.out")):
        raise RuntimeError("Verilog compile failed")    


def test_run(
    testbench_path: str, vvp_path: str, files_to_copy: List[str]
) -> str:
    cwd = os.path.dirname(testbench_path)

    for filename in files_to_copy:
        with open(filename) as fin:
            data = fin.read()
        with open(os.path.join(cwd, os.path.basename(filename)), "w") as fout:
            fout.write(data)

    result = subprocess.run([vvp_path, "a.out"], capture_output=True, cwd=cwd)

    if len(result.stderr):
        print(result.stderr.decode("utf-8"), file=sys.stderr)

    return result.stdout.decode("utf-8")

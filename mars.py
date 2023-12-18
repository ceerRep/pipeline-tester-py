#! /usr/bin/env python3

import os
import sys
import subprocess

from typing import List

MARS_PATH = os.path.join(os.path.dirname(__file__), "Mars.jar")
CODE_TEMP = os.path.join(os.path.dirname(__file__), "code.tmp")


def mars_run(asm_filename: str, mars_run_params: List[str]) -> str:
    result = subprocess.run(
        ["java", "-jar", MARS_PATH, asm_filename, *mars_run_params], capture_output=True
    )

    if len(result.stderr):
        print(result.stderr.decode("utf-8"), file=sys.stderr)

    return result.stdout.decode("utf-8")


def mars_compile(asm_filename: str, im_len: int) -> str:
    result = subprocess.run(
        [
            "java",
            "-jar",
            MARS_PATH,
            asm_filename,
            "dump",
            ".text",
            "HexText",
            CODE_TEMP,
            "a",
            "db",
            "nc",
            "mc",
            "CompactDataAtZero",
        ],
        capture_output=True,
    )

    if len(result.stderr):
        print(result.stderr.decode("utf-8"), file=sys.stderr)

    with open(CODE_TEMP) as fin:
        lines = fin.read().split()
    
    os.remove(CODE_TEMP)

    if len(lines) < im_len:
        lines.extend(['00000000'] * (im_len - len(lines)))

    return '\n'.join(lines)

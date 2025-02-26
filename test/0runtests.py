"""
Run the unit test files.
"""

# Copyright (C) 2021 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
#

import getopt
import os
import pathlib
import subprocess
import sys

# Debugging stuff
from pdb import set_trace as xx

if 0:
    import debug

    debug.SetDebugger()  # Start debugger on unhandled exception

P = pathlib.Path


def eprint(*p, **kw):
    "Print to stderr"
    print(*p, **kw, file=sys.stderr)


def Error(msg, status=1):
    eprint(msg)
    exit(status)


def Usage(status=1):
    name = sys.argv[0]
    s = f"""
Usage:  {name} [options] [file1 ...]
  Run the indicated unit test files.  If there is a failure, the file
  name that failed is printed.

Options:
    -a      Run all the files
    -q      No output; exit status = 0 means all passed, = 1 means at
            least one of the test files failed
    -v      Print the stdout and stderr strings of each file
"""[1:-1]
    print(s)
    exit(status)


def ParseCommandLine(d):
    d["-a"] = False
    d["-q"] = False
    d["-v"] = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ahqv")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("aqv"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(status=0)
    if not args and not d["-a"]:
        Usage(status=1)
    return args


def RunFile(file: P, failed: list):
    cmd = [sys.executable, str(file)]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode:
        out, err = "", ""
        if d["-v"]:
            out = "  stdout:\n" + r.stdout.decode().rstrip()
            err = "  stderr:\n" + r.stderr.decode().rstrip()
        failed.append((f"{file}", out, err))


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    p = P("/plib/test")
    os.chdir(p)
    failed = []
    if not files and d["-a"]:
        for file in p.glob("*_test.py"):
            print(f"Running {file}")
            RunFile(file, failed)
    else:
        for file in files:
            RunFile(P(file), failed)
    if failed:
        if not d["-q"]:
            print("The following test files failed:\n")
            for i, s, e in failed:
                print(f"{i}")
                if d["-v"]:
                    print(f"{s}")
                    print(f"{e}")
                    print("-" * 70)
        exit(1)
    exit(0)

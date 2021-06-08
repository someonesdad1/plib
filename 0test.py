'''

This script will examine the test trigger strings of the python files in
the current directory (use -r options to also search all other
directories) and run the indicated tests.

The trigger strings can be

<empty>     Don't do anything
run         Run the script directly; 0 status means passed
--test      Run with --test option
[a, b...]   One or more test files to run

If there is no test trigger string, nothing will be done.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Run self tests of python scripts with a test trigger string
    #∞what∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import subprocess
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent, indent, Wrap
    from columnize import Columnize
    import color as C
    import trigger
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    class G: pass
    G.red = C.fg(C.lred, s=1)
    G.cyn = C.fg(C.lcyan, s=1)
    G.grn = C.fg(C.lgreen, s=1)
    G.norm = C.normal(s=1)
    P = pathlib.Path
if 1:   # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
    Usage:  {name} [options] file1 [file2...]
      Find the python scripts with self test information in them and run
      the self tests.  If one of the command arguments is a directory, 
      all of its python files have their self tests run.

    Options:
      -h    Print a manpage
      -L    List the files without test trigger strings
      -l    List the files and their actions
      -r    Search for all python files recursively
      -v    Show test results
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-L"] = False     # List the files without trigger string
        d["-l"] = False     # List the files
        d["-r"] = False     # Recursive
        d["-v"] = False     # Verbose
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hLlrv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Llrv"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        return args
if 1:   # Core functionality
    def Run(file):
        if file.suffix == ".py":
            cmd = [sys.executable, str(file)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if d["-v"]:
                if r.stdout:
                    print(r.stdout, end="")
                if r.stderr:
                    print(r.stderr, end="")
            if r.returncode:
                d["failed"] += 1
                print(f"{G.red}{file} test failed{G.norm}")
        else:
            status = os.system(str(file))
            if status:
                d["failed"] += 1
                print(f"{G.red}{file} test failed{G.norm}")
    def GetTestTrigger(file):
        T = d["trigger"]
        triggers = T(file)
        if triggers is not None and "test" in triggers:
            return (file, triggers["test"].strip())
        return None
    def GetFiles(dir, negate=False):
        'Return a sorted list of (files, trigger)'
        p, glb, o, T = P(dir), "*.py", [], d["trigger"]
        for file in p.rglob(glb) if d["-r"] else p.glob(glb):
            triggers = T(file)
            if negate:
                if triggers is None or "test" not in triggers:
                    o.append((file, None))
            else:
                if triggers is not None and "test" in triggers:
                    o.append((file, triggers["test"].strip()))
        return list(sorted(o))
    def ListFilesWithoutTrigger(dir):
        if dir.is_file():
            t = GetTestTrigger(dir)
            if t is not None:
                return
            files = [t]
        else:
            files = GetFiles(dir, negate=True)
        print(f"{G.cyn}Directory = {dir.resolve()}{G.norm}")
        out = []
        for file, trig in files:
            out.append(f"{file!s}")
        for line in Columnize(out, indent=" "*2):
            print(line)
    def ListFiles(dir):
        if dir.is_file():
            t = GetTestTrigger(dir)
            if t is None:
                return
            files = [t]
        else:
            files = GetFiles(dir)
        n = max([len(str(i)) for i, j in files])
        print(f"{G.cyn}Directory = {dir.resolve()}{G.norm}")
        for file, trig in files:
            print(f"  {file!s:{n}s} {trig}")
    def RunTests(dir):
        'Only failed tests have their info printed out'
        if dir.is_file():
            t = GetTestTrigger(dir)
            if t is None:
                return
            files = [t]
        else:
            files = GetFiles(dir)
        count = 0
        for file, trig in files:
            count += 1
            if trig == "run":
                Run(P(file))
            elif trig[0] == "[":
                for testfile in eval(trig):
                    Run(P(testfile))
        return count

if __name__ == "__main__":
    d = {       # Options dictionary
        "trigger": trigger.Trigger(),
        "total": 0,
        "failed": 0,
    }
    dirs = [P(i) for i in ParseCommandLine(d)]
    for dir in dirs:
        if d["-l"]:
            print("Python files with tests:")
            ListFiles(dir)
        elif d["-L"]:
            print("Python files without a test trigger string:")
            ListFilesWithoutTrigger(dir)
        else:
            d["total"] += RunTests(dir)
    t, f = d["total"], d["failed"]
    if f or t:
        p = t - f
        print(f"{G.grn}{p} file{'s' if p != 1 else ''} tested OK{G.norm}")
        if f:
            print(f"{G.red}{f} file{'s' if f != 1 else ''} failed{G.norm}")

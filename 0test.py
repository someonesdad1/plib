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
    # <utility> Run self tests of python scripts with a test trigger
    # string.  A trigger string of "run" means run the script directly.
    # "--test" means run it with this option.  A list of strings
    # specifies one or more test files to run.
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
    from timer import Timer
    import color as C
    import clr
    import trigger
    import dpstr
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    P = pathlib.Path
    # Set up for color printing
    c = clr.Clr(bits=4, override=True)
    c.red = c("lred")
    c.cyn = c("lcyn")
    c.grn = c("lgrn")
if 1:   # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = P(sys.argv[0])
        print(dedent(f'''
    Usage:  {name} [options] file1 [file2...]
      Find the python scripts with self-test information in them and run
      the self-tests.  If one of the command arguments is a directory, 
      all of its python files have their self tests run.
 
      The default behavior with no arguments is to run the self tests on
      the files in the current directory.

      All output is quietly sent to a log file {name.stem}.log.x where x is a
      time stamp.
    Options:
      -C    Remove all log files
      -h    Print a manpage
      -L    List the files without test trigger strings
      -l    List the files and their actions
      -r    Search for all python files recursively
      -v    Show test results (don't show files not run)
      -V    Show test results and show files not run
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-C"] = False     # Remove all log files
        d["-L"] = False     # List the files without trigger string
        d["-l"] = False     # List the files
        d["-r"] = False     # Recursive
        d["-v"] = False     # Verbose
        d["-V"] = False     # Verbose with files not run
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hLlrvV")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("LlrvV"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if not args:
            args = ["."]
        return args
class tee:
    '''This behaves like a stream to allow use to make sure stdout and
    stderr go to their normal locations as well as a log file.
    '''
    def __init__(self, *streams):
        self.streams = streams
    def __del__(self):
        for i in self.streams:
            if i != sys.stdout and i != sys.stderr:
                i.close()
    def write(self, s):
        for i in self.streams:
            i.write(s)
    def flush(self):
        for i in self.streams:
            i.flush()

class TestRunner:
    def __init__(self):
        self.total = 0
        self.failed = 0
        self.not_run = 0
        self.trigger = trigger.Trigger()
    def GetTestTrigger(self, file):
        triggers = self.trigger(file)
        if triggers is not None and "test" in triggers:
            return (file, triggers["test"].strip())
        return None
    def GetFiles(self, dir):
        'Return a sorted list of (files, trigger)'
        p, glb, o = P(dir), "*.py", []
        for file in p.rglob(glb) if d["-r"] else p.glob(glb):
            triggers = self.trigger(file)
            if (triggers is not None and "test" in triggers and 
                triggers["test"].strip()):
                o.append((file, triggers["test"].strip()))
            else:
                o.append((file, None))
        return list(sorted(o))
    def ListFilesWithoutTrigger(self, dir):
        if dir.is_file():
            t = self.GetTestTrigger(dir)
            if t is not None:
                return
            files = [t]
        else:
            files = self.GetFiles(dir)
        # Keep only those with None for the second element
        files = [i for i in files if i[1] is None]
        c.print(f"{c.cyn}Directory = {dir.resolve()}")
        out = []
        for file, trig in files:
            out.append(f"{file!s}")
        for line in Columnize(out, indent=" "*2):
            print(line)
    def ListFiles(self, dir):
        if dir.is_file():
            t = self.GetTestTrigger(dir)
            if t is None:
                return
            files = [t]
        else:
            files = self.GetFiles(dir)
        # Keep only those without None for the second element
        files = [i for i in files if i[1] is not None]
        n = max([len(str(i)) for i, j in files])
        c.print(f"{c.cyn}Directory = {dir.resolve()}")
        for file, trig in files:
            print(f"  {file!s:{n}s} {trig}")
    def Run(self, file, additional=None):
        if file.suffix == ".py":
            cmd = [sys.executable, str(file)]
            if additional is not None:
                cmd.extend(additional)
            r = subprocess.run(cmd, capture_output=True, text=True)
            if d["-v"] or d["-V"]:
                if r.stdout:
                    print(r.stdout, end="")
                if r.stderr:
                    print(r.stderr, end="")
            if r.returncode:
                self.failed += 1
                c.print(f"{c.red}{file} test failed")
        else:
            status = os.system(str(file))
            if status:
                self.failed += 1
                c.print(f"{c.red}{file} test failed")
    def RunTests(self, dir):
        'Only failed tests have their info printed out'
        if dir.is_file():
            t = self.GetTestTrigger(dir)
            if t is None:
                self.not_run += 1
                if d["-V"]:
                    print(f"{file}: no test to run")
                return
            files = [t]
        else:
            files = self.GetFiles(dir)
        for file, trig in files:
            self.total += 1
            if trig is None:
                self.not_run += 1
                if d["-V"]:
                    print(f"{file}: no test to run")
            elif trig == "run":
                self.Run(P(file))
            elif trig == "--test":
                self.Run(P(file), additional=[trig])
            elif trig and trig[0] == "[":
                for testfile in eval(trig):
                    self.Run(P(testfile))
            else:
                self.not_run += 1
                if d["-V"]:
                    print(f"{file}: no test to run")
if __name__ == "__main__":
    d = {}      # Options dictionary
    items = [P(i) for i in ParseCommandLine(d)]
    tr = TestRunner()
    timer = Timer()
    timer.start
    for item in items:
        if d["-l"]:
            if item.is_dir():
                print("Python files with a test trigger string:")
            tr.ListFiles(item)
        elif d["-L"]:
            if item.is_dir():
                print("Python files without a test trigger string:")
            tr.ListFilesWithoutTrigger(item)
        else:
            tr.RunTests(item)
    timer.stop
    t, f, n = tr.total, tr.failed, tr.not_run
    if f or t:
        tm = timer.et
        tm.n = 2
        s = f"(took {tm/60} minutes)" if tm > 60 else f"(took {tm} seconds)"
        print(f"Test summary {s}:")
        passed = t - f - n
        print(f"  {passed} python file{'s' if passed != 1 else ''} tested OK")
        print(f"  {f} python file{'s' if f != 1 else ''} failed")
        print(f"  {n} python file{'s' if n != 1 else ''} were not tested")

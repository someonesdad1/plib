'''

- Trigger string policy
    - None means the file has no testing and shouldn't be listed
    - Empty means its missing and probably needs something
    - Ignore means the file is ignored for testing purposes
    - O
- Log file should have date-time in name.

Testing automation tool
    This script will examine the test trigger strings of the indicated
    files and run their indicated tests.  See the description of these
    strings below.

'''
 
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <utility> Run self tests of python scripts with a test trigger string:
        #   <empty>     Missing; probably needs a test written.
        #   "none"      Has no test and shouldn't be listed.
        #   "ignore"    Has no test; list as ignored file.
        #   "run"       Run the script to run the self-tests.
        #   "--test"    Run script with the '--test' option.
        #   A list of strings specifies one or more test files to run.
        #∞what∞#
        #∞test∞# ignore #∞test∞#
    # Standard imports
        import getopt
        import os
        import pathlib
        import subprocess
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from tee import Print
        from wrap import wrap, dedent, indent, Wrap
        from columnize import Columnize
        from timer import Timer
        from color import TRM as t
        import trigger
        import dpstr
        if 0:
            import debug
            debug.SetDebugger()  # Start debugger on unhandled exception
    # Global variables
        P = pathlib.Path
        # Set up for color printing
        t.red = t("redl")   # For failures
        t.dbg = t("royl")   # Debug output
        t.dbg = t("gryd")   # Debug output
        t.cyn = t("cynl")   # Directories
        t.grn = t("grnl")   # For files we'll run
        t.yel = t("yell")   # For files we'll run
        t.gry = t("gryl")   # For ignored files

if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        name = P(sys.argv[0])
        print(dedent(f'''
        Usage:  {name} [options] file1 [file2...]
          Find the python scripts with self-test information in them and run
          the self-tests.  If one of the command arguments is a directory, 
          all of its python files have their self tests run.  Example:
          an argument of '.' runs the tests on all the files in the current
          directory.
        Options:
          -C    Remove all log files
          -h    Print a manpage
          -L    List the files without test trigger strings
          -l    List the files and their actions
          -r    Search for all python files recursively
          -q    Quiet mode:  only show failures and summary
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug output
        d["-L"] = False     # List the files without trigger string
        d["-l"] = False     # List the files
        d["-q"] = False     # Quiet mode
        d["-r"] = False     # Recursive
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dhLlrq")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dLlrvV"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if not args:
           Usage()
        if d["-d"]:
            Dbg("Debugging turned on")
        return args
    def GetLogFile():
        '''Search the current directory for the set of files that end in
        '.0test'.  Get the largest integer counter and return one larger.
        '''
        def GetNum(s):
            if s.endswith(".0test"):
                try:
                    n = int(s[:-5])
                    return n
                except ValueError:
                    return None
            return None
        n = 1
        for i in P(".").glob("*.0test"):
            m = GetNum(str(i))
            if m is not None:
                if m > n:
                    n = m
        return P(str(n + 1) + ".0test")
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
        print(f"{t.cyn}Directory = {dir.resolve()}{t.n}")
        out = []
        for file, trig in files:
            out.append(f"{file!s}")
        for line in Columnize(out, indent=" "*2):
            print(line)
    def ListFiles(self, dir):
        if dir.is_file():
            T = self.GetTestTrigger(dir)
            if T is None:
                return
            files = [T]
        else:
            files = self.GetFiles(dir)
        # Keep only those without None for the second element
        files = [i for i in files if i[1] is not None]
        n = max([len(str(i)) for i, j in files])
        print(f"{t.cyn}Directory = {dir.resolve()}{t.n}")
        # We'll color code things based on trig:
        #    Green:  run, --test, list of test/ files
        #    Gray:   ignore
        for file, trig in files:
            if trig == "ignore":
                print(f"  {t.gry}{file!s:{n}s} {trig}{t.n}")
            else:
                print(f"  {t.yel}{file!s:{n}s} {t.grn}{trig}{t.n}")
    def Run(self, file, additional=None):
        if file.suffix == ".py":
            cmd = [sys.executable, str(file)]
            if additional is not None:
                cmd.extend(additional)
            r = subprocess.run(cmd, capture_output=True, text=True)
            if not d["-q"]:
                if r.stdout:
                    print(r.stdout, end="")
                if r.stderr:
                    print(r.stderr, end="")
            if r.returncode:
                # Always show a test failure
                self.failed += 1
                print(f"{t.red}{file} test failed{t.n}")
        else:
            status = os.system(str(file))
            if status:
                self.failed += 1
                print(f"{t.red}{file} test failed{t.n}")
    def RunTests(self, dir):
        'Only failed tests have their info printed out'
        if dir.is_file():
            t = self.GetTestTrigger(dir)
            if t is None:
                self.not_run += 1
                if not d["-q"]:
                    print(f"{file}: no test to run")
                return
            files = [t]
        else:
            files = self.GetFiles(dir)
        for file, trig in files:
            self.total += 1
            if trig is None or trig == "ignore":
                self.not_run += 1
                if not d["-q"]:
                    if trig is None:
                        print(f"{file}: no test to run")
                    else:
                        print(f"{file}: testing is ignored for this file")
            elif trig == "run":
                self.Run(P(file))
            elif trig == "--test":
                self.Run(P(file), additional=[trig])
            elif trig and trig[0] == "[":
                for testfile in eval(trig):
                    self.Run(P(testfile))
            else:
                self.not_run += 1
                if not d["-q"]:
                    print(f"{file}: no test to run")

def Dbg(*p, **kw):
    if not d["-d"]:
        return
    print(f"{t.dbg}", end="")
    print(*p, **kw)
    t.out()
def ShowWhatWillBeDone(tr, items):
    # Categories of trigger strings
    empty, none, ignore, run = [], [], [], []
    def Categorize(p, action):
        if 0:
            print(p, action)
        if not action:
            empty.append(p)
        elif action == "none":
            none.append(p)
        elif action == "ignore":
            ignore.append(p)
        else:
            run.append(p)
    def Show(title, seq):
        if seq:
            Dbg(title)
            for i in Columnize(sorted(seq), indent=" "*4):
                Dbg(i)
    for item in items:
        if item.is_dir():
            files = tr.GetFiles(item)
            for p, action in files:
                Categorize(p, action)
        else:
            Categorize(*tr.GetTestTrigger(item))
    # Print results
    Show("Trigger string is 'none':", none)
    Show("Empty trigger string (probably needs a test written):", empty)
    Show("Ignored:", ignore)
    Show("Files with tests to run:", run)

if __name__ == "__main__":
    d = {}      # Options dictionary
    items = [P(i) for i in ParseCommandLine(d)]
    if 1: # Hook up a tee to cause output to go to a log file
        logfile = GetLogFile()
        print("Testing logfile is", logfile)
        logfile_stream = open(logfile, "w")
        saved = sys.stderr
        sys.stderr = logfile_stream
        Print.print = print
        print = Print
        Print.streams = [logfile_stream]
    tr = TestRunner()
    if d["-d"]:
        ShowWhatWillBeDone(tr, items)
    timer = Timer()
    timer.start
    if 1:   # Run the tests
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
    if 1:   # Report
        if f or t:
            tm = timer.et
            tm.n = 2
            s = f"(took {tm/60} minutes)" if tm > 60 else f"(took {tm} seconds)"
            print(f"Test summary {s}:")
            passed = t - f - n
            print(f"  {passed} python file{'s' if passed != 1 else ''} tested OK")
            print(f"  {f} python file{'s' if f != 1 else ''} failed")
            print(f"  {n} python file{'s' if n != 1 else ''} "
                f"{'were' if n != 1 else 'was'} not tested")
    if d["-d"]:
        print(f"{t.n}")
    logfile_stream.close()
    Print.streams.clear()
    print = Print.print
    sys.stderr = saved

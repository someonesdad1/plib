'''

- Look at adding style tests via
  https://pycodestyle.pycqa.org/en/latest/advanced.html#automated-tests
- Trigger string policy
    - None means the file has no testing and shouldn't be listed
    - Empty means its missing and probably needs something
    - Ignore means the file is ignored for testing purposes
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
        #∞test∞# none #∞test∞#
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
        from timer import Timer, fnt
        from color import TRM as t
        import trigger
        import dpstr
        if 0:
            import debug
            debug.SetDebugger()  # Start debugger on unhandled exception
        try:
            import pycodestyle
            have_pycodestyle = True
        except ImportError:
            have_pycodestyle = False
    # Global variables
        P = pathlib.Path
        # Set up for color printing
        t.fail = t("redl")
        t.ok = t("grnl")
        t.ign = t("roy")
        t.dbg = t("purl")
        t.cyn = t("cynl")   # Directories
        t.grn = t("grnl")   # For files we'll run
        t.yel = t("yell")   # For files we'll run
        t.sty = t("ornl")   # Style errors/warnings
        # Files to ignore
        ignore = set((
            P("/plib/trigger.py"),
        ))
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
          directory.  Normally, only test failures cause output; use -v to
          show each of the files that is being run.
        Options:
          -d    Show what will be done and exit
          -r    Recursively search for files
          -s    Include style tests (pycodestyle module needed)
          -S    Like -s, but print the style errors
          -v    Verbose mode:  show what's being tested
          -w    Don't filter out nuisance warnings
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug output
        d["-q"] = False     # Quiet
        d["-r"] = False     # Recursive
        d["-s"] = False     # Style tests
        d["-S"] = False     # Style tests, verbose
        d["-v"] = False     # Verbose:  show ignored
        d["-w"] = False     # Don't filter out warnings
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dqrsSvw")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dqrSsvw"):
                d[o] = not d[o]
        if not args:
            Usage()
        if (d["-s"] or d["-S"]) and not have_pycodestyle:
            print("Warning:  pycodestyle not installed", file=sys.stderr)
        return args
    def GetLogFile():
        'Return a log file name that ends in .0test'
        suffix = fnt() + ".0test"
        return P(".testlog")/suffix
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
            if file.resolve() in ignore:
                continue
            triggers = self.trigger(file)
            if (triggers is not None and "test" in triggers and 
                triggers["test"].strip()):
                o.append((file, triggers["test"].strip()))
            else:
                o.append((file, None))
        return list(sorted(o))
    if 0:   # Functionality not being used
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
            # Run the script's test
            r = subprocess.run(cmd, capture_output=True, text=True)
            if not d["-q"]:
                if d["-v"] and r.stdout:
                    print(r.stdout, end="")
                if r.stderr:
                    if d["-w"]:
                        print(r.stderr, end="")
                    else:
                        # Filter out nuisance warnings
                        ignore = (
                            # The following occurs in sig.py when "0[0]" is
                            # sent to eval() (also happens with "0(0)" and
                            # subscripting a float).  These are valid
                            # expressions for the sig.py module's function,
                            # however.
                            "<string>:1: SyntaxWarning:",
                        )
                        for line in r.stderr.split("\n"):
                            show = True
                            for i in ignore:
                                if i in line:
                                    show = True
                                    break
                                if show:
                                    print(line, file=sys.stderr)
            if (d["-s"] or d["-S"]) and have_pycodestyle:
                # Run style test
                ignore = '''E1 E2 E3 E5 W2'''.split()
                if d["-S"]:
                    style = pycodestyle.StyleGuide(quiet=False, ignore=ignore)
                else:
                    style = pycodestyle.StyleGuide(quiet=True, ignore=ignore)
                result = style.check_files([file])
                if result.total_errors:
                    print(f"{t.sty}Style errors in", file)
            if r.returncode:
                # Always show a test failure
                self.failed += 1
                print(f"{t.fail}{file} test failed{t.n}")
        else:
            status = os.system(str(file))
            if status:
                self.failed += 1
                print(f"{t.fail}{file} test failed{t.n}")
    def RunTests(self, dir):
        'Only failed tests have their info printed out'
        if dir.is_file():
            t = self.GetTestTrigger(dir)
            if t is None:
                self.not_run += 1
                if d["-v"]:
                    print(f"{file}: no test to run")
                return
            files = [t]
        else:
            files = self.GetFiles(dir)
        for file, trig in files:
            self.total += 1
            if trig is None or trig == "ignore":
                self.not_run += 1
                if d["-v"]:
                    if trig is None:
                        print(f"{file}: no test to run")
                    else:
                        print(f"{file}: testing is ignored for this file")
            elif trig == "run":
                # Run as script
                self.Run(P(file))
            elif trig == "--test":
                # Test option
                self.Run(P(file), additional=[trig])
            elif trig and trig[0] == "[":
                # List of files
                for testfile in eval(trig):
                    self.Run(P(testfile))
            else:
                self.not_run += 1
                if d["-v"]:
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
            print(title)
            for i in Columnize(sorted(seq), indent=" "*4):
                print(i)
    for item in items:
        if item.is_dir():
            files = tr.GetFiles(item)
            for p, action in files:
                Categorize(p, action)
        else:
            trig = tr.GetTestTrigger(item)
            if trig:
                Categorize(*trig)
            else:
                Categorize(item, "none")
    # Print results
    print(f"{t('gry')}", end="")
    Show("Trigger string is 'none':", none)
    print(f"{t('ornl')}", end="")
    Show("Empty trigger string (probably needs a test written):", empty)
    print(f"{t('lil')}", end="")
    Show("Ignored:", ignore)
    print(f"{t('grn')}", end="")
    Show("Files with tests to run:", run)
    t.out()

if __name__ == "__main__":
    d = {}      # Options dictionary
    items = [P(i) for i in ParseCommandLine(d)]
    if not d["-d"]:     # Hook up a tee to cause output to go to a log file
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
        exit(0)
    if 1:   # Run the tests
        timer = Timer()
        timer.start
        for item in items:
            tr.RunTests(item)
        timer.stop
    if 1:   # Report
        if tr.total:
            tm = timer.et
            tm.n = 2
            s = f"(test time = {tm/60} minutes)" if tm > 60 else f"(took {tm} seconds)"
            print(f"{t('lav')}Test results {s}:")
            T, F, N = tr.total, tr.failed, tr.not_run
            ok = T - F - N
            print(f'''  {t.ok}{ok} OK{t.n}, '''
                  f'''{t.fail}{F} failed{t.n}, '''
                  f'''{t.ign}{N} not tested{t.n}''')
    logfile_stream.close()
    Print.streams.clear()
    print = Print.print
    sys.stderr = saved

'''
     
New design
    0test.py cmd

        Each file with a gist & testing instructions is run.  A class holds each file
        and captures its stdout, stderr, and return status.  A status of 0 means the 
        test passed and > 0 means a failure.  All the test data are cached to a file.
        The testing commands are

        scan [dirs]     Show the different categories of gists
        test files      Run the tests on each file and cache results
        report [cmd]    Report on the last test run

    class TestFile
        - Holds a single file for testing purposes
        - Running a test captures & caches stdout, stderr, return status
        - The file's current hash is gotten and if it hasn't changed from the last run,
          this file isn't tested.
        - Each instance gets a reference to a timer, which is uses to measure how long
          its test takes to run and put into the et[s] attribute.
   
    class TestRunner
        - Takes a list of files and constructs a TestFile object for each file.
        - Actions:
            - scan
            - test
            - report
        - Get working with single process, then use multiprocessing for faster execution

    Thoughts
        - Use /plib/.0test as a cache of the last testing information, keeping file
          hash, timedate of test, and test result.  This would allow avoiding running a
          test if the file passed last time and the hash hasn't changed.  In fact, the
          cache dict is exposed to each TestRun instance so it can decide what to do
          when runtest() is called.

    Old design
            - Look at changing default behavior:  'python 0test.py' looks for every
              python file in the current file and runs its self tests.  This means
              keeping things up to date.
                - Cache the file's hash in a hidden data file so that if the hash hasn't
                  changed, then the test isn't run.
                    - A -f option can override this
            - Trigger string policy
                - 'run', '--test', 'notest', 'testdir' are the allowed choices
                - An empty trigger string results in an exception
            - Commands
                - scan:  print a report on the trigger string of each file
                - test:  Run the tests
    
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Run the tests of the indicated python files oo>
        <oo desc ∞ 
            This script will examine the gist strings of the indicated files and run their
            indicated tests.
        oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ 
            MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 

            - 

        oo>
    '''
    if 1:  # Standard imports
        from collections import namedtuple, deque, defaultdict
        import enum
        import getopt
        import hashlib
        import os
        import pathlib
        import subprocess
        import sys
    if 1:  # Custom imports
        import get
        import gist
        from tee import Print
        from wrap import dedent
        from columnize import Columnize
        from timer import Timer, fnt
        from color import t
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()  # Start debugger on unhandled exception
    if 1:  # Global variables
        P = pathlib.Path
        class G:
            pass
        g = G()
        g.dbg = False
        g.dbg = True #∞∞ 
if 1:  # Classes 
    class File:
        '''Holds the name of a python file that will be tested.
        '''
        bytes_to_hash = 4096
        def __init__(self, file):
            self.file = P(file)
            self.hash = self.get_hash()
            # Get file's gist
            s = gist.Gist.GetGistString(self.file)
            try:
                mygist = gist.Gist(s)
            except Exception:
                t.print(f"{t.err}No gist in {file}")
                exit(1)
            # This file's method of testing
            self.test = mygist["test"].strip()
            # Other attributes
            self.status = None
            self.stdout = None
            self.stderr = None
        def run(self, *args):
            'Return (status, self) where status is "pass", "fail", "notest"'
            if self.test == "notest":
                Dbg(f"run:  {str(self.file)!r} is notest")
                return ("notest", self)
            elif self.test == "run" or self.test == "--test":
                cmd = [sys.executable, self.file]
                if self.test == "--test":
                    cmd += ["--test"]
                r = subprocess.run(cmd, capture_output=True)
                self.status = r.returncode
                self.stdout = r.stdout
                self.stderr = r.stderr
                self.returncode = "fail" if self.status else "pass"
                return ("pass" if not self.status else "fail", self)
            else:
                raise ValueError(f"Bug:  {self.test!r} not coded yet")
        def get_hash(self):
            m = hashlib.sha1()
            fp = self.file.open("rb")
            bytes = fp.read(File.bytes_to_hash)
            fp.close()
            m.update(bytes)
            return m.hexdigest()
        def __str__(self):
            return f"File<{self.file}>"
        def __repr__(self):
            return str(self)
        def dbgdump(self):
            'Print state after run() to stdout'
            msg = f"Testing:  {t.file}{str(self.file)!r}{t.dbg} ({self.test}) "
            msg += f"{t.failed}fail" if self.status else f"{t.passed}pass"
            Dbg(msg)
            if self.stdout:
                Dbg(f"  stdout ={t.n} {self.stdout}")
            if self.stderr:
                Dbg(f"  stderr ={t.pnk} {self.stderr}")

    class TestRunner:
        '''Initialize with a list of files.  Each file will be examined for a gist to
        determine how the file is to be tested.  Each file with a proper way of testing
        will be tested and and the output to stdout/stderr is cached.

        '''
        def __init__(self, dirs):
            self.files_or_dir = files_or_dirs

if 0:   # Old stuff
    g.teststr = "#∞test∞#"      # Marks a test directive in a python script
    # Named tuples
    if 1:   # Test information
        # This core data structure holds the name of each file in a directory along
        # with the tstr = test_string, describing how this file is to be tested.
        # Here are the different types that can be found:
        #  +  ""          Null; no g.teststr found in the file
        #  +  "empty"     No string between the g.teststr locations
        #     "notest"    No test needs to be run for this file
        #     "run"       Run the file to run the self tests
        #     "-t"        Run the file with this argument to test
        #     "--test"    Ditto
        #     "['test/abc.py']"    A list of testing scripts to be run
        # + means that file needs attention (an exception will be raised)
        Test = namedtuple("Test", "dir file tstr")
    if 0:   # Classes (old)
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
                "Return a sorted list of (files, trigger)"
                p, glb, o = P(dir), "*.py", []
                for file in p.rglob(glb) if d["-r"] else p.glob(glb):
                    if file.resolve() in ignore:
                        continue
                    triggers = self.trigger(file)
                    if triggers is not None and "test" in triggers and triggers["test"].strip():
                        o.append((file, triggers["test"].strip()))
                    else:
                        o.append((file, None))
                return list(sorted(o))
            if 0:  # Functionality not being used
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
                    for line in Columnize(out, indent=" " * 2):
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
                "Only failed tests have their info printed out"
                if dir.is_file():
                    t = self.GetTestTrigger(dir)
                    if t is None:
                        self.not_run += 1
                        if d["-v"]:
                            print(f"{dir}: no test to run")
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
    if 0:   # Old functionality
        def Dbg(*p, **kw):
            if not g.dbg:
                return
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
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
                    for i in Columnize(sorted(seq), indent=" " * 4):
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
    if 0:   # Identify files that need testing
        def GetTestString(file, exception_on_none=True):
            '''Return the test string for this file; the valid returned strings are:
                ""        No g.teststr found in file      --> Needs attention
                "empty"   g.teststr found, but no data    --> Needs attention
                "notest"  This file doesn't need to be tested
                "run"     Run the file as a script to test
                "-t"      Run as script with -t option
                "--test"  Run as script with --test option
                "testdir" Look in /plib/test for appropriately named script
            If exception_on_none is True, then a ValueError exception is raised on a file
            with "" or "empty".
            '''
            found = None
            dq = deque(get.GetLines(file,  ignore_empty=True))
            linenum = 0
            while dq:
                line = dq.popleft()
                linenum += 1
                loc = line.find(g.teststr)
                if loc == -1:
                    continue
                Dbg(f"Found {g.teststr!r} on line {linenum}:  {t.lill}{line!r}")
                line = line[loc + len(g.teststr):].strip()   # Strip off leading junk
                # Must have a second g.teststr at end of line
                loc = line.find(g.teststr)
                if loc == -1:
                    msg = f"{t.ornl}{file}:  missing {t.lill}{g.teststr!r}{t.ornl} at end of line {linenum}{t.n}"
                    raise ValueError(msg)
                found = line[:loc].strip()
                Dbg(f"Test string = {found!r}")
                break
            # Check that we have a valid value
            msg = ""
            if found is None:
                msg = f"{t.ornl}{file}:  no test string{t.n}"
            elif not found or found == "empty":
                msg = f"{t.ornl}{file}:  empty test string{t.n}"
            elif found in ("run", "-t", "--test", "notest", "testdir"):
                pass
            else:
                raise ValueError(f"{found!r} is an unrecognized value in {file!r}")
            if msg:
                if 0:   # Use this to stop on a missing test string
                    raise ValueError(msg)
                else:   # Use this to just print a message and finish processing
                    print(msg)
            return found
        def GetTestStrings(dir):
            'Return a deque of named tuples with test information'
            o = []
            p = P(dir)
            files = p.glob("*.py")
            for file in files:
                tstr = GetTestString(file)
                o.append(Test(dir, str(file), tstr))
            return deque(o)
        def Report():
            'Show file test string by category'
            dq, d = GetTestStrings("."), defaultdict(list)
            total_files = len(dq)
            while dq:
                item = dq.popleft()
                d[item.tstr].append(str(item.file))
            for i in d:
                n = len(d[i])
                t.print(f"{t.grn}{i}{t.n} ({n} items)")
                for j in Columnize(sorted(d[i]), indent=" "*4):
                    print(j)
            print(f"{total_files} total python files")
if 0:  # Old utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        name = P(sys.argv[0])
        print(
            dedent(f'''
        Usage:  {name} [options] file1 [file2...]
          Find the python scripts with self-test information in them and run the
          self-tests.  If one of the command arguments is a directory, all of its python
          files have their self tests run.  Example: an argument of '.' runs the tests
          on all the files in the current directory.  Normally, only test failures cause
          output; use -v to show each of the files that is being run.
        Options:
          -d    Show what will be done and exit
          -r    Recursively search for files
          -s    Include style tests (pycodestyle module needed)
          -S    Like -s, but print the style errors
          -v    Verbose mode:  show what's being tested
          -w    Don't filter out nuisance warnings
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False  # Debug output
        d["-q"] = False  # Quiet
        d["-r"] = False  # Recursive
        d["-s"] = False  # Style tests
        d["-S"] = False  # Style tests, verbose
        d["-v"] = False  # Verbose:  show ignored
        d["-w"] = False  # Don't filter out warnings
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dhqrsSvw")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dqrSsvw"):
                d[o] = not d[o]
        if not args or o == "-h":
            Usage()
        if (d["-s"] or d["-S"]) and not have_pycodestyle:
            print("Warning:  pycodestyle not installed", file=sys.stderr)
        return args
    def GetLogFile():
        "Return a log file name that ends in .0test"
        suffix = fnt() + ".0test"
        return P(".testlog") / suffix

if __name__ == "__main__":
    import cmddecode
    if 0:   # Old functionality
        d = {}  # Options dictionary
        items = [P(i) for i in ParseCommandLine(d)]
        if not d["-d"]:  # Hook up a tee to cause output to go to a log file
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
        if 1:  # Run the tests
            timer = Timer()
            timer.start
            for item in items:
                tr.RunTests(item)
            timer.stop
        if 1:  # Report
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
    if 1:   # Utility
        def GetColors():
            t.failed = t.redl
            t.passed = t.grnl
            t.file = t.brnl
            t.err = t.redl
            t.dbg = t.lill if g.dbg else ""
            t.dbg1 = t.brnl if g.dbg else ""
            t.N = t.n if g.dbg else ""
        def GetScreen():
            'Return (LINES, COLUMNS)'
            return (
                int(os.environ.get("LINES", "50")),
                int(os.environ.get("COLUMNS", "80")) - 1
            )
        def Dbg(*p, **kw):
            if g.dbg:
                print(f"{t.dbg}", end="")
                print(*p, **kw)
                print(f"{t.N}", end="")
        def Warn(*msg, status=1):
            print(*msg, file=sys.stderr)
        def Error(*msg, status=1):
            Warn(*msg)
            exit(status)
        def Usage(status=0):
            print(dedent(f'''
            Usage:  {sys.argv[0]} [options] cmd [args]
              Excecute the indicated testing commands:
                scan [dirs]   Identify files to be tested
                test            Test the cached file names
                report          Report on the last test run
            Options:
              -x re   Regex for files to ignore
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-v"] = False     # Debug mode
            d["-d"] = 3         # Number of significant digits
            if len(sys.argv) < 2:
                Usage()
            try:
                opts, args = getopt.getopt(sys.argv[1:], "hv") 
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("v"):
                    d[o] = not d[o]
                elif o == "-d":
                    try:
                        d[o] = int(a)
                        if not (1 <= d[o] <= 15):
                            raise ValueError()
                    except ValueError:
                        Error(f"-d option's argument must be an integer between 1 and 15")
                elif o == "-h":
                    Usage()
            if d["-v"]:
                g.dbg = True
            GetColors()
            if g.dbg:   # Dump options dictionary
                Dbg(f"Command line:  {t.dbg1}{sys.argv!r}")
                Dbg("Options dictionary:")
                for key in d:
                    Dbg(f"  {key}:  {t.dbg1}{d[key]!r}")
            return args
    if 1:   # Core functionality
        pass
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
if 0:
    test = []
    for file in files:
        tst = File(file)
        test.append(tst)
else:   # Prototyping stuff
    f = File("abbreviations.py")
    code, instance = f.run()
    instance.dbgdump()
    exit()

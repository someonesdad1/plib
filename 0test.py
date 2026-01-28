'''
     
New design
    - 0test.py cmd
        - list      Show test state of all files
        - action    Show files I need to take action on
        - test      Run the tests (any arguments are files or directories)
        - report    Show results of last run (cached data)
    - ToDo
        - Get commands working
        - Implement the cache for better testing speed
        - Use multiprocessing for faster testing

    - list [single dir or list of files]
        - Show categorized list of all python files
            - Have a gist:  Required keywords: gist test.  The test values are:
                - Ignored:  notest
                - Have selftest:  run, --test
                - Unrecognized gist
            - Missing gist
                - In ignore file
                - Not in ignore file
    - action [single dir or list of files]
        - Purpose:  show me files I need to take action on:
            - test string
                - notest? are types that might need some selftests
                - '' missing a test spec
                - <nogist> at all and not being ignored
        - Defaults to '.'.  Shows a colorized list of all python files:
            - gryl      Has selftests
            - gry       Is notest
            - ornl      Doesn't contain a gist and isn't in ignore list
        - A color key is printed at the bottom.

    - test [single dir or list of files]
        - Purpose:  run the tests in the dirs or the specified files
        - Defaults to '.'.  Runs the selftests.  Use -v for verbosity level:
            - 0 (default)  Will only print out failed tests
            - 1 Includes notest files
            - 2 Shows for all tested files
        - Caches test results
            - Creates a dict 'results'
                - key = filename
                - value = (file's hash (first 4k bytes), last_test_time, last_test_status)
            - The dict is only written to if the last test of the file passed
            - This dict is used to quickly decide if a file needs to be tested again
            - No error if file isn't present when script is run
            - File is written after each run; the dict is pickled





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
        import time
    if 1:  # Custom imports
        import cmddecode
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
if 1:  # Classes 
    class TestFile:
        '''Holds the name of a python file that will be tested.  Gets the file's hash,
        runs the test, and stores the results.  Typical usage is

            file = TestFile(myfilename)
            status, myinstance = file.run()  # Run this file's test
            status will be "fail" or "pass'
            myinstance is the TestFile instance, useful for the calling context to store
            away in a persistence container.

        Information stored in this class as attributes:
            - file      pathlib.Path to file
            - hash      SHA-1 hash of first 4 kB of file
            - test      Gist keyword indicating how to test
            - retcode   "fail" or "pass" ("pass" only if status == 0)
            - status    Integer return code of running the test
            - et        Elapsed time in s to run test
            - tm        Date/time string when test was run
            - stdout    String the test code sent to stdout
            - stderr    String the test code sent to stderr
        '''
        bytes_to_hash = 4096
        def __init__(self, file):
            self.file = P(file)
            self.hash = self.get_hash()
            self.test = None
            self.status = None
            self.stdout = None
            self.stderr = None
            self.retcode = None
            # Get file's gist
            s = gist.Gist.GetGistString(self.file)
            try:
                mygist = gist.Gist(s)
            except Exception:
                Dbg(f"{t.err}No gist in {file}")
                return
            # This file's method of testing
            self.test = mygist["test"].strip()
        def run(self, *args):
            'Return (status, self) where status is "pass", "fail", "notest"'
            if self.test == "notest":
                return ("notest", self)
            elif self.test == "run" or self.test == "--test":
                cmd = [sys.executable, self.file]
                if self.test == "--test":
                    cmd += ["--test"]
                self.tm = time.asctime()
                start = time.time()             # Time from epoch in s
                r = subprocess.run(cmd, capture_output=True)
                self.et = time.time() - start   # Elapsed time in s for test to run
                self.status = r.returncode
                self.stdout = r.stdout
                self.stderr = r.stderr
                self.retcode = "fail" if self.status else "pass"
                return self.retcode
            else:
                raise ValueError(f"Bug:  {self.test!r} not coded yet")
        def get_hash(self):
            m = hashlib.sha1()
            with self.file.open("rb") as fp:
                bytes = fp.read(TestFile.bytes_to_hash)
            m.update(bytes)
            return m.hexdigest()
        def __str__(self):
            return f"TestFile<{self.file}>"
        def __repr__(self):
            return str(self)
        def dump(self, verbose=False):
            '''Print the state after the test run.  If verbose is True, include the
            contents of stdout and stderr.  The output is plain text except for showing
            'notest' in color and highlighting 'fail' in bright red.  If verbose is true
            and there's output to stderr, it will be highlighted in color too.
            '''
            if self.status is None:
                t.print(f"{t.err}Test has not been run yet")
                return
            if self.test == "notest":
                msg = f"{str(self.file)!r} ({t.notest}{self.test}{t.n}) "
            else:
                msg = f"{str(self.file)!r} ({self.test}) "
            msg += f"{t.failed}fail{t.n}" if self.retcode == "failed" else "pass"
            print(msg)
            if verbose:
                if self.stdout:
                    print(f"  stdout = {self.stdout}")
                if self.stderr:
                    t.print(f"  stderr ={t.pnk} {self.stderr}")

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
    import gist
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
        def ShowColors(msg):
            t.list(msg)
        def GetColors():
            t.failed = t("whtl", "redl")
            t.passed = t.grnl
            t.notest = t.roy
            t.file = t.brnl
            t.err = t.redl
            t.warn = t.ornl
            t.dbg = t.lill
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
              X is a single directory or a list of files
                list X      Show test state of all files
                action X    Show files that need action
                test X      Run the tests on the files
                report X    Report on the last test run
            Options:
              -i file   File with list of files to ignore
              -x r      Regex for files to ignore
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-v"] = 0         # Verbosity level
            d["-d"] = False     # Turn debug on
            if len(sys.argv) < 2:
                Usage()
            try:
                opts, args = getopt.getopt(sys.argv[1:], "dhv:") 
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("d"):
                    d[o] = not d[o]
                elif o == "-v":
                    try:
                        d[o] = int(a)
                    except ValueError:
                        Error(f"-d option's argument must be an integer")
                elif o == "-h":
                    Usage()
            if d["-d"]:
                g.dbg = True
            GetColors()
            g.L, g.W = GetScreen()
            if not args:
                Usage()
            if g.dbg:   # Dump command line and options dictionary
                Dbg(f"Command line:  {t.file}{sys.argv!r}")
                Dbg("Options dictionary:")
                for key in d:
                    Dbg(f"  {key}:  {t.file}{d[key]!r}")
                Dbg("Defined attributes for t:")
                ShowColors("")
                Dbg("-"*g.W)
            return args
    if 1:   # Core functionality
        def ReadCache():
            Dbg(f"{t.warn}Need to write ReadCache()")
        def SaveCache():
            Dbg(f"{t.warn}Need to write SaveCache()")
        def Action(args):
            Dbg(f"Action({t.file}{args}{t.dbg})")
        def Test(args):
            Dbg(f"Test({t.file}{args}{t.dbg})")
        def Report(args):
            Dbg(f"Report({t.file}{args}{t.dbg})")

        def List(args):
            Dbg(f"List({t.file}{args}{t.dbg})")
            files = [P(i) for i in args]
            items_to_test = []
            if len(files) == 1 and files[0].is_dir():
                dir = files[0]
                for file in sorted(dir.glob("*.py")):
                    tf = TestFile(file)
                    items_to_test.append(tf)
                Dbg(f"Got {len(items_to_test)} files in directory {dir}")
            else:
                # It must be a list of files to check
                if not all(i.is_file() for i in files):
                    Error("For multiple arguments, all must be files")
                # Create TestFile instance for each file
                for file in files:
                    tf = TestFile(file)
                    items_to_test.append(tf)
                Dbg(f"Got {len(items_to_test)} files")
            if not items_to_test:
                Error(f"{t.err}No files found to test{t.n}")
            # Classify these files
            o = defaultdict(list)
            for tf in items_to_test:
                o[tf.test].append(tf.file)
            # Print out by test string category
            if o:
                s = "Python file 'test' string in gist"
                t.print(f"{t.yell}{s:^{g.W - 10}s}")
                for key in o:
                    t.print(f"{t.ornl}{key}")
                    p = [str(k) for k in o[key]]    # Get file's string
                    if key is None:
                        print(f"{t.denl}", end="")
                    elif key == "notest":
                        print(f"{t.purl}", end="")
                    for j in Columnize([str(k) for k in o[key]], indent=" "*2, sep=" "*2):
                        print(j)
                    t.print(end="")

    if 1:   # Get input
        d = {
            # This will hold the test results, keyed by file name
            # Values are the File instance
            "cache": {}
        }      # Options dictionary
        cmds = cmddecode.CommandDecode("list action test report".split())
        args = ParseCommandLine(d)
        cmd = args.pop(0)
        got = cmds(cmd)
        ReadCache()
        if len(got) == 1:
            command = got[0]
            if not args:
                args = ["."]
            if command == "list":
                List(args)
            elif command == "action":
                Action(args)
            elif command == "test":
                Test(args)
            elif command == "report":
                Report(args)
        else:
            Error(f"{cmd!r} not recognized")
        SaveCache()

if 0:
    test = []
    for file in files:
        tst = File(file)
        test.append(tst)
    # Perform the tests and report
    for item in test:
        status, instance = item.run()
        instance.dump()

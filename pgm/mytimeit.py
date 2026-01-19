_pgminfo = '''
<oo desc
    Uses timeit module to time a function or script
oo>
<oo cr Copyright © 2026 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat util oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from pathlib import Path as P
        import getopt
        import os
        import sys
        from timeit import timeit
        import subprocess
    if 1:   # Custom imports
        import timer
        from f import flt
        from wrap import dedent
        from color import t
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        # Variables from the command line arguments
        g.n = 1     # Number of times to repeat timing measurement
        g.file = None
        g.func = None
if 1:   # Utility
    def GetColors():
        t.err = t.redl
        t.dbg = t.gry if g.dbg else ""
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
        Usage:  {sys.argv[0]} [options] n file [function]
          Run the script in file n times and report the elapsed time.  If function is
          given, import the file and run the function, reporting on the function's
          timing.  You can leave n out if you wish and it will default to 1.
           
          Caution:  if you're timing a function, you'd be wise to make n a reasonably
          large number (the python timeit module uses 1e6 as the default) to average out
          the problems with a multitasking system.
        Options:
            -d      Set number of significant figures [{d["-d"]}]
            -v      Turn on debugging comments
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 2         # Number of significant digits
        d["-v"] = False     # Dbg on
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:hn:v") 
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
                    Error("-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = False
        if d["-v"]:
            g.dbg = True
        GetColors()
        return args
if 1:   # Core functionality
    def GetArguments(args):
        'args will be of length 1 to 3'
        def CheckFile(file):
            if file is None:
                Error("No file was given")
            if not file.exists():
                Error(f"{file} doesn't exist")
            if file.parent != P("."):
                Error(f"{file} must be in the current directory")
        n, file, func = 1, None, None
        currdir = P(".")
        if len(args) == 1:
            try:
                n = int(args[0])
            except ValueError:
                file = P(args[0])
        elif len(args) == 2:
            try:
                n = int(args[0])
                file = P(args[1])
            except ValueError:
                file = P(args[0])
                func = args[1]
        elif len(args) == 3:
            try:
                n = int(args[0])
            except ValueError:
                Error(f"{args[0]!r} is not an integer")
            file = P(args[1])
            func = args[2]
            if not func:
                Error("func can't be an empty string")
        else:
            Error("Too many arguments on command line")
        # Check we got what we wanted
        if n < 1:
            Error("The integer n must be > 0")
        CheckFile(file)
        Dbg(f"Getarguments:  n = {n}  file = {file}  func = {func}")
        g.n = n
        g.file = file
        g.func = func
    def ExecuteFile():
        s = "time" if g.n == 1 else "times"
        Dbg(f"Execute file:  {g.file!r} {g.n} {s}")
        cmd = [sys.executable, g.file]
        Dbg(f"cmd = {cmd!r}")
        for i in range(g.n):
            with timer.Timer() as tm:
                subprocess.run(cmd, capture_output=True)
            t.print(f"{i}: Time to run {g.file!s} = {t.ornl}{tm.et.engsi}s")
    def ExecuteFunction():
        sf = str(g.file)
        filename = sf.replace(".py", "") if sf.endswith(".py") else sf
        s = "time" if g.n == 1 else "times"
        # Put the file into our local namespace
        exec(f"import {filename}")
        cmd = f"{filename}.{g.func}()"
        # Do the timing
        tm = timeit(cmd, globals=locals(), number=g.n)
        tm = flt(tm)/g.n
        # Report
        u = "Mean t" if g.n > 1 else "T"
        t.print(f"{u}ime to run {g.func!r} {g.n} {s} = {t.ornl}{tm.engsi}s")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    GetArguments(args)
    if g.func is not None:
        ExecuteFunction()
    else:
        ExecuteFile()

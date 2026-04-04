'''

Experimental module for using GNU units for processing unit string expressions.  Goals
are:
    - Get 15 digit conversion factors
    - Do dimensional algebra
    - Recognize a variety of units

Conversion of mi/s to m/s:  returned [b'1609.344']
    - Note that 15 digits were asked for, but 7 were returned.  This can be used by the
      Num machinery to cause the local instance of the number be formatted to 7 figures
      only
        
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import getopt
        import os
        import pathlib
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        import columnize
        import dpstr
        import dptypes
        import f
        import trm
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Experiment:  GNU units access via pipe"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = ""
        __todo__      = '''
            
            -

        '''
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        namedtuple = collections.namedtuple
        #
        Columnize = columnize.Columnize
        dedent = wrap.dedent
        flt = f.flt
    if 1:   # Global variables
        t = trm.Trm()
        g = dptypes.Constant()
        g.dbg = False
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        t.dbg = "lil"
        t.err = "redl"
    def Dbg(*p, **kw):
        if not hasattr(Dbg, "file"):
            Dbg.file = sys.stdout
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.n}", end="", file=Dbg.file)
    def Warning(*msg, **kw):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warning(f"{t.err}", end="")
        Warning(*msg)
        Warning(f"{t.n}")
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [arg1 [arg2...]]
          Describe behavior
        Options:
            -a      Describe
            -d n    Number of significant digits
            -h      Print help
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Description
        d["-d"] = 3      # Description
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except Exception:
                    Error(f"{o!r} option must be an int between 1 and 15")
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Classes
    pass
if 1:   # Functions
    pass

if 0:   # Demonstrate a conversion via a single process call
    p = subprocess.PIPE
    loc = "/home/don/.0rc/bin"
    pgm = f"{loc}/units"
    defn = f"{loc}/definitions.units"
    cmd = [pgm, "-f", defn, "-d", "15", "-t", "mi/s", "m/s"]
    proc = subprocess.Popen(cmd, stdout=p, stderr=p)
    lines = [i.strip() for i in proc.stdout.readlines()]
    print(lines)
    exit()

if 1:   # Demonstrate opening a pipe for continuous conversation
    def units_repl():
        loc = "/home/don/.0rc/bin"
        pgm = f"{loc}/units"
        defn = f"{loc}/definitions.units"
        # We use -t (terse) for clean output and -e (exponential) if needed.
        # We do NOT use -f here if we want the default units, but since you
        # have a custom path, we keep it.
        cmd = [pgm, "-f", defn, "-d", "15", "-t"]
        # Start the "Engine"
        # bufsize=1 and universal_newlines=True (text mode) makes line-by-line comms easier
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print(f"--- GNU Units Bridge Active (PID: {proc.pid}) ---")
        print("Enter conversion (e.g., 'mi/s <enter> m/s') or Ctrl+C to exit.\n")
        try:
            while True:
                # 1. Get User Input
                try:
                    have_unit = input("Have: ").strip()
                    want_unit = input("Want: ").strip()
                except EOFError:
                    break
                if not have_unit or not want_unit:
                    continue
                # 2. Send to the Pipe
                # We send both lines followed by a newline
                proc.stdin.write(f"{have_unit}\n{want_unit}\n")
                proc.stdin.flush()
                # 3. Read the Response
                # In terse mode, units returns exactly one line for the factor.
                # However, if there's an error (non-conformable), it hits stderr.
                response = proc.stdout.readline().strip()
                if response:
                    print(f"Result: {response}")
                else:
                    # Check if it's a 'conformability error' or syntax error
                    # We use a non-blocking check or simply read the error line
                    err = proc.stderr.readline().strip()
                    print(f"ERROR: {err}")
        except KeyboardInterrupt:
            print("\nShutting down the bridge...")
        finally:
            proc.stdin.close()
            proc.terminate()
            proc.wait()
    units_repl()
    exit()

if __name__ == "__main__":  
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        import lwtest
    if 1:   # Import symbols
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
    if 0:   # For script
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        if args:
            for arg in args:
                pass    # Do stuff
    else:   # For module
        def Demo():
            pass
        def Test_Me():
            pass
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])

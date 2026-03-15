'''

Central module for sourcing data
    The trailing letters of the function names give a clue to what is returned.

    GetCategoryNames_di     Gist category names

'''
if 1:  # Header
    if 1:   # Standard imports
        import getopt
        import os
        import sys
    if 1:   # Custom imports
        import dptypes
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        g = dptypes.Constant()
        g.dbg = False
if 1:   # Functions
    def GetCategoryNames_di():
        '''Return a dict of category names allowed in gists
        key     <= 4 letter abbreviation
        value   Description of use
        '''
        return dptypes.SlushDict({
            "astr": "Astronomy",
            "clr" : "Color",
            "data": "Data for module/script tasks",
            "elec": "Electrical",
            "math": "Math",
            "prog": "Programming",
            "sci" : "Science",
            "shop": "Shop",
            "text": "Text processing",
            "time": "Time",
            "util": "Utility",
        })

if __name__ == "__main__":  
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        import lwtest
        import trm
        import wrap
    if 1:   # Import symbols
        Assert = lwtest.Assert
        dedent = wrap.dedent
        raises = lwtest.raises
        run = lwtest.run
        t = trm.Trm()
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
            Usage:  {sys.argv[0]} [options] [func1 [func2...]]
            List my shell functions.
            Options:
                -a      List all functions with description
                -h      Print a manpage
                -o      List other functions (from e.g., gawk, conda, git, etc.)
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
    if 0:   # For script
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        if args:
            pass
            #for arg in args:
            #    pass
    else:   # For module
        def Demo():
            pass
        def Test_GetCategoryNames_di():
            di = GetCategoryNames_di()
            Assert(len(di) > 10)
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])

def GetGist():
    gist = {}
    gist["gist"] = "Central module for sourcing data"
    gist["copy"] = "Copyright © 2026 Don Peterson"
    gist["lic"] = "MIT License (see /plib/_lic.mit)"
    gist["test"] = "notest"
    gist["cat"] = "data"
    gist["todo"] = '''
    '''
    return gist

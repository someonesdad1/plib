'''
Report the files that do/don't have gists
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import getopt
        import os
        import pathlib
        import re
        import sys
    if 1:   # Custom imports
        import columnize
        import dptypes
        import f
        import lwtest
        import trm
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Import symbols
        deque = collections.deque
        Path = pathlib.Path
        #
        Assert = lwtest.Assert
        Columnize = columnize.Columnize
        Constant = dptypes.Constant
        dedent = wrap.dedent
        flt = f.flt
    if 1:   # Global variables
        g = Constant()
        g.dbg = False
        g.gistname = "def GetGist():"
        t = trm.Trm()
        # These are filenames to ignore
        with g:
            g.ignore = set([
                Path("/gh/plib/repl.py"),
            ])
            g.found = []        # Files with proper gist
            g.not_found = []    # Files without proper gist
            g.ignored = []      # Files that were ignored
if 1:   # Utility
    def GetColors():
        t.err = t.red
        t.msg = t.orn
        t.dbg = t.skyl
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
            print(f"{t.n}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Check the gists in the indicated files or if a directory, all the python files
          in that directory.  
        Options:
          -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", "debug") 
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
            elif o == "--debug":
                with g.dbg:
                    g.dbg = True
        GetColors()
        if g.dbg:
            Dbg(f"Command line:  {sys.argv[0]} {t.brnl}{sys.argv[1:]}")
        return args
if 1:   # Core functionality
    def ProcessDir(pfile):
        for file in pfile.glob("*.py"):
            assert isinstance(file, Path)
            ProcessFile(file)
    def ProcessFile(pfile):
        'pfile is a Path'
        if pfile.is_dir():
            ProcessDir(p)
        else:
            if pfile.absolute() in g.ignore:
                g.ignored.append(str(pfile))
                return
            # Search for g.gistname in file
            with pfile.open() as f:
                text = f.read()
            if g.gistname not in text:
                #Warn(f"{t.err}No gist in file {str(pfile)!r}")
                g.not_found.append(str(pfile))
                return
            name = pfile.stem
            s = f"from {name} import GetGist"
            try:
                exec(s, globals())
            except Exception as e:
                #Warn(f"{t.err}Couldn't import GetGist() in file {str(pfile)!r}:")
                #Warn(f"  {t.err}{e}")
                g.not_found.append(str(pfile))
                return
            d = GetGist()
            g.found.append(str(pfile))
            # Check the important keys
            for key in "gist copy lic test".split():
                if not d[key].strip():
                    t.print(f"{t.msg}Missing key {key!r} in file {str(pfile)!r}")
    def Report():
        if g.ignored:
            print(f"{t.wht2}Ignored files:")
            o = []
            for i in sorted(set(g.ignored)):
                o.append(i)
            for i in Columnize(o, indent=" "*2):
                print(i)
            t.print(end="")
        if g.found:
            print(f"{t.wht}Files with gist:")
            o = []
            for i in sorted(set(g.found)):
                o.append(i)
            for i in Columnize(o, indent=" "*2):
                print(i)
            t.print(end="")
        if g.not_found:
            print(f"{t.ygr}Files without gist:")
            o = []
            for i in sorted(set(g.not_found)):
                o.append(i)
            for i in Columnize(o, indent=" "*2):
                print(i)
            t.print(end="")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    with g:
        g.gistdata = {}
    for file in files:
        p = Path(file)
        if not p.exists():
            t.print(f"{t.err}{file!r} doesn't exist")
            continue
        ProcessFile(p)
    Report()

def GetGist():
    g = {}
    g["gist"] = "Check the gists in python files"
    g["copy"] = "Copyright © 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "notest"
    g["cat"] = "utility"
    g["todo"] = ''' '''
    return g

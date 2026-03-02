'''

Script to find symbols in the /plib/dp*.py files
    
    In Feb 2026 I massively refactored /plib to try to reduce the number of
    files/modules.  This refactoring will break nearly every module & script, so the
    intent is to be able to locate the module that contains the symbol.
        
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import getopt
        import importlib
        import os
        import pathlib
        import pprint
        import re
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
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        namedtuple = collections.namedtuple
        pp = pprint.pprint
        #
        Columnize = columnize.Columnize
        Constant = dptypes.Constant
        dedent = wrap.dedent
        flt = f.flt
        t = trm.Trm()
    if 1:   # Global variables
        g = Constant()
        with g:
            g.dbg = False
            # Tuple of the files that are searched for symbols
            g.files = tuple()
            # Dictionary relating symbols to g.files number
            g.symbols = defaultdict(list)
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
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.n}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Warning(*msg, **kw):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warning(f"{t.err}", end="")
        Warning(*msg)
        Warning(f"{t.n}")
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [sym [...]]
          Locate the dp*.py file that contains the indicated symbol(s).
        Options:
            -h      Print help
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Description
        d["-d"] = 3      # Description
        if len(sys.argv) == 1:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
if 1:   # Core functionality
    class MyDummy:
        pass
    def GetFiles():
        "Put a tuple of the files with the symbols we're interested in into g.files"
        p = Path("/plib")
        files = list(p.glob("dp*.py"))
        #files.remove(Path("/plib/dp.py"))
        files.remove(Path("/plib/dpbp.py"))
        with g:
            g.files = tuple(files)
    def GetSymbols():
        '''Find all the public symbols in g.files and put them into the dictionary
        g.symbols.
        '''
        global dummy
        for file in g.files:
            name = file.stem
            if name != "dp":
                continue
            t.print(f"{t.orn}{str(file)}")
            try:
                dummy = importlib.import_module(name)
                for i in dummy.__dict__:
                    if i.startswith("_"): # or i == "t":
                        continue
                    var = eval(f"dummy.{i}")
                    print(f"{var!r}")
            except Exception as e:
                print(f"{t.err}Couldn't process {str(file)!r}: {e}")

if __name__ == "__main__":  
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    GetFiles()      # Files in tuple g.files
    GetSymbols()    # Symbols in dict g.symbols
    if args:
        for arg in args:
            pass    # Do stuff

def GetGist():
    gist = {}
    gist["gist"] = "Script to find symbols in the /plib/dp*.py files"
    gist["copy"] = "Copyright © 2026 Don Peterson"
    gist["lic"] = "MIT License (see /plib/_lic.mit)"
    gist["test"] = "notest"
    gist["cat"] = "utility"
    gist["todo"] = '''
    '''
    return gist

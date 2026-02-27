'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Check the gists in python files oo>
        <oo desc ∞ Description oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 

                - Todo items

        oo>
    '''
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        import trm
        from constant import Constant
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        g = Constant()
        g.dbg = False
        g.gistname = "def GetGist():"
        t = trm.Trm()
        # These are filenames in /plib to ignore
        with g:
            g.ignore = set([
                Path("/gh/plib/repl.py"),
            ])
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
          Check the gists in the indicates files or if a directory, all the python files
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
                return
            # Search for g.gistname in file
            text = pfile.open().read()
            if g.gistname not in text:
                Warn(f"{t.err}No gist in file {str(pfile)!r}")
                return
            name = pfile.stem
            s = f"from {name} import GetGist"
            try:
                exec(s, globals())
            except Exception:
                Warn(f"{t.err}Couldn't import GetGist() in file {str(pfile)!r}")
                return
            d = GetGist()
            # Check the important keys
            for key in "gist copy lic test".split():
                if not d[key].strip():
                    t.print(f"{t.msg}Missing key {key!r} in file {str(pfile)!r}")

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

def GetGist():
    g = {}
    g["gist"] = "Check the gists in python files"
    g["copy"] = "Copyright © 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "notest"
    g["cat"] = "utility"
    g["todo"] = ''' '''
    return g

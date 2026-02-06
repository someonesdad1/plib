'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Print prioritized todo items oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ Todo items
        
            - Decide on overall goals
        
        oo>
    '''
    if 1:   # Standard imports
        from collections import namedtuple
        from pathlib import Path
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.dbg = True
        ii = isinstance
        g.nt = nametuple("NT", "linenum filename line")
if 1:   # Utility
    def GetColors():
        t.err = t.redl
        t.dbg = t.sky if g.dbg else ""
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
        Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
          Print out a prioritized list of todo items in the python files.  If no files
          are given on the command line, the current directory is searched.  If a file
          is a directory, all python files are examined in that directory.
        Options:
          -s s    Define the todo string marker [{d["-s"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = ""        # Suffix to search for
        d["-s"] = "∞∞"      # Marker for todo items
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "n:s:h") 
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-n":
                d[o] = a
            elif o == "-s":
                d[o] = a
                if not a:
                    Error(f"{o} option's value cannot be empty")
            elif o == "-h":
                Usage()
        GetColors()
        if g.dbg:
            t.print(f"Command line: {sys.argv[0]} {t.brnl}{sys.argv[1:]}")
        return args
if 1:   # Core functionality
    def ProcessDirectory(dir):
        return [] #∞∞ 
    def ProcessFile(file):
        '''Process the indicated file or director and return a list of zero or more 
        lines from the file that match the marker string.  The list elements are 
        the namedtuple NT(linenum, filename, line).
        '''
        p = Path(file)
        if p.is_dir():
            return ProcessDirectory(file)
        else:
            assert p.is_file()
            if not p.exists():
                t.print(f"{t.err}{file!r} doesn't exist", file=sys.stderr)
                return []
            # File exists, so read it in
            with p.open() as fp:
                lines = fp.read().split("\n")
                fp.close()
    def GetFileList(*files):
        filelist = []
        for file in files:
            filelist += ProcessFile(file)
        pp(filelist)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    filelist = GetFilelist(*files)

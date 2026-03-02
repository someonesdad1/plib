'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Reverse text lines by characters oo>
        <oo desc ∞ Like /usr/bin/rev but handles UTF-8 text oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ 
            MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ --test oo>
        <oo todo ∞ Todo items oo>
    '''
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        import trm
        t = trm.Trm()
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
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
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
        Usage:  {sys.argv[0]} [options] [files]
          Reverse the strings on each line of a text file.  Use '-' for a file name to
          read from stdin.
        Options:
          -s      Strip whitespace out of each line before reversing
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-s"] = False     # Strip whitespace from each line
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("s"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def ProcessFile(file):
        if file == "-":
            s = sys.stdin.read()
        else:
            with open(file) as fp:
                s = fp.read()
                fp.close()
        lines = s.split("\n")
        o = []
        for line in lines:
            if d["-s"]:
                line = ''.join(line.split())    # Remove any whitespace
            o.append(''.join(reversed(line)))
        return '\n'.join(o)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        print(ProcessFile(arg), end="")

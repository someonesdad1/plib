if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Filter shell 'set' command to show functions oo>
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
        import get
        from columnize import Columnize
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
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.notmine = t.purl
        t.mine = t.sky
        t.has_dot = t.grn
        t.has_ul = t.royl
        t.conda = t.lip
        t.starship = t.lipl
        t.unclassified = t.ornl

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
        Usage:  {sys.argv[0]}
          In a bash shell, type 'set' and pipe its output to this script and it will
          print out the names of the defined shell functions.  
        Options:
          -h    Print a manpage
          -s    Only show special function names (start with . or underscore or 
                are likely not functions I've written)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-s"] = False     # Show special function names only
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs") 
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            exit(1)
        for o, a in opts:
            if o[1] in list("s"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def GetMyFunctionNames():
        '''Set GetMyFunctionNames.names to the set of function names defined in my ~.0rc
        files of dot_bin and dot_func.
        '''
        lines = []
        for file in ("/home/don/.0rc/dot_bin", "/home/don/.0rc/dot_func"):
            lines += get.GetLines(file, script=True, ignore_empty=True, strip=True, nonl=True)
        lines = list(filter(lambda x: x.startswith("function "), lines))
        keep = []
        for line in lines:
            f = line.split("##")
            if len(f) != 2:
                continue
            name = f[0]
            keep.append(name.split()[1])
        GetMyFunctionNames.names = set(keep)
    def ShowColorCode():
        print(
            f"{t.yell}Color coding:  {t.mine}Mine {t.notmine}Not mine "
            f"{t.has_dot}Dotted {t.has_ul}Leading _ "
            f"{t.conda}Conda {t.starship}Starship {t.unclassified}Stale func name"
        )
    def Unusual(name):
        if name.startswith(".") or name.startswith("_"):
            return True
    def Mine(name):
        "Return true if it's one of my files in dot_bin or dot_func"
        return name in GetMyFunctionNames.names
    def Conda(name):
        return True if "conda" in name.lower() else False
    def Starship(name):
        return True if "starship" in name.lower() else False
    def NotMine(name):
        'Return True if this function name is probably not one of mine'
        return True if name.startswith("__") else False
    def Classify(name):
        "Return the color code of the file's name"
        if name.startswith("."):
            return t.has_dot
        elif Mine(name):
            return t.mine
        elif Conda(name):
            return t.conda
        elif Starship(name):
            return t.starship
        elif name.startswith("_") and len(name) > 1 and name[1] != "_":
            return t.has_ul
        elif NotMine(name):
            return t.notmine
        else:
            return t.unclassified
    def Process(lines):
        # Get shell function names from output of bash 'set' command
        assert isinstance(lines, list)
        o = []
        r = re.compile(r"^\S+ \(\)")
        while lines:
            item = lines.pop(0)
            if r.search(item):
                o.append(item.replace("()", "").strip())
        # Filter these names as needed
        if d["-s"]:
            # Only keep special names
            o = filter(NotMine, o)
            for i in Columnize(o):
                print(i)
        else:
            # Decorate special ones in color
            for i, name in enumerate(o):
                o[i] = f"{Classify(name)}{name}{t.n}"
            for i in Columnize(o):
                print(i)
        ShowColorCode()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    GetMyFunctionNames()
    # Get input
    if 1:
        lines = sys.stdin.read().split("\n")
    else:
        lines = open("a").read().split("\n")
    Process(lines)

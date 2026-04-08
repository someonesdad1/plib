if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Utility to examine my shell & python functions oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2025 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:   # Standard imports
        from collections import deque, defaultdict
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from columnize import Columnize
        from wrap import dedent
        from dpstr import RegexpDecorate
        import trm
        t = trm.TrmDP()
        from dputil import PP
        import get
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.files = (
            P("/home/don/.0rc/dot_func"),
            P("/home/don/.0rc/dot_bin"),
        )
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.cat = t.lil
        t.name = t.yel
        t.warn = t.ornl
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
    def Warn(*msg):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [cmd] [args]
          Search my shell functions and python files for functions/classes.  Commands are:
            b   Show my bin executables
            c   Show category names
            l   List (args are optional categories to list)
            p   Python (args are files to search)
            s   Search for regex
        Options:
            -a      Include python function arguments
            -i      Make searches case sensitive
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = True     # Include python function arguments
        d["-i"] = True     # Case insensitive searches
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "aih") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ai"):
                d[o] = not d[o]
        GetColors()
        return args
if 1:   # Core functionality
    class Func:
        w = 0   # Will be maximum name width
        def __init__(self, line):
            self.line = line
            self.lines = []
            # Split the first line to get the desired fields
            f = line.split()
            assert f[0] == "function"
            self.name = f[1]
            Func.w = max(Func.w, len(self.name))
            assert f[2] == "##"
            assert f[3].startswith("<") and f[3].endswith(">")
            self.category = f[3].replace("<", "").replace(">", "")
            self.descr = ' '.join(f[4:])
        def __str__(self):
            return f"Func({self.name}, <{self.category}>, {self.descr!r}"
        def __repr__(self):
            return str(self)
        def __lt__(self, other):
            return self.name < other.name
    def CheckForDuplicates(funcs):
        funcset = set()
        found = False
        for name, _ in funcs:
            if name in funcset:
                print(f"{t.err}{name!r}{t.n} is a function name duplicate")
                found = True
            funcset.add(name)
        if found:
            exit(1)
    def GetFuncs():
        'Return list of (funcname, func_instance)'
        for file in g.files:
            lines = get.GetLines(file, script=True, ignore_empty=True, nonl=True)
        dq, o = deque(lines), []
        while dq:
            line = dq.popleft()
            if line.startswith("function"):
                func = Func(line)
                line = dq.popleft()
                assert line == "{"
                func.lines.append(line)
                while line != "}":
                    line = dq.popleft()
                    func.lines.append(line)
                assert line == "}"
                func.lines.append(line)
                o.append((func.name, func))
        CheckForDuplicates(o)
        # Also make a dict of function categories
        di = defaultdict(list)
        for name, func in o:
            di[func.category].append(func)
        return o, di
    def List(categories):
        'Print the categories and their functions'
        if categories:
            categories_to_use = categories
        else:
            categories_to_use = sorted(funcdict.keys())
        for cat in categories_to_use:
            if cat not in funcdict:
                t.print(f"{t.warn}{cat!r} not a recognized category")
                continue
            t.print(f"{t.cat}{cat}")
            for i in sorted(funcdict[cat]):
                print(f"  {i.name:{Func.w}s} {i.descr}")
    def ShowCategoryNames(category):
        'List the functions and their descriptions in this category'
        if not category:
            # Just print category names
            t.print(f"{t.cat}Category names:")
            for i in sorted(funcdict):
                print(f"  {i}")
            return
        if category not in funcdict:
            print(f"{category!r} invalid category name")
            return
        t.print(f"{t.cat}{category}")
        # Get maximum name width for this category
        w = 0
        for item in funcdict[category]:
            w = max(w, len(item.name))
        for item in sorted(funcdict[category]):
            print(f"  {t.name}{item.name:{w}s}{t.n} {item.descr}")
    def BinExecutables():
        o = []
        for file in P("/home/don/.0rc/bin").glob("*"):
            # Get first 20 bytes of file
            try:
                f = file.open("rb").read(20)
            except Exception:
                continue
            if f[:2] != b"#!":
                continue
            if file.name.endswith(".py"):
                continue
            if file.name in ("z",):
                continue
            o.append(file)
        # Report:  print the first line's info
        t.print(f"{t.cat}Scripts in ~/.0rc/bin:")
        w = 0
        for i in o:
            w = max(w, len(i.name))
        for i in sorted(o):
            line = i.open().read().split("\n")[1]
            descr = line[1:].strip()
            print(f"  {i.name:{w}s} {descr}")
    def SearchForRegexes(args):
        for arg in args:
            SearchForRegex(arg)
    def SearchForRegex(regex):
        r = re.compile(regex, re.I if d["-i"] else 0)
        # Find the names or descriptions that match the regex
        found = []
        for name, func in funcs:
            mo1 = r.search(name)
            mo2 = r.search(func.descr)
            if mo1 or mo2:
                found.append(func)
        # Report if we found anything
        if found:
            rd = RegexpDecorate()
            rd.register(r, t.yel, t.n)
            t.print(f"regex = {t.cat}{regex}")
            for i in found:
                s = f"  {i.name:{Func.w}s} {i.descr}"
                rd(s, insert_nl=True)
    def SearchForPythonStuff(files):
        'Find classes and functions in python files'
        t.fu, t.cl, t.na = t.sky, t.yell, t.ornl
        # Regex to recognize python functions
        rfunc = r"def +\w+ *\((.*)\) *:"
        rclass = r"class +(\w+) *(\(.*\))? *:"
        # Process files
        for file in files:
            with open(file) as f:
                s = f.read().strip()
            functions = []
            for i in re.finditer(rfunc, s, flags=re.MULTILINE):
                start, end = i.start(), i.end()
                name = s[i.start():i.end()].strip()
                if name[-1] == ":":
                    name = name[:-1]
                if name.startswith("def "):
                    name = name[4:].strip()
                if d["-a"]:
                    name = name.replace("(" + i.groups()[0] + ")", "")
                    name = name.replace("()", "")
                functions.append(f"{name}")
            classes = []
            for i in re.finditer(rclass, s, flags=re.MULTILINE):
                start, end = i.start(), i.end()
                name = s[i.start():i.end()].strip()
                if name[-1] == ":":
                    name = name[:-1]
                if name.startswith("class "):
                    name = name[6:].strip()
                classes.append(f"{name}")
            # Report
            if functions or classes:
                nf, nc = len(functions), len(classes)
                t.print(f"{t.na}{file}:    {t.fu}{nf} Functions {t.cl}{nc} Classes")
                functions = [f"{i}" for i in sorted(set(functions), key=str.lower)]
                classes = [f"{i}" for i in sorted(set(classes), key=str.lower)]
                for i in Columnize(functions, indent=" "*2, horiz=True):
                    t.print(f"{t.fu}{i}")
                for i in Columnize(classes, indent=" "*2, horiz=True, sep=" "*4):
                    t.print(f"{t.cl}{i}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    funcs, funcdict = GetFuncs()
    op = args[0]
    args = args[1:]
    if op == "b":
        BinExecutables()
    elif op == "c":
        items = args if args else [""]
        for category in items:
            ShowCategoryNames(category)
    elif op == "l":
        List(args)
    elif op == "p":
        SearchForPythonStuff(args)
    elif op == "s":
        SearchForRegexes(args)
    else:
        Error(f"{op!r} not recognized")

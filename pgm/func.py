_pgminfo = '''
<oo 
    Utility to examine my shell functions
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
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
        from color import t, RegexpDecorate
        from dpprint import PP
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
        Usage:  {sys.argv[0]} [options] [op] [args]
          Search my shell functions:
            b   Show my bin executables
            c   Show category names
            l   List (args are optional categories to list)
            s   Search for regex
        Options:
            -h      Print a manpage
            -i      Make searches case sensitive
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = True     # Case insensitive searches
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ih") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
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
        di = defaultdict(list)
        for name, func in funcs:
            di[func.category].append(name)
        for cat in sorted(di):
            if categories and cat not in categories:
                continue
            t.print(f"{t.cat}{cat}")
            for i in Columnize(sorted(di[cat]), indent=" "*4):
                print(i)
    def ShowCategoryNames(category):
        'List the functions and their descriptions in this category'
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

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    funcs, funcdict = GetFuncs()
    op = args[0]
    args = args[1:]
    if op == "b":
        BinExecutables()
    elif op == "c":
        items = args if args else sorted(funcdict.keys())
        for category in items:
            ShowCategoryNames(category)
    elif op == "l":
        List(args)
    elif op == "s":
        SearchForRegexes(args)
    else:
        Error(f"{op!r} not recognized")

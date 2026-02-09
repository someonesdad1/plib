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
        from collections import namedtuple, defaultdict
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
        from constant import Constant
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        g = Constant()
        g.dbg = False
        ii = isinstance
        g.NT = namedtuple("NT", "ln file s")
if 1:   # Utility
    def GetColors():
        t.file = t.orn
        t.ln = t.royl
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
        Usage:  {sys.argv[0]} [options] cmd [file1 [file2 ...]]
          Find todo items in python files.  If file argument is a directory, all python
          files in that directory are searched.  cmd can be "1", "2", or "3" for
          priority level or "0" means show everything found in the current directory.
          If no files are given, the current directory is searched.  If cmd is a file,
          then it's as if "0" was given as cmd.
        Options:
          -s s    Define the todo string marker [{d["-s"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = ""        # Suffix to search for
        d["-s"] = "∞∞"      # Marker for todo items
        d["-d"] = False     # Debugging
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dn:s:h") 
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o == "-n":
                d[o] = a
            elif o == "-s":
                d[o] = a
                if not a:
                    Error(f"{o} option's value cannot be empty")
            elif o == "-h":
                Usage()
        if d["-d"]:
            with g:
                g.dbg = True
        GetColors()
        if g.dbg:
            Dbg(f"Command line: {sys.argv[0]} {t.brnl}{sys.argv[1:]}")
        return args
if 1:   # Core functionality
    def ProcessDirectory(dir):
        'dir is a Path.  Return a list of elements NT(linenum, filename, line).'
        items = []
        for i in dir.glob("*.py"):
            items += ProcessFile(i)
        return items
    def ProcessFile(file):
        '''Process the indicated file or directory and return a list of zero or more 
        lines from the file that match the marker string.  The list elements are 
        the namedtuple NT(linenum, filename, line).
        '''
        p = Path(file)
        items = []
        if p.is_dir():
            for i in p.glob("*.py"):
                items += ProcessFile(i)
            return items
        assert p.is_file()
        if not p.exists():
            t.print(f"{t.err}{file!r} doesn't exist", file=sys.stderr)
        else:
            with p.open() as fp:
                lines = fp.read().split("\n")
                fp.close()
            for linenum, line in enumerate(lines):
                if d["-s"] in line:
                    items.append(g.NT(linenum + 1, file, line.strip()))
        return items
    def GetFileList(*files):
        filelist = []
        for file in files:
            filelist += ProcessFile(file)
        if 0:
            pp(filelist)
        return filelist
    def MakeDictionary(filelist):
        '''Classify the entries (namedtuple(linenum, file, line_string)) into three
        categories:  the priorities 1, 2, 3 and 0, meaning "other".
        '''
        di = defaultdict(list)
        for i in filelist:
            ln, file, line = i
            # Use ∞∞i to ignore the trigger lines, like in this file
            if "∞∞1" in line and "∞∞i" not in line:       # ∞∞i
                di[1].append(i)
            elif "∞∞2" in line and "∞∞i" not in line:     # ∞∞i
                di[2].append(i)
            elif "∞∞3" in line and "∞∞i" not in line:     # ∞∞i
                di[3].append(i)
            if "∞∞i" not in line:
                di[0].append(i)
        return di
    def Report(items):
        '''items is the list of g.NT items to print, such as:
        NT(ln=1557, file=PosixPath('f.py'), s='return  # These classes broke somehow ∞∞1') ∞∞i
        Organize and print by sorted file name:
            {
                file: [
                    (linenum, string),
                    ...
                ],
            }
        '''
        di = defaultdict(list)
        for i in items:
            ln, file, s = i
            di[str(file)].append((ln, s))
        for file in sorted(di):
            t.print(f"{t.file}{file}")
            for ln, s in sorted(di[file]):
                print(f"{t.ln}{ln:5d}{t.n} {s}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    p = Path(args[0])
    if p.is_file():
        # If first argument is a file, then assume all arguments are files to be looked at
        filelist = GetFileList(*args)
        cmd = "0"
    else:
        cmd = args.pop(0)
        if cmd not in "0 1 2 3".split():
            Usage()
        if not args:    # Do current directory by default
            args.append(".")
        filelist = GetFileList(*args)
    di = MakeDictionary(filelist)
    Report(di[int(cmd)])

_pgminfo = '''
<oo desc
    Print md5 hashes for files on command line.
oo>
<oo cr Copyright © 2014, 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - List of todo items here

oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        from pathlib import Path
        import getopt
        import os
        import hashlib
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        import trm
        t = trm.Trm()
        import termtables as tt
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
        t.warn = t.ornl
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
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Prints the MD5 hash for each file on the command line.  The file's 
          size in bytes is shown after the name.  The default output is (hash
          name, size).  Use -r to show (file, size, hash).
        Options:
          -c      Don't print the output in columns
          -r      Show MD5 hash last in output
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Don't print in columns
        d["-r"] = False     # Show MD5 hash first in output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chr") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cr"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def ProcessFile(file):
        'Return the filename, size, and MD5 hash'
        p = Path(file)
        if p.is_symlink():
            Warn(f"{t.warn}{file!r} is a symbolic link{t.n}")
            return None
        elif p.is_dir():
            Warn(f"{t.warn}{file!r} is a directory{t.n}")
            return None
        elif not p.exists():
            Warn(f"{t.warn}{file!r} doesn't exist{t.n}")
            return None
        m, s = hashlib.md5(), []
        try:
            m.update(open(file, "rb").read())
        except Exception:
            Warn(f"Could not read {file!r}")
            return None
        size = os.stat(file)[6]
        if d["-r"]:
            return [m.hexdigest(), file, str(size)]
        else:
            return [file, str(size), m.hexdigest()]
    def ReportColumns(results):
        'Print so that columns are aligned'
        w = []
        for i in range(3):
            w.append(max(len(j[i]) for j in results))
        s = [["MD5 Hash", "File", "Bytes"]] if d["-r"] else [["File", "Bytes", "MD5 Hash"]]
        s.append(["-"*w[0], "-"*w[1], "-"*w[2]])
        s.extend(results)
        tt.print(s, header=None, padding=(0, 0), style=" "*15, alignment="lll")
    def Report(results):
        'Print in compact form'
        for i in results:
            print(' '.join(i))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    results = []
    for file in args:
        result = ProcessFile(file)
        if result is not None:
            results.append(result)
    if d["-c"]:
        Report(results)
    else:
        ReportColumns(results)

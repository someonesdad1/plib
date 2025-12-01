_pgminfo = '''
<oo desc
    Choose one or more files and send them to stdout.  This is similar to my goto.py
    script, but is intended to be used to e.g. open a set of files in vi.
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat util oo>
<oo test none oo>
<oo todo

Config file is more standardized than goto.py.  Field separator is ';' and the fields are

    - Absolute path to file
    - Short name for display
    - Alias
    - Display format:  fg:bg:attr

All four fields must be present, but they can be empty (i.e., each line requires three
field separator characters).  Space characters are stripped off the fields.

oo>
'''
 
if 1:  # Header
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
        ii = isinstance
        Config = namedtuple("Config", "path, name, alias, format")
        # Config file lines whose path doesn't exist:  key is config file name, value is
        # tuple of line numbers with bad paths
        g.nonexistent_paths = {}
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
        Usage:  {sys.argv[0]} [options] re1 [re2...]
          Select a list of choices from a file by use of the regexps, which are ANDed
          together.  You're then prompted for the resulting items by their number or an
          alias if one was supplied in the configuration file.
        Options:
            -C      Check configuration files for paths that don't exist
            -c      Print an explanatory configuration file
            -d      Turn debugging on
            -f file Configuration file
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-C"] = False     # Check config files
        d["-c"] = False     # Print explanatory configuration file
        d["-d"] = False     # Turn debugging on
        d["-f"] = []        # Configuration file (can have more than one)
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "Ccdf:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Ccd"):
                d[o] = not d[o]
            elif o == "-f":
                p = Path(a)
                if not p.exists():
                    Error(f"Configuration file {a!r} doesn't exist")
                d[o].append(p)
            elif o == "-h":
                Usage()
        if d["-d"]:
            g.dbg = True
        GetColors()
        if d["-d"]:
            Dbg("Debugging turned on")
            Dbg("  Options dictionary:")
            for key in d:
                Dbg(f"    {t.sky}{key}: {d[key]}")
            if args:
                Dbg("  Command line arguments:")
                for arg in args:
                    Dbg(f"    {t.sky}{arg}")
        if not d["-f"]:
            Error("You must supply at least one configuration file")
        else:
            # Only process each configuration file once
            out = []
            for file in d["-f"]:
                if file not in out:
                    out.append(file)
            d["-f"] = out
        return args
if 1:   # Classes
    class Line:
        def __init__(self, file, linenum, fields):
            self.file = file
            self.linenum = linenum
            self.fields = fields
            # Our attributes
            self.path = Path(fields[0])
            self.name = fields[1]
            self.alias = fields[2]
            self.format = fields[3]
        def __str__(self):
            return f"{self.file}:{self.linenum} {self.fields}"
        def __repr__(self):
            return f"{self.file}:{self.linenum} {self.fields}"
        def IsOK(self):
            'Return True if this object is OK, False if not'
            if not self.CanBeRead():
                return False
            if not self.FormatOK():
                return False
            return True
        def FormatOK(self):
            'Return True if format OK, False if not'
            # Check format:  it must be 1 to 3 strings separated by ':'.  These strings
            # must be color abbreviations recognized by the t() instance of Trm.
            f = self.format.split(":")
            if len(f) not in (1, 2, 3):
                return False
            if f == [""]:
                return True
            try:
                t(*f)
                return True
            except Exception:
                return False
        def CanBeRead(self):
            try:
                b = open(self.path).read(1)
                return True
            except Exception:
                return False
        def ExplainProblem(self):
            if self.IsOK():
                return
            if not self.CanBeRead():
                s = str(self.path)
                print(f"  [{self.file}:{self.linenum}] {s!r} can't be read")
                return
            if not self.FormatOK():
                print(f"  [{self.file}:{self.linenum}] {self.format!r} is a bad formatting string")
                return
            raise Exception("Bug because self.IsOK() was False")
if 1:   # Core functionality
    def CheckConfigFiles(files):
        '''Read all the lines of the config files and examine each line.  If a line
        starts with a '#', remove it and process it.  If it still starts with a '#',
        ignore it.  Otherwise, try to parse it as a config file line and if there's a
        path in the first field, check that it exists.
        
        Return 0 if OK, 1 if not.
        '''
        not_ok = False
        for file in files:
            bad = []
            Dbg(f"Reading file {file!r}")
            lines = open(file).read().split("\n")
            for i, line in enumerate(lines):
                line = line.strip()
                if not line or line == "#":
                    continue
                if line.startswith("#"):
                    line = line[1:].strip()
                    if line.startswith("#"):
                        continue
                # This is a valid line to check
                Dbg(f"  Checking {t.pnkl}{line!r}")
                fields = [i.strip(" ") for i in line.strip().split(";")]
                ln = Line(file, i + 1, fields)
                if not ln.IsOK():
                    bad.append(ln)
                    continue
            if bad:
                not_ok = True
                s = "path, name, alias, format"
                t.print(f"{t.ornl}File {str(file.absolute())!r}:  {t.redl}bad lines")
                for ln in bad:
                    ln.ExplainProblem()
        return int(not_ok)
    def ReadConfigFile(file):
        'Return a list of the valid lines'
        lines = open(file).read().split("\n")
        out = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = [i.strip(" ") for i in line.strip().split(";")]
            ln = Line(file, i + 1, fields)
            out.append(ln)
        return out
    def ProcessLines(lines, regexps):
        '''For each line in lines, display them to the user and prompt for the ones to
        use.  Filter by the passed-in regular expressions (they are ANDed together).
        '''

if __name__ == "__main__":
    d = {}      # Options dictionary
    regexps = ParseCommandLine(d)
    if d["-C"]:
        exit(CheckConfigFiles(d["-f"]))
    else:
        lines = []
        for file in d["-f"]:
            lines.extend(ReadConfigFile(file))
        choices = ProcessLines(lines)

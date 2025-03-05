'''
Construct the github markdown documentation files in /plib/doc
'''
 
if 1:  # Header
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
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()
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
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
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
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if 0 and len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
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
        GetColors()
        return args
if 1:   # Classes
    class Info:
        '''Capture the information in the _pgminfo variable.  Instance attributes are:
        desc        Description of module
        cr          Legal statement of copyright with date
        cat         Category keyword to help with documentation
        test        How to run the module's self tests
        todo        Things that need to be done for the module
        '''
        def __init__(self, file, string):
            self.file = file
            self.string = string
            # Parse the string with regexes.
            # Description
            mo = re.search(r"<oo +desc +(.*?)oo>", string, re.S)
            self.desc = mo.groups()[0].strip() if mo else ""
            # Copyright
            mo = re.search(r"<oo +Copyright +(.*?)oo>", string, re.S)
            self.cr = "Copyright " + mo.groups()[0].strip() if mo else ""
            # Category
            mo = re.search(r"<oo +category +(.*?)oo>", string, re.S)
            self.cat = mo.groups()[0].strip() if mo else ""
            # Test
            mo = re.search(r"<oo +test +(.*?)oo>", string, re.S)
            self.test = mo.groups()[0].strip() if mo else ""
            # ToDo
            mo = re.search(r"<oo +todo +(.*?)oo>", string, re.S)
            self.todo = mo.groups()[0].strip() if mo else ""
        def __str__(self):
            ind = " "*2
            s = f"Info({file}\n"
            s += f"{ind}desc:  {self.desc}\n" if self.desc else ""
            s += f"{ind}cr  :  {self.cr}\n" if self.cr else ""
            s += f"{ind}cat :  {self.cat}\n" if self.cat else ""
            s += f"{ind}test:  {self.test}\n" if self.test else ""
            s += f"{ind}todo:  {self.todo}\n" if self.todo else ""
            s += ")"
            return s

if 1:   # Core functionality
    def GetFiles():
        'Return a list of the *.py files in /plib'
        files = []
        for p in P("/plib").glob("*.py"):
            files.append(p)
        return list(sorted(files))
    def GetFileData(file):
        '''File's docstring comes first.  The _pgminfo variable needs to be found, as it
        contains the string with our data.
        '''
        Assert(file.exists())
        dq = deque(file.open().read().split("\n"))
        pgminfo, found = [], False
        while dq:
            line = dq.popleft()
            ln = line.strip()
            if ln.startswith("_pgminfo"):
                found = True
                break
        if not found:
            return pgminfo
        # We are in the _pgminfo variable's text
        while dq:
            line = dq.popleft()
            ln = line.strip()
            if ln.startswith("'''") or ln.startswith('"""'):    
                break
            else:
                pgminfo.append(line)
        return pgminfo

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    files = GetFiles()
    filedict = {}
    for file in files:
        file = P("/plib/doc/a.py")
        data_list = GetFileData(file)
        info = Info(file, '\n'.join(data_list))
        filedict[file] = info
        break
    for i in filedict:
        print(filedict[file])

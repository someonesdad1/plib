_pgminfo = '''
<oo desc
    Given a directory of files X, make N zip files that constitute all of these files.
    The use case is to send someone a bunch of files that's too large to email and you
    don't want to e.g. send a flash drive or DVDs through the mail system.  If you use
    Google Drive, you can drop the zip files into a new directory and others can get
    access to those files if you send them an email message (use the Share feature in
    Google Drive).
oo>
<oo cr Copyright © 2025 Don Peterson oo>
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
        from collections import deque, defaultdict
        from pathlib import Path
        import getopt
        import math
        import os
        import re
        import sys
        import zipfile
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
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
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
        Usage:  {sys.argv[0]} [options] N dir 
          Build N zip files containing the files in directory dir.  When you include the
          prefix with -p, the zip files are actually constructed; otherwise, you get a
          report on the results.  Using -R also constructs the zip files.
        Options
          -d        Turn on debugging output
          -i regex  Only include files that match the regex; more than one -i allowed
          -R file   Use edited output from -r to construct the zip files
          -r        Report to stdout giving each zip file's name along with the files
                    and their sizes in bytes.
          -p prefix Use prefix to name the files (use "" for no prefix)
          -x regex  Ignore files that match the regex; more than one -x allowed
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Turn on debugging
        d["-i"] = []        # Regexes of files to include
        d["-p"] = ""        # Prefix to name the files with
        d["-R"] = None      # Construct zip files from this file
        d["-r"] = False     # Produce report file to stdout
        d["-x"] = []        # Regexes of files to ignore
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "di:p:hR:rx:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dr"):
                d[o] = not d[o]
            elif o in ("-i", "-x"):
                d[o].append(a)
            elif o == "-p":
                d[o] = a
            elif o == "-h":
                Usage()
        if d["-d"]:
            g.dbg = True
        GetColors()
        Dbg("Debugging on")
        Dbg(f"Command line: {sys.argv}")
        return args
if 1:   # Core functionality
    def GetFilelistDeque():
        '''Assumes we're in a directory where the files to be packaged are in the
        directory ./cache
        '''
        cwd = Path(".").cwd()
        os.chdir("cache")
        p, dq, total_size = Path("."), deque(), 0
        for i, pth in enumerate(p.glob("*")):
            size = pth.stat().st_size
            total_size += size
            dq.append((pth, size))
        os.chdir(cwd)
        return total_size, dq
    def ConstructFileDict(N):
        '''Return a dict indexed by file number containing a list of (file, size)
        entries that indicate what will be zipped into each zip file.
        '''
        total_size, dq = GetFilelistDeque()  # deque containing each file and its size
        target_size = math.ceil(total_size/N)
        filedict = defaultdict(list)
        for filenum in range(N):
            this_file_size = 0
            while dq and this_file_size < target_size:
                file, size = dq.popleft()
                this_file_size += size
                filedict[filenum].append((file, size))
        # Print the file list summary
        print("Summary of size of each zip file:")
        x = flt(0)
        x.N = 2
        x.rtz = False
        report = []
        for key in filedict:
            total_size = flt(0)
            report.append(f"{key}")
            for file, size in filedict[key]:
                total_size += size
                report.append(f"  {str(file)!r} {size}")
            print(f"  {key}:  {total_size.engsi}B")
        if d["-r"]:     # Report these files to stdout
            for i in report:
                print(i)
        return filedict
    def ConstructZipFiles(filedict):
        for key in filedict:
            with zipfile.ZipFile(f"{prefix}{key}.zip", "w") as zf:
                for file, size in filedict[key]:
                    zf.write(f"cache/{file}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    prefix = None
    N = abs(int(args[0]))
    Assert(N > 0)
    if len(args) == 2:
        prefix = args[1].strip()
    filedict = ConstructFileDict(N)
    if prefix:
        ConstructZipFiles(filedict)

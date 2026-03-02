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
            print(f"{t.dbg}+ ", end="")
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
          Build N zip files containing the files in directory dir.  If you attach an 'M'
          or 'G' to N with no space, then it means to construct each zip file with about
          N MB or N GB in it (the number N can be a float).  When you include the prefix
          with -p, the zip files are actually constructed; otherwise, you get a summary
          report on the names of the zipfiles (numbered by integers) and their
          uncompressed sizes.  Using -R also constructs the zip files.
        Examples
          '{sys.argv[0]} 2 dir'
            The report will show the uncompressed size of the two zipfiles this command
            will make.  If you include the -r option, you'll see the name of each file
            and its uncompressed size in bytes.
          '{sys.argv[0]} -i "^.*.py$" 1 dir'
            Construct 1 zip file containing the python files in directory dir.
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
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "di:p:hR:rx:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dr"):
                d[o] = not d[o]
            elif o in ("-i", "-x"):
                try:
                    d[o].append(re.compile(a))
                except Exception:
                    Error(f"{a!r} is a bad regex")
            elif o == "-p":
                d[o] = a
            elif o == "-h":
                Usage()
        if d["-d"]:
            g.dbg = True
        GetColors()
        Dbg(f"Debugging on; command line: {sys.argv}")
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def GetFileList(directory):
        'Return a list of (file_size, file_name) elements sorted largest first'
        filelist = []
        for file in directory.glob("**/*"):
            filelist.append((file.stat().st_size, file))
        filelist = list(sorted(filelist, reverse=True))
        if g.dbg:
            Dbg("Sorted contents of filelist in GetFileList()")
            for i in filelist:
                Dbg(" ", i)
        return filelist
    def ConstructZipFiles(filedict):
        for key in filedict:
            with zipfile.ZipFile(f"{prefix}{key}.zip", "w") as zf:
                for file, size in filedict[key]:
                    zf.write(f"cache/{file}")
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
        return filedict
    def FilterFiles(filelist):
        'Keep the files as indicated by the command line options'
        # filelist is list of (size_in_bytes, filename)
        # -i list:  regexes to keep
        keep = []
        Dbg("Filtering")
        for r in d["-i"]:
            Dbg(f"  Checking for {t.yell}{r}")
            for sz, filename in filelist:
                # Note we only use the regex on the name part of the Path object
                if r.search(str(filename.name)):
                    keep.append((sz, filename))
                    Dbg(f"  Kept {str(filename)!r}")
        filelist = keep
        # -x list:  regexes to ignore
        keep = []
        for r in d["-x"]:
            for sz, filename in filelist:
                if r.search(filename):
                    Dbg("  Ignored {str(filename)!r}")
                    continue
                keep.append((sz, filename))
        return keep
    def Report(filelist):
        # Print the file list summary
        print("Summary of size of each zip file")
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

if __name__ == "__main__":
    d = {}      # Options dictionary
    if 1:   # Get the command line information
        args = ParseCommandLine(d)
    if d["-R"]:
        ConstructZipFromList()
        exit()
    if 1: # Get number of zipfiles or their size in bytes
        g.prefix = None
        g.size = None
        g.size_units = ""
        N = args[0].strip()
        Dbg(f"Parsing of command line:")
        if N.endswith("M") or N.endswith("G"):
            g.size_units = "B"
            lastchar = N[-1]
            multiplier = 1e6 if lastchar == "M" else 1e9
            N = N[:-1]
            g.size = abs(flt(N))*multiplier
            Dbg(f"  {t.purl}{args[0]!r} gives zip file size of {g.size.engsi}{g.size_units}")
        else:
            g.size = abs(int(N))
            Dbg(f"  {t.magl}{args[0]!r} gives number of zip files as {g.size}")
        # Get the directory for the files
        g.dir = Path(args[1].strip())
        if not g.dir.exists() or not g.dir.is_dir():
            Error(f"{t.err}{str(g.dir)!r} is not a directory or doesn't exist{t.n}")
        Dbg(f"  {t.brnl}Directory is {str(g.dir)!r}")
    if 1:   # Construct a list of the files to zip
        # Each entry in the following list will be (size_in_bytes, filename) sorted from
        # smallest to largest
        g.filelist = GetFileList(g.dir)
        # Filter the files as instructed
        g.filelist = FilterFiles(g.filelist)
    if d["-p"]:
        ConstructZipFiles(g.filelist, d["-p"])
    else:
        Report(g.filelist)

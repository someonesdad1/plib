'''
Runs pycodestyle on the input files, collects the output data, and
summarizes it.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Runs pycodestyle on a set of python files
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import subprocess
        import sys
        from pdb import set_trace as xx
        from collections import defaultdict, namedtuple
        from pprint import pprint as pp
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from get import GetLines
        from lwtest import Assert
        from color import Color, TRM as t
        t.always = True
    # Global variables
        dbg = False
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Important and notable errors/warnings
        errors_important = set("E401 E402 E701 E702 E704 E722 E901 E902".split())
        errors_notable = set("E703 E711 E712 E713 E714 E731 E741 E742 E743".split())
        warnings_important = set("W191".split())
        warnings_notable = set("W601 W602 W603 W604 W605 W606".split())
        # Make a dict of errors/warnings that need colorizing
        clr = {}
        for i in errors_important:
            clr[i] = t("redl")
        for i in errors_notable:
            clr[i] = t("ornl")
        for i in warnings_important:
            clr[i] = t("purl")
        for i in warnings_notable:
            clr[i] = t("royl")
        # Colors
        t.dbg = t("lill")
        t.err = t("lip")
        # Named tuple to hold output lines' data
        Entry = namedtuple("Entry", "file linenum colnum errnum msg")
        # Dictionary mapping seen errors to the errors' description.  An
        # example entry is:
        #       "E501": "E501 line too long (81 > 79 # characters)"
        errors = {}
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2 ...]
          Run pycodestyle on the indicated files and present the summarized
          results.
        Options:
            -v      Debug output (more than one for more verbosity)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-v"] = 0     # Show debug output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ahv", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ad"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "-v":
                d[o] += 1
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        if d["-v"]:
            global dbg
            dbg = d["-v"]
        return args
    def Dbg(*p, **kw):
        'Assumes colorizing escape strings output to stdout'
        if not dbg:
            return
        print(f"{t.dbg}", end="")
        print(*p, **kw)
        print(f"{t.n}", end="")
if 1:   # Core functionality
    def ProcessFile(file, di):
        '''For the indicated python file, run pycodestyle in it and capture
        the output.  Return a list of Entry tuples.  The lines have the
        form
            fpformat.py:80:54: E241 multiple spaces after ','
        where the fields are the file name, line number, column number, and
        error message.
        '''
        Dbg(f"Processing file {file!r}")
        f = P(file)
        if not f.exists():
            t.print(f"{t.err}{file!r} doesn't exist")
            return
        cmd = ["pycodestyle", file]
        r = subprocess.run(cmd, capture_output=True, text=True)
        Dbg(f"pycodestyle returned {r.returncode} on {file!r}")
        # Return the list of strings from stdout
        out = []
        for line in r.stdout.split("\n"):
            line = line.strip()
            if not line:
                continue
            file, linenum, colnum, msg = line.split(":", maxsplit=4)
            linenum = int(linenum)
            colnum = int(colnum)
            msg = msg.strip()
            errnum = msg.split()[0]
            entry = Entry(file, linenum, colnum, errnum, msg)
            if dbg > 1:
                Dbg(f"{entry}")
            out.append(entry)
        return out
    def ProcessData(entries):
        '''entries is a list of Entry instances.  Classify these into a
        dict with the following structure
        {
            "E501": {
                "file1.py": [list of T tuples],
                "file2.py": [list of T tuples ],
                etc.
            },
        }
        where T tuples are (linenum, colnum, errnum); the first two are
        integers and the last is a string that indexes into the global errors.
        '''
        di = defaultdict(dict)
        Dbg(f"{len(entries)} entries to process")
        for entry in entries:
            if entry.errnum not in di:
                di[entry.errnum] = defaultdict(list)
            a = di[entry.errnum]
            T = (entry.linenum, entry.colnum, entry.errnum)
            a[entry.file].append(T)
            errors[entry.errnum] = entry.msg
        if d["-v"]:
            Dbg("Dump of dictionary of classified data:")
            print(f"{t.dbg}", end="")
            pp(di)
            t.out()
                
    def Report(di):
        pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    di = defaultdict(dict)
    entries = []
    for file in files:
        lines = ProcessFile(file, di)
        entries.extend(lines)
    di = ProcessData(entries)
    Report(di)


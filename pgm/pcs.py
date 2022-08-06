'''
Runs pycodestyle and summarizes results
    
    The basic goal is to classify the severity of the pycodestyle
    error/warning numbers into the following severity levels:

        0   Important and must be fixed
        1   Notable and should be fixed
        2   Low-priority fixes
        3   Ignored 

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
        # Dictionary to map seen errors to the errors' description.  An
        # example entry is:
        #       "E501": "E501 line too long (81 > 79 # characters)"
        errors = {}
        # Dictionary to map errors to their rank 0 to 3 with 0 most
        # important.
        error_ranks = {}
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
if 1:   # Rankings of error/warning types
    def GetErrorRankDict():
        '''Return a dict keyed by error/warning numbers like "E305" and
        values of integers on [0, 3]:
            0   Important and must be fixed
            1   Notable and should be fixed
            2   Low-priority fixes
            3   Ignored 
        '''
        global error_ranks
        for line in GetErrorRankDict.data.split("\n"):
            line = line.strip()
            if not line:
                continue
            f = line.split(maxsplit=3)
            rank = int(f[0])
            Assert(rank in range(4))
            errnum = f[1]
            error_ranks[errnum] = rank
    # Downloaded from https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
    # on 05 Aug 2022 06:58:55 PM
    GetErrorRankDict.data = '''
        0   E101 indentation contains mixed spaces and tabs
        0   E111 indentation is not a multiple of four
        2   E112 expected an indented block
        2   E113 unexpected indentation
        0   E114 indentation is not a multiple of four (comment)
        2   E115 expected an indented block (comment)
        2   E116 unexpected indentation (comment)
        2   E117 over-indented
        3   E121 continuation line under-indented for hanging indent
        2   E122 continuation line missing indentation or outdented
        3   E123 closing bracket does not match indentation of opening bracket’s line
        2   E124 closing bracket does not match visual indentation
        2   E125 continuation line with same indent as next logical line
        3   E126 continuation line over-indented for hanging indent
        2   E127 continuation line over-indented for visual indent
        2   E128 continuation line under-indented for visual indent
        2   E129 visually indented line with same indent as next logical line
        2   E131 continuation line unaligned for hanging indent
        1   E133 closing bracket is missing indentation
        1   E201 whitespace after ‘(’
        1   E202 whitespace before ‘)’
        1   E203 whitespace before ‘,’, ‘;’, or ‘:’
        1   E211 whitespace before ‘(’
        1   E221 multiple spaces before operator
        1   E222 multiple spaces after operator
        0   E223 tab before operator
        0   E224 tab after operator
        2   E225 missing whitespace around operator
        2   E226 missing whitespace around arithmetic operator
        1   E227 missing whitespace around bitwise or shift operator
        1   E228 missing whitespace around modulo operator
        1   E231 missing whitespace after ‘,’, ‘;’, or ‘:’
        1   E241 multiple spaces after ‘,’
        0   E242 tab after ‘,’
        1   E251 unexpected spaces around keyword / parameter equals
        1   E261 at least two spaces before inline comment
        1   E262 inline comment should start with ‘# ‘
        1   E265 block comment should start with ‘# ‘
        1   E266 too many leading ‘#’ for block comment
        1   E271 multiple spaces after keyword
        1   E272 multiple spaces before keyword
        0   E273 tab after keyword
        0   E274 tab before keyword
        1   E275 missing whitespace after keyword
        3   E301 expected 1 blank line, found 0
        3   E302 expected 2 blank lines, found 0
        1   E303 too many blank lines (3)
        1   E304 blank lines found after function decorator
        3   E305 expected 2 blank lines after end of function or class
        3   E306 expected 1 blank line before a nested definition
        0   E401 multiple imports on one line
        0   E402 module level import not at top of file
        3   E501 line too long (82 > 79 characters)
        1   E502 the backslash is redundant between brackets
        0   E701 multiple statements on one line (colon)
        0   E702 multiple statements on one line (semicolon)
        1   E703 statement ends with a semicolon
        0   E704 multiple statements on one line (def)
        0   E711 comparison to None should be ‘if cond is None:’
        0   E712 comparison to True should be ‘if cond is True:’ or ‘if cond:’
        1   E713 test for membership should be ‘not in’
        1   E714 test for object identity should be ‘is not’
        1   E721 do not compare types, use ‘isinstance()’
        0   E722 do not use bare except, specify exception instead
        1   E731 do not assign a lambda expression, use a def
        2   E741 do not use variables named ‘l’, ‘O’, or ‘I’
        2   E742 do not define classes named ‘l’, ‘O’, or ‘I’
        2   E743 do not define functions named ‘l’, ‘O’, or ‘I’
        0   E901 SyntaxError or IndentationError
        0   E902 IOError
        0   W191 indentation contains tabs
        3   W291 trailing whitespace
        2   W292 no newline at end of file
        3   W293 blank line contains whitespace
        2   W391 blank line at end of file
        3   W503 line break before binary operator
        3   W504 line break after binary operator
        2   W505 doc line too long (82 > 79 characters)
        0   W601 .has_key() is deprecated, use ‘in’
        0   W602 deprecated form of raising exception
        0   W603 ‘<>’ is deprecated, use ‘!=’
        0   W604 backticks are deprecated, use ‘repr()’
        0   W605 invalid escape sequence ‘x’
        0   W606 ‘async’ and ‘await’ are reserved keywords starting with Python 3.7
    '''
    GetErrorRankDict()

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
                "file1.py": [set of T tuples],
                "file2.py": [set of T tuples ],
                etc.
            },
        }
        where T tuples are (linenum, colnum); both entries are integers.
        '''
        di = defaultdict(dict)
        Dbg(f"{len(entries)} entries to process")
        for entry in entries:
            if entry.errnum not in di:
                di[entry.errnum] = defaultdict(set)
            a = di[entry.errnum]
            T = (entry.linenum, entry.colnum)
            a[entry.file].add(T)
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


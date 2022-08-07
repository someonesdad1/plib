'''
Runs pycodestyle and summarizes results

    The rankings used in this script are subjective.  Change the function
    GetErrorRankDict() to your tastes.  The script's purpose is to classify
    the severity of the pycodestyle error/warning numbers into: important,
    notable, low-priority, and ignored.

    For my python files, I will fix anything that is labeled a priority 3
    error.  Such things include 

        - Any use of tab characters
        - Indentation that is not a multiple of 4 spaces
        - Multiple imports or imports not at beginning of file
        - Multiple statements on one line
        - No bare 'except' usage
        - Deprecated usage.  

    Most of the priority 2 errors will be fixed.  I'll look at the
    remaining stuff and decide what needs fixing. 

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
        from wrap import wrap, dedent, HangingIndent
        from color import Color, TRM as t
        from get import GetLines
        from lwtest import Assert
        from color import Color, TRM as t
        if 0:
            import debug
            debug.SetDebugger()
    # Global variables
        t.always = True
        dbg = False
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.dbg = t("lill")
        t.err = t("lip")
        t.file = t("grnl")
        # Named tuple to hold output lines' data
        Entry = namedtuple("Entry", "file linenum colnum errnum msg")
        # Dictionary to map seen errors to the errors' description.  An
        # example entry is:
        #       "E501": "E501 line too long (81 > 79 # characters)"
        errors = {}
        # Dictionary to map errors to their rank 0 to 3 with 0 most
        # important.
        error_ranks = {}
        # Dictionary for error colors
        error_colors = {
            0: t("sky"),
            1: t("roy"),
            2: t("ornl"),
            3: t("redl"),
        }
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2 ...]
          Run pycodestyle on the indicated files and summarize the results.
          Returned status is 0 for nothing printed, 1 for one or more
          messages printed.  
        Options:
            -a      Show all errors/warnings [{d['-a']}]
            -f      Organize output by file  [{d['-f']}]
            -0      Print ignored items      [{d['-0']}]
            -1      Print low-priority items [{d['-1']}]
            -2      Print notable items      [{d['-2']}]
            -3      Print important items    [{d['-3']}]
            -c      Include column information with line numbers
            -v      Debug output (more than one for more verbosity)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all errors/warnings
        d["-f"] = True      # Organize output by file
        d["-0"] = False     # Show ignored items
        d["-1"] = False     # Show low-priority items
        d["-2"] = True      # Show notable items
        d["-3"] = True      # Show important items
        d["-c"] = False     # Include column numbers
        d["-v"] = 0         # Show debug output
        if len(sys.argv) < 2:
            Usage()
        a = ["help", "debug"]
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0123acfhv", a)
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("0123acf"):
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
        if d["-a"]:
            d["-0"] = d["-1"] = d["-2"] = d["-3"] = True
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
            0   Ignored
            1   Low-priority fixes
            2   Notable and should be fixed
            3   Important and must be fixed
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
    # Downloaded from
    # https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
    # on 05 Aug 2022 06:58:55 PM
    GetErrorRankDict.data = '''
        3   E101 indentation contains mixed spaces and tabs
        3   E111 indentation is not a multiple of four
        1   E112 expected an indented block
        1   E113 unexpected indentation
        3   E114 indentation is not a multiple of four (comment)
        1   E115 expected an indented block (comment)
        1   E116 unexpected indentation (comment)
        1   E117 over-indented
        0   E121 continuation line under-indented for hanging indent
        1   E122 continuation line missing indentation or outdented
        0   E123 closing bracket does not match indentation of opening bracket’s line
        1   E124 closing bracket does not match visual indentation
        1   E125 continuation line with same indent as next logical line
        0   E126 continuation line over-indented for hanging indent
        1   E127 continuation line over-indented for visual indent
        1   E128 continuation line under-indented for visual indent
        1   E129 visually indented line with same indent as next logical line
        1   E131 continuation line unaligned for hanging indent
        2   E133 closing bracket is missing indentation
        2   E201 whitespace after ‘(’
        2   E202 whitespace before ‘)’
        2   E203 whitespace before ‘,’, ‘;’, or ‘:’
        2   E211 whitespace before ‘(’
        2   E221 multiple spaces before operator
        2   E222 multiple spaces after operator
        3   E223 tab before operator
        3   E224 tab after operator
        1   E225 missing whitespace around operator
        0   E226 missing whitespace around arithmetic operator
        1   E227 missing whitespace around bitwise or shift operator
        1   E228 missing whitespace around modulo operator
        2   E231 missing whitespace after ‘,’, ‘;’, or ‘:’
        2   E241 multiple spaces after ‘,’
        3   E242 tab after ‘,’
        2   E251 unexpected spaces around keyword / parameter equals
        2   E261 at least two spaces before inline comment
        2   E262 inline comment should start with ‘# ‘
        0   E265 block comment should start with ‘# ‘
        1   E266 too many leading ‘#’ for block comment
        2   E271 multiple spaces after keyword
        2   E272 multiple spaces before keyword
        3   E273 tab after keyword
        3   E274 tab before keyword
        2   E275 missing whitespace after keyword
        0   E301 expected 1 blank line, found 0
        0   E302 expected 2 blank lines, found 0
        2   E303 too many blank lines (3)
        2   E304 blank lines found after function decorator
        0   E305 expected 2 blank lines after end of function or class
        0   E306 expected 1 blank line before a nested definition
        3   E401 multiple imports on one line
        3   E402 module level import not at top of file
        0   E501 line too long (82 > 79 characters)
        2   E502 the backslash is redundant between brackets
        3   E701 multiple statements on one line (colon)
        3   E702 multiple statements on one line (semicolon)
        2   E703 statement ends with a semicolon
        3   E704 multiple statements on one line (def)
        3   E711 comparison to None should be ‘if cond is None:’
        3   E712 comparison to True should be ‘if cond is True:’ or ‘if cond:’
        2   E713 test for membership should be ‘not in’
        2   E714 test for object identity should be ‘is not’
        2   E721 do not compare types, use ‘isinstance()’
        3   E722 do not use bare except, specify exception instead
        2   E731 do not assign a lambda expression, use a def
        1   E741 do not use variables named ‘l’, ‘O’, or ‘I’
        1   E742 do not define classes named ‘l’, ‘O’, or ‘I’
        1   E743 do not define functions named ‘l’, ‘O’, or ‘I’
        3   E901 SyntaxError or IndentationError
        3   E902 IOError
        3   W191 indentation contains tabs
        0   W291 trailing whitespace
        1   W292 no newline at end of file
        0   W293 blank line contains whitespace
        1   W391 blank line at end of file
        0   W503 line break before binary operator
        0   W504 line break after binary operator
        1   W505 doc line too long (82 > 79 characters)
        3   W601 .has_key() is deprecated, use ‘in’
        3   W602 deprecated form of raising exception
        3   W603 ‘<>’ is deprecated, use ‘!=’
        3   W604 backticks are deprecated, use ‘repr()’
        3   W605 invalid escape sequence ‘x’
        3   W606 ‘async’ and ‘await’ are reserved keywords starting with Python 3.7
    '''
if 1:   # Classes
    class Item:
        '''An item holds the following data:
            Error number (e.g. "E225")
            File name
            line_col = tuple of (line, column) where error was
        The __str__ method allows printing the item to stdout.
        '''
        # The default way of returning a string interpolation
        by_file = True
        def __init__(self, errnum, file, line_col):
            self.errnum = errnum
            self.file = file
            self.line_col = line_col
            self.rank = error_ranks[errnum]
            Assert(line_col)
            # Separate into line numbers and column numbers
            self.linenums, self.colnums = [], []
            for linenum, colnum in self.line_col:
                self.linenums.append(linenum)
                self.colnums.append(colnum)
            self.linenums = sorted(self.linenums)
            self.colnums = sorted(self.colnums)
        def __str__(self):
            '''Return a string that gives the filename, a ":", and the list
            of line numbers with one space between them.  Wrap things so
            that the line numbers are easy to read.
            '''
            if Item.by_file:
                if d["-c"]:
                    q = [f"{i}:{j}" for i, j in zip(self.linenums, self.colnums)]
                else:
                    q = self.linenums
                s = f"{' '.join(str(i) for i in q)}"
                i = " "*4
                return HangingIndent(s, indent=i, first_line_indent=i)
            else:
                if d["-c"]:
                    q = [f"{i}:{j}" for i, j in zip(self.linenums, self.colnums)]
                else:
                    q = self.linenums
                s = f"{self.file}: {' '.join(str(i) for i in q)}"
                return HangingIndent(s, indent=" "*4, first_line_indent=" "*2)
        def __repr__(self):
            'String for debugging'
            return f"Item({self.errnum}, {len(self.line_col)} lines)"
        def __lt__(self, other):
            return self.rank < other.rank
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
        cmd = ["pycodestyle", "--ignore=''", file]
        r = subprocess.run(cmd, capture_output=True, text=True)
        Dbg(f"pycodestyle returned {r.returncode} on {file!r}")
        # Return the list of strings from stdout
        out = []
        for line in r.stdout.split("\n"):
            line = line.strip()
            if not line:
                continue
            f = line.split(":", maxsplit=4)
            if len(f) == 4:
                file, linenum, colnum, msg = f
            else:
                file, linenum, colnum, msg, remainder = f
                msg = msg + ":" + remainder
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
                "file1.py": set of T tuples,
                "file2.py": set of T tuples,
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
        # Change the set of T tuples into an Item instance
        for errnum in di:
            for file in di[errnum]:
                T = di[errnum][file]
                item = Item(errnum, file, T)
                di[errnum][file] = item
        if d["-v"]:
            Dbg("Dump of dictionary of classified data:")
            print(f"{t.dbg}", end="")
            pp(di)
            t.out()
        return di
    def ReportByError(data):
        '''Print the condensed data by error/warning number.  data is a
        dict with the structure
        {
            "E501": {
                "file1.py": list of Item instances,
                "file2.py": list of Item instances,
                etc.
            },
        }
        '''
        Item.by_file = False
        count = 0  # Count number of items
        def Print(r):
            '''r is a dict keyed by error numbers with values of list of
            Item instances.
            '''
            nonlocal count
            for errnum, items in r.items():
                # Note all the items have the same rank
                c = error_colors[items[0].rank]
                t.print(f"{c}{errors[errnum]}")
                for item in items:
                    print(item)
                    count += 1
        # Divide up into ranked groups
        r0 = defaultdict(list)
        r1 = defaultdict(list)
        r2 = defaultdict(list)
        r3 = defaultdict(list)
        for errnum in data:
            for file in data[errnum]:
                item = data[errnum][file]
                if item.rank == 3:
                    r3[errnum].append(item)
                elif item.rank == 2:
                    r2[errnum].append(item)
                elif item.rank == 1:
                    r1[errnum].append(item)
                else:
                    r0[errnum].append(item)
        # Print data to stdout.  Notable and important items are printed
        # last so they are the easiest to see.
        if d["-0"]:
            Print(r0)
        if d["-1"]:
            Print(r1)
        if d["-2"]:
            Print(r2)
        if d["-3"]:
            Print(r3)
        return bool(count)
    def ReportByFile(data):
        '''Print the condensed data by file.  data is a dict with the
        structure
        {
            "E501": {
                "file1.py": list of Item instances,
                "file2.py": list of Item instances,
                etc.
            },
        }
        '''
        Item.by_file = True
        # Make a dictionary keyed by file name with values being that
        # file's Item instances.
        di = defaultdict(list)
        for errnum in data:
            for file in data[errnum]:
                di[file].append(data[errnum][file])
        def HasItemsToPrint(file):
            '''Return True if this file has data to print.  This determines
            if we should print the file's name.
            '''
            nonlocal di
            if d["-0"]:
                for item in di[file]:
                    if item.rank == 0:
                        return True
            if d["-1"]:
                for item in di[file]:
                    if item.rank == 1:
                        return True
            if d["-2"]:
                for item in di[file]:
                    if item.rank == 2:
                        return True
            if d["-3"]:
                for item in di[file]:
                    if item.rank == 3:
                        return True
            return False
        def Print(rank, items):
            'rank is int, items is list of Item instances'
            for item in items:
                if item.rank != rank:
                    continue
                c = error_colors[item.rank]
                t.print(f"  {c}{errors[item.errnum]}")
                s = str(item).replace(item.file + ":", "").strip()
                print(f"    {s}")
        # Sort the items by rank
        for file in di:
            di[file] = sorted(di[file])
        # Print items by file
        for file in sorted(di.keys()):
            if HasItemsToPrint(file):
                t.print(f"{t.file}{file}")
            else:
                continue
            items = di[file]
            if d["-0"]:
                Print(0, items)
            if d["-1"]:
                Print(1, items)
            if d["-2"]:
                Print(2, items)
            if d["-3"]:
                Print(3, items)

if __name__ == "__main__":
    d = {}      # Options dictionary
    GetErrorRankDict()
    files = ParseCommandLine(d)
    di = defaultdict(dict)
    entries = []
    for file in files:
        lines = ProcessFile(file, di)
        entries.extend(lines)
    di = ProcessData(entries)
    status = ReportByFile(di) if d["-f"] else ReportByError(di)
    exit(status)

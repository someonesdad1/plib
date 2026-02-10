#!/usr/bin/python
'''
Function to turn a sequence into columns
    - Run the module as a script to columnize stdin.  Use -h to get a usage statement.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Turn a sequence into columns for printing oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2012 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ text oo>
        <oo test ∞ --test oo>
        <oo todo ∞ 
        
            - ∞∞1 'res l' displays a serious bug
            - Feb  5 2024:  'ls --color=always | columnize.py' doesn't work right in
              /plib
            - Columnize(['a'], indent=" "*4) has an exception
            - Columnize raises a ValueError exception when something is too long.  There
              should be an option to just print this line anyway and continue, as it
              often breaks some application and you can't see your output.  Typical
              message is "ValueError: Cannot fit longest string (118 characters) on
              screen"
        
        oo>
    '''
    if 1:  # Standard imports
        import os
        import re
    if 1:  # Custom imports
        from dpprint import PP
        pp = PP()  # COLUMNS-aware version of pprint.pprint
if 1:  # Core functionality
    def Columnize(seq, **kw):
        '''Returns a list of strings with the elements of the sequence seq (if
        components are not strings, they will be converted to strings using str)
        formatted in columnar format.  Elements of seq that won't fit in a column either
        generate an exception if trunc is False or get truncated if trunc is True.
        
        The keyword arguments are (default values are in square brackets):
        
        align  [left]   How to align the string in each column.  Can be
                        "left" or "<", "center" or "^", or "right" or ">".
                        
        col_width [0]   Specify the column width to use.  If nonzero, then
                        this overrides the calculation of the column width.
                        
        columns [0]     Number of columns to format the strings into.  If
                        it's zero, it will be figured out from the length
                        of the largest string and the screen width.
                        
        debug           If True, print out debug information.
        
        esc [True]      Strip out ANSI escape sequences when calculating string
                        lengths.  This allows you to display colored text in
                        columns.
                        
        horiz   [False] If True, the sequence is listed from
                        left-to-right; the default is top-to-bottom.  The
                        "shape" of both outputs will be the same.
                        
                        
        indent [None]   If defined, then it is a string to prepend to each
                        line.
                        
        sep     [" "]   String to use to separate columns.
        
        to_string [False]  If true, convert the array that would be
                        returned to a single string with the rows
                        separated by newlines.
                        
        trunc   [False] If True, truncate a string to get it to fit into a
                        column.  If False, an exception is raised if a
                        string is too long for a column.
                        
        width   [0]     Specify the width of the screen.  If it's zero,
                        then get it from the COLUMNS environment variable
                        if it exists; if it doesn't exist, use 79.  If
                        columns is given instead, then width is set to
                        accommodate the desired output.
        '''
        '''
        Implementation details:  the formatting of the left-to-right format is
        straightforward.  The top-to-bottom format is a little more difficult.  Here's
        an example that shows how the algorithm was gotten.  Suppose we want to print
        the numbers in range(18) in 7 columns of a specified width.  The output will
        need to look as follows, as this shape matches the left-to-right output:
     
            0   3   6   9   12  14  16
            1   4   7   10  13  15  17
            2   5   8   11  .   .   .
     
        where '.' denotes the gap.  The number of full rows is int(n/columns) where n =
        len(seq) and columns is the number of columns).  Here, clearly, we need 3 rows
        to properly print; thus, the gap is (rows*columns - n).  Then we need to account
        for the number of numbers to print in each column; the vector for this is [3, 3,
        3, 3, 2, 2, 2] (see the code for how it's constructed).  Finally, in the
        iteration loop, we need to use a correction factor for when we append the empty
        string for the gap rather than a sequence element.
        '''
        if not seq:
            return [""]
        # Check keywords
        allowed = set(('''
            align col_width columns debug esc horiz ignore indent sep
            to_string trunc width'''.split()))
        for k in kw:
            if k not in allowed:
                raise ValueError(f"'{k}' is an unknown keyword")
        # Get keyword parameters
        align = kw.setdefault("align", "left")
        col_width = abs(int(kw.setdefault("col_width", 0)))
        columns = abs(int(kw.setdefault("columns", 0)))
        debug = bool(kw.setdefault("debug", False))
        esc = kw.setdefault("esc", True)
        horiz = kw.setdefault("horiz", False)
        ignore = kw.setdefault("ignore", False)
        if ignore:
            return [str(i) for i in seq]
        indent = kw.setdefault("indent", None)
        sep = kw.setdefault("sep", " ")
        to_string = kw.setdefault("to_string", False)
        trunc = kw.setdefault("trunc", False)
        width = abs(int(kw.setdefault("width", 0)))
        d = {"left": "<", "right": ">", "center": "^", "<": "<", ">": ">", "^": "^"}
        if align not in d:
            raise ValueError("align must be left, right, center, <, >, or ^")
        if indent is not None and not isinstance(indent, str):
            raise ValueError("indent must be a string")
        align = d[align]
        if esc:
            # Regular expression to recognize ANSI escape sequences
            r = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
            def Len(s):
                "Returns the length of a string s after removing the escape sequences"
                # This is same as Len in util.py, but avoids a circular import
                return len(r.sub("", s))
        else:
            Len = len
        # Turn seq into a sequence of strings
        sseq = [str(i) for i in seq]
        n, maxlen, lsep = len(sseq), max([Len(i) for i in sseq]), len(sep)
        # Pick reasonable defaults if width and columns not given
        if not width:
            width = int(os.environ.get("COLUMNS", 80)) - 1
            if not columns:
                columns = width // (maxlen + len(sep))
                if not columns:
                    msg = f"Cannot fit longest string ({maxlen} characters) on screen"
                    raise ValueError(msg)
            else:
                if columns < 1:
                    raise ValueError(f"'{columns}' is a bad value for columns")
                sw = lsep * (columns - 1)
                width = (columns * col_width if col_width else columns * maxlen) + sw
        if indent is not None:
            width -= len(indent)
            if width < 1:
                raise ValueError("indent is too large")
        # Get the number of columns we should print into
        e = ValueError("The width won't allow one column (try trunc=True)")
        if not columns:
            if col_width:
                columns = abs(int(width // (col_width + lsep)))
            else:
                columns = abs(int(width // (maxlen + lsep)))
                col_width = maxlen
        if not col_width:
            col_width = abs(int((width - (columns - 1) * lsep) / columns))
            if col_width < maxlen:
                columns -= 1
                if columns < 1:
                    raise e
                col_width = abs(int((width - (columns - 1) * lsep) / columns))
        # Ensure we're below the width of the screen
        total_width = col_width * columns + lsep * (columns - 1)
        while total_width > width:
            columns -= 1
            total_width = col_width * columns + lsep * (columns - 1)
        if not columns and not trunc:
            raise e
        # Set up number of rows and counts of number of items in each
        # column for non-horiz formatting.
        if not columns:
            columns = 1
        rows = int(n // columns) + (n % columns > 0)
        num_in_column, gap = [rows] * columns, rows * columns - n
        # Correct for gap
        for i in range(gap):
            num_in_column[-(i + 1)] -= 1
        if debug:
            print("Keyword dictionary:")
            pp(kw)
            print("screen width  = ", width)
            print("col_width     = ", col_width)
            print("total_width   = ", total_width)
            print("lsep          = ", lsep)
            print("columns       = ", columns)
            print("rows          = ", rows)
            print("gap           = ", rows * columns - n)
            print("num_in_column = ", num_in_column)
            print()
        s, fmt = [], "{0:" + align + str(col_width) + "}"
        II = indent if indent is not None else ""
        if horiz:
            for i, item in enumerate(sseq):
                row, col = divmod(i, columns)
                if not col:
                    srow = []  # Start a new row
                item = fmt.format(item)
                if not trunc and Len(item) > col_width:
                    msg = "'%s' too long for formatting" % item
                    raise ValueError(msg)
                srow.append(item[:col_width] if trunc else item)
                if col >= columns - 1:
                    s.append(sep.join(srow))
                    srow = []
            if srow:
                s.append(sep.join(srow))
            s = [II + i for i in s]
        else:
            # Construct each column.  We use a correction to account for
            # columns that don't require the full number of rows; this
            # ensures that we iterate over all items in sseq.
            cols, correction = [], 0
            for col in range(columns):
                scol = []  # Start a new column
                for row in range(rows):
                    # Get index into sseq
                    i = col * rows + row
                    if i > n - 1 + correction or row >= num_in_column[col]:
                        item = ""
                        correction += 1
                    else:
                        item = sseq[i - correction]
                    item = fmt.format(item)
                    if not trunc and Len(item) > col_width:
                        msg = "'%s' too long for formatting" % item
                        raise ValueError(msg)
                    # Append spaces if Len is < col_width
                    if Len(item) < col_width:
                        item += " " * (col_width - Len(item))
                    # Note truncation may damage ANSI sequences in some
                    # cases.
                    scol.append(item[:col_width] if trunc else item)
                cols.append(scol)
            # Get transpose of the just-constructed matrix
            mat = []
            for i in range(rows):
                mat.append([""] * columns)
            for col in range(columns):
                for row in range(rows):
                    mat[row][col] = cols[col][row]
            # Now build an array of the row strings
            for i in mat:
                s.append(II + sep.join(i))
        # Remove trailing spaces
        for i, x in enumerate(s):
            s[i] = x.rstrip()
        if to_string:
            s = "\n".join(s)
        return s
    def Uncolumnize(seq, in_sorted_order=False):
        '''Given a sequence of strings, uncolumnize them and return a single-line string.
        Here's an example: Suppose the following list of files was on your screen:
        
            atm.py             columnize.py       fmt.py             primes.py
            atomic_mass.py     cuncertainties.py  frange.py          prob.py
            bits.py            e.py               gauge_sizes.py     roundoff.py
            color.py           filesizes.py       globalcontainer.py sig.py
        
        This was a list of certain files in /plib that was printed by using Columnize.
        To Uncolumnize this list, you split each line on whitespace, then append each 
        line's elements to a new list.  Set in_sorted_order to True to have the list sorted.
        '''
        o = []
        for line in seq:
            o.extend(line.split())
        return list(sorted(o)) if in_sorted_order else o

if __name__ == "__main__":
    # Running as a script provides a utility similar to pr.
    import sys
    import getopt
    from wrap import dedent
    from lwtest import run, Assert
    requested_columns = 0
    column_width = 0
    alignment = "left"
    separator = " "
    truncate = False
    def TestBasicBehavior():
        strings = ["12345678"] * 30
        result = Columnize(strings, width=80, col_width=9)
        # Construct expected result
        e = ["12345678  "]
        row = "".join(e * 8).rstrip()
        expected = [row] * 3 + ["".join(e * 6).rstrip()]
        # Check they're the same
        Assert(result == expected)
    def TestHoriz():
        seq = [str(i) for i in range(32)]
        result = Columnize(seq, width=20, columns=4, horiz=False)
        expected = [
            i.lstrip()
            for i in '''
            0    8    16   24
            1    9    17   25
            2    10   18   26
            3    11   19   27
            4    12   20   28
            5    13   21   29
            6    14   22   30
            7    15   23   31'''[1:].split("\n")
        ]
        Assert(result == expected)
        result = Columnize(seq, width=20, columns=4, horiz=True)
        s = '''
            0    1    2    3
            4    5    6    7
            8    9    10   11
            12   13   14   15
            16   17   18   19
            20   21   22   23
            24   25   26   27
            28   29   30   31'''[1:]
        expected = [i.lstrip() for i in s.split("\n")]
        Assert(result == expected)
        # Now check that we can use the to_string keyword to get a string
        # equivalent.
        string = result = Columnize(
            seq, width=20, columns=4, horiz=True, to_string=True
        )
        Assert(string == "\n".join(expected))
    def TestIdentityXfm():
        seq = [str(i) for i in range(12)]
        result = Columnize(seq, ignore=True)
        Assert(seq == result)
    def TestSeparator():
        seq = [str(i) for i in range(12)]
        result = Columnize(seq, width=12, columns=4, sep="|")
        expected = [
            i.lstrip()
            for i in '''
            0 |3 |6 |9
            1 |4 |7 |10
            2 |5 |8 |11'''[1:].split("\n")
        ]
        Assert(result == expected)
    def TestIndent():
        seq = [str(i) for i in range(12)]
        result = Columnize(seq, width=18, columns=4, indent="qqq")
        expected = [
            i.lstrip()
            for i in '''
            qqq0   3   6   9
            qqq1   4   7   10
            qqq2   5   8   11'''[1:].split("\n")
        ]
        Assert(result == expected)
    def TestTruncation():
        seq = [str(i) for i in range(12)]
        result = Columnize(seq, col_width=1, columns=4, trunc=True)
        expected = [
            i.lstrip()
            for i in '''
            0 3 6 9
            1 4 7 1
            2 5 8 1'''[1:].split("\n")
        ]
        Assert(result == expected)
    def TestAlignment():
        seq = [str(i) for i in range(12)]
        result = Columnize(seq, col_width=10, columns=4, sep="|")
        expected = [
            i.lstrip()
            for i in '''
            0         |3         |6         |9
            1         |4         |7         |10
            2         |5         |8         |11'''[1:].split("\n")
        ]
        Assert(result == expected)
        # Show this is the same as left alignment
        result = Columnize(seq, col_width=10, columns=4, sep="|", align="left")
        Assert(result == expected)
        result = Columnize(seq, col_width=10, columns=4, sep="|", align="<")
        Assert(result == expected)
        # Centered
        result = Columnize(seq, col_width=10, columns=4, sep="|", align="^")
        expected = [
            "    0     |    3     |    6     |    9",
            "    1     |    4     |    7     |    10",
            "    2     |    5     |    8     |    11",
        ]
        Assert(result == expected)
        result = Columnize(seq, col_width=10, columns=4, sep="|", align="center")
        Assert(result == expected)
        # Right-aligned
        result = Columnize(seq, col_width=10, columns=4, sep="|", align=">")
        expected = [
            i
            for i in '''
            0|         3|         6|         9
            1|         4|         7|        10
            2|         5|         8|        11'''[1:].split("\n")
        ]
        expected = [
            "         0|         3|         6|         9",
            "         1|         4|         7|        10",
            "         2|         5|         8|        11",
        ]
        Assert(result == expected)
        result = Columnize(seq, col_width=10, columns=4, sep="|", align="right")
        Assert(result == expected)
    def Usage(status=1):
        name = sys.argv[0]
        print(
            dedent(f'''
        Usage:  {name} [options] [file1 ...]
          Prints in columns.  The number of columns is made a maximum to fit into the
          current screen width given in the COLUMNS environment variable less one
          character.  If no files are given on the command line, input is taken from
          stdin.
        Options
            -a s    Align each column as indicated by s:  left or <, center or ^,
                    right or >.
            -c n    Force number of columns to be n.  Resulting line length ignores
                    COLUMNS; no strings are truncated.
            -e      Ignore ANSI escape sequences (e.g., terminal color codes).
            -f      Adjust column width and number of columns to attempt to get the
                    output within the given number of LINES and COLUMNS.
            -h      Print this help message
            -i s    Indent each output line with the string s.
            -k s    Separate each column with the string s.
            -s      Sort the sequence when uncolumnizing (implies -u)
            -t      Truncate each string if needed to fit into the column width.
            -U      Same as supplying -u and -s
            -u      Uncolumnize the input into one line of data
            -w n    Set the column width.
        ''')
        )
        exit(status)
    def ParseCommandLine():
        d["-a"] = "left"    # Alignment
        d["-c"] = 0         # Requested number of columns
        d["-e"] = False     # Ignore ANSI escape sequences
        d["-f"] = False     # Fit into available screen
        d["-i"] = None      # Indent string
        d["-k"] = " "       # Separator
        d["-s"] = False     # Sort the uncolumnized data
        d["-t"] = False     # Truncate
        d["-U"] = False     # Uncolumnize and sort
        d["-u"] = False     # Uncolumnize
        d["-w"] = 0         # Column width
        d["--test"] = False # Run self tests
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "a:c:efhi:k:stUuw:", "test")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in "efstUu":
                d[o] = not d[o]
            elif o[1] in "aik":
                d[o] = a
            elif o == "-c":
                d[o] = int(a)
                if d[o] <= 0:
                    print("Number of columns must be > 0", file=sys.stderr)
                    exit(1)
            elif o == "-h":
                Usage()
            elif o in ("--test",):
                exit(run(globals(), halt=1)[0])
            elif o == "-w":
                d[o] = abs(int(a))
        if d["-U"]:
            d["-u"] = d["-s"] = True
        if d["-s"]:
            d["-u"] = True
        return args
    def GetInput(files):
        if not files:
            lines = [i.rstrip() for i in sys.stdin.readlines()]
        else:
            lines = []
            for file in files:
                lines += [i.rstrip() for i in open(file).readlines()]
        return lines
    def Fit(lines):
        '''Find out how many LINES and COLUMNS we have for the screen.
        Then adjust the parameters to Columnize to get the lines to
        fit on the screen; truncate as necessary.
        
        The basic task will be to get the resulting lines of the
        output to fit into LINES - 3 lines, as I use a prompt of 2
        lines (this lets me see an empty line at top, so that I know
        something hasn't scrolled off screen).  The canonical example
        of use of this feature is to get a long ls listing to fit on
        the screen.
        '''
        separator = " "
        width = int(os.environ["COLUMNS"]) - 1
        length = int(os.environ["LINES"]) - 2
        n = int(len(lines) // length)
        # Calculate truncation.  The formula for total width W is
        # n*cw+(n-1)*sep where n is number of columns, cw is column
        # width, and sep is the length of the separator.  This solves
        # to give cw = (W - (n-1)*sep)/n.
        cw = int((width - (n - 1) * len(separator)) / n)
        msg = "Can't fit the requested information"
        assert cw > 0, msg
        kw = {
            "align": d["-a"],
            "col_width": cw,
            "esc": d["-e"],
            "sep": separator,
            "trunc": True,
            "width": width,
        }
        s = Columnize(lines, **kw)
        while len(s) > length:
            kw["col_width"] -= 1
            assert kw["col_width"] > 1, msg
            s = Columnize(lines, **kw)
        for i in s:
            print(i)
        exit(0)
    if 1:   # Main code
        d = {}
        files = ParseCommandLine()
        if d["--test"]:
            exit(run(globals(), halt=1)[0])
        lines = GetInput(files)
        if d["-f"]:
            Fit(lines)
        elif d["-u"]:
            o = Uncolumnize(lines, in_sorted_order=d["-s"])
            print(' '.join(o))
        else:
            if d["-c"]:
                kw = {
                    "align": d["-a"],
                    "col_width": d["-w"],
                    "columns": d["-c"],
                    "esc": d["-e"],
                    "indent": d["-i"],
                    "sep": d["-k"],
                    "trunc": d["-t"],
                }
            else:
                kw = {
                    "align": d["-a"],
                    "col_width": d["-w"],
                    "esc": d["-e"],
                    "indent": d["-i"],
                    "sep": d["-k"],
                    "trunc": d["-t"],
                    "width": int(os.environ["COLUMNS"]) - 1,
                }
            s = Columnize(lines, **kw)
            for i in s:
                print(i)

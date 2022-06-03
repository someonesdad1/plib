'''
- Add --test option and make it a command line too for text files.
- Default splitting of lines for fields is str.split()
- Options
    - -c specifies the regex that marks a line as a comment, which
      is ignored.  Default is '^\s*#'.
    - --csv Parse as a CSV file
    - -s Specify string to split on
    - -r Specify regexp to split on

Generate the transpose of a nested list (matrix or vector) of objects
    
    The primary use case is when dealing with a text file of numbers.
    Often, we have data representing vectors of numbers on a single line of
    text, but we want to input such vectors to a program like the old
    XWindows' xplot program that needed these row vectors in column-vector
    form.  Running this file as a script on such a text file will produce
    the needed form.  Example:

    Input file of row vectors
        1 2 3 
        4 5 6
    Output of column vectors:
        1 4
        2 5
        3 6

    A basic data structures course will teach you that the easiest way to
    get the transpose of a two-dimensional array stored sequentially in
    memory is to store the array with row-major ordering, then read it out
    with column-major ordering.  If the matrix element is a[i][j], then the
    matrix's transposed element is a[j][i], just like you learned in basic
    matrix algebra.

    This is easy in languages like C/C++ where arrays are sequential chunks
    of memory and you use the right-size pointer strides, but it's not as
    trivial in python because you also need to handle row vectors, column
    vectors, matrices, and empty matrices, all of which can be either
    homogeneous or heterogeneous in their element types.  A further
    complication is that you can't blindly use python's len() function, as
    some matrix elements could be strings when you're assuming the contents
    of a matrix are nested lists.  Thus, the Len() function needs to be
    substituted.  It's not quite as simple a task as it first appears and
    most of the things found in a web search turn up naive solutions, at
    least in the context of what I wanted this function to do (naive
    solutions assume a nested list of numbers and don't handle the corner
    cases).  

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
        # Transpose a rectangular array of objects
        #∞what∞#
        #∞test∞# --test #∞test∞#
    # Standard imports
        from pprint import pprint as pp
        import getopt
        import re
        from pathlib import Path as P
        import sys
    # Custom imports
        from wrap import wrap, dedent
        from util import IsIterable
        from lwtest import run, raises, assert_equal, Assert
        from get import GetLines
    # Global variables
        ii = isinstance
        __all__ = ["Transpose"]
        class g: pass
        g.type = None
        g.homogenous = False
if 1:   # Core functionality
    def Transpose(seq, homogenous=False):
        '''seq must be 
            1) a list or tuple of objects (i.e., a vector) 
            2) a nested list or nested tuple of objects (a rectangular matrix)
        The transpose of the sequence seq is returned as a nested list.  If
        homogenous is True, then each element must be of the same type.
        '''
        if not ii(seq, (list, tuple)):
            raise TypeError("seq must be a list or tuple")
        nrows, ncols = Size(seq)
        trows, tcols = ncols, nrows
        if not nrows or not ncols:
            return []
        if nrows == 1 and ncols == 1:
            return list(seq)
        # Get the required type for testing homogeneity
        g.homogenous = homogenous
        if homogenous:
            item0 = seq[0]
            if ii(item0, (list, tuple)):
                item0 = item0[0]
            g.type = type(item0)
        # Set up the return matrix
        out, row_vector, col_vector = [], 0, 0
        if nrows == 1 and ncols != 1:       # seq was row vector
            # Result is column vector
            col_vector = ncols
            for i in range(trows):
                out.append([0])
        elif nrows != 1 and ncols == 1:     # seq was column vector
            # Result is row vector
            row_vector = nrows
            out = [0]*tcols
        else:
            # seq was a matrix
            if not IsRectangular(seq):
                raise ValueError("seq is not a rectangular matrix")
            for i in range(trows):
                out.append([0])
            for i in range(trows):
                out[i] = [0]*tcols
        # Replace the elements
        if col_vector:
            for i in range(col_vector):
                j = seq[i][0] if IsIterable(seq[i]) else seq[i]
                IsHomogenous(j)
                out[i][0] = j
        elif row_vector:
            for i in range(row_vector):
                j = seq[i][0] if IsIterable(seq[i]) else seq[i]
                IsHomogenous(j)
                out[i] = j
        else:
            for i in range(nrows):
                for j in range(ncols):
                    IsHomogenous(seq[i][j])
                    out[j][i] = seq[i][j]
        if 0:
            # Show the details
            print(f"{msg}")
            print(f"  seq = {seq}")
            print(f"  Size = ({nrows}, {ncols}])")
            print("  out sequence:")
            pp(out)
        g.homogenous = False
        return out
    def IsRectangular(m):
        ''' Return True if each row has the same number of columns as
        determined by Len().
        '''
        rows = Len(m)
        columns = Len(m[0])
        return all(Len(row) == columns for row in m)
    def IsHomogenous(x):
        if not g.homogenous:
            return
        if type(x) != g.type:
            raise TypeError(f"{x!r} is not of type {g.type}")
    def Size(m):
        'Return (rows, columns) for m'
        rows = Len(m)
        if not rows:
            # Corner case:  empty sequence
            return (0, 0)
        # Count the number of columns
        columns = 0
        n = Len(m[0])   # Number of items in first element
        if not n:
            # First element is a string or object, so the sequence must be
            # a row vector of analogous objects.  All other items must have
            # Len of zero.
            if len(m) == 1:
                return (1, 1)   # Corner case:  single element
            else:
                for item in m:
                    if Len(item):
                        raise TypeError(f"Element {item!r} doesn't have Len of zero")
                    columns += 1
                return (1, columns)
        else:
            # Each item in m must have the Len of n
            for item in m:
                if Len(item) != n:
                    raise TypeError(f"Non-rectangular matrix")
            return (rows, n)
        raise RuntimeError("Coding error:  should never reach this point")
    def Len(item):
        '''Return the length of the item.  If it's an iterable that's not a
        string, the normal len() is returned; otherwise, 0 is returned.
        '''
        return len(item) if IsIterable(item, ignore_strings=True) else 0

if __name__ == "__main__":
    if 1:   # Test code
        def TestEmpty():
            for i in ([], ()):
                Assert(Transpose(i) == [])
        def TestRowVector():
            v = ["abc", 1]
            expected = [["abc"], [1]]
            Assert(Transpose(v) == expected)
            # One element
            for v in (["abc"], ("abc",), [44], [44.]):
                Assert(Transpose(v) == list(v))
        def TestColumnVector():
            v = [["abc"], [1]]
            expected = ["abc", 1]
            Assert(Transpose(v) == expected)
            v = (("abc",), (1,))
            Assert(Transpose(v) == expected)
        def TestMatrix():
            m = [["abc", 1], [4.8, "Another string"]]
            expected = [["abc", 4.8], [1, "Another string"]]
            Assert(Transpose(m) == expected)
            # 
            m = [[1, 2, 3, 4], [5, 6, 7, 8]]
        def TestHomogeneity():
            v = [1, 2]
            expected = [[1], [2]]
            Assert(Transpose(v, homogenous=True) == expected)
            v = [1, "2"]
            with raises(TypeError):
                Transpose(v, homogenous=True)
        def TestInversion():
            # Use lists so that they'll compare equal
            import time
            import math
            from f import flt
            from decimal import Decimal
            # Vector
            v = ["a", 1, 2, 3-3j, Decimal(math.pi)]
            w = Transpose(v)
            Assert(Transpose(w) == v)
            # Matrix
            start = time.time()
            class g:
                def __init__(self):
                    self.x = 1e6*flt(time.time() - start)
                def __str__(self):
                    return f"g({self.x})"
                def __repr__(self):
                    return repr(str(self))
            m = [["a", 1, 2., g()], [1-1j, g(), g(), "glorp"]]
            w = Transpose(m)
            Assert(Transpose(w) == m)
        def RunSelfTests():
            exit(run(globals(), halt=True)[0])
    if 1:   # Script
        def Manpage():
            breakpoint() #xx
            exit(0)
        def Error(*msg, status=1):
            print(*msg, file=sys.stderr)
            exit(status)
        def Usage(status=1):
            print(dedent(f'''
            Usage:  {sys.argv[0]} [options] [file1 [file2...]]
              Transpose the text objects in the indicated files.  -r or -R
              take precedence over -s.  If you get an exception when
              processing, use the -v option to see how your input file was
              interpreted.
            Options:
              -c r    Define regexp that marks a line as a comment [{d['-c']}]
              --csv   Parse file for objects as a CSV file
              -h      Print a manpage
              -i r    Regexp for a line to ignore (can have more than one)
              -j s    String to rejoin fields for printing [' ']
              -R r    Specify regexp to split lines, case independent
              -r r    Specify regexp to split lines
              -s s    Specify string to split lines [whitespace]
              -v      Verbose output:  show input and output
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-c"] = "^\s*#"   # Regexp to mark line as a comment
            d["--csv"] = False  # Parse lines for objects as CSV file
            d["-h"] = False     # Manpage
            d["-i"] = []        # Regexps for lines to ignore
            d["-j"] = " "       # String to rejoin fields for printing
            d["-R"] = None      # Regexp to split lines, ignore case
            d["-r"] = None      # Regexp to split lines
            d["-s"] = None      # String to split lines
            d["-v"] = False     # Verbose output
            if len(sys.argv) < 2:
                Usage()
            try:
                opts, args = getopt.getopt(sys.argv[1:], "c:hi:j:R:r:s:v", 
                        ["help", "test", "csv"])
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("hv"):
                    d[o] = not d[o]
                elif o == "-c":
                    d[o] = re.compile(a)
                elif o == "-h":
                    Manpage()
                elif o == "-i":
                    d[o].append(re.compile(a))
                elif o == "-j":
                    d[o] = a
                elif o == "--csv":
                    d["--csv"] = not d["--csv"]
                elif o == "--test":
                    RunSelfTests()
                elif o == "-R":
                    d[o] = re.compile(a, re.I)
                elif o == "-r":
                    d[o] = re.compile(a)
                elif o == "-s":
                    d[o] = a
                    if not a:
                        raise ValueError("-s option must have nonempty string")
            if d["-h"]:
                Manpage()
            if d["-c"]:
                d["-i"].append(re.compile(d["-c"]))
            # Check that d["-i"] contains only compiled regular expressions
            if d["-i"]:
                t = type(re.compile("x"))
                if not all(type(i) == t for i in d["-i"]):
                    Error("Not all -i options are regular expressions")
            return args
        def PrintLines(seq):
            assert(seq)
            for i in seq:
                print(d["-j"].join(i))
        def ProcessFile(file):
            lines = GetLines(file, ignore=d["-i"], ignore_empty=True, strip= True) 
            # Build array
            input = []
            for line in lines:
                # Split line into fields
                if d["-R"]:
                    f = d["-R"].split(line)
                elif d["-r"]:
                    f = d["-r"].split(line)
                else:
                    f = line.split(d["-s"])
                input.append(f)
            if d["-v"]:
                print(f"Input {file!r}")
                PrintLines(input)
            output = Transpose(input)
            if d["-v"]:
                print("Output:")
            PrintLines(output)

    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    while True:
        if files:
            file = files.pop(0)
            ProcessFile(file)
        if files:
            print()
        else:
            break

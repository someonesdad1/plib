"""
Prints hex dumps of the differences between two files
"""

"""
Algorithm

    The method is to read in blocks of the files and perform comparisons on
    the blocks.  Any differences are stored in a range structure (that is
    just two integers) that gives the offset of the sequence of bytes that
    were different.  The scan through the files produces an array of these
    range structures.  Then this information is processed for display to
    the user.  Here, the sequences are displayed as hex dumps, but other
    software could e.g. display it on the screen using curses.

    The program was written to work in both 32 bit Windows and Linux.

    The basic algorithm for generating the ranges is based on a state
    machine.  The main variables are offset (the position of the pointer
    into the file stream), start, the beginning of a range, and end,
    the end of a range.  The states are:

        S0       Beginning state
        S1       Range on state (a difference was found, so we're in a state
                 of bytes continuing to be different)
        S2       Range off state (we were in a range on state, but now we 
                 found two bytes that were equal, so switch to range off state)
        S3       Ending state (processing of block finished)

    State transitions are caused by the events of the next two
    correspondings bytes are equal, not equal, or the end of the block
    is encountered.

    The state transitions and their actions are (= means bytes were equal,
    != means they were unequal, EOB means end of block):

        Transition  Caused by   Action
        ----------  ---------   --------------------------------------------------
        S0-S1          !=       Set start = end = offset
        S0-S2          =        No action
        S1-S1          !=       Set end = offset
        S1-S2          =        Append [start, end] to range list.
                                Then set start = end = INVALID_VALUE 
        S1-S3          EOB      If start != INVALID_VALUE append [start, end] to
        range list.
        S2-S1          !=       Set start = end = offset
        S2-S2          =        No action
        S2-S3          EOB      No action
        --------------------------------------------------------------------------

    (This looks a little cleaner on a state machine diagram.)
"""
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Prints hex dumps of the differences between two files
    ##∞what∞#
    ##∞test∞# --test #∞test∞#
    # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import sys
    import enum
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent
    from color import Color, TRM as t
    from lwtest import Assert

    if 0:
        from hexdump import hexdump
    else:
        from hd import hexdump
    # Global variables
    ii = isinstance

    class g:
        pass

    g.columns = int(os.environ.get("COLUMNS", "80")) - 1
    g.lines = int(os.environ.get("LINES", "50"))
    g.block_size = 2**16
    g.offset = 0  # Offset for both file buffers
    g.path1 = None  # Path object to file 1
    g.path2 = None  # Path object to file 2
    g.size1 = None  # Size of file1 in bytes
    g.size2 = None  # Size of file2 in bytes
    g.size = None  # Common number of bytes
    g.stream1 = None  # Stream 1
    g.stream2 = None  # Stream 2
    g.buf1 = None  # Buffer 1
    g.buf2 = None  # Buffer 2
    # States of the finite state machine
    g.start = 0  # Starting state
    g.eq = 1  # Last bytes were equal
    g.ne = 2  # Last bytes were unequal
    g.end = 3  # Encountered end of file
    g.previous_state = g.start
    g.state = g.start
    # The following list contains Diff objects that show where
    # the bytes were different.
    g.diffs = []
    # Set to True to get debug printing
    g.debug = 1
if 1:  # Utility

    def Debug(msg, **kw):
        if g.debug:
            print(f"{t('cyn')}", end="")
            print(msg, **kw)
            t.out()

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file1 file2
          Print hex dumps of the differences between two binary files.
          Returns 0 if files are identical, 1 if not.
        Options:
            -%      Print ASCII graphical summary indexed by percentage
                    through the files
            -q      Do not print differences, just return status
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-%"] = False  # ASCII graphical summary
        d["-q"] = False  # Only return status
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "%ad:h", ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug

                debug.SetDebugger()
        if len(args) != 2:
            Usage()
        return args


if 1:  # Classes

    class Diff:
        def __init__(self, start):
            assert ii(start, int)
            self._start = self._end = start

        def inc(self):
            self._end += 1

        @property
        def start(self):
            return self._start

        @property
        def end(self):
            return self._end

        def __str__(self):
            return f"Diff({self.start}, {self.end})"

        def __repr__(self):
            return str(self)


if 1:  # Core functionality

    def Initialize(file1, file2):
        "Set up our variables"
        g.path1, g.path2 = P(file1), P(file2)
        # The files must exist on the file system
        if not g.path1.is_file():
            raise ValueError(f"{file1!r} doesn't point to a file")
        if not g.path1.is_file():
            raise ValueError(f"{file2!r} doesn't point to a file")
        # Get the file sizes
        g.size1 = g.path1.stat().st_size
        g.size2 = g.path2.stat().st_size
        if not g.size1:
            raise ValueError(f"{file1!r} size is 0")
        if not g.size2:
            raise ValueError(f"{file2!r} size is 0")
        # Get number of bytes that can be compared
        g.size = min(g.size1, g.size2)
        # Open the streams
        g.stream1 = g.path1.open("rb")
        g.stream2 = g.path2.open("rb")

    def ReadBlock():
        """Read a block into both buffers.  Return the smaller of the number of
        bytes read.  Return 0 when one of the streams is at EOF.
        """

        def IsEOF(stream):
            "Return True if stream is at EOF"
            curr_position = stream.tell()
            stream.seek(0, 2)  # Go to EOF
            eof_position = stream.tell()
            # Go back to starting position
            stream.seek(curr_position)
            return curr_position == eof_position

        if IsEOF(g.stream1) or IsEOF(g.stream2):
            g.buf1 = g.buf2 = None
            return 0
        g.buf1 = g.stream1.read(g.block_size)
        g.buf2 = g.stream2.read(g.block_size)
        # Trim buffers to be the same size
        n1, n2 = len(g.buf1), len(g.buf2)
        n = min(n1, n2)
        g.buf1 = g.buf1[:n]
        g.buf2 = g.buf2[:n]
        return n

    def AnalyzeBlock(n):
        """n is the size of the next block of bytes to compare.  Compare
        each byte in the buffers and set the state.
        """
        # Logical checks
        Assert(n)
        Assert(g.buf1 is not None and g.buf2 is not None)
        Assert(len(g.buf1) == len(g.buf2) == n)
        if g.state != g.start:
            Assert(g.state in (g.eq, g.ne))
        # Analyze the block
        for i in range(n):
            g.offset += 1
            Assert(g.offset <= g.size)
            g.previous_state = g.state
            g.state = g.eq if g.buf1[i] == g.buf2[i] else g.ne
            if g.previous_state != g.state and g.state == g.ne:
                # Start a new Diff object
                g.diffs.append(Diff(g.offset))
            elif g.state == g.ne:
                # Increment Diff object's count
                g.diffs[-1].inc()

    def Dump():
        "Debug dump of g.diffs"
        for i in g.diffs:
            Debug(i)

    def PrintReport():
        for i in g.diffs:
            offset, length = i.start, i.end - i.start + 1
            # hexdump stream 1
            g.stream1.seek(offset)
            if 0:
                hexdump(g.stream1, offset=offset, length=length, out=sys.stdout)
            else:
                hexdump(g.stream1, offset=offset, n=length, out=sys.stdout)
            # hexdump stream 2
            g.stream2.seek(offset)
            if 0:
                hexdump(g.stream2, offset=offset, length=length, out=sys.stdout)
            else:
                hexdump(g.stream2, offset=offset, n=length, out=sys.stdout)


if __name__ == "__main__":
    d = {}  # Options dictionary
    file1, file2 = ParseCommandLine(d)
    Initialize(file1, file2)
    while True:
        n = ReadBlock()
        if not n:
            break
        AnalyzeBlock(n)
    Dump()
    PrintReport()

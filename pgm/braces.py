'''
'''
_pgminfo = '''
<oo desc
    Script to locate unmatched braces 
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo oo>
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
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        # The following dict keeps track of character pairs and their Char instance
        g.char_pairs = {}
        ii = isinstance
if 1:   # Classes
    class Char:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            Assert(len(start) == 1 and len(end) == 1)
            # Keep track of positions where characters were found
            self.start_locations = []
            self.end_locations = []
            # 'Register' with the character pair dictionary
            if self.start in g.char_pairs:
                Error(f"{self.start!r} already in g.char_pairs")
            if self.end in g.char_pairs:
                Error(f"{self.end!r} already in g.char_pairs")
            g.char_pairs[self.start] = self
            g.char_pairs[self.end] = self
        def __bool__(self):
            'Return True if character pairs match, False otherwise'
            return len(self.start_locations) == len(self.end_locations)
        def found(self, character, offset, linenum):
            'If character is found, log its offset and line number'
            if character == self.start:
                self.start_locations.append((offset, linenum))
            elif character == self.end:
                self.end_locations.append((offset, linenum))
            else:
                raise ValueError(f"{character!r} not tracked by this class")

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
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Examine files for unmatched pairs of characters.  If no files are given, input
          is taken from stdin.
        Options:
            -C s    Add set of characters s to character pairs
            -c s    Define the character pairs: '()[]{{}}' is the default
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = "()[]{}"     # Character pairs
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "Cch") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-C":
                if not len(a) or not (len(a) % 2):
                    Error("-C option requires an even number of characters")
            elif o == "-c":
                if not len(a) or not (len(a) % 2):
                    Error("-c option requires an even number of characters")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    '''

    Processing algorithm

    The character pairs are kept track of by the dictionary g.char_pairs; the character
    is the key and the character's associated Char instance is the value.

    Each character of the input file is examined to see if it is in g.char_pairs.  If it
    is, the character, offset, and line number are passed to the Char instance for logging.

    '''
    def Process(s, filename):
        'Process the string s contents of the indicated file'
        linenum = 0        # Line number counter (0-based)
        for offset, char in enumerate(s):
            if char == "\n":
                linenum += 1
            if char in g.char_pairs:
                Char_instance = g.char_pairs[char]
                Char_instance.found(char, offset, linenum)
        breakpoint() #xx

        # Identify pair mismatches 
        bad = set()
        for item in g.char_pairs:
            if not item:
                bad.add(item)
        if bad:
            Report(s, filename, bad)
    def Report(s, filename, bad):
        '''Print report.  s is file's string and bad is the Char instances that don't
        match.
        '''
        breakpoint() #xx 

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if files:
        for file in files:
            Process(open(file).read(), file)

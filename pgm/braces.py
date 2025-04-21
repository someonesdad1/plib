'''
    
Processing algorithm
    - The character pairs are kept track of by the dictionary g.char_pairs; the
      character is the key and the character's associated Char instance is the value.
    - Each character of the input file is examined to see if it is in g.char_pairs.  If
      it is, the character, offset, and line number are passed to the Char instance for
      logging.
     
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
        g.dbg = True
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
        def __str__(self):
            return f"Char({self.start}{self.end})"
        def __repr__(self):
            return f"Char(\n  {self.start_locations}\n  {self.end_locations}\n)"
        def __bool__(self):
            "Return True if character pairs don't match, False otherwise"
            return len(self.start_locations) != len(self.end_locations)
        def found(self, character, offset, linenum, column):
            'If character is found, log its offset, line number and column number'
            if character == self.start:
                self.start_locations.append((offset, linenum, column))
            elif character == self.end:
                self.end_locations.append((offset, linenum, column))
            else:
                raise ValueError(f"{character!r} not tracked by this class")
if 1:   # Utility
    def GetColors():
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.nomatch = t.yell
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
          Examine files for unmatched pairs of characters.  If no files are given, use
          -- for stdin.
        Options:
            -C s    Add set of characters s to character pairs
            -c s    Define the character pairs: '()[]{{}}' is the default
            -p      Print the line(s) with mismatches; color highlight the problem
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = "()[]{}"     # Character pairs
        d["-p"] = False        # Print the offending character in its line
        if len(sys.argv) < 2:
            Usage()
        GetColors()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "C:c:hp") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("p"):
                d[o] = not d[o]
                Dbg(f"{o!r} option used")
            elif o == "-C":
                if not len(a) or (len(a) % 2):
                    Error("-C option requires an even number of characters")
                Dbg(f"-C option:  {a!r}")
                d["-c"] += a
            elif o == "-c":
                if not len(a) or (len(a) % 2):
                    Error("-c option requires an even number of characters")
                Dbg(f"-c option:  {a!r}")
                d[o] = a
            elif o == "-h":
                Usage()
        RegisterCharacterPairs(d["-c"])
        return args
if 1:   # Core functionality
    def RegisterCharacterPairs(pairs):
        'pairs is a string of character pairs'
        Assert(pairs and (len(pairs) % 2 == 0))
        for i in range(0, len(pairs), 2):
            start, end = pairs[i], pairs[i + 1]
            Char(start, end)
    def Process(s, filename):
        'Process the string s contents of the indicated file'
        linenum = 0         # Line number counter (0-based)
        last_newline = 0    # Offset of last newline
        # offset is character count into text file
        for offset, char in enumerate(s):
            if char == "\n":
                linenum += 1
                last_newline = offset
            if char in g.char_pairs:
                Char_instance = g.char_pairs[char]
                column = offset - last_newline
                Char_instance.found(char, offset, linenum, column)
        if 0:
            for i in g.char_pairs:
                item = g.char_pairs[i]
                print(item)
                print(item.start_locations)
                print(item.end_locations)
                print()
            exit()
        # Identify pair mismatches 
        bad = set()
        for item in g.char_pairs:
            char = g.char_pairs[item]
            if char:
                bad.add(char)
        if bad:
            Report(s, filename, bad)
    def Report(s, filename, bad):
        '''Print report.  s is file's string and bad is the Char instances that don't
        match.
        '''
        for item in bad:
            start_locations = item.start_locations
            end_locations = item.end_locations
            if len(start_locations) > len(end_locations):
                offset, linenum, column = start_locations[0]
                char = item.start
            else:
                offset, linenum, column = end_locations[-1]
                char = item.end
            print(f"{filename}[{linenum + 1}:{column}]:  {char!r} "
                   "is missing matching character", end="")
            if d["-p"]:
                print(":")
                # Get the string for the whole line
                u = s.split("\n")[linenum]
                # Decorate the mismatched character in color
                print(f"  {u[:column - 1]}", end="")
                print(f"{t.nomatch}{u[column - 1:column]}{t.N}", end="")
                print(f"{u[column:]}")
            else:
                print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if files:
        for file in files:
            Process(open(file).read(), file)

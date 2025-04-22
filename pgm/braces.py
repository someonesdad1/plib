'''

Todo
    - Change architecture:  no exception for parity error.  Focus on getting test data
      needed and adapt Report() to use that information.  Eliminate -p option unless
      it remains easy.
        - Goal is to quickly locate the source of the error.  Since this will be a user
          with an editor the most, the line/col numbers are the most important.
    
Definitions
    - A brace pair is a pair of characters (a, b) defined where a is the opening
      character and b is the closing character.
    - Parity is a number associated with each defined character.  a's parity is +1 and
      b's parity is -1.
    - Parity sum is the sum of each brace pair's parity values over the whole file.
      For a brace pair to be declared OK, the parity sum must be zero at the end of the
      file.
    - The parity sum at any point in the file must be >= 0.  If the sum is negative, it
      is considered an error condition.

Processing algorithm
    - The character pairs are kept track of by the dictionary g.char_pairs; the
      character is the key and the character's associated Char instance is the value.
    - Each character of the input file is examined to see if it is in g.char_pairs.  If
      it is, the character, offset, and line number are passed to the Char instance for
      logging.

Test cases to consider/address:
    - OK cases
        - '{}', '{{}}', etc.
    - Mismatched
        - '{'       offset 0
        - '}'       offset 0
        - '{{}'     offset 0
        - '{}}'     offset 2
        - '}{}'     offset 0
        - '}}{{'    offset 0

     
'''
_pgminfo = '''
<oo desc
    Script to locate unmatched brace characters (defaults to '{}', '()', and '[]'
    pairs).  Correct forms are brace occurrences like '{}', '{{}}', etc., with other
    intervening characters.  Incorrect forms are things like '{{}', '}{', etc.

oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test none oo>
<oo todo 

    - Define parity.  Use it to detect a syntax error quickly and exit at that point.
    - Tokenize python code and set all string content to space characters to maintain
      character offsets.  Then process for braces.  The tokenizing might have to be done
      as bytes, not strings.

        - 'python -m tokenize -e a.py' does the needed job, as it identifies { as
          LBRACE, ( as LPAR, [ as LSQB.

oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        import getopt
        import os
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        from stack import Stack
        pp = PP()   # Get pprint with current screen width
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = True
        g.test = False
        # The following dict keeps track of character pairs and their Char instance
        g.char_pairs = {}
        ii = isinstance
if 1:   # Classes
    class ParityError(Exception):
        pass
    class Char:
        def __init__(self, open, close):
            if not ii(open, str) and len(open) != 1:
                raise ValueError(f"open ({open!r}) needs to be a string of one character")
            if not ii(close, str) and len(close) != 1:
                raise ValueError(f"close ({close!r}) needs to be a string of one character")
            self.open = open
            self.close = close
            # Keep track of (offset, line, column)  where characters were found.
            # Parameters are all 0-based.
            self.locations = Stack()
            # 'Register' with the character pair dictionary
            if self.open in g.char_pairs:
                Error(f"{self.open!r} already in g.char_pairs")
            if self.close in g.char_pairs:
                Error(f"{self.close!r} already in g.char_pairs")
            g.char_pairs[self.open] = self
            g.char_pairs[self.close] = self
        def __str__(self):
            return f"Char({self.open}{self.close}<{self.locations}>)"
        def __repr__(self):
            return f"Char({self.open}{self.close}<{self.locations}>)"
        def __bool__(self):
            "Return True if character pairs don't match, False otherwise"
            parity, st = 0, self.locations.copy()
            while st:
                character, offset, linenum, column = st.pop()
                if character == self.open:
                    parity += 1
                elif character == self.close:
                    parity -= 1
                else:
                    raise RuntimeError(f"{character!r} is unexpected")
            return parity == 0
        def found(self, character, offset, linenum, column):
            '''Log the occurrence of an open or close character.  
                offset0b    0-based character offset into the file
                linenum     0-based line number the character is on
                column      0-based column number in this line
            '''
            self.locations.push((character, offset, linenum, column))
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
          Examine files for unmatched pairs of characters.  If no files are given, the
          script will use stdin for input.
        Options:
            -C s    Add set of characters s to character pairs
            -c s    Define the character pairs: '()[]{{}}' is the default
            -p      Print the line(s) with mismatches; color highlight the problem
            -t      Run self tests
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = "()[]{}"     # Character pairs
        d["-p"] = False        # Print the offending character in its line
        d["-t"] = False        # Run self tests
        GetColors()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "C:c:hpt") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("pt"):
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
        if d["-t"]:
            g.test = True
            SelfTests()
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
        # linenum, offset, last_newline, and column are all 0-based
        linenum = 0
        last_newline = 0
        parity_errors = []
        for offset, char in enumerate(s):
            if char == "\n":
                linenum += 1
                last_newline = offset
            if char in g.char_pairs:
                Char_instance = g.char_pairs[char]
                column = offset - last_newline
                Char_instance.found(char, offset, linenum, column)
        # Now the Char instances contain a record of all the braces found in the file.
        # Suppose the input was s = "{{}".  
        pp(g.char_pairs)
        exit()

    def Report(s, filename, pair_mismatches, parity_errors):
        '''Print report.  s is file's string, pair_mismatches is a set of mismatched
        pairs, and parity_errors is a list of parity errors.
        '''
        for item in pair_mismatches:
            open_locations = item.open_locations
            close_locations = item.close_locations
            if len(open_locations) > len(close_locations):
                offset, linenum, column = open_locations[0]
                char = item.open
            else:
                offset, linenum, column = close_locations[-1]
                char = item.close
            print(f"{filename}[{linenum + 1}:{column + 1}]:  {char!r} "
                   "is missing matching character")
        for item in parity_errors:
            print(item)
if 1:   # Self tests
    def EmptyFile():
         # Empty file should also be successful
         pair_mismatches, parity_errors = Process("", "")
         Assert(not pair_mismatches and not parity_errors)
         # So should be a file with no braces in it
         pair_mismatches, parity_errors = Process("abc\ndef", "")
         Assert(not pair_mismatches and not parity_errors)
    def PairMismatch():
         for s in ("(()", "[[]", "{{}"):
            p, _ = Process(s, "")
            breakpoint() #xx 
            c = p.pop()
            Assert(c.open_locations == [(0, 0, 0), (1, 0, 1)])
            Assert(c.close_locations == [(3, 1, 1)])
    def ParityErrors():
         for s in ("())", "[]]", "{}}"):
            _, p = Process(s, "")
    def SelfTests():
        EmptyFile()
        PairMismatch()
        ParityErrors()
        exit(0)
    if 0:
        SelfTests()

if 1:
    C = Char("{", "}")
    s = "{{}"
    Process(s, "")
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if not files:
        s = sys.stdin.read()
        Process(s, "<stdin>")
    else:
        for file in files:
            Process(open(file).read(), file)

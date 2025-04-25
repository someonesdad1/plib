'''
    
Todo
    - Change architecture:  no exception for parity error.  Focus on getting test data
      needed and adapt Report() to use that information.  Eliminate -p option unless it
      remains easy.
        - Goal is to quickly locate the source of the error.  Since this will be a user
          with an editor the most, the line/col numbers are the most important.
    
Definitions
    - A brace pair is a pair of characters (a, b) defined where a is the opening
      character and b is the closing character.
    - Parity is a number associated with each defined character.  a's parity is +1 and
      b's parity is -1.
    - Parity sum is the sum of each brace pair's parity values over the whole file.  For
      a brace pair to be declared OK, the parity sum must be zero at the end of the
      file.
    - The parity sum at any point in the file must be >= 0.  If the sum is negative, it
      is considered an error condition.
    
Processing algorithm
    - The character pairs are kept track of by the dictionary g.char_pairs; the
      character is the key and the character's associated Char instance is the value.
    - Each character of the input file is examined to see if it is in g.char_pairs.  If
      it is, the character, offset, and line number are passed to the Char instance for
      logging.
    
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
    
    - Also make work for bytes instead of strings
    - Tokenize python code and set all string content to space characters to maintain
      character offsets.  Then process for braces.  The tokenizing might have to be done
      as bytes, not strings.
    
        - 'python -m tokenize -e a.py' does the needed job, as it identifies { as
          LBRACE, ( as LPAR, [ as LSQB.
    
oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        import getopt
        import os
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from lwtest import Assert, run
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False   # If true, print debugging messages
        ii = isinstance
if 1:   # Classes
    class Char:
        '''Container for opening and closing brace pairs.  Each occurrence in a file
        will result in an entry being added to this container's deque instance used to
        keep a record of where each character was.
        
        When starting to process a new file, call the clear() method of any existing
        Char instance to clear all the instance's location data.  Set the file property
        if you wish (it's a string to keep track of what's being processed, but not used
        internally).

        To start over and delete any Char instances, call the initialize() method.
        '''
        opening = []    # Keeps track of opening brace-type characters
        closing = []    # Keeps track of closing brace-type characters
        instances = {}  # Keeps track of Char instances (indexed by opening characters)
        string = None   # Keep a reference to the processed string
        def __init__(self, open, close):
            if not ii(open, str) and len(open) != 1:
                raise ValueError(f"open ({open!r}) needs to be a string of one character")
            if not ii(close, str) and len(close) != 1:
                raise ValueError(f"close ({close!r}) needs to be a string of one character")
            self._file = ""
            self.open = open
            self.close = close
            # Put these character pairs in g.char and g.char_match
            Char.opening.append(self.open)
            Char.closing.append(self.close)
            # Keep track of (char, offset, line, column)  where characters were found.
            # Parameters are all 0-based.
            self.locations = deque()
            # 'Register' with the character pair dictionary
            if self.open in Char.instances:
                Error(f"{self.open!r} already in Char.instances")
            Char.instances[self.open] = self
        def initialize(self):
            'Clear all class variable information to e.g. start over'
            Char.opening = []
            Char.closing = []
            Char.instances = {}
            Char.string = None
        def clear(self):
            'Reset self.locations to empty for each instance in Char.instances'
            for char in Char.instances:
                instance = Char.instances[char]
                instance.locations.clear()
            Char.string = None
        def _str(self):
            return f"Char({self.open}{self.close}<{self.locations}>)"
        def __str__(self):
            return self._str()
        def __repr__(self):
            return self._str()
        def __bool__(self):
            "Return True if character pairs don't properly match"
            return self.locate_mismatch() is not None
        def found(self, character, offset, linenum, column):
            '''Log the occurrence of an open or close character.  
                offset      0-based character offset into the file
                linenum     0-based line number the character is on
                column      0-based column number in this line
            The character is appended to the end of the deque; when the file is
            processed, the characters and their locations are in left-to-right order of
            how they were encountered in the file.
            '''
            self.locations.append((character, offset, linenum, column))
        def locate_mismatches(self):
            '''Return a list of lists of (status, (character, offset, linenum, column))
            elements of the brace-type characters that are mismatched.  None is returned
            if there are no mismatches.
            '''
            mismatches = []
            for c in Char.instances:
                instance = Char.instances[c]
                result = instance.locate_mismatch()
                if result is not None:
                    mismatches.append(result)
            return mismatches if mismatches else None
        def locate_mismatch(self):
            '''Return the (status, (character, offset, linenum, column)) element
            of the brace-type characters that is mismatched for this instance.  None is
            returned if there is no mismatch.
            
            status is a string that indicates the problem, e.g.:
                error1:  "{ character with no matching } character"
                error2:  "} character with no matching { character"

            The algorithm uses the cumulative sum of parities.  The parity of the
            opening character is +1 and the parity of the closing character is -1.  The
            following three strings demonstrate the algorithm with parity sums as lists:

                                                    csum =
                    Expr    List of parities    Cumulative sum   Result
                1.  "{{}}"  [+1, +1, -1, -1]    [1, 2, 1, 0]     Correct expression
                2.  "{{}"   [+1, +1, -1]        [1, 2, 1]        error1
                3.  "}{}"   [-1, +1, -1]        [-1, 0, -1]      error2

            '''
            error1 = f"{self.open} character with no matching {self.close} character"
            error2 = f"{self.close} character with no matching {self.open} character"
            Dbg(f"Char.locations = {self.locations}")
            if 1:   # New algorithm
                if not self.locations:  # No open/close characters were found
                    return None
                # Calculate cumulative sum of parities
                mysum, csum = 0, []
                for char, _, _, _ in self.locations:
                    if char == self.open:
                        mysum += 1
                    else:
                        mysum -= 1
                    csum.append(mysum)
                # Look for first negative element (has to be -1)
                try:
                    index = csum.index(-1)      # index is location of error2
                    # There's an unmatched self.close character
                    return (error2, self.locations[index])
                except ValueError:
                    pass
                # See if last element is 0, implying no mismatch
                if not csum[-1]:
                    return None
                else:
                    # There's an unmatched self.open character
                    if len(csum) == 1:  # Only one element
                        return (error1, self.locations[0])
                    # Look for largest cumulative sum value from the end of the list
                    last_element = 0
                    while csum:
                        elem = csum.pop()   # List's pop() removes rightmost element
                        if elem > last_element:
                            last_element = elem
                        else:
                            break
                    # Get index of largest cumulative sum value.  The remaining size of
                    # csum tells us the index of the largest element.
                    index = len(csum) + 1
                    return (error1, self.locations[index])
            else:   # Old algorithm
                parity, st, parityseq = 0, self.locations.copy(), []
                # parityseq will be list of (parity, item) where item is the (character, offset,
                # linenum, column) entry.
                while st:
                    entry = st.popleft()
                    if entry[0] == self.open:
                        parity += 1
                    elif entry[0] == self.close:
                        parity -= 1
                    else:
                        raise RuntimeError(f"Program bug:  {entry[0]!r} is unexpected")
                    parityseq.append((parity, entry))
                if not parityseq:
                    Dbg("Analyzed string is empty")
                    return None
                if 1:   # Show parity sequence if debugging
                    Dbg("Parity sequence: ", end="")
                    spc = Dbg.indent
                    Dbg.indent = ""
                    for item in parityseq:
                        Dbg(item[0], end=" ")
                    Dbg()
                    Dbg.indent = spc
                # Look first for a negative parity
                for parity, item in parityseq:
                    if parity < 0:
                        Dbg(f"Negative parity for item {item}")
                        return no_open, item     # Condition #2 violated
                # If ending parity is zero, there's no mismatch
                if not parityseq[-1][0]:
                    Dbg("Parity is OK")
                    return None
                Assert(parityseq[-1][0] > 0)
                # Ending parity was nonzero.  Offending character is the one just after it
                # was last zero.
                st = self.locations.copy()
                last_entry = None
                while st:
                    entry = st.pop()    # Remove last entry on the right
                    parity = entry[0]
                    if not parity :
                        # This is rightmost brace where parity was OK
                        if last_entry is None:
                            raise RuntimeError(f"Program bug:  unexpected parity of 0")
                        Dbg(f"Offending char = {last_entry}")
                        return no_close, last_entry
                    else:
                        last_entry = entry
                # Had no match, so offending character had to be first entry
                Dbg(f"Offending char = {entry}")
                if entry[0] == self.open:
                    return no_close, entry
                else:
                    return no_open, entry
        @property
        def file(self):
            return self._file
        @file.setter
        def file(self, filename):
            self._file = filename
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
            print(f"{Dbg.indent}{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    Dbg.indent = ""
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Manpage():
        print(dedent('''
        
        This script helps find brace-type character errors in programming expressions.
        An example is the following python expression:
        
            hdr = [f"{C('n')}", f"{C('d')}", f"{C('s'}", f"{C('A')}", f"{C('p')}"]
        
        which is missing a ')' character.
        
        Most of the time your compiler/interpreter or editor can do such things, but
        there are situations when they may fail you.  An example is a large shell script
        written without functions, say thousands of lines long.  A missing brace-type
        character ('(', '[', or '{' or its matching character) can lead to head
        scratching searches for where the problem is.  Older C compilers could have a
        similar issue pointing out where a missing brace '}' was.
        
        This script looks at each character of a file and if it is in the set of
        recognized "brace-type" character pairs (defined by the -c and -C options), its
        location is logged.  At the end of processing the file, these logged locations
        are examined to find pairs of brace-type characters that are mismatched.  For
        example, the string '{}' has matched braces, but '{{}' does not, nor do '{',
        '{', or '}{'.  
        
        '''))
        exit(0)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Examine files for unmatched pairs of characters.  If no files are given, the
          script will use stdin for input.
        Options:
            -C s    Add set of characters s to character pairs
            -c s    Define the character pairs: '()[]{{}}' is the default
            -d      Print debugging messages
            -t      Run self tests
            -H      Print a manpage
            -h      Print the usage message
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = "()[]{}"     # Character pairs
        d["-d"] = False        # Debugging printing
        #d["-p"] = False        # Print the offending character in its line
        d["-t"] = False        # Run self tests
        GetColors()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "C:c:dHht") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dt"):
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
            elif o == "-H":
                Manpage()
            elif o == "-h":
                Usage()
        if d["-d"]:     # Debugging printing
            g.dbg = True
            GetColors()
        if d["-t"]:     # Run self-tests
            SelfTests.c = Char("{", "}")
            exit(run(globals(), halt=True)[0])
        RegisterCharacterPairs(d["-c"])
        return args
if 1:   # Self tests
    def TestPassing():
        for s in ["", "{}", "{{}}"]:
            Process(s)
            Assert(SelfTests.c.locate_mismatch() is None)
    def TestFailures():
        m1 = "{ character with no matching } character"
        m2 = "} character with no matching { character"
        #
        Process("{")
        mm = SelfTests.c.locate_mismatch()
        Assert(mm[0] == m1)
        Assert(mm[1] == ('{', 0, 0, 0))
        #
        Process("}")
        mm = SelfTests.c.locate_mismatch()
        Assert(mm[0] == m2)
        Assert(mm[1] == ('}', 0, 0, 0))
        #
        Process("{{}")
        mm = SelfTests.c.locate_mismatch()
        Assert(mm[0] == m1)
        Assert(mm[1] == ('{', 1, 0, 1))
        #
        Process("{}}")
        mm = SelfTests.c.locate_mismatch()
        Assert(mm[0] == m2)
        Assert(mm[1] == ('}', 2, 0, 2))
        #
        Process("}{}")
        mm = SelfTests.c.locate_mismatch()
        Assert(mm[0] == m2)
        Assert(mm[1] == ('}', 0, 0, 0))
        #
        Process("}}{{")
        mm = SelfTests.c.locate_mismatch()
        Assert(mm[0] == m2)
        Assert(mm[1] == ('}', 0, 0, 0))
    def SelfTests():
        pass
if 1:   # Core functionality
    def RegisterCharacterPairs(pairs):
        'pairs is a string of character pairs'
        Assert(pairs and (len(pairs) % 2 == 0))
        for i in range(0, len(pairs), 2):
            start, end = pairs[i], pairs[i + 1]
            Char(start, end)
    def Report(s, file):
        "Print report.  s is file's string and file is file's name."
        # Get any Char instance
        c = list(Char.instances)[0]
        item = Char.instances[c]
        mismatches = item.locate_mismatches()
        if mismatches is None:
            Dbg(f"No mismatches in {file}")
            return
        for mismatch in mismatches:
            msg = mismatch[0]
            char, offset, linenum, column = mismatch[1]
            print(f"{file}[{linenum + 1}:{column + 1}]:  {msg}")
    def Process(s, file=""):
        'Process the string s contents of the indicated file'
        Dbg(f"Processing file {file!r}")
        # Clear the Char instances of any prior information
        if not Char.instances:
            raise ValueError("No registered Char instances")
        for char in Char.instances:
            instance = Char.instances[char]
            instance.clear()
            break   # Only need to call this for one instance and it clears all of them
        instance.file = file
        # linenum, offset, last_newline, and column are all 0-based
        linenum = 0
        column = 0
        last_newline = 0
        # Look at each character c and its offset.  If c is one of the primary
        # brace-type characters (in g.char) or its matching brace-type character, log
        # its occurrence in the appropriate Char instance.
        for offset, c in enumerate(s):
            if c == "\n":
                linenum += 1
                last_newline = offset
            if c in Char.opening or c in Char.closing:
                if c in Char.opening:
                    Char_instance = Char.instances[c]
                else:
                    # Get matching opening character
                    index = Char.closing.index(c)
                    Char_instance = Char.instances[Char.opening[index]]
                # Calculating column number needs a 1 subtracted except for first line
                column = offset - last_newline - (linenum > 0)
                Char_instance.found(c, offset, linenum, column)
        # Now the Char instances contain a record of all the braces found in the file.
        # Suppose the input was s = "{{}".  Then the Char.instances dictionary will be
        # {'{': Char({}<Stack([('{', 0, 0, 0), ('{', 1, 0, 1), ('}', 2, 0, 2)])>)},
        # showing the location of each 'brace' character.

if 0:   
    s = "()("
    t.print(f"{t.ornl}file = {s!r}")
    g.dbg = True
    GetColors()
    c = Char("(", ")")
    Process(s, "")
    print(c.locate_mismatch())
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if not files:
        s, file = sys.stdin.read(), "<stdin>"
        Process(s, file)
        Report(s, file)
    else:
        for file in files:
            s = open(file).read()
            Process(s, file)
            Report(s, file)

_pgminfo = '''
    <oo desc

        Tokenizer() function for tokenizing text.  The basic use case for this function
        is to split ASCII text into words, whitespace, linefeeds, digits, punctuation,
        and other characters.  PrintTokens() is useful with colorizing to show how a
        text file has been tokenized and it will also number the lines if desired.  On
        my older computer, the tokenizing rate is about 100-500 tokens/ms.  The higher
        values are for plain text ASCII files and the lower values for programming
        source code files.  The tokens are string instances that give the token type via
        their class and include the line number, column number and offset of the token
        in the string (all of these are 0-based integers).

    oo>
    <oo cr Copyright © 2025 Don Peterson oo>
    <oo license
        Licensed under the Open Software License version 3.0.
        See http://opensource.org/licenses/OSL-3.0.
    oo>
    <oo cat utility oo>
    <oo test -t oo>
    <oo todo oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        from collections import defaultdict
        from enum import Enum
        import getopt
        import io
        import itertools
        import math
        import operator
        import string
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from get import GetLines
        from lwtest import Assert, run
        from dpprint import PP
        import timer
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        __all__ = '''
            Tokenizer PrintTokens 
            wrd dig nln wht pnc oth
        '''.split()
        # Unicode symbols for whitespace characters
        g.ws = {"\t": "␉", "\r": "␍", "\x0b": "␋", "\x0c": "␌"}
        # Colors
        t.wrd = t.wht
        t.dig = t.grnl
        t.nln = t.lip
        t.ws = t("whtl", "blul")
        t.pnc = t.purl
        t.oth = t("blk", "yell")
        t.linenum = t("gry", "#000030")
if 1:   # Utility
    def out(*s):
        'Print the components to stdout with no linefeeds'
        for i in s:
            print(i, end="")
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
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Tokenize the indicated files and print them in a colorized fashion to stdout.
          This provides a demonstration of the Tokenizer() functions abilities.  Use "-"
          to read from stdin.
        Options:
            -T      Print tokenizing timing information for each file
            -s      Demonstrate a spell checking task
            -t      Run self-tests
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-s"] = False     # Demonstrate spell checking
        d["-T"] = False     # Tokenizing timing
        d["-t"] = False     # Run self-tests
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hsTt") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("sTt"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        if d["-t"]:
            exit(run(globals(), halt=True)[0])
        return args
    def MeasureTiming(file):
        'Print execution time and tokens/s tokenizing rate'
        s = open(file).read()
        with timer.Timer() as tm:
            o = Tokenizer(s)
        time = tm.et
        tokens = len(o)
        t.print(f"{t.ornl}File = {file!r}")
        print(f"  Time to tokenize = {time.engsi}s")
        print(f"  Number of tokens = {tokens}")
        print(f"  File size = {len(s)} UTF-8 characters (not bytes)")
        print(f"  Tokenizing rate = {tokens/time} tokens/s")
    def SpellCheck(file):
        'Print misspelled words in file with their location'
        words = set(i.lower() for i in GetLines("/words/words.default", nonl=True))
        tokens = Tokenizer(open(file).read().lower())
        misspelled = defaultdict(list)
        for word in tokens:
            if not ii(word, wrd):
                continue
            if word not in words:
                misspelled[word].append(f"{word.linenum + 1}:{word.column + 1}")
        if misspelled:
            t.print(f"{t.ornl}{file}")
        # Get maximum word length so locations can be lined up
        w = 0
        for word in misspelled:
            w = max(w, len(word))
        w = min(w, 20)  # Limit it to 20 characters maximum
        for word in sorted(misspelled):
            print(f"  {word:{w}s}  {' '.join(misspelled[word])}")

if 1:   # PrintTokens
    def PrintTokens(o, colorize=False, linenum=False):
        '''o is a sequence of tokens that is produced by Tokenizer().  Print them to
        stdout with their defined colorizing if colorize is True.  Include line numbers
        if linenum is True.
        '''
        if not o:
            return
        Assert(ii(o[0], tkn))
        w = math.ceil(math.log10(o[-1].linenum))   # Width for line numbers
        ntokens = len(o)
        for i, token in enumerate(o):
            if not i and linenum:
                if colorize:
                    print(f"{t.linenum}{1:{w}d}{t.n} ", end="")
                else:
                    print(f"{1:{w}d} ", end="")
            if ii(token, wrd):
                if colorize:
                    print(f"{t.wrd}{token}{t.n}", end="")
                else:
                    print(f"{token}", end="")
            elif ii(token, dig):
                if colorize:
                    print(f"{t.dig}{token}{t.n}", end="")
                else:
                    print(f"{token}", end="")
            elif ii(token, nln):
                if colorize:
                    print(f"{t.nln}␤{t.n}")
                    if i < ntokens - 1 and linenum:
                        next_token = o[i + 1]
                        print(f"{t.linenum}{next_token.line:{w}d}{t.n} ", end="")
                else:
                    print(f"␤")
                    if i < ntokens - 1 and linenum:
                        next_token = o[i + 1]
                        print(f"{next_token.line:{w}d} ", end="")
            elif ii(token, wht):
                # Whitespace is handled specially:  a space character is printed plain.
                # The other characters show their Unicode equivalent symbols and are
                # printed in red:  cr, ff, vt, ht
                for char in token:
                    if char == " ":
                        out(" ")
                    else:
                        if colorize:
                            out(f"{t.ws}{g.ws[char]}{t.n}")
                        else:
                            out(f"{g.ws[char]}")
            elif ii(token, pnc):
                if colorize:
                    print(f"{t.pnc}{token}{t.n}", end="")
                else:
                    print(f"{token}", end="")
            elif ii(token, oth):
                if colorize:
                    print(f"{t.oth}{token}{t.n}", end="")
                else:
                    print(f"{token}", end="")
            else:
                raise Exception("Bug:  unknown token type")
if 1:   # Testing functions
    def TestTokenizer():
        if 1:   # Empty string
            o = Tokenizer("")
            Assert(o == [])
        if 1:   # String with no newline
            o = Tokenizer("a1\b \t\f\r")
            Assert(o == ['a', '1', '\x08', ' \t\x0c\r'])
            Assert(type(o[0]) == wrd)
            Assert(type(o[1]) == dig)
            Assert(type(o[2]) == oth)
            Assert(type(o[3]) == wht)
        if 1:   # String with one newline
            o = Tokenizer("\n")
            Assert(o == ['\n'])
            o = Tokenizer("ab\n")
            Assert(o == ['ab', '\n'])
            o = Tokenizer("a\nb")
            Assert(o == ['a', '\n', 'b'])
        if 1:   # String with two newlines
            o = Tokenizer("\n\n")
            Assert(o == ['\n', '\n'])
            o = Tokenizer("a\nb\n")
            Assert(o == ['a', '\n', 'b', '\n'])
        if 1:   # General test case that has all types in it
            o = Tokenizer("a1.\x0c∞\n")
            Assert(o == ['a', '1', '.', '\x0c', '∞', '\n'])
            # Check types
            Assert(type(o[0]) == wrd)
            Assert(type(o[1]) == dig)
            Assert(type(o[2]) == pnc)
            Assert(type(o[3]) == wht)
            Assert(type(o[4]) == oth)
            Assert(type(o[5]) == nln)
            # Check linenum, column, offset
            # Element 0 is a 'a' wrd
            Assert(o[0].linenum == 0)
            Assert(o[0].column == 0)
            Assert(o[0].offset == 0)
            # Element 1 is a '1' dig
            Assert(o[1].linenum == 0)
            Assert(o[1].column == 1)
            Assert(o[1].offset == 1)
            # Element 2 is a '.' pnc
            Assert(o[2].linenum == 0)
            Assert(o[2].column == 2)
            Assert(o[2].offset == 2)
            # Element 3 is a formfeed pnc
            Assert(o[3].linenum == 0)
            Assert(o[3].column == 3)
            Assert(o[3].offset == 3)
            # Element 4 is a Unicode ∞ pnc
            Assert(o[4].linenum == 0)
            Assert(o[4].column == 4)
            Assert(o[4].offset == 4)
            # Element 5 is a '\n' nln
            Assert(o[5].linenum == 0)
            Assert(o[5].column == 5)
            Assert(o[5].offset == 5)
if 1:   # Classes to hold token types
    '''
    These classes are string types used to hold different token types by virtue of their
    type.  Each will contain the line number, column number, and offset of where the
    token starts in the original string.
    '''
    class tkn(str):
        'Base class for these strings'
        def __new__(cls, value):
            instance = super(tkn, cls).__new__(cls, value)
            # Positions of the start of this string in the original string
            instance.linenum = None
            instance.column = None
            instance.offset = None
            return instance
        @property
        def d(self):
            'Return the attributes in a string'
            return (f"{self}:  linenum = {self.linenum}, "
                    f"column = {self.column}, "
                    f"offset = {self.offset}")
    # The __iadd__ method lets us add a plain str type to the types below and get the
    # same type as the constructor called, making the code syntax a little simpler.
    class wrd(tkn):     # Words
        def __new__(cls, value):
            return super(wrd, cls).__new__(cls, value)
        def __iadd__(self, value):
            assert ii(value, wrd)
            return wrd(self + value)
    class dig(tkn):     # Digits
        def __new__(cls, value):
            return super(dig, cls).__new__(cls, value)
        def __iadd__(self, value):
            assert ii(value, dig)
            return dig(self + value)
    class nln(tkn):     # Single newlines
        def __new__(cls, value):
            return super(nln, cls).__new__(cls, value)
        def __iadd__(self, value):
            raise TypeError("Operation not allowed for newlines")
    class wht(tkn):     # Whitespace (less newline)
        def __new__(cls, value):
            return super(wht, cls).__new__(cls, value)
        def __iadd__(self, value):
            assert ii(value, wht)
            return wht(self + value)
    class pnc(tkn):     # Punctuation
        def __new__(cls, value):
            return super(pnc, cls).__new__(cls, value)
        def __iadd__(self, value):
            assert ii(value, pnc)
            return pnc(self + value)
    class oth(tkn):     # All other token characters
        def __new__(cls, value):
            return super(oth, cls).__new__(cls, value)
        def __iadd__(self, value):
            assert ii(value, oth)
            return oth(self + value)
if 1:   # Tokenizer
    TYP = Enum("TYP", "wrd dig nln wht pnc oth".split())
    def getcls(typ, s):
        'Return the string s as the indicated type (typ is a TYP enum)'
        assert ii(typ, TYP)
        if typ == TYP.wrd:
            return wrd(s)
        elif typ == TYP.dig:
            return dig(s)
        elif typ == TYP.nln:
            return nln(s)
        elif typ == TYP.wht:
            return wht(s)
        elif typ == TYP.pnc:
            return pnc(s)
        else:
            return oth(s)
    def gettyp(char):
        "Return the TYP enum for the character char's type"
        if char in Tokenizer.wrd:
            return TYP.wrd
        elif char in Tokenizer.dig:
            return TYP.dig
        elif char in Tokenizer.nln:
            return TYP.nln
        elif char in Tokenizer.wht:
            return TYP.wht
        elif char in Tokenizer.pnc:
            return TYP.pnc
        else:
            return TYP.oth
    def Finish(accum, o, linenum, column, offset):
        'Finish accumulation of the attributes and append to the list o'
        accum.linenum = linenum
        accum.column = column
        accum.offset = offset
        o.append(accum)
    def Tokenizer(s, diacritics=False):
        '''Return a list that contains all the characters of the string s in the derived
        string objects:
            wrd (a word)
            dig (digits)
            nln (a single newline)
            wht (whitespace)
            pnc (punctuation)
            oth (all other characters)
        that characterize the type of each token.
        
        Each of these token string types contain the line number and column number that
        it starts on in the original text string along with the offset of the string.
        Note all of these numbers are zero-based.
         
        The basic use case of this function is to tokenize UTF-8 encoded text into
        words, whitespace, and punctuation.  I use it in conjunction with a spell
        checker that gives me the line number and column number of misspelled words. 
        
        To use, you must store sets of characters in the following containers:
            Tokenizer.wrd    Characters in words
            Tokenizer.dig    Characters in numbers
            Tokenizer.wht    Characters interpreted as whitespace excluding the newline
            Tokenizer.pnc    Punctuation characters
            Tokenizer.oth    Empty set for other characters
        Tokenizer.nln is only allowed to contain a newline because the
        io.StringIO.readlines() method only splits on newlines.
        '''
        if not ii(s, str):
            raise TypeError("s must be a str instance")
        if not s:
            return []
        assert Tokenizer.nln == set("\n")   # We only split on newlines
        Tokenizer.wrd = Tokenizer.ascii
        if diacritics:
            Tokenizer.wrd.update(Tokenizer.diacritics)
        # Split s into a set of lines on the newlines.  Each line contains one ending
        # newline except possibly on the last line.
        lines = io.StringIO(s).readlines()
        # Get offset of each line:  offsets[n] is for lines[n + 1]
        offsets = list(itertools.accumulate([len(i) for i in lines], func=operator.add))
        o = [] # List of token instances to return
        # Process each line
        for linenum, line in enumerate(lines):
            if g.dbg:
                t.print(f"{t.cynl}line = {line!r} linenum = {linenum}")
            for column, char in enumerate(line):
                offset = column + offsets[linenum - 1] if linenum else column
                if g.dbg:
                    t.print(f"  {t.skyl}char = {char!r}, column = {column}, offset = {offset}")
                if not column:  # First character of line
                    if char == "\n":
                        # This character is the last character of the line and there's
                        # only one of them
                        accum = nln("\n")
                        Finish(accum, o, linenum, column, offset)
                        accum = None
                    else:
                        # Start a new accumulator string of the proper type
                        oldtyp = gettyp(char)
                        accum = getcls(oldtyp, char)
                else:  # Every character except the first character of the line
                    newtyp = gettyp(char)
                    if newtyp == oldtyp:
                        accum += type(accum)(char)
                    else:
                        n = len(accum)
                        if char == "\n":
                            Finish(accum, o, linenum, column - n, offset - n)
                            accum = nln("\n")
                            Finish(accum, o, linenum, column, offset)
                            accum = None
                        else:
                            Finish(accum, o, linenum, column - n, offset - n)
                            accum = getcls(newtyp, char)
                            oldtyp = newtyp
        else:
            if accum:
                Finish(accum, o, linenum, column, offset)
        # Check invariant:  our tokenizing algorithm is consistent if we can recreate the
        # original string from the list o.
        if ''.join(o) != s:
            raise Exception("Tokenizer() invariant failed:  ''.join(o) != s")
        return o
    # Set up default character types
    Tokenizer.ascii = set(string.ascii_letters)
    Tokenizer.diacritics = set('''
        æ Æ
        ąăāåäãâáà ĄĂĀÅÄÃÂÁÀ
        ß
        čċĉćç ČĊĈÇĆ
        đď ĐĎ
        ëêéèěęėĕē ËĚĘĖĔĒÊÉÈ
        ģĢġĠğĞĝĜ
        ħĦĥĤ
        ïîíìıįĭīĩ ÏÎÍÌİĮĬĪĨ
        ĵĴ
        ĸķĶ
        łŀľļĺ ŁĽĻĹĿ
        ñŋŉňņń ÑŊŇŅŃ
        øöõôóòðőŏō ØÖÕÔÓÒŎŐŌ
        þ Þ
        řŗŕ ŘŖŔ
        šşŝś ŠŞŜŚ
        ŧťţ ŦŤŢ
        üûúùųűůŭūũ ÜÛÚÙŲŰŮŬŪŨ
        ŵ Ŵ
        ÿýŷ ŸÝŶ
        žżź ŽŻŹ
    ''')
    Tokenizer.diacritics.discard(" ")
    Tokenizer.diacritics.discard("\n")
    Tokenizer.dig = set(string.digits)
    Tokenizer.nln = set("\n")   # Should only be the newline character
    Tokenizer.wht = set(string.whitespace)
    Tokenizer.wht.discard("\n")
    Tokenizer.pnc = set(string.punctuation)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        if d["-T"]:
            MeasureTiming(file)
        elif d["-s"]:
            SpellCheck(file)
        else:
            o = Tokenizer(sys.stdin.read() if file == "-" else open(file).read())
            PrintTokens(o, colorize=True)

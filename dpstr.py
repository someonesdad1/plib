r'''
String utilities
    Chop                Return a string chopped into equal parts
    CommonPrefix        Return a common prefix of a sequence of strings
    CommonSuffix        Return a common suffix of a sequence of strings
    CountLeadingSpaces  Return number of common leadings spaces in a multiline string
    Decorate            Make whitespace and control characters easier to see in a string
    Edit                Edit a set of files
    FilterStr           Return a function that removes characters from strings
    FilterSeqRegex      Return a sequence of strings filtered by regexes
    FindAll             Find all locations of a substring in a string
    FindFirstIn         Find first item in sequence in a given set
    FindLastIn          Find last item in sequence in a given set
    FindFirstNotIn      Find first item not in sequence in a given set
    FindLastNotIn       Find last item not in sequence in a given set
    FindDiff            Return where two strings first differ
    FindStrings         Find locations of a sequence of strings in a string
    FindSubstring       Return indexes of substring in string
    FindSymbol          Find a symbol in one or more python files
    GetChoice           Return choice from a set of choices (minimizes typing)
    GetStartingChars    Return starting characters of a string
    GetEndingChars      Return ending characters of a string
    GetTransFunc        Return a function that translates strings
    GetString           Return string from user that matches choices
    IgnoreFilter        Return a function which removes ignored strings
    IsASCII             Return True if string is all ASCII characters
    Keep                Return items in sequence that are in keep sequence
    KeepFilter          Returns a function that keeps a set of items in a sequence
    KeepOnlyLetters     Replace all non-word characters with spaces
    CountLeadingSpaces  Return the number of leading or trailing spaces in a string
    Len                 Length of string with ANSI escape sequences removed
    ListInColumns       Obsolete (use columnize.py)
    MatchCapitalization Match string capitalization
    MultipleReplace     Replace multiple patterns in a string
    PrepareMultilineString  Helper function to trim leading & trailing whitespace
    ReadData            Read data from a multiline string
    RegisteredOpen      Open file with its registered application
    Remove              Return items from sequence not in the remove sequence
    RemoveASCII         Remove all ASCII characters from a string
    RemoveComment       Remove '#.*$' from a string
    RemoveEndingChars   Remove ending characters from a string
    RemoveCharClass     Remove character classes from a string
    RemoveFilter        Functional form of Remove (it's a closure)
    RemoveStartingChars Remove starting characters from a string
    RemoveWhitespace    Remove whitespace from a string
    RmEsc               Remove ANSI escape strings from string arguments
    Scramble            Randomly shuffle words in a string
    soundex             Return 4-character soundex value for a string
    SoundSimilar        Return True if two strings sound similar
    SpellCheck          Spell check a sequence of words
    SplitOnNewlines     Split on \r, \n, or \r\n
    StringSplit         Pick out specified fields of a string
    Str                 String class whose len() ignores ANSI escape sequences
    TimeStr             Readable string for time() in s
    Tokenize            Return a list of tokens from tokenizing a string
    Trim                Remove characters from a string
    WordID              Return an ID string that is somewhat pronounceable
        
    Token naming conversions:
        cw2mc            Cap-words to mixed-case
        cw2us            Cap-words to underscore
        mc2cw            Mixed-case to cap-words
        mc2us            Mixed-case to underscore
        us2cw            Underscore to cap-words
        us2mc            Underscore to mixed-case
'''
if 1:   # Header
    _pgminfo = '''
        <oo gist ∞ String utilities oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ text oo>
        <oo test ∞ run oo>
        <oo todo ∞
        
            - ∞∞1 Missing tests for GetString, WordID
            - ∞∞1 Many of these functions can be made to work with bytes
            - Convert token naming conversions to a class
            - ∞∞3 Consider upper & lower keywords for Keep and Remove
            - ∞∞2 Many functions: divide docstring into multiple categories and then divide
              the code up into the same sections with 'if 1:    # Section' strings.
    
        oo>
    '''
    if 1:   # Standard imports
        import collections
        import fractions
        import functools
        import importlib
        import io
        import itertools
        import os
        import pathlib
        import random
        import re
        import string
        import struct
        import subprocess
        import sys
        import textwrap
        import time
        import typing as ty
    if 1:   # Custom imports
        import asciify
        import dpseq
        import dptypes
        import f
        import trm
        import wrap
        import wsl
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        g = dptypes.Constant()
        g.nl = "\n"
        g.cr = "\r"
        g.sp = " "
        try:
            with g:
                g.noflag = re.NOFLAG
        except Exception:
            with g:
                g.noflag = 0
    if 1:   # Type information
        T = ty.TypeVar("T")
        # AnyStr ensures that if you pass str, you get str; if bytes, you get bytes.
        AnyStr = ty.TypeVar("AnyStr", str, bytes)
        # SupportsWrite is an output Protocol that is usually sys.stdout, but can also
        # be an output file stream or hardware buffer.
        # ∞∞1 This needs work, as StringIO only fits the 'write(self, str, /) -> int'
        # pattern
        @ty.runtime_checkable
        class SupportsWrite(ty.Protocol):
            def write(self, s: str, /) -> int: ...
if 1:   # Classes
    class NameConvert:
        'Convert programming naming styles, "Python Cookbook" pg. 91'
        def cw2us(self, x: str) -> str:
            '''Cap-words to underscore:
            ALotOfFuss -> a_lot_of_fuss
            '''
            if not x:
                return x
            return re.sub(r"(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])", r"_\g<0>", x).lower()
        def cw2mc(self, x: str) -> str:
            '''Cap-words to mixed-case:
            ALotOfFuss -> aLotOfFuss
            '''
            if not x:
                return x
            return x[0].lower() + x[1:]
        def us2mc(self, x: str) -> str:
            '''Underscore to mixed-case:
            a_lot_of_fuss -> aLotOfFuss
            '''
            if not x:
                return x
            return re.sub(r"_([a-z])", lambda m: (m.group(1).upper()), x)
        def us2cw(self, x: str) -> str:
            '''Underscore to cap-words:
            a_lot_of_fuss -> ALotOfFuss
            '''
            if not x:
                return x
            s = self.us2mc(x)
            return s[0].upper() + s[1:]
        def mc2us(self, x: str) -> str:
            '''Mixed-case to underscore:
            aLotOfFuss -> a_lot_of_fuss
            '''
            if not x:
                return x
            return self.cw2us(x)
        def mc2cw(self, x: str) -> str:
            '''Mixed-case to cap-words:
            aLotOfFuss -> ALotOfFuss
            '''
            if not x:
                return x
            return x[0].upper() + x[1:]
    class Str(str):
        '''This is a str object except that its len() method ignores any ANSI
        escape sequences.  The basic use case is to allow embedded colorizing
        escape sequences in the string without the escape sequences contributing
        to the string's length.
        
        You can turn off this behavior by setting the .on attribute to False.
        '''
        __slots__ = ("on",)
        def __new__(cls, s):
            instance = super(cls, Str).__new__(cls, s)
            instance.on = True
            return instance
        def __len__(self):
            return Len(self) if bool(self.on) else super().__len__()
if 1:   # RegexpDecorate class
    class RegexpDecorate:
        '''Decorate regular expression matches with color
        
        You must initialize an instance with a trm.Trm instance.  If you don't, a
        default Trm instance will be used.
        
        The styles attribute is a dictionary that contains the styles to apply for each
        regexp's match (key is the compiled regexp).  The style is a tuple of 1 to 3
        values:  fg color, bg color, and text attributes.  None means to use the
        default.
        
        Example use:  highlight lines to stdout that contain '[Mm]adison'
        
            u = trm.Trm()
            rd = RegexpDecorate(u)
            r = re.compile(r"[Mm]adison")
            fg = u.yel
            bg = u.n
            # Note fg and bg must be escape sequences
            rd.register(r, fg, bg)    # Print matches in light yellow on black
            for line in open(file).readlines():
                rd(line)    # Lines with matches are printed to stdout
                
            Can also be done with
                rd(open(file))
                
        Suppose you have python files in a directory "mydir" and you're interested in knowing how many
        lines contain the string "MySymbol".  This can be done with
        
            rd = RegexpDecorate()
            r = re.compile(r"MySymbol")
            files = pathlib.Path("mydir").glob("*.py")
            rd.register(r, t(Color("yell")), t.n)
            rd(*files)
            
        A command line tool like grep is capable of more precise searching
        including file names and line numbers.
        '''
        def __init__(self, mytrm: ty.Any|None=None) -> None:
            self._styles: dict[re.Pattern, tuple[str, str]] = {}   
            # The following is our trm.Trm instance to get escape codes
            self._u: dict[str, str] = mytrm if mytrm is not None else trm.Trm()
        def register(self, r: re.Pattern, match_style: str, nomatch_style: str|None=None) -> None:
            '''Register a regular expression and its styles
            
            Arguments:
                - match_style:  escape code to print before a match
                - nomatch_style:  escape code to print before a nonmatching string.  If
                  it is None, then self._u.n is used as the return-to-standard escape
                  code.
                  
            You can generate these escape codes with a trm.Trm instance.
            
            If your escape code for match_style includes an attribute, you'll want to
            include the 'no' attribute for normal text in your nomatch_style.
            Otherwise, the remaining text will continue to be printed in the
            match_style's attribute.  The easiest way to do this is to not set
            nomatch_style.
            '''
            assert isinstance(r, re.Pattern)
            if nomatch_style is None:
                # In the following, the type is ignored because all Trm instances have
                # the n attribute at instantiation, but mypy doesn't know this
                nomatch_style = self._u.n   # type: ignore
            self._styles[r] = (match_style, nomatch_style)
        def unregister(self, r: re.Pattern) -> None:
            "Remove regexp r from our styles dict"
            if r in self._styles:
                del self._styles[r]
        def __str__(self) -> str:
            return f"RegexpDecorate(<styles={len(self._styles)}>)"
        def __repr__(self) -> str:
            return str(self)
        def decorate(self, line: str) -> str:
            '''Apply the registered regular expressions to the string line and return the string,
            decorated if there was a match.
            '''
            assert isinstance(line, str)
            out = io.StringIO()
            self(line, file=out)
            return out.getvalue()
        def __call__(self, line: str, file: SupportsWrite=sys.stdout, insert_nl: bool=False) -> bool:
            '''Print the decorated line to a stream.  Check line for a match to one of the
            registered regexps and if there's a match, print the decorated line to the indicated
            stream.  Returns True if there was a match, False otherwise.
            
            Arguments:
                - line:  String to search
                - file:  Stream to send the decorated line
                - insert_nl:  If True, print a newline if line doesn't end with a newline.
                
            '''
            assert isinstance(line, str)
            if not line:
                return False
            has_nl = line.endswith("\n")
            had_match = False
            match_style, nomatch_style = "", t.n
            while line:
                # Find regexp match closest to beginning of line
                shortest = []
                for r in self._styles:
                    mo = r.search(line)
                    if mo:
                        shortest.append((mo.start(), mo, r))
                        had_match = True
                if not shortest:
                    # No more matches
                    if line and had_match:
                        if not has_nl and insert_nl:
                            print(f"{line}{nomatch_style}", file=file)
                        else:
                            print(f"{line}{nomatch_style}", end="", file=file)
                    elif line:
                        # Print rest of line
                        if not has_nl and insert_nl:
                            print(f"{nomatch_style}{line}{t.n}", file=file)
                        else:
                            print(f"{nomatch_style}{line}{t.n}", end="", file=file)
                    return had_match
                # Sort shortest to find the first match
                location, mo, r = sorted(shortest, key=lambda x: x[0])[0]
                match_style, nomatch_style = self._styles[r]
                # Print non-matching start stuff in nomatch_style
                print(f"{nomatch_style}{line[:location]}", end="", file=file)
                # Print the match in match_style, then the escape code to
                # switch back to the default print style (t.n).
                match = line[mo.start():mo.end()]
                print(f"{match_style}{match}{nomatch_style}", file=file, end="")
                # Trim the line and search again
                line = line[mo.end():]
            if had_match:
                print(f"{t.n}", end="")  # Default text style
                if not line and not has_nl and insert_nl:
                    print(file=file)
            return True
if 1:   # Core functionality
    def MatchCapitalization(s: str, t: str) -> str:
        '''Return string t capitalized as string s is
        
        Must have len(s) >= len(t).
        
        Example
            >>> s = "StuVwxyz"
            >>> t = "abcd"
            >>> MatchCapitalization(s, t) 
            "AbcD"
        
        If the example is confusing to you, what's going on is that s has the 0th and
        3rd characters capitalized, so the function will return t capitalized in the
        same fashion.
        '''
        @functools.lru_cache(maxsize=1)
        def GetCharacterSets() -> tuple[set, set, set]:
            'Cache our string constants'
            return (set(string.ascii_letters), set(string.ascii_uppercase), set(string.ascii_lowercase))
        if not t:
            return t
        if len(s) < len(t):
            raise ValueError("len(s) must be >= len(t)")
        ac, uc, lc = GetCharacterSets()
        out = []
        for i in range(len(t)):
            if s[i] in ac and t[i] in ac:
                if s[i] in uc and t[i] in lc:
                    out.append(t[i].upper())
                elif s[i] in lc and t[i] in uc:
                    out.append(t[i].lower())
                else:
                    out.append(t[i])
            else:
                out.append(t[i])
        return ''.join(out)
    def soundex(s: str) -> str:
        '''Return the 4-character soundex value to a string argument
        
        The string s must be one word formed with ASCII characters and with no
        punctuation or spaces.  The returned soundex string can be used to compare the
        sounds of words; from US patents 1261167(1918) and 1435663(1922) by Odell and
        Russell.
        
        The algorithm is from Knuth, "The Art of Computer Programming", volume 3,
        "Sorting and Searching", pg. 392:
        
            1. Retain first letter of name and drop all occurrences
               of a, e, h, i, o, u, w, y in other positions.
            2. Assign the following numbers to the remaining letters after the first:
                1: b, f, p, v
                2: c, g, j, k, q, s, x, z
                3: d, t
                4: l
                5: m, n
                6: r
            3. If two or more letters with the same code were adjacent in the original
               name (before step 1), omit all but the first.
        
            4. Convert to the form "letter, digit, digit, digit" by adding trailing
               zeroes (if there are less than three digits), or by dropping rightmost
               digits (if there are more than three).

        Example
            >>> soundex("knuth")
            'K530'
            >>> soundex("MatchCapitalization")
            'M322'
        '''
        if not s:
            raise ValueError("Argument s must not be empty string")
        if set(s) - set(string.ascii_letters):
            raise ValueError("String s must contain only ASCII letters")
        mdict = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "01230120022455012623010202", strict=True))
        # Function to map upper-case letters to soundex number
        def getnum(x):
            return [mdict[i] for i in x]
        all_caps = s.upper()
        num, keep = getnum(all_caps), []
        # Step 0 (and step 3): keep only those letters that don't map to
        # the same number as the previous letter.
        for i, code in enumerate(num):
            if not i:
                keep.append(all_caps[0])  # Always keep first letter
            else:
                if code != num[i - 1]:
                    keep.append(all_caps[i])
        # Step 1: remove vowels, etc.
        first_letter = keep[0]
        ignore, process = set("AEHIOUWY"), []
        process += [i for i in keep[1:] if i not in ignore]
        # Step 2: assign numbers for remaining letters
        code = first_letter + "".join(getnum("".join(process)))
        # Step 3: same as step 0
        # Step 4: adjust length
        if len(code) > 4:
            code = code[:4]
        while len(code) < 4:
            code += "0"
        return code
    def SoundSimilar(s: str, t: str) -> bool:
        'Return True if the strings s and t sound similar'
        return True if soundex(s) == soundex(t) else False
    def CommonPrefix(seq: ty.Sequence[str]) -> str:
        'Return the largest string that is a prefix of all the strings in seq'
        return os.path.commonprefix(seq)
    def CommonSuffix(seq: ty.Sequence[str]) -> str:
        'Return the largest string that is a suffix of all the strings in seq'
        # Reverse each string in seq, find their common prefix, reverse the result
        def rev(s):  # Reverse the string s
            return ''.join([''.join(list(i)) for i in reversed(s)])
        return ''.join(rev(CommonPrefix([rev(i) for i in seq])))
    def FindAll(s: str | bytes, substr: str | bytes ="∞") -> ty.Generator[int, None, None]:
        '''Generator to find all locations of substr in string s
        
        An example of use is to let you only see a chunk of a string between two
        occurrences of ∞:
            >>> s = "This ∞is an example of a∞ string"
            >>> start, finish = list(FindAll(s))
            >>> print(repr(s[start + 1:finish]))
            'is an example of a'
        You'll get an exception if there aren't two ∞ characters in the file.
        '''
        if isinstance(s, str):
            if not isinstance(substr, str):
                raise TypeError("substr must be a str")
            loc = s.find(substr)
            while loc != -1:
                yield loc
                loc = s.find(substr, loc + 1)
        elif isinstance(s, bytes):
            if not isinstance(substr, bytes):
                raise TypeError("substr must be a bytes object")
            loc = s.find(substr)
            while loc != -1:
                yield loc
                loc = s.find(substr, loc + 1)
    #yy
    def FindFirstIn(s, items, invert=False):
        '''Return smallest integer i such that s[i] is in items or else None.  If invert
        is True, find the smallest integer i such that s[i] is not in items.
                
        if s is a reversed type, then we're searching for the last index of the item in
        items if invert is False or the last index of the first item in reversed(s)
        that's in items when invert is True.
        '''
        if not s or not items:
            return None
        set_of_items = set(items)
        # If s is a reversed iterator, convert it to a list so s[i]
        # doesn't fail
        rev = isinstance(s, reversed)
        r = list(s) if rev else s
        n = len(r)
        for i in range(n):
            if invert:
                if r[i] not in set_of_items:
                    return n - i - 1 if rev else i
            else:
                if r[i] in set_of_items:
                    return n - i - 1 if rev else i
        return None
    def FindLastIn(s, items):
        "Return index of last element in s in items or None"
        return FindFirstIn(reversed(s), items)
    def FindFirstNotIn(s, items):
        "Return smallest integer i such that s[i] not in items else None"
        return FindFirstIn(s, items, invert=True)
    def FindLastNotIn(s, items):
        "Return index of last element in s not in items or None"
        return FindFirstIn(reversed(s), items, invert=True)
    def Keep(s, keep, whole=True, left=False, middle=False, right=False):
        '''Return a list (or a string if s is a string) of the items in s that
        are in keep.
        
        If whole is True:
            Returns s only with elements that are in keep.
            Examples:
                Keep("a;bc;d;", ";") returns ";;;"
                Keep("a;bc;d;", string.ascii_lowercase) returns "abcd"
            Note whole is True by default.  If left, middle, or right are
            True, then whole is set to False.
        else:
            Splits s into sl + sm + sr where
                - sl is the sequence of leftmost elements of s not in keep
                - sr is the sequence of rightmost elements of s not in keep
                - sm is the sequence of elements of s with sl and sr trimmed
                    off where only the elements of s in keep are kept
            Examples:
                s = "a;bc;d;"
                keep = string.ascii_lowercase
                Keep(s, keep, left=True) returns "a"
                Keep(s, keep, middle=True) returns ";bc;d"
                Keep(s, keep, right=True) returns ""
            Note that the middle section of the string may contain elements
            not in keep.  If you don't want this, run Keep(..., whole=True)
            on the result.
        '''
        kp = set(keep)
        if left or middle or right:
            whole = False
        if whole:
            result = []
            for i in s:
                if i in kp:
                    result.append(i)
            return "".join(result) if isinstance(s, str) else result
        else:
            sl = FindFirstNotIn(s, keep)
            sr = FindLastNotIn(s, keep)
            # Get components
            s_left = s[:sl]
            s_right = s[sr + 1 :]
            s_middle = s[sl : sr + 1]
            # Check invariant
            if s_left + s_middle + s_right != s:
                if isinstance(s, str):
                    msg = "Bug:  s_left + s_middle + s_right != original string"
                else:
                    msg = "Bug:  s_left + s_middle + s_right != original sequence"
                raise RuntimeError(msg)
            result = []
            if left:
                result.append(s_left)
            if middle:
                result.append(s_middle)
            if right:
                result.append(s_right)
            if isinstance(s, str):
                return "".join(result)
            else:
                return result
    def KeepFilter(keep):
        '''Return a function that takes a string and returns a string
        containing only those characters that are in keep.
        '''
        def func(s):
            return Keep(s, keep, whole=True)
        return func
    def Remove(s, remove):
        'Return a sequence of the items in s that are not in remove'
        r = set(remove)
        def f(x):
            return x in r
        ret = itertools.filterfalse(f, s)
        return "".join(ret) if isinstance(s, str) else type(s)(ret)
    def RemoveFilter(remove):
        '''Return a function that takes a string and returns a string containing only
        those characters that are not in remove.
        '''
        def func(s):
            return Remove(s, remove)
        return func
    def CountLeadingSpaces(s, trim_start=True, trim_end=True):
        '''Return the number of common leading space characters in the multiline string
        s.  The use case for this is a multiline string in an indented function in which
        you want all the lines aligned to the left margin.  You would do this by getting
        the number of spaces n returned by this function, then removing that number of
        leading spaces from each line in the sequence.  You'd do this by 
        
            s = PrepareMultilineString(s)
         
        A common pattern for defining a multiline function in a string is such as the
        following
        
        x = """
            Line1
            Line2
        """
        
        or x = "\n    Line1\n    Line2\n        "
        
        and we want the returned multiline string array to be ["····Line1", "····Line2"]
        (spaces replaced with '·' characters).  This would require removing everything
        up to the first newline (including the newline), then removing the trailing
        spaces up to the last newline, then removing the last newline.  Then if you use
        split("\n") on the string, you get the two lines you expect and this function
        will tell you there are 4 leading spaces.
        '''
        if not isinstance(s, str):
            raise TypeError("Argument s must be a string")
        spacecharset = set([g.sp])
        if trim_start or trim_end:
            x = PrepareMultilineString(s, trim_start=trim_start, trim_end=trim_end)
        else:
            # No trimming, so just count the leading space characters
            return len(GetStartingChars(s, chars=spacecharset))
        # Break into lines and count spaces on each line
        lines = x.split(g.nl)
        # Count number of leading space characters on each line
        counts = [len(GetStartingChars(line, chars=spacecharset)) for line in lines]
        return min(set(counts))
    def PrepareMultilineString(s, trim_start=True, trim_end=True):
        '''If trim_start, remove leading spaces of s up to the first newline, then
        remove the first newline.  If trim_end, remove trailing spaces of s up to the
        last newline, then remove the last newline.  Return the string.
        '''
        n = bool(trim_start) + bool(trim_end) - 1
        if s.count(g.nl) < n:
            raise ValueError("Not enough newline characters in multiline string s")
        dq = collections.deque(s)
        if trim_start:
            while dq and dq[0] == g.sp:
                dq.popleft()
            # All leading spaces removed; check for newline
            if dq and dq[0] == g.nl:
                dq.popleft()
        if trim_end:
            while dq and dq[-1] == g.sp:
                dq.pop()
            # All trailing spaces removed; check for newline
            if dq and dq[-1] == g.nl:
                dq.pop()
        return ''.join(list(dq))
    def RemoveWhitespace(s: str) -> str:
        '''Remove all whitespace characters from the string s
        
        Whitespace characters are:
            " "     space 
            "\t"    tab
            "\n"    linefeed
            "\r"    carriage return
            "\f"    formfeed
            "\v"    vertical tab
        This method is fast and elegant because it's done by C code (from
        https://mark-summerfield.github.io/01_nows.html).
        '''
        return ''.join(s.split())
    def RemoveEndingChars(s, chars=""):
        'Remove any ending characters in chars from s and return the result'
        if not s or not chars:
            return s
        S = set(chars)
        while s and s[-1] in S:
            s = s[:-1]
        return s
    def RemoveStartingChars(s, chars=""):
        'Remove any starting characters in chars from s and return the result'
        if not s or not chars:
            return s
        i, S = 0, set(chars)
        while s[i] in S:
            i += 1
        return s[i:]
    def FilterSeqRegex(seq, regexes=None, ANDed=True, re_flags=g.noflag):
        '''Return a sequence of strings filtered by regexes.  The regexes are ANDed
        together by default; set ANDed to False to OR the regexes.  If the regexes are
        ORed together, no duplicates are returned.  In both cases, the returned strings
        are in the same relative order as they were in seq.
        '''
        if regexes is None:
            return seq
        # Only keep the strings in seq
        myseq, o = [i for i in seq if isinstance(i, str)], []
        if ANDed:
            for pattern in regexes:
                myseq = list(filter(lambda x: re.search(pattern, x, re_flags), myseq))
            return myseq
        else:
            for pattern in regexes:
                o.extend(list(filter(lambda x: re.search(pattern, x, re_flags), myseq)))
            # Remove duplicates
            return dpseq.DupNodupHashable(o)[1]
    def FilterStr(remove, replacements):
        '''Return a function that removes the characters in sequence remove from other
        strings and replaces them with corresponding characters in the sequence
        replacements.
        '''
        if len(remove) != len(replacements):
            raise ValueError("remove and replacements must be the same length")
        T = "".maketrans(dict(zip(remove, replacements, strict=True)))
        return lambda s: s.translate(T)
    def FindDiff(s1, s2, ignore_empty=False, equal_length=False):
        '''Returns the integer index of where the strings s1 and s2 first differ.  The
        number returned is the index where the first difference was found.  If the
        strings are equal, then -1 is returned, implying one string is a substring of
        the other (or they are the same string).  If ignore_empty is False, an exception
        is raised if one of the strings is empty.  If equal_length is True, then the
        strings must be of equal length or a ValueError exception is raised.
        '''
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Arguments must be strings")
        if (not s1 or not s2) and not ignore_empty:
            raise ValueError("String cannot be empty")
        if equal_length and len(s1) != len(s2):
            raise ValueError("Strings must be equal lengths")
        n = min(len(s1), len(s2))
        if not n:
            return 0
        if s1[:n] == s2[:n]:
            return -1
        # Compare characters until we get a mismatch
        for i in range(n):
            if s1[i] != s2[i]:
                return i
        raise RuntimeError("Bug:  strings differed")
    def FindStrings(seq, Str, ignorecase=False):
        '''Return list of (i, j) pairs which indicate where the strings in sequence seq
        (index i) are located in string Str (index j).  An empty list is returned if
        there are no matches.
        
        Example:
            seq = "Jan Feb Mar".split()
            Str = "1Jan2001"
            found = FindStrings(seq, Str)
            Then found is [(0, 1)]
        '''
        found, sq = [], seq
        if ignorecase:
            sq = [i.lower() for i in seq]
        for i, u in enumerate(sq):
            j = Str.find(u)
            if j != -1:
                found.append((i, j))
        return found
    def FindSubstring(mystring, substring):
        '''Return a tuple of the all the indexes of where the substring is found in the
        string mystring.
        '''
        if not isinstance(mystring, str):
            raise TypeError("mystring needs to be a string")
        if not isinstance(substring, str):
            raise TypeError("substring needs to be a string")
        d, ls, lsub = [], len(mystring), len(substring)
        if not ls or not lsub or lsub > ls:
            return tuple(d)
        start = mystring.find(substring)
        while start != -1 and ls - start >= lsub:
            d.append(start)
            start = mystring.find(substring, start + 1)
        return tuple(d)
    def FindSymbol(symbol, filelist=None, ignore_case=False):
        '''Given a string symbol, return a list of the python files in filelist that
        contain the indicated symbol.  The items in filelist can be strings or 
        pathlib.Path instances and can end in '.py' or not.
         
        The symbols are found by importing the python file as a module and seeing if 
        it contains the symbol.
        '''
        if filelist is None or not symbol:
            return []
        found = []
        for file in filelist:
            myfile = pathlib.Path(file) if isinstance(file, str) else file
            if not isinstance(myfile, pathlib.Path):
                raise TypeError(f"{file!r} can't be made a pathlib.Path instance")
            name = myfile.stem if myfile.suffix == ".py" else myfile.name
            dummy = importlib.import_module(name)
            symbols = dir(dummy)
            if ignore_case:
                symbols = [i.lower() for i in symbols]
                symbol = symbol.lower()
            if symbol in symbols:
                found.append(str(myfile))
        return found
    def GetString(prompt_msg, default, allowed_values, ignore_case=True):
        '''Get a string from a user and compare it to a sequence of allowed values.  If
        the response is in the allowed values, return it.  Otherwise, print an error
        message and ask again.  The letter 'q' or 'Q' will let the user quit the
        program.  The returned string will have no leading or trailing whitespace.
        '''
        if ignore_case:
            allowed_values = [i.lower() for i in allowed_values]
        while True:
            msg = prompt_msg + " [" + default + "]: "
            response = input(msg)
            s = response.strip()
            if not s:
                return default
            if s.lower() == "q":
                exit(0)
            s = s.lower() if ignore_case else s
            if s in allowed_values:
                return s
            print(f"{response.strip()!r} is not a valid response")
    def GetChoice(name, names):
        '''name is a string and names is a set or dict of strings.  Find if name
        uniquely identifies a string in names; if so, return it.  If it isn't unique,
        return a list of the matches.  Otherwise return None.  The objective is to allow
        name to be the minimum length prefix string necessary to uniquely identify the
        choice.
        '''
        # See self tests below for an example of use
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if not isinstance(names, (set, dict)):
            raise ValueError("names must be a set or dictionary")
        d = collections.defaultdict(list)
        for i in names:
            d[i[: len(name)]] += [i]
        if name in d:
            if len(d[name]) == 1:
                return d[name][0]
            else:
                return d[name]
        return None
    def KeepOnlyLetters(s, underscore=False, digits=False):
        '''Replace all non-word characters with spaces.  If underscore is True, keep
        underscores too (e.g., typical for programming language identifiers).  If digits
        is True, keep digits too.
        '''
        allowed = string.ascii_letters + "_" if underscore else string.ascii_letters
        allowed += string.digits if digits is True else ""
        c = [chr(i) for i in range(256)]
        t = "".join([i if i in allowed else " " for i in c])
        return s.translate(t)
    def StringSplit(fields, string, remainder=True, strict=True):
        '''Pick out the specified fields of the string and return them as a tuple of
        strings.  fields can be either a format string or a list/tuple of numbers.
        
        Field numbering starts at 0.  If strict is True, then the indicated number of
        fields must be returned or a ValueError exception will be raised.
        
        fields is a format string
            A format string is used to get particular columns of the string.  For
            example, the format string "5s 3x 8s 8s" means to pick out the first five
            characters of the string, skip three spaces, get the next 8 characters, then
            the next 8 characters.  If remainder is False, this is all that's returned;
            if remainder is True, then whatever is left over will also be returned.
            Thus, if remainder is False, you'll have a 3-tuple of strings returned; if
            True, a 4-tuple.
            
        fields is a sequence of numbers
            The numbers specify cutting the string at the indicated columns (numbering
            is 0-based).  Example: for the input string "hello there", using the fields
            of [3, 7] will return the tuple of strings ("hel", "lo t", "here").
        
                "hello there"
                 01234567890
                 
        Derived from code by Alex Martelli at
        http://code.activestate.com/recipes/65224-accessing-substrings/ Downloaded Sun
        27 Jul 2014 07:52:44 AM
        '''
        if isinstance(fields, str):
            left_over = len(string) - struct.calcsize(fields)
            if left_over < 0:
                raise ValueError("string is shorter than requested format")
            format = f"{fields} {left_over}s"
            s = bytes(string.encode("ascii"))
            result = list(struct.unpack(format, s))
            return result if remainder else result[:-1]
        else:
            pieces = [string[i:j] for i, j in zip([0] + fields, fields)]    # noqa
            if remainder:
                pieces.append(string[fields[-1] :])
            num_expected = len(fields) + 1
            if num_expected != len(pieces) and strict:
                raise ValueError(f"Expected {num_expected} pieces; got {len(pieces)}")
            return pieces
    def ListInColumns(alist, col_width=0, num_columns=0, space_betw=0, truncate=0):
        '''Returns a list of strings with the elements of alist (if components are not
        strings, they will be converted to strings using str) printed in columnar
        format.  Elements of alist that won't fit in a column either generate an
        exception if truncate is 0 or get truncated if truncate is nonzero.  The number
        of spaces between columns is space_betw.
        
        If col_width and num_columns are 0, then the program will set them by reading
        the COLUMNS environment variable.  If COLUMNS doesn't exist, col_width will
        default to 80.  num_columns will be chosen by finding the length of the largest
        element so that it is not truncated.
        
        Caveat: if there are a small number of elements in the list, you may not get
        what you expect.  For example, try a list size of 1 to 10 with num_columns equal
        to 4: for lists of 1, 2, 3, 5, 6, and 9, you'll get fewer than four columns.
        
        This function is obsolete; instead, use Columnize in columnize.py.
        '''
        # Make all integers
        col_width = int(col_width)
        num_columns = int(num_columns)
        space_betw = int(space_betw)
        truncate = int(truncate)
        lines = []
        N = len(alist)
        if not N:
            return [""]
        # Get the length of the longest line in the alist
        maxlen = max([len(str(i)) for i in alist])
        if not maxlen:
            return [""]
        if not col_width:
            if "COLUMNS" in os.environ:
                columns = int(os.environ["COLUMNS"]) - 1
            else:
                columns = 80 - 1
            col_width = maxlen
        if not num_columns:
            try:
                num_columns = int(columns // maxlen)
            except Exception:
                return [""]
            if num_columns < 1:
                raise ValueError("A line is too long to display")
            space_betw = 1
        if not col_width or not num_columns or space_betw < 0:
            raise ValueError("Error: invalid parameters")
        num_rows = int(N // num_columns + (N % num_columns != 0))
        for row in range(num_rows):
            s = ""
            for column in range(num_columns):
                i = int(num_rows*column + row)
                if 0 <= i <= (N - 1):
                    if len(str(alist[i])) > col_width:
                        if truncate:
                            s += str(alist[i])[:col_width] + " "*space_betw
                        else:
                            raise ValueError(f"Error: element {i} too long")
                    else:
                        s += (
                            str(alist[i])
                            + " "*(col_width - len(str(alist[i])))
                            + " "*space_betw
                        )
            lines.append(s)
        assert len(lines) == num_rows
        msg = "dpstr.ListInColumns is obsolete.  Use columnize.Columnize."
        raise ValueError(msg)
        return lines
    def MultipleReplace(text, patterns, flags=0):
        '''Replace multiple patterns in the string text.  patterns is a dictionary whose
        keys are the regular expressions and values are the replacement text.  The flags
        keyword variable is the same as that used by the re.compile function.
        
        From page 88 of Python Cookbook.
        '''
        # Make a compound regular expression from all the keys
        r = re.compile("|".join(map(re.escape, patterns.keys())), flags)
        # For each match, look up the corresponding value in the dictionary
        return r.sub(lambda match: patterns[match.group(0)], text)
    def RemoveComment(line, code=False):
        '''Remove the largest string starting with '#' from the string line.  If code is
        True, then the resulting line will be compiled and an exception will occur if
        the modified line won't compile.  This typically happens if '#' is inside of a
        comment.
        '''
        orig = line
        loc = line.find("#")
        if loc != -1:
            line = line[:loc]
        if code:
            try:
                compile(line, "", "single")
            except Exception as e:
                msg = f"Line with comment removed won't compile:\n  {orig!r}"
                raise ValueError(msg) from e
        return line
    def SpellCheck(input, words, ignore_case=True):
        '''input is a sequence of word strings; words is a dictionary or set
        of correct spellings.  Return the set of any words in input that are not
        in words.
        '''
        if not input:
            return []
        if not words:
            raise ValueError("words parameter is empty")
        misspelled = set()
        for word in input:
            if ignore_case:
                word = word.lower()
            if word not in words:
                misspelled.add(word)
        return misspelled
    def SplitOnNewlines(s):
        '''Splits s on all of the three newline sequences: "\r\n", "\r", or "\n".
        Returns a list of the strings.
        
        Copyright (c) 2002-2009 Zooko Wilcox-O'Hearn, who put it under the GPL.
        '''
        res = []
        for x in s.split(g.cr + g.nl):
            for y in x.split(g.cr):
                res.extend(y.split(g.nl))
        return res
    def TimeStr(time_in_s=None):
        '''Return a readable string for the indicated time in seconds.  If the parameter
        is None, the time is time.now().  Example:
            Time(1646408691.9415808) returns '4Mar2022-084451.942am'
        This is a convenience aimed at producing names that can be used in a filename
        for things like timestamping.
        '''
        def Rm0(s):
            if s.startswith("0"):
                return s[1:]
            return s
        # Get t as time in seconds from the epoch (note it is local time, not GMT)
        T = time_in_s if time_in_s else time.time()
        # ts will contain the time structure needed by time's functions
        ts = time.localtime(T)
        # Date portion
        d = Rm0(time.strftime("%d%b%Y", ts))
        t = time.strftime("%I%M%S", ts)
        ampm = time.strftime("%p", ts).lower()
        # Get fractions of seconds.  Resolution is to the nearest μs because this gave
        # what looked to be sufficient time resolution on my system to avoid generating
        # an accidental collision, at least in the same process.
        n = 6
        fs = round(T - int(T), n)
        f = Rm0(f"{fs:.{n}f}")
        return f"{d}-{t}{f}{ampm}"
    def WordID(half_length=3, unique=None, num_tries=100):
        '''Return an ID string that is (somewhat) pronounceable.  The returned number of
        characters will be twice the half_length.  If unique is not None, it must be a
        container that can be used to determine if the ID is unique.  You are
        responsible for adding the returned word to the container.
        
        The method is to choose a consonant from 'bdfghklmnprstvw' and append a vowel;
        do this half_length number of times.
        
        Interestingly, the words often look like they come from Japanese or Hawaiian.
        
        I derived the code from http://code.activestate.com/recipes/576858, but this
        link now points to a different algorithm.  The original recipe was by Robin
        Palmer on 8 Aug 2007 under PSF license.
        '''
        v, c, r, count = "aeiou", "bdfghklmnprstvw", range(half_length), 0
        while count < num_tries:
            word = "".join([random.choice(c) + random.choice(v) for i in r])
            if not unique or (unique and word not in unique):
                return word
            count += 1
        raise RuntimeError("Couldn't generate unique word")
        '''Here's some driver code that prints out lists of these words:
            from columnize import Columnize
            from words import words_ic
            num_words = 100
            for n in range(2, 6):
                print("{} letters:".format(2*n))
                uniq = set()
                for i in range(num_words):
                    is_word = True
                    while is_word:
                        w = WordID(n, unique=uniq)
                        is_word = w in words_ic
                        if not is_word:
                            uniq.add(w)
                s = sorted(list(uniq))
                for line in Columnize(s, col_width=2*n+2, indent=" "*2):
                    print(line)
                print()
        '''
    def Chop(seq, size):
        '''Return a list of the sequence seq chopped into subsequences of length size.
        The last subsequence will be shorter than size if len(seq) % size is not zero.
        '''
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be integer > 0")
        out = []
        for i in range(0, len(seq), size):
            out.append(seq[i : i + size])
        return out
    def ReadData(data, structure, **kw):
        '''Read data from a multiline string 'data'.  structure is a list of the field
        types.  Any line starting with optional whitespace and the comment string is
        ignored, as is any line with only whitespace.
        
        Keywords:
            comment     Ignore lines that start with this string and optional
                        whitespace.  Can also be a compiled regular expression.
            sep         Separator string for fields.  Defaults to whitespace.
                        Can be a compiled regular expression.
        
        Example: For the string
        
            data = """
                 9   680     2100    0       750
                10   680     2100    250     750
            """
        the call ReadData(data, structure=[str, int, int, int, int] returns the list
            [
                ["9", 680, 2100, 0, 750],
                ["10", 680, 2100, 250, 750]
            ]
            
        If an error occurs, the 1-based line number of the offending string will be
        printed along with the problem.
        
        ∞∞2 ReadData:  This function can be made to work with bytes too
            s = b"1 2 3\n4 5 6"
            s.split(b"\n") gives [b'1 2 3', b'4 5 6'] and these can be converted to
            integers.  re works with str and bytes, but they can't be mixed.
        '''
        # Get keywords
        comment = kw.get("comment", None)
        sep = kw.get("sep", None)
        out = []
        for linenum, line in enumerate(data.split("\n")):
            linenum += 1
            line = line.strip()
            if not line:
                continue
            if comment is not None:
                if isinstance(comment, str) and line.startswith(comment):
                    continue
                elif hasattr(comment, "search"):
                    # It's a compiled regular expression
                    if comment.search(line):
                        continue
            if sep is not None:
                if isinstance(sep, str):
                    fields = line.split(sep)
                elif hasattr(sep, "split"):
                    fields = sep.split(line)
                else:
                    raise ValueError("sep '{sep}' is unknown type")
            else:
                fields = line.split()
            if len(fields) != len(structure):
                n, m = len(fields), len(structure)
                msg = wrap.dedent(f'''
                Line {linenum} has {n} field{"s" if n > 1 else ""}
                The structure list has {m} field{"s" if m > 1 else ""}
                They must be the same.
                ''')
                raise ValueError(msg)
            thisline = []
            for i in range(len(structure)):
                thisline.append(structure[i](fields[i]))
            out.append(thisline)
        return out
    def Len(s):
        '''Same as built-in len(), except if the argument is a str, the ANSI escape
        sequences are stripped out.
        '''
        if not hasattr(Len, "len"): # Cache built-in len in case someone redefines it
            Len.len = len
        if isinstance(s, str):
            return Len.len(RmEsc(s))
        return Len.len(s)
    def RmEsc(s, on=True):
        '''Remove ANSI escape strings if on is True; otherwise just return s.
        
        The primary use case is to remove colorizing ANSI escape strings from a string
        s.  Not all ANSI escape strings are supported, just the ones that contain a CSI
        sequence.
        '''
        if not on:
            # Don't check the type of s if on is False; this makes this the identity
            # function for any type.
            return s
        assert isinstance(s, str)
        if not hasattr(RmEsc, "r"):
            # This regexp was constructed from the information given on the
            # page https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences
            # This is:
            #   esc [
            # then "parameter bytes":    zero or more bytes 0x30-0x3f       [0-?]
            # then "intermediate bytes": zero or more bytes 0x20-0x2f       [ -/]
            # then "single byte":        one byte in range of 0x40-0x7e     [@-~]
            RmEsc.r = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
        return RmEsc.r.sub("", s)
    def Tokenize(s, wordchars=None, check=False):
        '''Split the string s into a list lst such that ''.join(lst) is the original
        string.  wordchars is a sequence of characters that are in words.  wordchars
        defaults to string.ascii_letters + string.digits.  If check is True, verify the
        invariant s == ''.join(lst).
        '''
        if not isinstance(s, str):
            raise TypeError("Argument s needs to be a string")
        if wordchars is None:
            S = set(string.ascii_letters + string.digits)
        else:
            S = set(wordchars)
        out, word = [], []
        for c in s:
            if c in S:
                word.append(c)
            else:
                if word:
                    out.append("".join(word))
                    word = []
                out.append(c)
        if word:
            out.append(''.join(word))
        if check and ''.join(out) != s:
            raise ValueError("Invariant s == ''.join(out) is not True")
        return out
    def GetStartingChars(s, chars=None):
        '''Return the string defining the starting characters in the string s.  If chars
        is not None, use it as the set of allowed leading characters.  If chars is None,
        then return the leading whitespace characters, which are defined by the re
        module's '\\s' metacharacters.
        '''
        if not isinstance(s, str):
            raise TypeError("s must be a string")
        if chars is None:
            r = re.compile(r"^(\s+).*$", re.M)
            mo = r.match(s)
            return mo.groups()[0] if mo else ""
        else:
            S = set(chars)
            t = re.escape(''.join(S))
            r = re.compile(f"^([{t}]+).*$", re.M)
            mo = r.match(s)
            return mo.groups()[0] if mo else ""
    def GetEndingChars(s, chars=None):
        '''Return the string defining the trailing characters in the string s.  If chars
        is not None, use it as the set of allowed trailing characters.  If chars is
        None, then return the leading whitespace characters, which are defined by the re
        module's '\\s' metacharacters.
        '''
        if not isinstance(s, str):
            raise TypeError("s must be a string")
        if chars is None:
            r = re.compile(r"^[^\s]*(\s+)$", re.M)
            mo = r.match(s)
            return mo.groups()[0] if mo else ""
        else:
            S = set(chars)
            t = re.escape(''.join(S))
            r = re.compile(f"([{t}]+)$", re.M)
            mo = r.search(s)
            return mo.groups()[0] if mo else ""
    def RegisteredOpen(file):
        '''Open the indicated file with its registered application.  file must be a string
        or a Path instance.
        '''
        if isinstance(file, str):
            p = pathlib.Path(file)
        elif isinstance(file, pathlib.Path):
            p = file
        else:
            raise TypeError(f"{file} must be a string or a pathlib.Path instance")
        if not p.exists():
            raise ValueError(f"{str(p)!r} does not exist")
        cwd = os.getcwd()
        try:
            dirname = p.parent
            filename = p.name
            os.chdir(dirname)
            if wsl.wsl:
                # Running under Windows in Windows Subsystem for Linux.  The method is to use
                # explorer.exe to open files.  To get this to work, we have to cd to the file's
                # directory.  It appears Explorer returns 1 under all conditions.
                cmd = f"explorer.exe {filename}"
                subprocess.run(cmd, shell=True)
            else:
                # Must be cygwin; file can be opened with cygstart.exe.
                cmd = f"cygstart {filename}"
                subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"{e}")
        finally:
            os.chdir(cwd)
    def RemoveASCII(s):
        '''Remove ASCII characters from string s.  This means the returned string only
        consists of Unicode characters above 0x7f.  This is done with a cached translation
        table, so it will be fast after the first invocation.
        '''
        if not hasattr(RemoveASCII, "table"):
            # Cache a translation table
            r = range(0, 0x7F)
            chars = [chr(i) for i in r]
            none = [None]*len(chars)
            RemoveASCII.table = "".maketrans(dict(zip(chars, none, strict=True)))
        return s.translate(RemoveASCII.table)
    def IgnoreFilter(regex_seq, ignore_case=False):
        '''Return a function which removes ignored strings.  regex_seq is a sequence of
        regular expressions that should be ignored.  Set ignore_case to True to ignore
        case in the matching.
        
        The intent of this filter is to provide functionality like the .gitignore file
        in a git repository:  any filename in the repository that matches a line in the
        .gitignore file is ignored by git.
        
        Example:
            f = IgnoreFilter(["bob", "carol"])
            g = IgnoreFilter(["bob", "carol"], ignore_case=True)
            seq = [
                "Bob",
                "bob",
                "bobwhite",
                "Carol",
                "carol",
                "Alice"
            ]
            f(seq) returns ["Bob", "Carol", "Alice"].
            g(seq) returns ["Alice"].
        '''
        # Compile the regular expressions
        regexes = []
        for regex in regex_seq:
            if regex:
                regexes.append(re.compile(regex, re.I if ignore_case else 0))
        # Bundle them into a closure
        def f(seq):
            results = seq.copy()
            for regex in regexes:
                results = itertools.filterfalse(regex.search, results)
            return list(results)
        return f
    def IsASCII(s):
        '''Return True if string s is all ASCII characters.  This means the string only
        consists of characters chr(0x0) to chr(0x7e) inclusive.
        '''
        return not bool(RemoveASCII(s))
    def Scramble(mystring, punc=None, start_end_const=False):
        '''Return a string with the letters in the words randomly shuffled but with the
        punctuation and whitespace unchanged if punc is None.
        
        Set punc to a different set of punctuation characters if you wish (the
        punctuation characters are ignored when shuffling words).  For example, you
        might want to include common Unicode characters included as punctuation also.
        
        If start_end_const is True, then the first and last letters of each word are
        unchanged.  This lets you test the assertion that leaving the first and last
        letters intact but shuffling the interior letters doesn't change the readability
        of the text.  I've found this assertion pretty much untrue except for some
        fairly easy-to-read pieces of text.  For example, transform things like "The
        Martian", "Tom Sawyer", and "Pride and Prejudice".  If you get away from the
        well-known sections, you'll likely find them hard to read.  A good demonstration
        is to get a copy of an academic paper on something out of your field and you'll
        probably find you can understand almost nothing of it.  I did this with a long
        article on genetics with a lot of biochemistry and it was gibberish.
        
        If you wish to save memory, make mystring a list of individual characters; then
        a copy of the string isn't made.  Note there is no check that the list's
        elements are single character strings.
        
        Example with random.seed('0'):
            s = '"Hello there", said John.'
        returns
                '"loeHl eerth", isda noJh.'
        '''
        if punc is None:
            punc = set(string.punctuation + string.whitespace)
        dummy = "."
        prepended = appended = False
        is_string = isinstance(mystring, str)
        s = list(mystring) if is_string else mystring
        # Add dummy punctuation characters at start and end if needed.  This
        # regularizes the algorithm.
        if s[0] not in punc:
            s.insert(0, dummy)
            prepended = True
        if s[-1] not in punc:
            s.append(dummy)
            appended = True
        # Generate a list of integers showing where punctuation characters are
        loc = []
        for i in range(len(s)):
            if s[i] in punc:
                loc.append(i)
        # Use loc to pick out words and scramble them
        i = 0
        while i < len(loc):
            try:
                start, end = loc[i], loc[i + 1]
                if end - start > 1:  # It's a word, so shuffle its letters
                    do_shuffle = True
                    if start_end_const:
                        # Need at least 3 characters to shuffle
                        if end - start < 3:
                            do_shuffle = False
                    if do_shuffle:
                        if start_end_const:
                            start += 1
                            end -= 1
                        substr = s[start + 1 : end]
                        if len(substr) > 1:
                            random.shuffle(substr)  # Shuffles sequence in place
                            s[start + 1 : end] = substr
                i += 1
            except IndexError:
                break
        # Clean up
        if prepended:
            s.pop(0)
        if appended:
            s.pop(-1)
        # Return scrambled string or list
        return "".join(s) if is_string else s
    def Trim(s, chars="", left=True, right=True, check=False):
        '''Remove characters in the string chars from the left and right sides of s,
        returning the result.
        
        This routine breaks s into three strings L, M, and R such that s = L + M + R.  L
        and R consist only of characters in chars.  The returned string is
            left    right       returned
            ----    -----     -------------
            True    True            M
            True    False         M + R
            False   True          L + M
            False   False     s = L + M + R
        If check is True, the invariants are validated.
        '''
        if not chars or (not left and not right):
            return s
        cs = "".join(set(chars))
        # Partition s into L, M, R pieces so that s == L + M + R
        MR = s.lstrip(cs)
        LM = s.rstrip(cs)
        M = s.strip(cs)
        L = LM[: len(LM) - len(M)]
        R = MR[len(M) :]
        if check and not set(s).issubset(cs):  # Validate invariants
            if set(s).issubset(cs):
                assert not L and not M and not R
            else:
                assert L + M + R == s
        if left:
            return M if right else M + R
        else:
            return L + M
    def GetTransFunc(chars_from, chars_to, delete=None):
        '''Return a function that will change characters in chars_from to the characters
        in chars_to.  This function uses str.translate() to perform its work at C
        speeds.  If chars_from has N characters, then chars_to must have 1 or N
        characters.  The rules are:
        
            - Any characters in the sequence delete are deleted from chars_from.
            - If delete is not None, then it must be a str whose characters are deleted
              from the string.
            - If chars_to has 1 character, then remaining characters in the string will
              be replaced by the character in chars_to.
              
        Example:  Let chars_from = string.punctuation and chars_to = " ".  Then
        GetTransFunc(chars_from, chars_to) returns a function f that substitutes a space
        character for every punctuation character.  Given a string s, f(s) returns a
        string of the same length as s but with all ASCII punctuation characters
        replaced by a string.
        '''
        if not chars_from:
            return lambda x: x
        N = len(chars_from)
        if len(chars_to) not in (1, N):
            raise ValueError("chars_to must have 1 or len(chars_from) characters")
        From, To = chars_from, chars_to
        if len(chars_to) == 1:
            From, To = chars_from, chars_to*N
        # Check delete
        if delete is None:
            Delete = None
        elif not isinstance(delete, str):
            raise TypeError("delete must be None or a string")
        else:
            Delete = "".join(set(delete))
        # Make the translation table
        tt = str.maketrans(From, To, Delete) if Delete else str.maketrans(From, To)
        # Now make the function
        def f(s):
            return s.translate(tt)
        return f
    def Edit(*files, strict=False, opt=None):
        '''Launch editor on those files that exist.  If strict is True, raise an
        exception if there are no files or a file doesn't exist.  Otherwise, just return
        quietly.  opt is a list of option strings to append before the list of files.
        '''
        editor = os.environ["EDITOR"]
        files_to_edit = []
        for file in files:
            p = pathlib.Path(file)
            if p.exists():
                files_to_edit.append(file)
            else:
                if strict:
                    raise ValueError(f"{file!r} doesn't exist")
        if not files_to_edit:
            if strict:
                raise ValueError("No files to edit")
            return
        # Construct editing string
        e = [editor]
        if opt:
            if isinstance(opt, (list, tuple)):
                e.extend(list(opt))
            elif isinstance(opt, str): 
                e += [opt]
            else:
                raise TypeError("opt must be string or list/tuple of strings")
        e += files_to_edit
        subprocess.call(e)
    def RemoveCharClass(s, keys=""):
        '''Given s, a string, bytes, or bytearry, remove the characters indicated by the
        letters in the keys:
            A   Convert Unicode characters to rough ASCII equivalents
            B   Remove characters under 0x20
            b   Remove characters under 0x20 except newline
            d   Remove characters that are ASCII digits (∈ string.digits)
            h   Remove characters that are hex digits (∈ string.hexdigits)
            l   Remove lower case letters (∈ string.ascii_lowercase)
            n   Remove punctuation (∈ string.punctuation)
            o   Remove characters that are octal digits (∈ string.octdigits)
            p   Remove non-printable characters (∉ string.printable)
            u   Remove upper case letters (∈ string.ascii_uppercase)
            W   Remove whitespace (∈ string.whitespace)
            w   Remove whitespace except newlines
            7   Remove characters above 0x7f (i.e., keep only 7-bit characters)
            8   Remove characters above 0xff (i.e., keep only 8-bit characters)
            0   Remove nothing (identity transformation)
        
        When s is a string, "character" means "Unicode character".  When s is a bytes or
        bytearray type, "character" means "byte".
        
        The A key (ASCIIFY) is the exception to the function's pattern:  no characters are
        removed.  This transliteration is idiomatic and it won't convert any Unicode
        characters that don't look similar to Latin letters.  The length of the string may
        increase:  for example, '∞' is changed to 'oo'.  For bytes or bytearray objects, the
        A letter results in an identity transformation.
        
        For convenience, the above set of letters coding the transformation are stored in
        the RemoveCharClass.allowed_keys variable.
        '''
        letters = "ABbdhlnopWwu780"
        allowed_keys = set(letters)
        if not hasattr(RemoveCharClass, "allowed_keys"):
            RemoveCharClass.allowed_keys = allowed_keys
        keys = set(keys)
        if not keys.issubset(allowed_keys):
            raise ValueError(f"{keys!r} must only contain the letters {letters!r}")
        # Check type of s
        if isinstance(s, str):
            is_str = True
        elif isinstance(s, (bytes, bytearray)):
            is_str = False
        else:
            raise TypeError("s must be str, bytes, or bytearray")
        if 1:
            # Class C is a notational convenience for holding the various sets of characters in
            # the string module.  The attribute letters correspond to the letters that code the
            # transformation.
            class C:
                pass
            c = C()
            c.d = string.digits
            c.h = string.hexdigits
            c.l = string.ascii_lowercase
            c.n = string.punctuation
            c.o = string.octdigits
            c.p = string.printable
            c.W = string.whitespace
            c.w = c.W.replace("\n", "")
            c.u = string.ascii_uppercase
        if is_str:
            if "A" in keys:
                s = asciify.Asciify(s)
            if "B" in keys:
                s = ''.join(i for i in s if ord(i) >= 0x20)
            if "b" in keys:
                s = ''.join(i for i in s if ord(i) >= 0x20 or i == "\n")
            if "d" in keys:
                s = ''.join(i for i in s if i not in set(c.d))
            if "h" in keys:
                s = ''.join(i for i in s if i not in set(c.h))
            if "l" in keys:
                s = ''.join(i for i in s if i not in set(c.l))
            if "o" in keys:
                s = ''.join(i for i in s if i not in set(c.o))
            if "n" in keys:
                s = ''.join(i for i in s if i not in set(c.n))
            if "p" in keys:
                s = ''.join(i for i in s if i     in set(c.p))
            if "W" in keys:
                s = ''.join(i for i in s if i not in set(c.W))
            if "w" in keys:
                s = ''.join(i for i in s if i not in set(c.w))
            if "u" in keys:
                s = ''.join(i for i in s if i not in set(c.u))
            if "7" in keys:
                s = ''.join(i for i in s if ord(i) <= 0x7f)
            if "8" in keys:
                s = ''.join(i for i in s if ord(i) <= 0xff)
            if "0" in keys:
                pass
            return s
        else:
            b = s
            T = bytes if isinstance(b, bytes) else bytearray
            if "A" in keys:
                pass
            if "B" in keys:
                b = T(i for i in b if i >= 0x20)
            if "b" in keys:
                b = T(i for i in b if i >= 0x20 or i == ord("\n"))
            if "d" in keys:
                b = T(i for i in b if i not in set(c.d.encode()))
            if "h" in keys:
                b = T(i for i in b if i not in set(c.h.encode()))
            if "l" in keys:
                b = T(i for i in b if i not in set(c.l.encode()))
            if "o" in keys:
                b = T(i for i in b if i not in set(c.o.encode()))
            if "n" in keys:
                b = T(i for i in b if i not in set(c.n.encode()))
            if "p" in keys:
                b = T(i for i in b if i     in set(c.p.encode()))
            if "W" in keys:
                b = T(i for i in b if i not in set(c.W.encode()))
            if "w" in keys:
                b = T(i for i in b if i not in set(c.w.encode()))
            if "u" in keys:
                b = T(i for i in b if i not in set(c.u.encode()))
            if "7" in keys:
                b = T(i for i in b if i <= 0x7f)
            if "8" in keys or "0" in keys:
                pass
            return b
    class TextWrapper(textwrap.TextWrapper):
        '''This is the same as the textwrap.TextWrapper class except the
        method with calls to len had each occurrence replaced with Len.
        '''
        def _wrap_chunks(self, chunks):
            '''_wrap_chunks(chunks : [string]) -> [string]
            
            Wrap a sequence of text chunks and return a list of lines of
            length 'self.width' or less.  (If 'break_long_words' is false,
            some lines may be longer than this.)  Chunks correspond roughly
            to words and the whitespace between them: each chunk is
            indivisible (modulo 'break_long_words'), but a line break can
            come between any two chunks.  Chunks should not have internal
            whitespace; ie. a chunk is either all whitespace or a "word".
            Whitespace chunks will be removed from the beginning and end of
            lines, but apart from that whitespace is preserved.
            '''
            lines = []
            if self.width <= 0:
                raise ValueError(f"Invalid width {self.width!r} (must be > 0)")
            if self.max_lines is not None:
                if self.max_lines > 1:
                    indent = self.subsequent_indent
                else:
                    indent = self.initial_indent
                if Len(indent) + Len(self.placeholder.lstrip()) > self.width:
                    raise ValueError("placeholder too large for max width")
            # Arrange in reverse order so items can be efficiently popped
            # from a stack of chucks.
            chunks.reverse()
            while chunks:
                # Start the list of chunks that will make up the current line.
                # cur_len is just the length of all the chunks in cur_line.
                cur_line = []
                cur_len = 0
                # Figure out which static string will prefix this line.
                if lines:
                    indent = self.subsequent_indent
                else:
                    indent = self.initial_indent
                # Maximum width for this line.
                width = self.width - Len(indent)
                # First chunk on line is whitespace -- drop it, unless this
                # is the very beginning of the text (ie. no lines started yet).
                if self.drop_whitespace and chunks[-1].strip() == "" and lines:
                    del chunks[-1]
                while chunks:
                    L = Len(chunks[-1])
                    # Can at least squeeze this chunk onto the current line.
                    if cur_len + L <= width:
                        cur_line.append(chunks.pop())
                        cur_len += L
                    # Nope, this line is full.
                    else:
                        break
                # The current line is full, and the next chunk is too big to
                # fit on *any* line (not just this one).
                if chunks and Len(chunks[-1]) > width:
                    self._handle_long_word(chunks, cur_line, cur_len, width)
                    cur_len = sum(map(Len, cur_line))
                # If the last chunk on this line is all whitespace, drop it.
                if self.drop_whitespace and cur_line and cur_line[-1].strip() == "":
                    cur_len -= Len(cur_line[-1])
                    del cur_line[-1]
                if cur_line:
                    if (
                        self.max_lines is None
                        or Len(lines) + 1 < self.max_lines
                        or (
                            not chunks
                            or self.drop_whitespace
                            and Len(chunks) == 1
                            and not chunks[0].strip()
                        )
                        and cur_len <= width
                    ):
                        # Convert current line back to a string and store it in
                        # list of all lines (return value).
                        lines.append(indent + "".join(cur_line))
                    else:
                        while cur_line:
                            if (
                                cur_line[-1].strip()
                                and cur_len + Len(self.placeholder) <= width
                            ):
                                cur_line.append(self.placeholder)
                                lines.append(indent + "".join(cur_line))
                                break
                            cur_len -= Len(cur_line[-1])
                            del cur_line[-1]
                        else:
                            if lines:
                                prev_line = lines[-1].rstrip()
                                if Len(prev_line) + Len(self.placeholder) <= self.width:
                                    lines[-1] = prev_line + self.placeholder
                                    break
                            lines.append(indent + self.placeholder.lstrip())
                        break
            return lines
    def Decorate(s: str | bytes, encoding: str="UTF-8") -> str:
        '''Return a string that is the "decorated" form of the string s
        
        Here, "decorated" means whitespace and control characters have Unicode character
        substitutions that make them easier to see.  If s is bytes, it is first
        converted to a string with the given encoding.
        
        Example
            >>> Decorate(" \t\n")
            '·␉␊'
            >>> Decorate(b" \t\n")
            '·␉␊'
        '''
        @functools.lru_cache(maxsize=1)
        def GetTranslationTable() -> dict[int, str]:
            'Build and cache the translation table'
            di = {i: chr(0x2400 + i) for i in range(0x20)}
            di[0x20] = "·"  # U+B7 for space
            return di
        translation_table = str.maketrans(GetTranslationTable())
        if isinstance(s, str):
            return s.translate(translation_table)
        elif isinstance(s, bytes):
            return s.decode(encoding).translate(translation_table)
        else:
            raise TypeError("s must be a str or bytes instance")
if 1:   # Old util stuff
    def StringToNumbers(s, sep=" ", handle_i=True):
        '''s is a string; return the sequence (tuple) of numbers it represents; number
        strings are separated by the string sep.  The numbers returned are integers,
        fractions, floats, or complex.  If handle_i is True, 'i' or 'I' are allowed as the
        imaginary unit.
        '''
        seq = []
        for line in s.strip().split(g.nl):
            if sep is None:
                seq.extend(line.split(sep))
            else:
                seq.extend(line.split())
        return tuple([ConvertToNumber(i, handle_i=handle_i) for i in seq])
    def RemoveIndent(s, numspaces=4):
        '''Given a multi-line string s, remove the indicated number of spaces from the beginning each
        line.  If that number of space characters aren't present, then leave the line alone.
        '''
        if numspaces < 0:
            raise ValueError("numspaces must be >= 0")
        lines = s.split(g.nl)
        for i, line in enumerate(lines):
            if line.startswith(" " * numspaces):
                lines[i] = lines[i][numspaces:]
        return g.nl.join(lines)
    def GetLeadingString(string, prefix=" "):
        '''Return the leading string from string, made up of one or more groups of the
        indicated string prefix.  A use case is to match the indentation of a previous line.
        
        Examples:
            GetLeadingString(b"zzzHi", prefix=b"z") -> b"zzz"
            GetLeadingString("zzzHi", prefix="z") -> "zzz"
            GetLeadingString("ababHi", prefix="ab") -> "abab"
        '''
        np, lp, ls = 0, len(prefix), len(string)
        while np * lp < ls:
            if string[np * lp : (np + 1) * lp] == prefix:
                np += 1
            else:
                break
        return np * prefix
    def GetTrailingString(string, suffix=" "):
        '''Return the trailing string from string, made up of one or more groups of the
        indicated string suffix.
        '''
        # This is done by reversing string and suffix and using GetLeadingString(), but it
        # does mean we have to create copies in memory.
        def f(x):
            return list(reversed(x))
        result = f(GetLeadingString(f(string), prefix=f(suffix)))
        if type(string) is bytes:
            return bytes(result)
        else:
            return ''.join(result)
    def GetHash(file, method="sha256"):
        "Return a file's hash as a hex string, None if file can't be read"
        ''' 3 Mar 2026  Being moved to dpstr.py
        - ∞∞2 Change parameters
            - file:  should be a Path instance for a file, a str, or bytes
            - add trunc keyword to truncate the returned hex string; None or 0 means
              don't truncate.  trunc will be an integer specifying the number of bytes
              in the hash to keep; the hex string returned will be 2*trunc long.
        - I've made the default hash to be sha256.  git currently uses sha1 by default,
          but will be transitioning to sha256 (supported as of 2.30).  However,
          transitioning is nontrivial.  See
          https://www.codestudy.net/blog/does-git-use-sha-256-to-calculate-commit-hashes/
        '''
        if method.lower() in "md5 sha1 sha224 sha256 sha384 sha512".split():
            h = eval(f"hashlib.{method.lower()}")()
        else:
            raise ValueError(f"{method!r} is unsupported")
        try:
            h.update(open(file, "rb").read())
        except Exception:
            return None
        return h.hexdigest()
    def EBCDIC():
        '''Returns two byte-translation tables to use with
        bytes.translate().  The first converts ASCII bytes to EBCDIC and the
        second converts EBCDIC bytes to ASCII.
        '''
        a2e = [int(i) for i in
            '''0 1 2 3 55 45 46 47 22 5 37 11 12 13 14 15 16 17 18 19 60 61 50 38 24 25
            63 39 28 29 30 31 64 79 127 123 91 108 80 125 77 93 92 78 107 96 75 97 240
            241 242 243 244 245 246 247 248 249 122 94 76 126 110 111 124 193 194 195
            196 197 198 199 200 201 209 210 211 212 213 214 215 216 217 226 227 228 229
            230 231 232 233 74 224 90 95 109 121 129 130 131 132 133 134 135 136 137 145
            146 147 148 149 150 151 152 153 162 163 164 165 166 167 168 169 192 106 208
            161 7 32 33 34 35 36 21 6 23 40 41 42 43 44 9 10 27 48 49 26 51 52 53 54 8
            56 57 58 59 4 20 62 225 65 66 67 68 69 70 71 72 73 81 82 83 84 85 86 87 88
            89 98 99 100 101 102 103 104 105 112 113 114 115 116 117 118 119 120 128 138
            139 140 141 142 143 144 154 155 156 157 158 159 160 170 171 172 173 174 175
            176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 202 203 204
            205 206 207 218 219 220 221 222 223 234 235 236 237 238 239 250 251 252 253
            254 255'''.split()
        ]
        e2a = [int(i) for i in 
            '''0 1 2 3 156 9 134 127 151 141 142 11 12 13 14 15 16 17 18 19 157 133 8
            135 24 25 146 143 28 29 30 31 128 129 130 131 132 10 23 27 136 137 138 139
            140 5 6 7 144 145 22 147 148 149 150 4 152 153 154 155 20 21 158 26 32 160
            161 162 163 164 165 166 167 168 91 46 60 40 43 33 38 169 170 171 172 173 174
            175 176 177 93 36 42 41 59 94 45 47 178 179 180 181 182 183 184 185 124 44
            37 95 62 63 186 187 188 189 190 191 192 193 194 96 58 35 64 39 61 34 195 97
            98 99 100 101 102 103 104 105 196 197 198 199 200 201 202 106 107 108 109
            110 111 112 113 114 203 204 205 206 207 208 209 126 115 116 117 118 119 120
            121 122 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226
            227 228 229 230 231 123 65 66 67 68 69 70 71 72 73 232 233 234 235 236 237
            125 74 75 76 77 78 79 80 81 82 238 239 240 241 242 243 92 159 83 84 85 86 87
            88 89 90 244 245 246 247 248 249 48 49 50 51 52 53 54 55 56 57 250 251 252
            253 254 255'''.split()
        ]
        s, t = bytearray(a2e), bytearray(e2a)
        return s.maketrans(s, t), s.maketrans(t, s)
    def ConvertToNumber(s, handle_i=True):
        '''This is a general-purpose routine that will return a python number for a string if it is
        possible.  The basic logic is:
            - If it contains 'j' or 'J', it's complex
            - If it contains '/', it's a fraction
            - If it contains ',', '.', 'E', or 'e', it's a float
            - Otherwise it's interpreted as an integer
        Since I prefer to use 'i' for complex numbers, we'll also allow an 'i' in the number unless
        handle_i is False.
        '''
        s = s.lower()
        if handle_i:
            s = s.replace("i", "j")
        if "j" in s:
            return complex(s)
        elif "." in s or "e" in s or "," in s:
            return float(s)
        elif "/" in s:
            return fractions.Fraction(s)
        else:
            return int(s)
    class astr(str):
        '''This is a string object that uses a regular expression to remove
        ANSI color-coding strings before calculating the string length.
        '''
        # This regular expression is used to replace color-coding escape sequence with the
        # empty string.  See https://en.wikipedia.org/wiki/ANSI_escape_code.
        r = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
        def __len__(self):
            return len(astr.r.sub("", str(self)))
    def alen(s):
        'Function to get the length of a string, ignoring any ANSI escape sequences'
        return len(astr.r.sub("", s))
    def Len(string):
        "Return the length of a string with ANSI escape sequences removed"
        return len(ANSI_strip(string))
    def ANSI_strip(string):
        '''Return the string with ANSI escape sequences removed.  16 Feb 2023 Suggested
        regexp from
        https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
        (see the answer below this answer, as it is a more general regexp).
        '''
        r = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        return r.sub("", string)
    def BuildTagsFile(dir, files, verbose=False, dbg=False):
        '''Construct a tags file for the indicated directory.
          dir       Directory where the files reside
          files     Sequence of file names
          verbose   If True, print where tags file constructed
          
        For vim's help files, this is done by searching for text between two asterisk characters
        and extracting the tag.  This is written to the tags file in the form
        
            symbol\tsymbol.hld\t/*symbol*
            
        and the file is sorted on these lines.  The first line of the file must be
        'help-tags\ttags\t1'.
        '''
        if not files and verbose:
            print("BuildTagsFile:  no files found in files sequence", file=sys.stderr)
            return
        # Make sure dir is a string or a Path instance
        Assert(isinstance(dir, (str, pathlib.Path)))
        # Make sure files is an iterable
        Assert(dpseq.IsIterable(files))
        # Make sure each item in files is a string or Path instance
        Assert(all(isinstance(i, (str, pathlib.Path)) for i in files))
        # Our working directory is an invariant
        cwd = os.getcwd()
        # regex is a C-type token name between asterisks
        r = re.compile(r"\*([A-Za-z_][A-Za-z0-9_]*)\*")
        tags = ["help-tags\ttags\t1"]
        # Change to the output directory so there will be no directory names in the file's name
        os.chdir(dir)
        for file in files:
            p = pathlib.Path(file) if isinstance(file, str) else file
            with p.open() as f:
                for line in f.readlines():
                    line = line.rstrip()
                    mo = r.search(line)
                    if mo:
                        for tag in mo.groups():
                            t = f"{tag}\t{file}\t/*{tag}*"
                            tags.append(t)
                        if dbg:
                            print(f"tag(s) found in [{file}]:  {line!r}")
        # Get rid of duplicates
        tags = list(sorted(list(set(tags))))
        n = len(tags) - 1
        # Write the tags file
        tagsfile = pathlib.Path("tags")
        with tagsfile.open("w") as f:
            f.write("\n".join(tags))
            f.write("\n")
        if verbose:
            print(f"{n} tags constructed in {tagsfile.absolute()}")
        # Go back to the directory we started from
        os.chdir(cwd)

if __name__ == "__main__":
    if 1:   # Standard imports
        import contextlib
        import io
        import math
        import os
    if 1:   # Custom imports
        import lwtest
    if 1:   # Import symbols
        Assert = lwtest.Assert
        assert_equal = lwtest.assert_equal
        raises = lwtest.raises
        run = lwtest.run
        t = trm.Trm()
    def Test_RegexpDecorate():
        u = trm.Trm()
        rd = RegexpDecorate(u)
        r = re.compile(r"[Mm]adison")
        # Note fg and bg must be escape sequences
        fg = u.yel
        bg = u.n
        rd.register(r, fg, bg)    # Print matches in light yellow on black
        f = io.StringIO()
        rd("Dolly\n", file=f) 
        rd("Madison", file=f) 
        s = f.getvalue()
        expected = (    # Check actual escape codes
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m"     # u.n
            "Dolly\n"
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m"     # u.n
            
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m"     # u.n
            "\x1b[38;2;254;239;0m"                              # u.yel
            "Madison"
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m")    # u.n
        Assert(s == expected)
        # This is what should happen
        expected = u.n + "Dolly\n" + u.n + u.n + u.yel + "Madison" + u.n
        Assert(s == expected)
    def Test_Decorate():
        s = "www \t\n\r\f\vzzz"
        Assert(Decorate(s) == "www·␉␊␍␌␋zzz")
        b = b"www \x08\t\n\r\f\vzzz"
        Assert(Decorate(b) == "www·␈␉␊␍␌␋zzz")
    def Test_IgnoreFilter():
        seq = [ "Bob", "bob", "bobwhite", "Carol", "carol", "Alice" ]
        # Empty sequence is identity function
        f = IgnoreFilter([])
        Assert(f(seq) == seq)
        # Don't ignore case
        f = IgnoreFilter(["bob", "carol"])
        Assert(f(seq) == ['Bob', 'Carol', 'Alice'])
        # Ignore case
        f = IgnoreFilter(["bob", "carol"], ignore_case=True)
        Assert(f(seq) == ['Alice'])
    def Test_GetTransFunc():
        From = '''Mr. Dee, a, a--b; 'z' and "a", ok.'''
        expected = '''r  Dee  a  a  b   z  and  a   ok '''
        f = GetTransFunc(string.punctuation, " ", delete="M")
        got = f(From)
        Assert(got == expected)
    def Test_Trim():
        for s in ("", "a", "abc"):
            Assert(Trim(s) == s)
        u = "a b"
        s = f" {u} "
        cs = " "
        Assert(Trim(s, chars=cs) == f"{u}")
        Assert(Trim(s, chars=cs, left=True, right=False) == f"{u} ")
        Assert(Trim(s, chars=cs, left=False, right=True) == f" {u}")
        Assert(Trim(s, chars=cs, left=True, right=True) == f"{u}")
        # Test when s is a subset of chars
        s = "aaaaaaaaaa"
        cs = "eoirtjwpo op4er9qorja"
        Assert(Trim(s, chars=cs, check=True) == "")
        Assert(Trim(s, chars=cs, left=True, right=False, check=True) == "")
        Assert(Trim(s, chars=cs, left=False, right=True, check=True) == "")
        Assert(Trim(s, chars=cs, left=True, right=True, check=True) == "")
    def Test_Keep():
        Assert(Keep("", "") == "")
        Assert(Keep("", "a") == "")
        Assert(Keep("a", "") == "")
        # Works on strings
        Assert(Keep("abc", "bc") == "bc")
        Assert(Keep("abc", "bc", whole=True) == "bc")
        # Works on list sequence
        A, B = "a b c".split(), "b c".split()
        Assert(Keep(A, B) == B)
        # Using keywords
        s = "a;bc;d;"
        keep = string.ascii_lowercase
        Assert(Keep(s, keep, left=True) == "a")
        t = Keep(s, keep, middle=True)
        Assert(t == ";bc;d;")
        Assert(Keep(t, keep) == "bcd")
        Assert(Keep(s, keep, right=True) == "")
    def Test_KeepFilter():
        f = KeepFilter("bc")
        Assert(f("abc") == "bc")
    def Test_Remove():
        Assert(Remove("", "ab") == "")
        Assert(Remove("ab", "") == "ab")
        Assert(Remove("abc", "cb") == "a")
    def Test_RemoveFilter():
        f = RemoveFilter("bc")
        Assert(f("abc") == "a")
    def Test_FindNotIn():
        # Tests are only on strings, but they should work for any sequence
        if 1:  # FindFirstIn, FindLastIn
            F, L = FindFirstIn, FindLastIn
            Assert(F("", "abc") is None)
            Assert(L("", "abc") is None)
            Assert(F("abc", "") is None)
            Assert(L("abc", "") is None)
            Assert(F("abc", "d") is None)
            Assert(L("abc", "d") is None)
            #
            Assert(F("dabc", "d") == 0)
            Assert(L("dabc", "d") == 0)
            Assert(F("abc;d", ";") == 3)
            Assert(L("abc;de", ";") == 3)
            Assert(L("abc;", ";") == 3)
            Assert(L(";abc;", ";") == 4)
        if 1:  # FindFirstNotIn, FindLastNotIn
            F, L = FindFirstNotIn, FindLastNotIn
            Assert(F("", "abc") is None)
            Assert(L("", "abc") is None)
            Assert(F("abc", "") is None)
            Assert(L("abc", "") is None)
            #
            Assert(F("abc", "d") == 0)
            Assert(L("abc", "d") == 2)
            Assert(F("dabc", "d") == 1)
            Assert(L("dabc", "d") == 3)
            Assert(F("abc;d", string.ascii_letters) == 3)
            Assert(L("abc;de", string.ascii_letters) == 3)
            Assert(L("abc;", string.ascii_letters) == 3)
            Assert(L(";abc;", string.ascii_letters) == 4)
    def Test_FindStrings():
        seq = "Jan Feb Mar".split()
        str = "1Jan2001"
        found = FindStrings(seq, str)
        Assert(found == [(0, 1)])
        # Show case insensitivity works
        str = "1jan2001"
        found = FindStrings(seq, str, ignorecase=True)
        Assert(found == [(0, 1)])
        # Show get empty list on no matches
        str = ""
        found = FindStrings(seq, str, ignorecase=True)
        Assert(not found)
    def Test_Scramble():
        random.seed("0")
        s = '"Yes", said John. Åé—'
        s1 = Scramble(s)
        Assert(s1 == '"sYe", dsai ohnJ. —éÅ')
        # Don't modify first and last characters in word
        s1 = Scramble(s, start_end_const=True)
        Assert(s1 == '"Yes", siad John. Åé—')
        # Use only space as punctuation
        s = "oblong clink calf"
        s1 = Scramble(s)
        Assert(s1 == "nbgloo lncik lafc")
    def Test_IsASCII():
        s1, s2 = "abc", "abc∞"
        # RemoveASCII
        Assert(RemoveASCII(s1) == "")
        Assert(RemoveASCII(s2) == "∞")
        Assert(IsASCII(s1))
        # IsASCII
        Assert(IsASCII(""))
        Assert(not IsASCII(s2))
    def Test_GetWhitespace():
        for u in (
            "",
            " ",
            "  ",
            "\t",
            "\n",
            "\t\r\n\f    \t\t\t",
        ):
            Assert(GetStartingChars(u) == u)
            Assert(GetStartingChars(u + "a") == u)
            Assert(GetEndingChars(u) == u)
            Assert(GetEndingChars("a" + u) == u)
        # Define custom sets of whitespace
        if 1:  # Leading
            Assert(GetStartingChars("  \t  a", chars="z") == "")
            Assert(GetStartingChars("  \t  a", chars="\t") == "")
            Assert(GetStartingChars("  \t  a", chars=" ") == "  ")
            ws, u = ".;:", ".;..:::."
            a = GetStartingChars(u + "a", chars=ws)
            Assert(a == u)
        if 1:  # Trailing
            Assert(GetEndingChars("a  \t  ", chars="z") == "")
            Assert(GetEndingChars("a  \t  ", chars="\t") == "")
            Assert(GetEndingChars("a  \t  ", chars=" ") == "  ")
            ws, u = ".;:", ".;..:::."
            a = GetEndingChars("a" + u, chars=ws)
            Assert(a == u)
    def Test_Tokenize():
        Assert(Tokenize("", check=True) == [])
        Assert(Tokenize(" ", check=True) == [" "])
        Assert(Tokenize(" "*2, check=True) == [" ", " "])
        s = "How so?  How can it affect them?"
        t = Tokenize(s, check=True)
        u = [
            "How",
            " ",
            "so",
            "?",
            " ",
            " ",
            "How",
            " ",
            "can",
            " ",
            "it",
            " ",
            "affect",
            " ",
            "them",
            "?",
        ]
        Assert(t == u)
        # Using a comment string (makes sure the last word is there)
        s = "# A b"
        t = Tokenize(s, check=True)
        Assert(t == ["#", " ", "A", " ", "b"])
    def Test_Str():
        a, b, c = f"{t('wht')}", "mystr", t.n
        s = Str(a + b + c)
        Assert(len(s) == len(b))
        s.on = False
        Assert(len(s) == len(a + b + c))
    def Test_Len():
        s = "simple string"
        Assert(len(s) == Len(s))
        Assert(RmEsc(s) == s)
        s = wrap.dedent(f'''
        This is some multiline
        text with {t("purl")}some
        escape codes.{t.n}
        ''')
        u = RmEsc(s)
        Assert(Len(s) == len(u))
    def Test_ReadData():
        data = ''' #
                    9 , 680  ,  2100  , 0  ,    750
                    10,  680  ,  2100  , 250    ,750
        '''
        o = ReadData(data, structure=[str, int, int, int, int], sep=",", comment="#")
        # Note the space after '9'
        e = [["9 ", 680, 2100, 0, 750], ["10", 680, 2100, 250, 750]]
        Assert(o == e)
        o = ReadData(data, structure=[str, f.flt, int, int, int], sep=",", comment="#")
        e = [["9 ", f.flt(680), 2100, 0, 750], ["10", f.flt(680), 2100, 250, 750]]
        Assert(o == e)
        data = '''
                    9  680    2100   0      750
                        10  680    2100   250    750
        '''
        o = ReadData(data, structure=[str, int, int, int, int])
        e = [["9", 680, 2100, 0, 750], ["10", 680, 2100, 250, 750]]
        Assert(o == e)
    def Test_Chop():
        s = "10f6b8a"
        L = Chop(s, 2)
        Assert(L == ["10", "f6", "b8", "a"])
        s = ""
        L = Chop(s, 2)
        Assert(L == [])
        # Works with sequences
        s = (1, 2, 3, 4, 5)
        L = Chop(s, 2)
        Assert(L == [(1, 2), (3, 4), (5,)])
    def Test_MatchCapitalization():
        t = "AbCdEf"
        # s needs to have as many characters as t
        raises(ValueError, MatchCapitalization, "", t)
        # Empty string returns empty string
        Assert(MatchCapitalization("", "") == "")
        Assert(MatchCapitalization(t, "") == "")
        # No letters in s just gets t back if length sufficient
        Assert(MatchCapitalization("......", t) == t)
        # Idempotent
        Assert(MatchCapitalization(t, t) == t)
        Assert(MatchCapitalization("", "") == "")
        # Routine use
        Assert(MatchCapitalization(t.lower(), t) == t.lower())
        Assert(MatchCapitalization(t.upper(), t) == t.upper())
        Assert(MatchCapitalization("T", "t") == "T")
        Assert(MatchCapitalization("t", "T") == "t")
        Assert(MatchCapitalization("MatchCapitalization", t) == "AbcdeF")
        Assert(MatchCapitalization("MATCHCAP", t) == "ABCDEF")
        Assert(MatchCapitalization("matchcap", t) == "abcdef")
        Assert(MatchCapitalization("matchcap", t) == "abcdef")
        # Check example given in function's docstring
        s = "StuVwxyz"
        t = "abcd"
        Assert(MatchCapitalization(s, t) == "AbcD")
    def Test_soundex():
        test_cases = (
            ("Euler", "E460"),
            ("Gauss", "G200"),
            ("Hilbert", "H416"),
            ("Knuth", "K530"),
            ("Lloyd", "L300"),
            ("Lukasiewicz", "L222"),
            ("chute", "C300"),
            ("shoot", "S300"),
            ("a", "A000"),
            ("A", "A000"),
        )
        for s, expected in test_cases:
            Assert(soundex(s) == expected)
        Assert(soundex("a") == "A000")
        raises(ValueError, soundex, "")
        raises(ValueError, soundex, " ")
        raises(ValueError, soundex, ".")
    def Test_SoundSimilar():
        Assert(SoundSimilar("bob", "bib"))
        Assert(SoundSimilar("mike", "make"))
        Assert(SoundSimilar("mike", "muke"))
        Assert(SoundSimilar("mike", "moke"))
        Assert(SoundSimilar("mike", "meke"))
        Assert(SoundSimilar("don", "dan"))
        Assert(SoundSimilar("don", "din"))
        Assert(not SoundSimilar("robert", "rabbit"))
        Assert(not SoundSimilar("aorta", "rabbit"))
    def Test_CommonPrefix():
        Assert(not CommonPrefix(["a", "b"]))
        Assert("a" == CommonPrefix(["aone", "atwo", "athree"]))
        Assert("abc" == CommonPrefix(["abc", "abc", "abc"]))
        Assert("abc" == CommonPrefix(["abc", "abc", "abcd"]))
        Assert("abc" == CommonPrefix(["abc", "abcd", "abce"]))
        raises(TypeError, CommonPrefix, ["a", 1])
    def Test_CommonSuffix():
        Assert(not CommonSuffix(["a", "b"]))
        Assert("a" == CommonSuffix(["onea", "twoa", "threea"]))
        Assert("abc" == CommonSuffix(["abc", "abc", "abc"]))
        Assert("abc" == CommonSuffix(["1abc", "abc", "abc"]))
        Assert("abc" == CommonSuffix(["1abc", "2abc", "abc"]))
        raises(TypeError, CommonSuffix, ["a", 1])
    def Test_FindAll():
        if 1:   # str
            s = "This ∞is an example of a∞ string"
            start, finish = list(FindAll(s, substr="∞"))
            Assert(s[start + 1:finish] == "is an example of a")
        if 1:   # bytes
            s = "This ∞is an example of a∞ string".encode("UTF-8")
            start, finish = list(FindAll(s, substr="∞".encode()))
            n = len("∞".encode())
            Assert(s[start + n:finish] == b"is an example of a")
    def Test_FilterStr():
        s = '''"Not that easy, I'm sure."'''
        f = FilterStr('''"',.''', [None]*4)
        t = f(s)
        Assert(t == "Not that easy Im sure")
    def Test_RemoveWhitespace():
        s = "a b\tc\nd\re\ff\vg"
        t = RemoveWhitespace(s)
        Assert(t == "abcdefg")
    def Test_RemoveEndingChars():
        s = "a b\tc\nd\re\ff\vg"
        e = " b\tc\nd\re\ff\vg"
        v = RemoveEndingChars(s, s)
        Assert(v == "")
        v = RemoveEndingChars(s, e)
        Assert(v == "a")
        v = RemoveEndingChars(s, "")
        Assert(v == s)
    def Test_RemoveStartingChars():
        s = "a b\tc\nd\re\ff\vg"
        e = "a b\tc\nd\re\ff\v"
        v = RemoveEndingChars(s, s)
        Assert(v == "")
        v = RemoveStartingChars(s, e)
        Assert(v == "g")
        v = RemoveStartingChars(s, "")
        Assert(v == s)
    def Test_FindDiff():
        s1 = "hello"
        s2 = "hello there"
        Assert(FindDiff(s1, s2) == -1)
        s1 = "hellx"
        Assert(FindDiff(s1, s2) == 4)
        s1 = ""
        Assert(FindDiff(s1, s2, ignore_empty=True) == 0)
    def Test_FindSubstring():
        #    01234567890
        s = "x  x    x  "
        Assert(FindSubstring(s, "x") == (0, 3, 8))
    def Test_GetChoice():
        names = set(("one", "two", "three", "thrifty"))
        Assert(GetChoice("o", names) == "one")
        Assert(set(GetChoice("th", names)) == set(["three", "thrifty"]))
        Assert(GetChoice("z", names) is None)
    def Test_KeepOnlyLetters():
        s = "\t\n\xf8abcABC123_"
        # digits True
        expected = "   abcABC123"
        t = KeepOnlyLetters(s, underscore=False, digits=True)
        Assert(t == expected + " ")
        t = KeepOnlyLetters(s, underscore=True, digits=True)
        Assert(t == expected + "_")
        # digits False
        expected = "   abcABC"
        t = KeepOnlyLetters(s, underscore=False, digits=False)
        Assert(t == expected + " "*4)
        t = KeepOnlyLetters(s, underscore=True, digits=False)
        Assert(t == expected + " "*3 + "_")
    def Test_StringSplit():
        s = "hello there"
        Assert(StringSplit([4, 7], s) == ["hell", "o t", "here"])
        t = "3s 3x 4s"
        def f(x):
            return bytes(x, encoding="ascii")
        q = [f("hel"), f("ther"), f("e")]
        Assert(StringSplit(t, s, remainder=True) == q)
        Assert(StringSplit(t, s, remainder=False) == q[:-1])
    def Test_NamingConventionConversions():
        cw, us, mc = "AbcDef", "abc_def", "abcDef"
        nc = NameConvert()
        Assert(nc.cw2us(cw) == us)
        Assert(nc.cw2mc(cw) == mc)
        Assert(nc.us2mc(us) == mc)
        Assert(nc.us2cw(us) == cw)
        Assert(nc.mc2us(mc) == us)
        Assert(nc.mc2cw(mc) == cw)
        # No barfing on empty strings
        s = ""
        nc.cw2mc(s)
        nc.cw2us(s)
        nc.mc2cw(s)
        nc.mc2us(s)
        nc.us2cw(s)
        nc.us2mc(s)
        # Check inverses
        Assert(nc.us2cw(nc.cw2us(cw)) == cw)
        Assert(nc.mc2cw(nc.cw2mc(cw)) == cw)
        Assert(nc.cw2mc(nc.mc2cw(mc)) == mc)
        Assert(nc.us2mc(nc.mc2us(mc)) == mc)
        Assert(nc.cw2us(nc.us2cw(us)) == us)
        Assert(nc.mc2us(nc.us2mc(us)) == us)
    def Test_MultipleReplace():
        text = '''This
        is some
        text'''
        patterns = {
            " *": "",
            "\n": "",
            "This": "x",
            "is": "x",
            "some": "x",
            "text": "x",
        }
        result = MultipleReplace(text, patterns)
        Assert(result == "x        x x        x")
    def Test_RemoveComment():
        s = ""
        Assert(RemoveComment(s) == s)
        s = "abc"
        Assert(RemoveComment(s) == s)
        s = " #"
        Assert(RemoveComment(s) == " ")
        s = "a = 1 # kdjjfd"
        Assert(RemoveComment(s, code=True) == "a = 1 ")
        s = "a = '#'"
        try:
            RemoveComment(s, code=True)
            raise Exception("Expected a ValueError exception")
        except ValueError:
            pass
    def Test_SpellCheck():
        input_list = ("dog", "cAt", "hurse")
        word_dictionary = {"dog": "", "cat": "", "horse": "", "chicken": ""}
        s = SpellCheck(input_list, word_dictionary, ignore_case=True)
        Assert(len(s) == 1 and "hurse" in s)
        s = SpellCheck(input_list, word_dictionary, ignore_case=False)
        Assert(len(s) == 2 and "cAt" in s and "hurse" in s)
    def Test_SplitOnNewlines():
        Assert(SplitOnNewlines("1\n2\r\n3\r") == ["1", "2", "3", ""])
    def Test_PrepareMultilineString():
        u = g.sp*10
        s = f"{u}\n{u}line1\n{u}line2\n{u}"
        if 1:   # Normal usage
            x = PrepareMultilineString(s)
            lines = x.split(g.nl)
            Assert(len(lines) == 2)
            Assert(lines[0] == u + "line1")
            Assert(lines[1] == u + "line2")
        if 1:   # Use only trim_start = True
            x = PrepareMultilineString(s, trim_end=False)
            lines = x.split(g.nl)
            Assert(lines[0] == u + "line1")
            Assert(lines[1] == u + "line2")
            Assert(lines[2] == u)
        if 1:   # Use only trim_end = True
            x = PrepareMultilineString(s, trim_start=False)
            lines = x.split(g.nl)
            Assert(lines[0] == u)
            Assert(lines[1] == u + "line1")
            Assert(lines[2] == u + "line2")
        # Too few newlines
        raises(ValueError, PrepareMultilineString, u)
    def Test_CountLeadingSpaces():
        f = CountLeadingSpaces
        if 1:   # Show it works if no trimming done
            Assert(f("", trim_start=False, trim_end=False) == 0)
            Assert(f(" ", trim_start=False, trim_end=False) == 1)
            Assert(f("  ", trim_start=False, trim_end=False) == 2)
            Assert(f("   ", trim_start=False, trim_end=False) == 3)
            Assert(f(" \n", trim_start=False, trim_end=False) == 1)
            Assert(f(" \n\n", trim_start=False, trim_end=False) == 1)
            Assert(f(" \n\n\n", trim_start=False, trim_end=False) == 1)
            Assert(f("  \n", trim_start=False, trim_end=False) == 2)
        if 1:   # Show it works for left trimming
            Assert(f(" ", trim_start=True, trim_end=False) == 0)
            Assert(f(" \n", trim_start=True, trim_end=False) == 0)
            Assert(f("  \n", trim_start=True, trim_end=False) == 0)
            Assert(f("   \n", trim_start=True, trim_end=False) == 0)
            Assert(f(" \n ", trim_start=True, trim_end=False) == 1)
            Assert(f("  \n ", trim_start=True, trim_end=False) == 1)
            Assert(f("  \n  ", trim_start=True, trim_end=False) == 2)
        if 1:   # Show it works for right trimming
            Assert(f(" ", trim_start=False, trim_end=True) == 0)
            Assert(f("\n  ", trim_start=False, trim_end=True) == 0)
            Assert(f(" \n  ", trim_start=False, trim_end=True) == 1)
            Assert(f("  \n  ", trim_start=False, trim_end=True) == 2)
    def Test_FindSymbol():
        filelist = ["dpstr.py"]
        found = FindSymbol("FindSymbol", filelist=filelist)
        Assert(found == ['dpstr.py'])
        found = FindSymbol("findsymbol", filelist=filelist, ignore_case=True)
        Assert(found == ['dpstr.py'])
        found = FindSymbol("nowayray", filelist=filelist)
        Assert(found == [])
    def Test_FilterSeqRegex():
        from lwtest import Assert
        # With no regexes, it's the identity unless the sequence contains a non-string
        s = "str1 str2 str3 str4 str5"
        s1 = s.split()
        s2 = s1 + [10]
        Assert(FilterSeqRegex([]) == [])
        Assert(FilterSeqRegex(s1, regexes=[]) == s1)
        Assert(FilterSeqRegex(s2, regexes=[]) == s1)
        # ANDing the regexes
        Assert(FilterSeqRegex(s1, regexes=["[123]", "[1]"]) == ["str1"])
        # ORing the regexes
        Assert(FilterSeqRegex(s1, regexes=["[123]", "[1]"], ANDed=False) == ["str1", "str2", "str3"])
        # re flag works
        Assert(FilterSeqRegex(s.upper().split(), regexes=["str1"], re_flags=re.I) == ["STR1"])
    def Test_RemoveCharClass():
        '''Note the tests cover strings, bytes, and bytearrays.  Test cases:
            A   Convert Unicode characters to rough ASCII equivalents
            B   Remove characters under 0x20
            b   Remove characters under 0x20 except newline
            d   Remove characters that are ASCII digits (∈ string.digits)
            h   Remove characters that are hex digits (∈ string.hexdigits)
            l   Remove lower case letters (∈ string.ascii_lowercase)
            n   Remove punctuation (∈ string.punctuation)
            o   Remove characters that are octal digits (∈ string.octdigits)
            p   Remove non-printable characters (∉ string.printable)
            u   Remove upper case letters (∈ string.ascii_uppercase)
            W   Remove whitespace (∈ string.whitespace)
            w   Remove whitespace except newlines
            7   Remove characters above 0x7f (i.e., keep only 7-bit characters)
            8   Remove characters above 0xff (i.e., keep only 8-bit characters)
        '''
        def mk(s):  # Turn string s into (string, bytes, bytearray)
            return (s, bytes(s.encode()), bytearray(s.encode()))
        def Check(s, b, a, keys, s_exp, b_exp, a_exp):
            Assert(f(s, keys=keys) == s_exp)
            Assert(f(b, keys=keys) == b_exp)
            Assert(f(a, keys=keys) == a_exp)
        f = RemoveCharClass
        if 1:   # No keys => identity xfm
            s, b, a = mk("∞©")
            Check(s, b, a, "", s, b, a)
        if 1:   # A
            s, b, a = mk("∞©")
            Check(s, b, a, "A", "oo(C)", b, a)
        if 1:   # B
            s, b, a = mk("a\t\n\r\x0b\x0cb")
            Check(s, b, a, "B", "ab", b"ab", bytearray(b"ab"))
        if 1:   # b
            s, b, a = mk("a\t\n\r\x0b\x0cb")
            Check(s, b, a, "b", "a\nb", b"a\nb", bytearray(b"a\nb"))
        if 1:   # d
            s, b, a = mk("a0123456789b")
            Check(s, b, a, "d", "ab", b"ab", bytearray(b"ab"))
            Assert(f(s, keys="d") == "ab")
            Assert(f(string.digits, keys="d") == "")
        if 1:   # h
            s = "g0123456789abcdefh"
            s, b, a = mk("g0123456789abcdefh")
            Check(s, b, a, "h", "gh", b"gh", bytearray(b"gh"))
        if 1:   # l
            s, b, a = mk("g0123456789abcdefh")
            Check(s, b, a, "l", "0123456789", b"0123456789", bytearray(b"0123456789"))
        if 1:   # n
            s, b, a = mk("a;,!b")
            Check(s, b, a, "n", "ab", b"ab", bytearray(b"ab"))
            s, b, a = mk(string.punctuation)
            Check(s, b, a, "n", "", b"", bytearray(b""))
        if 1:   # o
            s, b, a = mk("a012345678b")
            Check(s, b, a, "o", "a8b", b"a8b", bytearray(b"a8b"))
            s, b, a = mk(string.octdigits)
            Check(s, b, a, "o", "", b"", bytearray(b""))
        if 1:   # p
            s, b, a = mk("\x00aA0∞\n")
            Check(s, b, a, "p", "aA0\n", b"aA0\n", bytearray(b"aA0\n"))
            s, b, a = mk(string.printable)
            Check(s, b, a, "p", s, b, a)
        if 1:   # u
            s, b, a = mk(string.ascii_uppercase)
            Check(s, b, a, "u", "", b"", bytearray(b""))
        if 1:   # W
            s, b, a = mk("∞ D\t\n\r\v\f:")
            e = "∞D:".encode()
            Check(s, b, a, "W", "∞D:", e, bytearray(e))
        if 1:   # w
            s, b, a = mk("∞ D\t\n\r\v\f:")
            e = "∞D\n:".encode()
            Check(s, b, a, "w", "∞D\n:", e, bytearray(e))
        if 1:   # 7
            s, b, a = mk("∞©a(.;38fzK~")
            e = b"a(.;38fzK~"
            Check(s, b, a, "7", "a(.;38fzK~", e, bytearray(e))
        if 1:   # 8
            u = "a∞ăĂāĀÿ"
            s, b, a = mk(u)
            # Note this is the identity transformation for a and b
            Check(s, b, a, "8", "aÿ", b, a)
        if 1:   # 0
            s, b, a = mk("∞©")
            Check(s, b, a, "0", s, b, a)
        if 1:   # Check passed key characters
            keys = list(f.allowed_keys)
            f("", keys=keys)
            raises(ValueError, f, "", keys=keys + ["x"])
    if 1:   # Test old util stuff
        def Test_StringToNumbers():
            s = "4j 3/5 6. 7"
            Assert(StringToNumbers(s) == (4j, fractions.Fraction(3, 5), 6.0, 7))
        def Test_RemoveIndent():
            s = '''
            This is a test
                Second line
              Third line
            '''
            n = 12  # Depends on how much this code is indented
            lines = RemoveIndent(s, numspaces=n).split("\n")
            Assert(lines[0] == "")
            Assert(lines[1] == "This is a test")
            Assert(lines[2] == "    Second line")
            Assert(lines[3] == "  Third line")
            Assert(lines[4] == "")
        def Test_GetLeadingString():
            if 1:   # GetLeadingString
                f = GetLeadingString
                # Test with bytes
                Assert(f(b'zzzHi', prefix=b'z') == b'zzz') 
                # Test with string
                s = 'zzzHi'
                Assert(f(s, prefix='z') == 'zzz') 
                Assert(f(s, prefix='zz') == 'zz') 
                Assert(f(s, prefix='zzz') == 'zzz') 
                Assert(f('ababHi', prefix='ab') == 'abab') 
                Assert(f('abbaHi', prefix='ab') == 'ab') 
            if 1:   # GetTrailingString
                f = GetTrailingString
                # Test with bytes
                Assert(f(b'Hizzz', suffix=b'z') == b'zzz') 
                # Test with string
                s = 'Hizzz'
                Assert(f(s, suffix='z') == 'zzz') 
                Assert(f(s, suffix='zz') == 'zz') 
                Assert(f(s, suffix='zzz') == 'zzz') 
                Assert(f('Hiabab', suffix='ab') == 'abab') 
                Assert(f('Hiabba', suffix='ba') == 'ba') 
        def Test_GetHash():
            lwtest.ToDoMessage("Need to write test")

        def Test_EBCDIC():
            a2e, e2a = EBCDIC()
            # Show that these byte translation tables are inverses
            a = bytearray(range(256))
            e = a.translate(a2e)
            a1 = e.translate(e2a)
            Assert(a == a1)
        def Test_ConvertToNumber():
            Assert(ConvertToNumber("1+i") == 1 + 1j)
            Assert(ConvertToNumber("1+j") == 1 + 1j)
            Assert(ConvertToNumber("j") == 1j)
            Assert(ConvertToNumber("1.") == 1)
            Assert(ConvertToNumber("1e2") == 1e2)
            Assert(ConvertToNumber("1E2") == 1e2)
            Assert(ConvertToNumber("1/2") == fractions.Fraction(1, 2))
            Assert(ConvertToNumber("1") == 1)
            n = 10**50  # Large integer
            Assert(ConvertToNumber(str(n)) == n)
        def Test_alen_astr():
            # Note the Unicode '∞' in the third line.
            tststring = wrap.dedent('''
            [1;37;42mstring1[0m
            string2
            [1;36mstring3∞[0m''')
            for i, s in enumerate(tststring.split("\n")):
                a = astr(s)
                if i in (0, 1):
                    assert_equal(len(a), 7)
                    assert_equal(alen(s), 7)
                else:
                    assert_equal(len(a), 8)
                    assert_equal(alen(s), 8)
        def Test_Len_ANSI_strip():
            "Also test ANSI_strip"
            s = "hello world"
            Assert(Len(s) == 11)
            s = "\x1b[38;2;198;174;239m12.578\x1b[38;2;192;192;192m\x1b[48;2;0;0;0m\x1b[0m"
            Assert(Len(s) == 6)
            u = ANSI_strip(s)
            Assert(u == "12.578")
    def Test_BuildTagsFile():
        '''Test this in my ~/.manpages directory where there is a collection of *.hld files.
        Manual verification has proven the method works, so now running this file is the way to
        rebuild my ~/.manpages directory's tags file.
        '''
        dir = pathlib.Path("/home/don/.manpages")
        files = list(dir.glob("*.hld"))
        BuildTagsFile(dir, files, dbg=False)
    def Demo():
        "Demonstrate the various functions to stdout"
        t.print(f"{t('ornl')}Demo of /plib/dpstr.py functions")
        if 1:
            # Chop
            s = "abcdefghij"
            print(f"Chop({s!r}, 3) = {Chop(s, 3)}")
            # CommonPrefix and CommonSuffix
            s = ["a.b.c", "a.c.c", "a.d.c"]
            print(f"CommonPrefix({s!r}) = {CommonPrefix(s)}")
            print(f"CommonSuffix({s!r}) = {CommonSuffix(s)}")
            # FilterStr
            print(wrap.dedent('''
 
            FilterStr() returns a function that can replace a sequence of characters
            with a corresponding sequence from another equally-sized list of characters.''')
            )
            s = "abc"
            u = "αβɣ"
            print(f"  Characters to remove  :  {s!r}")
            print(f"  Replacement characters:  {u!r}")
            f = FilterStr(s, u)
            o = "abc are the leading characters of the alphabet"
            print(f"  Original   :  '{o}'")
            print(f"  Transformed:  '{f(o)}'")
            # FindFirstIn, FindLastIn, etc.
            s = "abc Are the leading characTers of the alphabet"
            items = string.ascii_uppercase
            from ruler import Ruler
            r = Ruler(0, zb=True)
            print("FindFirstIn, FindLastIn, FindFirstNotIn, FindLastNotIn")
            print("  Test string s is:")
            for i in r(len(s)).split("\n"):
                print(f"    {i}")
            print(f"    {s}")
            print(f"  items argument is {items!r}")
            print("  The functions return the 0-based index of the found item")
            print(f"    FindFirstIn(s, items) = {FindFirstIn(s, items)} (A)")
            print(f"    FindLastIn(s, items)  = {FindLastIn(s, items)} (T)")
            items = string.ascii_lowercase
            print(f"  items argument is {items!r}")
            print(f"    FindFirstNotIn(s, items) = {FindFirstNotIn(s, items)} (space)")
            print(f"    FindLastNotIn(s, items)  = {FindLastNotIn(s, items)} (space)")
            # FindDiff
            a, b = "abc", "aBc"
            print(f"FindDiff({a!r}, {b!r}) = {FindDiff(a, b)}")
            # FindStrings
            a = "Jan Feb Mar".split()
            b = "1Jan2001"
            print(f"FindStrings({a!r}, {b!r}) = {FindStrings(a, b)}")
            # FindSubstring
            mystring = "cat rat hat"
            substring = "at"
            print(
                f"FindSubtring({mystring!r}, {substring!r}) = "
                f"{FindSubstring(mystring, substring)}"
            )
            # GetStartingChars, GetEndingChars
            s = "this STRING HAS UPPER AND LOWER CASE letters"
            chars = string.ascii_lowercase
            print(
                f"GetStartingChars({s!r},\n {' '*15}{chars!r}) = "
                f"{GetStartingChars(s, chars)}"
            )
            # IsASCII
            s, u = "abc", "∞"
            print(f"IsASCII({s!r}) = {IsASCII(s)}, IsASCII({u!r}) = {IsASCII(u)}")
            # Keep
            print("Keep is used to keep only desired elements in a sequence")
            s, items = "a;bc;d;", string.ascii_lowercase
            print(f"  items = desired elements = {items!r}")
            print(f"  Keep({s!r}, items) returns {Keep(s, items)!r}")
            print(
                f"  Keep({s!r}, items, left=True) returns {Keep(s, items, left=True)!r}"
            )
            print(
                f"  Keep({s!r}, items, middle=True) returns {Keep(s, items, middle=True)!r}"
            )
            print(
                f"  Keep({s!r}, items, right=True) returns {Keep(s, items, right=True)!r}"
            )
            # KeepFilter
            print("KeepFilter returns a filter based on Keep's arguments")
            print("  f = KeepFilter returns a filter based on Keep's arguments")
            f = KeepFilter(string.ascii_lowercase)
            print("  f = KeepFilter(string.ascii_lowercase + )")
            s = "this STRING"
            print(f"  f({s!r}) = {f(s)}")
        # KeepOnlyLetters
        s = "88; Hello    there!"
        print(f"KeepOnlyLetters({s!r}) = {KeepOnlyLetters(s)!r}")
        # MatchCapitalization
        s = "StuVwxyz"
        u = "abcd"
        print(f"MatchCapitalization({s!r}, {u!r}) = {MatchCapitalization(s, u)!r}")
        # Decorate
        s = " \t\n\r\f\v"
        print(f"Decorate({s!r}) = {Decorate(s)!r}")
        t.print(end="")
    if len(sys.argv) > 1:
        Demo()
        exit()
    exit(run(globals(), regexp="^Test", halt=1)[0])

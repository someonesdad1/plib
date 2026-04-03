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
    GetString           Return string from user that matches choices
    IgnoreFilter        Return a function which removes ignored strings
    IsASCII             Return True if string is all ASCII characters
    Keep                Return items in sequence that are in keep sequence
    KeepFilter          Returns a function that keeps a set of items in a sequence
    KeepOnlyLetters     Replace all non-word characters with spaces
    CountLeadingSpaces  Return the number of leading or trailing spaces in a string
    Len                 Length of string with ANSI escape sequences removed
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
            - ∞∞2 Many functions: divide docstring into multiple categories and then divide
              the code up into the same sections with 'if 1:    # Section' strings.
    
        oo>
    '''
    if 1:   # Standard imports
        import collections
        import fractions
        import functools
        import hashlib
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
        # This is used by RmEsc and is put here in a "private" variable.  The re module
        # keeps its own global cache, so there's no need for RmEsc to cache it.
        # This regexp was constructed from the information given on the
        # page https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences
        # This is:
        #     esc [
        #     then "parameter bytes":    zero or more bytes 0x30-0x3f       [0-?]
        #     then "intermediate bytes": zero or more bytes 0x20-0x2f       [ -/]
        #     then "single byte":        one byte in range of 0x40-0x7e     [@-~]
        _RE_ANSI_CSI = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
    if 1:   # Type information
        T = ty.TypeVar("T")
        # Python's basic numbers for use with StringToNumbers
        TNum = int | float | complex | fractions.Fraction
        # AnyStr ensures that if you pass str, you get str; if bytes, you get bytes.
        AnyStr = ty.TypeVar("AnyStr", str, bytes)
        # SupportsWrite is an output Protocol that is usually sys.stdout, but can also
        # be an output file stream or hardware buffer.
        # ∞∞1 This needs work, as StringIO only fits the 'write(self, str, /) -> int'
        # pattern
        @ty.runtime_checkable
        class SupportsWrite(ty.Protocol):
            def write(self, s: str, /) -> int: ...
        Iterable = collections.abc.Iterable
        Container = collections.abc.Container
        Callable = collections.abc.Callable
        
        class Hashable:     # Duplicate of what's in dpseq.py ∞∞1 Need canonical location
            '''Internal wrapper to force hashability on heterogeneous/unhashable items.
        
            If you want to have things like the integer 1 NOT compare equal to 1.0, then 
            set the instance's typ attribute to True.  In regular python, bool(1 == 1.0)
            is True.
            '''
            __slots__ = ("object", "typ")
            def __init__(self, object: ty.Any, typ: bool = False) -> None:
                self.object = object
                self.typ = bool(typ)
            def __hash__(self) -> int:
                if self.typ:
                    return hash(repr(self.object))
                try:
                    return hash(self.object)
                except TypeError:
                    # Fallback to repr for unhashable types (lists, dicts, etc.)
                    return hash(repr(self.object))
            def __eq__(self, other: ty.Any) -> bool:
                if not isinstance(other, Hashable):
                    return False
                eqval = bool(self.object == other.object)
                if self.typ:
                    return eqval and (type(self.object) is type(other.object))
                return eqval

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
    class RegexpDecorate_OLD:
        '''Decorate regular expression matches with color
        
        You must initialize an instance with a trm.Trm instance.  If you don't, a
        default Trm instance will be used.
        
        The styles attribute is a dictionary that contains the styles to apply for each
        regexp's match (key is the compiled regexp).  The style is a tuple of 1 to 3
        values:  fg (foreground) color, bg (background) color, and text attributes.
        None means to use the default.
        
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
            self._u: ty.Any = mytrm if mytrm is not None else trm.Trm()
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

    class RegexpDecorate:
        '''
        Decorate regular expression matches with terminal color codes.
        Uses a master regex for single-pass high-speed decoration.
        '''
        def __init__(self, mytrm: ty.Any|None=None) -> None:
            self._styles: dict[str, tuple[str, str]] = {}
            self._master_re: re.Pattern|None = None
            # self._u is our trm.Trm instance for escape codes
            self._u = mytrm if mytrm is not None else trm.Trm()
        def register(self, r: re.Pattern, match_style: str, nomatch_style: str|None=None) -> None:
            '''Register a regular expression and its associated terminal styles.'''
            nm = nomatch_style if nomatch_style is not None else self._u.n
            # We use the pattern string as a key; store as (match, nomatch)
            self._styles[r.pattern] = (match_style, nm)
            # Rebuild the master pattern: a giant 'OR' of all registered patterns
            # We wrap each in a named group to identify which style to apply
            pattern_str = "|".join(f"(?P<g{i}>{p})" for i, p in enumerate(self._styles.keys()))
            self._master_re = re.compile(pattern_str)
        def unregister(self, r: re.Pattern) -> None:
            "Remove regexp r from our styles dict"
            if r in self._styles:
                del self._styles[r]     # type: ignore
        def decorate(self, line: str) -> str:
            '''Return a string with all registered matches wrapped in escape codes.'''
            if not self._master_re or not line:
                return line
            def _replace(mo: re.Match) -> str:
                # Find which group matched
                group_name = mo.lastgroup
                idx = int(group_name[1:])       # type: ignore
                pattern_key = list(self._styles.keys())[idx]
                m_style, n_style = self._styles[pattern_key]
                return f"{m_style}{mo.group()}{n_style}"
            # re.sub handles the 'between matches' text automatically
            return self._master_re.sub(_replace, line)      # type: ignore
        def __call__(self, line: str, file: ty.Any=sys.stdout, insert_nl: bool=False) -> bool:
            '''Decorate and print. Returns True if any matches were found.'''
            decorated = self.decorate(line)
            had_match = decorated != line
            end = "\n" if insert_nl and not line.endswith("\n") else ""
            print(decorated, end=end, file=file)
            return had_match
        def __str__(self) -> str:
            return f"RegexpDecorate(<styles={len(self._styles)}>)"


    if 0:
        u = trm.Trm()
        rd = RegexpDecorate(u)
        r = re.compile(r"[Mm]adison")
        fg = u.yel
        bg = u.n
        # Note fg and bg must be escape sequences
        rd.register(r, fg, bg)    # Print matches in light yellow on black
        for line in open("bb").readlines():
            rd(line)    # Lines with matches are printed to stdout
        exit()

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
    def FindAll(s: AnyStr, substr: AnyStr) -> ty.Generator[int, None, None]:
        '''Generator to find all locations of substr in string s
        
        An example of use is to let you only see a chunk of a string between two
        occurrences of ∞:
            >>> s = "This ∞is an example of a∞ string"
            >>> start, finish = list(FindAll(s, "∞"))
            >>> print(repr(s[start + 1:finish]))
            'is an example of a'
        You'll get a ValueError if there aren't two ∞ characters in the file.
        '''
        if isinstance(s, str):
            if not isinstance(substr, str):
                raise TypeError("substr must be a str")
            if not s or not substr:
                return
            loc = s.find(substr)
            while loc != -1:
                yield loc
                loc = s.find(substr, loc + 1)
        elif isinstance(s, bytes):
            if not isinstance(substr, bytes):
                raise TypeError("substr must be a bytes object")
            if not s or not substr:
                return
            loc = s.find(substr)
            while loc != -1:
                yield loc
                loc = s.find(substr, loc + 1)
    def FindFirstIn(s: AnyStr, items: set[AnyStr]) -> int | None:
        'Return smallest integer i such that s[i] is in items or else None'
        if not s or not items:
            return None
        for i in range(len(s)):
            if s[i] in items:
                return i
        return None
    def FindLastIn(s: AnyStr, items: set[AnyStr]) -> int | None:
        'Return index of last element in s in items or None'
        if isinstance(s, str):
            n = FindFirstIn(''.join(reversed(s)), items)
        else:
            n = FindFirstIn(bytes(reversed(s)), items)
        return None   if n is None   else    len(s) - n - 1
    def FindFirstNotIn(s: AnyStr, items: set[AnyStr]) -> int | None:
        'Return smallest integer i such that s[i] not in items else None'
        if not s or not items:
            return None
        for i in range(len(s)):
            if s[i] not in items:
                return i
        return None
    def FindLastNotIn(s: AnyStr, items: set[AnyStr]) -> int | None:
        'Return index of last element in s not in items or None'
        if isinstance(s, str):
            n = FindFirstNotIn(''.join(reversed(s)), items)
        else:
            n = FindFirstNotIn(bytes(reversed(s)), items)
        return None   if n is None   else    len(s) - n - 1
    def Keep_old(s, keep, whole=True, left=False, middle=False, right=False):
        '''Return a list (or a string if s is a string) of the items in s that
        are in keep.
        
        ∞∞1 Mar 2026 This function was replaced by the new version of Keep(), but I'm
        keeping the old version around for a while in case its functionality is needed.  
        If not used by Sep 2026, delete.
        
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
        if left or middle or right:
            whole = False
        if whole:
            result = [item for item in s if item in set(keep)]
        else:
            sl = FindFirstNotIn(s, keep)
            sr = FindLastNotIn(s, keep)
            # Get components
            s_left = s[:sl]
            s_right = s[sr + 1 :]
            s_middle = s[sl : sr + 1]
            # Check invariant
            if s_left + s_middle + s_right != s:
                a = ("string" if isinstance(s, str) else 
                     "bytes" if isinstance(s, bytes) else "sequence")
                raise RuntimeError("Bug in {__file__}:Keep():  "
                                  f"s_left + s_middle + s_right != original {a}")
            result = []
            if left:
                result.append(s_left)
            if middle:
                result.append(s_middle)
            if right:
                result.append(s_right)
        if isinstance(s, str):
            return ''.join(result)
        elif isinstance(s, bytes):
            return b''.join(result)
        else:
            return result
    def Keep(seq: ty.Iterable[T],
             keep: ty.Sequence[ty.Any] | ty.Callable[[T], bool],
             strict_type: bool = False
            ) -> ty.Generator[T, None, None]:
        '''Yields items from seq that are found in keep
        
        This O(n) generator returns items from seq that are in keep (n = len(seq)).
        keep can also be a predicate function, which means this is like filter(seq,
        keep).  
        
        Warning
            As the user, it's your responsibility to make sure none of the items in seq
            change during the processing of this function, as Hashable, a wrapper class,
            is used internally on the items to make them appear to be hashable even if
            they are not.
        
        Mathematical description:  
            keep is a sequence:   Keep(seq, keep) = {x ∈ seq | x ∈ keep}
            keep is a predicate:  Keep(seq, keep) = {x ∈ seq | keep(x) == True}
        
        Arguments
            seq     A sequence of items as candidates to keep
            keep    A container of items to be kept OR a predicate such that keep(item)
                    is True if the item from seq is to be kept
        
            strict_type
                If True, then for an item in seq to be equal to an item in keep, we must
                have that bool(seq_item == keep_item) is True AND that both items have
                the same type.  Example:  if strict_type is False, then an integer 1 in
                seq will be kept if a floating point 1.0 is in keep (but a 1 is not in
                keep).  If strict_type is True, then the integer 1 would not be kept.
        
        Algorithm
            - If keep is a predicate, this is effectively filter(seq, keep)
            - Otherwise, keep is turned into a set (using the Hashable class) to make 
              'item in keep' be O(1).
            - The code is short enough to visually inspect that it's correct
        
        Thanks
            - This function was a joint effort by me and Google's Gemini AI.  Gemini
              gave me a lot of help and instruction during my refactoring of my /plib
              set of modules and helping me with type annotations.  What was interesting
              was the synergism developed during this work, as this short and elegant
              algorithm came from both our efforts (neither of use would have produced
              it by ourselves).
        
        Examples
            >>> ''.join(Keep("", ""))
            ''
            >>> ''.join(Keep("abc", "bc"))
            'bc'
            >>> def predicate(x):
            ...     return x in "bc"
            ...
            >>> ''.join(Keep("abc", predicate))
            'bc'
            >>> bytes(Keep(b"abc", b"bc"))
            b'bc'
        '''
        if callable(keep):
            for item in seq:
                if keep(item):
                    yield item
            return
        else:
            lookup_set = {Hashable(item, typ=strict_type) for item in keep}
            for item in seq:
                if Hashable(item, typ=strict_type) in lookup_set:
                    yield item  
    def KeepFilter(keep: ty.Sequence[ty.Any] | ty.Callable[[ty.Any], bool]
                  ) -> ty.Callable[[ty.Iterable[T]], ty.Generator[T, None, None]]:
        '''Return a function that keeps items in a sequence
        
        This is a closure using Keep().  Read about your user's responsibilities in
        Keep().
        
        Example
            >>> hex_only = KeepFilter("0123456789ABCDEFx")
            >>> ''.join(hex_only("Ref: 0xCAFE"))
            '0xCAFE'
        '''
        def filter_func(seq: ty.Iterable[T]) -> ty.Generator[T, None, None]:
            return Keep(seq, keep)
        return filter_func
    def Remove(seq: ty.Iterable[T],
               remove: ty.Sequence[ty.Any] | ty.Callable[[T], bool],
               strict_type: bool = False
              ) -> ty.Generator[T, None, None]:
        '''Yields items from seq that are not in remove
        
        See the comments for Keep().
        
        Mathematical description:  
            remove is a sequence:   Remove(seq, remove) = {x ∈ seq | x ∉ remove}
            remove is a predicate:  Remove(seq, remove) = {x ∈ seq | remove(x) == False}
        
        Examples
            >>> ''.join(Remove("abc", "bc"))
            'a'
            >>> def predicate(x):
            ...     return x in "bc"
            ...
            >>> ''.join(Remove("abc", predicate))
            'a'
            >>> bytes(Remove(b"abc", b"bc"))
            b'a'
        '''
        if callable(remove):
            for item in seq:
                if not remove(item):
                    yield item
            return
        else:
            lookup_set = {Hashable(item, typ=strict_type) for item in remove}
            for item in seq:
                if Hashable(item, typ=strict_type) not in lookup_set:
                    yield item  
    def RemoveFilter(remove: ty.Sequence[ty.Any] | ty.Callable[[ty.Any], bool]
                    ) -> ty.Callable[[ty.Iterable[T]], ty.Generator[T, None, None]]:
        '''Return a function that removes items in a sequence
        
        This is a closure using Remove().  Read about your user's responsibilities in
        Keep().
        
        Example
            >>> hex_only = RemoveFilter("Ref: ")
            >>> ''.join(hex_only("Ref: 0xCAFE"))
            '0xCAFE'
        '''
        def filter_func(seq: ty.Iterable[T]) -> ty.Generator[T, None, None]:
            return Remove(seq, remove)
        return filter_func
    def CountLeadingSpaces(s: str, trim_start: bool=True, trim_end: bool=True) -> int:
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
        spacecharset = set([" "])
        if trim_start or trim_end:
            x = PrepareMultilineString(s, trim_start=trim_start, trim_end=trim_end)
        else:
            # No trimming, so just count the leading space characters
            return len(GetStartingChars(s, spacecharset))
        # Break into lines and count spaces on each line
        lines = x.split("\n")
        # Count number of leading space characters on each line
        counts = [len(GetStartingChars(line, spacecharset)) for line in lines]
        return min(set(counts))
    def PrepareMultilineString(s: str, trim_start: bool=True, trim_end: bool=True) -> str:
        '''If trim_start, remove leading spaces of s up to the first newline, then
        remove the first newline.  If trim_end, remove trailing spaces of s up to the
        last newline, then remove the last newline.  Return the string.
        '''
        n = bool(trim_start) + bool(trim_end) - 1
        if s.count("\n") < n:
            raise ValueError("Not enough newline characters in multiline string s")
        dq = collections.deque(s)
        if trim_start:
            while dq and dq[0] == " ":
                dq.popleft()
            # All leading spaces removed; check for newline
            if dq and dq[0] == "\n":
                dq.popleft()
        if trim_end:
            while dq and dq[-1] == " ":
                dq.pop()
            # All trailing spaces removed; check for newline
            if dq and dq[-1] == "\n":
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
    def RemoveEndingChars(s: str, chars: str="") -> str:
        'Remove any ending characters in chars from s and return the result'
        if not s or not chars:
            return s
        S = set(chars)
        while s and s[-1] in S:
            s = s[:-1]
        return s
    def RemoveStartingChars(s: str, chars: str="") -> str:
        'Remove any starting characters in chars from s and return the result'
        if not s or not chars:
            return s
        i, S = 0, set(chars)
        while s[i] in S:
            i += 1
        return s[i:]
    def FilterSeqRegex(seq: ty.Sequence[AnyStr],
                       regex: re.Pattern
                      ) -> ty.Generator[AnyStr, None, None]:
        '''Generator of a sequence of strings filtered by a regular expression
        
        Only the items in seq where regex.search(item) return a True match object are in
        the returned sequence.
        
        Variables
            seq     The sequence whose components are to be filtered
            regex   A compiled regular expression from re.compile()
        
        Example
            >>> seq = "str1 str2 str3".split()
            >>> list(FilterSeqRegex(seq, re.compile(r"[12]")))
            ['str1', 'str2']
        '''
        if regex is None:
            for i in seq:
                yield i
            return
        if not isinstance(regex, re.Pattern):
            raise TypeError("regex must be an re.Pattern (output of re.compile())")
        for i in seq:
            try:
                mo = regex.search(i)
                if mo:
                    yield i
            except TypeError:
                continue
    def ReplacementFilter(remove: AnyStr, 
                          replacements: AnyStr
                         ) -> ty.Callable[[AnyStr], AnyStr]:
        'Return a closure that performs character/byte replacement'
        if type(remove) is not type(replacements):
            raise TypeError("remove and replacements must be the same type")
        if len(remove) != len(replacements):
            raise ValueError("remove and replacements must be the same length")
        if isinstance(remove, bytes) and isinstance(replacements, bytes):
            # Build the 256-byte translation table for bytes
            table_bytes = bytearray(range(256))
            for i, j in zip(remove, replacements, strict=True):
                table_bytes[i] = j
            # Capture the immutable version for the closure
            final_table_bytes = bytes(table_bytes)
            return lambda s: ty.cast(AnyStr, s.translate(final_table_bytes))
        else:
            # Use str.maketrans to create the mapping dict
            table_str = str.maketrans(remove, replacements)
            return lambda s: ty.cast(AnyStr, s.translate(table_str))
    def FindDiff(s1: AnyStr,
                 s2: AnyStr,
                 ignore_empty: bool = False,
                 equal_length: bool = False
                ) -> int:
        '''Returns the integer index of where the strings s1 and s2 first differ.  The
        number returned is the index where the first difference was found.  If the
        strings are equal, then -1 is returned, implying one string is a substring of
        the other (or they are the same string).  If ignore_empty is False, an exception
        is raised if one of the strings is empty.  If equal_length is True, then the
        strings must be of equal length or a ValueError exception is raised.
        '''
        if isinstance(s1, str) and not isinstance(s2, str):
            raise TypeError("Both arguments must be strings")
        if isinstance(s1, bytes) and not isinstance(s2, bytes):
            raise TypeError("Both arguments must be bytes")
        if (not s1 or not s2) and not ignore_empty:
            raise ValueError("s1 and/or s2 cannot be empty")
        if equal_length and len(s1) != len(s2):
            raise ValueError("Strings must be equal lengths")
        n = min(len(s1), len(s2))
        if not n:
            return 0
        if s1[:n] == s2[:n]:
            return -1
        # Compare characters/bytes until we get a mismatch
        for i in range(n):
            if s1[i] != s2[i]:
                return i
        raise RuntimeError("Bug:  strings differed")
    def FindStrings(seq: ty.Sequence[AnyStr],
                    x: AnyStr,
                    ignorecase: bool=False
                   ) -> list[tuple[int, int]]:
        '''Return list of (i, j) pairs which indicate where the strings in sequence seq
        (index i) are located in string x (index j).  An empty list is returned if
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
            j = x.find(u)
            if j != -1:
                found.append((i, j))
        return found
    def FindSubstring(mystring: AnyStr, substring: AnyStr) -> tuple[int, ...]:
        '''Return a tuple of the all the indexes of where the substring is found in the
        string mystring.
        '''
        if isinstance(mystring, str) and not isinstance(substring, str):
            raise TypeError("mystring needs to be a string")
        if isinstance(mystring, bytes) and not isinstance(substring, bytes):
            raise TypeError("substring needs to be bytes")
        d: list[int] = []
        ns, nsub = len(mystring), len(substring)
        if not ns or not nsub or nsub > ns:
            return tuple()
        start = mystring.find(substring)
        while start != -1 and ns - start >= nsub:
            d.append(start)
            start = mystring.find(substring, start + 1)
        return tuple(d)
    def FindSymbol(symbol: str,
                   filelist: list[str | pathlib.Path],
                   ignore_case: bool=False
                  ) -> list[str | pathlib.Path]:
        '''Given a string symbol, return a list of the python files in filelist that
        contain the indicated symbol.  The items in filelist can be strings or 
        pathlib.Path instances and can end in '.py' or not.
         
        The symbols are found by importing the python file as a module and seeing if 
        it contains the symbol.
        '''
        if filelist is None or not symbol:
            return []
        found: list[str | pathlib.Path] = []
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
    def GetString(prompt_msg: str,
                  default: str,
                  allowed_values: list[str],
                  ignore_case=True
                 ) -> str:
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
    def GetChoice(name: str, names: set[str]) -> str | list[str] | None:
        '''name is a string and names is a set of strings.  Find if name
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
        d: dict[str, list[str]] = collections.defaultdict(list)
        for i in names:
            d[i[: len(name)]] += [i]
        if name in d:
            if len(d[name]) == 1:
                return d[name][0]
            else:
                return d[name]
        return None
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
    def Len(s: ty.Any) -> int:
        '''Same as built-in len(), except if the argument is a str, the ANSI escape
        sequences are stripped out.
        '''
        return len(RmEsc(s)) if isinstance(s, str) else len(s)
    def RmEsc(s: str, on: bool = True) -> str:
        '''Remove ANSI escape strings if on is True; otherwise just return s.
        
        The primary use case is to remove colorizing ANSI escape strings from a string
        s.  Not all ANSI escape strings are supported, just the ones that contain a CSI
        sequence.
        '''
        if not on or not isinstance(s, str):
            return s
        return _RE_ANSI_CSI.sub("", s)
    def RmEsc(s:str, on: bool=True) -> str:
        @functools.lru_cache(maxsize=1)
        def GetRegex() -> re.Pattern:
            return re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
        if not on:
            return s
        return GetRegex().sub("", s)
    def Tokenize(s: str, wordchars: set[str]) -> list[str]:
        '''Split the string s into a list of tokens
         
        The input string s is split into tokens (words) at any character not in
        wordchars.  An invariant is that ''.join(results) is the original string.
        
        Example
            >>> wordchars = string.ascii_letters
            >>> Tokenize("Zheenl@Punczna.zhmmyr")
            ['Zheenl', '@', 'Punczna', '.', 'zhmmyr']
        
        '''
        if not isinstance(s, str):
            raise TypeError("Argument s needs to be a string")
        out: list[str] = []
        word: list[str] = []
        for char in s:
            if char in wordchars:
                word.append(char)
            else:
                if word:
                    out.append(''.join(word))
                    word = []
                out.append(char)
        if word:
            out.append(''.join(word))
        assert ''.join(out) == s    # Check invariant
        return out
    def GetStartingChars(s: str, allowed: set[str]) -> str:
        '''Return the string with characters in allowed that start s
        
        Example
            >>> GetStartingChars("abcabHabc", set("abc"))
            'abcab'
        '''
        out = []
        for i in s:
            if i in allowed:
                out.append(i)
            else:
                break
        return ''.join(out)
    def GetEndingChars(s: str, allowed: set[str]) -> str:
        '''Return the string with characters in allowed that end s
        
        Example
            >>> GetEndingChars("abcabHabcab", set("abc"))
            'abcab'
        '''
        out = []
        for i in reversed(s):
            if i in allowed:
                out.append(i)
            else:
                break
        return ''.join(reversed(out))
    def RegisteredOpen(file: str | pathlib.Path) -> None:
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
    def RemoveASCII(s: str):
        '''Remove ASCII characters from string s
        
        This means the returned string only consists of Unicode characters above U+7e.
        
        Example
            >>> RemoveASCII("Hello ∞")
            '∞'
        '''
        @functools.lru_cache(maxsize=1)
        def GetTranslation() -> dict[int, None]:
            return str.maketrans({i: None for i in range(0x7f)})
        return s.translate(GetTranslation())
    def IgnoreFilter(regex_seq: ty.Sequence[str],
                     flags: int =re.NOFLAG
                    ) -> ty.Callable[[ty.Sequence[str]], list[str]]:
        '''Return a function (closure) which removes ignored strings from a sequence
        
        regex_seq is a sequence of regular expression strings that should be ignored;
        this routine will compile them with the indicated re module flags.  
        
        A use case for this filter is to provide functionality like the .gitignore file in a
        git repository:  any filename in the repository that matches a line in the
        .gitignore file is ignored by git (however, note that git uses file globbing
        expressions and this function uses python's re module's expressions).
        
        Example:
            >>> f = IgnoreFilter(["bob", "carol"])
            >>> g = IgnoreFilter(["bob", "carol"], flags=re.I)
            >>> seq = ["Bob", "bob", "bobwhite", "Carol", "carol", "Alice"]
            >>> f(seq)
            ['Bob', 'Carol', 'Alice']
            >>> g(seq)
            ['Alice']
        '''
        # Compile the regular expressions
        regexes = [re.compile(i, flags) for i in regex_seq if i]
        # Bundle them into a closure
        def regex_filter(seq: ty.Sequence[str]) -> list[str]:
            results = [i for i in seq]  # Make a copy
            for regex in regexes:
                results = list(itertools.filterfalse(regex.search, results))
            return results
        return regex_filter
    def IsASCII(s: str) -> bool:
        '''Return True if string s consists only of ASCII characters
        
        This means the string only consists of characters chr(0x0) to chr(0x7e) inclusive.
        '''
        return not bool(RemoveASCII(s))
    def Scramble(mystr: str,
                 punc: set[str] = set(string.punctuation + string.whitespace),
                 start_end_const: bool=False
                ) -> str:
        '''Return a string with the letters in the words randomly shuffled
        
        Arguments
            mystr       String whose words are to be shuffled
        
        but with the
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
        article on genetics with a lot of biochemistry and it was essentially total
        gibberish.
        
        Example with random.seed('0'):
            s = '"Hello there", said John.'
        returns
                '"loeHl eerth", isda noJh.'
        '''
        dummy = "."
        prepended = appended = False
        s = list(mystr)
        # Add dummy punctuation characters at start and end if needed.  This
        # regularizes the algorithm.
        if s[0] not in punc:
            s.insert(0, dummy)
            prepended = True
        if s[-1] not in punc:
            s.append(dummy)
            appended = True
        # Generate a list of integers showing where punctuation characters are
        loc = [i for i, x in enumerate(s) if x in punc]
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
        return ''.join(s)
    def Trim(s: AnyStr,
             chars: set[AnyStr],
             left: bool=True,
             right: bool=True
            ) -> AnyStr:
        'Remove characters in chars from the left and right sides of s & return result'
        if not chars or (not left and not right):
            return s
        dq = collections.deque(s)
        isstr = True if isinstance(s, str) else False
        if left:
            while dq:
                if dq[0] in chars:
                    dq.popleft()
                else:
                    break
        if right:
            while dq:
                if dq[-1] in chars:
                    dq.pop()
                else:
                    break
        return ''.join(dq) if isstr else bytes(dq)  # type: ignore
    def Edit(*files: ty.Sequence[str | pathlib.Path],
             strict: bool = False,
             opt: list[str] | None = None,
             ret: bool = False
            ) -> None | list[str]:
        '''Launch editor on those files that exist (or return the command strings)
        
        The bare call launches the editor (gotten from the EDITOR environment string);
        you'll get an exception from subprocess() if the file doesn't exist or can't be
        opened.
        
        Set strict to False and ret to True to raise no exceptions (files don't have to
        exist); the function then just returns the list of command strings.
         
        Arguments
            files       A string or pathlib.Path instance (file to edit)
            strict      If True, raise Exception on no files or if a file doesn't exist
            opt         List of strings options to append before the files
            ret         If True, return the list of strings rather than executing the
                        editing command
        Example
            >>> Edit("testfile", ret=True, opt=["a", "b"])
            ["<editor_executable>", "a", "b", "testfile"]
        '''
        editor = os.environ["EDITOR"]
        files_to_edit = []
        if strict and not files:
            raise ValueError(f"No files given")
        # Construct list of file strings to edit
        for file in files:
            if isinstance(file, str):
                p = pathlib.Path(file)
            elif isinstance(file, pathlib.Path):
                p = file
            else:
                raise TypeError(f"{file!r} needs to be a str or pathlib.Path")
            if strict and not p.exists():
                raise ValueError(f"{file!r} doesn't exist")
            files_to_edit.append(str(file))
        # Construct editing command string list
        editing_commands = [editor]
        if opt:
            editing_commands.extend(list(opt))
        editing_commands.extend(files_to_edit)
        if not ret:
            subprocess.call(editing_commands)
            return None
        else:
            return editing_commands
    def RemoveCharClass(s: AnyStr, keys: str=""):
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
        '''
        letters = set("ABbdhlnopWwu780")
        mykeys = set(keys)
        if not mykeys.issubset(letters):
            raise ValueError(f"keys = {keys!r} must only contain the letters {letters!r}")
        if 1:
            cd = string.digits
            ch = string.hexdigits
            cl = string.ascii_lowercase
            cn = string.punctuation
            co = string.octdigits
            cp = string.printable
            cW = string.whitespace
            cw = cW.replace("\n", "")
            cu = string.ascii_uppercase
        if isinstance(s, str):
            r = s
            if "A" in mykeys:
                r = asciify.Asciify(s)
            if "B" in mykeys:
                r = ''.join(i for i in s if ord(i) >= 0x20)
            if "b" in mykeys:
                r = ''.join(i for i in s if ord(i) >= 0x20 or i == "\n")
            if "d" in mykeys:
                r = ''.join(i for i in s if i not in set(cd))
            if "h" in mykeys:
                r = ''.join(i for i in s if i not in set(ch))
            if "l" in mykeys:
                r = ''.join(i for i in s if i not in set(cl))
            if "o" in mykeys:
                r = ''.join(i for i in s if i not in set(co))
            if "n" in mykeys:
                r = ''.join(i for i in s if i not in set(cn))
            if "p" in mykeys:
                r = ''.join(i for i in s if i     in set(cp))
            if "W" in mykeys:
                r = ''.join(i for i in s if i not in set(cW))
            if "w" in mykeys:
                r = ''.join(i for i in s if i not in set(cw))
            if "u" in mykeys:
                r = ''.join(i for i in s if i not in set(cu))
            if "7" in mykeys:
                r = ''.join(i for i in s if ord(i) <= 0x7f)
            if "8" in mykeys:
                r = ''.join(i for i in s if ord(i) <= 0xff)
            if "0" in mykeys:
                pass
            return r
        elif isinstance(s, (bytes, bytearray)):
            b = s
            T = bytes if isinstance(b, bytes) else bytearray
            if "A" in mykeys:
                pass
            if "B" in mykeys:
                b = T(i for i in b if i >= 0x20)
            if "b" in mykeys:
                b = T(i for i in b if i >= 0x20 or i == ord("\n"))
            if "d" in mykeys:
                b = T(i for i in b if i not in set(cd.encode()))
            if "h" in mykeys:
                b = T(i for i in b if i not in set(ch.encode()))
            if "l" in mykeys:
                b = T(i for i in b if i not in set(cl.encode()))
            if "o" in mykeys:
                b = T(i for i in b if i not in set(co.encode()))
            if "n" in mykeys:
                b = T(i for i in b if i not in set(cn.encode()))
            if "p" in mykeys:
                b = T(i for i in b if i     in set(cp.encode()))
            if "W" in mykeys:
                b = T(i for i in b if i not in set(cW.encode()))
            if "w" in mykeys:
                b = T(i for i in b if i not in set(cw.encode()))
            if "u" in mykeys:
                b = T(i for i in b if i not in set(cu.encode()))
            if "7" in mykeys:
                b = T(i for i in b if i <= 0x7f)
            if "8" in mykeys or "0" in mykeys:
                pass
            return b
        else:
            raise TypeError("s must be str, bytes, or bytearray")
    class TextWrapper(textwrap.TextWrapper):
        '''This is the same as the textwrap.TextWrapper class except the method with
        calls to len had each occurrence replaced with Len.  This allows this text
        wrapper to work with strings with embedded escape strings.
        '''
        def __init__(self, *args, **kw) -> None:    # type: ignore
            super().__init__(*args, **kw)
        def _wrap_chunks(self, chunks: list[str]) -> list[str]:
            '''_wrap_chunks(chunks : [string]) -> [string]
            
            Wrap a sequence of text chunks and return a list of lines of
            length 'self.width' or less.  (If 'break_long_words' is False,
            some lines may be longer than this.)  Chunks correspond roughly
            to words and the whitespace between them: each chunk is
            indivisible (modulo 'break_long_words'), but a line break can
            come between any two chunks.  Chunks should not have internal
            whitespace; ie. a chunk is either all whitespace or a "word".
            Whitespace chunks will be removed from the beginning and end of
            lines, but apart from that whitespace is preserved.
            '''
            lines: list[str] = []
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
            # from a stack of chunks.
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
                    if cur_len + L <= width:
                        # Can squeeze this chunk onto the current line
                        cur_line.append(chunks.pop())
                        cur_len += L
                    else:
                        break   # Nope, this line is full.
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
                    if     (self.max_lines is None
                            or Len(lines) + 1 < self.max_lines
                            or (not chunks
                                or self.drop_whitespace
                                and Len(chunks) == 1
                                and not chunks[0].strip())
                        and cur_len <= width):
                        # Convert current line back to a string and store it in
                        # list of all lines (return value).
                        lines.append(indent + "".join(cur_line))
                    else:
                        while cur_line:
                            if     (cur_line[-1].strip()
                                    and cur_len + Len(self.placeholder) <= width):
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
    def Decorate(s: AnyStr, encoding: str="UTF-8") -> str:
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
    def ConvertToNumber(s: str) -> int | float | complex | fractions.Fraction:
        '''Maps a string to the simplest python number
        
        Human-friendly features:
            - Maps 'i'/'I' to 'j' while protecting 'inf' strings
            - Allows '1 + 2i' and '1 / 2' by removing internal spaces
            - Changes ',' to '.' for international radix support
            - Detects 'nan' and 'inf' as float instances
        '''
        s = s.lower().strip()
        if "inf" in s:
            s = s.replace("inf", "~~~").replace("i", "j").replace("~~~", "inf")
        else:
            s = s.replace("i", "j")
        if "," in s:
            s = s.replace(",", ".")
        if any(op in s for op in "+-/"):
            s = s.replace(" ", "")
        try:
            if "j" in s:
                return complex(s)
            if "." in s or "e" in s or "nan" in s or "inf" in s:
                return float(s)
            if "/" in s:
                return fractions.Fraction(s)
            return int(s)
        except ValueError as err:
            raise ValueError(f"{s!r} is not a python number representation") from err
    def StringToNumbers(s: str,
                        sep: str | None = " "
                       ) -> list[TNum] | list[list[TNum]]:
        r'''Transforms a string into a vector or 2D matrix

        - If 'sep' is None, splits on all whitespace (returns 1D list)
        - If 'sep' is a string and '\n' is present, returns a nested 2D list
        - Otherwise, returns a flat 1D list of numbers

        Examples (need to change the code)
            >>> StringToNumbers("1 2\n3 4", sep=" ")
            [[1, 2], [3, 4]]
            >>> StringToNumbers("1 2\n3 4", sep=None)
            [1, 2, 3, 4]
            >>> StringToNumbers("1 2 3 4")
            [1, 2, 3, 4]
        '''
        s = s.strip()
        if not s:
            return []
        if sep is None:
            return [ConvertToNumber(j) for j in s.split()]
        if "\n" in s:   # It will be a nested list
            matrix: list[list[TNum]] = []
            for line in s.splitlines():
                line_data = [ConvertToNumber(j) for j in line.split(sep) if j.strip()]
                if line_data:
                    matrix.append(line_data)
            return matrix
        else:
            return [ConvertToNumber(j) for j in s.split(sep) if j.strip()]
    def Int(s):
        '''Convert the string (or bytes) s to an integer.  Allowed forms are:
            - Plain base 10 string
            - 0b, 0B:  binary
            - 0o, 0O:  octal
            - 0x, 0X:  hex
            - u+, U+:  hex style for Unicode codepoints
        '''
        if not isinstance(s, (str, bytes, bytearray)):
            raise TypeError("s must be str, bytes, or bytearray")
        isstr = True if isinstance(s, str) else False
        neg = 1
        if s[0] == "-" or s[0] == ord("-"):
            neg = -1
            s = s[1:]
        if s.lower().startswith("0b" if isstr else b"0b"):
            return neg*int(s, 2)
        elif s.lower().startswith("0o" if isstr else b"0o"):
            return neg*int(s, 8)
        elif s.lower().startswith("0x" if isstr else b"0x"):
            return neg*int(s, 16)
        elif s.lower().startswith("u+" if isstr else b"u+"):
            return neg*int(s, 16)
        else:
            return neg*int(s, 10)
if 1:   # Old util stuff
    def RemoveIndent(s: str, numspaces: int=4) -> str:
        '''Given a multi-line string s, remove the indicated number of spaces from the beginning each
        line.  If that number of space characters aren't present, then leave the line alone.
        '''
        if numspaces < 0:
            raise ValueError("numspaces must be >= 0")
        lines = s.split("\n")
        for i, line in enumerate(lines):
            if line.startswith(" "*numspaces):
                lines[i] = lines[i][numspaces:]
        return "\n".join(lines)
    def GetLeadingString(string: AnyStr, prefix: AnyStr) -> AnyStr:
        '''Return the leading string from string
        
        The leading string is one or more groups of the prefix.  A use case is to match
        the indentation of a previous line.
        
        Example
            >>> GetLeadingString(b"zzzHi", prefix=b"z")
            b"zzz"
            >>> GetLeadingString("zzzHi", prefix="z")
            "zzz"
            >>> GetLeadingString("ababHi", prefix="ab")
            "abab"
        '''
        num_chunks, len_prefix = 0, len(prefix)
        while num_chunks*len_prefix < len(string):
            if string[num_chunks*len_prefix : (num_chunks + 1)*len_prefix] == prefix:
                num_chunks += 1
            else:
                break
        return num_chunks*prefix
    def GetTrailingString(string: AnyStr, suffix: AnyStr) -> AnyStr:
        '''Return the trailing string from string
        
        The trailing string is one or more groups of the suffix.  A use case is to match
        the indentation of a previous line.
        
        Example
            >>> GetTrailingString(b"Hizzz", suffix=b"z")
            b"zzz"
            >>> GetTrailingString("Hizzz", suffix="z")
            "zzz"
            >>> GetTrailingString("Hiabab", suffix="ab")
            "abab"
        '''
        def Reversed(x: AnyStr) -> AnyStr:
            return bytes(reversed(x)) if isinstance(x, bytes) else ''.join(reversed(x))
        return Reversed(GetLeadingString(Reversed(string), prefix=Reversed(suffix)))
    def GetHash(item: pathlib.Path | AnyStr,
                method: str="sha256",
                encoding: str="UTF-8"
               ) -> str:
        '''Return item's hash as a hex string
         
        item can be:
            - pathlib.Path instance to a file
            - string instance (UTF-8 encoding assumed)
            - bytes instance
        method is the hash method and can be
            - md5 sha1 sha224 sha256 sha384 sha512
        encoding
            - Is used for text files and strings.  Set it to None to read files in
              binary.
        
        Example
            >>> GetHash("string")
            '473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8'
            >>> GetHash(b"string")
            '473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8'
        '''
        if method.lower() in "md5 sha1 sha224 sha256 sha384 sha512".split():
            h = eval(f"hashlib.{method.lower()}")()
        else:
            raise ValueError(f"{method!r} is unsupported")
        if isinstance(item, str):
            h.update(item.encode(encoding))
        elif isinstance(item, bytes):
            h.update(item)
        elif isinstance(item, pathlib.Path):
            if encoding is None:
                h.update(item.open("rb").read())
            else:
                h.update(item.open("r").read().encode(encoding))
        return str(h.hexdigest())
    def EBCDIC():
        'Return two byte-translation tables ASCII_to_EBCDIC and EBCDIC_to_ASCII'
        # ∞∞3:  It's not known whether either of these two transformations are "correct"
        # and it's complicated because things are complicated by many encodings.
        # Virtually everything you'll come across is poorly documented to, so to fiddle
        # with old data may take quite a bit of work.  I had to work with this stuff
        # once a few decades ago with voting data from someone's mainframe reel of tape
        # and it was frustrating to find documentation, but I finally figured things
        # out.
        if 1:   # These two tables are the old code and unattributed
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
            s, t = bytes(a2e), bytes(e2a)
            A2E, E2A = bytes.maketrans(s, t), bytes.maketrans(t, s)
            return A2E, E2A
        else:
            # EBCDIC to/from ASCII
            # https://www.ibm.com/docs/en/iis/11.7.0?topic=tables-ebcdic-ascii
            # Downloaded 23 Mar 2026 10:42:46 am Mon
            e = bytes(list(range(0x100)))   # EBCDIC codes
            a = bytes((
                    0x00, 0x01, 0x02, 0x03, 0x1A, 0x09, 0x1A, 0x7F, 0x1A, 0x1A, 0x1A,
                    0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x1A, 0x1A,
                    0x08, 0x1A, 0x18, 0x19, 0x1A, 0x1A, 0x1C, 0x1D, 0x1E, 0x1F, 0x1A,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x0A, 0x17, 0x1B, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x1A, 0x05, 0x06, 0x07, 0x1A, 0x1A, 0x16, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x04, 0x1A, 0x1A, 0x1A, 0x1A, 0x14, 0x15, 0x1A, 0x1A, 0x20, 0x1A,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x5B, 0x2E, 0x3C,
                    0x28, 0x2B, 0x21, 0x26, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x5D, 0x24, 0x2A, 0x29, 0x3B, 0x5E, 0x2D, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x7C, 0x2C, 0x25, 0x5F,
                    0x3E, 0x3F, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x60, 0x3A, 0x23, 0x40, 0x27, 0x3D, 0x22, 0x1A, 0x61, 0x62, 0x63,
                    0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x7E, 0x73, 0x74, 0x75,
                    0x76, 0x77, 0x78, 0x79, 0x7A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x7B, 0x41, 0x42, 0x43, 0x44, 0x45,
                    0x46, 0x47, 0x48, 0x49, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x7D,
                    0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x1A, 0x1A, 0x5C, 0x1A, 0x53, 0x54, 0x55, 0x56, 0x57,
                    0x58, 0x59, 0x5A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x30, 0x31,
                    0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x1A, 0x1A, 0x1A,
                    0x1A, 0x1A, 0x1A))
            return bytes.maketrans(a, e), bytes.maketrans(e, a)
    class astr(str):
        '''This is a string object that uses a regular expression to remove
        ANSI color-coding strings before calculating the string length.
        '''
        # This regular expression is used to replace a color-coding escape sequence with
        # the empty string.  See https://en.wikipedia.org/wiki/ANSI_escape_code.
        r = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
        def __len__(self) -> int:
            return len(astr.r.sub("", str(self)))
    def alen(s: str) -> int:
        'Function to get the length of a string, ignoring any ANSI escape sequences'
        return len(astr.r.sub("", s))
    def EscapeSequenceStrip(string: str) -> str:
        '''Return the string with ANSI escape sequences removed
        
        16 Feb 2023 Suggested regexp from
        https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-\
        escape-sequences-from-a-string-in-python (see the answer below this answer,
        as it is a more general regexp).
        
        Example:
            >>>EscapeSequenceStrip("\x1b[38;2;198;174;239m12.578")
            '12.578'
        '''
        r = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        return r.sub("", string)
    def BuildTagsFile(directory: str | pathlib.Path,
                      files: ty.Sequence[str | pathlib.Path],
                      verbose: bool = False
                     ) -> None:
        r'''For vim-style help files, construct a tags file for the indicated directory
        
        Arguments
          dir       Directory where the files reside
          files     Sequence of file names
          verbose   If True, print where tags file constructed
          
        For vim's help files, this is done by searching for text between two asterisk
        characters and extracting the tag.  This is written to the tags file in the form
        
            symbol\tsymbol.hld\t/*symbol*
            
        and the file is sorted on these lines.  The first line of the file must be
        'help-tags\ttags\t1'.
        '''
        if not files and verbose:
            print(f"{__file__}:BuildTagsFile: no files found in files sequence", file=sys.stderr)
            return
        base_path = pathlib.Path(directory)
        tag_pattern = re.compile(r"\*([A-Za-z_][A-Za-z0-9_]*)\*")
        tags_set: set[str] = {"help-tags\ttags\t1"}
        for file_ref in files:
            p = pathlib.Path(file_ref)
            # Handle relative paths: if p isn't absolute, assume it's relative to 'directory'
            full_path = p if p.is_absolute() else base_path / p
            try:
                with full_path.open("r", encoding="utf-8") as f:
                    for line in f:
                        for tag in tag_pattern.findall(line):
                            t = f"{tag}\t{p.name}\t/*{tag}*"
                            tags_set.add(t)
            except (OSError, UnicodeDecodeError) as e:
                if verbose:
                    print(f"Error reading {full_path}: {e}", file=sys.stderr)
        sorted_tags = sorted(list(tags_set))
        output_file = base_path/"tags"
        output_file.write_text("\n".join(sorted_tags) + "\n", encoding="utf-8")
        if verbose:
            # Subtracting 1 because the first line is the header
            count = len(sorted_tags) - 1
            print(f"{count} tags constructed in {output_file.absolute()}")

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
    def Test_Int():
        data = (
            # Positive integers
            ("0b11", 3),
            ("0o10", 8),
            ("0x10", 16),
            ("10", 10),
                # Bytes
                (b"0b11", 3),
                (b"0o10", 8),
                (b"0x10", 16),
                (b"10", 10),
            # Negative integers
            ("-0b11", -3),
            ("-0o10", -8),
            ("-0x10", -16),
            ("-10", -10),
                # Bytes
                (b"-0b11", -3),
                (b"-0o10", -8),
                (b"-0x10", -16),
                (b"-10", -10),
        )
        for s, n in data:
            Assert(Int(s) == n)
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
        expected_old = (    # Check actual escape codes
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m"     # u.n
            "Dolly\n"
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m"     # u.n
            
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m"     # u.n
            "\x1b[38;2;254;239;0m"                              # u.yel
            "Madison"
            "\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m")    # u.n
        expected = (    # Check actual escape codes
            # Note this is the more efficient Mike implementation
            'Dolly\n\x1b[38;2;254;239;0mMadison\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m'
            )
        Assert(s == expected)
        # This is what should happen
        expected_old = u.n + "Dolly\n" + u.n + u.n + u.yel + "Madison" + u.n
        expected = "Dolly\n" + u.yel + "Madison" + u.n
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
        f = IgnoreFilter(["bob", "carol"], flags=re.I)
        Assert(f(seq) == ['Alice'])
    def Test_Trim():
        for s in ("", "a", "abc"):
            Assert(Trim(s, set("")) == s)
        u = "a b"
        s = f" {u} "
        cs = set(" ")
        Assert(Trim(s, chars=cs) == f"{u}")
        Assert(Trim(s, chars=cs, left=True, right=False) == f"{u} ")
        Assert(Trim(s, chars=cs, left=False, right=True) == f" {u}")
        Assert(Trim(s, chars=cs, left=True, right=True) == f"{u}")
        # Test when s is a subset of chars
        s = "aaaaaaaaaa"
        cs = set("eoirtjwpo op4er9qorja")
        Assert(Trim(s, chars=cs) == "")
        Assert(Trim(s, chars=cs, left=True, right=False) == "")
        Assert(Trim(s, chars=cs, left=False, right=True) == "")
        Assert(Trim(s, chars=cs, left=True, right=True) == "")
    def Test_Keep():
        Assert(''.join(Keep("", "")) == "")
        Assert(''.join(Keep("", "a")) == "")
        Assert(''.join(Keep("a", "")) == "")
        # Works using a predicate
        def predicate(x):
            return x in "bc"
        Assert(''.join(Keep("abc", predicate)) == "bc")
        # Works on strings
        Assert(''.join(Keep("abc", "bc")) == "bc")
        # Works on bytes
        Assert(bytes(Keep(b"abc", b"bc")) == b"bc")
        # Works on list sequence
        A, B = "a b c".split(), "b c".split()
        Assert(list(Keep(A, B)) == B)
    def Test_KeepFilter():
        f = KeepFilter("bc")
        Assert(''.join(f("abc")) == "bc")
    def Test_Remove():
        # A modicum of tests, as the logic is just the negated logic of Keep
        Assert(''.join(Remove("", "ab")) == "")
        Assert(''.join(Remove("ab", "")) == "ab")
        Assert(''.join(Remove("abc", "cb")) == "a")
    def Test_RemoveFilter():
        f = RemoveFilter("bc")
        Assert(''.join(f("abc")) == "a")
    def Test_FindNotIn():
        if 1:  # Strings
            Assert(FindFirstIn("", "abc") is None)
            Assert(FindLastIn("", "abc") is None)
            Assert(FindFirstIn("abc", "") is None)
            Assert(FindLastIn("abc", "") is None)
            Assert(FindFirstIn("abc", "d") is None)
            Assert(FindLastIn("abc", "d") is None)
            #
            Assert(FindFirstIn("dabc", "d") == 0)
            Assert(FindLastIn("dabc", "d") == 0)
            Assert(FindFirstIn("abc;d", ";") == 3)
            Assert(FindLastIn("abc;de", ";") == 3)
            Assert(FindLastIn("abc;", ";") == 3)
            Assert(FindLastIn(";abc;", ";") == 4)
        if 1:  # Bytes
            Assert(FindFirstIn(b"", b"abc") is None)
            Assert(FindLastIn(b"", b"abc") is None)
            Assert(FindFirstIn(b"abc", b"") is None)
            Assert(FindLastIn(b"abc", b"") is None)
            Assert(FindFirstIn(b"abc", b"d") is None)
            Assert(FindLastIn(b"abc", b"d") is None)
            #
            Assert(FindFirstIn(b"dabc", b"d") == 0)
            Assert(FindLastIn(b"dabc", b"d") == 0)
            Assert(FindFirstIn(b"abc;d", b";") == 3)
            Assert(FindLastIn(b"abc;de", b";") == 3)
            Assert(FindLastIn(b"abc;", b";") == 3)
            Assert(FindLastIn(b";abc;", b";") == 4)
        if 1:  # FindFirstNotIn, FindLastNotIn
            Assert(FindFirstNotIn("", "abc") is None)
            Assert(FindLastNotIn("", "abc") is None)
            Assert(FindFirstNotIn("abc", "") is None)
            Assert(FindLastNotIn("abc", "") is None)
            #
            Assert(FindFirstNotIn("abc", "d") == 0)
            Assert(FindLastNotIn("abc", "d") == 2)
            Assert(FindFirstNotIn("dabc", "d") == 1)
            Assert(FindLastNotIn("dabc", "d") == 3)
            Assert(FindFirstNotIn("abc;d", string.ascii_letters) == 3)
            Assert(FindLastNotIn("abc;de", string.ascii_letters) == 3)
            Assert(FindLastNotIn("abc;", string.ascii_letters) == 3)
            Assert(FindLastNotIn(";abc;", string.ascii_letters) == 4)
    def Test_FindStrings():
        if 1:   # Strings
            seq = "Jan Feb Mar".split()
            x = "1Jan2001"
            found = FindStrings(seq, x)
            Assert(found == [(0, 1)])
            # Show case insensitivity works
            x = "1jan2001"
            found = FindStrings(seq, x, ignorecase=True)
            Assert(found == [(0, 1)])
            # Show get empty list on no matches
            x = ""
            found = FindStrings(seq, x, ignorecase=True)
            Assert(not found)
        if 1:   # Bytes
            seq = b"Jan Feb Mar".split()
            x = b"1Jan2001"
            found = FindStrings(seq, x)
            Assert(found == [(0, 1)])
            # Show case insensitivity works
            x = b"1jan2001"
            found = FindStrings(seq, x, ignorecase=True)
            Assert(found == [(0, 1)])
            # Show get empty list on no matches
            x = b""
            found = FindStrings(seq, x, ignorecase=True)
            Assert(not found)
    def Test_Edit():
        s = Edit("testfile", ret=True, opt=["a", "b"])
        # Ignore the first element, which will be the user's editor
        Assert(s[1:] == ['a', 'b', 'testfile'])
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
        ws = string.whitespace
        for u in (
            "",
            " ",
            "  ",
            "\t",
            "\n",
            "\t\r\n\f    \t\t\t",
        ):
            Assert(GetStartingChars(u, ws) == u)
            Assert(GetStartingChars(u + "a", ws) == u)
            Assert(GetEndingChars(u, ws) == u)
            Assert(GetEndingChars("a" + u, ws) == u)
        # Define custom sets of whitespace
        if 1:  # Leading
            Assert(GetStartingChars("  \t  a", set("z")) == "")
            Assert(GetStartingChars("  \t  a", set("\t")) == "")
            Assert(GetStartingChars("  \t  a", set(" ")) == "  ")
            ws, u = ".;:", ".;..:::."
            a = GetStartingChars(u + "a", ws)
            Assert(a == u)
        if 1:  # Trailing
            Assert(GetEndingChars("a  \t  ", set("z")) == "")
            Assert(GetEndingChars("a  \t  ", set("\t")) == "")
            Assert(GetEndingChars("a  \t  ", set(" ")) == "  ")
            ws, u = ".;:", ".;..:::."
            a = GetEndingChars("a" + u, ws)
            Assert(a == u)
    def Test_Tokenize():
        letters = set(string.ascii_letters)
        Assert(Tokenize("", letters) == [])
        Assert(Tokenize(" ", letters) == [" "])
        Assert(Tokenize(" "*2, letters) == [" ", " "])
        s = "How so?  How can it affect them?"
        t = Tokenize(s, letters)
        u = ["How", " ", "so", "?", " ", " ", "How", " ", "can", " ", "it",
             " ", "affect", " ", "them", "?", ]
        Assert(t == u)
        # Using a comment string (makes sure the last word is there)
        s = "# A b"
        t = Tokenize(s, letters)
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
            b = "This ∞is an example of a∞ string".encode("UTF-8")
            start, finish = list(FindAll(b, substr="∞".encode()))
            n = len("∞".encode())
            Assert(b[start + n:finish] == b"is an example of a")
        if 1:   # Corner cases
            Assert(list(FindAll("", substr="x")) == [])
            Assert(list(FindAll(s, substr="")) == [])
            Assert(list(FindAll(b"", substr="∞".encode())) == [])
            Assert(list(FindAll(b, substr=b"")) == [])
        if 1:   # Raises an exception
            s = "∞"
            with raises(ValueError):
                start, finish = list(FindAll(s, substr="x"))
            with raises(ValueError):
                start, finish, _ = list(FindAll(s + s, substr="x"))
            # Note that FindAll("a", b"a") doesn't raise an exception like it would be
            # expected from the code; it has to be tested as follows.
            with raises(TypeError):
                x = list(FindAll("a", b"a"))
            with raises(TypeError):
                x = list(FindAll(b"a", "a"))
    def Test_ReplacementFilter():
        if 1:   # Strings
            s = "abcdefghi"
            f = ReplacementFilter("abcdefghi", "ABCDEFGHI")
            t = f(s)
            Assert(t == "ABCDEFGHI")
            f = ReplacementFilter("abcdefghi", "         ")
            t = f(s)
            Assert(t == "         ")
        if 1:   # Bytes
            s = b"abcdefghi"
            f = ReplacementFilter(b"abcdefghi", b"ABCDEFGHI")
            t = f(s)
            Assert(t == b"ABCDEFGHI")
            f = ReplacementFilter(b"abcdefghi", b"         ")
            t = f(s)
            Assert(t == b"         ")
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
        s = b"x  x    x  "
        Assert(FindSubstring(s, b"x") == (0, 3, 8))
    def Test_GetChoice():
        names = set(("one", "two", "three", "thrifty"))
        Assert(GetChoice("o", names) == "one")
        Assert(set(GetChoice("th", names)) == set(["three", "thrifty"]))
        Assert(GetChoice("z", names) is None)
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
        found = FindSymbol("FindSymbol", filelist)
        Assert(found == ['dpstr.py'])
        found = FindSymbol("findsymbol", filelist, ignore_case=True)
        Assert(found == ['dpstr.py'])
        found = FindSymbol("nowayray", filelist)
        Assert(found == [])
    def Test_FilterSeqRegex():
        s = "str1 str2 str3 str4 str5"
        seq1 = s.split()
        seq2 = seq1 + [10]
        regex = re.compile(r"[123]")
        # Empty sequence gets back empty sequence
        Assert(list(FilterSeqRegex([], regex)) == [])
        # regex == None means an identity transformation
        Assert(list(FilterSeqRegex(seq1, None)) == seq1)
        Assert(list(FilterSeqRegex(seq2, None)) == seq2)
        # Actual filtering
        Assert(list(FilterSeqRegex(seq1, regex)) == seq1[:3])
        Assert(list(FilterSeqRegex(seq2, regex)) == seq1[:3])
        Assert(list(FilterSeqRegex(seq1, re.compile("."))) == seq1)
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
            keys = list("ABbdhlnopWwu780")  # Allowed key letters
            f("", keys=keys)
            raises(ValueError, f, "", keys=keys + ["x"])
    def Test_ConvertToNumber():
        n, NaN = 10**50, float("nan")
        testcases = [
            ("1+i", 1+1j),
            ("1+j", 1+1j),
            ("1 + i", 1+1j),
            ("j", 1j),
            ("0", 0),
            ("-0", 0),
            ("0.0", 0),
            ("-0.0", 0),
            ("1", 1),
            ("1.", 1.0),
            ("1,", 1.0),
            ("1e2", 1e2),
            ("1E2", 1e2),
            ("1/2", fractions.Fraction(1, 2)),
            (str(n), n),
            ("1e308", 1e308),
            ("1e-308", 1e-308),
            ("-1e308", -1e308),
            ("-1e-308", -1e-308),
            ("inf", math.inf),
            ("-inf", -math.inf),
            # "Human" formatting
            (" 1 ", 1),
            (" 1 / 2 ", fractions.Fraction(1, 2)),
            (" 1 + 1i ", 1+1j),
            (" 1,5 ", 1.5),
        ]
        for x, expected in testcases:
            got = ConvertToNumber(x)
            Assert(got == expected)
        if 1:   # NaN:  because float("nan") != float("nan")
            got = ConvertToNumber("nan")
            Assert(math.isnan(got))
        if 1:   # Bad forms
            raises(ValueError, ConvertToNumber, "")
            raises(ValueError, ConvertToNumber, " ")
            raises(ValueError, ConvertToNumber, "1/")
            raises(ValueError, ConvertToNumber, "x")
            raises(ValueError, ConvertToNumber, "i+1")

    def Test_StringToNumbers():
        '''Test both the 'string to list of numbers' functionality along with the 
        'string to nested list of numbers' functionality.
        '''
        if 1:   # Empty string returns empty list
            Assert(StringToNumbers("") == [])
        if 1:   # Normal operation
            s = "1 2. 1/3 1+4j"     # The four number types
            n_expected = len(s.split())
            got = StringToNumbers(s)
            expected = [1, 2.0, fractions.Fraction(1, 3), complex(1, 4)]
            Assert(got == expected)
            Assert(n_expected == len(got))
            # Can use 'i' as unit imaginary
            Assert(StringToNumbers("1+i") == [complex(1, 1)])
            Assert(StringToNumbers("1+I") == [complex(1, 1)])
            # Can use comma radix
            Assert(StringToNumbers("1,") == [1.0])
        if 1:   # Normal but unusual input
            s = "nan NaN -inf inf"
            got = StringToNumbers(s)
            expected = [float("nan"), float("nan"), float("-inf"), float("inf")]
            Assert(math.isnan(expected[0]))
            Assert(math.isnan(expected[1]))
            Assert(-math.inf == expected[2])
            Assert(math.inf == expected[3])
        if 1:   # Weird input
            raises(ValueError, StringToNumbers, "1 ekiu 2")
        if 1:   # Getting back a nested list
            s = "1 2\n3 4" 
            expected = [[1, 2], [3, 4]]
            Assert(StringToNumbers(s, sep=" ") == expected)
            Assert(StringToNumbers(s) == expected)
            expected = [1, 2, 3, 4]
            s = "1 2 3 4" 
            Assert(StringToNumbers(s) == expected)

            '''
            >>> StringToNumbers("1 2\n3 4", sep=" ")
            [[1, 2], [3, 4]]
            >>> StringToNumbers("1 2\n3 4", sep=None)
            [1, 2, 3, 4]
            >>> StringToNumbers("1 2 3 4")
            [1, 2, 3, 4]
            '''
        if 1:   # Mike's test cases
            # 2D nesting & spacing
            s_jagged = r'''
            1   2   3
            4   5
            6  7  8  9
            '''
            expected_jagged = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
            assert StringToNumbers(s_jagged) == expected_jagged
            # Testing: Sci-notation, European comma, Fractions, Complex Infinity, and NaNs.
            # Note: Using sep=";" to test explicit separator logic.
            s_gnarly = r'''
                        1.2e-1 ; 1 / 2 ; 1 + i
            nan ; -inf ; 3 + 4i
                        0 ; -0.0 ; 1,23
            42 ; 0 ; inf + inf i ; 0 + 0j
            '''
            result = StringToNumbers(s_gnarly, sep=";")
            # Row 1: float, Fraction, complex
            assert result[0][0] == 0.12
            assert result[0][1] == fractions.Fraction(1, 2)
            assert result[0][2] == (1 + 1j)
            # Row 2: NaN, inf, and complex
            assert math.isnan(result[1][0])
            assert result[1][1] == float('-inf')
            assert result[1][2] == (3 + 4j)
            # Row 3: Zero, signed Zero and comma radix
            assert result[2][0] == 0
            assert result[2][1] == -0.0
            assert result[2][2] == 1.23     # Comma radix case
            # Row 4: The Hitchhiker's Row (Complex Infinity Guard)
            assert result[3][0] == 42
            # This is the "Infinity Shield" test: 'inf + inf i' -> 'inf + inf j'
            assert result[3][2] == complex(float('inf'), float('inf'))
            # 0 and 0+0j are the same mathematically, but in python they have different
            # types
            assert result[3][3] == complex(0, 0) == 0
            assert isinstance(result[3][3], complex)
    def Test_RemoveIndent():
        n = 8
        u = " "*n
        s = f"\n{u}This is a test\n{u}    Second line\n{u}  Third line\n{u}"
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
        expected = "473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8"
        h = GetHash("string")
        Assert(h == expected)
        h = GetHash(b"string")
        Assert(h == expected)
    def Test_EBCDIC():
        a2e, e2a = EBCDIC()
        # Show that these byte translation tables are inverses
        a = bytes((range(256)))
        e = a.translate(a2e)
        a1 = e.translate(e2a)
        Assert(a == a1)
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
        "Also test EscapeSequenceStrip"
        s = "hello world"
        Assert(Len(s) == 11)
        #                          ↓↓↓↓↓↓  Actual string characters
        s = "\x1b[38;2;198;174;239m12.578\x1b[38;2;192;192;192m\x1b[48;2;0;0;0m\x1b[0m"
        Assert(Len(s) == 6)
        u = EscapeSequenceStrip(s)
        Assert(u == "12.578")
    def Test_BuildTagsFile():
        '''Test this in my ~/.manpages directory where there is a collection of *.hld files.
        Manual verification has proven the method works, so now running this file is the way to
        rebuild my ~/.manpages directory's tags file.
        '''
        dir = pathlib.Path("/home/don/.manpages")
        files = list(dir.glob("*.hld"))
        BuildTagsFile(dir, files)
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
            # ReplacementFilter
            print(wrap.dedent('''
 
            ReplacementFilter() returns a function that can replace a sequence of characters
            with a corresponding sequence from another equally-sized list of characters.''')
            )
            s = "abc"
            u = "αβɣ"
            print(f"  Characters to remove  :  {s!r}")
            print(f"  Replacement characters:  {u!r}")
            f = ReplacementFilter(s, u)
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

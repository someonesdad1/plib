"""

Todo
    - Convert token naming conversions to a class
    - Missing tests for GetString, WordID
    - Consider upper & lower keywords for Keep and Remove

String utilities
    Chop             Return a string chopped into equal parts
    CommonPrefix     Return a common prefix of a sequence of strings
    CommonSuffix     Return a common suffix of a sequence of strings
    FilterStr        Return a function that removes characters from strings
    FindFirstIn      Find first item in sequence in a given set
    FindLastIn       Find last item in sequence in a given set
    FindFirstNotIn   Find first item not in sequence in a given set
    FindLastNotIn    Find last item not in sequence in a given set
    FindDiff         Return where two strings first differ
    FindStrings      Find locations of a sequence of strings in a string
    FindSubstring    Return indexes of substring in string
    GetChoice        Return choice from a set of choices (minimizes typing)
    GetLeadingChars  Return leading characters of a string
    GetTrailingChars Return trailing characters of a string
    GetTransFunc     Return a function that translates strings
    GetString        Return string from user that matches choices
    IsASCII          Return True if string is all ASCII characters
    Keep             Return items in sequence that are in keep sequence
    KeepFilter       Returns a function that keeps a set of items in a sequence
    KeepOnlyLetters  Replace all non-word characters with spaces
    Len              Length of string with ANSI escape sequences removed
    ListInColumns    Obsolete (use columnize.py)
    MatchCap         Match string capitalization
    MultipleReplace  Replace multiple patterns in a string
    ReadData         Read data from a multiline string
    Remove           Return items from sequence not in the remove sequence
    RemoveASCII      Remove all ASCII characters from a string
    RemoveComment    Remove '#.*$' from a string
    RemoveFilter     Functional form of Remove (it's a closure)
    RemoveWhitespace Remove whitespace from a string
    RmEsc            Remove ANSI escape strings from string arguments
    Scramble         Randomly shuffle words in a string
    soundex          Return 4-character soundex value for a string
    SoundSimilar     Return True if two strings sound similar
    SpellCheck       Spell check a sequence of words
    SplitOnNewlines  Split on \r, \n, or \r\n
    StringSplit      Pick out specified fields of a string
    Str              String class whose len() ignores ANSI escape sequences
    TimeStr          Readable string for time() in s
    Tokenize         Return a list of tokens from tokenizing a string
    Trim             Remove characters from a string
    WordID           Return an ID string that is somewhat pronounceable
Token naming conversions:
    cw2mc            Cap-words to mixed-case
    cw2us            Cap-words to underscore
    mc2cw            Mixed-case to cap-words
    mc2us            Mixed-case to underscore
    us2cw            Underscore to cap-words
    us2mc            Underscore to mixed-case
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <programming> A number of utilities that deal with strings.
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    # Standard imports
    from collections import deque, defaultdict
    from itertools import filterfalse
    from pdb import set_trace as xx
    import os
    import random
    import re
    import string
    import struct
    import sys
    import time

    # Custom imports
    from f import flt
    from color import t
    from wrap import dedent

    # Global variables
    ii = isinstance
if 1:  # Classes

    class NameConvert:
        'Convert programming naming styles, "Python Cookbook" pg. 91'

        def cw2us(self, x):
            """Cap-words to underscore:
            ALotOfFuss --> a_lot_of_fuss
            """
            if not x:
                return x
            return re.sub(r"(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])", r"_\g<0>", x).lower()

        def cw2mc(self, x):
            """Cap-words to mixed-case:
            ALotOfFuss --> aLotOfFuss
            """
            if not x:
                return x
            return x[0].lower() + x[1:]

        def us2mc(self, x):
            """Underscore to mixed-case:
            a_lot_of_fuss --> aLotOfFuss
            """
            if not x:
                return x
            return re.sub(r"_([a-z])", lambda m: (m.group(1).upper()), x)

        def us2cw(self, x):
            """Underscore to cap-words:
            a_lot_of_fuss --> ALotOfFuss
            """
            if not x:
                return x
            s = self.us2mc(x)
            return s[0].upper() + s[1:]

        def mc2us(self, x):
            """Mixed-case to underscore:
            aLotOfFuss --> a_lot_of_fuss
            """
            if not x:
                return x
            return self.cw2us(x)

        def mc2cw(self, x):
            """Mixed-case to cap-words:
            aLotOfFuss --> ALotOfFuss
            """
            if not x:
                return x
            return x[0].upper() + x[1:]

    class Str(str):
        """This is a str object except that its len() method ignores any ANSI
        escape sequences.  The basic use case is to allow embedded colorizing
        escape sequences in the string without the escape sequences contributing
        to the string's length.

        You can turn off this behavior by setting the .on attribute to False.
        """

        __slots__ = ("on",)

        def __new__(cls, s):
            instance = super(cls, Str).__new__(cls, s)
            instance.on = True
            return instance

        def __len__(self):
            return Len(self) if bool(self.on) else super().__len__()


if 1:  # Core functionality

    def MatchCap(s, t):
        """Return t capitalized as s is.  s and t are expected to be sequences
        of characters.  The returned sequence matches the type of t and has
        a length equal to the shorter of s and t.  Must have len(s) >=
        len(t).

        Example:
            s = "StuVwxyz"
            t = "abcd"
            MatchCap(s, t) = "AbcD"
        """
        if not t:
            return t
        if len(s) < len(t):
            raise ValueError("len(s) must be >= len(t)")
        # Cache our string constants
        if not hasattr(MatchCap, "ac"):
            MatchCap.ac = ac = set(string.ascii_letters)
            MatchCap.uc = uc = set(string.ascii_uppercase)
            MatchCap.lc = lc = set(string.ascii_lowercase)
        else:
            ac, uc, lc = MatchCap.ac, MatchCap.uc, MatchCap.lc
        out = deque()
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
        return "".join(out) if ii(t, str) else type(t)(out)

    def soundex(s):
        """Return the 4-character soundex value to a string argument.  The
        string s must be one word formed with ASCII characters and with no
        punctuation or spaces.  The returned soundex string can be used to
        compare the sounds of words; from US patents 1261167(1918) and
        1435663(1922) by Odell and Russell.

        The algorithm is from Knuth, "The Art of Computer Programming",
        volume 3, "Sorting and Searching", pg. 392:

            1. Retain first letter of name and drop all occurrences
               of a, e, h, i, o, u, w, y in other positions.
            2. Assign the following numbers to the remaining letters
               after the first:
                1: b, f, p, v
                2: c, g, j, k, q, s, x, z
                3: d, t
                4: l
                5: m, n
                6: r
            3. If two or more letters with the same code were adjacent in
               the original name (before step 1), omit all but the first.
            4. Convert to the form "letter, digit, digit, digit" by adding
               trailing zeroes (if there are less than three digits), or
               by dropping rightmost digits (if there are more than
               three).
        """
        if not s:
            raise ValueError("Argument s must not be empty string")
        if set(s) - set(string.ascii_letters):
            raise ValueError("String s must contain only ASCII letters")
        if not hasattr(soundex, "m"):
            soundex.m = dict(
                zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "01230120022455012623010202")
            )

        # Function to map lower-case letters to soundex number
        def getnum(x):
            return [soundex.m[i] for i in x]

        t = s.upper()
        num, keep = getnum(t), []
        # Step 0 (and step 3): keep only those letters that don't map to
        # the same number as the previous letter.
        for i, code in enumerate(num):
            if not i:
                keep.append(t[0])  # Always keep first letter
            else:
                if code != num[i - 1]:
                    keep.append(t[i])
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

    def SoundSimilar(s, t):
        "Return True if the strings s and t sound similar"
        return True if soundex(s) == soundex(t) else False

    def CommonPrefix(seq):
        """Return the largest string that is a prefix of all the strings in
        seq.
        """
        return os.path.commonprefix(seq)

    def CommonSuffix(seq):
        """Return the largest string that is a suffix of all the strings in
        seq.
        """

        # Method: reverse each string in seq, find their common prefix, then
        # reverse the result.
        def f(lst):
            return "".join(lst)  # Convert the list back to a string

        def rev(s):  # Reverse the string s
            return f([f(list(i)) for i in reversed(s)])

        return rev(CommonPrefix([rev(i) for i in seq]))

    def FindFirstIn(s, items, invert=False):
        """Return smallest integer i such that s[i] is in items or else
        None.  If invert is True, find the smallest integer i such that
        s[i] is not in items.

        if s is a reversed type, then we're searching for the last
        index of the item in items if invert is False or the last
        index of the first item in reversed(s) that's in items when
        invert is True.
        """
        if not s or not items:
            return None
        set_of_items = set(items)
        # If s is a reversed iterator, convert it to a list so s[i]
        # doesn't fail
        rev = ii(s, reversed)
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
        """Return a list (or a string if s is a string) of the items in s that
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
        """
        kp = set(keep)
        if left or middle or right:
            whole = False
        if whole:
            result = []
            for i in s:
                if i in kp:
                    result.append(i)
            return "".join(result) if ii(s, str) else result
        else:
            sl = FindFirstNotIn(s, keep)
            sr = FindLastNotIn(s, keep)
            # Get components
            s_left = s[:sl]
            s_right = s[sr + 1 :]
            s_middle = s[sl : sr + 1]
            # Check invariant
            if s_left + s_middle + s_right != s:
                if ii(s, str):
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
            if ii(s, str):
                return "".join(result)
            else:
                return result

    def KeepFilter(keep):
        """Return a function that takes a string and returns a string
        containing only those characters that are in keep.
        """

        def func(s):
            return Keep(s, keep, whole=True)

        return func

    def Remove(s, remove):
        "Return a sequence of the items in s that are not in remove"
        r = set(remove)

        def f(x):
            return x in r

        ret = filterfalse(f, s)
        return "".join(ret) if isinstance(s, str) else type(s)(ret)

    def RemoveFilter(remove):
        """Return a function that takes a string and returns a string
        containing only those characters that are not in remove.
        """

        def func(s):
            return Remove(s, remove)

        return func

    def RemoveWhitespace(s):
        """Remove whitespace characters from the string s.  Whitespace
        characters are:  space, tab, linefeed, return, formfeed and
        vertical tab, which are ' ', \t, \n, \r, \f, and \v.
        """
        # This is a specialized fast method because it's done by C code
        return "".join(s.split())

    def FilterStr(remove, replacements):
        """Return a function that removes the characters in sequence remove
        from other strings and replaces them with corresponding characters
        in the sequence replacements.
        """
        if len(remove) != len(replacements):
            raise ValueError("remove and replacements must be the same length")
        T = "".maketrans(dict(zip(remove, replacements)))
        return lambda s: s.translate(T)

    def FindDiff(s1, s2, ignore_empty=False, equal_length=False):
        """Returns the integer index of where the strings s1 and s2 first
        differ.  The number returned is the index where the first
        difference was found.  If the strings are equal, then -1 is
        returned, implying one string is a substring of the other (or they
        are the same string).  If ignore_empty is False, an exception is
        raised if one of the strings is empty.  If equal_length is True,
        then the strings must be of equal length or a ValueError exception
        is raised.
        """
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Arguments must be strings")
        if (not s1 or not s2) and not ignore_empty:
            raise ValueError("String cannot be empty")
        ls1, ls2 = len(s1), len(s2)
        if equal_length and ls1 != ls2:
            raise ValueError("Strings must be equal lengths")
        n = min(ls1, ls2)
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
        """Return list of (i, j) pairs which indicate where the strings in
        sequence seq (index i) are located in string Str (index j).  An
        empty list is returned if there are no matches.

        Example:
            seq = "Jan Feb Mar".split()
            Str = "1Jan2001"
            found = FindStrings(seq, Str)
            Then found is [(0, 1)]
        """
        found, s, sq = [], Str, seq
        if ignorecase:
            # Make copy so we don't change the original seq
            s = Str.lower()
            sq = [i.lower() for i in seq]
        for i, u in enumerate(sq):
            j = Str.find(u)
            if j != -1:
                found.append((i, j))
        return found

    def FindSubstring(mystring, substring):
        """Return a tuple of the all the indexes of where the substring is
        found in the string mystring.
        """
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

    def GetString(prompt_msg, default, allowed_values, ignore_case=True):
        """Get a string from a user and compare it to a sequence of
        allowed values.  If the response is in the allowed values, return
        it.  Otherwise, print an error message and ask again.  The letter
        'q' or 'Q' will let the user quit the program.  The returned
        string will have no leading or trailing whitespace.
        """
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
            print("'%s' is not a valid response" % response.strip())

    def GetChoice(name, names):
        """name is a string and names is a set or dict of strings.  Find
        if name uniquely identifies a string in names; if so, return it.
        If it isn't unique, return a list of the matches.  Otherwise
        return None.  The objective is to allow name to be the minimum
        length string necessary to uniquely identify the choice.
        """
        # See self tests below for an example of use
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if not isinstance(names, (set, dict)):
            raise ValueError("names must be a set or dictionary")
        d, n = defaultdict(list), len(name)
        for i in names:
            d[i[: len(name)]] += [i]
        if name in d:
            if len(d[name]) == 1:
                return d[name][0]
            else:
                return d[name]
        return None

    def KeepOnlyLetters(s, underscore=False, digits=False):
        """Replace all non-word characters with spaces.  If underscore is
        True, keep underscores too (e.g., typical for programming language
        identifiers).  If digits is True, keep digits too.
        """
        allowed = string.ascii_letters + "_" if underscore else string.ascii_letters
        allowed += string.digits if digits is True else ""
        c = [chr(i) for i in range(256)]
        t = "".join([i if i in allowed else " " for i in c])
        return s.translate(t)

    def StringSplit(fields, string, remainder=True, strict=True):
        """Pick out the specified fields of the string and return them as
        a tuple of strings.  fields can be either a format string or a
        list/tuple of numbers.

        Field numbering starts at 0.  If strict is True, then the indicated
        number of fields must be returned or a ValueError exception will be
        raised.

        fields is a format string
            A format string is used to get particular columns of the
            string.  For example, the format string "5s 3x 8s 8s" means to
            pick out the first five characters of the string, skip three
            spaces, get the next 8 characters, then the next 8 characters.
            If remainder is False, this is all that's returned; if
            remainder is True, then whatever is left over will also be
            returned.  Thus, if remainder is False, you'll have a 3-tuple
            of strings returned; if True, a 4-tuple.

        fields is a sequence of numbers
            The numbers specify cutting the string at the indicated
            columns (numbering is 0-based).  Example: for the input string
            "hello there", using the fields of [3, 7] will return the tuple
            of strings ("hel", "lo t", "here").
                "hello there"
                 01234567890

        Derived from code by Alex Martelli at
        http://code.activestate.com/recipes/65224-accessing-substrings/
        Downloaded Sun 27 Jul 2014 07:52:44 AM
        """
        if isinstance(fields, str):
            left_over = len(string) - struct.calcsize(fields)
            if left_over < 0:
                raise ValueError("string is shorter than requested format")
            format = "%s %ds" % (fields, left_over)
            s = bytes(string.encode("ascii"))
            result = list(struct.unpack(format, s))
            return result if remainder else result[:-1]
        else:
            pieces = [string[i:j] for i, j in zip([0] + fields, fields)]
            if remainder:
                pieces.append(string[fields[-1] :])
            num_expected = len(fields) + 1
            if num_expected != len(pieces) and strict:
                raise ValueError(
                    "Expected %d pieces; got %d" % (num_expected, len(pieces))
                )
            return pieces

    def ListInColumns(alist, col_width=0, num_columns=0, space_betw=0, truncate=0):
        """Returns a list of strings with the elements of alist (if
        components are not strings, they will be converted to strings
        using str) printed in columnar format.  Elements of alist that
        won't fit in a column either generate an exception if truncate is
        0 or get truncated if truncate is nonzero.  The number of spaces
        between columns is space_betw.

        If col_width and num_columns are 0, then the program will set them
        by reading the COLUMNS environment variable.  If COLUMNS doesn't
        exist, col_width will default to 80.  num_columns will be chosen
        by finding the length of the largest element so that it is not
        truncated.

        Caveat: if there are a small number of elements in the list, you
        may not get what you expect.  For example, try a list size of 1 to
        10 with num_columns equal to 4: for lists of 1, 2, 3, 5, 6, and 9,
        you'll get fewer than four columns.

        This function is obsolete; instead, use Columnize in columnize.py.
        """
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
                i = int(num_rows * column + row)
                if 0 <= i <= (N - 1):
                    if len(str(alist[i])) > col_width:
                        if truncate:
                            s += str(alist[i])[:col_width] + " " * space_betw
                        else:
                            raise ValueError("Error: element %d too long" % i)
                    else:
                        s += (
                            str(alist[i])
                            + " " * (col_width - len(str(alist[i])))
                            + " " * space_betw
                        )
            lines.append(s)
        assert len(lines) == num_rows
        t.print(
            f"{t('ornl')}dpstr.ListInColumns is obsolete.  Use columnize.Columnize.",
            file=sys.stderr,
        )
        return lines

    def MultipleReplace(text, patterns, flags=0):
        """Replace multiple patterns in the string text.  patterns is a
        dictionary whose keys are the regular expressions and values are the
        replacement text.  The flags keyword variable is the same as that used
        by the re.compile function.

        From page 88 of Python Cookbook.
        """
        # Make a compound regular expression from all the keys
        r = re.compile("|".join(map(re.escape, patterns.keys())), flags)
        # For each match, look up the corresponding value in the dictionary
        return r.sub(lambda match: patterns[match.group(0)], text)

    def RemoveComment(line, code=False):
        """Remove the largest string starting with '#' from the string
        line.  If code is True, then the resulting line will be compiled
        and an exception will occur if the modified line won't compile.
        This typically happens if '#' is inside of a comment.
        """
        orig = line
        loc = line.find("#")
        if loc != -1:
            line = line[:loc]
        if code:
            try:
                compile(line, "", "single")
            except Exception:
                msg = "Line with comment removed won't compile:\n  '%s'" % orig
                raise ValueError(msg)
        return line

    def SpellCheck(input, Words, ignore_case=True):
        """input is a sequence of word strings; Words is a dictionary or set
        of correct spellings.  Return the set of any words in input that are not
        in Words.
        """
        misspelled = set()
        if not input:
            return []
        if not Words:
            raise ValueError("Words parameter is empty")
        for word in input:
            if ignore_case:
                word = word.lower()
            if word not in Words:
                misspelled.add(word)
        return misspelled

    def SplitOnNewlines(s):
        """Splits s on all of the three newline sequences: "\r\n", "\r", or
        "\n".  Returns a list of the strings.

        Copyright (c) 2002-2009 Zooko Wilcox-O'Hearn, who put it under the GPL.
        """
        cr, nl = "\r", "\n"
        res = []
        for x in s.split(cr + nl):
            for y in x.split(cr):
                res.extend(y.split(nl))
        return res

    def TimeStr(time_in_s=None):
        """Return a readable string for the indicated time in seconds.
        If the parameter is None, the time is time.now().  Example:
            Time(1646408691.9415808) returns '4Mar2022-084451.942am'
        This is a convenience aimed at producing names that can be used
        in a filename for things like timestamping.
        """

        def Rm0(s):
            if s.startswith("0"):
                return s[1:]
            return s

        # The /plib/0test.py file in this file's directory uses this method to
        # produce log files when it is run.
        #
        # Get t as time in seconds from the epoch (note it is local time, not
        # GMT)
        T = time_in_s if time_in_s else time.time()
        # ts will contain the time structure needed by time's functions
        ts = time.localtime(T)
        # Date portion
        d = Rm0(time.strftime("%d%b%Y", ts))
        t = time.strftime("%I%M%S", ts)
        ampm = time.strftime("%p", ts).lower()
        # Get fractions of seconds.  Resolution is to the nearest μs because
        # this gave what looked to be sufficient time resolution on my system
        # to avoid generating an accidental collision, at least in the same
        # process.
        n = 6
        fs = round(T - int(T), n)
        f = Rm0(f"{fs:.{n}f}")
        return f"{d}-{t}{f}{ampm}"

    def WordID(half_length=3, unique=None, num_tries=100):
        """Return an ID string that is (somewhat) pronounceable.  The
        returned number of characters will be twice the half_length.  If
        unique is not None, it must be a container that can be used to
        determine if the ID is unique.  You are responsible for adding the
        returned word to the container.

        The method is to choose a consonant from 'bdfghklmnprstvw' and append a
        vowel; do this half_length number of times.

        Interestingly, the words often look like they come from Japanese or
        Hawaiian.
        """
        # Derived from http://code.activestate.com/recipes/576858
        # downloaded Tue 12 Aug 2014 12:38:54 PM.  Original recipe by
        # Robin Parmar on 8 Aug 2007 under PSF license.
        v, c, r, count = "aeiou", "bdfghklmnprstvw", range(half_length), 0
        while count < num_tries:
            word = "".join([random.choice(c) + random.choice(v) for i in r])
            if not unique or (unique and word not in unique):
                return word
            count += 1
        raise RuntimeError("Couldn't generate unique word")
        """Here's some driver code that prints out lists of these words:
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
        """

    def Chop(seq, size):
        """Return a list of the sequence seq chopped into subsequences of
        length size.  The last subsequence will be shorter than size if
        len(seq) % size is not zero.
        """
        if not ii(size, int) or size <= 0:
            raise ValueError("size must be integer > 0")
        out = []
        for i in range(0, len(seq), size):
            out.append(seq[i : i + size])
        return out

    def ReadData(data, structure, **kw):
        '''Read data from a multiline string data.  structure is a list of the
        field types.  Any line starting with optional whitespace and the
        comment string is ignored, as is any line with only whitespace.

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
        the call ReadData(data, structure=[str, int, int, int, int] returns
        the list
            [["9", 680, 2100, 0, 750],
            ["10", 680, 2100, 250, 750]]

        If an error occurs, the 1-based line number of the offending string
        will be printed along with the problem.
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
                if ii(comment, str) and line.startswith(comment):
                    continue
                elif hasattr(comment, "search"):
                    # It's a compiled regular expression
                    if comment.search(line):
                        continue
            if sep is not None:
                if ii(sep, str):
                    fields = line.split(sep)
                elif hasattr(sep, split):
                    fields = sep.split(line)
                else:
                    raise ValueError("sep '{sep}' is unknown type")
            else:
                fields = line.split()
            if len(fields) != len(structure):
                n, m = len(fields), len(structure)
                msg = dedent(f"""
                Line {linenum} has {n} field{"s" if n > 1 else ""}
                The structure list has {m} field{"s" if m > 1 else ""}
                They must be the same.
                """)
                raise ValueError(msg)
            thisline = []
            for i in range(len(structure)):
                thisline.append(structure[i](fields[i]))
            out.append(thisline)
        return out

    def Len(s) -> int:
        """Same as built-in len(), except if the argument is a str, the ANSI
        escape sequences are stripped out.
        """
        if not hasattr(Len, "len"):
            # Cache the built-in len in case someone redefines it
            Len.len = len
        if ii(s, str):
            return Len.len(RmEsc(s))
        return Len.len(s)

    def RmEsc(s: str, on=True) -> str:
        "Remove ANSI escape strings if on is True; otherwise just return s"
        # The primary use case is to remove colorizing ANSI escape strings from
        # a string s.  Not all ANSI escape strings are supported, just the ones
        # that contain a CSI sequence.
        if not on:
            # Note it's deliberate that we don't check the type of s if on is
            # False; this makes this the identity function for any type.
            return s
        assert ii(s, str)
        if not hasattr(RmEsc, "r"):
            # This regexp was constructed from the information given on the
            # page https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences
            # This is:
            #   ESC [
            # then "parameter bytes":    zero or more bytes 0x30-0x3f       [0-?]
            # then "intermediate bytes": zero or more bytes 0x20-0x2f       [ -/]
            # then "single byte":        one byte in range of 0x40-0x7e     [@-~]
            RmEsc.r = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
        return RmEsc.r.sub("", s)

    def Tokenize(s, wordchars=None, check=False):
        """Split the string s into a list lst such that ''.join(lst) is the
        original string.  wordchars is a sequence of characters that are in
        words.  wordchars defaults to string.ascii_letters + string.digits.  If
        check is True, verify the invariant s == ''.join(lst).
        """
        if not ii(s, str):
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
            out.append("".join(word))
        if check and "".join(out) != s:
            raise ValueError("Invariant s == ''.join(out) is not True")
        return out

    def GetLeadingChars(s, chars=None):
        """Return the string defining the leading characters in the string
        s.  If chars is not None, use it as the set of allowed leading
        characters.  If chars is None, then return the leading whitespace
        characters, which are defined by the re module's '\\s'
        metacharacters.
        """
        if not ii(s, str):
            raise TypeError("s must be a string")
        if chars is None:
            r = re.compile(r"^(\s+).*$", re.M)
            mo = r.match(s)
            return mo.groups()[0] if mo else ""
        else:
            S = set(chars)
            t = re.escape("".join(S))
            r = re.compile(f"^([{t}]+).*$", re.M)
            mo = r.match(s)
            return mo.groups()[0] if mo else ""

    def GetTrailingChars(s, chars=None):
        """Return the string defining the trailing characters in the string
        s.  If chars is not None, use it as the set of allowed trailing
        characters.  If chars is None, then return the leading whitespace
        characters, which are defined by the re module's '\\s'
        metacharacters.
        """
        if not ii(s, str):
            raise TypeError("s must be a string")
        if chars is None:
            r = re.compile(r"^[^\s]*(\s+)$", re.M)
            mo = r.match(s)
            return mo.groups()[0] if mo else ""
        else:
            S = set(chars)
            t = re.escape("".join(S))
            r = re.compile(f"([{t}]+)$", re.M)
            mo = r.search(s)
            return mo.groups()[0] if mo else ""

    def RemoveASCII(s):
        """Remove ASCII characters from string s.  This means the string
        only consists of characters chr(0x0) to chr(0x7e) inclusive or
        Unicode characters above 0x7f.
        """
        if not hasattr(RemoveASCII, "table"):
            # Cache a translation table
            r = range(0, 0x7F)
            chars = [chr(i) for i in r]
            none = [None] * len(chars)
            RemoveASCII.table = "".maketrans(dict(zip(chars, none)))
        return s.translate(RemoveASCII.table)

    def IsASCII(s):
        """Return True if string s is all ASCII characters.  This means the
        string only consists of characters chr(0x0) to chr(0x7e) inclusive.
        """
        return not bool(RemoveASCII(s))

    def Scramble(mystring, punc=None, start_end_const=False):
        """Return a string with the letters in the words randomly shuffled
        but with the punctuation and whitespace unchanged if punc is None.

        Set punc to a different set of punctuation characters if you wish
        (the punctuation characters are ignored when shuffling words).  For
        example, you might want to include common Unicode characters
        included as punctuation also.

        If start_end_const is True, then the first and last letters of each
        word are unchanged.  This lets you test the assertion that leaving
        the first and last letters intact but shuffling the interior
        letters doesn't change the readability of the text.  Personally,
        I've found that's mostly nonsense except for some fairly easy
        pieces of text.  In particular, doing this scrambling on a
        complicated technical document virtually always results in
        jibberish.

        If you wish to save memory, make mystring a list of individual
        characters; then a copy of the string isn't made.  Note there is no
        check that the list's elements are single character strings.

        Example with random.seed('0'):
            s = '"Hello there", said John.'
        returns
                '"loeHl eerth", isda noJh.'
        """
        if punc is None:
            punc = set(string.punctuation + string.whitespace)
        dummy = "."
        prepended = appended = False
        is_string = ii(mystring, str)
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
        """Remove characters in the string chars from the left and right
        sides of s, returning the result.

        This routine breaks s into three strings L, M, and R such that s =
        L + M + R.  L and R consist only of characters in chars.  The
        returned string is
            left    right       returned
            ----    -----     -------------
            True    True            M
            True    False         M + R
            False   True          L + M
            False   False     s = L + M + R
        If check is True, the invariants are validated.
        """
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
                assert set(L).issubset(charset)
                assert set(R).issubset(charset)
        if left:
            return M if right else M + R
        else:
            return L + M

    def GetTransFunc(chars_from, to, delete=None):
        """Return a function that will change characters in chars_from to the characters in to.
        This function will use str.translate() to perform its work at C speeds.  If chars_from has
        N characters, then to must have 1 or N characters.  The rules are:

            - Any characters in the sequence delete are deleted from chars_from.
            - If delete is not None, then it must be a str whose characters are deleted from the
              string.
            - If to has 1 character, then remaining characters in the string will be replaced by
              the character in to.

        Example:  Let chars_from = string.punctuation and to = " ".  Then GetTransFunc(chars_from,
        to) returns a function f that substitutes a space character for every punctuation
        character.  Given a string s, f(s) returns a string of the same length as s but with all
        ASCII punctuation characters replaced by a string.
        """
        if not chars_from:
            return lambda x: x
        N = len(chars_from)
        if len(to) not in (1, N):
            raise ValueError("to must have 1 or len(chars_from) characters")
        From, To = chars_from, to
        if len(to) == 1:
            From, To = chars_from, to * N
        # Check delete
        if delete is None:
            Delete = None
        elif not ii(delete, str):
            raise TypeError("delete must be None or a string")
        else:
            Delete = "".join(set(delete))
        # Make the translation table
        tt = str.maketrans(From, To, Delete) if Delete else str.maketrans(From, To)

        # Now make the function
        def f(s):
            return s.translate(tt)

        return f


if __name__ == "__main__":
    from lwtest import run, raises, assert_equal, Assert
    import math
    import os
    from sig import sig
    from color import TRM as t

    def Test_GetTransFunc():
        From = """Mr. Dee, a, a--b; 'z' and "a", ok."""
        expected = """r  Dee  a  a  b   z  and  a   ok """
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
            Assert(F("", "abc") == None)
            Assert(L("", "abc") == None)
            Assert(F("abc", "") == None)
            Assert(L("abc", "") == None)
            Assert(F("abc", "d") == None)
            Assert(L("abc", "d") == None)
            #
            Assert(F("dabc", "d") == 0)
            Assert(L("dabc", "d") == 0)
            Assert(F("abc;d", ";") == 3)
            Assert(L("abc;de", ";") == 3)
            Assert(L("abc;", ";") == 3)
            Assert(L(";abc;", ";") == 4)
        if 1:  # FindFirstNotIn, FindLastNotIn
            F, L = FindFirstNotIn, FindLastNotIn
            Assert(F("", "abc") == None)
            Assert(L("", "abc") == None)
            Assert(F("abc", "") == None)
            Assert(L("abc", "") == None)
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
        for t in (
            "",
            " ",
            "  ",
            "\t",
            "\n",
            "\t\r\n\f    \t\t\t",
        ):
            Assert(GetLeadingChars(t) == t)
            Assert(GetLeadingChars(t + "a") == t)
            Assert(GetTrailingChars(t) == t)
            Assert(GetTrailingChars("a" + t) == t)
        # Define custom sets of whitespace
        if 1:  # Leading
            Assert(GetLeadingChars("  \t  a", chars="z") == "")
            Assert(GetLeadingChars("  \t  a", chars="\t") == "")
            Assert(GetLeadingChars("  \t  a", chars=" ") == "  ")
            ws, t = ".;:", ".;..:::."
            a = GetLeadingChars(t + "a", chars=ws)
            Assert(a == t)
        if 1:  # Trailing
            Assert(GetTrailingChars("a  \t  ", chars="z") == "")
            Assert(GetTrailingChars("a  \t  ", chars="\t") == "")
            Assert(GetTrailingChars("a  \t  ", chars=" ") == "  ")
            ws, t = ".;:", ".;..:::."
            a = GetTrailingChars("a" + t, chars=ws)
            Assert(a == t)

    def Test_Tokenize():
        Assert(Tokenize("", check=True) == [])
        Assert(Tokenize(" ", check=True) == [" "])
        Assert(Tokenize(" " * 2, check=True) == [" ", " "])
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
        s = dedent(f"""
        This is some multiline
        text with {t("purl")}some
        escape codes.{t.n}
        """)
        u = RmEsc(s)
        Assert(Len(s) == len(u))

    def Test_ReadData():
        data = """
                    #
                    9 , 680  ,  2100  , 0  ,    750
                    10,  680  ,  2100  , 250    ,750
        """
        o = ReadData(data, structure=[str, int, int, int, int], sep=",", comment="#")
        # Note the space after '9'
        e = [["9 ", 680, 2100, 0, 750], ["10", 680, 2100, 250, 750]]
        Assert(o == e)
        o = ReadData(data, structure=[str, flt, int, int, int], sep=",", comment="#")
        e = [["9 ", flt(680), 2100, 0, 750], ["10", flt(680), 2100, 250, 750]]
        Assert(o == e)
        data = """
                    9  680    2100   0      750
                        10  680    2100   250    750
        """
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

    def Test_MatchCap():
        t = "AbCdEf"
        # s needs to have as many characters as t
        raises(ValueError, MatchCap, "", t)
        # Empty string returns empty string
        Assert(MatchCap("", "") == "")
        Assert(MatchCap(t, "") == "")
        # No letters in s just gets t back if length sufficient
        Assert(MatchCap("∞∞∞∞∞∞", t) == t)
        # Idempotent
        Assert(MatchCap(t, t) == t)
        Assert(MatchCap("", "") == "")
        # Routine use
        Assert(MatchCap(t.lower(), t) == t.lower())
        Assert(MatchCap(t.upper(), t) == t.upper())
        Assert(MatchCap("T", "t") == "T")
        Assert(MatchCap("t", "T") == "t")
        Assert(MatchCap("MatchCap", t) == "AbcdeF")
        Assert(MatchCap("MATCHCAP", t) == "ABCDEF")
        Assert(MatchCap("matchcap", t) == "abcdef")
        Assert(MatchCap("matchcap", t) == "abcdef")
        s = "StuVwxyz"
        t = "abcd"
        Assert(MatchCap(s, t) == "AbcD")

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
        raises(TypeError, CommonPrefix, ["a", 1])

    def Test_CommonSuffix():
        Assert(not CommonSuffix(["a", "b"]))
        Assert("a" == CommonSuffix(["onea", "twoa", "threea"]))
        Assert("abc" == CommonSuffix(["abc", "abc", "abc"]))
        raises(TypeError, CommonSuffix, ["a", 1])

    def Test_FilterStr():
        s = '''"Not that easy, I'm sure."'''
        f = FilterStr(""""',.""", [None] * 4)
        t = f(s)
        Assert(t == "Not that easy Im sure")

    def Test_RemoveWhitespace():
        s = "a b\tc\nd\re\ff\vg"
        t = RemoveWhitespace(s)
        Assert(t == "abcdefg")

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
        Assert(t == expected + " " * 4)
        t = KeepOnlyLetters(s, underscore=True, digits=False)
        Assert(t == expected + " " * 3 + "_")

    def Test_StringSplit():
        s = "hello there"
        Assert(StringSplit([4, 7], s) == ["hell", "o t", "here"])
        t = "3s 3x 4s"

        def f(x):
            return bytes(x, encoding="ascii")

        q = [f("hel"), f("ther"), f("e")]
        Assert(StringSplit(t, s, remainder=True) == q)
        Assert(StringSplit(t, s, remainder=False) == q[:-1])

    def Test_ListInColumns():
        if 0:
            s = [sig(math.sin(i / 20), 3) for i in range(20)]
            got = "\n".join(ListInColumns(s))
            ts = "  "  # Note there are two spaces after these rows...
            exp = "0.00   0.0998 0.199  0.296  0.389  0.479  0.565  0.644  0.717  0.783"
            exp += ts
            exp += "\n"
            exp += (
                "0.0500 0.149  0.247  0.343  0.435  0.523  0.605  0.682  0.751  0.813"
            )
            exp += ts
            Assert(got == exp)

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
        text = """This
        is some
        text"""
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

    def Demo():
        "Demonstrate the various functions to stdout"
        print(f"{t('ornl')}Demo of /plib/dpstr.py functions{t('skyl')}")
        if 0:  # xx
            # Chop
            s = "abcdefghij"
            print(f"Chop({s!r}, 3) = {Chop(s, 3)}")
            # CommonPrefix and CommonSuffix
            s = ["a.b.c", "a.c.c", "a.d.c"]
            print(f"CommonPrefix({s!r}) = {CommonPrefix(s)}")
            print(f"CommonSuffix({s!r}) = {CommonSuffix(s)}")
            # FilterStr
            print(
                dedent("""
 
            FilterStr() returns a function that can replace a sequence of characters
            with a corresponding sequence from another equally-sized list of characters.""")
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
            print(f"  The functions return the 0-based index of the found item")
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
            # GetLeadingChars, GetTrailingChars
            s = "this STRING HAS UPPER AND LOWER CASE letters"
            chars = string.ascii_lowercase
            print(
                f"GetLeadingChars({s!r},\n {' ' * 15}{chars!r}) = "
                f"{GetLeadingChars(s, chars)}"
            )
            # IsASCII
            s, u = "abc", "∞"
            print(f"IsASCII({s!r}) = {IsASCII(s)}, IsASCII({u!r}) = {IsASCII(u)}")
            # Keep
            print(f"Keep is used to keep only desired elements in a sequence")
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
            print(f"KeepFilter returns a filter based on Keep's arguments")
            print(f"  f = KeepFilter returns a filter based on Keep's arguments")
            f = KeepFilter(string.ascii_lowercase)
            print(f"  f = KeepFilter(string.ascii_lowercase + )")
            s = "this STRING"
            print(f"  f({s!r}) = {f(s)}")
        # KeepOnlyLetters
        s = "88; Hello    there!"
        print(f"KeepOnlyLetters({s!r}) = {KeepOnlyLetters(s)!r}")
        # MatchCap
        s = "StuVwxyz"
        u = "abcd"
        print(f"MatchCap({s!r}, {u!r}) = {MatchCap(s, u)!r}")
        # MultipleReplace
        t.print(end="")

    if len(sys.argv) > 1:
        Demo()
        exit()
    exit(run(globals(), regexp="^Test", halt=1)[0])

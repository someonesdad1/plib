#TODO
#  * Convert token naming conversions to a class
#  * Missing tests for GetString, WordID
'''
String utilities
    CommonPrefix     Return a common prefix of a sequence of strings
    CommonSuffix     Return a common suffix of a sequence of strings
    FilterStr        Return a function that removes characters from strings
    FindDiff         Return where two strings first differ
    FindSubstring    Return indexes of substring in string
    GetChoice        Return choice from a set of choices (minimizes typing)
    GetString        Return string from user that matches choices
    Keep             Return items in sequence that are in keep sequence
    KeepFilter       Returns a function that will keep a character set
    KeepOnlyLetters  Replace all non-word characters with spaces
    ListInColumns    Obsolete (use columnize.py)
    MatchCap         Match string capitalization
    MultipleReplace  Replace multiple patterns in a string
    Remove           Return items from sequence not in the remove sequence
    RemoveComment    Remove '#.*$' from a string
    RemoveFilter     Functional form of Remove (it's a closure)
    soundex          Return 4-character soundex value for a string
    SoundSimilar     Return True if two strings sound similar
    SpellCheck       Spell check a sequence of words
    SplitOnNewlines  Split on \r, \n, or \r\n
    StringSplit      Pick out specified fields of a string
    WordID           Return an ID string that is somewhat pronounceable
    
    Token naming conversions:
    cw2mc
    cw2us
    mc2cw
    mc2us
    us2cw
    us2mc
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> A number of utilities that deal with strings.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    from collections import deque, defaultdict
    import re
    import string
    import struct
    import sys
    from itertools import filterfalse
    from random import choice
    from pdb import set_trace as xx 
if 1:  # Global variables
    ii = isinstance
def MatchCap(s, t):
    '''Return t capitalized as s is.  s and t are expected to be sequences
    of characters.  The returned sequence matches the type of t.
    '''
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
    return ''.join(out) if ii(t, str) else type(t)(out)
def soundex(s):
    '''Return the 4-character soundex value to a string argument.  The
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
            1:  b, f, p, v
            2:  c, g, j, k, q, s, x, z
            3:  d, t
            4:  l
            5:  m, n
            6:  r
        3. If two or more letters with the same code were adjacent in
           the original name (before step 1), omit all but the first.
        4. Convert to the form "letter, digit, digit, digit" by adding
           trailing zeroes (if there are less than three digits), or
           by dropping rightmost digits (if there are more than
           three).
    '''
    if not s:
        raise ValueError("Argument s must not be empty string")
    if set(s) - set(string.ascii_letters):
        raise ValueError("String s must contain only ASCII letters")
    if not hasattr(soundex, "m"):
        soundex.m = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             "01230120022455012623010202"))
    # Function to map lower-case letters to soundex number
    getnum = lambda x: [soundex.m[i] for i in x]
    t = s.upper()
    num, keep = getnum(t), []
    # Step 0 (and step 3):  keep only those letters that don't map to
    # the same number as the previous letter.
    for i, code in enumerate(num):
        if not i:
            keep.append(t[0])   # Always keep first letter
        else:
            if code != num[i - 1]:
                keep.append(t[i])
    # Step 1:  remove vowels, etc.
    first_letter = keep[0]
    ignore, process = set("AEHIOUWY"), []
    process += [i for i in keep[1:] if i not in ignore]
    # Step 2:  assign numbers for remaining letters
    code = first_letter + ''.join(getnum(''.join(process)))
    # Step 3:  same as step 0
    # Step 4:  adjust length
    if len(code) > 4:
        code = code[:4]
    while len(code) < 4:
        code += "0"
    return code
def SoundSimilar(s, t):
    'Return True if the strings s and t sound similar'
    return True if soundex(s) == soundex(t) else False
def CommonPrefix(seq):
    '''Return the largest string that is a prefix of all the strings in
    seq.
    '''
    return os.path.commonprefix(seq)
def CommonSuffix(seq):
    '''Return the largest string that is a suffix of all the strings in
    seq.
    '''
    # Method:  reverse each string in seq, find their common prefix, then
    # reverse the result.
    f = lambda lst:  ''.join(lst)   # Convert the list back to a string
    def rev(s):     # Reverse the string s
        return f([f(list(i)) for i in reversed(s)])
    return rev(CommonPrefix([rev(i) for i in seq]))
def Keep(s, keep):
    '''Return a list (or a string if s is a string) of the items in s that
    are in keep.
    '''
    k = set(keep)
    if 0:
        f = lambda x: x not in k
        ret = filterfalse(f, s)
    f = lambda x: x in k
    ret = filter(f, s)
    return ''.join(ret) if isinstance(s, str) else list(ret)
def KeepFilter(keep):
    '''Return a function that takes a string and returns a string
    containing only those characters that are in keep.
    '''
    def func(s):
        return Keep(s, keep)
    return func
def Remove(s, remove):
    'Return a sequence of the items in s that are not in remove'
    r = set(remove)
    f = lambda x: x in r
    ret = filterfalse(f, s)
    return ''.join(ret) if isinstance(s, str) else type(s)(ret)
def RemoveFilter(remove):
    '''Return a function that takes a string and returns a string
    containing only those characters that are not in remove.
    '''
    def func(s):
        return Remove(s, remove)
    return func
def FilterStr(remove, replacements):
    '''Return a function that removes the characters in sequence remove
    from other strings and replaces them with corresponding characters
    in the sequence replacements.
    '''
    if len(remove) != len(replacements):
        raise ValueError("remove and replacements must be the same length")
    T = ''.maketrans(dict(zip(remove, replacements)))
    return lambda s:  s.translate(T)
def FindDiff(s1, s2, ignore_empty=False, equal_length=False):
    '''Returns the integer index of where the strings s1 and s2 first
    differ.  The number returned is the index where the first
    difference was found.  If the strings are equal, then -1 is
    returned, implying one string is a substring of the other (or they
    are the same string).  If ignore_empty is True, an exception is
    raised if one of the strings is empty.  If equal_length is True,
    then the strings must be of equal length or a ValueError exception
    is raised.
    '''
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Arguments must be strings")
    if (not s1 or not s2) and not ignore_empty:
        raise ValueError("String cannot be empty")
    ls1, ls2 = len(s1), len(s2)
    if equal_length and ls1 != ls2:
        raise ValueError("Strings must be equal lengths")
    n = min(len(s1), len(s2))
    if not n:
        return 0
    for i in range(n):
        if s1[i] != s2[i]:
            return i
    # If we get here, every character matched up to the end of the
    # shorter string.
    return -1
def FindSubstring(mystring, substring):
    '''Return a tuple of the indexes of where the substring is found
    in the string mystring.
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
def GetString(prompt_msg, default, allowed_values, ignore_case=True):
    '''Get a string from a user and compare it to a sequence of
    allowed values.  If the response is in the allowed values, return
    it.  Otherwise, print an error message and ask again.  The letter
    'q' or 'Q' will let the user quit the program.  The returned
    string will have no leading or trailing whitespace.
    '''
    if ignore_case:
        allowed_values = [i.lower() for i in allowed_values]
    while True:
        msg = prompt_msg + " [" + default + "]:  "
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
    '''name is a string and names is a set or dict of strings.  Find
    if name uniquely identifies a string in names; if so, return it.
    If it isn't unique, return a list of the matches.  Otherwise
    return None.  The objective is to allow name to be the minimum
    length string necessary to uniquely identify the choice.
    '''
    # See self tests below for an example of use
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(names, (set, dict)):
        raise ValueError("names must be a set or dictionary")
    d, n = defaultdict(list), len(name)
    for i in names:
        d[i[:len(name)]] += [i]
    if name in d:
        if len(d[name]) == 1:
            return d[name][0]
        else:
            return d[name]
    return None
def KeepOnlyLetters(s, underscore=False, digits=True):
    '''Replace all non-word characters with spaces.  If underscore is
    True, keep underscores too (e.g., typical for programming language
    identifiers).  If digits is True, keep digits too.
    '''
    allowed = string.ascii_letters + "_" if underscore else string.ascii_letters
    allowed += string.digits if digits is True else ""
    c = [chr(i) for i in range(256)]
    t = ''.join([i if i in allowed else " " for i in c])
    return s.translate(t)
def StringSplit(fields, string, remainder=True, strict=True):
    '''Pick out the specified fields of the string and return them as
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
        columns (numbering is 0-based).  Example:  for the input string
        "hello there", using the fields of [3, 7] will return the tuple
        of strings ("hel", "lo t", "here").
            "hello there"
             01234567890
 
    Derived from code by Alex Martelli at
    http://code.activestate.com/recipes/65224-accessing-substrings/
    Downloaded Sun 27 Jul 2014 07:52:44 AM
    '''
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
            pieces.append(string[fields[-1]:])
        num_expected = len(fields) + 1
        if num_expected != len(pieces) and strict:
            raise ValueError("Expected %d pieces; got %d" % (num_expected,
                             len(pieces)))
        return pieces
def ListInColumns(alist, col_width=0, num_columns=0, space_betw=0, truncate=0):
    '''Returns a list of strings with the elements of alist (if
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
 
    Caveat:  if there are a small number of elements in the list, you
    may not get what you expect.  For example, try a list size of 1 to
    10 with num_columns equal to 4:  for lists of 1, 2, 3, 5, 6, and 9,
    you'll get fewer than four columns.
 
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
            num_columns = int(columns//maxlen)
        except Exception:
            return [""]
        if num_columns < 1:
            raise ValueError("A line is too long to display")
        space_betw = 1
    if not col_width or not num_columns or space_betw < 0:
        raise ValueError("Error: invalid parameters")
    num_rows = int(N//num_columns + (N % num_columns != 0))
    for row in range(num_rows):
        s = ""
        for column in range(num_columns):
            i = int(num_rows*column + row)
            if 0 <= i <= (N-1):
                if len(str(alist[i])) > col_width:
                    if truncate:
                        s += str(alist[i])[:col_width] + " "*space_betw
                    else:
                        raise ValueError("Error:  element %d too long" % i)
                else:
                    s += (str(alist[i]) + " " * (col_width -
                          len(str(alist[i]))) + " " * space_betw)
        lines.append(s)
    assert(len(lines) == num_rows)
    return lines
def MultipleReplace(text, patterns, flags=0):
    '''Replace multiple patterns in the string text.  patterns is a
    dictionary whose keys are the regular expressions and values are the
    replacement text.  The flags keyword variable is the same as that used
    by the re.compile function.
    
    From page 88 of Python Cookbook.
    '''
    # Make a compound regular expression from all the keys
    r = re.compile("|".join(map(re.escape, patterns.keys())), flags)
    # For each match, look up the corresponding value in the dictionary
    return r.sub(lambda match: patterns[match.group(0)], text)
def RemoveComment(line, code=False):
    '''Remove the largest string starting with '#' from the string
    line.  If code is True, then the resulting line will be compiled
    and an exception will occur if the modified line won't compile.
    This typically happens if '#' is inside of a comment.
    '''
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
    '''input is a sequence of word strings; Words is a dictionary or set
    of correct spellings.  Return the set of any words in input that are not
    in Words.
    '''
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
    ''' Splits s on all of the three newline sequences: "\r\n", "\r", or
    "\n".  Returns a list of the strings.
 
    Copyright (c) 2002-2009 Zooko Wilcox-O'Hearn, who put it under the GPL.
    '''
    cr, nl = "\r", "\n"
    res = []
    for x in s.split(cr + nl):
        for y in x.split(cr):
            res.extend(y.split(nl))
    return res
def WordID(half_length=3, unique=None, num_tries=100):
    '''Return an ID string that is (somewhat) pronounceable.  The
    returned number of characters will be twice the half_length.  If
    unique is not None, it must be a container that can be used to
    determine if the ID is unique.  You are responsible for adding the
    returned word to the container.
 
    The method is to choose a consonant from 'bdfghklmnprstvw' and append a
    vowel; do this half_length number of times.
 
    Interestingly, the words often look like they come from Japanese or
    Hawaiian.
    '''
    # Derived from http://code.activestate.com/recipes/576858
    # downloaded Tue 12 Aug 2014 12:38:54 PM.  Original recipe by
    # Robin Parmar on 8 Aug 2007 under PSF license.
    v, c, r, count = 'aeiou', 'bdfghklmnprstvw', range(half_length), 0
    while count < num_tries:
        word = ''.join([choice(c) + choice(v) for i in r])
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
class NameConvert:
    'Convert programming naming styles, "Python Cookbook" pg. 91'
    def cw2us(self, x):
        '''Cap-words to underscore:
            ALotOfFuss --> a_lot_of_fuss
        '''
        if not x:   
            return x
        return re.sub(r"(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])",
                    r"_\g<0>", x).lower()
    def cw2mc(self, x):
        '''Cap-words to mixed-case:
            ALotOfFuss --> aLotOfFuss
        '''
        if not x:   
            return x
        return x[0].lower() + x[1:]
    def us2mc(self, x):
        '''Underscore to mixed-case:
            a_lot_of_fuss --> aLotOfFuss
        '''
        if not x:   
            return x
        return re.sub(r"_([a-z])", lambda m: (m.group(1).upper()), x)
    def us2cw(self, x):
        '''Underscore to cap-words:
            a_lot_of_fuss --> ALotOfFuss
        '''
        if not x:   
            return x
        s = self.us2mc(x)
        return s[0].upper() + s[1:]
    def mc2us(self, x):
        '''Mixed-case to underscore:
            aLotOfFuss --> a_lot_of_fuss
        '''
        if not x:   
            return x
        return self.cw2us(x)
    def mc2cw(self, x):
        '''Mixed-case to cap-words:
            aLotOfFuss --> ALotOfFuss
        '''
        if not x:   
            return x
        return x[0].upper() + x[1:]
if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    import math
    import os
    from sig import sig
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
    def Test_soundex():
        test_cases = (
            ("Euler",       "E460"),
            ("Gauss",       "G200"),
            ("Hilbert",     "H416"),
            ("Knuth",       "K530"),
            ("Lloyd",       "L300"),
            ("Lukasiewicz", "L222"),
            ("chute",       "C300"),
            ("shoot",       "S300"),
            ("a",           "A000"),
            ("A",           "A000"),
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
    def TestCommonPrefix():
        Assert(not CommonPrefix(["a", "b"]))
        Assert("a" == CommonPrefix(["aone", "atwo", "athree"]))
        Assert("abc" == CommonPrefix(["abc", "abc", "abc"]))
        raises(TypeError, CommonPrefix, ["a", 1])
    def TestCommonSuffix():
        Assert(not CommonSuffix(["a", "b"]))
        Assert("a" == CommonSuffix(["onea", "twoa", "threea"]))
        Assert("abc" == CommonSuffix(["abc", "abc", "abc"]))
        raises(TypeError, CommonSuffix, ["a", 1])
    def TestKeep():
        Assert(Keep("abc", "bc") == "bc")
        A, B = "a b c".split(), "b c".split()
        Assert(Keep(A, B) == B)
    def TestKeepFilter():
        f = KeepFilter("bc")
        Assert(f("abc") == "bc")
    def TestRemove():
        Assert(Remove("abc", "cb") == "a")
    def TestRemoveFilter():
        f = RemoveFilter("bc")
        Assert(f("abc") == "a")
    def Test_FilterStr():
        s = '''"Not that easy, I'm sure."'''
        f = FilterStr('''"',.''', [None]*4)
        t = f(s)
        Assert(t == "Not that easy Im sure")
    def TestFindDiff():
        s1 = u"hello"
        s2 = u"hello there"
        Assert(FindDiff(s1, s2) == -1)
        s1 = u"hellx"
        Assert(FindDiff(s1, s2) == 4)
        s1 = u""
        Assert(FindDiff(s1, s2, ignore_empty=True) == 0)
    def TestFindSubstring():
        #    01234567890
        s = "x  x    x  "
        Assert(FindSubstring(s, "x") == (0, 3, 8))
    def TestGetChoice():
        names = set(("one", "two", "three", "thrifty"))
        Assert(GetChoice("o", names) == "one")
        Assert(set(GetChoice("th", names)) == set(["three", "thrifty"]))
        Assert(GetChoice("z", names) == None)
    def TestKeepOnlyLetters():
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
    def TestStringSplit():
        s = "hello there"
        Assert(StringSplit([4, 7], s) == ['hell', 'o t', 'here'])
        t = "3s 3x 4s"
        f = lambda x: bytes(x, encoding="ascii")
        q = [f('hel'), f('ther'), f('e')]
        Assert(StringSplit(t, s, remainder=True) == q)
        Assert(StringSplit(t, s, remainder=False) == q[:-1])
    def TestListInColumns():
        s = [sig(math.sin(i/20), 3) for i in range(20)]
        got = "\n".join(ListInColumns(s))
        ts = "  "   # Note there are two spaces after these rows...
        exp = "0.00   0.0998 0.199  0.296  0.389  0.479  0.565  0.644  0.717  0.783"
        exp += ts
        exp += "\n"
        exp += "0.0500 0.149  0.247  0.343  0.435  0.523  0.605  0.682  0.751  0.813"
        exp += ts
        Assert(got == exp)
    def TestNamingConventionConversions():
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
        Assert(result == 'x        x x        x')
    def TestRemoveComment():
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
    def TestSpellCheck():
        input_list = ("dog", "cAt", "hurse")
        word_dictionary = {"dog":"", "cat":"", "horse":"", "chicken":""}
        s = SpellCheck(input_list, word_dictionary, ignore_case=True)
        Assert(len(s) == 1 and "hurse" in s)
        s = SpellCheck(input_list, word_dictionary, ignore_case=False)
        Assert(len(s) == 2 and "cAt" in s and "hurse" in s)
    def TestSplitOnNewlines():
        Assert(SplitOnNewlines("1\n2\r\n3\r") == ["1", "2", "3", ""])
    exit(run(globals(), regexp="^Test", halt=1)[0])

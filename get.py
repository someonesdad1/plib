'''
Module for getting data from files, strings, and streams.

TODO:  
    * Add Zn to GetNumbers
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Module for getting data from files, strings, and
    # streams.  An example is reading a text file, getting all the lines
    # except for those that match a sequency of regular expressions.
    # Other examples are getting all the words (tokens) from a file or a
    # set of numbers.  # Handles a number of common programming tasks.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import locale
    import pathlib
    import re
    from collections import defaultdict
    from collections.abc import Iterable
    from io import StringIO
    from fractions import Fraction
    from pdb import set_trace as xx
if 1:   # Custom imports
    from asciify import Asciify
    try:
        from uncertainties import ufloat, ufloat_fromstr
        _have_unc = True
    except ImportError:
        _have_unc = False
    try:
        from f import flt, cpx
        _have_f = True
    except ImportError:
        _have_f = False
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
def GetText(thing, enc=None):
    '''Return the text from thing, which can be a string, bytes,
    or stream.  If thing is a string, it's assumed to be a file name;
    if trying to read the file generates an exception, the string itself
    is used as the text.
    
    If enc is not None, then it is an encoding to decode the data and
    if thing is a str, the file will be read as binary.
    '''
    if ii(thing, bytes):
        # Bytes
        s = thing.decode(encoding="UTF-8" if enc is None else enc)
    elif ii(thing, (str, pathlib.Path)):
        # File name
        p = pathlib.Path(thing)
        try:
            s = p.read_text(encoding=enc) if enc else p.read_text()
        except FileNotFoundError:
            s = thing
    elif hasattr(thing, "read"):
        # Stream
        s = thing.read()
    else:
        raise TypeError("Type of 'thing' not recognized")
    return s
def GetLines(thing, enc=None, regex=None):
    '''Return a list of lines that are in thing.  See GetText for
    details on thing.
 
    regex:  must be None or a sequence of strings that are regular
    expressions.  Any line that matches any of the regular expressions
    is ignored.
 
    Example:
        s = """# Comment
        ## Another comment
        Line 1
            Line 2
        """
        r = ["^ *#"]
        lines = GetLines(s, regex=r)
        print(f"lines {list(lines)}")
    outputs 
        lines ['Line 1', '    Line 2', '']
    '''
    def Filter(line):
        if regex is not None:
            for r in regex:
                if re.search(r, line):
                    return False     # Don't keep this line
        return True     # Keep this line
    if regex is not None and (ii(regex, str) or not ii(regex, Iterable)):
        raise TypeError("regex must be an iterable")
    lines = GetText(thing, enc=enc).split("\n")
    lines = list(filter(Filter, lines))
    return lines
def GetLine(thing, enc=None):
    '''Similar to GetLines, but is a generator so it gets a line at a time.
    thing can be a string, bytes, or a stream.  If it is a string, it's
    assumed to be a file name; if trying to read the file generates an
    exception, the string itself is used as the text.
 
    If it is a bytes object, then the indicated encoding is used to
    decode it, then it's read a line at a time.
    '''
    if ii(thing, bytes): # Bytes
        s = thing.decode(encoding="UTF-8" if enc is None else enc)
        stream = StringIO(s)
    elif ii(thing, (str, pathlib.Path)): # File name
        p = pathlib.Path(thing)
        try:
            stream = open(p)
        except Exception:
            stream = StringIO(thing)
    elif hasattr(thing, "read"): # Stream
        stream = thing
    else:
        raise TypeError("Type of 'thing' not recognized")
    line = stream.readline()
    while line:
        yield line
        line = stream.readline()
def GetNumberedLines(thing, enc=None):
    '''Return a tuple of (linenum, line_string) tuples where linenum is
    the line number in the file.  See GetText for details on the enc
    argument.
    '''
    lines = GetText(thing, enc=enc).split("\n")
    return tuple((i + 1, j) for i, j in enumerate(lines))
def GetWords(thing, sep=None, enc=None, regex=None):
    '''Return a list of words separated by the string sep from the thing
    (see details for GetLines).  If sep is None, then the data are split
    on whitespace; otherwise, the newlines are replaced by sep, then the
    data are split on sep.  
    '''
    lines = GetLines(thing, regex=regex)
    if sep is not None:
        s = sep.join(lines)
        return sep.join(lines).split(sep)
    else:
        return ' '.join(lines).split()
def GetTokens(thing, sep=None, enc=None, regex=None):
    '''Similar to GetWords(), but this is a generator so that arbitrarily 
    large files can be processed.
    '''
    for line in GetLine(thing, enc=enc):
        if sep is None:
            for token in line.split():
                yield token
        else:
            for token in line.split(sep):
                yield token
def GetBinary(thing, encoded=False):
    '''Read in thing as binary (thing is a stream or filename).  Bytes
    will be returned.
    
    If encoded is True, then try to decode it by using a number of 
    encodings.  A string will be returned if it can be decoded.
    '''
    # See ConstructEncodingData in /pylib/enc.py, as it gives the
    # frequency of these encodings found on web pages.
    encodings = '''
        utf_8 latin_1 cp1251 cp1252 shift_jis gb2312 euc_kr euc_jp
        iso8859_2 gbk cp1250 big5 iso8859_9 iso8859_15
    '''.split()
    if encoded:
        try:
            s = thing.read()
        except AttributeError:
            s = open(thing, "rb").read()
        if ii(s, str):
            return s
        # Got bytes; try to decode them
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                pass
        raise ValueError("'thing' could not be decoded")
    else:
        try:
            return thing.read()
        except AttributeError:
            return open(thing, "rb").read()
def GetNumbers(thing, numtype=None,  enc=None):
    '''Uses GetText() to get a string, then recognizes integers, floats,
    fractions, complex, and uncertain numbers in the string separated by
    whitespace and returns a list of these numbers.  If numtype is
    given, all found strings are converted to that type.
 
    If flt and cpx types are available (_have_f is True), then floats
    and complex types are converted to these over float and complex, 
    respectively.
 
    If the uncertainties library is present, the ufloat type can be
    recognized.
    '''
    lst, dp = [], locale.localeconv()["decimal_point"]
    for s in GetText(thing, enc=enc).split():
        if numtype:
            lst.append(numtype(s))
        else:
            if _have_unc and "+-" in s:
                s = s.replace("+-", "+/-")
            if _have_unc and ("+/-" in s or "(" in s or "±" in s):
                x = ufloat_fromstr(s)
            elif "/" in s:
                x = Fraction(s)
            elif "j" in s.lower():
                x = cpx(s) if _have_f else complex(s)
            elif dp in s or "e" in s.lower():
                x = flt(s) if _have_f else float(s)
            else:
                x = int(s)
            lst.append(x)
    return lst
if __name__ == "__main__": 
    import os
    from wrap import dedent
    from lwtest import run, raises, Assert
    from io import StringIO
    if _have_f:
        from get import flt, cpx
    text_file, S = None, None
    def SetUp():
        global text_file, S
        text_file = P("get.test")
        S = "Some\ntext\n"
        text_file.write_text(S)
    def TearDown():
        if text_file.exists():
            text_file.unlink()
    def TestGetText():
        sio = StringIO(S)
        t = GetText(sio)
        Assert(t == S)
        t = GetText(S)
        Assert(t == S)
        t = GetText(text_file)
        Assert(t == S)
        # Test with bytes
        b = b"Some\ntext\n"
        t = GetText(b)
        Assert(t == S)
        t = GetText(b, enc="ISO-8859-1")
        Assert(t == S)
        t = GetText(b"\xb5", enc="ISO-8859-1")
        Assert(t == "µ")
        # Test with regexp
        s = dedent('''
        # Comment
        ## Another comment
    Line 1
        Line 2''')
        r = ("^ *#",)
        lines = GetLines(s, regex=r)
        Assert(lines == ['Line 1', '    Line 2'])
    def TestGetLine():
        # Test with stream
        sio = StringIO(S)
        lines = ["Some\n", "text\n"]
        for i, line in enumerate(GetLine(sio)):
            Assert(line == lines[i])
        # Test with string
        for i, line in enumerate(GetLine(S)):
            Assert(line == lines[i])
        # Test with file
        for i, line in enumerate(GetLine(text_file)):
            Assert(line == lines[i])
    def TestGetLines():
        # Test with stream
        sio = StringIO(S)
        l = S.split() + [""]
        t = GetLines(sio)
        Assert(t == l)
        # Test with string
        t = GetLines(S)
        Assert(t == l)
        # Test with file
        t = GetLines(text_file)
        Assert(t == l)
    def TestGetWords():
        sio = StringIO(S)
        l = S.split()
        t = GetWords(sio)
        Assert(t == l)
        t = GetWords(S)
        Assert(t == l)
        t = GetWords(text_file)
        Assert(t == l)
    def TestGetTokens():
        s = "1 2 3\n4 5 6\n"
        l = list(GetTokens(s))
        Assert(l == "1 2 3 4 5 6".split())
    def TestGetBinary():
        enc = "iso-8859-1"
        open(text_file, "wb").write(S.encode(enc))
        t = GetBinary(text_file)
        Assert(t == S.encode("ascii"))
    def TestGetNumberedLines():
        expected = ((1, "Some"), (2, "text"), (3, ""))
        sio = StringIO(S)
        t = GetNumberedLines(sio)
        Assert(t == expected)
        t = GetNumberedLines(S)
        Assert(t == expected)
        t = GetNumberedLines(text_file)
        Assert(t == expected)
    def TestGetNumbers():
        # Check general python numerical types
        s = "1 1.2 3/4 3+1j"
        l = GetNumbers(s)
        Assert(l == [1, 1.2, Fraction(3, 4), (3+1j)])
        # Check f.py types flt and cpx
        if _have_f:
            s = "1.2 3+1j"
            x, z = GetNumbers(s)
            Assert(ii(x, flt) and ii(z, cpx))
            Assert(x == flt(1.2))
            Assert(z == cpx(3+1j))
        # Check uncertainties library forms
        if _have_unc:
            s = "3±4 3+-4 3+/-4 3(4)"
            for u in GetNumbers(s):
                Assert(u.nominal_value == 3)
                Assert(u.std_dev == 4)
        # Test with a float type
        s = "1 1.2"
        l = GetNumbers(s, numtype=float)
        Assert(l == [1.0, 1.2])
        Assert(all([ii(i, float) for i in l]))
        l = GetNumbers(s, numtype=flt)
        Assert(l == [flt(1.0), flt(1.2)])
        Assert(all([ii(i, flt) for i in l]))
        # Test with a complex type
        s = "1 1.2 3+4j"
        l = GetNumbers(s, numtype=complex)
        Assert(l == [1+0j, 1.2+0j, 3+4j])
        l = GetNumbers(s, numtype=cpx)
        Assert(all([ii(i, cpx) for i in l]))
        Assert(l == [cpx(1+0j), cpx(1.2+0j), cpx(3+4j)])
        # Test Fraction
        s = "3/8 7/16 1/2"
        l = GetNumbers(s)
        Assert(all([ii(i, Fraction) for i in l]))
        Assert(l == [Fraction(3, 8), Fraction(7, 16), Fraction(1, 2)])
    SetUp()
    status = run(globals(), halt=True)[0]
    TearDown()
    exit(status)

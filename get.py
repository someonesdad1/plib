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
    import sys
    from collections import defaultdict
    from collections.abc import Iterable
    from io import StringIO
    from fractions import Fraction
    from pdb import set_trace as xx
if 1:   # Custom imports
    import u
    from asciify import Asciify
    try:
        from uncertainties import ufloat, ufloat_fromstr, UFloat
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
def GetTokens(*things, sep=None, enc=None):
    '''Similar to GetWords(), but this is a generator so that arbitrarily 
    large sets of files or streams can be processed.
    '''
    for thing in things:
        for line in GetLine(thing, enc=enc):
            for token in line.split() if sep is None else line.split(sep):
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
def Choice(seq, default=1, indent=None, col=False):
    '''Display the choices in seq with numbers and prompt the user for his
    choice.  Note the numbers are 1-based as displayed to the user, but the
    returned value of choice will be 0-based.  Return the choice_number.
 
    indent is a string to prepend to each line if not None.  If col is
    True, use Columnize to print the choices (allows more dense listings
    for a given screen space).
 
    '''
    if not seq:
        raise ValueError("seq can't be empty")
    items, n = [], len(seq)
    for i, item in enumerate(seq):
        items.append("{}) {}".format(i + 1, str(item)))
    if col:
        for i in Columnize(items, indent=indent, sep=" "*3):
            print(i)
    else:
        s = "" if indent is None else indent
        for i in items:
            print(s, i, sep="")
    choice = GetNumber("Choice? ", numtype=int, default=default, 
                       low=1, high=n) - 1
    return (choice, seq[choice])
def GetNumber(prompt_msg, **kw):
    '''General-purpose routine to get a number (integer, float [default],
    or UFloat types) from the user with the prompt msg:
 
        num_float = GetNumber(prompt_msg)
        num_int   = GetNumber(prompt_msg, numtype=int)
 
    If use_unit is False, the returned value is the indicated number type
    (float is default).  If use_unit is True, (value, unit) is returned
    where value is the indicated number type and unit is a string
    representing the physical unit.
 
    The user can utilize python expressions in the input; the math library's
    functions are in scope.
 
    If you wish to restrict the allowed values of the number, use the
    following keyword arguments (default values are in square brackets):
 
        numtype     Number type [float].  Use int if you want the
                    number to be an integer.  You can use a number type as
                    long as it obeys the required ordering semantics and
                    the constructor returns a number object that raises a
                    ValueError if the initializing string is of improper
                    form.  For an example, see the use of mpmath's mpf
                    numbers in the unit tests.
 
        default     Default value.  This value will be returned if
                    the user just presses the return key when prompted.
 
        low         Lowest allowed value.  [None]
 
        high        Highest allowed value.  [None]
 
        low_open    Boolean; if True, then the low end of the acceptance
                    interval is open.  [False]
 
        high_open   Boolean; if True, then the high end of the acceptance
                    interval is open.  [False]
 
        invert      If true, the value must be in the complement interval.
                    This is used to allow numbers except those in a
                    particular range.  See note below.
 
        outstream   Stream to print messages to.  [stdout]
 
        instream    Stream to get input from (intended for unit tests).
 
        prefix      Prefix string for error messages
                        ["Error:  must have "]
 
        use_unc     If true, lets you use number strings that can be
                    interpreted by the python uncertainties library.
                    If use_unit is true, then all units must be
                    separated from the uncertain number string by one or
                    more spaces (i.e., no cuddled units).  Note:  if you
                    use a number string like '9 m' and use_unc is True,
                    then the returned number will be 9+/-1, which is the
                    default interpretive behavior of the uncertainties
                    library's ufloat_fromstr() function.  The following
                    strings mean the same number and uncertainty:
                    "4.2+/-0.4", "4.2+-0.4", "4.2(4)".  [False]
 
        use_unit    If true, allows a unit to be included in the string.
                    The return value will be a tuple of (number,
                    unit_string).  [False]
 
        allow_quit  If true, "Q" or "q" quits the program.  [True]
 
        inspect     If not None, it's a string that should be
                    inspected to see if it meets the requirements.  If
                    it does, True will be returned; otherwise, False
                    is returned.
 
        vars        Dictionary to use as locals to evaluate expressions.
 
    For programming ease, any errors in the keyword values will cause a
    SyntaxError exception.  Other exceptions are probably caused by my
    programming mistakes.
 
    Note:  if you call
 
        GetNumber("", low=a, high=b)
 
    the number returned will be the number in the closed interval [a, b].
    If you make the same call but with invert set to True
 
        GetNumber("", low=a, high=b, invert=True)
 
    then the returned number must lie in the union of the open intervals
    (-inf, a) and (b, inf); this set of numbers is the complement of the
    previous call's.  If you make the call
 
        GetNumber("", low=a, high=b, low_open=True, high_open=True)
 
    the number returned will be in the open interval (a, b).  If this is
    inverted by setting invert to True as in
 
        GetNumber("", low=a, high=b, low_open=True,
                  high_open=True, invert=True)
 
    then you'll get a number returned in the union of the half-closed
    intervals (-inf, a] and [b, inf).  A programmer might be confused
    by the fact that the intervals were half-closed, even though the
    settings low_open and high_open were used, implying the programmer
    wanted open intervals.  The way to look at this is to realize that
    if invert is True, it changes an open half-interval to a closed
    half-interval.  I chose to make the function behave this way
    because it's technically correct.  However, if this behavior is
    not to your liking, it's easy to change by changing the
    conditional statements in the conditionals dictionary.  (I debated
    as to whether I should make this function an object instead; then
    this could be done by subclassing rather than changing the
    function.  But the convenience of a simple function won out.)
    '''
    outstream  = kw.get("outstream", sys.stdout)
    instream   = kw.get("instream", None)
    numtype    = kw.get("numtype", float)
    default    = kw.get("default", None)
    low        = kw.get("low", None)
    high       = kw.get("high", None)
    low_open   = kw.get("low_open", False)
    high_open  = kw.get("high_open", False)
    inspect    = kw.get("inspect", None)
    invert     = kw.get("invert", False)
    prefix     = kw.get("prefix", "Error:  must have ")
    use_unc    = kw.get("use_unc", False)
    use_unit   = kw.get("use_unit", False)
    allow_quit = kw.get("allow_quit", True)
    vars       = kw.get("vars", {})
    Debug      = kw.get("Debug", None)
    # If the variable Debug is defined and True, then we
    # automatically return the default value.
    if Debug:
        return default
    if (low is not None) and (high is not None):
        if low > high:
            raise ValueError("low must be <= high")
        if default is not None and not (low <= numtype(default) <= high):
            raise ValueError("default must be between low and high")
    if invert and low is None and high is None:
        raise ValueError("low and high must be defined to use invert")
    if inspect is not None and not isinstance(inspect, str):
        raise ValueError("inspect must be a string")
    out = outstream.write
    # The following dictionary is used to get conditionals for testing the
    # values entered by the user.  If a set of keywords is not in this
    # dictionary's keys, then it is considered a syntax error by the
    # programmer making a call to this function.  This dictionary is used
    # to both check the conditions as well as provide an error message back
    # to the user.
    conditionals = {
        # low     high   low_open  high_open  invert
        (True,  False, False,    False,     False): "x >= low",
        (True,  False, True,     False,     False): "x > low",
        (True,  False, False,    False,     True):  "x < low",
        (True,  False, True,     False,     True):  "x <= low",
        (False, True,  False,    False,     False): "x <= high",
        (False, True,  False,    True,      False): "x < high",
        (False, True,  False,    False,     True):  "x > high",
        (False, True,  False,    True,      True):  "x >= high",
        (True,  True,  False,    False,     False): "low <= x <= high",
        (True,  True,  True,     False,     False): "low < x <= high",
        (True,  True,  False,    True,      False): "low <= x < high",
        (True,  True,  True,     True,      False): "low < x < high",
        (True,  True,  False,    False,     True):  "x < low or x > high",
        (True,  True,  True,     False,     True):  "x <= low or x > high",
        (True,  True,  False,    True,      True):  "x < low or x >= high",
        (True,  True,  True,     True,      True):  "x <= low or x >= high",
    }
    unit_string = ""
    while True:
        if inspect is None:
            out(prompt_msg)
            if default is not None:
                out("[" + str(default) + "] ")
            if instream is not None:
                s = instream.readline()
                if not s:
                    if default is None:
                        # This should only be seen during testing.
                        raise RuntimeError("Empty input!")
                    else:
                        if use_unit:
                            return (numtype(default), "")
                        else:
                            return numtype(default)
            else:
                s = input().strip()
        else:
            s = inspect
        if not s:
            if default is None:
                raise ValueError("Default value not defined")
            else:
                if inspect is not None:
                    return True
                if use_unit:
                    return (numtype(default), "")
                else:
                    return numtype(default)
        if len(s) == 1 and s in "qQ" and allow_quit:
            exit(0)
        if use_unc and "+-" in s:  # Change 8+-1 to 8+/-1
            if not _have_unc:
                raise ValueError("Uncertainties library not available")
            s = s.replace("+-", "+/-")
        # Check to see if number contains a unit
        if use_unit:
            number_string, unit_string = u.ParseUnit(s, allow_unc=use_unc)
            s = number_string
        try:
            if use_unc:
                if ii(s, str):
                    x = ufloat_fromstr(s)
                else:
                    x = s   # It's already a uncertainties.core.Variable
            else:
                # Note the use of eval lets the user type expressions in.
                # The math module's symbols are in scope.
                x = numtype(eval(s, globals(), vars))
        except ValueError:
            if inspect is not None:
                return False
            if numtype == int:
                out("'%s' is not a valid integer\n" % s)
            else:
                out("'%s' is not a valid number\n" % s)
        else:
            if low is None and high is None:
                if inspect is not None:
                    return True
                if use_unit:
                    return (x, unit_string)
                else:
                    return x
            # Check if this number meets the specified conditions; if it
            # does, return it.  Otherwise, print an error message on the
            # output stream and re-prompt the user.
            c = (low is not None, high is not None, low_open, 
                 high_open, invert)
            if c not in conditionals:
                # Programmer mistake
                raise ValueError('''Bad set of parameters to GetNumber:
    low       = {low}
    high      = {high}
    low_open  = {low_open}
    high_open = {high_open}
    invert    = {invert}
  
    For example, low and high must not be None.'''.format(**locals()))
            condition = conditionals[c]
            if not eval(condition):
                if inspect is not None:
                    return False
                # Test failed, so send error message to user
                condition = condition.replace("x", "number")
                condition = prefix + condition
                condition = condition.replace("high", "{high}")
                condition = condition.replace("low", "{low}")
                out(condition.format(**locals()) + "\n")
                # If instream is defined, we're testing, so just return.
                if instream is not None:
                    return
                continue
            # Got a good number, so return it
            if inspect is not None:
                return True
            if use_unit:
                return (x, unit_string)
            else:
                return x
def GetFraction(s):
    '''Return a Fraction object if string s contains a '/' and can be interpreted
    as an improper or proper fraction; otherwise return None.  The following 
    forms are allowed:
        A   5/4     +5/4    -5/4
        B   1 1/4   +1 1/4  -1 1/4
        C   1-1/4   +1-1/4  -1-1/4
        D   1+1/4   +1+1/4  -1+1/4
    '''
    if "/" not in s:
        return None
    s = s.strip()
    try:
        neg = 1
        if s[0] == "+":
            s = s[1:]
        elif s[0] == "-":
            s = s[1:]
            neg = -neg
        s = s.replace("+", " ").replace("-", " ")
        ip = 0
        if " " in s:
            ip, s = s.split()
            ip = int(ip)
        n, d = s.split("/")
        return neg*(ip + Fraction(int(n), int(d)))
    except Exception:
        return None
if __name__ == "__main__": 
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
        Assert(lines == ['Line 1', '  Line 2'])
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
    def sio(*s):
        'Allows StringIO to be used for input or output'
        if not s:
            return StringIO()
        return StringIO(s[0])
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
    def TestGetNumberExceptionalCases():
        # low > high
        raises(ValueError, GetNumber, "", low=1, high=0, instream=sio("0"))
        # Invert True without low or high
        raises(ValueError, GetNumber, "", invert=True, instream=sio("0"))
    def TestGetNumberAll():
        msg = "Error:  must have "
        # Note:  the test case comment is a picture of the allowed interval;
        # '(' and ')' mean open, '[' and ']' mean closed.
        #
        # [----...
        s_out = sio()
        GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("4"))
        assert(s_out.getvalue() == msg + "number >= 5\n")
        s_out = sio()
        n = GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("5"))
        assert(n == 5 and isinstance(n, int))
        s_out = sio()  # Test we can get a float like this too
        GetNumber("", numtype=float, low=5, outstream=s_out, instream=sio("4"))
        assert(s_out.getvalue() == msg + "number >= 5\n")
        n = GetNumber("", numtype=float, low=5, outstream=sio(), instream=sio("5"))
        assert(n == 5 and isinstance(n, float))
        # The remaining tests will be done implicitly with floats
        # (----...
        s_out = sio()
        GetNumber("", low=5, low_open=True, outstream=s_out,
            instream=sio("4"))
        assert(s_out.getvalue() == msg + "number > 5\n")
        s_out = sio()
        n = GetNumber("", low=5, low_open=True, outstream=s_out,
                instream=sio("6"))
        assert(n == 6 and isinstance(n, float))
        # ...----]
        s_out = sio()
        GetNumber("", high=5, outstream=s_out, instream=sio("6"))
        assert(s_out.getvalue() == msg + "number <= 5\n")
        s_out = sio()
        n = GetNumber("", high=5, outstream=s_out, instream=sio("5"))
        assert(n == 5 and isinstance(n, float))
        # ...----)
        s_out = sio()
        GetNumber("", high=5, high_open=True, outstream=s_out,
            instream=sio("5"))
        assert(s_out.getvalue() == msg + "number < 5\n")
        s_out = sio()
        n = GetNumber("", high=5, high_open=True, outstream=s_out,
                instream=sio("4"))
        assert(n == 4 and isinstance(n, float))
        # [----]
        s_out = sio()
        GetNumber("", low=2, high=5, outstream=s_out, instream=sio("6"))
        assert(s_out.getvalue() == msg + "2 <= number <= 5\n")
        s_out = sio()
        GetNumber("", low=2, high=5, outstream=s_out, instream=sio("1"))
        assert(s_out.getvalue() == msg + "2 <= number <= 5\n")
        # Also test at boundaries because this is probably the most important
        # case.
        s_out = sio()
        n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("5"))
        assert(n == 5 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("2"))
        assert(n == 2 and isinstance(n, float))
        # [----)
        s_out = sio()
        GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
            instream=sio("5"))
        assert(s_out.getvalue() == msg + "2 <= number < 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
                instream=sio("4.999999999999"))
        assert(n == 4.999999999999)
        s_out = sio()
        GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
            instream=sio("1"))
        assert(s_out.getvalue() == msg + "2 <= number < 5\n")
        # (----]
        s_out = sio()
        GetNumber("", low=2, high=5, low_open=True, outstream=s_out,
            instream=sio("2"))
        assert(s_out.getvalue() == msg + "2 < number <= 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, outstream=s_out,
                instream=sio("2.0000000000001"))
        assert(n == 2.0000000000001)
        # (----)
        s_out = sio()
        GetNumber("", low=2, high=5, low_open=True, high_open=True,
            outstream=s_out, instream=sio("5"))
        assert(s_out.getvalue() == msg + "2 < number < 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, high_open=True,
                outstream=s_out, instream=sio("4.999999999999"))
        assert(n == 4.999999999999 )
        s_out = sio()
        GetNumber("", low=2, high=5, low_open=True, high_open=True,
            outstream=s_out, instream=sio("2"))
        assert(s_out.getvalue() == msg + "2 < number < 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, high_open=True,
                outstream=s_out, instream=sio("2.0000000000001"))
        assert(n == 2.0000000000001)
        # ...---[  ]---...
        s_out = sio()
        GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
            outstream=s_out, instream=sio("2.0000000000001"))
        assert(s_out.getvalue() == msg + "number <= 2 or number >= 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
            outstream=s_out, instream=sio("2"))
        assert(n == 2 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
            outstream=s_out, instream=sio("5"))
        assert(n == 5 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                outstream=s_out, instream=sio("1"))
        assert(n == 1 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                outstream=s_out, instream=sio("6"))
        assert(n == 6 and isinstance(n, float))
        # ...---[  )---...
        s_out = sio()
        GetNumber("", low=2, high=5, low_open=True, invert=True,
            outstream=s_out, instream=sio("5"))
        assert(s_out.getvalue() == msg + "number <= 2 or number > 5\n")
        s_out = sio()
        GetNumber("", low=2, high=5, low_open=True, invert=True,
            outstream=s_out, instream=sio("4"))
        assert(s_out.getvalue() == msg + "number <= 2 or number > 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, invert=True,
            outstream=s_out, instream=sio("2"))
        assert(n == 2 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, low_open=True, invert=True,
            outstream=s_out, instream=sio("1"))
        assert(n == 1 and isinstance(n, float))
        # ...---(  ]---...
        s_out = sio()
        GetNumber("", low=2, high=5, high_open=True, invert=True,
            outstream=s_out, instream=sio("2"))
        assert(s_out.getvalue() == msg + "number < 2 or number >= 5\n")
        s_out = sio()
        GetNumber("", low=2, high=5, high_open=True, invert=True,
            outstream=s_out, instream=sio("4"))
        assert(s_out.getvalue() == msg + "number < 2 or number >= 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, high_open=True, invert=True,
            outstream=s_out, instream=sio("1.999999"))
        assert(n == 1.999999 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, high_open=True, invert=True,
            outstream=s_out, instream=sio("5"))
        assert(n == 5 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, high_open=True, invert=True,
            outstream=s_out, instream=sio("6"))
        assert(n == 6 and isinstance(n, float))
        # ...---(  )---...
        s_out = sio()
        GetNumber("", low=2, high=5, invert=True, outstream=s_out,
            instream=sio("2"))
        assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
        s_out = sio()
        GetNumber("", low=2, high=5, invert=True, outstream=s_out,
            instream=sio("5"))
        assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
        s_out = sio()
        GetNumber("", low=2, high=5, invert=True, outstream=s_out,
            instream=sio("3"))
        assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
        s_out = sio()
        n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
            instream=sio("1"))
        assert(n == 1 and isinstance(n, float))
        s_out = sio()
        n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
            instream=sio("6"))
        assert(n == 6 and isinstance(n, float))
        # Show that we can evaluate things with a variables dictionary.
        from math import sin, pi
        v = {"sin":sin, "pi":pi}
        s_out = sio()
        n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
            instream=sio("sin(pi/6)"), vars=v)
        assert(n == sin(pi/6) and isinstance(n, float))
    def TestGetNumber_mpmath():
        # Import mpmath and use for testing if available.
        # Demonstrates that GetNumber works with ordered number types
        # other than int and float.
        try:
            import mpmath
        except ImportError:
            print("** mpmath not tested in getnumber_test.py", file=err)
        else:
            # [----
            n = GetNumber("", numtype=mpmath.mpf, low=2, outstream=sio(),
                    instream=sio("4"))
            assert(n == 4 and isinstance(n, mpmath.mpf))
    def TestGetNumberDefaultValue():
        # See that we get an exception when the default is not between low and
        # high.
        with raises(ValueError):
            GetNumber("", low=2, high=5, invert=True, outstream=sio(), default=1,
                instream=sio(""))
        # Test default value with int
        default = 2
        num = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                    numtype=int, default=default, instream=sio(""))
        assert(num == default)
        # Test default value with float
        default = 3.77
        num = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                    default=default, instream=sio(""))
        assert(num == default)
    def TestGetNumberNumberWithUnit():
        # Show that we can return numbers with units
        # 5 with no unit string
        n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5"),
            use_unit=True)
        assert(n == (5, "") and isinstance(n[0], float))
        # 5 meters, cuddled
        n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5m"),
            use_unit=True)
        assert(n == (5, "m") and isinstance(n[0], float))
        # 5 meters
        n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5 m"),
            use_unit=True)
        assert(n == (5, "m") and isinstance(n[0], float))
        # millimeters, cuddled
        n = GetNumber("", low=0, high=1e100, outstream=sio(),
            instream=sio("123.456e7mm"), use_unit=True)
        assert(n == (123.456e7, "mm") and isinstance(n[0], float))
        # millimeters
        n = GetNumber("", low=0, high=1e100, outstream=sio(),
            instream=sio("123.456e7   mm"), use_unit=True)
        assert(n == (123.456e7, "mm") and isinstance(n[0], float))
        # millimeters, negative number
        n = GetNumber("", low=-1e100, high=1e100, outstream=sio(),
            instream=sio("-123.456e7   mm"), use_unit=True)
        assert(n == (-123.456e7, "mm") and isinstance(n[0], float))
        #--------------------
        # Uncertainties
        #--------------------
        for t in ("8 mm", "8+-1 mm", "8+/-1 mm", "8(1) mm"):
            n = GetNumber("", low=-1e100, high=1e100, outstream=sio(),
                        instream=sio(t), use_unit=True, use_unc=True)
            assert(isinstance(n[0], UFloat))
            assert(n[0].nominal_value == 8)
            assert(n[0].std_dev == 1)
            assert(n[1] == "mm")
    def TestGetNumberInspect():
        # Test that 2 isn't in the first interval, but is in the second.
        assert(GetNumber("", low=0, high=1, inspect="2") == False)
        assert(GetNumber("", low=0, high=3, inspect="2") == True)
        # If inspect is not a string, get exception
        raises(ValueError, GetNumber, "", inspect=1)
    def TestGetFraction():
        e = Fraction(5, 4)
        for i in ("5/4", "+5/4", " -5/4", "1   1/4", "+1 1/4", "  -1 1/4",
            "1-1/4", "+1-1/4", "-1-1/4", "1+1/4", "+1+1/4", "-1+1/4"):
            i = i.strip()
            neg = -1 if i[0] == "-" else 1
            assert(GetFraction(i) == neg*e)
    SetUp()
    status = run(globals(), halt=True)[0]
    TearDown()
    exit(status)

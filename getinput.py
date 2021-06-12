'''
xx This functionality should be moved to get.py as needed and the
rest obsoleted.

Utility functions to get various types of input.  Should work with python
2.7 and 3.

GetLines()
    Get lines from text files and streams.  This is a generator, so
    arbitrarily large files can be processed.

GetAllLines()
    Same as GetLines(), but returns a list of all the lines.

GetTokens()
    Get tokens from text files and streams.  This is a generator, so
    arbitrarily large files can be processed.

TokenizeString()
    Get tokens from a multiline string.

GetNumber()
    Prompts the user for a number until an acceptable number is gotten.
    The number can contain an optional physical unit string if desired.

ParseUnit()
    Prompts user for a number and its physical unit.

GetWireDiameter()
    Prompts a user for a wire diameter; the user can use any common units
    or AWG sizes.

AWG()
    Return wire diameter in inches for an AWG (American Wire Gauge) 
    gauge number.
    
Choice()
    Prompts user for a choice amongst a sequence of items.

ToolzAdapter()
    Convenience function to return a list of functions if the toolz library
    is available.  See an example of use in TokenizeString().
'''

# Copyright (C) 2010, 2018 Don Peterson
# Contact:  gmail.com@someonesdad1
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

# Built-in modules
import re
import sys
from pdb import set_trace as xx 

# Other modules
from u import u, ParseUnit
from columnize import Columnize

# If the toolz module is available, the compose object (in functoolz)
# allows a sequence of univariate functions to be used to transform
# arguments: if the sequence of functions is [f, g, h], then the
# transformed object will be f(g(h(object))) (i.e., function composition).
# To get toolz, use 'pip install toolz'.
have_toolz = False
try:
    have_toolz = True
    from toolz import compose
except ImportError:
    pass

# Identity transformation function
identity = lambda x: x

# Numbers may also include an uncertainty specification if the python
# uncertainties library's facilities are available.  A string indicates
# a number with uncertainty if it includes either '+-' or '+/-'.
try:
    from uncertainties import ufloat_fromstr
    from uncertainties.umath import *
    have_unc = True
    # Regular expression to recognize uncertain number candidates
    unc_re = re.compile(r"(\+/-|\(\d+\))")
except ImportError:
    have_unc = False
    from math import *
    unc_re = None

__all__ = [
    "AWG",
    "Choice",
    "GetAllLines",
    "GetLines",
    "GetNumber",
    "GetTokens",
    "have_toolz",
    "GetWireDiameter",
    "ParseUnit",
    "ParseUnitString",
    "TokenizeString",
    "ToolzAdapter",
    ]

def AWG(n):
    '''Returns the wire diameter in inches given the AWG (American Wire
    Gauge) number (also known as the Brown and Sharpe gauge).  Use negative
    numbers as follows:  -1 for 00, -2 for 000, and -3 for 000.
    '''
    # Reference:  the units.dat file with version 1.80 of the GNU units
    # program gives the following statement:
    # 
    #     American Wire Gauge (AWG) or Brown & Sharpe Gauge appears to be
    #     the most important gauge. ASTM B-258 specifies that this gauge is
    #     based on geometric interpolation between gauge 0000, which is
    #     0.46 inches exactly, and gauge 36 which is 0.005 inches exactly.
    #     Therefore, the diameter in inches of a wire is given by the
    #     formula
    #             1|200 92^((36-g)/39).
    #     Note that 92^(1/39) is close to 2^(1/6), so diameter is
    #     approximately halved for every 6 gauges.  For the repeated zero
    #     values, use negative numbers in the formula.  The same document
    #     also specifies rounding rules which seem to be ignored by makers
    #     of tables.  Gauges up to 44 are to be specified with up to 4
    #     significant figures, but no closer than 0.0001 inch.  Gauges from
    #     44 to 56 are to be rounded to the nearest 0.00001 inch.
    # 
    # An equivalent formula is 0.32487/1.12294049**n where n is the
    # gauge number (works for n >= 0).
    if n < -3 or n > 56:
        raise ValueError("AWG argument out of range")
    diameter = 92.**((36 - n)/39)/200
    if n <= 44:
        return round(diameter, 4)
    return round(diameter, 5)

def Choice(seq, default=1, indent=None, col=False):
    '''Display the choices in seq with numbers and prompt the user for his
    choice.  Note the numbers are 1-based as displayed to the user, but the
    returned value of choice will be 0-based.  Return (choice_number,
    seq[choice_number]).  indent is a string to prepend to each line if not
    None.  If col is True, use Columnize to print the choices (allows more
    dense listings for a given screen space).
    '''
    items, n = [], len(seq)
    for i, item in enumerate(seq):
        items.append("{}) {}".format(i + 1, str(item)))
    if col:
        for i in Columnize(items, indent=indent, sep=" "*3):
            if not Choice.test:
                print(i)
    else:
        s = "" if indent is None else indent
        for i in items:
            if not Choice.test:
                print(s, i, sep="")
    if Choice.test:
        # We need to use the Choice.instream and Choice.outstream settings
        # with GetNumber.
        choice = GetNumber("Choice? ", numtype=int, default=default, 
                           low=1, high=n, instream=Choice.instream,
                           outstream=Choice.outstream) - 1
    else:
        choice = GetNumber("Choice? ", numtype=int, default=default, 
                           low=1, high=n) - 1
    return (choice, seq[choice])
Choice.test = False     # Used for self tests

def GetAllLines(*files, **kw):
    '''Returns a list of all the lines from the indicated input
    source(s).  *files can contain file names and stream objects.  
 
    Simple wrapper for GetLines, so uses the same keyword arguments.
    '''
    if not files:
        return []
    return list(GetLines(*files, **kw))

def GetLines(*files, **kw):
    '''Generator that returns a sequence of lines from the indicated input
    source(s).  *files can contain file names and stream objects.  
 
    Keywords [default value]:
        ignore      Univariate function that takes a line as an argument
                    and returns True if it should be ignored.  [do not
                    ignore]
        nonl        Boolean: if True, remove newline. [False]
        xfm         Univariate function that takes a line as an argument
                    and returns xfm(line).  [identity]
 
    If the toolz library is available, xfm can be a sequence of univariate
    functions.

    Convenience functions for the ignore keyword:
        GetLines.IgnoreComment returns True if line is a python comment.
        GetLines.IgnoreEmpty returns True if line only contains whitespace.
         
    Examples:
        Get the lines from the filenames on the command line without
        their newlines:
            GetLines(*sys.argv[1:], nonl=True)
 
        Same as previous, but include stdin too:
            GetLines(*[sys.argv[1:]] + [sys.stdin], nonl=True)
 
        Get the lines from the files 'file1.txt' and 'file2.txt', ignoring
        empty lines and convert them to all uppercase:
            GetLines(*["file1.txt", "file2.txt"], xfm=str.upper,
                     ignore=GetLines.IgnoreEmpty)
            
    '''
    if not files:
        return
    ignore = kw.setdefault("ignore", lambda x: False)
    xfm = ToolzAdapter(kw.setdefault("xfm", identity))
    nonl = kw.setdefault("nonl", False)
    NoNl = lambda line: line[:-1] if line[-1] == "\n" else line
    for file in files:
        if hasattr(file, "write"):      # It's a stream
            line = file.readline()
            while line:
                if not ignore(line):
                    line = NoNl(line) if nonl else line
                    yield xfm(line)
                line = file.readline()
        else:                           # It's a file
            for line in open(file):
                if not ignore(line):
                    line = NoNl(line) if nonl else line
                    yield xfm(line)
# Convenience functions
GetLines.IgnoreComment = lambda x: True if x.lstrip()[0] == "#" else False
GetLines.IgnoreEmpty = lambda x: True if not x.strip() else False

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
 
        GetNumber("", low=a, high=b, low_open=True, high_open=True), the
 
    number returned will be in the open interval (a, b).  If this is
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
            if not have_unc:
                raise ValueError("Uncertainties library not available")
            s = s.replace("+-", "+/-")
        # Check to see if number contains a unit
        if use_unit:
            number_string, unit_string = ParseUnit(s)
            s = number_string
        try:
            if use_unc:
                x = ufloat_fromstr(s)
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

def GetTokens(*files, **kw):
    '''Generator that returns a sequence of tokens gotten from the
    indicated input source(s).  files can be either file names or stream
    objects.
    
    Keywords [default value]:
        convert     Univariate function(s) to apply to each token.
                    [identity]
        sep         Split each line on this string.  [" "]
        fltr        Univariate function(s) to filter each input line.
                    [identity]
 
    The filtering functions convert and fltr can be a sequence of functions
    to apply if the toolz module is available.
    '''
    if not files:
        return
    remove_nl = lambda line: line[:-1] if line[-1] == "\n" else line
    # Keyword options
    convert = ToolzAdapter(kw.setdefault("convert", identity))
    fltr    = ToolzAdapter(kw.setdefault("fltr", identity))
    sep     = kw.setdefault("sep", " ")
    # Process each file/stream
    for line in GetLines(*files):
            line = fltr(line)
            tokens = remove_nl(line).split(sep)
            for token in tokens:
                yield convert(token)

def GetWireDiameter(default_unit="mm"):
    '''Returns (s, d) where d is a wire diameter in the indicated units and
    s is the string the user input.  The user is prompted for the value,
    which can use an optional length unit (must be separated from the value
    by one or more spaces) or ' ga' to denote AWG.  The number portion of
    the input can be a valid python expression.
    '''
    msg = "Enter wire diameter (use 'ga' suffix for AWG): "
    while True:
        if GetWireDiameter.input is not None:
            # This is a StringIO stream used for testing
            s = GetWireDiameter.input.readline()
        else:
            s = input(msg).strip()
        if s == "q":
            exit(0)
        # See if it's AWG
        if s.endswith("ga"):
            t = s[:-2].strip()
            try:
                dia_inches = AWG(int(t))
            except ValueError:
                print("'{}' is not a valid AWG number".format(t))
                continue
            return s, dia_inches*u("inches")/u(default_unit)
        else:
            x, unit = ParseUnit(s)
            try:
                value = float(eval(x))
            except Exception:
                print("Expression '{}' not valid".format(x))
                continue
            if value <= 0:
                print("The value must be > 0")
                continue
            if u.dim(unit) == u.dim("m"):
                return s, value*u(unit)/u(default_unit)
            elif not unit:
                return s, value
GetWireDiameter.input = None    # Used for self tests

def ParseUnit(s):
    '''Assume the string s has a unit and possible SI prefix appended
    to the end, such as '123Pa', '123 Pa', or '1.23e4 Pa'.  Remove the
    unit and prefix and return the tuple (num, unit).  Note that two
    methods are used.  First, if the string contains one or more space
    characters, the string is split on the space and the two parts are
    returned immediately; an exception is thrown if there are more
    than two portions.  The other method covers the case where the
    unit may be cuddled against the number.
    '''
    if " " in s:
        f = s.split()
        if len(f) != 2:
            raise ValueError("'%s' must have only two fields" % s)
        return f
    # The second method is done by reversing the string and looking for
    # unit characters until a character that must be in the number is
    # found.  Note this means that digit characters cannot be in the unit.
    unit, num, num_chars, done = [], [], set("1234567890."), False
    for i in reversed(s):
        if done:
            num.append(i)
            continue
        if i in num_chars:
            num.append(i)
            done = True
        else:
            unit.append(i)
    return (''.join(reversed(num)), (''.join(reversed(unit))).strip())

def ParseUnitString(x, allowed_units, strict=True):
    '''This routine will take a string x and return a tuple (prefix,
    unit) where prefix is a power of ten gotten from the SI prefix
    found in x and unit is one of the allowed_units strings.
    allowed_units must be an iterable container.  Note things are
    case-sensitive.  prefix will either be a float or an integer.
 
    The typical use case is where ParseUnit() has been used to
    separate a number and unit.  Then ParseUnitString() can be used to
    parse the returned unit string to get the SI prefix actual unit
    string.  Note parsing of composite units (such as m/s) must take
    place outside this function.
 
    If strict is True, then one of the strings in allowed_units must
    be anchored at the right end of x.  If strict is False, then the
    strings in allowed_units do not have to be present in x; in this
    case, (1, "") will be returned.
    '''
    # Define the allowed SI prefixes
    si = {"y":  -24, "z": -21, "a": -18, "f": -15, "p": -12, "n": -9,
          "u": -6, "m": -3, "c": -2, "d": -1, "": 0, "da": 1, "h": 2,
          "k":  3, "M":  6, "G":  9, "T": 12, "P": 15, "E": 18, "Z": 21,
          "Y": 24}
    s = x.strip()  # Remove any leading/trailing whitespace
    # See if s ends with one of the strings in allowed_units
    unit = ""
    for u in allowed_units:
        u = u.strip()
        # The following can be used if a unit _must_ be supplied.
        # However, it's convenient to allow for a default unit, which
        # is handled by the empty string for the unit.
        #if not u:
        #    raise ValueError("Bad unit (empty or all spaces)")
        if u and s.endswith(u):
            unit = u
            break
    if not unit:
        if strict:
            raise ValueError("'%s' did not contain an allowed unit" % x)
        else:
            return (1, "")
    else:
        # Get right index of unit string
        index = s.rfind(unit)
        if index == -1:
            raise Exception("Bug in ParseUnitString() routine")
        prefix = s[:index]
        if prefix not in si:
            raise ValueError("'%s' prefix not an SI prefix" % prefix)
        return (10**si[prefix], unit)

def TokenizeString(*strings, **kw):
    '''Generator to produce tokens from a group of string arguments.
 
    Keywords [default value]:
        linesep         (string) Separates lines ["\n"]
        sep             (string) Separates tokens [" "]
        line_filter     Function to filter line strings [identity]
        token_filter    Function to filter tokens [identity]
 
    The filtering functions line_filter and token_filter can be a sequence
    of functions to apply if the toolz module is available; otherwise they
    must be univariate functions accepting a string argument.
 
    Example:
        multiline_string = """
            one two
            three
        """
        for i in TokenizeString(multiline_string):
            print(i)
      produces
        one
        two 
        three
    '''
    # Keyword options
    sep = kw.setdefault("sep", " ")
    linesep = kw.setdefault("linesep", "\n")
    line_filter = ToolzAdapter(kw.setdefault("line_filter", identity))
    token_filter = ToolzAdapter(kw.setdefault("token_filter", identity))
    # Process the string
    for string in strings:
        for line in string.split(linesep):
            for token in line_filter(line).split(sep):
                if token:
                    yield token_filter(token)

def ToolzAdapter(arg):
    '''For toolz.compose, the argument must be a sequence of functions, so
    we'll convert a single function to a list.  If toolz isn't available,
    then it must be a single function.
    '''
    if have_toolz:
        try:
            iter(arg)
            return compose(*arg)
        except TypeError:
            return compose(*[arg])
    else:
        if callable(arg):
            return arg
        raise TypeError("Argument arg must be a single function")

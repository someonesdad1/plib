'''
TODO
    * If kerf is zero, don't print out kerf loss.

Solve a one-dimensional cutting stock problem
    Uses the best-fit decreasing heuristic to generate a solution to a
    one-dimensional cutting stock problem.  Run the script with no
    arguments to get a usage statement.  See the associated cut.pdf
    documentation file.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Solve a one-dimensional cutting stock problem
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import hashlib
    import traceback as TB
    from collections import defaultdict, OrderedDict
    from fractions import Fraction
    from time import asctime
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from sig import sig
    from lwtest import run, raises, assert_equal, Assert
    # Optional library for clipboard -c option
    try:
        import pygtk
        pygtk.require("2.0")
        import gtk
        _have_gtk = True
    except ImportError:
        _have_gtk = False
    # Optional library for plotting -p option
    try:
        from g import *
        _have_g = True
    except ImportError:
        _have_g = False
    # Optional library for colored debug printing
    try:
        import color as C
        _have_color = True
    except ImportError:
        _have_color = False
if 1:   # Global variables
    # Number types we'll support
    Number = (int, float, Fraction)
    ii = isinstance
def ParseCommandLine(d):
    d["-c"] = False     # Get input from clipboard
    d["-p"] = False     # Plot
    d["-v"] = False     # Show time, datafile information
    d["significant_digits"] = 3
    d["kerf"] = 0
    d["resolution"] = 1
    Z.remove = True     # Removes trailing zeros & decimal point
    D.on = False
    ConvertLength.exception = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "cdpstv")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o == "-c":
            d["-c"] = not d["-c"]
        elif o == "-d":     # Show algorithm's progress
            D.on = True
        elif o == "-p":
            d["-p"] = not d["-p"]
            if not _have_g:
                Error("g library is missing, so -p option won't work")
        elif o == "-s":     # Dump sample datafile
            DumpConfigFileTemplate(d)
        elif o == "-t":     # Run self-tests (not quietly)
            failed, messages = run(globals())
            exit(failed)
        elif o == "-v":
            d["-v"] = not d["-v"]
    if d["-c"]:
        if not _have_gtk:
            Error("GTK isn't available, so -c option won't work.")
        return None
    else:
        if len(args) != 1:
            Usage(d)
        datafile = args[0]
        return datafile
def Usage(d, status=1):
    name = sys.argv[0]
    digits = d["significant_digits"]
    kerf = d["kerf"]
    res = d["resolution"]
    print(dedent(f'''
    Usage:  {name} [options] datafile
      Generate a cutting list for parts that must be cut from lengths of raw
      materials.  The datafile contains the information used to define the
      problem and is executable python code.  The algorithm used is the
      best-fit decreasing heuristic, which picks the largest piece which needs
      to be cut and cuts it from the smallest remaining stock piece.
    
      The variables in the datafile must be [default]:
        significant_digits      Integer from 1 to 15 [{digits}]
        kerf                    Number >= 0 [{kerf}]
        resolution              Number > 0 [{res}]
        stock                   Dictionary
        pieces                  Dictionary
    
      The stock and pieces dictionaries have the forms {{length:count, ...}}
      where length is a number (or a string representing a number) and count is
      an integer.  The AddStock() and AddPieces() convenience functions can
      also be used to define the stock or pieces to be cut.
    
      -c    Use the clipboard's contents for the datafile.
      -d    Turn on debug printing to see the heuristic's progress.
      -p    Plot the cutting details to a PostScript file cut.ps.
      -s    Print a datafile template to stdout with explanatory comments.
      -t    Run self-tests.
      -v    Include time, information on datafile in printed report.
    '''))
    exit(status)
def Error(*msg, status=1):
    line = TB.extract_stack()[-2:][0][1]
    print(*msg, "[line {}]".format(line), file=sys.stderr)
    exit(status)
def DumpConfigFileTemplate(d):
    print(dedent(f'''
    # Sample configuration file for cut.py script.  This file must be
    # executable python code.
    
    # Specify the number of significant digits in the output report.
    significant_digits = 6
    
    # The kerf keyword is used to define the kerf width of a cut.  It
    # is essentially tacked onto the end of each piece desired as it
    # is cut from a stock piece.  The default value is 0.
    kerf = 0.1
    
    # The resolution is used to convert each stock and piece length to an
    # integer so that the arithmetic is exact.  Each length is divided by this
    # number and converted to an integer.  If you define it as a string in
    # fractional form, the report will use fractions for output.
    resolution = 0.01
    
    # The stock dictionary defines stock on-hand for the problem.
    stock = {{
        # length : count,
        96: 4,      # Four 8 foot 2x4's
    }}
    
    # The pieces dictionary defines the cut pieces desired.
    pieces = {{ # length : count,
        # Proper and improper fractions are allowed as lengths.  The following
        # fractional forms result in the same length.
        "16+3/4": 1,
        "16-3/4": 1,
        "16 3/4": 1,
        "69/4": 1,
    
        # Integers, floats, and strings representing numbers are allowed as
        # lengths.  Python hashes integers and floats to the same value, so the
        # following second entry overwrites the first.
        33: 1,
        33.0: 1,
        "33": 1,
    }}
    
    # The AddPieces(*p) function is a convenience function to let you define
    # a set of desired piece lengths.  Example:  AddPieces(3, "3", 3.0)
    # would cause three pieces of length 3 to be added to the pieces
    # dictionary.  Note you can define lengths to be integers, strings, or
    # floats.  Stings can also be fractions as given above.  The function
    # AddStock(*p) works analogously for individual stock pieces.
    
    '''))
    exit(0)
def AddPieces(*p):
    '''Convenience function to add individual lengths.  Call as many
    times as needed.
    '''
    AddPieces.items.extend(list(p))
def AddStock(*p):
    '''Convenience function to add individual stock lengths.  Call as many
    times as needed.
    '''
    AddStock.items.extend(list(p))
def BasicCheck(opts):
    total_stock_length = sum([len(i) for i in opts["stock"]])
    total_piece_length = sum(opts["pieces"])
    sl = sig(total_stock_length*opts["resolution"])
    pl = sig(total_piece_length*opts["resolution"])
    if total_piece_length > total_stock_length:
        print('''Error:  length of desired pieces exceeds stock length
    Piece length = {pl}
    Stock length = {sl}'''.format(**locals()))
        exit(1)
def Exec(opts, variables):
    # exec is apparently needed in separate function for python 2.7
    if opts["datafile"] is None:
        # Get input from clipboard
        opts["datafile"] = "<Input from clipboard>"
        if _have_gtk:
            cb = gtk.clipboard_get()
            s = cb.wait_for_text()
        else:
            s = os.popen("xsel").read().encode("utf-8")
    else:
        s = open(opts["datafile"]).read()
    m = hashlib.md5()
    exec(s, globals(), variables)
    m.update(s.encode("utf8"))
    opts["hash"] = m.hexdigest()
def InterpretNumber(s, name):
    '''s is a possible number or a string representing a number.  Return a
    suitable int, float, or Fraction.
    '''
    e = ValueError("'{}' is an improper number".format(name))
    if ii(s, Number):
        return s
    elif ii(s, str):
        try:
            if "." in s:
                return float(s)
            elif "/" in s:
                f = InterpretFraction(s)
                if f is not None:
                    return f
                raise e
            else:
                return int(s)
        except Exception:
            raise e
    else:
        raise e
def InterpretFraction(s):
    '''Return a Fraction object if the string s contains '/' and can be
    interpreted as a fraction.  Allowed forms are
        a
        a/b
        a b/c
        a-b/c
        a+b/c
    where a, b, and c are positive integers with no signs.
 
    Return None if it cannot be interpreted as a fraction.
    '''
    if not ii(s, str) or "." in s:
        return None
    if "/" not in s:
        # It must be an integer
        try:
            n = int(s)
            return Fraction(n, 1)
        except Exception:
            return None
    # It contains '/', so pick it apart
    s = s.replace("-", " ").replace("+", " ")
    f = s.split("/")
    if len(f) != 2:
        return None
    numer, denom = f
    # See if numerator can be split on space characters
    f = numer.split()
    if len(f) == 1:
        try:
            f = Fraction(s)
            return None if f.denominator == 1 else f
        except Exception:
            return None
    elif len(f) == 2:
        ip, numer = f
        try:
            fr = Fraction(numer + "/" + denom)
            f = int(ip) + fr
            return None if f.denominator == 1 else f
        except Exception:
            return None
    else:
        return None
def TestInterpretFraction():
    f = InterpretFraction
    for s in ("", 1, 1.1, "-", "+", ".", "/", "1/", "/1", "1 /1", "1/0",
              "1/1", "1 1/1"):
        Assert(f(s) is None)
    for s, n, d in (
        ("2", 2, 1),
        ("1/2", 1, 2),
        ("0 1/2", 1, 2),
        ("1 1/2", 3, 2),
    ):
        Assert(f(s) == Fraction(n, d))
def ConvertLength(length, resolution):
    '''Convert the given expression for a length to an integer number of
    resolution units.  The expression is converted to a type that depends
    on the type of resolution.
    '''
    eps = ConvertLength.eps
    # The following exception is used for the self-tests only
    e = ValueError("length = '{}', resolution = '{}'".format(str(length),
                   str(resolution)))
    retval = None
    if ii(resolution, Fraction):
        # length is to be interpreted as a Fraction
        if ii(length, Fraction):
            retval = int(length/resolution)
        elif ii(length, str):
            f = InterpretFraction(length)
            if f is None:
                try:
                    # Evaluate it as a float and convert it to a fraction
                    f = Fraction(float(eval(length))*(1 + eps))
                    retval = int(f/resolution)
                except Exception:
                    if ConvertLength.exception:
                        raise e
                    Error("'{}' is an invalid expression".format(length))
            else:
                retval = int(f/resolution)
        elif ii(length, (int, float)):
            retval = int(Fraction(length)/resolution)
        else:
            if ConvertLength.exception:
                raise e
            Error("Bad type for length '{}'".format(str(length)))
    elif ii(resolution, (int, float)):
        if ii(length, str):
            try:
                retval = int(float(eval(length))/resolution*(1 + eps))
            except Exception:
                if ConvertLength.exception:
                    raise e
                Error("'{}' is an invalid expression".format(length))
        elif ii(length, (Fraction, int, float)):
            try:
                retval = int(float(length)/resolution*(1 + eps))
            except Exception:
                if ConvertLength.exception:
                    raise e
                Error("'{}' is an invalid expression".format(str(length)))
        else:
            if ConvertLength.exception:
                raise e
            Error("Bad type for length '{}'".format(str(length)))
    else:
        if ConvertLength.exception:
            raise e
        Error("Bad type for resolution")
    if retval is None or not ii(retval, int):
        if ConvertLength.exception:
            raise e
        Error("Bug in program for length conversion")
    return retval
def TestConvertLength():
    def Check(expr, value):
        if expr != value or not ii(expr, int):
            raise ValueError()
    f, F = ConvertLength, Fraction
    f.exception = True
    f.eps = 1e-14
    for res in (1, 1.0, F(1, 1)):
        Check(f(0, res), 0)
        Check(f(1, res), 1)
        Check(f(2, res), 2)
        Check(f(2., res), 2)
        Check(f(F(2, 1), res), 2)
        Check(f("2", res), 2)
        Check(f("2.", res), 2)
        Check(f("2/1", res), 2)
        raises(ValueError, f, "0 2/1", res)
    # Check fractional resolutions more carefully
    res = F(1, 8)
    Check(f(2, res), 16)
    Check(f(2.0, res), 16)
    Check(f(F(2, 1), res), 16)
    Check(f("2", res), 16)
    Check(f("2/1", res), 16)
    Check(f("1/2", res), 4)
    Check(f("3/8", res), 3)
    Check(f("0 3/8", res), 3)
    Check(f("1 3/8", res), 11)
    Check(f("3/16", res), 1)
    del f.exception
    del f.eps
def ReadDataFile(opts):
    '''Add the information from the datafile to the opts dictionary under
    the keys
        significant_digits
        kerf
        resolution
        stock
        pieces
    The first three will be numbers and the last two will be
    defaultdict(int) with keys of integer piece lengths and values
    of integer counts.
    '''
    variables = {
        "significant_digits": 3,
        "kerf": 0,
        "resolution": 1,
    }
    needed_keys = variables.keys()
    Exec(opts, variables)
    # Make sure we have the required variables
    required = "significant_digits kerf resolution"
    for key in required.split():
        if key not in variables:
            Error("'{}' variable missing in datafile".format(key))
    if "pieces" not in variables:
        variables["pieces"] = {}
    if "stock" not in variables:
        variables["stock"] = {}
    # Validate the values
    sd = variables["significant_digits"]
    if not ii(sd, int):
        Error("'significant_digits' must be an integer")
    sig.digits = opts["significant_digits"] = sd
    kerf = InterpretNumber(variables["kerf"], "kerf")
    if kerf < 0:
        Error("'kerf' must be >= 0")
    opts["kerf"] = kerf
    resolution = InterpretNumber(variables["resolution"], "resolution")
    if resolution <= 0:
        Error("'resolution' must be > 0")
    opts["resolution"] = resolution
    # Note that _Stock.kerf is in units of resolution
    _Stock.kerf = int(kerf/resolution)
    if not _Stock.kerf:
        print("Warning:  kerf is zero in resolution units")
    _Stock.resolution = resolution
    # Check that each value in the dictionaries is an integer
    for name in ("stock", "pieces"):
        if not isinstance(variables[name], dict):
            Error("'{}' variable is not a dictionary".format(name))
        if not all([isinstance(i, int) for i in variables[name].values()]):
            Error("'{}' dictionary has a non-integer value".format(name))
    # Create the stock and pieces dictionaries we'll use for subsequent
    # computations.  Their keys are integer lengths and their values are
    # counts.  Note these are different than the dictionaries defined in
    # the datafile.
 
    # The following small number is used to ensure that floating point
    # numbers can be converted sensibly to integer units of resolution.
    # For example, if a length was 8.7 and the resolution is 0.1, python
    # will calculate that the integer number of resolutions is 86, not 87
    # as you'd suppose.  The reason is because 8.7/0.1 = 86.99999999999999.
    # The multiplication by (1 + eps) is intended to correct this roundoff
    # problem.
    eps = opts["eps"] = _Stock.eps = 1e-14
    # stock
    stock = defaultdict(int)
    for length, count in variables["stock"].items():
        if ii(length, str):
            try:
                n = InterpretNumber(length, "stock")
                L = int(n/resolution)
            except Exception:
                Error("'{}' is an invalid number".format(length))
        elif ii(length, Number):
            L = int(length/resolution*(1 + eps))
        else:
            Error("stock key '{}' is not convertible to a number".format(
                str(length)))
        if not ii(count, int):
            Error("stock count for key '{}' is not an integer".format(
                str(length)))
        Assert(ii(L, int))
        stock[_Stock(L)] += count
    # Add any pieces from the convenience AddStock function
    for length in AddStock.items:
        if ii(length, str):
            try:
                n = InterpretNumber(length, "stock")
                L = int(n/resolution)
            except Exception:
                Error("'{}' is an invalid number".format(length))
        elif ii(length, Number):
            L = int(length/resolution*(1 + eps))
        else:
            Error("AddStock() item '{}' is not convertible to a number".format(
                str(length)))
        Assert(ii(L, int))
        stock[_Stock(L)] += 1
    # pieces
    pieces = defaultdict(int)
    for length, count in variables["pieces"].items():
        if ii(length, str):
            try:
                n = InterpretNumber(length, "pieces")
                L = int(n/resolution)
            except Exception:
                Error("'{}' is an invalid number".format(length))
        elif ii(length, Number):
            L = int(length/resolution*(1 + eps))
        else:
            Error("pieces key '{}' is not convertible to a number".format(
                str(length)))
        if not ii(count, int):
            Error("pieces count for key '{}' is not an integer".format(
                str(length)))
        Assert(ii(L, int))
        pieces[L] += count
    # Add any pieces from the convenience AddPieces function
    for length in AddPieces.items:
        if ii(length, str):
            try:
                n = InterpretNumber(length, "pieces")
                L = int(n/resolution)
            except Exception:
                Error("'{}' is an invalid number".format(length))
        elif ii(length, Number):
            L = int(length/resolution*(1 + eps))
        else:
            Error("AddPieces() item '{}' is not convertible to a number".
                  format(str(length)))
        Assert(ii(L, int))
        pieces[L] += 1
    opts["pieces"] = pieces
    # Make containers of the stock and pieces so that we can apply the
    # algorithm and keep the containers sorted.
    stock_container = []
    for st, count in stock.items():
        for i in range(count):
            stock_container.append(_Stock(len(st)))
    stock_container.sort(key=lambda x: len(x))
    pieces_container = []
    for length, count in pieces.items():
        pieces_container.extend([length]*count)
    pieces_container.sort()
    # Put them into the options container
    opts["stock"] = stock_container
    opts["pieces"] = pieces_container
    if not len(opts["pieces"]):
        Error("No piece lengths were given")
def Z(x, digits=None):
    '''x is a string representing a number.  Convert it to a string using
    sig() and remove trailing zeros and the decimal point if possible.
    '''
    s = sig(x) if digits is None else sig(x, digits)
    if not Z.remove:
        return s
    if "." not in s:
        return s
    else:
        while s[-1] == "0":
            s = s[:-1]
        if s[-1] == ".":
            s = s[:-1]
        return s
def D(*p, **kw):
    '''Debug printing.  Set D.on to True to cause printing.
    '''
    if D.on:
        if _have_color:
            C.fg(C.lblue)
        print(*p, **kw)
        if _have_color:
            C.normal()
class _Stock(object):
    '''Models a piece of stock.  The length of the stock is always an
    integer (and is in resolution units) to avoid floating point arithmetic
    issues.  Has a container to keep track of the pieces cut from it.
    You must set kerf_width to an integer.
    '''
    kerf_width = None
    resolution = None       # Used for printing actual lengths
    physical = False        # If True, show string in physical units
    eps = None              # Used for rounding near zero
    def __init__(self, length):
        Assert(ii(length, int))
        Assert(length > 0)
        Assert(ii(_Stock.kerf, int))
        Assert(_Stock.kerf >= 0)
        self._original_length = self._length = length
        # The _cuts container will contain each length cut followed by a
        # negative number (or zero) representing the kerf width.
        self._cuts = []
    def __len__(self):
        return self._length
    def __bool__(self):
        return self._length != 0
    def __str__(self):
        return "<{}:{}:{}>".format(self._length, self._original_length,
                                   str(tuple(self._cuts)))
    '''Comparisons:  The first comparison is on the original stock length;
    then number of cuts, then amount of scrap.  These two comparisons
    allow sorting of sequences of _Stock objects.
    '''
    def __lt__(self, other):
        if not ii(other, _Stock):
            raise ValueError("other item must be a _Stock object")
        if self.L0 == other.L0:
            if len(self._cuts) == len(other._cuts):
                # Length tie:  compare remaining stock.
                return self._uncut_stock() < other._uncut_stock()
            else:
                return len(self._cuts) < len(other._cuts)
        else:
            return self.L0 < other.L0
    def __eq__(self, other):
        if not ii(other, _Stock):
            raise ValueError("other item must be a _Stock object")
        return (self.L0 == other.L0 and len(self._cuts) == len(other._cuts)
                and self._uncut_stock() == other._uncut_stock())
    def _uncut_stock(self):
        # Note this is in resolution units
        kerf_loss = sum([-i for i in self._cuts if i <= 0])
        cut_lengths = [i for i in self._cuts if i > 0]
        return self.L0 - sum(cut_lengths) - kerf_loss
    def __repr__(self):
        return str(self)
    def __hash__(self):
        # Hash by the details string, which allows us to also save plot
        # data in Report().
        return hash(self.details())
    @property
    def L0(self):
        return self._original_length
    @property
    def cuts(self):
        return len(self._cuts)
    def cut(self, length):
        '''Simulate cutting off a length of the stock.  Clearly, length
        must be <= the existing length.  If length is less than the
        existing length and the kerf width, add the cut length to the
        self._cuts container and adjust to the new length.  If the piece
        can't be cut, raise a ValueError exception.
        '''
        Assert(self._length > 0)
        if length > self._length:
            raise ValueError("Not long enough for {}".format(length))
        else:
            perfect_cut = (length == self._length)
            self._cuts.append(length)
            self._length -= length
            if not perfect_cut:
                self._cuts.append(-_Stock.kerf)
            if self._length <= _Stock.kerf:
                self._length = 0  # Piece is used up
            else:
                self._length -= _Stock.kerf
                Assert(self._length > 0)
    def details(self):
        '''Return a string showing the original length, cuts, and scrap
        percentage.  If _Stock.resolution is a fraction, then the output
        strings are also fractions.
        '''
        res = _Stock.resolution if _Stock.physical else 1
        frac = ii(res, Fraction)
        fmt = MakeProperFraction if frac else Z
        L = self.L0*res
        s = [fmt(L), ": "]
        # Cut details
        cd = [i*res for i in self._cuts if i > 0]
        cd.sort()
        s.append(Collapse([fmt(i) for i in cd]))
        # Remaining material
        kl = sum([-i for i in self._cuts if i <= 0])*res    # Kerf loss
        uncut_stock = L - sum(cd) - kl
        if abs(uncut_stock) < _Stock.eps:
            uncut_stock = 0
        sp = ""  # Allows for space between number and %
        if uncut_stock:
            pct = 100*float(uncut_stock/L)
            s.append("  [{}{}({}%)]".format(fmt(uncut_stock), sp, Z(pct, 2)))
        # Kerf loss
        s.append("  <{}{}({}%)>".format(fmt(kl), sp, Z(100*float(kl/L), 2)))
        return ''.join(s)
def MakeCutList(opts):
    '''Construct the cut list; it's a list of _Stock items that have been
    cut until the remaining piece is too short for any remaining piece.
 
    The algorithm is the "first fit decreasing heuristic", which cuts the
    largest piece needed from the smallest piece of stock that is long
    enough.  This is easy to do because the stock and pieces containers are
    kept sorted.
 
    The stock container is changed to have the form
        [[length0, ], [length1, ], ...]
    because this allows the container to be sorted by the first element
    (the length) and the smallest remaining stock length is gotten by
    popping off the left element.  The piece and kerf are cut, the piece is
    added to the stock's list
    '''
    cutlist = []  # Hold stock pieces that can't be used anymore
    stock, pieces = opts["stock"], opts["pieces"][:]
    indent = " "*1
    D(dedent('''
    Debug output showing operation of algorithm in resolution units:
    (kerf cuts are shown as negative numbers or zero)'''))
    # Make sure pieces is sorted so that pop() (which removes the
    # right-most element) gets the largest piece.
    pieces.sort()
    while pieces:
        largest_piece = pieces.pop()
        D(indent, "Need to cut piece =", largest_piece)
        # Find the smallest piece of stock that can be used for this piece
        found = failure = False
        for i, st in enumerate(stock):
            if largest_piece == len(st):
                # Perfect match with no cut
                D(indent, "  Perfect match to", repr(st), "(added to cutlist)")
                st.cut(largest_piece)
                cutlist.append(st)
                del stock[i]
                found = True
                break
            elif largest_piece + _Stock.kerf <= len(st):
                # Can cut to fit this piece
                D(indent, "  Can cut from stock piece", repr(st), end=" ")
                st.cut(largest_piece)
                del stock[i]
                found = True
                if len(st) <= _Stock.kerf:
                    # A kerf or less would be left after cut
                    cutlist.append(st)
                    D("(stock piece used up)")
                    break
                # Put back into stock list
                stock.append(st)
                stock.sort(key=lambda x: len(x))
                D("(put back {} into stock container)".format(len(st)))
                break
        if not found:
            D(indent, "Failure:  couldn't find a long enough piece")
            failure = True
            break
    opts["failure"] = largest_piece if failure else None
    # Put the cutlist items back into the stock sequence & sort
    stock.extend(cutlist)
    stock.sort(key=lambda x: x._original_length)
    D(indent, "Ending stock state:")
    if D.on:
        for i in stock:
            D(" "*4, repr(i))
def SetUp(file):
    '''Convenience function to set up the drawing environment and return a
    file object to the output stream.
    '''
    ofp = open(file, "w")
    ginitialize(ofp, False)
    setOrientation(landscape, inches)
    return ofp
def MakeProperFraction(f):
    '''Return the Fraction f as a proper fraction string.
    '''
    ip, remainder = divmod(f.numerator, f.denominator)
    if ip:
        fr = Fraction(remainder, f.denominator)
        if remainder:
            return "{}-{}".format(ip, str(fr))
        else:
            return "{}".format(ip)
    return str(f)
def Collapse(seq, sortkey=None, proper_fractions=True):
    '''Collapse a sequence of numbers to a compact string form by
    indicating the {counts} of repeated objects.  Example:
      (3, 1, 2, 4, 1, 1, 2, 4) --> 1{3} 2{2} 3 4{2}
    The numbers in seq can be integers, floats, or Fractions.  Any 
    fractions are converted to proper form:  e.g., 9/4 --> 2-1/4.
    '''
    # Comment 14May2017:  this could probably be rewritten more efficiently
    # with itertools.groupby().
    if not seq:
        return ""
    items, out = defaultdict(int), []
    while seq:
        item = seq.pop(0)
        items[item] += 1
    # Try to order the keys by numerical order
    keys = items.keys()
    try:
        if sortkey is None:
            #keys.sort()  # Works only for python 2
            keys = sorted(keys)
        else:
            #keys.sort(key=sortkey)  # Works only for python 2
            keys = sorted(keys, key=sortkey)
    except Exception:
        pass
    # Construct a sequence of output strings
    for k in keys:
        s, count = str(k), items[k]
        if ii(k, Fraction) and "/" in s and proper_fractions:
            ip, remainder = divmod(k.numerator, k.denominator)
            if ip:
                fr = Fraction(remainder, k.denominator)
                s = "{}-{}".format(ip, str(fr))
        if count == 1:
            out.append(s)
        else:
            out.append("{}{{{}}}".format(s, count))
    # Convert to one string
    return ' '.join(out)
def TestCollapse():
    f, F = Collapse, Fraction
    raises(Exception, f, 1)
    raises(Exception, f, 1.0)
    raises(Exception, f, F(1, 1))
    raises(Exception, f, object())
    Assert(f([]) == "")
    Assert(f([1]) == "1")
    Assert(f([1, 1]) == "1{2}")
    Assert(f([1, 1, 1]) == "1{3}")
    Assert(f([1, 1, 2]) == "1{2} 2")
    Assert(f([1, 2]) == "1 2")
    Assert(f([1, 2.0]) == "1 2.0")
    Assert(f([1.0, 2.0]) == "1.0 2.0")
    Assert(f([1.0, 2.0, 2]) == "1.0 2.0{2}")
    Assert(f([1.0, 2, 2.0]) == "1.0 2{2}")
    Assert(f([2, 1, 1, 2]) == "1{2} 2{2}")
    Assert(f([2, 1, 1.0, 2]) == "1{2} 2{2}")
    Assert(f([2, 1, F(1, 1), 2]) == "1{2} 2{2}")
    Assert(f([1.0, F(1, 1)]) == "1.0{2}")
    Assert(f([F(1, 1), 1.0]) == "1{2}")
    Assert(f([1, F(1, 1)]) == "1{2}")
    Assert(f([F(1, 1), 1]) == "1{2}")
    Assert(f([F(1, 2), 1]) == "1/2 1")
    Assert(f([F(1, 2), F(1, 2)]) == "1/2{2}")
    Assert(f([F(9, 4)], proper_fractions=False) == "9/4")
    Assert(f([F(9, 4), F(9, 4)], proper_fractions=False) == "9/4{2}")
    Assert(f([F(9, 4)]) == "2-1/4")
    Assert(f([F(9, 4), F(9, 4)]) == "2-1/4{2}")
    Assert(f([2.25, F(9, 4)]) == "2.25{2}")
    Assert(f([F(9, 4), 2.25]) == "2-1/4{2}")
def ListStr(l):
    print(" "*3, ' '.join([str(i) for i in l]))
def Test1():
    '''Simplest test case:  stock length of 1 and a piece of 1 needed.
    '''
    _Stock.kerf = 0
    d = {}
    d["resolution"] = 1
    d["stock"] = [_Stock(1)]
    d["pieces"] = [1]
    MakeCutList(d)
    Assert(len(d["stock"]) == 1)
    st = d["stock"][0]
    Assert(st._cuts == [1])  # It's a perfect match (no kerf needed)
def Test2():
    '''This test case came from the document
    http://mrking.cmswiki.wikispaces.net/file/view/BinPacking.docx, page 5.
    The pieces are (1, 1, 2, 2, 4, 4, 5, 6, 7, 8) with four stock lengths
    of 10 each.  The stock gets cut into (2, 8), (1, 2, 7), (4, 6), and
    (1, 4, 5).
    '''
    _Stock.kerf = 0
    d = {}
    def cl(x):
        return len(x)
    d["resolution"] = 1
    d["stock"] = [_Stock(10), _Stock(10), _Stock(10), _Stock(10)]
    d["stock"].sort(key=cl)
    d["pieces"] = [1, 1, 2, 2, 4, 4, 5, 6, 7, 8]
    MakeCutList(d)
    S = frozenset
    expected = [S((2, 8)), S((1, 2, 7)), S((4, 6)), S((1, 4, 5))]
    got = []
    for i in d["stock"]:
        s = S([j for j in i._cuts if j])
        Assert(s in expected)
        got.append(s)
    Assert(len(got) == 4)
def Test3():
    '''This example comes from the web page
    http://www.ams.org/samplings/feature-column/fcarc-bins1.  The problem
    is stock lengths of 20 and pieces of (4, 8, 7, 10, 3, 8).  The sum of
    the piece lengths is 40, so they might be cut from two stock pieces
    (kerf = 0); in fact, an optimal solution is (8, 8, 4) and (10, 7, 3).
    The first-fit decreasing heuristic doesn't find this solution, however.
 
    Here's the operation of the FFD heuristic:
        Sorted lengths = [3, 4, 7, 8, 8, 10]
    Pop off largest piece = 10
    Put in bin1:  1:(10, )
    Pop off next largest piece = 8
    Put in bin1:  1:(10, 8,)
    Pop off next largest piece = 8
    No room in bin1; start bin2:  2:(8,)
    Pop off next largest piece = 7
    Put in bin2:  2:(8, 7,)
    Pop off next largest piece = 4
    Put in bin2:  2:(8, 7, 4,)
    Pop off last piece = 3
    Put in bin3:  3:(3,)
 
    Thus, solution via FFD is
        (10, 8)
        (8, 7, 4)
        (3,)
    '''
    _Stock.kerf = 0
    d = {}
    d["resolution"] = 1
    d["stock"] = [_Stock(i) for i in (20, 20, 20)]
    d["pieces"] = [4, 8, 7, 10, 3, 8]
    MakeCutList(d)
    S = frozenset
    expected = [S((10, 8)), S((8, 7, 4)), S((3,))]
    got = []
    for i in d["stock"]:
        s = S([j for j in i._cuts if j])
        Assert(s in expected)
        got.append(s)
    Assert(len(got) == 3)
def RunSelfTests(opts):
    debug_state = D.on
    D.on = False
    failed, messages = run(globals(), quiet=True)
    if failed:
        run(globals())
        exit(1)
    D.on = debug_state
def PrintStartingState(opts):
    res = opts["resolution"]
    kerf = opts["kerf"]
    digits = opts["significant_digits"]
    fmt = MakeProperFraction if ii(res, Fraction) else Z
    if opts["-v"]:
        # Print datafile data, date
        print(sys.argv[0], "script")
        print(asctime())
        print("Datafile = '{}'".format(opts["datafile"]))
        print("MD5 hash of datafile =", opts["hash"], "\n")
    print(dedent(f'''
    Input data ({{n}} is a count):
      significant digits = {digits}
      resolution = {res}
      kerf       = {kerf}'''))
    st = [len(i) for i in opts["stock"][:]]
    st.sort()
    s = Collapse([fmt(i*res) for i in st])
    print("  stock  =", s)
    p = opts["pieces"][:]
    p.sort()
    s = Collapse([fmt(i*res) for i in p])
    print("  pieces =", s)
def Dump(opts, physical=False):
    _Stock.physical = physical
    if _have_color:
        if physical:
            C.fg(C.lgreen)
        else:
            C.fg(C.lred)
    indent = " "*3
    print("-"*70)
    print("Dump of stock and pieces containers")
    print("  Dimensions in physical units:  {}".format(physical))
    print("Stock:")
    for i in opts["stock"]:
        print(indent, i)
    print("Pieces:")
    print(indent, str(opts["pieces"]))
    print("-"*70)
    if _have_color:
        C.normal()
def PrintReport(opts):
    resolution = opts["resolution"]
    # Summary information
    uncut, used_up, partial = [], [], []
    for i in opts["stock"]:
        if not i.cuts:
            uncut.append(i)
        elif len(i):
            partial.append(i)
        else:
            used_up.append(i)
    print("\nCutting details:    length: cuts  "
          "[left over (%)]  <kerf loss (%)>", sep="")
    indent = " "*3
    _Stock.physical = True      # Make sure output is in physical units
    fmt = MakeProperFraction if ii(resolution, Fraction) else Z
    num_cuts = 0
    def f(x):
        return len([j for j in x._cuts if j <= 0])
    opts["plot"] = plot = {     # Stores data for plotting
        "uncut": [],
        "used_up": OrderedDict(),
        "partial": OrderedDict(),
    }
    if uncut:
        if _have_color:
            C.fg(C.green)
        print("  Uncut stock pieces: ")
        t = [i.L0*resolution for i in uncut]
        t.sort()
        s = Collapse([fmt(i) for i in t])
        print(indent, s)
        plot["uncut"] = t
        plot["uncut_string"] = s
        if _have_color:
            C.normal()
    if used_up:
        if _have_color:
            C.fg(C.lgreen)
        used_up.sort()
        collect = OrderedDict()  # Organize by counts
        uu = plot["used_up"]
        print("  Completely used stock pieces:")
        for st in used_up:
            s = st.details()
            if s in collect:
                collect[s] += 1
                uu[st] += 1
            else:
                collect[s] = 1
                uu[st] = 1
            num_cuts += f(st)
        for s in collect:
            c = "{{{}}} ".format(collect[s]) if collect[s] > 1 else ""
            print("{indent} {c}{s}".format(**locals()))
        if _have_color:
            C.normal()
    if partial:
        partial.sort()
        collect = OrderedDict()  # Organize by counts
        par = plot["partial"]
        print("  Partially used stock pieces:")
        for st in partial:
            s = st.details()
            if s in collect:
                collect[s] += 1
                par[st] += 1
            else:
                collect[s] = 1
                par[st] = 1
            num_cuts += f(st)
        for s in collect:
            c = "{{{}}} ".format(collect[s]) if collect[s] > 1 else ""
            print("{indent} {c}{s}".format(**locals()))
    if opts["failure"] is not None:
        fl = opts["failure"]*resolution
        if _have_color:
            C.fg(C.lred)
        print("Failed on piece of length {}".format(fl))
        if _have_color:
            C.normal()
    else:
        # Check consistency:  positive numbers in lists of cuts should sum to
        # the total length of all pieces.
        total_cut = 0
        for i in used_up + partial:
            total_cut += sum([j for j in i._cuts if j > 0])
        Assert(total_cut == sum(opts["pieces"]))
        # Get totals
        total_stock = sum([i._original_length for i in opts["stock"]])
        total_kerf = -sum([sum([j for j in i._cuts if j < 0]) for i in
                          used_up + partial])
        scrap = total_stock - total_cut - total_kerf
        scrap_pct = 100*scrap/total_stock
        lcp = fmt(total_cut*resolution)
        lcpp = Z(100*total_cut/total_stock, 2)
        sl = fmt(total_stock*resolution)
        kl = fmt(total_kerf*resolution)
        klp = Z(100*total_kerf/total_stock, 2)
        sc = fmt(scrap*resolution)
        scp = Z(scrap_pct, 2)
        w = max([len(i) for i in (lcpp, klp, scp, sl)])
        print(dedent(f'''
        Summary:
            Starting stock length   {sl:>{w}}
            Length of cut pieces    {lcp:>{w}} ({lcpp}%)
            Kerf loss               {kl:>{w}} ({klp}%)
            Scrap left over         {sc:>{w}} ({scp}%)
            Number of cuts          {num_cuts:>{w}}'''))
        plot["total_stock"] = total_stock*resolution
        plot["total_kerf"] = total_kerf*resolution
        plot["scrap"] = scrap*resolution
        plot["num_cuts"] = num_cuts
def Plot(opts):
    Assert(1/2 == 0.5)
    # Constants
    scrap_color = gray(0.5)
    scrap_color = coral
    cut_color = lavender
    kerf_color = khaki1
    T = None
    # Get info to plot
    plot = opts["plot"]
    uncut = plot["uncut"]       # List of numbers
    partial = plot["partial"]   # OrderedDict of st:count
    used_up = plot["used_up"]   # OrderedDict of st:count
    Assert(ii(uncut, list) and ii(partial, OrderedDict) and
           ii(used_up, OrderedDict))
    total_stock = plot["total_stock"]
    total_kerf = plot["total_kerf"]
    scrap = plot["scrap"]
    num_cuts = plot["num_cuts"]
    SetUp("cut.ps")
    # Assume letter-size paper in landscape mode using inches
    margin = 0.4
    W, H = 11 - 2*margin, 8.5 - 2*margin  # Viewport size
    translate(margin, margin)
    move(0, 0)
    if 0:  # Plot a bounding rectangle
        push()
        LineColor(red)
        rectangle(W, H)
        pop()
    # Number of bars we'll need
    res = _Stock.resolution
    nbars = len(partial) + len(used_up)
    a = max([i.L0 for i in partial]) if partial else 0
    b = max([i.L0 for i in used_up]) if used_up else 0
    maxlen = max(a, b)
    if not maxlen:
        Error("Can't plot:  maxlen is zero")
    # Constants for plot
    wmax, hmax = 0.95*W, 0.8*H      # Leave room for annotations
    dy = min(hmax/nbars, hmax/10)   # Increment between each bar
    T = dy/3                        # Font size
    res = _Stock.resolution
    TextSize(T)
    def PlotCuts(st, dy, bar_width, count):
        push()
        FillOn()
        x, L = 0.0, float(st.L0)
        ytext = dy/2 - T/3
        fmt = MakeProperFraction if ii(res, Fraction) else Z
        for cutlen in st._cuts:
            move(x/L*bar_width, 0)     # Left edge of subrectangle
            width = abs(cutlen)/L*bar_width
            if cutlen < 0:
                # Finite kerf
                FillColor(kerf_color)
                rectangle(width, dy)
            elif cutlen > 0:
                FillColor(cut_color)
                rectangle(width, dy)
                # Add label of length
                move((x + cutlen/2)/L*bar_width, ytext)
                ctext(fmt(cutlen*res))
            x += abs(cutlen)
        # Plot remaining space as scrap
        FillOn()
        FillColor(scrap_color)
        delta = x/L
        move(delta*bar_width, 0)
        rectangle((1 - delta)*bar_width, dy)
        # Label multiplicity
        move(bar_width + T/3, ytext)
        text("X" + str(count))
        pop()
    # Starting position of lower left corner of first bar
    x, y = 0, H - dy
    d = OrderedDict()
    d.update(used_up)
    d.update(partial)
    for st, count in d.items():
        push()
        # Put origin at lower left corner of bar
        translate(x, y)
        bar_width = wmax*st.L0/maxlen
        move(0, 0)
        rectangle(bar_width, dy)
        PlotCuts(st, dy, bar_width, count)
        pop()
        y -= dy
    # Plot legend
    a = dy/2
    dx = T/3
    x = 0
    push()
    FillOn()
    translate(0, a)
    move(x, 0)
    FillColor(cut_color)
    rectangle(a, a)
    move(a + dx, T/3)
    text("Cut piece")
    x += 5*a
    move(x, 0)
    FillColor(kerf_color)
    rectangle(a, a)
    move(x + a + dx, T/3)
    text("Kerf")
    x += 5*a
    move(x, 0)
    FillColor(scrap_color)
    rectangle(a, a)
    move(x + a + dx, T/3)
    text("Scrap")
    # Textual summary
    x += 5*a
    move(x, T/3)
    text("Maximum length = {}".format(sig(maxlen*res)))
    # Uncut stock
    if "uncut_string" in plot:
        move(0, dy)
        text("Uncut stock: " + plot["uncut_string"])
    pop()
if __name__ == "__main__":
    opts = {}       # Options dictionary
    AddPieces.items = []   # Convenience function sequence
    AddStock.items = []    # Convenience function sequence
    opts["datafile"] = ParseCommandLine(opts)
    RunSelfTests(opts)
    ReadDataFile(opts)
    BasicCheck(opts)
    PrintStartingState(opts)
    MakeCutList(opts)
    PrintReport(opts)
    if opts["failure"] is None and _have_g and opts["-p"]:
        Plot(opts)

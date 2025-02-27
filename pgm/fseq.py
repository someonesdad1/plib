"""
TODO:
    - wor 100 10 doesn't work

    - Ensure the -x xfms are applied to the array before the -X
      operations so that they will be applied sequentially.

Output an arithmetic sequence of numbers

Can also generate sequences of random numbers (use -h to see
details).
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2008, 2012 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Generate sequences of numbers
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import os
    import random
    import math
    import fractions
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    import numpy as np
    import numpy.random as npr
    from sig import sig as _sig
    from cmddecode import CommandDecode

    _have_scipy = False
    try:
        from scipy.stats import binom, hypergeom, expon, norm, poisson

        _have_scipy = True
    except ImportError:
        pass
if 1:  # Global variables
    _out = sys.stdout.write
    _err = sys.stderr.write
    _nl = "\n"
    _digits = 3  # Default number of significant figures in floats
    _sep = " "  # Default separator
    # The following string is common to the usage message and the manpage.
    _basic = """
    Output a sequence of numbers from n to m inclusive in steps of
    inc.  For just n, output from 1 to n by 1.  For n to m, output
    n to m by 1.  n, m, and inc can be integers, floats, fractions
    or python expressions.  The absolute value of inc will be taken
    unless the -g option is used.
    """


def Manpage(d, bye=None):
    name = os.path.split(sys.argv[0])[1]
    basic = _basic
    digits = _digits
    eps = d["-e"]
    sep = _sep
    _out(
        dedent("""
    Usage:  {name} [options] n [m [inc]]
      Output a sequence of numbers from n to m inclusive in steps of
      inc.  For just n, output from 1 to n by 1.  For n to m, output
      n to m by 1.  n, m, and inc can be integers, floats, fractions
      or python expressions.  The absolute value of inc will be taken
      unless the -g option is used.
    
    Other command line forms for generating random numbers:
        bin n N p       n binomial variates with population N and prob. p
        hyp n N p m     n hypergeometric variates from a population of
                        N total items and a fraction p with the
                        characteristic of interest.  The draw is a
                        sample of m items.
        exp n mu        n exponential deviates with mean mu
        normal n        n normal deviates, mean = 0, stddev = 1
        normal n s      n normal deviates, mean = 0, stddev = s
        normal n mu s   n normal deviates, mean = mu, stddev = s
        poisson n mu    n Poisson variates with mean of mu
        randint n a b   n random integers x such that a <= x < b
        uniform n a b   n random floats x such that a <= x < b
        wr n m          Sample of m items with replacement from a
                            population of n
        wor n m         Sample of m items without replacement from
                            a population of n
        shuffle n       Random permutation of n items
    
    The -c and -p options calculate the CDFs or PDFs, respectively,
    for the distributions with the following parameters (the
    probabilities are for the CDFs):
        bin n p x1 [x2 ...]     Binomial P(X <= x1 | n, p)
        hyp N p m x1 [x2 ...]   Hypergeometric P(X <= x1 | N, p, m)
        exp mu x1 [x2 ...]      Exponential P(X <= x1 | mu)
        norm x1 [x2 ...]        Standard normal P(X <= x1 | mu=0, sigma=1)
        norm mu:s x1 [x2 ...]   Normal P(X <= x1 | mu, sigma=s)
        poisson mu x1 [x2 ...]  Poisson P(X <= x1 | mu)
    
    p for the binomial and hypergeometric distributions is the
    fraction of the population that has the desired trait.
    
    You may use arbitrary python expressions in the command line
    parameters; all the symbols in the math module are available.
    You can also use numpy expressions; numpy is in the global
    namespace with the name np.
    
    Options:
        -0      Use 0-based arrays for output.
        -1      Use 1-based arrays for output [default].
    
        -E N    Return n times the IEC 60063 numbers (i.e., the "E"
                series).  m and inc are ignored.  N must be 6, 12, 24,
                48, 96, or 192.
        -F D    Convert the output to a fraction.  The denominator of
                all the fractions will be <= D.  We must have D >= 0.
                If D is 0, then a full-precision fraction is
                generated.
                greater than 0.
        -I      Force all numbers output to be converted to integers;
                the integer will be the integer closest to the number
                (only applies to n m inc functionality).
        -L      Logarithmically increment between n and m where inc is
                the natural logarithm increment.
        -R N    Return n times the Renard series numbers; m and
                inc are ignored.  For a standard Renard series, N must be
                one of 5, 10, 20, 40, or 80; however, the script will
                accept any series number greater than 1.  If the series
                number is not standard, a warning message is printed to
                stderr.
        -S      Sort the output random number array.
        -X f    Specify a function f that is used to transform the
                output.  The difference from the -x option is that f
                is capable of operating on the whole array at once
                (e.g., it is a numpy ufunc).
        -c      For the random number distributions, return the CDF.
                See above for how to specify parameters.
        -d D    For floating point, set the number of significant
                digits to D.  The default is set such that there's
                enough resolution to see the differences between the
                numbers.
        -e eps  eps is a relative difference used to determine when a
                floating point number should be expressed as an
                integer (only works with -i option).  [default = {eps}]
        -f      Convert all output to floating point.
        -g      Generate a geometric series starting from n and going
                to m with ratio inc.  Thus, the series is m, m*inc,
                m*inc^2, ... until the absolute value of the result is
                greater than m (this allows inc to be negative).  The
                default number of figures is controlled by the number
                of significant figures in inc.
        -i      Display the numbers as integers if possible (only applies
                to n m inc functionality).
        -l      Logarithmically increase between n and m where inc is the
                base 10 logarithm increment.
        -m      If the -F option is used, convert improper fractions
                to mixed fractions.
        -o x    Set the output field separator (defaults to '{sep}').
                Note this only applies when the -t option is used.
        -p      For the random number distributions, return the CDF.
                See above for how to specify parameters.
        -s x    Seed the random number generator with a string x.
        -t      Output the transpose.  Normally, one number is printed per
                line; using -t lets you get all the output on one line.
        -x f    Specify a function f(x) that is used to transform the
                output.
    
     Examples
        1.  Generate the numbers from 1 to 10:
                python {name} 10
        2.  Generate from 0 to 10*pi by steps of pi/2:
                python {name} 0 10*pi pi/2
        3.  Generate the 16ths of an inch to four significant figures
                python {name} -d 4 0 1 1/16
        4.  From a population of 100 integers, randomly select without
            replacement a sample of 10:
                python {name} wor 100 10
        5.  Generate from arcsin(0.2) in degrees to 90 degrees in steps of
            5.5 degrees; output to 5 significant figures:
                python {name} -d 5 "asin(0.2)*180/pi" 90 5.5

    """)
    )
    if bye is not None:
        exit(bye)


def ParseCommandLine(d):
    d["mixed"] = "+"  # Separates mixed fraction components
    d["-0"] = False  # Used 0-based arrays

    d["-D"] = None  # Calculate nth difference for output
    d["-E"] = None  # Output in E series ratios
    d["-F"] = None  # Output in fractions; value is largest denom
    d["-I"] = False  # Force output to integer values
    d["-L"] = False  # Output in loge ratios
    d["-R"] = None  # Output using Renard numbers ratios
    d["-S"] = False  # Sort output array for wr
    d["-T"] = False  # Run self-tests
    d["-X"] = None  # Output array transformation function

    d["-c"] = False  # Calculate CDF
    d["-d"] = None  # Digits in output or fmt str (None => figure out)
    d["-e"] = 1e-14  # Rel diff to determine when float == integer
    d["-f"] = False  # Convert output to float
    d["-g"] = False  # Geometric series
    d["-i"] = False  # Display as integer if possible
    d["-l"] = False  # Output in log10 ratios
    d["-m"] = False  # Convert improper to mixed fractions
    d["-o"] = _sep  # Output separator string
    d["-p"] = False  # Calculate PDF
    d["-s"] = None  # Seed RNG; None means system clock
    d["-t"] = False  # Output the transpose
    d["-x"] = None  # Output transformation function
    if len(sys.argv) < 2:
        Usage(status=1)
    try:
        optletters = "01"
        optletters += "D:E:F:ILR:STX:"
        optletters += "cd:e:fghilmo:ps:tx:"
        optlist, args = getopt.getopt(sys.argv[1:], optletters)
    except getopt.GetoptError as str:
        msg, option = str
        Error(msg)
    for opt in optlist:
        if opt[0] == "-0":
            d["-0"] = True
        if opt[0] == "-1":
            d["-0"] = False

        # Upper-case option letters
        if opt[0] == "-D":
            try:
                d["-D"] = int(opt[1])
            except ValueError:
                Error("'%s' is a bad integer for -D option" % opt[1])
            if d["-D"] < 0:
                Error("-D option's number must be integer >= 0")
        if opt[0] == "-E":
            try:
                d["-E"] = int(opt[1])
            except ValueError:
                Error("'%s' is a bad integer for -E option" % opt[1])
            if d["-E"] not in (6, 12, 24, 48, 96, 192):
                Error("E series number must be 6, 12, 24, 48, 96, or 192")
        if opt[0] == "-F":
            msg = "'%s' is a bad integer for -F option" % opt[1]
            try:
                d["-F"] = int(opt[1])
            except ValueError:
                Error(msg)
            if d["-F"] < 0:
                Error(msg)
        if opt[0] == "-I":
            d["-I"] = not d["-I"]
        if opt[0] == "-L":
            d["-L"] = not d["-L"]
        if opt[0] == "-R":
            try:
                d["-R"] = int(opt[1])
            except ValueError:
                Error("'%s' is a bad integer for -R option" % opt[1])
            if d["-R"] not in (5, 10, 20, 40, 80):
                if d["-R"] < 2:
                    Error("'%s' is a bad integer for -R option" % opt[1])
                msg = (
                    "Warning:  Renard series with non-standard series "
                    "number %d\n" % d["-R"]
                )
                _err(msg)
                factor = 10 ** (1 / float(d["-R"]))
                msg = "          (The geometric series factor is %s)\n" % _sig(
                    factor, 6
                )
                _err(msg)
        if opt[0] == "-S":
            d["-S"] = not d["-S"]
        if opt[0] == "-T":
            d["-T"] = not d["-T"]
        if opt[0] == "-X":
            d["-X"] = opt[1]

        # Lower-case option letters
        if opt[0] == "-c":
            d["-c"] = not d["-c"]
            if not _have_scipy:
                Error("Need scipy to calculate CDFs")
        if opt[0] == "-d":
            try:
                digits = int(opt[1])
            except ValueError:
                # OK, it must be a format string
                d["-d"] = opt[1]
            else:
                if digits < 1:
                    Error("-d option must be > 0")
                d["-d"] = digits
        if opt[0] == "-e":
            try:
                d["-e"] = abs(float(opt[1]))
            except ValueError:
                Error("'%s' is a bad number for -e option" % opt[1])
        if opt[0] == "-f":
            d["-f"] = not d["-f"]
        if opt[0] == "-g":
            d["-g"] = not d["-g"]
        if opt[0] == "-h":
            Manpage(d, bye=0)
        if opt[0] == "-i":
            d["-i"] = not d["-i"]
        if opt[0] == "-l":
            d["-l"] = not d["-l"]
        if opt[0] == "-m":
            d["-m"] = not d["-m"]
        if opt[0] == "-o":
            d["-o"] = opt[1].decode("string_escape")
        if opt[0] == "-p":
            d["-p"] = not d["-p"]
            if not _have_scipy:
                Error("Need scipy to calculate PDFs")
        if opt[0] == "-s":
            d["-s"] = opt[1]
        if opt[0] == "-t":
            d["-t"] = not d["-t"]
        if opt[0] == "-x":
            d["-x"] = opt[1]
    if not d["-T"] and len(args) == 0:
        Usage()
    return args


def Error(msg):
    _err(msg + _nl)
    exit(1)


def Usage(status=1):
    name = os.path.split(sys.argv[0])[1]
    basic = _basic
    _out(
        dedent(f"""
    Usage:  {name} [options] n [m [inc]]
      Output a sequence of numbers from n to m inclusive in steps of
      inc.  For just n, output from 1 to n by 1.  For n to m, output
      n to m by 1.  n, m, and inc can be integers, floats, fractions
      or python expressions.  The absolute value of inc will be taken
      unless the -g option is used.
     
      The script is also capable of generating sequences of random
      numbers, samples with and without replacement, permutations of
      a set of integers, IEC "E series", Renard numbers, geometric
      progressions, and numbers in specified logarithmic ratios.  Use
      the -h option for a man page.\n""")
    )
    exit(status)


def Convert(s):
    s = s.replace("\n", "")
    s = [int(i) for i in s.split()]
    s.sort()
    return np.array(s)


def E(series):
    """Return numpy array values that are the IEC 60063 numbers.
    Reference: http://en.wikipedia.org/wiki/Preferred_value#E_series

    series should be an integer:  6, 12, 24, 48, 96, or 192.  If you
    give a bad integer, None is returned.
    """
    d = {
        6: Convert("""100 150 220 330 470 680 1000"""),
        12: Convert("""100 120 150 180 220 270 330 390 470 560 680 820
                       1000"""),
        24: Convert("""100 110 120 130 150 160 180 200 220 240 270 300
                       330 360 390 430 470 510 560 620 680 750 820 910
                       1000"""),
        48: Convert("""100 105 110 115 121 127 133 140 147 154 162 169
                       178 187 196 205 215 226 237 249 261 274 287 301
                       316 332 348 365 383 402 422 442 464 487 511 536
                       562 590 619 649 681 715 750 787 825 866 909 953
                       1000"""),
        96: Convert("""100 102 105 107 110 113 115 118 121 124 127 130
                       133 137 140 143 147 150 154 158 162 165 169 174
                       178 182 187 191 196 200 205 210 215 221 226 232
                       237 243 249 255 261 267 274 280 287 294 301 309
                       316 324 332 340 348 357 365 374 383 392 402 412
                       422 432 442 453 464 475 487 499 511 523 536 549
                       562 576 590 604 619 634 649 665 681 698 715 732
                       750 768 787 806 825 845 866 887 909 931 953 976
                       1000"""),
        192: Convert("""100 101 102 104 105 106 107 109 110 111 113 114
                        115 117 118 120 121 123 124 126 127 129 130 132
                        133 135 137 138 140 142 143 145 147 149 150 152
                        154 156 158 160 162 164 165 167 169 172 174 176
                        178 180 182 184 187 189 191 193 196 198 200 203
                        205 208 210 213 215 218 221 223 226 229 232 234
                        237 240 243 246 249 252 255 258 261 264 267 271
                        274 277 280 284 287 291 294 298 301 305 309 312
                        316 320 324 328 332 336 340 344 348 352 357 361
                        365 370 374 379 383 388 392 397 402 407 412 417
                        422 427 432 437 442 448 453 459 464 470 475 481
                        487 493 499 505 511 517 523 530 536 542 549 556
                        562 569 576 583 590 597 604 612 619 626 634 642
                        649 657 665 673 681 690 698 706 715 723 732 741
                        750 759 768 777 787 796 806 816 825 835 845 856
                        866 876 887 898 909 920 931 942 953 965 976 988
                        1000"""),
    }
    if series not in d:
        return None
    s = d[series].astype(float)
    s /= s[0]  # Normalize
    return s


def Renard(series):
    """Returns a sequence of Renard numbers (see
    http://en.wikipedia.org/wiki/Preferred_value#Renard_numbers).
    Note:  the series number is allowed to be any positive integer greater
    than 1, although a warning message is printed to stderr when the series
    number isn't in the dictionary d.

    For another listing, see page 689 of Machinery's Handbook, 27th
    edition, 2004.
    """
    d = {
        5: Convert("""10   16  25  40  63 100"""),
        10: Convert("""100 125 160 200 250 315 400 500 630 800 1000"""),
        20: Convert("""100 112 125 140 160 180 200 224 250 280
                       315 355 400 450 500 560 630 710 800 900
                       1000"""),
        40: Convert("""100 106 112 118 125 132 140 150 160 170
                       180 190 200 212 224 236 250 265 280 300
                       315 335 355 375 400 425 450 475 500 530
                       560 600 630 670 710 750 800 850 900 950
                       1000"""),
        80: Convert("""100 103 106 109 112 115 118 122 125 128
                       132 136 140 145 150 155 160 165 170 175
                       180 185 190 195 200 206 212 218 224 230
                       236 243 250 258 265 272 280 290 300 307
                       315 325 335 345 355 365 375 387 400 412
                       425 437 450 462 475 487 500 515 530 545
                       560 580 600 615 630 650 670 690 710 730
                       750 775 800 825 850 875 900 925 950 975
                       1000"""),
    }
    if series not in d:
        # We'll allow non-standard Renard series, as they can be calculated
        # from the formula 10**(i/N) where i goes from 0 to N in steps of
        # 1.
        if not isinstance(series, int):
            raise ValueError("Renard series number must be an integer")
        if series < 2:
            raise ValueError("Renard series number must be > 1")
        s = np.arange(0, series + 1, 1) / series
        return 10**s
    s = d[series].astype(float)
    s /= s[0]  # Normalize
    return s


def GetInt(x, msg, minimum=None, minimum_ge=None):
    """x should be convertible to an integer.  If minimum is not None,
    then x must be > minimum.  If not, print the error message in
    msg.  minimum_ge is the same as minimum by the comparison is >=.

    Note we round to the nearest integer
    """
    if isinstance(x, str):
        # This gets rid of annoying things like appended carriage
        # returns.
        x = x.strip()
    try:
        y = int(eval(x) + 0.5)
        if minimum is not None and y <= minimum:
            raise Exception
        if minimum_ge is not None and y < minimum_ge:
            raise Exception
        return y
    except Exception:
        Error(msg)


def GetFloat(x, msg, minimum=None, minimum_ge=None, maximum=None, maximum_le=None):
    """x should be convertible to a float.  If minimum is not None,
    then x must be > minimum.  If maximum is not None, then x must be
    < maximum.  For *_ge or *_le, the = sign is added to the
    comparison.  Print error message msg otherwise.
    """
    if isinstance(x, str):
        # This gets rid of annoying things like appended carriage
        # returns.
        x = x.strip()
    try:
        y = float(eval(x))
        if minimum is not None and y <= minimum:
            raise Exception
        if minimum_ge is not None and y < minimum_ge:
            raise Exception
        if maximum is not None and y >= maximum:
            raise Exception
        if maximum_le is not None and y > maximum_le:
            raise Exception
        return y
    except Exception:
        Error(msg)


def PrintArray(y, d, test=False):
    """The difference between the -X option and the -x option is
    that -X applies to the whole array at once; therefore it must
    be a vectorized function.  -x applies to each element and can
    contain e.g. math module functions.  If test is True, then
    return a list with the formatted array.

    Note that the -x transformation is applied before the -X
    transformation.
    """
    assert isinstance(y, np.ndarray)
    # Get math module's symbols into local namespace for the -x
    # option evaluations.
    for i in [i for i in math.__dict__ if i[0] != "_"]:
        exec("from math import %s" % i)
    if 0:
        _out("Dump of d:" + _nl)
        k = d.keys()
        k.sort()
        for i in k:
            _out("  " + i + "    " + repr(d[i]) + _nl)
    if d["-x"]:  # Transform each component separately
        for i, x in enumerate(y):
            try:
                x1 = eval(d["-x"])
                if isinstance(x1, float):
                    y = y.astype(float)
                y[i] = x1
            except Exception:
                try:
                    y[i] = np.nan
                except ValueError:
                    y = y.astype(float)
                    y[i] = np.nan
    if d["-X"]:  # Transform the whole array at once
        x = y
        y = eval(d["-X"])
    if d["-D"]:  # Calculate diffs
        for i in range(d["-D"]):
            y = np.diff(y)
    if d["-S"]:  # Sort output
        y.sort()
    # T is made True if we must print out in floating point, even
    # if the array is made of integers.
    T = (d["-f"]) or (isinstance(d["-d"], str))
    if y.dtype == np.int32 and not T:  # Integer array
        s = [str(i) for i in y]
    else:
        # In the following loop, the order of checking the
        # options is important.  For example, if you give the -i
        # and -f options on the command line, the -i option is
        # seen first and is thus processed.
        s = []
        for x in y:
            try:
                if d["-F"] is not None:  # Output as fraction
                    f = fractions.Fraction(str(x))
                    if d["-F"]:
                        # Denominator is limited
                        f = f.limit_denominator(d["-F"])
                    else:
                        # Full precision
                        f = f.from_float(x)
                    if d["-m"]:  # Allow mixed fraction
                        N, D = f.numerator, f.denominator
                        i, r = divmod(N, D)
                        if r:
                            f = "%d%s%d/%d" % (i, d["mixed"], r, D)
                        else:
                            f = str(i)
                    s.append(str(f))
                elif d["-I"]:  # Force to an integer
                    s.append(str(int(x + 0.5)))
                elif d["-i"]:  # Display as integer if possible
                    if int(x) == x:
                        s.append(str(int(x)))
                    else:
                        diff = abs(x - int(x + 0.5))
                        reldiff = diff / abs(x) if x else 1
                        if reldiff <= d["-e"]:
                            s.append(str(int(x + 0.5)))
                        else:
                            s.append(FormatFloat(x, d))
                elif isinstance(d["-d"], str):
                    s.append(d["-d"] % x)
                elif d["-f"]:
                    s.append(FormatFloat(x, d))
                else:  # Default behavior
                    if x == int(x):  # Display as integer if possible
                        s.append(str(int(x)))
                    else:  # Normal float display
                        s.append(FormatFloat(x, d))
            except ValueError:
                s.append("nan")
    if test:
        if d["-t"]:
            return d["-o"].join(s)
        else:
            return _nl.join(s) + _nl
    else:
        if d["-t"]:
            _out(d["-o"].join(s) + _nl)
        else:
            _out(_nl.join(s) + _nl)


def FormatFloat(x, d):
    """Format the float x with d["-d"].  This is either an
    integer for the number of significant figures or a format
    string.
    """
    s = d["-d"]
    if s is not None:
        if isinstance(s, str):  # It's a format string
            return s % x
        else:  # Use _sig()
            assert isinstance(s, int)
            return _sig(x, s)
    else:
        return _sig(x)  # Default _sig()


def GetNumber(s, d):
    """s can be an expression.  Evaluate it and get a float.  If
    it can be exactly expressed as an integer, then do so.
    """
    # Get math module's symbols into local namespace
    # option evaluations.
    for i in [i for i in math.__dict__ if i[0] != "_"]:
        exec("from math import %s" % i)
    x = s  # Expressions must have independent variable named 'x'
    y = float(eval(s))
    i = int(y)
    return i if i == y else y


def RandomNumbers(cmd, args, d):
    n = GetInt(args[0], "n must be an integer > 0", minimum=1)
    start = 0 if d["-0"] else 1
    end = n if d["-0"] else n + 1
    if cmd == "binomial":
        if len(args) != 3:
            Error("binomial uses 3 arguments")
        N = GetInt(args[1], "N must be an integer >= 1", minimum_ge=1)
        p = GetFloat(
            args[2],
            "p must be a float such that 0 <= p <= 1",
            minimum_ge=0,
            maximum_le=1,
        )
        PrintArray(npr.binomial(N, p, n), d)
    elif cmd == "hypergeometric":
        if len(args) != 4:
            Error("hypergeometric uses 4 arguments")
        # Total number of items in the population
        N = GetInt(args[1], "N must be an integer >= 1", minimum_ge=1)
        # Fraction of items with desired characteristic
        p = GetFloat(
            args[2],
            "p must be a float such that 0 <= p <= 1",
            minimum_ge=0,
            maximum_le=1,
        )
        # Size of sample drawn
        m = GetInt(args[3], "m must be an integer >= 1", minimum_ge=1)
        M = int(p * N + 0.5)  # Round to nearest integer
        if m > N:
            Error("We must have m <= N")
        PrintArray(npr.hypergeometric(N - M, M, m, n), d)
    elif cmd == "exponential":
        if len(args) != 2:
            Error("exponential uses 2 arguments")
        mu = GetFloat(args[1], "mu must be a float >= 0", minimum_ge=0)
        PrintArray(npr.exponential(mu, n), d)
    elif cmd == "normal":
        if not (1 <= len(args) <= 3):
            Error("normal uses 1 to 3 arguments")
        mu, sigma = 0, 1
        if len(args) == 2:
            mu = GetFloat(args[1], "mu must be a float > 0", minimum=0)
        elif len(args) == 3:
            mu = GetFloat(args[1], "mu must be a float > 0", minimum=0)
            sigma = GetFloat(args[2], "sigma must be a float > 0", minimum=0)
        PrintArray(npr.normal(mu, sigma, n), d)
    elif cmd == "poisson":
        if len(args) != 2:
            Error("poisson uses 2 arguments")
        mu = GetFloat(args[1], "mu must be a float > 0", minimum=0)
        PrintArray(npr.poisson(mu, n).astype(int), d)
    elif cmd == "randint":
        if len(args) != 3:
            Error("randint uses 2 arguments")
        a = GetInt(args[1], "a must be an integer")
        b = GetInt(args[2], "b must be an integer")
        PrintArray(npr.randint(a, b + 1, n), d)
    elif cmd == "shuffle":
        if len(args) != 1:
            Error("shuffle uses 1 argument")
        x = np.arange(start, end).astype(int)
        npr.shuffle(x)
        PrintArray(x.astype(int), d)
    elif cmd == "uniform":
        if len(args) != 3:
            Error("uniform uses 3 arguments")
        a = GetFloat(args[1], "a must be a float")
        b = GetFloat(args[2], "b must be a float")
        PrintArray(npr.uniform(a, b, n), d)
    elif cmd == "wor":
        if len(args) != 2:
            Error("wor uses 2 arguments")
        m = GetInt(args[1], "m must be an integer > 0", minimum=1)
        if m > n:
            Error("wor must have m <= n")
        x = np.arange(start, end).astype(int)
        s = np.array(random.sample(set(x), m)).astype(int)
        PrintArray(s, d)
    elif cmd == "wr":
        if len(args) != 2:
            Error("wr uses 2 arguments")
        m = GetInt(args[1], "m must be an integer > 0", minimum=1)
        x = np.arange(start, end).astype(int)
        s = []
        for i in range(m):
            s.append(random.choice(x))
        s = np.array(s).astype(int)
        PrintArray(s, d)
    else:
        raise RuntimeError("Bug in program:  '%s' is bad command" % cmd)


def CDFs(cmd, args, d):
    if cmd == "binomial":
        if len(args) < 3:
            Error("binomial CDF uses 3 or more arguments")
        n = GetInt(args[0], "n must be an integer >= 1", minimum_ge=1)
        p = GetFloat(
            args[1],
            "p must be a float such that 0 <= p <= 1",
            minimum_ge=0,
            maximum_le=1,
        )
        x = []
        for i in args[2:]:
            num = GetInt(i, "x must be an integer >= 0", minimum_ge=0)
            x.append(num)
        x = np.array(x)
        rv = binom(n, p)  # Frozen distribution
        if d["-c"]:
            PrintArray(rv.cdf(x), d)
        else:
            PrintArray(rv.pmf(x), d)
    elif cmd == "hypergeometric":
        if len(args) < 4:
            Error("hypergeometric CDF uses 4 or more arguments")
        N = GetInt(args[0], "n must be an integer >= 1", minimum_ge=1)
        p = GetFloat(
            args[1],
            "p must be a float such that 0 <= p <= 1",
            minimum_ge=0,
            maximum_le=1,
        )
        M = int(N * p + 1 / 2)
        m = GetInt(args[2], "m must be an integer >= 1", minimum_ge=1)
        if m > N:
            Error("m must be <= N")
        x = []
        for i in args[3:]:
            num = GetInt(i, "x must be an integer >= 0", minimum_ge=0)
            x.append(num)
        x = np.array(x)
        rv = hypergeom(N, M, m)  # Frozen distribution
        if d["-c"]:
            PrintArray(rv.cdf(x), d)
        else:
            PrintArray(rv.pmf(x), d)
    elif cmd == "exponential":
        if len(args) < 2:
            Error("exponential CDF uses 2 or more arguments")
        mu = GetFloat(args[0], "mu must be a float > 0", minimum=0)
        x = []
        for i in args[1:]:
            num = GetFloat(i, "x must be a float >= 0", minimum_ge=0)
            x.append(num)
        x = np.array(x)
        rv = expon(mu, loc=0)  # Frozen distribution
        if d["-c"]:
            PrintArray(rv.cdf(x), d)
        else:
            PrintArray(rv.pdf(x), d)
    elif cmd == "normal":
        mu, s = 0, 1
        if len(args) < 1:
            Error("hypergeometric CDF uses at least one argument")
        if ":" in args[0]:
            # Contains mu:s
            try:
                mu, s = [float(i) for i in args[0].strip().split(":")]
            except ValueError:
                Error("Bad mu or s for normal CDF")
            if s <= 0:
                Error("Bad standard deviation for normal CDF")
            del args[0]
        x = []
        for i in args:
            num = GetFloat(i, "x must be a float")
            x.append(num)
        x = np.array(x)
        rv = norm(mu, s)  # Frozen distribution
        if d["-c"]:
            PrintArray(rv.cdf(x), d)
        else:
            PrintArray(rv.pdf(x), d)
    elif cmd == "poisson":
        if len(args) < 2:
            Error("poisson CDF uses 2 or more arguments")
        mu = GetFloat(args[0], "mu must be a float > 0", minimum=0)
        x = []
        for i in args[1:]:
            num = GetInt(i, "x must be an integer >= 0", minimum_ge=0)
            x.append(num)
        x = np.array(x)
        assert x.dtype == np.int32
        rv = poisson(mu)  # Frozen distribution
        if d["-c"]:
            PrintArray(rv.cdf(x), d)
        else:
            PrintArray(rv.pmf(x), d)


def Sequence(args, d):
    # Get math module's symbols into local namespace
    for i in [i for i in math.__dict__ if i[0] != "_"]:
        exec("from math import %s" % i)
    n, inc, y = 1, 1, []
    m = GetNumber(args[0], d)
    if len(args) == 1:
        pass
    elif len(args) in (1, 2):
        n = GetNumber(args[0], d)
        m = GetNumber(args[1], d)
    elif len(args) == 3:
        n = GetNumber(args[0], d)
        m = GetNumber(args[1], d)
        if d["-g"]:
            inc = GetNumber(args[2], d)
        else:
            inc = abs(GetNumber(args[2], d))
    else:
        Error("Need 1 to 3 arguments for a numerical sequence")
    # Get number of significant figures to use if it's not set
    if d["-d"] is None and not (d["-R"] or d["-E"] or d["-g"]):
        delta = abs(math.log10(max(abs(n), abs(m)) / abs(inc)))
        T = int(delta) != delta
        digits = math.ceil(delta) if T else math.ceil(delta) + 1
        if delta < 1:
            digits += 1
        d["-d"] = int(digits)
    if d["-R"]:
        if d["-R"] not in (5, 10, 20, 40, 80):
            digits = 3 if d["-R"] < 10 else int(np.log10(d["-R"]) + 1)
    if n == m and not (d["-R"] or d["-E"]):
        Error("n and m cannot be equal")
    # OK, generate sequence
    if d["-E"]:
        # E series
        E = E(d["-E"])
        if d["-d"] is None:
            d["-d"] = 3
        for e in E:
            y.append(e * m)
    elif d["-R"]:
        # Renard numbers
        R = Renard(d["-R"])
        if d["-d"] is None:
            d["-d"] = 3
        for r in R:
            y.append(r * m)
    elif d["-g"]:
        # Geometric series.  We need to decide on the number of
        # significant figures if this isn't defined.  To do this,
        # count the digits in the significand of inc.
        if d["-d"] is None:
            s = args[2]
            if "e" in s:
                s = s.split("e")[0]
            if "E" in s:
                s = s.split("E")[0]
            s = s.replace(".", "").replace("-", "").replace("+", "")
            # Now s should be only the significand's digits
            d["-d"] = len(s)
        if inc == 1:
            Error("inc can't be 1 for a geometric series")
        if n < m:
            if abs(inc) < 1:
                Error("inc < 1; series won't terminate")
            while abs(n) <= abs(m):
                y.append(n)
                n *= inc
        else:
            if abs(inc) >= 1:
                Error("inc >= 1; series won't terminate")
            while abs(n) >= abs(m):
                y.append(n)
                n *= inc
    elif d["-l"]:
        # Output in base 10 logarithmic ratio as determined by inc
        try:
            start = log10(n)
        except ValueError:
            Error("Bad value for n (can't take logarithm)")
        try:
            stop = log10(m)
        except ValueError:
            Error("Bad value for m (can't take logarithm)")
        if n < m:
            while start <= stop:
                y.append(10**start)
                start += inc
        else:
            while start >= stop:
                y.append(10**start)
                start -= inc
    elif d["-L"]:
        # Output in base e logarithmic ratio as determined by inc
        try:
            start = log(n)
        except ValueError:
            Error("Bad value for n (can't take logarithm)")
        try:
            stop = log(m)
        except ValueError:
            Error("Bad value for m (can't take logarithm)")
        if n < m:
            while start <= stop:
                y.append(e**start)
                start += inc
        else:
            while start >= stop:
                y.append(e**start)
                start -= inc
    else:
        if n < m:
            while n <= m:
                y.append(n)
                n += inc
        else:
            while n >= m:
                y.append(n)
                n -= inc
    y = np.array(y)
    PrintArray(y, d)


if __name__ == "__main__":
    d = {}  # Hold options & globally-needed stuff
    d["decode"] = CommandDecode(
        set(
            (
                "binomial",
                "exponential",
                "hypergeometric",
                "normal",
                "poisson",
                "randint",
                "shuffle",
                "uniform",
                "wor",
                "wr",
            )
        ),
        ignore_case=True,
    )
    args = ParseCommandLine(d)
    # Set up seeds
    if d["-s"] is not None:
        sd = abs(hash(d["-s"]))
        npr.seed(sd)
        random.seed(sd)
    # Try to decode the first argument as one of our allowed commands.
    # If it decodes OK, then use RandomNumbers().
    cmd = d["decode"](args[0])
    if len(cmd) > 1:
        msg = "'%s' is an ambiguous command; it could be:\n  " % args[0]
        s = str(cmd).replace("[", "").replace("]", "").replace(",", "")
        Error(msg + s)
    elif len(cmd) == 1:
        if len(args) < 2:
            Error("Need at least 2 arguments after the command")
        if d["-c"] or d["-p"]:
            CDFs(cmd[0], args[1:], d)
        else:
            RandomNumbers(cmd[0], args[1:], d)
    else:
        Sequence(args, d)

"""
Uses mpmath and sympy to try to identify a real number
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Uses mpmath and sympy to try to identify a real number
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from fractions import Fraction
    from time import strftime
    from pdb import set_trace as xx
if 1:  # Custom imports
    from sympy import sympify
    from wrap import dedent
    from sig import sig, SigFig
    from mpmath import *
    from columnize import Columnize


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] num1 [num2...]
      Try to identify the real numbers given on the command line.  If an argument is 'h', the
      history of the commands that resulted in output are printed to stdout.  Because arguments
      are evaluated, you can also use this script to perform special function evaluations.
    Options
      -d n  Set the number of significant digits to display.  The default is {d["-d"]}.
      -e    Include e in the output expression(s)
      -f    List available function names
      -P n  Find a polynomial of degree n with the given number as a root
      -p    Include pi in the output expression(s).
      -r d  Include a rational approximation to the number with a maximum indicated denominator d
      -s s  Include the sequence s of other expressions.  For example, if you think the square
            root of 33 might be in the number, include -s ['sqrt(33)'] on the command line.
      -S    Don't use sympy for simplification
      -u c  Use char c for the variable and Unicode when printing the polynomial found with the
            -P option.  Use %alp for lowercase Greek alpha, %Alp for uppercase, etc.
    """)
    )
    exit(0)


def Functions(*p):
    """If p is empty, print out a list of available function names.
    Otherwise, list syntax for each non-obvious function.
    """
    if p:
        xx()
    else:
        f = """
            acos acosh asin asinh atan atan2 atanh bei ber bernoulli besseli
            besselj besselk bessely beta betainc binomial cbrt chebyfit
            chebyt chebyu chi ci cos cosh degrees diff diffs digamma ei
            ellipe ellipf ellipfun ellipk ellippi erf erfc eulernum exp fac
            factorial fib fibonacci fourier fourierval gamma gammainc
            hermite hyp0f1 hyp1f1 hyp1f2 hyp2f0 hyp2f1 hyper hypot jtheta
            kei ker laguerre legendre legenp legenq li limit ln log log10
            loggamma ncdf npdf nprod nsum pade polyroots polyval power psi
            quad radians root shi si sin sinc sinh spherharm sqrt stirling1
            stirling2 sumem tan tanh taylor zeta zetazero
    """
        f = f.replace("\n", " ").split()
        for i in Columnize(f):
            print(i)
    exit(0)


def ParseCommandLine(d):
    d["-P"] = None  # Find polynomial of indicated degree
    d["-d"] = 15  # Number of significant digits
    d["-e"] = False  # Include e
    d["-f"] = False  # Function listing
    d["-r"] = None  # Maximum fraction denominator
    d["-p"] = False  # Include pi
    d["-s"] = None  # Include a sequence of things
    d["-S"] = True  # Use sympy
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:efP:pr:s:S")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-P",):
            try:
                d["-P"] = int(a)
                if d["-P"] < 1:
                    raise ValueError()
            except ValueError:
                msg = "-P option's argument must be an integer > 0"
                Error(msg)
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if d["-d"] < 1:
                    raise ValueError()
            except ValueError:
                msg = "-d option's argument must be an integer > 0"
                Error(msg)
        elif o in ("-f",):
            d["-f"] = not d["-f"]
        elif o in ("-e",):
            d["-e"] = not d["-e"]
        elif o in ("-p",):
            d["-p"] = not d["-p"]
        elif o in ("-r",):
            try:
                d["-r"] = int(a)
                if d["-r"] < 1:
                    raise ValueError()
            except ValueError:
                Error("Denominator must be an integer > 0")
        elif o in ("-S",):
            d["-S"] = not d["-S"]
    if d["-f"]:
        Functions(*args)
    if not args:
        Usage(d)
    return args


def FindPolynomial(x, d):
    """Print out the polynomial of degree d["-d"] which has x as a root."""
    p = findpoly(x, d["-P"], maxcoeff=100000)
    if p is None:
        print("   No polynomial found")
        return
    else:
        print("   Polynomial(deg={}) =".format(len(p) - 1), p)
        print("       (last element is the constant)")
        print("       Roots of polynomial:")
        for r in polyroots(p):
            s = " "
            if isinstance(r, mpf) and r < 0:
                s = ""
            elif isinstance(r, mpc) and r.real < 0:
                s = ""
            print(" " * 10, s, sig(r, d["-d"]), sep="")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    cmdline = " ".join(sys.argv[1:])
    mp.dps = d["-d"]
    sig.imag_pre = " "
    sig.imag_post = " "
    for arg in args:
        if arg.lower() == "h":
            print("History of commands:")
            ofp = open("/pylib/pgm/real.history", "r")
            for i in ofp.readlines():
                print("  ", i, end="")
            ofp.close()
        else:
            try:
                x = eval(arg)
                if isinstance(x, Fraction):
                    x = float(x)
                print(arg, end=" ")
                if str(x) != arg:
                    print("= {}".format(str(x)))
                else:
                    print()
                extra = []
                if d["-p"]:
                    extra.append("pi")
                if d["-e"]:
                    extra.append("e")
                if d["-s"] is not None:
                    extra.append(d["-s"])
                # Print mpmath's/sympy's guess
                if d["-S"]:
                    s = sympify(identify(x, extra))
                else:
                    s = identify(x, extra)
                print("  ", s)
                # Print rational approximation if needed
                if d["-r"] is not None:
                    f = Fraction(str(x)).limit_denominator(d["-r"])
                    sigfig = SigFig()
                    sigfig.low = 1e-8
                    sigfig.digits = 1
                    pct = 100 * (float(f) - x) / x
                    print(
                        "   Rational approximation = {}/{} [{}%]".format(
                            f.numerator, f.denominator, sigfig(pct)
                        )
                    )
                # Find polynomial if indicated
                if d["-P"] is not None:
                    FindPolynomial(x, d)
                # Log to history file
                t = strftime("%d%b%Y %I:%M:%S %p")
                t = t.replace("PM", "pm").replace("AM", "am")
                s = ["'{}'".format(cmdline), "[{}]".format(t), "\n"]
                ofp = open("/pylib/pgm/real.history", "a")
                ofp.write(" ".join(s))
                ofp.close()
            except RuntimeError:  # Exception
                print("'{}' couldn't be evaluated".format(arg), file=sys.stderr)
"""
Note the following example leads to different results, even though the
expressions are the same (the first gives the second expression):
 
1.  Command line is:  -p -P 5 'sqrt(3) - sqrt(2)', which gives
        sqrt(3) - sqrt(2) = 0.317837245195782
           sqrt(-2*sqrt(6) + 5)
           Polynomial(deg=3) = [1320, 3249, 813, -629]
               (last element is the constant)
               Roots of polynomial:
                  -2.04667482170286
                  -0.732526059856562
                   0.317837245195782
2.  Command line is:  -p -P 5 'sqrt(-2*sqrt(6) + 5)', which gives
        sqrt(5 - 2*sqrt(6)) = 0.317837245195783
           sqrt(-2*sqrt(6) + 5)
           Polynomial(deg=3) = [-691, -1929, -3854, 1442]
               (last element is the constant)
               Roots of polynomial:
                   0.317837245195783
                  (-1.5547218063895 + 2.03680168889097j)
                  (-1.5547218063895 - 2.03680168889097j)
Note the expressions in single quotes are identical, but their printed
numerical values differ.  However, repeating with the addition of '-d
20' gives identical numerical results for the evaluation, but the
polynomials are still different.
"""

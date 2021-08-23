'''
Given a string of digits 0-9, this routine searches for them in the
square roots of the integers.  If you have the mpmath library, you'll
find it runs 5 to 6 times faster than python's decimal module.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2009 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Find a string of digits in square roots of integers
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import decimal
    import getopt
    import re
    import sys
    import time
    from sys import argv
if 1:   # Custom imports
    import color as C
    from wrap import dedent
    try:
        import mpmath as mp
        use_mpmath = True
    except ImportError:
        use_mpmath = False
class CalculationDone(Exception):
    pass
def CheckNumber(n, root, want, d):
    '''Look for the string of digits (in variable want) in the number
    n**(1/root).  If found, print out the square root with a space before
    the location of the number.  Return True if it is found.
    '''
    if use_mpmath:
        num = mp.mpf(n)**(1/mp.mpf(root))
    else:
        num = decimal.Decimal(n)**(1/decimal.Decimal(root))
    s = str(num)
    pos = s.find(want)
    if pos != -1:
        print(f"1/{root} root of {n}")
        print(f"Found '{want}' at location {pos}")
        if d["-c"]:
            print(s[:pos], end="")
            C.fg(C.lred)
            end = pos + len(want)
            print(s[pos:end], end="")
            C.normal()
            print(s[end:])
        else:
            print(s[:pos] + " " + s[pos:])
        print()
        return True
    return False
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage: {sys.argv[0]} [-d] num1 [num2...]
      Given strings of the digits 0-9, searches the square roots of the numbers
      from 2 to {N}.  Square roots are calculated to a precision of {digits}
      digits for these strings.  If they are found, the number and locations
      are printed.
    Options:
      -c    Disable use of color highlighting
      -d    Force use of python's Decimal objects (even if mpmath present)
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = True      # If True, use color highlighting
    d["-d"] = False     # If True, force use of Decimal numbers
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cd")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-c",):
            d["-c"] = not d["-c"]
        elif o in ("-d",):
            d["-d"] = not d["-d"]
    if not args:
        Usage(d)
    return args
if __name__ == "__main__":
    nl = "\n"
    ii = isinstance
    # How many digits to use in the decimal numbers
    digits = 1000
    # What's the largest integer we should search?
    N = 100
    # What's the largest root we should look for?
    max_root = 10
    # Regular expression to check input numbers
    proper = re.compile(r"^\d+$")
    #
    d = {}
    args = ParseCommandLine(d)
    if use_mpmath:
        mp.mp.dps = digits
    else:
        decimal.getcontext().prec = digits
    print(dedent(f'''
    Calculating to {digits} decimal places
      Searching numbers from 2 to {N}
      Using roots from 2 to {max_root}'''))
    print()
    for want in args:
        try:
            start = time.time()
            for root in range(2, max_root + 1):
                if not proper.match(want):
                    print(f"'{want}' is not a proper integer\n")
                    continue
                for i in range(2, N+1):
                    if CheckNumber(i, root, want, d):
                        raise CalculationDone
        except CalculationDone:
            pass
        tm = time.time() - start
        print(f"Searched for {tm:.1f} seconds")

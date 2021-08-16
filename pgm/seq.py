'''
TODO:

    * Use Unicode for fractions
    * Use flt for floating point ease

Generates sequences of numbers
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Generates sequences of numbers
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from string import ascii_letters, digits, punctuation
    from fractions import Fraction
    from math import *
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from frange import frange, Rational as R
    from sig import sig
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] n [m [inc]]
      Generate an arithmetical progression from n to m in steps of inc.
      If only n is given, the sequence goes from 1 to int(n).  inc
      defaults to 1.  The arguments n, m, and inc can be integers,
      floating point numbers, or improper fractions such as '5/3'.
    
      For some fractional and floating point inc values, you may get a
      finishing value in the sequence larger than m because the ending point
      in the sequence must be >= the specified endpoint when the -e option
      isn't used.
    
      Use the -t option to see some examples.
    Options
      -0    Make the sequences 0-based instead of 1-based
      -b b  Output in the indicated base (defaults to 10)
      -d n  Change the number of significant digits in the output.  n
            defaults to {digits}.
      -e    Don't include the end point of the sequence
      -n    Don't include a newline after the numbers
      -p p  Prepend the prefix string p to each number
      -S    Use the sig library to output the specified number of
            significant digits.  Normal output is to use "%g" string
            interpolation, which truncates trailing zeros.
      -s s  Append the suffix string s to each number
      -t    Show some examples
      -x    Allow expressions in n, m, and inc.  The math module's symbols
            are in scope.  Unless the result of an expression is an
            integer, the results will be floating point (i.e., fractions
            will be evaluated away).
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-0"] = False     # 0-based sequences
    d["-b"] = 10        # Output base
    d["-d"] = 3         # Number of significant digits
    d["-e"] = True      # Include end point
    d["-n"] = True      # If True, include newline after number
    d["-p"] = ""        # Prefix string
    d["-S"] = False     # Use sig if True
    d["-s"] = ""        # Suffix string
    d["-t"] = False     # Show some examples
    d["-x"] = False     # Allow expressions
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "0b:d:ehnp:Ss:tx")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-0":
            d["-0"] = True
        elif opt[0] == "-b":
            try:
                d["-b"] = int(opt[1])
                if not (2 <= d["-b"] <= 94):
                    raise ValueError()
            except ValueError:
                msg = "-b argument must be an integer between 2 and 94"
                Error(msg)
        elif opt[0] == "-d":
            try:
                d["-d"] = int(opt[1])
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = "-d argument must be an integer between 1 and 15"
                Error(msg)
        elif opt[0] == "-e":
            d["-e"] = False
        elif opt[0] == "-h":
            Usage(d, status=0)
        elif opt[0] == "-n":
            d["-n"] = False
        elif opt[0] == "-p":
            d["-p"] = opt[1]
        elif opt[0] == "-S":
            d["-S"] = True
        elif opt[0] == "-s":
            d["-s"] = opt[1]
        elif opt[0] == "-t":
            d["-t"] = True
        elif opt[0] == "-x":
            d["-x"] = True
    sig.digits = d["-d"]
    if not d["-t"] and len(args) not in range(1, 4):
        Usage(d)
    return args
def int2base(x, base):
    '''Converts the integer x to a string representation in a given
    base.  base may be from 2 to 94.
 
    Method by Alex Martelli
    http://stackoverflow.com/questions/2267362/convert-integer-to-a-string-in-a-given-numeric-base-in-python
    Modified slightly by DP.
    '''
    if not (2 <= base <= len(int2base.digits)):
        msg = "base must be between 2 and %d inclusive" % len(int2base.digits)
        raise ValueError(msg)
    if not isinstance(x, (int, str)):
        raise ValueError("Argument x must be an integer or string")
    if isinstance(x, str):
        x = int(x)
    sgn = 1
    if x < 0:
        sgn = -1
    elif not x:
        return '0'
    x, answer = abs(x), []
    while x:
        answer.append(int2base.digits[x % base])
        x //= base
    if sgn < 0:
        answer.append('-')
    answer.reverse()
    return ''.join(answer)
int2base.digits = digits + ascii_letters + punctuation
def GetParameters(args, d):
    '''Return n, m, inc as strings, suitably processed as
    expressions if the -x option was used.
    '''
    def f(x):
        return repr(eval(x, globals())) if d["-x"] else x
    if len(args) == 1:
        n, m, inc = "0" if d["-0"] else "1", f(args[0]), "1"
    elif len(args) == 2:
        n, m, inc = f(args[0]), f(args[1]), "1"
    else:
        n, m, inc = [f(i) for i in args]
    return (n, m, inc)
def Fractions(n, m, inc, d):
    for i in frange(n, m, inc, impl=R, return_type=R,
                    include_end=d["-e"]):
        t = d["-p"] + str(i) + d["-s"]
        if d["-n"]:
            print(t, "")
        else:
            print(t, "", end=" ")
    if not d["-n"]:
        print()
def FloatingPoint(n, m, inc, d):
    fmt = "%s%%.%dg%s" % (d["-p"], d["-d"], d["-s"])
    for i in frange(n, m, inc, include_end=d["-e"]):
        if i <= float(m):
            if d["-S"]:
                t = d["-p"] + sig(i) + d["-s"]
                if d["-n"]:
                    print(t, "")
                else:
                    print(t, "", end="")
            else:
                if d["-n"]:
                    print(fmt % i, "")
                else:
                    print(fmt % i, "", end="")
    if not d["-n"]:
        print()
def Integers(n, m, inc, d):
    for i in frange(n, m, inc, return_type=int, include_end=d["-e"]):
        s = int2base(i, d["-b"]) if d["-b"] else str(i)
        s = d["-p"] + s + d["-s"]
        if i <= int(m):
            if d["-n"]:
                print(s, "")
            else:
                print(s, "", end="")
    if not d["-n"]:
        print()
def ShowExamples(d):
    'Print some examples'
    d["-n"] = False
    f = "%-20s "
    print("Output for various command line arguments:\n")
    #
    print(f % "'-n 8'  ", end="")
    Integers(1, 8, 1, d)
    #
    print(f % "'-n -e 8'  ", end="")
    d["-e"] = False
    Integers(1, 8, 1, d)
    d["-e"] = True
    #
    print(f % "'-n -0 8'  ", end="")
    Integers(0, 8, 1, d)
    #
    d["-e"] = False
    print(f % "'-n -0 -e 8'  ", end="")
    Integers(0, 8, 1, d)
    d["-e"] = True
    #
    print()
    print(f % "'-n 0 1 1/8'  ", end="")
    Fractions(0, 1, "1/8", d)
    #
    print(f % "'-n -e 0 1 1/8'  ", end="")
    d["-e"] = False
    Fractions(0, 1, "1/8", d)
    d["-e"] = True
    #
    print()
    print(f % "'-n 1 6 0.75'  ", end="")
    FloatingPoint(1, 6, "0.75", d)
    #
    print(f % "'-n 1 6 3/4'  ", end="")
    Fractions(1, 6, "3/4", d)
    #
    print(f % "'-n -e 1 6 0.75'  ", end="")
    d["-e"] = False
    FloatingPoint(1, 6, "0.75", d)
    d["-e"] = True
    #
    print(f % "'-n -e 1 6 3/4'  ", end="")
    d["-e"] = False
    Fractions(1, 6, "3/4", d)
    d["-e"] = True
    #
    print(f % "'-n -S 1 6 0.75'  ", end="")
    d["-S"] = True
    FloatingPoint(1, 6, "0.75", d)
    exit(0)
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"]:
        ShowExamples(d)
    n, m, inc = GetParameters(args, d)
    # fp identifies a floating point string
    fp = lambda s:  s.find(".") != -1 or s.lower().find("e") != -1
    # fr identifies a fraction string
    fr = lambda s:  s.find("/") != -1
    if any([fr(s) for s in (n, m, inc)]):       # Fractions
        Fractions(n, m, inc, d)
    elif any([fp(s) for s in (n, m, inc)]):     # Floating point
        FloatingPoint(n, m, inc, d)
    else:   # Integers
        Integers(n, m, inc, d)

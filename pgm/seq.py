'''
TODO:
    - Use Unicode for fractions
    - Use flt for floating point ease

Generates sequences of numbers
'''
if 1:  # Header
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
        #from math import *
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import dedent
        from frange import frange, Rational as R
        from f import *
        from sig import sig
        from columnize import Columnize
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] n [m [inc]]
          Generate an arithmetical progression from n to m in steps of inc.  If only n is given,
          the sequence goes from 1 to int(n).  inc defaults to 1.  The arguments n, m, and inc can
          be integers, floating point numbers, or improper fractions such as '5/3'.
        
          For some fractional and floating point inc values, you may get a finishing value in the
          sequence larger than m because the ending point in the sequence must be >= the specified
          endpoint when the -e option isn't used.
        
          Use the -t option to see some examples.
        Options
          -0    Make the sequences 0-based instead of 1-based
          -b b  Output in the indicated base (defaults to 10)
          -C    Print output in columns like -c, but increasing horizontally
          -c    Print output in columns
          -d n  Number of significant digits in output [{d["-d"]}]
          -e    Don't include the end point of the sequence
          -n    Don't include a newline after the numbers
          -p p  Prepend the prefix string p to each number
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
        d["-C"] = False     # Output in columns like -c but increasing in rows
        d["-c"] = False     # Output in columns
        d["-d"] = 3         # Number of significant digits
        d["-e"] = False     # Include end point
        d["-n"] = False     # If True, include newline after number
        d["-p"] = ""        # Prefix string
        d["-s"] = ""        # Suffix string
        d["-t"] = False     # Show some examples
        d["-x"] = False     # Allow expressions
        if len(sys.argv) < 2:
            Usage(d)
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "0b:Ccd:ehnp:Ss:tx")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in list("0CcenStx"):
                d[o] = not d[o]
            elif o == "-b":
                try:
                    d["-b"] = int(a)
                    if not (2 <= d["-b"] <= 94):
                        raise ValueError()
                except ValueError:
                    msg = "-b argument must be an integer between 2 and 94"
                    Error(msg)
            elif o == "-d":
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(d, status=0)
            elif o == "-p":
                d["-p"] = a
            elif o == "-s":
                d["-s"] = a
        x = flt(0)
        x.N = d["-d"]
        if not d["-t"] and len(args) not in range(1, 4):
            Usage(d)
        return args
if 1:  # Core functionality
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
    def ShowExamples(d):
        'Print some examples'
        def P(seq):
            print(' '.join(seq))
        # dd will be a copy of d but with -e set to True
        dd = d.copy()
        dd["-e"] = True
        f = "%-25s "
        print("Output for various command line arguments:\n")
        #
        print(f % "'-n 8'  ", end="")
        P(Integers(1, 8, 1, d))
        #
        print(f % "'-n -e 8'  ", end="")
        P(Integers(1, 8, 1, dd))
        #
        print(f % "'-n -0 8'  ", end="")
        P(Integers(0, 8, 1, d))
        #
        print(f % "'-n -0 -e 8'  ", end="")
        P(Integers(0, 8, 1, dd))
        #
        print()
        print(f % "'-n 0 1 1/8'  ", end="")
        P(Fractions(0, 1, "1/8", d))
        #
        print(f % "'-n -e 0 1 1/8'  ", end="")
        P(Fractions(0, 1, "1/8", dd))
        #
        print()
        print(f % "'-n 1 6 0.75'  ", end="")
        P(FloatingPoint(1, 6, "0.75", d))
        #
        print(f % "'-n 1 6 3/4'  ", end="")
        P(Fractions(1, 6, "3/4", d))
        #
        print(f % "'-n -e 1 6 0.75'  ", end="")
        P(FloatingPoint(1, 6, "0.75", dd))
        #
        print(f % "'-n -e 1 6 3/4'  ", end="")
        P(Fractions(1, 6, "3/4", dd))
        print("The last two examples show why floating point implementations are naive.")
        # 
        # Demo of generating file names
        print("Demo of how to generate file names:")
        d["-p"] = "abc"
        d["-s"] = ".png"
        print(f % "'-p abc -s .png  1 4'  ", end="")
        P(Integers(1, 4, 1, d))
        exit(0)
    def IsFloatingPointString(s):
        return s.find(".") != -1 or s.lower().find("e") != -1
    def IsFractionString(s):
        return s.find("/") != -1
    def Fractions(n, m, inc, d):
        o = []
        for i in frange(n, m, inc, impl=R, return_type=R, include_end=d["-e"]):
            o.append(d["-p"] + str(i) + d["-s"])
        return o
    def FloatingPoint(n, m, inc, d):
        o = []
        for i in frange(n, m, inc, return_type=flt, include_end=d["-e"]):
            if i <= float(m):
                o.append(d["-p"] + str(i) + d["-s"])
        return o
    def Integers(n, m, inc, d):
        o = []
        for i in frange(n, m, inc, return_type=int, include_end=d["-e"]):
            s = int2base(i, d["-b"]) if d["-b"] else str(i)
            o.append(d["-p"] + s + d["-s"])
        return o

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"]:
        ShowExamples(d)
    n, m, inc = GetParameters(args, d)
    if any([IsFractionString(s) for s in (n, m, inc)]):       # Fractions
        o = Fractions(n, m, inc, d)
    elif any([IsFloatingPointString(s) for s in (n, m, inc)]):
        o = FloatingPoint(n, m, inc, d)
    else:
        o = Integers(n, m, inc, d)
    # Print output
    if d["-C"]:
        for i in Columnize(o, horiz=True):
            print(i)
    elif d["-c"]:
        for i in Columnize(o):
            print(i)
    elif d["-n"]:
        print(f"{' '.join(o)}")
    else:
        print('\n'.join(o))

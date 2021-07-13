'''
Command-line inch/mm converter
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Inch/mm converter
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import sys
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from sig import sig
    from f import flt
if 1:   # Global variables
    in2mm = flt(25.4)
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    digits = d["-d"]
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] dist1 [dist2...]
      Convert the arguments in inches to mm.  If -r is used, convert the arguments
      in mm to inches.
    Options:
      -d n      Number of significant figures [{d["-d"]}]
      -m        Arguments are in mm; convert to inches
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-d"] = 4         # Number of significant digits
    d["-m"] = False     # Convert from inches to mm
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:m")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                       "1 and 15")
                Error(msg)
        elif o == "-m":
            d[o] = not d[o]
    if not args:
        Usage(d)
    return args
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    flt(0).n = d["-d"]
    for i in args:
        if d["-m"]:
            print(f"{flt(i)} mm = {flt(i)/25.4} inches")
        else:
            print(f"{flt(i)} inches = {flt(i)*25.4} mm")

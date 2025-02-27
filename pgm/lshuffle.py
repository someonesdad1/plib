"""
Shuffle n integers
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2015 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Shuffle n integers
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import math
    import random
    import sample
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def GetFormat(population_size, d):
    num_digits = int(math.log10(population_size)) + 1
    if d["-n"] < 0:
        num_digits += 1
    return "%%%dd" % num_digits


def ShuffleStdin():
    lines = sys.stdin.readlines()
    random.shuffle(lines)
    sys.stdout.writelines(lines)
    exit(0)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] population_size [num_times]
      Prints a random permutation of the integers from 1 to population_size.
      num_times defaults to 1.
    Options:
      -@        Shuffle lines from stdin
      -n n      Start the sequence of numbers at n [1]
      -s d      Set the seed for the random number generator
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-@"] = False
    d["-n"] = 1  # Start of number sequence
    d["-s"] = None  # Seed
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "@n:s:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-@",):
            d["-@"] = True
        elif o in ("-n",):
            try:
                d["-n"] = int(a)
            except Exception:
                print("'{0}' is a bad integer".format(a))
                exit(1)
        elif o in ("-s",):
            d["-s"] = a
            random.seed(a)
    if (d["-@"] and args) or (not d["-@"] and len(args) not in (1, 2)):
        Usage(d)
    return args


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-@"]:
        ShuffleStdin()
    else:
        num_times = 1
        try:
            population_size = int(args[0])
        except Exception:
            print(f"'{args[0]}' is a bad population size")
            exit(1)
        if len(args) == 2:
            try:
                num_times = int(args[1])
            except Exception:
                print(f"'{args[1]}' is a bad number of times")
                exit(1)
        format = GetFormat(population_size, d)
        r = range(d["-n"], d["-n"] + population_size)
        for i in range(num_times):
            for num in sample.shuffle(list(r)):
                print(format % num, end=" ")
            print()

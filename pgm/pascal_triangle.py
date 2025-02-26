"""
Print out Pascal's triangle
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Print out Pascal's triangle
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    from math import factorial
if 1:  # Custom imports
    from wrap import dedent


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} m [n]
      Print Pascal's triangle from 1 to m or m to n if the second argument
      is given.
    """)
    )
    if d["-h"]:
        print(
            dedent(f"""
        Formula
          The kth number on each line that begins with m is Bin(m, k) where we must
          have 0 <= k <= m and Bin is the binomial coefficient, which is 
          m!/(k!*(m - k)!).  Example:  for the line that begins with '5:', the third
          number will be for k = 2.  It's value is 5!/(2!*(5 - 2)!), which is 
          5!/(2*3*2) = 5*4*3*2/(3*4) = 10.
        """)
        )
    exit(status)


def ParseCommandLine(d):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", "help")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            d[o] = not d[o]
            Usage(d, status=0)
    if len(args) not in (1, 2):
        Usage(d)
    m = int(args[0])
    n = int(args[1]) if len(args) == 2 else None
    if m < 0 or (n is not None and n < 0):
        Error("m and n must be integers >= 0")
    if n is not None and n < m:
        Error("n must be >= m")
    return m, n


def Line(n):
    a, s = [], 0
    print(f"{n}: ", end="")
    for i in range(n + 1):
        value = factorial(n) // (factorial(i) * factorial(n - i))
        s += value
        print(value, end=" ")
    print()
    # An invariant is that the sum of Bin(m, n) over n for 0 to m must be
    # 2**n.  This is a check on the calculation.
    assert s == 2**n


if __name__ == "__main__":
    d = {"-h": False}  # Options dictionary
    m, n = ParseCommandLine(d)
    s = [1]
    if n is None:
        for i in range(m + 1):
            Line(i)
    else:
        for i in range(m, n + 1):
            Line(i)

"""
Finds expressions for a given number in terms of sum and differences of the
powers of a set of integers.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Expressions for integers in terms of the sums and differences of a set of integers
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    max_num_to_use = 100
    highest_power = 9


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] N [M]
        For the set of integers from N to M (1 to N if M isn't given), print
        out the sums and differences of powers of integers from 1 to n that
        yield that integer.
    Note:  You can also use commas on the command line to separate
    integers.  These individual integers will then be searched.
    Options:
        -n n    Highest integer to use for power base [{d["-n"]}]
        -p p    Highest power to use [{d["-p"]}]
        -u      Use Unicode power codepoints for easier reading
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-n"] = 100  # Highest integer to use
    d["-p"] = 3  # Highest power to use
    d["-u"] = False  # Use Unicode power codepoints
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:p:u")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "u":
            d[o] = not d[o]
        elif o in ("-n",):
            d["-n"] = int(a)
            if d["-n"] < 2:
                Error(f"-n option must be > 1")
        elif o in ("-p",):
            d["-p"] = int(a)
            if d["-p"] < 2:
                Error(f"-p option must be > 1")
        elif o in ("-h", "--help"):
            Usage(status=0)
    if "," in " ".join(args):
        args = [int(i) for i in "".join(args).split(",")]
        return args
    else:
        if len(args) not in (1, 2):
            Usage()
        if len(args) == 1:
            N, M = 1, int(args[0])
        else:
            N, M = int(args[0]), int(args[1])
        if N < 2 or M < 2:
            Error(f"M and N have to be > 1")
        if N > M:
            M, N = N, M
        return N, M


def Translate(s):
    'Make Unicode powers if d["-u"] is True'
    tt = "".maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    def F(t):
        assert "^" in t
        a, b = t.split("^")
        return "".join([a, b.translate(tt)])

    if not d["-u"]:
        return s
    f = s.split()
    return "  " + " ".join([F(f[0]), f[1], F(f[2])])


def Search(n, highest_power, highest_base):
    terms, found = [f"{n}"], False
    already_have = set()

    def Find(n, power):
        m = power
        for i in range(1, highest_base + 1):
            for j in range(i, highest_base + 1):
                if i**m + j**m == n:
                    s = Translate(f"  {i}^{m} + {j}^{m}")
                    if s not in already_have:
                        terms.append(s)
                        found = True
                        already_have.add(s)
                if j**m - i**m == n:
                    s = Translate(f"  {j}^{m} - {i}^{m}")
                    if s not in already_have:
                        terms.append(s)
                        found = True
                        already_have.add(s)

    for i in range(2, highest_power + 1):
        Find(n, i)
    if len(terms) > 1:
        terms.append("")
    else:
        terms[0] += " -- no expressions\n"
    print("\n".join(terms), end="")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    highest_base = d["-n"]
    highest_power = d["-p"]
    if ii(args, list):
        for i in args:
            Search(i, highest_power, highest_base)
    else:
        N, M = args
        for i in range(N, M + 1):
            Search(i, highest_power, highest_base)

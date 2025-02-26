"""
Replacement for the UNIX-style nl program for line numbering.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Line numbering script
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    import re
    from math import log10, ceil
if 1:  # Custom imports
    from wrap import dedent


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [file1 [file2...]]
      Number lines of a file.  If more than one file is given, it is as if
      they were all concatenated together.  Use '-' to read stdin.
    Options:
      -E re   Same as -e except search is case-sensitive
      -e re   Only number lines that contain the given regular expression.
              Search is case-insensitive.  The sense of matching is reversed
              by using the -R option (i.e., the lines which don't contain
              the regexp are numbered).
      -h      Show this usage statement.
      -i n    Line number increment [1]
      -n n    Start with this line number [1]
      -p n    Pages defined to be n lines long.  Line numbers are printed as
              page number, '.', and line count within page. [0]
      -q s    Surround line's text with the string s
      -R      Reverse the sense of the regexp match for -e and -E
      -r      Right justify numbers
      -s s    Print string s after line number.  Escape codes are decoded,
              so you can use things like \\t for tabs.
      -t      Use a tab character between the number and line's text.
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-e"] = None  # Number only if this regexp in line
    d["-i"] = 1  # Line increment number
    d["-n"] = 1  # Starting line number
    d["-p"] = 0  # Page length
    d["-q"] = None  # Delimit text with ' characters
    d["-R"] = False  # Reverse sense of -e/-E
    d["-r"] = False  # Right justify numbers
    d["-s"] = " "  # String to print after line number
    d["-t"] = False  # Tab separates number & text
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "ce:E:hi:n:p:q:Rrs:t")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o == "-E":
            try:
                d["-e"] = re.compile(a)
            except Exception:
                Error("Bad regular expression")
        if o == "-e":
            try:
                d["-e"] = re.compile(a, re.I)
            except Exception:
                Error("Bad regular expression")
            if d["-p"]:
                Error("Options -e and -E cannot be used with option -p")
        if o == "-h":
            Usage(d, status=0)
        if o == "-i":
            try:
                d["-i"] = int(a)
            except Exception:
                Error("'%s' is not an integer" % a)
            if d["-i"] <= 0:
                Error("-i option argument must be > 0")
        if o == "-R":
            d["-R"] = True
        if o == "-r":
            d["-r"] = True
        if o == "-n":
            try:
                d["-n"] = int(a)
            except Exception:
                Error("'%s' is not an integer" % a)
            if d["-n"] < 0:
                Error("-n option argument must be >= 0")
        if o == "-p":
            try:
                d["-p"] = int(a)
            except Exception:
                Error("'%s' is not an integer" % a)
            if d["-p"] <= 0:
                Error("-p option argument must be > 0")
            if d["-e"] is not None:
                Error("Options -e and -E cannot be used with option -p")
        if o == "-q":
            d["-q"] = opt[1]
        if o == "-s":
            d["-s"] = opt[1].decode("string_escape")
        if o == "-t":
            d["-s"] = "\t"
    if not args:
        Usage(d, status=1)
    return args


def GetLines(files):
    lines = []
    for file in files:
        if file == "-":
            lines += sys.stdin.readlines()
        else:
            try:
                lines += open(file).readlines()
            except Exception:
                Error("Bad file '%s'" % file)
    lines = [i.rstrip("\n") for i in lines]
    return lines


def Width(n):
    """Return the number of spaces required to hold the integer n."""
    assert n > 0
    if n == 1:
        return 1
    else:
        power_of_ten = set([int(10**i) for i in range(1, 10)])
        return int(ceil(log10(n))) + (n in power_of_ten)


def GetNumberWidth(lines, d):
    """Return the required number of spaces to hold the maximum line
    number.
    """
    if d["-p"]:
        num_pages = len(lines) // d["-p"]
        return Width(num_pages) + 1 + Width(d["-p"])
    else:
        nmax = d["-n"] + (len(lines) - 1) * d["-i"]  # Maximum line number
        return Width(nmax)


def GetNumbers(lines, d):
    """Return an array of the same length as lines containing the
    desired line numbers.  Note they will be the formatted strings, so
    all that needs to be done is to concatenate them with each line.
    """
    if d["-p"]:  # Page numbering (ignores -r option)
        num_pages = len(lines) // d["-p"]
        fmt = "%%%dd.%%-%dd%s" % (Width(num_pages), Width(d["-p"]), d["-s"])
        s = []
        for i in range(len(lines)):
            n, l = divmod(i, d["-p"])
            s.append(fmt % (n + 1, l + 1))
        return s
    else:
        maxnum = d["-n"] + d["-i"] * len(lines)
        fmt = "%%-%ds%s" % (Width(maxnum), d["-s"])
        if d["-r"]:
            fmt = "%%%ds%s" % (Width(maxnum), d["-s"])
        if d["-e"] is not None:
            linenums, count, incr = [], d["-n"], d["-i"]
            for line in lines:
                if d["-R"]:
                    if not d["-e"].search(line):
                        s = fmt % count
                        count += incr
                    else:
                        s = fmt % ""
                else:
                    if d["-e"].search(line):
                        s = fmt % count
                        count += incr
                    else:
                        s = fmt % ""
                linenums.append(s)
            return linenums
        else:
            return [
                (fmt % i) for i in range(d["-n"], d["-i"] * len(lines) + 1, d["-i"])
            ]


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    lines = GetLines(args)
    numbers = GetNumbers(lines, d)
    for n, l in zip(numbers, lines):
        if d["-q"]:
            s = n + d["-q"] + l + d["-q"]
        else:
            s = n + l
        print(s)

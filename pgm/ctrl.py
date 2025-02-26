"""
Remove printable characters from the lines of the text files (or stdin)
and report on which lines have control characters or Unicode characters.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Report ctrl/Unicode characters
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import string
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from columnize import Columnize
    from wrap import dedent
if 1:  # Global variables
    nl = "\n"
    ii = isinstance
    # Set up a translation dictionary to remove printable characters
    tr = {}
    for i in string.printable:
        tr[ord(i)] = None
    # The following dictionary will turn control characters into capital
    # letters by adding 0x40 to the ordinal value.
    ct = {}
    for i in range(0x20):
        ct[i] = i + 0x40


def CTRL(x):
    return x.translate(ct)


def TR(x):
    return x.translate(tr)


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    name = sys.argv[0]
    print(
        dedent("""
    Usage:  {name} [options] file1 [file2...]
      Writes out line numbers with control or Unicode characters.  Use
      '-' to get lines from stdin.
    Options:
      -a    Annotate Unicode characters with codepoint in parentheses
    """)
    )
    exit(status)


def ParseCommandLine():
    d["-a"] = False  # Annotate Unicode
    try:
        opts, files = getopt.getopt(sys.argv[1:], "ah")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-a",):
            d["-a"] = not d["-a"]
        elif o in ("-h", "--help"):
            Usage(status=0)
    if not files:
        Usage(status=0)
    return files


def GetLines(file):
    lines = sys.stdin.readlines() if file == "-" else open(file).readlines()
    return [i.rstrip() for i in lines]


def Controlify(c):
    if ord(c) < 0x60:
        return "^" + c
    return c


def Check(line, line_number, d):
    """Print out a message if this line contains control or Unicode
    characters.
    """
    chars = TR(line)
    if chars:
        print(f"  {line_number}: ", end="")
        for i in chars:
            d["chars"].add(i)
            if ord(i) < 0x60:
                print(Controlify(CTRL(i)))
            elif ord(i) > 127:
                if d["-a"]:
                    print(f" {i} (U+{ord(i):04x})")
                else:
                    print(i)


def Summary():
    if d["chars"]:
        out, s = [], []
        print("\nUnicode codepoints of characters used:")
        for i in d["chars"]:
            s.append((ord(i), i))
        for o, i in sorted(s):
            if o < 0x60:
                out.append(f"U+{o:x}: {Controlify(CTRL(i))} ")
            else:
                out.append(f"U+{o:x}: {i} ")
        for i in Columnize(out):
            print(i)


if __name__ == "__main__":
    d = {"chars": set()}  # Options dictionary
    files = ParseCommandLine()
    for file in files:
        lines = GetLines(file)
        f = "stdin" if file == "-" else file
        print(f)
        for count, line in enumerate(lines):
            Check(line, count + 1, d)
    Summary()

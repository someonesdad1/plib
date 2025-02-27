if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Show text file contents with lines truncated to screen width
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [file1 [file2 ...]
      Print the files' contents to the screen, chopping off each line at the
      number of columns specified by one less than the COLUMNS environment
      variable.  The intent is to see the contents with no wrapping.
      Use a file name of '-' for stdin.
    Options:
      -c c      Set the number of columns to chop, overriding COLUMNS - 1
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-c"] = int(os.environ.get("COLUMNS", 80)) - 1
    try:
        opts, files = getopt.getopt(sys.argv[1:], "c:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-c",):
            try:
                d["-c"] = int(a)
                if d["-c"] < 1:
                    raise ValueError()
            except ValueError:
                Error("-c option's argument must be an integer > 0")
    if not files:
        Usage()
    return files


def ProcessFile(stream):
    for line in [i.rstrip()[: d["-c"]] for i in stream.readlines()]:
        print(line)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(sys.stdin if file == "-" else open(file))

"""
Convert HTML file(s) on command line to plain text.

Needed:  'pip install html2text'
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Convert HTML file(s) to plain text
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    import html2text
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [file1 [file2...]]
      Prints HTML files converted to basic markdown text to stdout.
    Options:
        -l      Include links
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-l"] = True  # Print links too
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("l"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if not args:
        Usage(d)
    return args


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        tm = html2text.HTML2Text()
        tm.ignore_links = True if d["-l"] else False
        html = open(file).read()
        text = tm.handle(html)
        print(text)
        if len(files) > 1:
            print()

"""
Remove multiple blank lines in one or more files.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Remove multiple blank lines in one or more files
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import pathlib
    import re
    import getopt
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    P = pathlib.Path
    nl = "\n"
    r = re.compile(r"\n[ \t\r\f\v]+\n", re.S)


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] file1 [file2...]
      Replace multiple blank lines in a file with a single line.  The blank
      lines can include whitespace.  The indicated files are read in and
      the transformed text is sent to stdout.  If you want to permanently
      modify each file, use the -o option.  Use "-" as a filename to modify
      stdin.
    Options
        -f  Force overwriting of a backup file
        -o  Modify each file and overwrite it.  Create a backup version of the
            file with the '.bak' extension.
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-f"] = False
    d["-o"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, files = getopt.getopt(sys.argv[1:], "fo")
    except getopt.GetoptError as e:
        Error(str(e))
    for o, a in opts:
        if o[1] in "fo":
            d[o] = not d[o]
    if not files:
        Usage(d)
    return files


def ProcessString(s):
    """s is a string representing a text file.  Remove the indicated
    multiple blank lines and return the fixed string.
    """
    # Replace a line with only whitespace with a single newline
    while r.search(s):
        s = r.sub("\n", s)
    # Replace multiple newline characters
    nl3, nl2 = nl * 3, nl * 2
    while nl3 in s:
        s = s.replace(nl3, nl2)
    return s


def ProcessStdin():
    s = sys.stdin.read()
    print(ProcessString(s))


def ProcessFile(file):
    if file == "-":
        ProcessStdin()
        return
    p = P(file)
    backup = P(file + ".bak")
    if backup.is_file() and not d["-f"]:
        Error(f"Backup file '{backup}' exists (use -f to overwrite)")
    s = open(file).read()
    open(backup, "w").write(s)  # Make backup copy
    t = ProcessString(s)
    open(file, "w").write(t)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    if d["-o"]:
        for file in files:
            ProcessFile(file)
    else:
        s = []
        for file in files:
            if file == "-":
                s.append(sys.stdin.read())
            else:
                s.append(open(file).read())
        print(ProcessString("".join(s)), end="")

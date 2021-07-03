'''
Show regex matches on lines in files
    For the files given on the command line, find the regular expression
    given on the command line (take input from stdin if no files given).
    Then decorate each line with a found string.  Print all lines; the
    color shows where the matches were.

    In other words, it's the GNU grep tool that prints all lines of the
    files out and decorates the matches in color.  The name is 'dec',
    which is short for decorate.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Show decorated lines in files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import re
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from color import fg, normal, black, gray, blue, lblue, green, lgreen
    from color import cyan, lcyan, red, lred, magenta, lmagenta, brown
    from color import yellow, white, lwhite
if 1:   # Global variables
    # Define the color pairs you want to use.
    c_filename = (lmagenta, black)
    c_match = (lred, black)
    c_colon = (lcyan, black)
    c_numbers = (lgreen, black)
    # Keep track of number of lines printed
    _lines_printed = 0
    _lines_default = 25
def Usage(d, status=1):
    name = sys.argv[0]
    try:
        lines = int(os.environ["LINES"])
    except KeyError:
        lines = _lines_default
    linesdef = _lines_default
    print(dedent(f'''
    Usage:  {name} [options] regexp [file1 [file2 ...]]
      Decorate a regexp in a text stream.  Behaves like GNU grep in
      searching for a regular expression.  However, all lines of each of the
      files are printed and the matches are highlighted in color.  Use '-'
      for stdin.
    Options:
      -f    Don't print filename before each line
      -g    Act like grep
      -i    Ignore case in search
      -p    Page the output at {lines} lines (uses LINES environment variable
            if present; {linesdef} if not).
      -n    Show line numbers
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-f"] = False
    d["-g"] = False
    d["-i"] = False
    d["-n"] = False
    d["-p"] = 0
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "fginp")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o[1] in "fgin":
            d[o] = not d[o]
        elif opt[0] == "-p":
            try:
                d["-p"] = int(os.environ["LINES"])
            except KeyError:
                d["-p"] = _lines_default
    if not args:
        Usage(d)
    return args
def CheckMatches(line, regexp):
    '''Look for all matches of regexp in the line and return a list of
    the beginning and ending indexes of the matches.
    '''
    matches = []
    mo = regexp.search(line)
    while mo:
        start, end = mo.start(), mo.end()
        matches.append(start)
        matches.append(end)
        mo = regexp.search(line, end + 1)
    return matches
def ProcessLine(line, linenum, regexp, d, file=None):
    def ShowLineNumber():
        if d["-n"]:  # Show line numbers
            fg(c_numbers)
            print(str(linenum), end="")
            fg(c_colon)
            print(":", end="")
            normal()
    def ShowFileName():
        if file is not None:    # Color the file name
            fg(c_filename)
            print(file, end="")
            fg(c_colon)
            print(":", end="")
            normal()
    global _lines_printed
    matched = CheckMatches(line, regexp)
    if matched:  # Color highlight the line where the matches are
        matched = [0] + matched
        matched.append(len(line))
        ShowFileName()
        ShowLineNumber()
        # Print the line using the partition gotten from the regular
        # expression.
        for i in range(len(matched) - 1):
            if i % 2 == 0:
                normal()
                print(line[matched[i]:matched[i+1]], end="")
            else:
                fg(c_match)
                print(line[matched[i]:matched[i+1]], end="")
        print()
        _lines_printed += 1
    else:
        normal()
        if not d["-g"]:
            ShowFileName()
            ShowLineNumber()
            print(line)
            _lines_printed += 1
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    exp = "(" + files[0] + ")"
    regexp = re.compile(exp, re.I) if d["-i"] else re.compile(exp)
    del files[0]
    for file in files:
        if file == "-":
            filename = "stdin"
            lines = sys.stdin.readlines()
        else:
            filename = file
            lines = open(file).readlines()
        for i, line in enumerate(lines):
            linenum = i + 1
            line = line.rstrip("\n")
            f = None if d["-f"] else filename
            ProcessLine(line, linenum, regexp, d, file=f)

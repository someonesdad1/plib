# Adapted from
# http://stackoverflow.com/questions/13506033/filtering-out-ansi-escape-sequences
# Downloaded 11 Jul 2014

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
import os
import re
import sys
from get import GetLines

_ansi_regexp = re.compile(r'\033\[((?:\d|;)*)([a-zA-Z])')

def StripANSIEscapeSequences(string):
    '''Remove ANSI escape sequences from string and return the result.
    '''
    lastend = 0
    matches = []
    for match in _ansi_regexp.finditer(string):
        start, end = match.start(), match.end()
        matches.append(match)
    matches.reverse()
    for match in matches:
        start, end = match.start(), match.end()
        string = string[0:start] + string[end:]
    return string
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} [-h] [file1 [file2...]]
      Removes ANSI escape sequences from the indicated files and prints
      their lines to stdout.
    '''))
    exit(0)
if __name__ == "__main__":
    # If used as a script, read the lines from any files given on the
    # command line.  If none are given, read them from stdin.
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h":
            Usage()
        for file in sys.argv[1:]:
            for line in GetLines(file):
                print(StripANSIEscapeSequences(line))
    else:
        for line in sys.stdin.readlines():
                print(StripANSIEscapeSequences(line), end="")

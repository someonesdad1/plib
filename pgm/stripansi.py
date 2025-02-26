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
from wrap import dedent


def Usage():
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [-h] [file1 [file2...]]
      Removes ANSI escape sequences from the indicated text files and prints
      them to stdout.  Use '-' for stdin.
    """)
    )
    exit(0)


if 0:
    _ansi_regexp = re.compile(r"\033\[((?:\d|;)*)([a-zA-Z])")

    def StripANSIEscapeSequences(string):
        """Remove ANSI escape sequences from string and return the result."""
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
elif 0:

    def ProcessString(text):
        """16 Feb 2023 Suggested regexp from
        https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
        """
        regex = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return regex.sub("", text)

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            if sys.argv[1] == "-h":
                Usage()
            for file in sys.argv[1:]:
                text = open(file).read()
                print(ProcessString(text))
        else:
            text = sys.stdin.read()
            print(ProcessString(text))
else:

    def ProcessString(text):
        """16 Feb 2023 Suggested regexp from
        https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
        (see the answer below this answer, as it is a more general regexp).
        """
        regex = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        return regex.sub("", text)

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            if sys.argv[1] == "-h":
                Usage()
            for file in sys.argv[1:]:
                text = sys.stdin.read() if file == "-" else open(file).read()
                print(ProcessString(text))
        else:
            text = sys.stdin.read()
            print(ProcessString(text))

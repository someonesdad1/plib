"""
TODO:

    - Modernize to a python 3 implementation using f-strings
    - Use -a to asciify.  This would convert all latin-1 letters to
      their ASCII 'equivalents' and make it easier to find the words in
      an English dictionary.
    - Use gettokens module.  Keep contractions & possessives; use -k to
      remove them.
    - Use lowercase by default (-i to make case sensitive)
    - Show cumulative percentage too so it's easy to e.g. spot
      the quartiles and median
    - Use -c option to print lines with cumulative frequency up to
      50% in green.
    - Include rank numbers
    - Print hapaxes with -h in columns, as there will typically be many
    - Print summary statistics with -s
        - Total number of words
        - Histogram of number of syllables
        - Histogram for number of characters
        - Histogram of letter frequencies
        - Set of non-7-bit characters

----------------------------------------------------------------------
Count the words in a file.
"""

# Copyright (C) 2014, 2024 Don Peterson
# Contact:  gmail.com@someonesdad1
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
import sys
import getopt
import fileinput
from collections import defaultdict
from string import ascii_letters
from pdb import set_trace as xx

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Program description string
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:  # Custom imports
        from color import t
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
        # from columnize import Columnize
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Utility

    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)

    Dbg.file = sys.stdout

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] etc.
          Read in the text from the files and print the word counts with the least-frequent words first in
          the output.  Use '-' to read input from stdin.
        Options:
          -i        Ignore case
          -r        Make the most-frequent words in the output first
          -t n      Only show the top n words
          -w        Just print the words in sorted order
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-i"] = False  # Ignore case
        d["-r"] = False  # Most frequent words first in output
        d["-s"] = False  # Read from stdin first
        d["-t"] = 0  # Only show the top number of words if > 0
        d["-w"] = False  # Only print the words
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hirst:w")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("irsw"):
                d[o] = not d[o]
            elif o == "-t":
                try:
                    d["-t"] = int(opt[1])
                    if d["-t"] < 0:
                        raise ValueError()
                except ValueError:
                    msg = "-t option's argument must be an integer >= 0"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        if not args and not d["-s"]:
            Usage()
        return args


if 1:  # Core functionality

    def Keep(s):
        "Replace all non-word characters with spaces"
        return s.translate(Keep.t)

    Keep.allowed = set(ascii_letters)
    Keep.c = [chr(i) for i in range(256)]
    Keep.t = "".join([i if i in Keep.allowed else " " for i in Keep.c])

    def ProcessFile(words, file):
        for line in GetLines(file):
            line = Keep(line)
            line = line.lower() if d["-i"] else line
            for word in line.split():
                words[word] += 1

    def Report(words):
        # Print the words only if -w given
        if d["-w"]:
            wordlist = (
                reversed(sorted(words.keys())) if d["-r"] else sorted(words.keys())
            )
            for word in wordlist:
                print(word)
            return
        # Generate a list with elements (count, word)
        tmp = [(count, word) for word, count in words.items()]
        # Sort by count, lowest first
        tmp = sorted(tmp)
        # Keep only a subset if -t option used
        if d["-t"]:
            tmp = tmp[-d["-t"] :]
        # Reverse the order if -r option was given
        if d["-r"]:
            tmp = list(reversed(tmp))
        # Include the percentages
        total = sum([count for count, word in tmp])
        wordlist = [
            (word, count, "{:.2g}%".format(100 * count / total)) for count, word in tmp
        ]
        # Get largest string lengths so we can format things
        largest_word = max([len(i[0]) for i in wordlist]) + 3
        largest_count = max([len(str(i[1])) for i in wordlist]) + 3
        # Print the report
        f = "{:{}s} {:{}d}       {}"
        for word, count, pct in wordlist:
            print(f.format(word, largest_word, count, largest_count, pct))


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    # Fill a dictionary keyed by words with the word counts as values
    words = defaultdict(int)
    for file in files:
        ProcessFile(words, file)
    Report(words)

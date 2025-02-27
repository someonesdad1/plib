"""
Todo
    - Add option to replace punctuation (except ' for contractions) in
      words with spaces before splitting.
        - -p replaces punctuation except ' and single - (thus keeping
          contractions and hyphenations)
        - -P replaces all punctuation
    - Make columnization an option

Provides WordParse(string) to get a list of words in the string.

Run as a script to print a set of the words in the files given on the
command line.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Program description string
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        import getopt
        import os
        from pathlib import Path as P
        import re
        import string
        import sys
    if 1:  # Custom imports
        from asciify import Asciify
        from wrap import dedent
        from color import t
        from columnize import Columnize
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        punc = set(string.punctuation)
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Print out the words in the indicated text files.  Use "-" to read
          from stdin.  
        Options:
            -a      Do not asciify the input text
            -P      Replace all punctuation with space characters
            -p      Same as -P except for ' and -
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = True  # Do not asciify the text
        d["-P"] = False  # Replace all punctuation with space
        d["-p"] = False  # Replace punc except ' and single -
        try:
            opts, args = getopt.getopt(sys.argv[1:], "aPph")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("aPp"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        if not args:
            Usage()
        return args


if 1:  # Core functionality

    def FixWord(word):
        "Remove leading and trailing punctuation"
        dq = deque(word)
        # Remove left punctuation characters
        while dq:
            if dq[0] in punc:
                dq.popleft()
            else:
                break
        # Remove right punctuation characters
        while dq:
            if dq[-1] in punc:
                dq.pop()
            else:
                break
        if d["-P"] or d["-p"]:
            print("-P, -p option not working")
            exit()
            # Remove middle punctuation characters
            ndq = dq.copy()
            while dq:
                c = dq.popleft()
                if c in punc:
                    if d["-P"]:
                        continue
                    elif c == "-":
                        if dq and dq[0] == "-":
                            dq.popleft()
                            continue
                        ndq.append(c)
                    elif c == "'":
                        ndq.append(c)
                    else:
                        continue
                else:
                    ndq.append(c)
            dq = ndq.copy()
        return "".join(dq)

    def WordParse(s, ic=False):
        """Returns a set of words from the string s.
        ic      Ignore case if True
        """
        if ic:
            s = s.lower()
        words = set(s.split())
        new_words = set()
        for w in words:
            word = FixWord(w)
            if word:
                new_words.add(word)
        return new_words

    def FixFile(s):
        """s is the string read from a file.  Do the needed fix-ups and
        return a set of words from the string.
        """
        s1 = Asciify(s) if d["-a"] else s
        # Substitute ' ' for most punctuation characters except ' . -
        p = (
            r"!|\"|#|\$|%|&|\(|\)|\*|\+|,|/|:|;|<|=|>|"
            r"\?|@|\[|\\|\]|\^|_|`|\{|\||\}|~"
        )
        s2 = re.sub(p, " ", s1)
        # Substitute ' ' for two or more hyphens, periods, single quotes
        s3 = re.sub(r"---*|'''*|\.\.\.*", " ", s2)
        wrds = set(s3.split())
        if 1:  # Specific fixups
            # Remove ' or " at beginning of word
            f = lambda x: x.startswith("'") or x.startswith('"')
            a = list(filter(f, wrds))
            for i in a:
                wrds.add(i[1:])
                wrds.remove(i)
            # Remove .' at end of word
            f = lambda x: x.endswith(".'")
            a = list(filter(f, wrds))
            for i in a:
                wrds.add(i[:-2])
                wrds.remove(i)
            # Remove . at end of word
            f = lambda x: x.endswith(".")
            a = list(filter(f, wrds))
            for i in a:
                wrds.add(i[:-1])
                wrds.remove(i)
            # Remove ' at end of word
            if 1:
                f = lambda x: x.endswith("'")
                a = list(filter(f, wrds))
                for i in a:
                    wrds.add(i[:-1])
                    wrds.remove(i)
        return wrds


if 0:
    exit()

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    words = set()
    for file in files:
        if file == "-":
            s = sys.stdin.read()
        else:
            s = open(file).read()
        wrds = FixFile(s)
        words.update(wrds)
    if 1:
        from dpstr import KeepFilter
        from abbreviations import IsAbbreviation

        f = KeepFilter("'.-")
        words = filter(f, words)
    for i in sorted(words):
        print(i)

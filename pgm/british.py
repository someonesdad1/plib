"""
Identify British spellings in files on command line
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Identify British spellings in files on command line
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from collections import defaultdict
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from columnize import Columnize
        from color import t
    if 1:  # Global variables
        stdin = "stdin"
        # regexp to convert all 7-bit punctuation to spaces
        punct = re.compile(r"[~`!@#$%\^&*()\-+={}\[\]\\\;:\"'\|,\.<>\?/]+")
        t.brit = t("lill")
        t.us = t("yell")
        t.file = t("ornl")
if 1:  # Utility

    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)

    def Usage():
        name = sys.argv[0]
        print(
            dedent(f"""
        Usage:  {name} [options] [file1 [file2...]]
          For each file, find words with British spelling and print out the American form.  Include the
          file and line number.  Use a file of '-' for stdin.
        """)
        )
        exit(0)

    def ParseCommandLine(d):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                Usage(d, status=0)
        if not args:
            Usage()
        return args


if 1:  # Core functionality

    def GetDict():
        di = {}
        lines = open("/words/words.brit").read().split("\n")
        # US word first, British form second
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            us, brit = line.split()
            di[brit] = us
        return di

    def Process(file):
        "Print a list of British words in the file along with the line number"
        lines = sys.stdin.readlines() if file == "-" else open(file).readlines()
        out, total = defaultdict(list), 0
        for ln, line in enumerate(lines):
            words = punct.sub(" ", line).split()
            total += len(words)
            for word in words:
                w = word.lower()
                if w in british_words:
                    out[w].append(ln + 1)
        if out:
            print("Line numbers in file(s) where British words are:")
            print(
                f"{t.file}stdin{t.n}" if file == "-" else f"{t.file}{file}{t.n}",
                end=" ",
            )
            print(f"({total} words in file)")
            for w in sorted(out):
                us = british_words[w]
                W = [str(i) for i in out[w]]
                l = " ".join(W)
                s = f"  {t.brit}{w}{t.n} -> {t.us}{us}{t.n}:  "
                print(f"{s}{l}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    british_words = GetDict()
    width = int(os.environ.get("COLUMNS", 80)) - 1
    files = ParseCommandLine(d)
    for file in files:
        Process(file)

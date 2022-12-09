'''
Find synonyms (based on Moby thesaurus)
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Find synonyms (based on Moby thesaurus).
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, t
        from columnize import Columnize
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regex1 [regex2...]
          Show matches for the given regular expressions in the Moby
          thesaurus.  To show the synonyms for thse words, use the -s
          option.
        Options:
            -a      Color always on
            -c      No color
            -i      Don't ignore case
            -s      Show synonyms for the words
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-c"] = True
        d["-i"] = True
        d["-s"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acihs") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acis"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        return args
if 1:   # Core functionality
    def SetupColor():
        t.on = d["-a"] or sys.stdout.isatty()
        on = d["-c"]
        t.rgx = t("lip") if on else ""
        t.wrd = t("magl") if on else ""
        t.syn = t("wht") if on else ""
        t.N = t.n if on else ""
    def BuildThesaurus():
        'Return dict of keyword: synonyms'
        th = {}
        for line in lines:
            a = line.split(",")
            th[a[0]] = a[1:]
        return th
    def FindWord(w):
        r = re.compile(w, re.I if d["-i"] else 0)
        matches = []
        for word in thesaurus:
            mo = r.search(word)
            if mo:
                matches.append(word)
        if matches:
            print(f"{t.rgx}{w}{t.N}")
            if d["-s"]:
                # Print the core word matches and synonyms
                for i in matches:
                    print(f"  {t.wrd}{i}{t.N}")
                    for j in Columnize(thesaurus[i], indent=" "*4):
                        print(f"{t.syn}{j}{t.N}")
            else:
                # Only print the core word matches
                for i in Columnize(matches, indent=" "*2):
                    print(f"{t.wrd}{i}{t.N}")

if __name__ == "__main__":
    file = "/home/Don/bin/mthesaur.txt"
    d = {}      # Options dictionary
    wordlist = ParseCommandLine(d)
    SetupColor()
    lines = open(file).read().split("\n")
    thesaurus = BuildThesaurus()
    for word in wordlist:
        FindWord(word)

'''
Construct the anagrams text file, which is a list of lines containing words
that are anagrams of each other.  This is done by reading a large number
of text files.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        import anagram
        import get
        from timer import Timer
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        t.tm = t("purl")
        t.total = t("yell")
        t.stats = t("grnl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] choice
          choice is a letter.  'd' means to build the debug version.
          Anything else means to build the production version.

          Constructs the anagram file, a sequence of lines that contain
          anagrams from a set of input files.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ah") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        if 0 and not args:
            Usage(status=1)
        return args
    def GetFileString(file):
        "Return string of file, but delete lines beginning with '#'"
        lines = get.GetLines(file, script=True)
        return '\n'.join(lines)

if __name__ == "__main__":
    d = {}      # Options dictionary
    arg = ParseCommandLine(d)
    print("Reading files:")
    if arg == ["d"]:
        # Debug:  just use PnP
        files = [
            "/ebooks/kindle/Austen/Pride_and_Prejudice.txt",
        ]
    else:
        files = [
            "/ebooks/kindle/Austen/*.txt",
            "/ebooks/kindle/Burroughs/*.txt",
            "/ebooks/kindle/Christie/*.txt",
            "/ebooks/kindle/Comedy/*.txt",
            "/ebooks/kindle/Dickens/*.txt",
            "/ebooks/kindle/Doyle/*.txt",
            "/ebooks/kindle/Misc/*.txt",
            "/ebooks/kindle/ScienceFiction/*.txt",
            "/ebooks/kindle/Sherlock_Holmes/*.txt",
            "/ebooks/kindle/Twain/*.txt",
            "/ebooks/kindle/Verne/*.txt",
            "/ebooks/kindle/from_Dave/TheMartian.txt",
            "/ebooks/kindle/from_Dave/WorstJourneyInTheWorld.txt",
            "/ebooks/kindle/from_Dave/herbert/dune/Dune1.txt",
            "/pylib/pgm/words.x.beale.2of12inf",
            "/pylib/pgm/words.2005.wayne",
            "/pylib/pgm/words.additional",
            "/pylib/pgm/words.don",
            "/pylib/pgm/words.x.nltk",
            "/pylib/pgm/words.x.universal",
            "/pylib/pgm/words.x.wordnet",
            "/pylib/pgm/words.x.female_names.nltk",
            "/pylib/pgm/words.x.male_names.nltk",
            "/pylib/pgm/words.x.wordnet",
            "/pylib/pgm/wordlists/*.txt",
        ]
    o, total, numwords = set(), 0, 0
    with Timer() as tm:
        for file in files:
            if "*" in file:
                loc = file.find("*")
                p = P(file[:loc])
                assert(p.is_dir())
                for f in p.glob(file[loc:]):
                    s = GetFileString(f)
                    words = anagram.GetWords(s)
                    numwords += len(words)
                    o = o.union(words)
                    print(f"  {f}")
            else:
                s = GetFileString(file)
                words = anagram.GetWords(s)
                numwords += len(words)
                o = o.union(words)
                print(f"  {file}")
    t.print(f"{t.tm}Reading files took {tm.et} s")
    t.print(f"{t.stats}Read {numwords} words")
    total += tm.et
    print("Getting anagrams")
    with Timer() as tm:
        anagrams = anagram.GetAnagrams(' '.join(o))
    t.print(f"{t.tm}Getting anagrams took {tm.et} s")
    total += tm.et
    print("Writing /plib/pgm/anagrams")
    numwords, numlines = 0, 0
    with Timer() as tm:
        with open("anagrams", "w") as f:
            for item in anagrams:
                numlines += 1
                numwords += len(item.split())
                f.write(item + "\n")
    t.print(f"{t.tm}Writing took {tm.et} s")
    t.print(f"{t.stats}{numlines} anagram lines, {numwords} words on those lines")
    total += tm.et
    t.print(f"{t.total}Total time was {total} s")
    print("Done")

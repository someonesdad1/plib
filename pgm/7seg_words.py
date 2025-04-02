_pgminfo = '''
<oo 
    Show words made from 7-segment letters
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from columnize import Columnize
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.lower = set("bcdhijlnoqrtuy")
        g.upper = set("ABCEFGHIJLNOPSTUXYZ")
        g.descr = P("/words/descriptions")
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [wordlist1 [wordlist2...]]
          Show the words that can be made from 7-segment letters:
            A B C E F G H I J L N O P S T U X Y Z
            b c d h i j l n o q r t u y
          The wordlist(s) to use are regexes to identify the following suffixes:
            additional 2of12inf default 1000 3000 all bsl experimental nawl ngsl nltk
            univ wcf wik1000 
          Use -w to show the descriptions of these wordlists.  Multiple wordlists are
          OR'd together.  Uppercase letters are the default.
        Options:
            -f      Define a word file to use (one word per line)
            -l n    Limit to words of n letters or less
            -U      Show uppercase letter words [default]
            -u      Show lowercase letter words
            -w      Show descriptions of the wordlists
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-f"] = []        # Word file(s) to use (ORs with command line)
        d["-l"] = 0         # Maximum length of word
        d["-U"] = False     # Show uppercase
        d["-u"] = False     # Show lowercase
        d["-w"] = False     # Show descriptions of the wordlists
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "f:l:Uuw")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("w"):
                d[o] = not d[o]
            elif o == "-f":
                file = P(a)
                if not file.exists():
                    print(f"{a!r} does not exist")
                d[o].append(a)
            elif o == "-l":
                try:
                    d[o] = int(a)
                    if d[o] <= 0:
                        raise ValueError()
                except ValueError:
                    Error(f"{a!r} isn't a valid integer > 0")
            elif o == "-U":
                d[o] = True
                d["-u"] = False
            elif o == "-u":
                d[o] = True
                d["-U"] = False
        if d["-w"]:
            print(g.descr.open().read())
            exit(0)
        GetColors()
        return args
if 1:   # Core functionality
    def GetWordsFromFile(file):
        'file must be a pathlib.Path instance'
        words = set(file.open().read().split("\n"))
        if d["-l"]:
            # Keep only words with d["-l"] or less letters
            keep = set()
            for word in words:
                if len(word) <= d["-l"]:
                    keep.add(word)
            words = keep
        return words
    def GetWords(regex):
        files = '''
            /words/words.additional             
            /words/words.beale.2of12inf
            /words/words.default
            /words/words.ef.1000
            /words/words.ef.3000
            /words/words.ngsl.all
            /words/words.ngsl.bsl
            /words/words.ngsl.experimental
            /words/words.ngsl.nawl
            /words/words.ngsl.ngsl
            /words/words.nltk
            /words/words.syllables
            /words/words.univ
            /words/words.wcf
            /words/words.wik1000
        '''
        # Key these by their suffix
        di = {}
        for file in files.split("\n"):
            p = P(file.strip())
            suffix = p.suffix[1:]
            di[suffix] = p
        # Read in the requisite word files
        r = re.compile(regex, re.I)
        words = set()
        for suffix in di:
            mo = r.search(suffix)
            if mo:
                words = words.union(GetWordsFromFile(di[suffix]))
        if not words:
            print(f"{regex!r} didn't match a words file")
        return words
    def GetWordsThatMatch(words):
        # Get the correct case
        wordlist = [i.lower() if d["-u"] else i.upper() for i in words]
        # Select the words that match
        matched = set()
        required_letters = set("bcdhijlnoqrtuy") if d["-u"] else set("ABCEFGHIJLNOPSTUXYZ")
        for word in wordlist:
            if set(word).issubset(required_letters):
                matched.add(word)
        return matched
    def Report(matched):
        for i in Columnize(sorted(matched)):
            print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    regexes = ParseCommandLine(d)
    # Build list of words
    words = set()
    for regex in regexes:
        words = words.union(GetWords(regex))
    # Get user-specified words from files
    for file in d["-f"]:
        words = words.union(GetWordsFromFile(file))
    if not words:
        exit(1)
    matched = GetWordsThatMatch(words)
    Report(matched)

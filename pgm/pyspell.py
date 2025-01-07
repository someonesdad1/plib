'''
Print out misspelled tokens in source code files.
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out misspelled tokens in source code files.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from columnize import Columnize
        import timer
        import get
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
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
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Tokenize the indicated source code files and list the tokens that may be misspelled.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        return args
if 1:   # Classes
    class Token(str):
        'Hold words so they can be sorted in dictionary order'
        def __new__(cls, value, file_number):
            instance = super().__new__(cls, value)
            instance.n = file_number
            return instance
        def __str__(self):
            return super().__str__()
        def __repr__(self):
            return super().__str__() + f"<{self.n}>"
        def __lt__(self, other):
            return self.lower() < other.lower()
if 1:   # Core functionality
    def GetWordlist():
        'Load the default set of words'
        g.wordlist = set()
        # Remove any underscores
        for w in open("/donrepo/words/words.univ").read().split():
            g.wordlist.add(w.replace("_", ""))
    def SplitOnCapitals(word):
        assert "_" not in word
        capitals = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        # Method:  create a new list of the word's letters with a space character before each
        # capital letter, then split it into a list of words.
        w, o = list(word), []
        o = []
        for i in word:
            o.append(f" {i}") if i in capitals else o.append(f"{i}")
        return ''.join(o).split()
    def IsMisspelled(word):
        '''Check the indicated word for a misspelling.  Split it on '_' if it contains
        underscores.  If not, split it on uppercase letters and spell check each token.
        The spell checking method is to first see if it's in the set of words.  If not,
        change the word to all lowercase.
        '''
        if "_" in word:
            bad = []
            for w in word.split("_"):
                if IsMisspelled(w):
                    return True
            return False
        else:
            if word in g.wordlist or word.lower() in g.wordlist:
                return False
            for word in SplitOnCapitals(word):
                if word not in g.wordlist and word.lower() not in g.wordlist:
                    return True
            return False
    def DebugPrintTokens(words):
        o = []
        for i in sorted(words):
            o.append(str(i))
        for i in Columnize(o):
            print(i)
    def SortTokens(words):
        'Sort the tokens in dictionary order'
        return list(sorted(words))
    def Report(misspelled, files):
        if not misspelled:
            return
        print("File            Word")
        print("------   --------------------")
        # Print the words (they are in folded sort order)
        for word in misspelled:
            print(f"{word.n:^6d}   {word}")
        print(f"\nFile numbers:")
        for i, file in enumerate(files):
            print(f"{i:^6d}   {file}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    GetWordlist()
    # The words to be checked will be in the words set, which will be (n, word) where n is the
    # number of the file it came from.
    words = set()
    for n, file in enumerate(files):
        text = open(file).read()
        dq = get.Tokenize(text)
        for token in dq:
            if ii(token, get.wrd):
                words.add(Token(token, n))
    if 0:
        DebugPrintTokens(words)
        exit()
    # Report the words that seem to be misspelled
    misspelled = set()
    for word in words:
        if IsMisspelled(word):
            misspelled.add(word)
    misspelled = SortTokens(misspelled)
    Report(misspelled, files)

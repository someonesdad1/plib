_pgminfo = '''
<oo 
    Find duplicated words in a file.  'the the' is duplicated, but 'The the' is not.
    A legitimate example is 'that that', but most of the time you'd want it flagged.

    Algorithm:  read whole file in as a string, split on whitespace to get the words,
    then look for matches.
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
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
        import dpstr
        from f import flt
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
        g.punc = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
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
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
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
        GetColors()
        return args
if 1:   # Classes
    class Word:
        def __init__(self, word, linenum):
            self.word = word
            self.linenum = linenum
        def __repr__(self):
            return repr(self.word)
        def __str__(self):
            return self.word
        def __eq__(self, other):
            return self.word == other.word
if 1:   # Core functionality
    def RemovePunc(word_instance):
        s = dpstr.RemoveEndingChars(str(word_instance), g.punc)
        s = dpstr.RemoveStartingChars(s, g.punc)
        return s
    def Process(file):
        lines = open(file).read().split("\n")
        # Fill a list with Word instances
        o = []
        for i, line in enumerate(lines):
            for word in line.split():
                o.append(Word(word, i + 1))
        if 0:   #xx
            print(o)
        # Analyze these words
        for i in range(len(o)):
            if not i:
                continue
            # Find exact copies
            if o[i] == o[i - 1]:
                t.print(f"{t.ornl}[{file}:{o[i - 1].linenum}]:  {o[i - 1]}")
                continue
            # Find copies with ending punctuation removed
            a, b = RemovePunc(o[i]), RemovePunc(o[i - 1])
            if (a and b) and (a == b):
                t.print(f"{t.sky}[{file}:{o[i - 1].linenum}]:  {o[i - 1]}")
                continue

if 0:   # xx
    s = '"Hello,"'
    print(RemovePunc(s))
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        Process(file)

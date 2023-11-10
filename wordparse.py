'''
Provides WordParse(string) to get a list of words in the string.

Run as a script to print a set of the words in the files given on the
command line.
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
        from collections import deque
        import getopt
        import os
        from pathlib import Path as P
        import string
        import sys
    if 1:   # Custom imports
        from asciify import Asciify
        from wrap import dedent
        from color import t
        from columnize import Columnize
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        punc = set(string.punctuation)
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
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
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def FixWord(word):
        'Remove leading and trailing punctuation'
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
        return ''.join(dq)
    def WordParse(s, ic=False):
        '''Returns a set of words from the string s.
        ic      Ignore case if True
        '''
        if ic:
            s = s.lower()
        words = set(s.split())
        new_words = set()
        for w in words:
            word = FixWord(w)
            if word:
                new_words.add(word)
        return new_words

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    words = set()
    for file in files:
        if file == "-":
            s = sys.stdin.read()
        else:
            s = open(file).read()
        s = Asciify(s)
        words.update(WordParse(s))
    for i in Columnize(sorted(words)):
        print(i)

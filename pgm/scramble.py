'''

Scramble the letters of plain text.  An option lets you leave the first and
last letters of a word alone.  Each file on the command line is processed
in sequence, sending the processed text to stdout.  If no files are given,
stdin is read.

Algorithm

- Read in the string
- Create a list containing (offset, char) each punctuation character.
- Replace each punctuation character with a space.
- Split into words on spaces.
- Scramble the letters in each word.
- Reinsert the punctuation characters.

'''
'''
Description of program
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
        # Scramble the letters of plain text files.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from pprint import pprint as pp
        import random
        import string
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from asciify import Asciify
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        punctuation = set(string.punctuation)
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
          Scramble the letters in words of the text files.  Use '-' to read
          from stdin.
        Options:
            -a      'ASCIIfy' the file by changing Unicode characters to
                    their ASCII equivalents.
            -f      Leave the first and last letters alone.
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # ASCIIfy the input file(s)
        d["-f"] = False     # Leave first and last letters alone
        d["-s"] = None      # Seed for random number generator
        try:
            opts, files = getopt.getopt(sys.argv[1:], "afhs:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("af"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
            elif o == "-s":
                d[o] = a
        if not files:
            Usage()
        return files
if 1:   # Core functionality
    def ProcessFile(file):
        s = sys.stdin.read() if file == "-" else open(file).read()
        if d["-a"]:
            s = Asciify(s)
        # Find each punctuation character [(offset, char)]
        pchars, R = [], range(len(s))
        for i in range(len(s)):
            if s[i] in punctuation:
                pchars.append((i, s[i]))
        # Replace each punctuation character with a space
        sl = list(s)
        for i, c in pchars:
            sl[i] = " "
        # Make new string and split into words
        words = ''.join(sl).split()
        # Scramble the letters in the words
        for i in range(len(words)):
            words[i] = Scramble(words[i])
        # Reinsert punctuation
        tl = list(' '.join(words))
        for i, c in pchars:
            tl[i] = c
        pp(tl)
    def Scramble(word):
        # If short word, don't bother
        n = 4 if d["-f"] else 3
        if len(word) < n:
            return word
        # OK, needs scrambling
        w = list(word)
        if d["-f"]:
            first, last = w[0], w[-1]
            w = w[1:-1]
        random.shuffle(w)
        if d["-f"]:
            w.insert(0, first)
            w.append(last)
        return ''.join(w)

random.seed(0) #xx

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)

'''
Change a wordlist into words that an Igor would say.  Inspiration from 
Terry Pratchett's "Fifth Elephant" and other Discworld stories
containing Igors.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# Put test file information here (see 0test.py) #∞test∞#
    pass
if 1:   # Standard imports
    from collections import deque
    import getopt
    import os
    import pathlib
    import re
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent, indent, Wrap
    from globalcontainer import Global, Variable, Constant
    from get import GetLines
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    G = Global()
    G.ro = Constant()
    G.rw = Variable()
    P = pathlib.Path
if 1:   # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
    Usage:  {name} [options] [file1 [file2...]]
      Turn the files' content into words that Igor would say.  Mostly,
      this is done by changing 's' characters into 'sh'.  Inspiration
      from Terry Pratchett's "Fifth Elephant" and other Discworld
      stories containing Igors.
      
    Options:
        -h          Print a manpage.
        -w dict     Specify the word file
    '''))
        exit(status)
    def ParseCommandLine(d):
        try:
            opts, files = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                Usage(d, status=0)
        if not files:
            Usage(d)
        return files
if 1:   # Core functionality
    def ProcessWord(word):
        word1 = word.replace("ss", "th").replace("s", "th")
        word2 = word1.replace("S", "Th")
        # Print the word to stderr if it contains a 'c' character
        # in the interior
        loc = word2.find("c")
        if loc != -1 and (loc != 0 and loc != len(word) - 1):
            c_words.append(word2)
        return word2
    def ProcessLine(line):
        words = deque()
        for word in line.split():
            words.append(ProcessWord(word))
        print(' '.join(words))
    def ProcessFile(file):
        lines = open(file).read().split("\n")
        for line in lines:
            ProcessLine(line)
if __name__ == "__main__":
    d = {}      # Options dictionary
    c_words = []
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)
    for item in sorted(set(c_words)):
        print(item, file=sys.stderr)

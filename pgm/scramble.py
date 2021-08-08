'''
Script to scramble the letters in words, leaving the first and last letter
the same.

Each file on the command line is processed in sequence, sending the
processed text to stdout.  If no files are given, stdin is read.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2009 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Scrambles the internal letters in words, leaving the first and last
    # letters alone.  Some text may still be readable; some may not.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import re
    import sys
    import random
def repl(m):
    '''This method is from the python documentation on the re module (the
    section called "Text Munging").
    '''
    inner_word = list(m.group(2))
    random.shuffle(inner_word)
    return m.group(1) + "".join(inner_word) + m.group(3)
if __name__ == "__main__":
    if len(sys.argv) == 1:
        for line in sys.stdin.readlines():
            print(re.sub(r"(\w)(\w+)(\w)", repl, line), end="")
    else:
        lines = []
        for filename in sys.argv[1:]:
            for line in open(filename).readlines():
                print(re.sub(r"(\w)(\w+)(\w)", repl, line), end="")

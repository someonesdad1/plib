'''
Change a sequence of letters into numbers and vice versa per the phone's
correspondence.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Change a sequence of letters into numbers and vice versa per the
    # phone dial's correspondence.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import string
    import sys
    import itertools
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
if 1:   # Global variables
    numbers = {
        "1": (".",),
        "2": ("a", "b", "c"),
        "3": ("d", "e", "f"),
        "4": ("g", "h", "i"),
        "5": ("j", "k", "l"),
        "6": ("m", "n", "o"),
        "7": ("p", "q", "r", "s"),
        "8": ("t", "u", "v"),
        "9": ("w", "x", "y", "z"),
        "0": ("0",),
    }
    letters = {}
    for n in numbers:
        for l in numbers[n]:
            letters[l] = n
    word_dict = "/pylib/pgm/words.x.universal"
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] letters
      Changes the letters into numbers or numbers into letters per the
      correspondence between digits and letters on a phone dial:
      abc:2, def:3, ghi:4, jkl:5, mno:6, pqrs:7, tuv:8, wxyz:9
      The resulting words are only printed if they are in the dictionary
      {word_dict}.
    Options:
      -a    List all "words" found
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-a"] = False     # Letter combinations must be in dictionary
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("a"):
            d[o] = not d[o]
    return args
def Search(chars, d):
    # First character decides whether it's letters or numbers
    if chars[0].lower() in set(string.ascii_lowercase):
        for c in chars.lower():
            if c not in set(string.ascii_lowercase):
                Error(f"'{chars} is not all letters")
        SearchLetters(chars.lower(), d)
    elif chars[0] in set(string.digits):
        for c in chars:
            if c not in set(string.digits):
                Error(f"'{chars} is not all numbers")
        SearchNumbers(chars, d)
    else:
        Error("First character not a letter or a number")
def SearchLetters(chars, d):
    for c in chars:
        print(letters[c], end="")
    print()
def SearchNumbers(nums, d):
    items = []
    for n in nums:
        items.append(numbers[n])
    results = []
    # The desired output is the Cartesian product of each of the sets of
    # letters associated with each digit.  The itertools module provides
    # this functionality.
    for i in itertools.product(*items):
        s = ''.join(i)
        results.append(s)
    if not d["-a"]:
        # Must be in dictionary to print out
        words = []
        for line in open(word_dict):
            line = line.strip()
            if not line or line[0] == "#":
                 continue
            words.append(line.lower())
        words = set(words)
        new_results = []
        for item in results:
            if item in words:
                new_results.append(item)
        if sys.stdout.isatty():
            for line in Columnize(new_results):
                print(line)
        else:
            for line in new_results:
                print(line)
    else:
        for line in Columnize(results):
            print(line)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        Search(arg, d)

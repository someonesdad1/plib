"""
Select a word randomly from the word file
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Select a word randomly from the word file
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import os
    import string
    import sys
    import getopt
    import random
    from pdb import set_trace as xx
if 1:  # Custom imports
    import dpstr
    from wrap import dedent
    from columnize import Columnize
    from get import GetWords
    from util import RandomIntegers
if 1:  # Global variables
    PunctuationFilter = dpstr.FilterStr(
        string.punctuation, " " * len(string.punctuation)
    )


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} n
      Select n words randomly from a words file.  The list of words won't
      be repeatable unless you use -s.  There are about 94 kwords in the
      default wordlist.
    Options
      -1        Use WordNet wordlist (147 kwords)
      -2        Use large dictionary (511 kwords)
      -h        Comments on use
      -i        Ignore case (all words are lowercase)
      -l        Print one word per line instead of in columns
      -o        Sort the output
      -s seed   Seed the random number generator
      -w file   Use a different word file (more than one -w OK)
    """)
    )
    exit(status)


def Manpage():
    print(
        dedent(
            f"""
    This script produces a sequence of n random words where n is the
    integer argument on the command line.  When n is a small number, you
    might be able to use the set of words as a passphrase.  For example, 
    'python {sys.argv[0]} -s 0 4' produces the list of words

        loathes boorish gabions loggia

    Modern password requirements often require a combination of upper and
    lower case letters, digits, and punctuation characters.  This
    requirement could be met by e.g. 

        Loathes:boorish:gabions:loggia:42

    Even if someone knew you were using a dictionary of 93 kwords and you
    used 4 words, they'd have to check over 1e18 combinations of words.  If
    they knew you used capital letters and punctuation, the task would be
    far, far larger.

    For folks who like words and definitions, using the dictionary used by
    the -1 or -2 option and, say, 50 words produces a list of words that
    will challenge your abilities to know what they mean.  The number of
    combinations of 50 words from the -2 dictionary is on the order of
    1e220, a gigantic number of possibilities.  You'll rarely see a word
    duplicated between samples, so this scheme could provide a nearly
    unlimited number of lists of words for various purposes.  I have a
    fairly good vocabulary and a few samples of 50 word lists show me that
    I typically recognize less than half of the words -- and that includes
    making guesses as to what a word means based on its components.

    The -w option lets you choose your own word file (you can have more
    than one -w option).  The file is read in as a string and space
    characters are substituted for punctuation characters.  The words are
    gotten by splitting on whitespace.  This algorithm lets you use nearly
    any text file as a source of words.

    """.rstrip()
        )
    )
    exit(0)


def ParseCommandLine(d):
    d["-1"] = False
    d["-2"] = False
    d["-i"] = False
    d["-l"] = False
    d["-o"] = False
    d["-s"] = None
    d["-w"] = []
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "12hilos:w:")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "12lio":
            d[o] = not d[o]
        elif o == "-h":
            Manpage()
        elif o == "-s":
            d["-s"] = a
        elif o == "-w":
            d["-w"].append(a)
    if not args:
        Usage()
    if d["-1"] and d["-2"]:
        d["-2"] = False
    try:
        n = int(args[0])
        if n < 1:
            raise Exception()
    except Exception:
        Error(f"'{args[0]}' is not a proper integer > 0")
    return n


def GetWordList():
    "Return the chosen list of words"
    # Choose word list
    if d["-w"]:
        # User defined word list(s)
        w = set()  # Use a set to eliminate duplicates
        for file in d["-w"]:
            s = open(file).read()
            if d["-i"]:
                s = s.lower()
            w.update(set(PunctuationFilter(s).split()))
        # We need to sort to allow the -s option to work because we used a
        # set and the ordering of a set is different on each invocation.
        w = list(sorted(w))
    else:
        if d["-2"]:
            # file = "/pylib/pgm/words.x.universal"
            file = "/words/words.univ"
        elif d["-1"]:
            # file = "/pylib/pgm/words.x.wordnet"
            file = "/words/words/words.nltk"
        else:
            # file = "/pylib/pgm/words"
            file = "/words/words.default"
        w = GetWords(file, ignore=[r"^\s*#"])
    if d["-i"]:
        w = [i.lower() for i in w]
    return w


def GetSample(n):
    w = GetWordList()
    N = len(w)
    if d["-s"] is not None:
        random.seed(d["-s"])
        sample = random.sample(w, n)
    else:
        sample = []
        for i in RandomIntegers(n, len(w)):
            sample.append(w[i])
    if d["-o"]:
        sample = list(sorted(sample))
    return sample


if __name__ == "__main__":
    d = {}  # Options dictionary
    n = ParseCommandLine(d)
    sample = GetSample(n)
    for i in sample if d["-l"] else Columnize(sample, horiz=True):
        print(i)

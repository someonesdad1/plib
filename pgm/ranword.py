'''
Select a word randomly from the word file
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Select a word randomly from the word file
    ##∞what∞#
    ##∞test∞# #∞test∞#
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
        string.punctuation, " "*len(string.punctuation)
    )
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Manpage():
    print(dedent(f'''
    This script produces a sequence of n random words where n is the integer argument on
    the command line.  When n is a small number, you might be able to use the set of
    words as a passphrase.  For example, 'python {sys.argv[0]} -s 0 4' produces the list
    of words
    
        loathes boorish gabions loggia
        
    Modern password requirements often require a combination of upper and lower case
    letters, digits, and punctuation characters.  If your birth year was 72, you could
    meet this requirement by e.g.
    
        Loathes;Boorish;Gabions;Loggia;72

    Unfortunately, most password prompts are poorly written and disallow numerous
    desirable characters or restrict you to stupidly small lengths.
        
    Even if someone knew you were using a dictionary of 93 kwords and you used 4 words,
    they'd have to check over 1e18 combinations of words.  If they knew you used capital
    letters, digits, and punctuation, their task would be much larger.
    
    For folks who like words and definitions, using the dictionary used by the -3 or -4
    option and, say, 50 words produces a list of words that will challenge your
    abilities to know what they mean.  The number of combinations of 50 words from these
    wordlists is gigantic, more than the estimated number of atoms in the universe.  You'll
    rarely see a word duplicated between samples, so this scheme could provide a nearly
    unlimited number of lists of words for various purposes.
    
    The -f option lets you choose your own word file (you can have more than one -f
    option).  The file is read in as a string and space characters are substituted for
    punctuation characters.  The words are gotten by splitting on whitespace.  This
    algorithm lets you use nearly any text file as a source of words.
    
    '''.rstrip()
        )
    )
    exit(0)
def Usage(status=1):
    name = sys.argv[0]
    print(
        dedent(f'''
    Usage:  {name} n
      Select n words randomly from a words file.  The list of words won't be repeatable
      unless you use -s.  The wordlists are from /words (see /words/descriptions).
    Options (number in square brackets is number of kwords in wordlist)
      -0        words.ngsl.all [5]   (default)
      -1        words.ef.3000 [3]
      -2        words.beale.2of12inf [82]
      -3        words.nltk [242]
      -4        words.univ [302]
      -F file   Use a file to specify wordlist files to read in
      -f file   Use a different word file (more than one -f OK)
      -h        Comments on use
      -i        Ignore case (all words are lowercase)
      -l        Print one word per line instead of in columns
      -o        Sort the output
      -s seed   Seed the random number generator
    Wordlists
      If you specify files with the -F or -f options, these files will be read in and
      any punctuation characters from string.punctuation will be replaced by space
      characters; then the files will be split on whitespace.
    ''')
    )
    exit(status)
def ParseCommandLine(d):
    d["-0"] = False     # words.ngsl.all
    d["-1"] = False     # words.ef.3000
    d["-2"] = False     # words.beale.2of12inf
    d["-3"] = False     # words.nltk
    d["-4"] = False     # words.univ
    d["-f"] = []        # Define a words file
    d["-i"] = False     # Ignore case
    d["-l"] = False     # Print one word per line
    d["-o"] = False     # Sort the output
    d["-s"] = None      # Seed the random number generator
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "01234f:hilos:")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "01234lio":
            d[o] = not d[o]
        elif o == "-h":
            Manpage()
        elif o == "-s":
            d["-s"] = a
        elif o == "-f":
            d["-f"].append(a)
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
    if d["-f"]:     # User defined word list(s)
        w = set()
        for file in d["-f"]:
            s = open(file).read()
            if d["-i"]:
                s = s.lower()
            w.update(set(PunctuationFilter(s).split()))
    else:
        file = "words.ngsl.all"
        if d["-0"]:
            file = "words.ngsl.all"
        elif d["-1"]:
            file = "words.ef.3000"
        elif d["-2"]:
            file = "words.beale.2of12inf"
        elif d["-3"]:
            file = "words.nltk"
        elif d["-4"]:
            file = "words.univ"
        w = GetWords("/words/" + file, ignore=[r"^\s*#"])
    if d["-i"]:
        w = [i.lower() for i in w]
    # We need a sorted list to allow the -s option to work because we used
    # sets and the ordering of a set is different on each invocation.
    w = list(sorted(w))
    return w
def GetSample(n):
    '''Select a random sample of n words.  Unless the -s option is used, the
    random.SystemRandom() generator is used, which uses os.urandom() behind the scenes.
    If -s is used, then random.seed() is used to set a known, repeatable state.
    '''
    if d["-s"] is not None:
        random.seed(d["-s"])
    sample = random.sample if d["-s"] else random.SystemRandom().sample 
    w = GetWordList()
    random_sample = sample(w, n)
    if d["-o"]:
        random_sample = list(sorted(random_sample, key=str.lower))
    return random_sample
if __name__ == "__main__":
    d = {}  # Options dictionary
    n = ParseCommandLine(d)
    sample = GetSample(n)
    for i in sample if d["-l"] else Columnize(sample):
        print(i)

'''
Spell-checking script
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Spell-checking script
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports & globals
    import getopt
    import os
    import pathlib
    import string
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from asciify import Asciify
    import get
    from columnize import Columnize
if 1:   # Global variables
    wordlist = {
        "additional": "/words/words.additional",
        0: "/words/words.ngsl.experimental",
        1: "/words/words.beale.2of12inf",
        2: "/words/words.univ",
    }
    default_wordlist = 1
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def BuildTranslate(d):
    '''Construct the d["trans"] dictionary used to translate the strings
    to be read to tokenize.
    '''
    d["trans"] = t = {}
    for c in string.punctuation:
        t[ord(c)] = " "
    for c in string.whitespace:
        if c == " ":
            continue
        t[ord(c)] = " "
    if d["-d"]:
        for c in string.digits:
            t[ord(c)] = None
    if d["-h"]:
        del t[ord("-")]
def Usage(d, status=1):
    wl = "-" + str(default_wordlist)
    # Get names of wordlists
    def P(p):
        return pathlib.Path(p).name
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 [file2 ...]
      Spell check the indicated files by replacing non-letters with space
      characters and tokenizing on whitespace.  Use '-' to read stdin.
      Default wordlist is {wl}.  Case is ignored by default.
    Options:
      -0    Basic dictionary          {P(wordlist[0])}
      -1    Medium-size dictionary    {P(wordlist[1])}
      -2    Large dictionary          {P(wordlist[2])}
      -a    Apply Asciify() to tokens
      -d    Don't remove digit characters in tokens
      -h    Don't replace hyphen with space
      -i    Don't ignore case of tokens
      -k    Columnize output
      -n    Shows tokens in dictionary
      -s    Only print the number misspelled
      -u    Ignore tokens with non-7-bit characters
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-0"] = False
    d["-1"] = False
    d["-2"] = False
    d["-a"] = False
    d["-d"] = True
    d["-h"] = False
    d["-i"] = True
    d["-k"] = False
    d["-n"] = False
    d["-s"] = False
    d["-u"] = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "012adhiknsu")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("012adhiknsu"):
            d[o] = not d[o]
    if not d["-0"] and not d["-1"] and not d["-2"]:
        d["-" + str(default_wordlist)] = True
    if not args:
        Usage(d)
    return args
def GetWordlists(d):
    # regex ignores comments; convert to lowercase if d["-i"] is True
    regex = r"^\s*#"
    wl = set()
    wl.update(get.GetWords(wordlist["additional"], ignore=[regex]))
    if d["-0"]:
        wl.update(get.GetWords(wordlist[0], ignore=[regex]))
    if d["-1"]:
        wl.update(get.GetWords(wordlist[1], ignore=[regex]))
    if d["-2"]:
        wl.update(get.GetWords(wordlist[2], ignore=[regex]))
    d["words"] = wl
    if d["-i"]:
        wl = set([i.lower() for i in wl])
def ProcessFile(file, d):
    s = sys.stdin.read() if file == "-" else open(file).read()
    if d["-i"]:
        s = s.lower()
    t = s.translate(d["trans"])
    for word in t.split():
        w = Asciify(word) if d["-a"] else word
        if d["-a"] and w != word:
            W = f"{w} ({word})"
        else:
            W = word
        if w in d["words"]:
            d["correct"].add(W)
        else:
            d["incorrect"].add(W)
def Report(d):
    words = d["correct"] if d["-n"] else d["incorrect"]
    if d["-k"]:
        for i in Columnize(sorted(words)):
            print(i)
    elif d["-s"]:
        if d["-n"]:
            print(f"{len(words)} correctly spelled")
        else:
            print(f"{len(words)} misspelled")
    else:
        for i in sorted(words):
            print(i)
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    BuildTranslate(d)
    GetWordlists(d)
    data = []
    d["correct"] = set()
    d["incorrect"] = set()
    for file in files:
        ProcessFile(file, d)
    Report(d)

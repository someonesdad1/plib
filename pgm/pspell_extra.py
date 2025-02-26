"""
Load the symbols from pspell.extra and identify duplicates
"""

from get import GetLines


def LoadWords():
    "Return list of (linenum, word)"
    mywords = []
    with open("pspell.extra") as f:
        for linenum, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for word in line.split():
                mywords.append((word, linenum))
    return mywords


def GetWords(mywords):
    "Return a set of lowercase words in mywords"
    words = set()
    for word, linenum in mywords:
        words.add(word.lower())
    return words


def Analyze(words, mywords):
    "Print out duplicates"
    found = set()
    for word, linenum in mywords:
        w = word.lower()
        if w in found:
            print(linenum, word)
        else:
            found.add(w)


mywords = LoadWords()
words = GetWords(mywords)
Analyze(words, mywords)

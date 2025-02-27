"""
Index to Lautard's TMBR

    The index was taken from
    http://machinistindex.com/Metalworking_index_2000.txt, a defunct
    website.  The text included the name "Joe Landau's Metalworking Index
    2000 Edition", so maybe someone else has archived it on the web.

    Todo:
        - Collapse entries like 'Dial' and 'dial' into one.  Give the
          capitalized word precedence.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Index to Lautard's books
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import re
    import string
if 1:  # Custom imports
    from wrap import dedent
    from tmbr_data import data
    from columnize import Columnize


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] regexp
      Look up topics in Lautard's "The Machinist Bedside Reader" books.
      Matches are printed to stdout.  Use the command '{sys.argv[0]} .'
      to list all the entries.  TMBR#3:72 means volume 3, page 72.
      HTIM:45 means "Hey, Tim...", a small 1990 51 page book.
    Options:
      -i    Make the search case-sensitive
      -x    Print a concordance to stdout
    """)
    )
    exit(status)


def ParseCommandLine():
    d["-i"] = True  # Ignore case
    d["-x"] = False  # Generate index
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ix")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "ix":
            d[o] = not d[o]
    if d["-x"]:
        GenerateConcordance(d)
        exit(0)
    if not args:
        Usage()
    return args


def PrintMatches(regexp):
    f = re.I if d["-i"] else 0
    r = re.compile(regexp, f)
    for i in data:
        title, loc = i
        mo = r.search(title)
        if mo:
            print(title, loc)


def FilterWords(words):
    """Remove words we don't want to keep.  words is a sequence of
    words.
    """
    remove = set(
        """
        'flat 's - /or 0 018 1 1/4 118 15/16 160 1st 2 240 3 3/4 3000
        490 5161 6th 7/8 75 9 900 a after against ago ahead aid aided al
        along an and any are as at back be before big by c c/p can co
        come d dark de do does don't down el etc for from get half have
        her how i if in inc into is it its m22 may might more my not of
        on one ones only onto or other out over own p per pre re ref s
        see self so some t takes than that the then there there's they
        things this thou to too two up upon use used useful uses using v
        very vs w/ was we what what when where which while why why/where
        with without you your
    """.split()
    )
    words = set(words)
    keep = set()
    for word in words:
        if word.lower() in remove:
            continue
        keep.add(word)
    return keep


def Split(line):
    """Return a sequence of words from the line after replacing
    punctuation, etc. with spaces.  Also weed out lines that aren't to
    be used, so the returned sequence could be empty.
    """
    p = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    p = string.punctuation
    for i in "/-'":
        p = p.replace(i, "")
    for i in p:
        line = line.replace(i, " ")
    words = line.split()
    return FilterWords(words)


def NormalizeRefs(refs):
    "Split on ';', then sort"
    out = []
    for i in refs:
        for j in i.split(";"):
            out.append(j.strip())
    return list(sorted(set(out)))


def GenerateConcordance(d):
    "Print a concordance to stdout"
    # Get all the words in the descriptions
    words = set()
    for text, vol in data:
        words.update(Split(text))
    words = list(sorted(words))
    for word in words:
        refs = []
        for text, ref in data:
            if word.lower() in text.lower():
                refs.append(ref)
        if refs:
            print(word)
            sep = " " * 2
            refs = NormalizeRefs(refs)
            for line in Columnize(refs, indent=sep, sep=sep):
                print(line)
    exit(0)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    for regexp in args:
        PrintMatches(regexp)

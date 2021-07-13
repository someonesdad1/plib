'''
Print out minimum strings to identify a set of tokens
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
    # Print out minimum strings to identify a set of tokens
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from collections import defaultdict
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from bidict import bidict
def CommonPrefix(*s):
    "Return the common prefix to the strings in s or '' if None"
    return os.path.commonprefix(s)
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 [file2 ...]
      The files contain tokens separated by whitespace.  Print out a minimum
      set of strings that can be used to identify each token.  The intended use
      is to help you design a command set for a program.  Use '-' to read from
      stdin.  Case is ignored.
    Options:
      -h      Print an example
      -i      Don't ignore the case of the tokens
      -D      Flag duplicate tokens to stderr
    '''))
    exit(status)
def Manpage():
    print(dedent(f'''
    Suppose the following commands were in a file: 
        cost      material  shape
        dump      number    size
        help      quit      units
        length    reset
    Running this script on the file produces the following output:
        Unique commands:
            q   quit
            r   reset
            l   length
            u   units
            h   help
            c   cost
            m   material
            d   dump
            n   number
        Remaining commands:
            s   ['size', 'shape']
    Using a tool like cmddecode.py, you'd then be able to have a command
    set where users could type in single character commands except for
    those starting with 's', which would need two characters to identify
    the command.
    '''))
    exit(0)
def ParseCommandLine(d):
    d["-D"] = False
    d["-i"] = False
    d["-h"] = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Dhi")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "Dih":
            d[o] = not d[o]
    if d["-h"]:
        Manpage()
    if not args:
        Usage(d)
    return args
def ReadTokens(file, d):
    '''Read the tokens in from the indicated file, splitting first on
    newlines then on spaces.  Add to the set d["tokens"].
    '''
    s = sys.stdin.read() if file == "-" else open(file, "r").read()
    T, msg = d["tokens"], set()
    for num, line in enumerate(s.split("\n")):
        l = line.split()
        if d["-i"]:
            l = [i.lower() for i in l]
        # Check for duplication
        for token in l:
            if token in T and token not in msg and d["-D"]:
                m = f"Token '{token}' in file '[{file}:{num}]' already defined"
                print(m, file=sys.stderr)
                msg.add(token)
            T.add(token)
def Split(tokens):
    '''tokens is a dictionary of tokens.  The keys are the first
    characters of the tokens and the values are the tokens that begin with
    that character.  Return (unique, not_unique) where unique is a list
    of tuples (token, first_char) and not_unique is the tokens
    dictionary with the unique tokens removed.
    '''
    unique = []
    for token in tokens:
        if len(tokens[token]) == 1:
            first_letter = tokens[token][0]
            unique.append((token, first_letter))
    # Remove these from tokens
    for token, letter in unique:
        del tokens[token]
    # Find any remaining tokens of length 1:  they need to be removed
    # too.
    for letter in tokens:
        if letter in tokens[letter]:
            tokens[letter].remove(letter)
            unique.append((letter, letter))
    # Consistency:  all tokens in the lists must have a length > 1
    for letter in tokens:
        assert(all([len(i) > 1 for i in tokens[letter]]))
    return unique, tokens
def Process1(tokenset):
    '''Find a minimal set of strings which can identify the set
    of tokens.  tokenset is a set of tokens.

    Method:  use a bidict to store the token's abbreviations.
    '''
    tokens = tokenset.copy()
    dbg = 0
    if dbg:
        print("Starting token set:")
        for i in Columnize(list(tokens)):
            print(i)
    results = bidict()
    # Remove tokens with single letters
    for i in [i for i in tokens if len(i) == 1]:
        results[i] = i
        tokens.discard(i)
    if dbg:
        print("Tokens after single character removal:")
        for i in Columnize(list(tokens)):
            print(i)
        pp(results)
    # Put in dict keyed by first letter
    d = defaultdict(list)
    for i in tokens:
        first_letter = i[0]
        d[first_letter].append(i[1:])
    if dbg:
        print("Dict keyed by first letter:")
        pp(d)
def Process(tokenset):
    '''Find a minimal set of strings which can identify the set
    of tokens.  tokenset is a set of tokens.
    '''
    # unique will be a list of (token, abbreviation) pairs.
    tokendict, unique = defaultdict(list), []
    for i in tokenset:
        tokendict[i[0]].append(i)
    unique, remaining = Split(tokendict)
    if 0:
        print("Tokens:")
        pp(tokenset)
        print("Unique:")
        pp(unique)
        print("Remaining:")
        pp(remaining)
    # Put any length 1 list commands into unique
    more = []
    for letter in remaining:
        if len(remaining[letter]) == 1:
            w = remaining[letter][0]
            more.append((w, w))
    if more:
        unique.extend(more)
        for i in more:
            del remaining[i[0][0]]
    print("Unique commands:")
    for a, b in unique:
        print(f"    {a}   {b}")
    print("Remaining commands:")
    for k in remaining:
        print(f"    {k}   {remaining[k]}")
if __name__ == "__main__":
    d = {      # Options dictionary
        "tokens": set(),
    }
    files = ParseCommandLine(d)
    for file in files:
        ReadTokens(file, d)
    Process(d["tokens"])

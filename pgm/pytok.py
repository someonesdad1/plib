"""
Tokenize the input file and print out the tokens that are symbols in
the indicated python modules.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2018 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Show tokens in an input file that are in python modules named on the command line
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from string import punctuation
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from dpstr import RemoveFilter
    from columnize import Columnize


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] inputfile module1 [module2 ...]
      For the tokens from inputfile, show those that are in the given python
      modules.  Tokenizing is done by replacing all punctuation with space
      characters and then tokenizing on space characters.
    Options:
      -i    Ignore case
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-i"] = False  # Ignore case
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-i",):
            d["-i"] = not d["-i"]
    if len(args) < 2:
        Usage(d)
    return args


def GetModuleSymbols(module, d):
    exec("import " + module)
    symbols = set(eval(module + ".__dict__"))
    if d["-i"]:
        symbols = set([i.lower() for i in symbols])
    delete = []
    for sym in symbols:
        if sym.startswith("__"):
            delete.append(sym)
    for i in delete:
        symbols.remove(i)
    return symbols


def GetInputTokens(d):
    s = open(d["input_file"]).read().replace("\n", " ")
    for char in punctuation:
        s = s.replace(char, " ")
    if d["-i"]:
        s = s.lower()
    return set(s.split())


def CheckModule(module, d):
    symbols, tokens = GetModuleSymbols(module, d), d["tokens"]
    matches = list(sorted(list(symbols.intersection(tokens))))
    width = max([len(i) for i in matches])
    if matches:
        print(module + ":")
        for i in Columnize(matches, indent=" " * 4, col_width=width + 2):
            print(i)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    d["input_file"] = args[0]
    modules = args[1:]
    d["tokens"] = GetInputTokens(d)
    for module in modules:
        CheckModule(module, d)

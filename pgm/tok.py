"""
Tokenize files on whitespace
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Tokenize files on whitespace
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import sys
if 1:  # Custom imports
    from wrap import wrap, dedent
if 1:  # Utility

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file1 [file2 ...]
          Tokenize files on whitespace.
        Options:
            -i      Ignore case (all tokens will be lower case)
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-i"] = False  # Ignore case if true
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "i")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
        return files


if 1:  # Core functionality

    def GetTokens(file, tokens):
        s = open(file).read()
        if d["-i"]:
            s = s.lower()
        t = set(s.split())
        tokens.update(t)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    tokens = set()
    for file in files:
        GetTokens(file, tokens)
    if tokens:
        print("\n".join(sorted(list(tokens))))

'''
Generate a tags file for various types of files:
    dBase
    BASIC
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Generate a tags file for various types of files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import re
    import getopt
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    language = None
    header = '''!_TAG_FILE_SORTED\t1\t/0=unsorted, 1=sorted, 2=foldcase/'''
    dbase = re.compile(
        r"^(func\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$|" +
        r"^(func\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(function\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$|" +
        r"^(function\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(procedure\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(procedure\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$|" +
        r"^(proc\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(proc\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$|" +
        r"^(static\s+func\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(static\s+func\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$|" +
        r"^(static\s+function\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(static\s+function\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$|" +
        r"^(static\s+procedure\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$"
        r"^(static\s+procedure\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$"
        r"^(static\s+proc\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$"
        r"^(static\s+proc\s+([_A-Za-z][A-Za-z0-9_]*)\s*)$"
        , re.I)
    basic = re.compile(
        r"^(def\s+([A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +            # def =
        r"^(\d+\s+def\s+([A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +      # def = w/line num
        r"^(def\s+([A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*=.*)$|" +         # def
        r"^(\d+\s+def\s+([A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*=.*)$|" +   # def w/line num
        r"^(sub\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(\d+\s+sub\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*)$|" +
        r"^(sub\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s+static\s*)$|" +
        r"^(\d+\s+sub\s+([_A-Za-z][A-Za-z0-9_]*)\s*\(.*\)\s*static\s*)$"
        , re.I)
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 [file2...]
      Produces a tags file for older/oddball programming languages.
    Options:
      -b   BASIC
      -d   dBase'''))
    exit(1)
def ProcessCommandLine():
    global language
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "bdh")
    except getopt.error as s:
        print("getopt error:  %s" % s)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-b":
            language = "basic"
        if opt[0] == "-d":
            language = "dbase"
        if opt[0] == "-h":
            Usage()
    if not language:
        print("You need to specify a language")
        Usage()
    return args
'''
Keywords:
    ^func
    ^Func
    ^static Func
    ^FUNCTION
    ^static FUNCTION
    ^PROCEDURE
    ^STATIC PROCEDURE
'''
def ProcessFile(regexp, file, tags):
    for line in open(file).readlines():
        match = regexp.match(line)
        if match:
            s = [x for x in match.groups() if x is not None]
            reg, symbol = s
            while reg[-1] == "\n":
                reg = reg[:-1]
            tags.append((symbol, file, reg))
def Output(tags):
    out = open("tags", "wb")
    print(header, file=out)
    for item in sorted(tags):
        print("%s\t%s\t/^%s$/" % item, file=out)
if __name__ == "__main__":
    files = ProcessCommandLine()
    if len(files) == 0:
        Usage()
    tags = []
    for file in files:
        if language == "dbase":
            ProcessFile(dbase, file, tags)
        elif language == "basic":
            ProcessFile(basic, file, tags)
        else:
            raise "No language"
    Output(tags)

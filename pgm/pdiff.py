'''
Generate an HTML difference of two files and launch in browser
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import difflib
    import getopt
    import sys
    import tempfile
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    import launch
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 file2
      Show an HTML difference between the two files in a browser.
    Options:
      -i   Ignore case
    '''))
    print(s)
    exit(status)
def ParseCommandLine(d):
    d["-i"] = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("i"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if len(args) != 2:
        Usage(d)
    return args
def GetFile(file):
    s = open(file, "rb").read()
    if type(s) == type(b""):
        s = s.decode()
    assert(isinstance(s, str))
    return s
if __name__ == "__main__":
    d = {}      # Options dictionary
    file1, file2 = ParseCommandLine(d)
    old, new = GetFile(file1), GetFile(file2)
    nl = "\n"
    if d["-i"]:
        old = old.lower()
        new = new.lower()
    h = difflib.HtmlDiff()
    s = h.make_file(old.split(nl), new.split(nl))
    fd, name = tempfile.mkstemp(suffix=".html", dir="/tmp/dontmp")
    open(name, "w").write(s)
    launch.Launch(name)

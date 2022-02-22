'''
Generate an HTML difference of two files and launch in browser
    Note the tempfile used is not cleaned up.
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
    import webbrowser
    from textwrap import dedent
    from pdb import set_trace as xx 
if 1:   # Custom imports
    import launch
if 1:   # Core functionality
    def ShowDifference(old_str, new_str):
        h = difflib.HtmlDiff()
        s = h.make_file(old_str.split(nl), new_str.split(nl))
        fd, name = tempfile.mkstemp(suffix=".html", dir="/tmp/dontmp")
        open(name, "w").write(s)
        if 1:
            # This uses the launch.py module
            launch.Launch(name)
        else:
            # This doesn't work with Firefox
            url = f"file:///C:/cygwin{name}"
            webbrowser.open_new_tab(url)
        # This leaves the temporary file because there's no easy way to
        # determine when the browser is finished looking at it.  This might
        # be fixed by launching another browser window and waiting for it
        # to exit, but this is more trouble than it's worth because the
        # browser executable would have to be hard-coded in.
if __name__ == "__main__":
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 file2
          Show an HTML difference between the two files in a browser.
        Options:
          -i   Ignore case'''[1:]))
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
    d = {}      # Options dictionary
    file1, file2 = ParseCommandLine(d)
    old, new = GetFile(file1), GetFile(file2)
    nl = "\n"
    if d["-i"]:
        old = old.lower()
        new = new.lower()
    ShowDifference(old, new)

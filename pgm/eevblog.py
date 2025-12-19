'''

Searches for keywords in the EEVblog video titles.

To use this script, you must
    - Go to the page https://www.eevblog.com/episodes in your browser and save it as a
      text file. 
        - Set the global variable g.data to point to the location of this text file.
    - This script is set up to open the URLs in FireFox, Chrome, or Edge on my Windows
      system running WSL.  You'll have to hack on OpenURL() if you're on a different
      system.  Also check where the g.browser global variable is pointed to.
        - If you don't want to mess with a different setup, comment out the call to
          OpenURL() at the end of the file.  The URL is printed to the screen and you
          can copy and paste it into a browser.

'''
if 1:   # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2025 Don Peterson #∞copyright∞#
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
    if 1:   # Standard imports
        from collections import defaultdict
        from pathlib import Path as P
        from datetime import date
        import getopt
        import os
        import re
        import sys
        import subprocess
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        from months import months
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.browser = "/mnt/c/Program Files/Mozilla Firefox/firefox.exe"
        g.data = "/plib/pgm/eevblog.txt"
        ii = isinstance
if 1:   # Classes
    class Line:
        r = re.compile(r"(/\d\d\d\d/\d\d/\d\d)")
        def __init__(self, line):
            self.line = line
            # Split into title and url
            loc = line.find("<http")
            if loc == -1:
                Error("Bad line:  {line!r}")
            self.title = line[:loc].strip()
            self.url = line[loc:].strip().replace("<", "").replace(">", "")
            # Get the date from the URL
            self.date = self.convert_date(Line.r.search(self.url).groups()[0])
        def __str__(self):
            m = months[self.date.month]
            return f"{self.title} {self.date.day}{m}{t.yel}{self.date.year}{t.n}" 
        def __repr__(self):
            return self.title
        def convert_date(self, dt):
            mydate = [int(i) for i in dt.replace("/", " ").split()]
            return date(*mydate)
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [regex1 [regex2...]] [o]
          Search EEVblog titles for regex1; AND together with any following regexes.
          Note case is ignored by default.  Use -o to open the relevant URLs in the
          default browser (FireFox) or, if you use an o at the end of the command line,
          it's the same as typing -o..
        Options:
            -b x    Change browser:  c for Chrome, e for Edge, f for Firefox
            -i      Don't ignore case
            -n      Limit to number of URLs to open [{d["-n"]}]
            -p      Print the matched URLs
            -o      Open the matched URLs
            -w      Show keywords with number of title hits
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = None      # Change browser
        d["-i"] = True      # Don't ignore case
        d["-n"] = 5         # Limit to number of URLs to open
        d["-o"] = False     # Open the matched URLs
        d["-w"] = False     # Show keywords
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "b:hion:w") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ceiow"):
                d[o] = not d[o]
            elif o == "-b":
                if a == "c":
                    g.browser = "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
                elif a == "e":
                    g.browser = "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
                elif a == "f":
                    g.browser = "/mnt/c/Program Files/Mozilla Firefox/firefox.exe"
                else:
                    Error(f"{a!r} is an unknown browser")
            elif o == "-n":
                try:
                    d[o] = int(a)
                    if d[o] <= 0:
                        raise Exception()
                except Exception:
                    Error(f"{a!r} is a bad integer (must be > 0)")
            elif o == "-h":
                Usage()
        GetColors()
        # Check to see if o is the last argument; if it is, set -o to True
        if len(args) > 1:
            if args[-1] == "o":
                args.pop()
                d["-o"] = True
        return args
if 1:   # Core functionality
    def GetData():
        'Return a list of the relevant EEVblog lines'
        lines = open(g.data).read()
        lines = [i.strip() for i in lines.split("\n")]
        # Get rid of top junk
        while True:
            if lines[0] == "*Blog links to every Episode:*":
                lines.pop(0)
                break
            lines.pop(0)
        # Save relevant lines
        a = []
        while True:
            if lines[0] == "* Surgery Update <https://www.eevblog.com/2016/07/29/surgery-update/>":
                break
            a.append(lines.pop(0))
        if 0:
            print("First:")
            for line in a[:10]:
                print(line)
            print("\nLast:")
            for line in a[-10:]:
                print(line)
        # Fold lines to single lines
        o, s = [], ""
        while a:
            line = a.pop(0)
            if not line:
                continue
            if line[0] == "*":
                o.append(s)
                s = line
            else:
                s += line
        o.append(s)
        # Get rid of blank lines
        o = [i for i in o if i]
        # Strip off leading stuff
        for i, s in enumerate(o):
            s = s[2:]     # Gets rid of "* "
            if s.lower().startswith("eevblog"):
                s = s[7:].strip()
            if s.startswith("#"):
                s = s[1:].strip()
            o[i] = s
        # Make class
        o = [Line(i) for i in o]
        if 0:
            for i in o:
                print(i.title)
        return o
    def FilterItems(items, regex):
        'Return a list of the items that match the regex'
        r = re.compile(regex, re.I if d["-i"] else 0)
        keep = []
        for item in items:
            if r.search(item.title):
                keep.append(item)
        return keep
    def OpenURL(url):
        subprocess.run([g.browser, url])
    def Keywords(items):
        'Print keywords and their counts'
        wordrefs = defaultdict(list)
        ignore = '''- + 0 1 2 3 4 5 6 7 8 9 the a & to of and is vs an with is vs for an
                    in on are at i do from can my from / you '''.split()
        for item in items:
            for i in item.title.split():
                if i not in ignore:
                    wordrefs[i.lower()].append(item)
        # Create list of (count, token)
        refs = []
        for i in wordrefs:
            refs.append((len(wordrefs[i]), i))
        # Report
        for n, item in sorted(refs, key=lambda x: x[0]):
            print(n, item)

if __name__ == "__main__":  
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    g.items = GetData()
    if d["-w"]:
        Keywords(g.items)
        exit()
    for regex in args:
        g.items = FilterItems(g.items, regex)
    if g.items:
        for item in g.items:
            print(item)
        t.print(f"{t.brnl}Video links at https://www.eevblog.com/episodes/")
    if d["-o"]:
        n = d["-n"]
        for item in g.items[:n]:
            print(f"{item.url}")
            OpenURL(item.url)

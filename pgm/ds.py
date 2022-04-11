'''
Open a document file

    File is opened if it's the only match to the regexp on the command
    line.  Otherwise print out the matches.  Example:
 
        ds 3456
 
    will prompt you for manuals/datasheets/catalogs that contain the
    string 3456.

    Current --exec options support datasheets (ds), ebooks (eb), and HP
    Journal articles (hpj).  For the HP Journal stuff, use the -j
    option.
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
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import glob
    import os
    import pathlib
    import pickle
    import re
    import subprocess
    import sys
    from itertools import filterfalse
    from os.path import join, isfile, split
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from selection import Select
    from dirfiles import Dirfiles
    # Try to import the color module
    _have_color = False
    try:
        import kolor as c
        _have_color = True
    except ImportError:
        # Dummy object that will swallow calls to the color module
        class _C:
            def __setattr__(self, attr, x):
                pass
            def __getattr__(self, attr):
                return None
            def fg(self, *p):
                pass
            def normal(self):
                pass
        c = _C()
        del _C
if 1:   # Global variables
    # app to open a file with registered application
    unix = False
    if unix:
        app = "/usr/bin/exo-open"       # Linux
    else: # Windows
        #app = "<dir>/app.exe"
        app = "c:/cygwin/bin/cygstart.exe" 
if 1:   # Colors for output; colors available are:
    #   black   gray
    #   blue    lblue
    #   green   lgreen
    #   cyan    lcyan
    #   red     lred
    #   magenta lmagenta
    #   brown   yellow
    #   white   lwhite
    (black, blue, green, cyan, red, magenta, brown, white, gray, lblue,
    lgreen, lcyan, lred, lmagenta, yellow, lwhite) = (
        c.black, c.blue, c.green, c.cyan, c.red, c.magenta, c.brown,
        c.white, c.gray, c.lblue, c.lgreen, c.lcyan, c.lred, c.lmagenta,
        c.yellow, c.lwhite)
    c_norm = (white, black)  # Color when finished
    c_plain = (white, black)
    # The following variable can be used to choose different color styles
    colorstyle = 0
    if colorstyle == 0:
        c_dir = (lred, black)
        c_match = (yellow, black)
    elif colorstyle == 1:
        c_dir = (lred, black)
        c_match = (white, blue)
    elif colorstyle == 2:
        c_dir = (lgreen, black)
        c_match = (black, green)
    elif colorstyle == 3:
        c_dir = (lmagenta, black)
        c_match = (yellow, black)
    elif colorstyle == 4:
        c_dir = (lgreen, black)
        c_match = (lwhite, magenta)
    elif colorstyle == 5:
        c_dir = (lred, black)
        c_match = (black, yellow)
    # Index files hold the files to be searched.  These are stored in files
    # because caching on my system doesn't work well for the d:/ drive.  It
    # only takes a few seconds to generate the index files with -I.
    index_files = {
        "bk": "/plib/pgm/ds.bk.index", 
        "ds": "/plib/pgm/ds.ds.index", 
        "eb": "/plib/pgm/ds.eb.index", 
        "hpj": "/plib/pgm/ds.hpj.index", 
    }
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    name = d["--exec"]
    print(dedent(f'''
    Usage:  {name} [options] regexp
      Open a document if it's the only match to the regexp.  Otherwise print
      out the matches and choose which ones to display.  When choosing, you
      can select multiple numbers by separating them with spaces or commas.
      Ranges like 5-8 are recognized.
    Options
      -I    Generate the index
      -i    Make the search case sensitive
      -j    Search HP Journal and Bench Brief files (note:  consider
            using the hpj.py script for such searches)
    Long options
      --exec n
        Name of index file for usage statement.  Choices are:
          {' '.join(index_files.keys())}
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-I"] = False     # If True, then generate indexes
    d["-i"] = False     # If True, then case-sensitive search
    d["-j"] = False     # Show HPJ matches
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hIij", ["exec="])
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o[1] in list("Iij"):
            d[o] = not d[o]
        elif o == "--exec":
            d["--exec"] = a
            if a not in index_files:
                Error("'{a}' not an index")
        elif o == "-h":
            Usage(d, 0)
    if d["-I"]:
        GenerateIndexFiles(d)
    if d["-j"]:
        d["--exec"] = "hpj"
    if len(args) != 1:
        Usage(d)
    return args
def PrintMatch(num, path, start, end, d):
    '''For the match in path, print things out in the appropriate colors.
    Note start and end are the indices into just the file part of the
    whole path name.
    '''
    c.fg(c_plain)
    print("%3d  " % num, end="")
    s = str(path)
    dir, file = split(s[len(d["root"]) + 1:])  # Gets rid of leading stuff
    dir += "/"
    print(dir, end="")
    print(file[:start], end="")
    c.fg(c_match)
    print(file[start:end], end="")
    c.fg(c_plain)
    print(file[end:])
def GenerateIndexFiles(d):
    '''Generate all of the index files at once.
    '''
    # ebooks
    df = Dirfiles("/ebooks", clear=True)
    df.add("**/*")
    with open(index_files["eb"], "wb") as fp:
        pickle.dump(df.files, fp)
    # Datasheets
    df = Dirfiles("/manuals", clear=True)
    df.add("**/*")
    with open(index_files["ds"], "wb") as fp:
        pickle.dump(df.files, fp)
    # HP Journal
    df = Dirfiles("/cygdrive/d/ebooks/hpj", clear=True)
    df.add("**/*")
    with open(index_files["hpj"], "wb") as fp:
        pickle.dump(df.files, fp)
    # B&K
    df = Dirfiles("/manuals/manuals/bk", clear=True)
    df.add("**/*")
    with open(index_files["bk"], "wb") as fp:
        pickle.dump(df.files, fp)
    exit(0)
def ReadIndexFile(d):
    '''Read the index file keyed by d["--exec"].
    '''
    key = d["--exec"]
    with open(index_files[key], "rb") as fp:
        d["files"] = pickle.load(fp)
    # Set d["root"] which is the files' prefix to remove
    root = {
        "bk": "/manuals/manuals",
        "ds": "/manuals",
        "eb": "/ebooks",
        "hpj": "/cygdrive/d/ebooks",
    }
    d["root"] = r = root[key]
def GetChoices(matches):
    '''Return a set of integers representing the user's choices.
    '''
    while True:
        answer = input("? ").strip()
        if not answer or answer == "q":
            exit(0)
        n = len(matches) + 1
        found, not_found = Select(answer, range(1, n + 1))
        if found:
            break
    if not_found:
        s = ' '.join([str(i) for i in not_found])
        print(f"Selections not found:  {s}")
    return found
def OpenFile(app, matches, choice):
    'Open indicated choice (subtract 1 first)'
    # Send stderr to /dev/null because some apps on Linux have annoying
    # bug messages sent to the console.
    subprocess.Popen([app, matches[choice - 1][0]],
                     stderr=subprocess.DEVNULL)
def GetMatches(regexp, d):
    r = re.compile(regexp) if d["-i"] else re.compile(regexp, re.I)
    matches = []
    for i in d["files"]:
        # Only search for match in file name
        dir, file = split(i)
        mo = r.search(file)
        if mo:
            matches.append((i, mo))
    # Sort the matches so that they always appear in the same order (not
    # doing this will sometimes give different orders.
    f = lambda i: str(i[0])     # Get the path string
    matches = list(sorted(matches, key=f))
    return matches
def PrintChoices(matches, d):
    print("Choose which file(s) to open:")
    for num, data in enumerate(matches):
        file, mo = data
        PrintMatch(num + 1, file, mo.start(), mo.end(), d)
def OpenMatches(matches, d):
    '''Each match item will be (full_filename, match_object) where
    match_object is the mo for _only_ the actual file name (not the
    path).
    '''
    if len(matches) > 1:
        PrintChoices(matches, d)
        for choice in GetChoices(matches):
            OpenFile(app, matches, choice)
    elif len(matches) == 1:
        OpenFile(app, matches, 0)
    else:
        print("No matches")
if __name__ == "__main__":
    d = {   # Options dictionary
        "--exec": "ds",
    }
    regexp = ParseCommandLine(d)[0]
    ReadIndexFile(d)    # Get list of the files to search
    matches = GetMatches(regexp, d)
    OpenMatches(matches, d)

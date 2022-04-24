'''
List directories in the current directory
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
    # List directories in the current directory
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import glob
    import pathlib
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import columnize
    _no_color = True
    if sys.stdout.isatty():
        try:
            import color as color
            _no_color = False
        except ImportError:
            pass
    if _no_color:
        class Color:  # Swallow function calls
            def fg(self, *p):
                pass
            def __getattr__(self, a):
                pass
        color = Color()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} dir1 [dir2 ...]
      Print the directories under the given directories.  Defaults to
      '.' if no directories given.
    Options
      -a    Show hidden directories
      -c    Show output in color
      -f    Fold the names in sorting
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-a"] = False     # Show hidden directories
    d["-c"] = False     # Output in color
    d["-f"] = False     # Fold the sorting
    try:
        optlist, directories = getopt.getopt(sys.argv[1:], "acfh")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o[1] in list("acf"):
            d[o] = not d[o]
        elif o == "-h":
            Usage(d, status=0)
    if not directories:
        ProcessDir(P("."), no_header=True)
        exit(0)
    return directories
def ProcessDir(dir, no_header=False):
    assert(ii(dir, P))
    if not dir.is_dir():
        return
    # Get list of directories
    os.chdir(dir)   # Now directory list will be relative to dir
    dirs = []
    for i in P(".").glob("*"):
        if i.is_dir():
            if d["-a"]:
                # Show all directories
                dirs.append(i)
            else:
                # Don't show hidden directories
                if not str(i).startswith("."):
                    dirs.append(i)
    if dirs:
        # Decorate with ending '/' to help flag that they are directories
        dirs = [str(i) + "/" for i in dirs]
        dirs = sorted(dirs, key=str.lower) if d["-f"] else sorted(dirs)
        if not no_header:
            if d["-c"]:
                color.fg(color.white)
            print("Directory ", dir, ":", sep="")
        s = columnize.Columnize(dirs)
        if d["-c"]:
            color.fg(color.lred)
        for line in s:
            print(line)
    if d["-c"]:
        color.fg(color.white)
if __name__ == "__main__": 
    d = {}  # Options dictionary
    directories = ParseCommandLine(d)
    for dir in directories:
        ProcessDir(P(dir))
    if d["-c"]:
        color.normal()

'''
Provide the output of the ls command for a directory, but color the
files per their Mercurial status.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # An ls command, but color the output per the Mercurial status
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from collections import defaultdict
    import getopt
    import os
    import sys
    import subprocess
    from pdb import set_trace as xx
    from pprint import pprint as pp
if 1:   # Custom imports
    from wrap import dedent
    old_color = 0
    from color import TRM as t
    from columnize import Columnize
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Mercurial installation
    if 0:
        hg = "/usr/bin/hg"
        ls = "/bin/ls"
    else:
        hg = "c:/bin/mercurial/hg.exe"
        ls = "c:/cygwin/bin/ls.exe"
    # Colors for status type
    if old_color:
        colors = {
            "M": yellow,
            "A": lgreen,
            "R": red,
            "C": white,
            "!": lred,
            "?": lcyan,
            "I": lblue,
        }
    else:
        colors = {
            "M": "yell",
            "A": "grnl",
            "R": "red",
            "C": "wht",
            "!": "redl",
            "?": "cynl",
            "I": "blul",
        }
    status_name = {
        "M": "Modified:",
        "A": "Added:",
        "R": "Removed:",
        "C": "Clean:",
        "!": "Deleted:",
        "?": "Not tracked:",
        "I": "Ignored:",
    }
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]}
      Displays the Mercurial type of the files in the current directory.
    Options
      -a    Show hidden files
      -i    Include ignored files in listing
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-a"] = False     # Show hidden files
    d["-i"] = False     # Show ignored files
    try:
        opts, dir = getopt.getopt(sys.argv[1:], "ahi")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-a",):
            d["-a"] = True
        elif o in ("-i",):
            d["-i"] = True
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if len(dir) > 1:
        Usage(d)
    elif not dir:
        dir = ["."]
    return dir[0]
def GetRoot(dir, d):
    '''Add the Mercurial root directory to d["root"].  Issue an error
    message and exit if dir is not in a Mercurial repository.
    '''
    try:
        cmd = [hg, "root"]
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ss = [i.decode("utf8").strip() for i in s.stdout.readlines()]
        se = [i.decode("utf8").strip() for i in s.stderr.readlines()]
    except Exception as e:
        Error("Unexpected error:  '{}'".format(repr(e)))
    if not se and len(ss) == 1:
        d["root"] = ss[0].strip()
    else:
        Error("'{}' not in a Mercurial repository".format(dir))
def GetFiles(d):
    pth = os.path.abspath(".")
    GetRoot(pth, d)
    s = subprocess.Popen([hg, "st", "-A", "."], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    u = [i.decode("utf8") for i in s.stdout.readlines()]
    files = [os.path.abspath(i.rstrip()) for i in u]
    curdir = os.getcwd()
    # Keep the files in the indicated directory
    keep = []
    for file in files:
        mydir, name = os.path.split(os.path.abspath(file))
        if mydir == curdir:
            dir, name = os.path.split(file)
            keep.append(name)
    # Build a list of (file, status_letter)
    results = []
    for i in keep:
        status, file = i[0], i[2:]
        if file[0] == "." and not d["-a"]:
            continue
        results.append((file, status))
    # Sort by name in a case-independent fashion
    results = sorted(results, key=lambda x: x[0].lower())
    return results
def Print(results, key, d):
    '''Print the results color-coded for key.
    '''
    if key not in results:
        return
    if key == "I" and not d["-i"]:
        return
    if sys.stdout.isatty():
        if old_color:
            fg(colors[key])
        else:
            print(f"{t(colors[key])}", end="")
    print(status_name[key])
    # Check to see if we can use Columnize without an exception
    can_use_columnize = True
    try:
        Columnize(results[key], indent=" "*2)
    except Exception:
        can_use_columnize = False
    indent = " "*2
    if can_use_columnize:
        for i in Columnize(results[key], indent=indent):
            print(i)
    else:
        for i in results[key]:
            print(indent, i, sep="")
    if sys.stdout.isatty():
        if old_color:
            normal()
        else:
            print(t.n, end="")
def PrintResults(files, d):
    if sys.stdout.isatty():
        if old_color:
            SetStyle("underline")
        else:
            print(f"{t(None, None, 'ul')}", end="")
    print("Repository root", end=" ")
    if sys.stdout.isatty():
        if old_color:
            SetStyle("normal")
        else:
            print(t.n, end="")
    print("=", d["root"])
    results = defaultdict(list)
    for file, status in files:
        results[status].append(file)
    for key in list("IC!RAM?"):
        Print(results, key, d)
if __name__ == "__main__":
    d = {}      # Options dictionary
    dir = ParseCommandLine(d)
    os.chdir(dir)
    files = GetFiles(d)
    PrintResults(files, d)

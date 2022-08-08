'''
Display the size of one or more directories and their subdirectories
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Display size of directories
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import atexit
    import getopt
    from math import log10
    import glob
    import os
    import subprocess
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import color as C
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    clr = "off" if d["-c"] else "on"
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [dir1 [dir2...]]
      Display the sizes of the files in each of the directories.  The intent
      is to help you quickly see where the most space is being consumed.
      If no directory is given, the argument defaults to the current
      directory.
    Options:
      -c    Turn color {clr}
      -h    Print a manpage.
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = True      # Enable color
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ch")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-c",):
            d["-c"] = not d["-c"]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if not args:
        args = ["."]
    return args
def Eng(n):
    '''Given an integer n, return (s, clr) where s is a string in
    engineering notation with 1 significant figure and clr is a color to
    display this number in.  s will have the following format depending
    on the size of n:
    
              1         2 
     ....+....|....+....|..
       KKKk
           mmmM
               gggG
 
    This causes the sizes to line up in a way to help you parse the
    information quickly.  Note any file's size will be at least 4k
    because of the minimum disk block size.
    '''
    clr = {
        1: C.white, 2: C.white, 3: C.white, 4: C.white, 5: C.white,
        6: C.white, 7: C.yellow, 8: C.yellow, 9: C.lgreen, 10: C.lred,
        11: C.lmagenta,
    }
    prefix = {0: " ", 3: "k", 6: "M", 9: "G", 12: "T"}
    l = int(log10(n))
    div, rem = divmod(l, 3)
    # Build engineering string
    first_digit = str(n)[0]
    pr = prefix[3*div]
    s = str(int(first_digit)*10**rem) + prefix[3*div]
    while len(s) < 4:
        s = " " + s
    # Indent (note the min size will be in k)
    s = (" "*4)*(div - 1) + s
    return s, clr[l]
def GetDirSize(dir):
    p = subprocess.PIPE
    s = subprocess.Popen(("/usr/bin/du", "-B1", "-s", dir), stdout=p, stderr=p)
    result = s.stdout.readline().decode("ascii")
    return int(result.split("\t")[0])
def CleanUp(d):
    'Make sure color is turned off'
    if d["-c"]:
        C.normal()
def ProcessDir(dir, d):
    c = "·"
    if d["-c"]:
        C.fg(C.lmagenta)
    if dir == ".":
        print(dir, "({})".format(os.getcwd()), end=" ")
    else:
        print(dir, end=" ")
    if d["-c"]:
        C.normal()
    # Print size of files in this directory
    sz = GetDirSize(dir)
    s, clr = Eng(sz)
    if d["-c"]:
        C.fg(clr)
    print(f"{s.strip()}", end=" ")
    if d["-c"]:
        C.normal()
    print()
    # Note we also need to examine hidden directories too
    for i in sorted(glob.glob(dir + "/*") + glob.glob(dir + "/.*")):
        if os.path.isdir(i):
            sz = GetDirSize(i)
            if sz:
                d["total"] += sz
                s, clr = Eng(sz)
                if d["-c"]:
                    C.fg(clr)
                if i.startswith("./"):
                    i = i[2:]
                print(f"  {s:<15s} {i}/")
                if d["-c"]:
                    C.normal()
if __name__ == "__main__":
    d = {}      # Options dictionary
    d["total"] = 0
    dirs = ParseCommandLine(d)
    atexit.register(CleanUp, d)
    for dir in dirs:
        ProcessDir(dir, d)
    if d["total"]:
        s, clr = Eng(d["total"])
        print("\nTotal =", end=" ")
        if d["-c"]:
            C.fg(clr)
        print(s.strip(), end="")
        if d["-c"]:
            C.normal()
        print("\nSizes are to 1 significant figure")

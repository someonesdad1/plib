"""
Plot a histogram of the file sizes for the directories given on the command
line.  Recursively walk each of the directories.  Uses matplotlib and
numpy.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Plot file sizes in given directories
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import os
    from pylab import *
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    out = sys.stdout.write
    nl = "\n"


def Usage(d, status=1):
    name = sys.argv[0]
    binsize = d["-b"]
    print(
        dedent(f"""
    Usage:  {name} [options] dir1 [dir2...]
      Plots a histogram of file sizes for the indicated directories.  The
      directories are descended recursively.  Files of zero size are ignored
      unless the -z option is used.
    
    Options:
      -f file
        Instead of plotting to the screen, save the plot to a file.  The
        suffix .png will be added to the file name.
      -b num
        Set the histogram's bin size (default = {binsize})
      -n file
        Write to the indicated file each file size in bytes and path, one
        line per file.
      -r
        Do not descend directories recursively.
      -z
        Do not ignore zero-length files.  These zero-length files are encoded
        with logarithms of -0.5.
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-b"] = 40
    d["-f"] = None
    d["-n"] = None
    d["-r"] = False
    d["-z"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "b:f:n:rz")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-b":
            d["-b"] = int(opt[1])
        elif opt[0] == "-f":
            d["-f"] = opt[1]
        elif opt[0] == "-n":
            d["-n"] = open(opt[1], "wb")
        elif opt[0] == "-r":
            d["-r"] = True
        elif opt[0] == "-z":
            d["-z"] = True
    if not args:
        Usage(d)
    return args


def ProcessFiles(root, files, d):
    sizes = []
    for file in files:
        file = os.path.join(root, file).replace("\\", "/")
        try:
            size = os.stat(file).st_size
            if d["-n"] is not None:
                d["-n"].write("%-12d %s\n" % (size, file))
            if size or (not size and d["-z"]):
                sizes.append(os.stat(file).st_size)
        except Exception:
            pass
    return sizes


def ProcessDir(dir, d):
    sizes = []
    for root, dirs, files in os.walk(dir):
        sizes += ProcessFiles(root, files, d)
        if d["-r"]:
            break
    return sizes


if __name__ == "__main__":
    d = {}  # Options dictionary
    dirs = ParseCommandLine(d)
    sizes = []
    for dir in dirs:
        sizes += ProcessDir(dir, d)
    sizes = [max(i, 0.316) for i in sizes]
    hist([log10(i) for i in sizes], bins=d["-b"])
    xlabel("Base 10 log of file size in bytes")
    ylabel("Count")
    grid()
    title("%d files" % len(sizes))
    if d["-f"] is not None:
        savefig(d["-f"] + ".png", dpi=600)
    else:
        show()

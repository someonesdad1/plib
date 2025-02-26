"""
Find files above a specified size
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Find files above a specified size
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    from operator import itemgetter
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from fpformat import FPFormat
if 1:  # Global variables
    nl = "\n"
    size_string = ""
    size_in_bytes = 0
    fp = FPFormat()
    fp.digits(2)
    num_largest = None
    sorted = 1  # 1 == smallest first, 2 == largest first
    dirlist = []
    topdown = True
    dirs_to_ignore = []


def Usage():
    name = sys.argv[0]
    print(
        dedent(
            """
    Usage:  %(name)s size [dir1 [dir2...]]
      Print all files above the specified size at and below each directory
      specified.  The size is the number of bytes; it can have "k", "M",
      or "G" (case-insensitive) appended.  If dir1 is not given, the current
      directory is assumed.
    Options
      -b
          Use a bottom-up directory walk.  A topdown walk is normally used.
          Is irrelevant if -s or -S are used.
      -d digits
          Set the number of digits shown in the output size.  Default is 3.
      -l num
          Show only the num largest files.
      -s
          Sort output by size, smallest first
      -S
          Sort output by size, largest first
      -x dir
          Ignore files in this directory.  More than one -x option OK.
      -X
          Ignore the directories I don't normally search on my Linux box.
    """
            % locals()
        )
    )
    sys.exit(2)


def ParseCommandLine():
    global size_in_bytes, size_string, sorted, num_largest, topdown
    global dirs_to_ignore
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "bd:l:sSx:X")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o == "-b":
            topdown = False
        elif o == "-d":
            try:
                digits = int(a)
            except ValueError:
                msg = "'%s' is not a valid number of digits" % a
                print(msg)
                exit(1)
            if digits < 1:
                msg = "-d:  digits must be > 0"
                print(msg)
                exit(1)
            fp.digits(digits)
        elif o == "-l":
            try:
                num = int(a)
            except ValueError:
                msg = "'%s' is not a valid number for -l option" % a + nl
                print(msg)
                exit(1)
            if num < 1:
                msg = "-l:  num must be > 0"
                print(msg)
                exit(1)
            num_largest = num
        elif o == "-s":
            sorted = 1
        elif o == "-S":
            sorted = 2
        elif o == "-x":
            dirs_to_ignore.append(a)
        elif o == "-X":
            dirs_to_ignore = [
                "/media/donp/c",
                "/media/donp/d",
                "/media/donp/dcopy",
                "/mnt/pictures",
                "/mnt/bup1",
                "/mnt/pictures2",
                "/dev",
                "/proc",
                "/tmp",
            ]
    if not args:
        Usage()
    size_string = size = args[0]
    d = {"k": 3, "M": 6, "G": 9, "K": 3, "m": 6, "g": 9}
    multiplier = 1
    if size[-1] in d:
        multiplier = 10 ** d[size[-1]]
        size = size[:-1]
    try:
        size_in_bytes = int(float(size) * multiplier)
    except ValueError:
        print("Bad number for size")
        sys.exit(1)
    del args[0]
    if not args:
        args = ["."]
    # Turn dirs_to_ignore's paths to absolute paths
    dirs_to_ignore = [os.path.abspath(i) for i in dirs_to_ignore]
    return tuple(args)


def FormatSize(n):
    def RemoveDecimalPoint(s):
        if s[-1] == ".":
            s = s[:-1]
        return s

    s = fp.engsi(n).strip()
    if " " in s:
        num, suffix = s.split()
        num = RemoveDecimalPoint(num)
        return "".join((num, suffix))
    else:
        return RemoveDecimalPoint(s)


def GetSizeStringFormat(list_of_dirs):
    # list_of_dirs is a list of tuples containing
    # (size, formatted size, path)
    longest = max(map(len, map(itemgetter(1), list_of_dirs)))
    return "%%%ds %%s" % longest


def PrintList(list_of_dirs):
    fmt = GetSizeStringFormat(list_of_dirs)
    for size, formatted_size, path in list_of_dirs:
        print(fmt % (formatted_size, path))


def PrintLargest():
    # dirlist is a list of tuples containing (size, formatted size, path)
    global dirlist
    dirlist.sort()
    dirlist.reverse()
    largest = dirlist[:num_largest]
    if sorted == 1:
        largest.reverse()
    if largest:
        PrintList(largest)


def PrintResults():
    global dirlist
    if not dirlist:
        return
    if sorted:
        dirlist.sort()
        if sorted == 2:
            dirlist.reverse()
    PrintList(dirlist)


def ProcessDirectory(dir):
    for root, dirs, files in os.walk(dir, topdown=topdown):
        ap = os.path.abspath(root)
        if ap in dirs_to_ignore:
            continue
        for file in files:
            filepath = os.path.join(root, file).replace("\\", "/")
            try:
                size = os.stat(filepath)[6]
            except Exception:
                print("Couldn't stat '%s'" % filepath)
                continue
            if size > size_in_bytes:
                dirlist.append((size, FormatSize(size), filepath))


if __name__ == "__main__":
    directories = ParseCommandLine()
    for dir in directories:
        ProcessDirectory(dir)
    if num_largest:
        PrintLargest()
    else:
        PrintResults()

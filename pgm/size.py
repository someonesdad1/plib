'''
List sizes for files/patterns specified on the command line
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
    # List file sizes for glob patterns 
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import pathlib
    import re
    import glob
    import os
    from pprint import pprint as pp
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    import color as c
    from color import t
if 1:   # Global variables
    P = pathlib.Path
    flt(0).N = 2    # Number of significant figures for sizes with SI suffix
    colors = {
        "": t("wht"),
        "kB": t("grnl"),
        "MB": t("magl"),
        "GB": t("redl"),
    }
def Usage():
    name = sys.argv[0]
    print(dedent(rf'''
    {name} [options] p1 [p2...]
        List the sizes for all files that match globbing patterns p1, p2,... given
        on the command line.  These patterns can also be directories to be
        searched.  If no directories are given on the command line, the current
        directory is processed.
    Examples:
        To see the size of all files in current directory:
            {name} \*
        To see size of all python files at and below the current directory:
            {name} -r . \*.py
    Options:
        -g    The patterns are python regular expressions, not globbing patterns
        -r    Recurse into directories
        -v    Include version control directories
    '''))
    exit(0)
def Error(*msg):
    print(*msg, file=sys.stderr)
    exit(1)
def ParseCommandLine():
    d["-g"] = False  # Use regular expressions
    d["-r"] = False  # Recurse
    d["-v"] = False  # Include version control directories
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hgrv")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        exit(1)
    for o, a in optlist:
        if o[1] in "grv":
            d[o] = not d[o]
        elif o == "-h":
            Usage()
    if not args:
        Usage()
    return args
def GetPatterns(args):
    '''Return [patterns, directories] where patterns is a list of
    the form
        [
            [p1, 0],
            [p2, 0],
            ...
        ]
    where p1, p2 are the patterns and the 0's are the future locations of
    the number of bytes for that pattern.
 
    directories is a list of the directories found on the command line,
    given as pathlib.Path objects.  If there were none, the empty list is
    returned.
    '''
    patterns, directories = [], []
    for arg in args:
        p = P(arg)
        if p.is_dir():
            directories.append(p.resolve())
        else:
            patterns.append([arg, 0])
    if not patterns:
        patterns = [[".*", 0]] if d["-g"] else [["*", 0]]
    if not directories:
        directories = [P(".").resolve()]
    return patterns, directories
def CountBytes(pattern, directory):
    old_directory = os.getcwd()
    try:
        try:
            os.chdir(directory)
        except Exception:
            return 0
        bytes = 0
        for file in glob.glob(pattern):
            try:
                bytes += os.stat(file).st_size
            except Exception:
                print("Can't stat %s" % os.path.join(directory, file),
                      file=sys.stderr)
        return bytes
    finally:
        os.chdir(old_directory)
def ProcessPattern(pattern, directory):
    'Return the number of bytes matched by the given pattern'
    size = 0
    size = CountBytes(pattern, directory)  # Process given directory
    if d["-r"]:  # Recurse
        # Process all directories below directory
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                if ".hg" in dir and not d["-v"]:
                    continue
                size += CountBytes(pattern, os.path.join(root, dir))
    return size
def ProcessDirectory(patterns, directory):
    'patterns is a list of [glob_pattern, byte_count]'
    assert(isinstance(directory, P))
    # Check for a version control directory
    if not d["-v"]:
        parts = directory.parts
        for part in parts:
            if part in (".git", ".hg", ".bzr", "RCS"):
                return
    for pattern in patterns:
        bytes = ProcessPattern(pattern[0], directory)
        pattern[1] += bytes
def Collapse(size):
    'Return (size_str, x) where x is kB, MB, or GB.  size is number of bytes.'
    size = flt(size)
    if size < 10**3:
        return str(size), ""
    elif size < 10**6:
        return str(size/10**3), "kB"
    elif size < 10**9:
        return str(size/10**6), "MB"
    else:
        return str(size/10**9), "GB"
def PrintResults(directories, patterns):
    print("Directories processed", end="")
    if d["-r"]:
        print(" recursively", end="")
    print(":\n  ", end="")
    print(f"{t('lipl')}", end="")
    for i in directories:
        print(f"{i} ", end="")
    print(f"{t.n}")
    if not patterns:
        return
    print(dedent('''
    Size, bytes                Pattern
    ------------               -------'''))
    total_size = 0
    for pattern, size in patterns:
        print(f"{size:12d} = ", end="")
        num, ext = Collapse(size)
        print(f"{colors[ext]}{num + ' ' + ext:12s}{t.n}", end="")
        print(f"{pattern}")
        total_size += size
    print(f"Total bytes = {total_size} = ", end="")
    num, ext = Collapse(total_size)
    t.print(f"{colors[ext]}{num} {ext}")

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine()
    patterns, directories = GetPatterns(args)
    for directory in directories:
        ProcessDirectory(patterns, directory)
    PrintResults(directories, patterns)

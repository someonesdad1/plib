'''
Utility to rename files with given extensions
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2004 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Rename a large set of files with given extensions.  
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import math
    import os
    import pathlib
    import sys
    from io import StringIO
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent, wrap
    from color import C
    from get import GetLines
if 1:   # Global variables
    ii = isinstance
    P = pathlib.Path
    PosixPath = pathlib.PosixPath
    class g:
        pass
    g.name = P(sys.argv[0])
    g.err = C.lred
    g.dir = C.lcyn
    g.n = C.norm
    g.colors = [C.lyel, C.lmag, C.lred, C.lcyn, C.lgrn, C.lwht]
    g.width = 0
    # Container for undo information.  First entry will be the directory
    # and following items will be [newname, oldname] pairs.
    g.undo = []     # Container for undo information
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Manpage():
    print(wrap(f'''
    {g.name.name} will number all the files in directory dir that end with .ext1,
    .ext2, etc.  The files are numbered sequentially.  The program will not
    overwrite any existing files.  Normal behavior is to show what will be
    done, but don't rename any files.  Use -x to perform the actual
    renaming.

    After renaming with -x, an "undo" file is written to the directory 
    that lets you rename the files back to what they were before running
    the script.  Do this with the -u option and the directory argument you
    used for the renaming.  Individual renames may fail if you subsequently
    renamed files, but the script will undo as many of the changed names as
    possible.

    A tool like this should be used cautiously, as it could result in
    making significant changes that might be hard to undo.  An example
    would be to accidentally rename all the python files in a large git
    repository.  Yes, you can recover from such things, but it's better to
    e.g. move all the files you want to rename to a temporary directory,
    verify you'll get what you want by a dry run (i.e., don't use the -x
    option), then peform the renaming with -x.  

    Another caution is that sometimes significant information can be
    'encoded' in the file's names, such as date, location, people, etc.
    For picture files, this could be a big loss with accidental renaming,
    so careful scrutiny of the dry run results is suggested.

    '''))
    print(dedent(f'''

    Example:
      Suppose we're in a directory that has the following files:
          a.jpg
          abc.jpg
          b.jpg
          in.obj
          out.obj
      If we execute the command
          {g.name.name} -p test . jpg obj
      the files will be renamed to:
          a.jpg   ->  test1.jpg
          abc.jpg ->  test2.jpg
          b.jpg   ->  test3.jpg
          in.obj  ->  test1.obj
          out.obj ->  test2.obj
      There is no specified relationship between the old filenames and 
      the new filenames.

    The -c option is recommended, as it will color-highlight the extensions,
    making it a bit easier to see that you're getting what you asked for.

    A typical use case is to rename a large number of *.jpg files in a
    directory, as shown in the example above.  In fact, such a use case was
    the progenitor of this script.  My family would go on a trip and when
    we returned, we'd have hundreds of snapshots on my camera.  This script
    let me rename file more meaningfully.  For example, a group of files
    might have been taken at the fiddling contest on Tuesday, so that set
    of files would e.g. be renamed with the prefix 'FiddlingContestTuesday'.
    This would allow easy reorganization later into e.g. separate
    directories, where the file names could be refined or annotations added.

    '''))
    exit(0)
def Usage(status=1):
    print(dedent(f'''
    Usage:  {g.name} [opt] dir ext1 [ext2...]
      Rename a sequence of files in a directory with the given extensions.
      Normal behavior is to show what will be done; you must use the -x
      option to have the renaming actually be done.  After renaming is
      finished, a file named {g.name.stem}.undo will be written that will allow
      you to undo the renaming by using it with the -u option.
    Options
      -c    Colorize extensions
      -h    Show a man page
      -i    Ignore any file that cannot be renamed
      -p p  Use prefix p for renaming
      -s p  Use suffix p for renaming
      -u f  Use the file f to undo the renaming
      -x    Do the renaming
    '''))
    exit(status)
def ParseCommandLine():
    d["-c"] = False     # Colorize
    d["-i"] = False     # Ignore errors
    d["-p"] = ""        # Prefix to rename with
    d["-s"] = ""        # Suffix to rename with
    d["-u"] = None      # Undo command
    d["-x"] = False     # Do the renaming
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "chip:s:u:x")
    except getopt.error as str:
        print(str)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "cix":
            d[o] = not d[o]
        elif o in ("-p", "-s"):
            d[o] = a
        elif o == "-h":
            Manpage()
        elif o == "-u":
            d[o] = a
    if len(args) < 2 and not d["-u"]:
        Usage()
    if not d["-c"]:
        g.dir = g.n = ""
        g.colors = []
    return args
def GetWidth():
    'Find the longest filename we have to print'
    currdir = os.getcwd()
    os.chdir(directory)
    cd = P(".")
    for ext in extensions:
        files = list(cd.glob("*." + ext if ext[0] != "." else "*" + ext))
        for file in files:
            g.width = max(len(str(file)), g.width)
    os.chdir(currdir)
def ProcessExtension(ext, directory, ext_number):
    currdir = os.getcwd()
    os.chdir(directory)
    cd = P(".")
    ext = ext.strip()
    files = list(cd.glob("*." + ext if ext[0] != "." else "*" + ext))
    numfiles = len(files)
    m = int(math.log10(numfiles) + 1)
    fmt = d["-p"] + f"%0{m}d" + d["-s"]
    number = 1
    # Get longest file name width
    w = 0
    for file in files:
        if " " in str(file):
            Error(f"'{file}':  can't have space characters in file names")
        w = max(len(str(file)), w)
    # Determine color to use for this extension
    if d["-c"]:
        n = ext_number % len(g.colors) 
        clr = g.colors[n]
    else:
        clr = ""
    # Print results if dry run, otherwise do the renaming
    for file in files:
        p = P(file)
        name, ext = p.stem.lower(), p.suffix.lower()
        newname = P(fmt % number + ext)
        while newname.exists():
            number += 1
            newname = P((fmt % number) + ext)
        if dry_run:
            s = f"{p!s:{g.width}s}{g.n}"
            s = s.replace(".", f"{clr}.")
            print(f"  {s}    {newname.stem}{clr}{newname.suffix}{g.n}")
        else:
            try:
                os.rename(file, newname)
            except Exception:
                print(f"Couldn't rename '{file}' to '{newname}'")
                if not d["-i"]:
                    exit(1)
        # Write undo command
        g.undo.append((str(newname), str(p)))
        number = number + 1
    os.chdir(currdir)
def WriteUndoFile(directory):
    if not d["-x"]:
        return 
    currdir = os.getcwd()
    os.chdir(directory)
    name, num = P(f"{g.name.stem}.undo"), 0
    while name.exists():
        num += 1
        name = P(f"{g.name.stem}.undo{num}")
    stream = open(name, "w")
    for item in g.undo:
        print(repr(item), file=stream)
    os.chdir(currdir)
def RunUndoFile(directory):
    currdir = os.getcwd()
    os.chdir(directory)
    # Get undo file
    p = P(d["-u"])
    if not p.exists():
        Error(f"'{d['-u']}' doesn't exist in {directory}")
    lines = [i for i in GetLines(p) if i]
    if not lines:
        Error(f"No lines in '{d['-u']}'")
    # First line must be the directory we're in
    first_line = P(lines.pop(0))
    dir = eval(str(first_line))
    if dir != directory:
        Error("Undo file for different directory")
    # Rename each file
    for line in lines:
        new, old = [P(i) for i in eval(line)]
        try:
            new.rename(old)
        except Exception:
            print(f"{g.err}'{new}' --> '{old}' rename failed{g.n}")
    os.chdir(currdir)
if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine()
    try:
        directory = P(args[0]).resolve()
    except IndexError:
        Error("You must include a directory on the command line")
    if d["-u"]:
        RunUndoFile(directory)
        exit()
    dry_run = not d["-x"]
    g.undo.append(directory)
    if dry_run:
        print(f"Directory = {g.dir}{directory}{g.n}")
    extensions, processed = args[1:], []
    GetWidth()
    for ext_number, extension in enumerate(extensions):
        if extension in processed:
            continue
        ProcessExtension(extension, directory, ext_number)
        processed.append(extension)
    WriteUndoFile(directory)

'''

- TODO
    - Architectural
        - From inspecting the code, it's not obvious how things work.  In
          particular, I can't see how Find() works.  Needs comments and a
          simpler implementation.
        - Uses os.walk:  switch to pathlib glob.  Depth can be found by
          counting items in p.parents.
        - TranslatePath shouldn't be needed -- this can be done by pathlib
        - Utilize the regex colorizing functions of color.py.
        - Use filter() and filterfalse() to more compactly do the required
          filtering.
        - Files with spaces in the names need to be quoted to allow
          downstream tools to work with them.
            - Look at -0 option to terminate strings with nulls so can work
              with xargs -0.
            - Also look at what character escapes are needed for the shell
    - Speed considerations
        - Avoid calling functions/lambdas written in python in inner loops.
          In-lining the loop can save a lot of time.
        - Locals are faster than globals.  If you need a global in a
          function, copy it to a local.  Function names(global or built-in)
          are also global constants.
        - map() with a built-in function beats a for loop
    - Other
        - Add -k to print in columns
        - Shorten the help.  Use -h for more complete explanations and more
          arcane options.
        - Change -h to -H
    - Bugs
        - f -d gsl doesn't show gsl-2.7/ in ~.
        - It should be able to find files that begin with 'r' by using the
        regex '^r.*$'.  Note that currently you have to use '/r' and it
        doesn't color the r of the files in the current directory.

File finding utility
    Similar to UNIX find, but less powerful.  It's not especially fast, but
    the usage is more convenient than find and the output is colorized to
    see the matches unless it's not going to a TTY.
 
 
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2008, 2012 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # File finding utility
        #∞what∞#
        #∞test∞# #∞test∞#
    # Imports
        import sys
        import re
        import getopt
        import os
        import fnmatch
        import subprocess
        from collections import OrderedDict as odict
        from pdb import set_trace as xx
        from pathlib import Path as P
    # Custom imports
        from wrap import dedent
        from color import Color, TRM as t
if 1:   # Global variables
    nl = "\n"
    # If you're using cygwin, set the following variable to point to the
    # cygpath utility.  Otherwise, set it to None or the empty string.
    # This tool allows UNIX-style path conversions so that command line
    # directory arguments like /home/myname work correctly.
    cygwin = "c:/cygwin/bin/cygpath.exe"
    #
    # The following variable, if True, causes a leading './' to be removed
    # from found files and directories.  This shortens things up a bit.
    # However, when the -s option is used, leaving rm_dir_tag False causes
    # the current directory's entries to be printed last and sorted in
    # alphabetical order.  This is how I prefer to see things, as
    # sometimes the matches can be quite long and scroll off the top of
    # the page.  Usually, I'm only interested in stuff in the current
    # directory.
    rm_dir_tag = False
    #
    # Colorizing 
    t.dir = t("redl")
    t.match = t("sky")
    t.end = t.n
if 1:   # Glob patterns and file extensions
    def GetSet(data, extra=None):
        # Glob patterns for source code files
        s = ["*." + i for i in data.split()]
        t = list(sorted(set(s)))
        if extra is not None:
            t.extend(extra)
        return t
    data_short = '''
        a asm awk bas bash bat bsh c c++ cc cpp cxx f f77
        f90 f95 gcode h hh hxx ino jav java json ksh
        l lex lib m m4 mk pas perl php pl rb
        re sh tcl tex tk vim yacc yaml
    '''
    source_code_files = GetSet(data_short, extra=["[Mm]akefile"])
    # Glob patterns for documentation files
    documentation_files = GetSet("doc docx odg ods odt xls xlsx")
    # Glob patterns for picture files
    picture_files = GetSet('''
        bmp clp dib emf eps gif img jpeg jpg pbm pcx pgm png ppm ps psd psp
        pspimage raw tga tif tiff wmf xbm xpm''')
    # Names of version control directories
    version_control = "git hg".split()
if 1:   # Utility
    def Help():
        print(dedent(f'''
        Sorting is used to make the directories come first in a listing.
        '''))
    def Usage(status=2):
        d["name"] = os.path.split(sys.argv[0])[1]
        d["-s"] = "Don't sort" if d["-s"] else "Sort"
        usage = r'''
        Usage:  {name} [options] regex [dir1 [dir2...]]
          Finds files using python regular expressions.  If no directories are
          given on the command line, searches at and below the current
          directory.  Color-coding is used if output is to a TTY.  Use -c
          to turn off color-coding.
        Options:
          -C str    Globbing pattern separation string (defaults to space)
          -c        Turn off color coding
          -D        Show documentation files
          -d        Show directories only
          -e glob   Show only files that match glob pattern (can be multiples)
          -f        Show files only
          -F        Show files only (exclude picture files)
          -h        Show hidden files/directories that begin with '.'
          -i        Case-sensitive search
          -L        Follow directory soft links (defaults to False)
          -l n      Limit recursion depth to n levels
          -P        Show picture files
          -p        Show python files
          -r        Not recursive; search indicated directories only
          -S        Show source code files excluding python
          -s        {-s} the output directories and files
          -x glob   Ignore files that match glob pattern (can be multiples)
          -V        Include revision control directories
          --git     Include git directories only
          --hg      Include Mercurial directories only
        Note:  
          regex on the command line is a python regular expression.
          Globbing patterns in the -e and -x options are the standard file
          globbing patterns in python's glob module.  The -e and -x options
          can contain spaces if you define a different separation string
          with the -C option
        Examples:
          - Find all python scripts at and below the current directory:
                  python {name} -p 
          - Find files at and below the current directory containing the string
              "rational" (case-insensitive search) excluding *.bak and *.o:
                  python {name} -C "," -f -x "*.bak,*.o" rational
          - Find any directories named TMP (case-sensitive search) in or below
              the current directory, but exclude any with 'cygwin' in the name:
                  python {name} -d -i -x "*cygwin*" TMP
          - Find all documentation and source code files starting with 't' in
              the directory foo
                  python {name} -DS /t foo
              This will also find files in directories that begin with 't' also.
          - Delete backup files at and below .; the '-u' for invoking python
              causes unbuffered output, allowing xargs use:
                  python -u {name} -f bak\$ | xargs rm
              Omit the 'rm' to have xargs echo what will be removed.
        '''[1:].rstrip()
        print(dedent(usage).format(**d))
        exit(status)
    def ParseCommandLine():
        d["-."] = False     # Show hidden files/directories
        d["-C"] = " "       # Separation string for glob patterns
        d["-D"] = False     # Print documentation files
        d["-L"] = False     # Follow directory soft links
        d["-P"] = False     # Print picture files
        d["-S"] = False     # Print source code files
        d["-c"] = True      # Turn off color coding
        d["-d"] = False     # Show directories only
        d["-F"] = False     # Show files only but no picture files
        d["-f"] = False     # Show files only
        d["-i"] = False     # Case-sensitive search
        d["-e"] = []        # Only list files with these glob patterns
        d["-l"] = -1        # Limit to this number of levels (-1 is no limit)
        d["-p"] = False     # Show python files
        d["-r"] = False     # Don't recurse into directories
        d["-s"] = False     # Sort the output directories and files
        d["-x"] = []        # Ignore files with these glob patterns
        d["-V"] = []        # Revision control directories to include
        if len(sys.argv) < 2:
            Usage()
        try:
            optlist, args = getopt.getopt(
                    sys.argv[1:], 
                    ".C:DLPScde:Ffhil:prsVx:",
                    longopts="git hg".split()
            )
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in ".DLPScdFfhiprs":
                d[o] = not d[o]
            if o == "-D":
                d["-e"] += documentation_files
            if o == "-P":
                d["-e"] += picture_files
            if o == "-S":
                d["-e"] += source_code_files
            if o == "-e":
                d[o] += a.split(d["-C"])
            if o == "-l":
                n = int(a)
                if n < 0:
                    raise ValueError("-l option must include number >= 0")
                d[o] = n
            if o == "-p":
                d["-e"] += ["*.py"]
            if o == "-V":
                d["-h"] = True
                d["-V"] = version_control
            if o == "-x":
                s, c = o, d["-C"]
                d["-x"] += a.split(d["-C"])
            # Long options
            elif o == "--hg":
                d["-h"] = True
                d["-V"] += ["hg"]
            elif o == "--git":
                d["-h"] = True
                d["-V"] += ["git"]
        if len(args) < 1:
            Usage()
        if d["-h"]:
            Help()
        if d["-i"]:
            d["regex"] = re.compile(args[0])
        else:
            d["regex"] = re.compile(args[0], re.I)
        args = args[1:]
        if len(args) == 0:
            args = ["."]
        # Store search information in order it was found
        d["search"] = odict()
        # Normalize -V option
        d["-V"] = list(sorted(list(set(d["-V"]))))
        if not d["-c"] or not sys.stdout.isatty():
            # No color is wanted, so turn off escape sequences
            t.dir = t.match = t.end = ""
            # Eventually, the following will work instead
            #t.on = False
        return args
if 1:   # Core functionality
    def Normalize(x):
        return x.replace("\\", "/")
    def TranslatePath(path, to_DOS=True):
        '''Translates an absolute cygwin (a UNIX-style path on Windows) to
        an absolute DOS path with forward slashes and returns it.  Use
        to_DOS set to True to translate from cygwin to DOS; set it to
        False to translate the other direction.
        '''
        direction = "-w" if to_DOS else "-u"
        if to_DOS and path[0] != "/":
            raise ValueError("path is not an absolute cygwin path")
        if "\\" in path:
            # Normalize path (cypath works with either form, but let's not
            # borrow trouble).
            path = path.replace("\\", "/")
        msg = ["Could not translate path '%s'" % path]
        s = subprocess.Popen((cygwin, direction, path),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errlines = s.stderr.readlines()
        if errlines:
            # Had an error, so raise an exception with the error details
            msg.append("  Error message sent to stderr:")
            for i in errlines:
                msg.append("  " + i)
            raise ValueError(nl.join(msg))
        lines = [i.strip() for i in s.stdout.readlines()]
        if len(lines) != 1:
            msg.append("  More than one line returned by cygpath command")
            raise ValueError(nl.join(msg))
        return lines[0].replace("\\", "/")
    def Ignored(s):
        '''s is a file name.  If s matches any of the glob patterns in
        d["-x"], return True.
        '''
        for pattern in d["-x"]:
            if d["-i"]:
                if fnmatchcase(s, pattern):
                    return True
            else:
                if fnmatch.fnmatch(s, pattern):
                    return True
        return False
    def Included(s):
        '''s is a file name.  If s matches any of the glob patterns in
        d["-e"], return True.
        '''
        for pattern in d["-e"]:
            if d["-i"]:
                if fnmatch.fnmatchcase(s, pattern):
                    return True
            else:
                if fnmatch.fnmatch(s, pattern):
                    return True
        return False
    def PrintMatch(s, start, end, isdir=False):
        'For the match in s, print things out in the appropriate colors'
        if isdir:
            print(f"{t.dir}{s[:start]}", end="")
        else:
            print(s[:start], end="")
        print(f"{t.match}{s[start:end]}", end="")
        if isdir:
            print(f"{t.dir}", end="")
        else:
            print(f"{t.end}", end="")
    def PrintMatches(s, isdir=False):
        '''Print the string s and show the matches in appropriate
        colors.  Note that s can end in '/' if it's a directory.
        '''
        if d["-f"] and not d["-d"]:
            # Files only -- don't print any matches in directory
            dir, file = os.path.split(s)
            print(dir, end="")
            if dir and dir[:-1] != "/":
                print("/", end="")
            s = file
        while s:
            if isdir and s[-1] == "/":
                mo = d["regex"].search(s[:-1])
            else:
                mo = d["regex"].search(s)
            if mo:
                PrintMatch(s, mo.start(), mo.end(), isdir=isdir)
                s = s[mo.end():]
            else:
                # If the last character is a '/', we'll print it in color
                # to make it easier to see directories.
                if s[-1] == "/":
                    print(s[:-1], end="")
                    print(f"{t.dir}/{t.end}", end="")
                else:
                    try:
                        print(s, end="")
                    except IOError:
                        # Caused by broken pipe error when used with less
                        exit(0)
                s = ""
        print()
    def Join(root, name, isdir=False):
        '''Join the given root directory and the file name and store
        appropriately in the d["search"] odict.  isdir will be True if
        this is a directory.  Note we use UNIX notation for the file
        system's files, regardless of what system we're on.
        '''
        # Note we check both the path and the filename with the glob
        # patterns to see if they should be included or excluded.
        is_ignored = Ignored(name) or Ignored(root)
        is_included = Included(name) or Included(root)
        if is_ignored:
            return
        if d["-e"] and not is_included:
            return
        root, name = Normalize(root), Normalize(name)
        if d["-V"]:         # Ignore version control directories
            # git
            if "git" not in d["-V"]:
                r = re.compile("/.git$|/.git/")
                mo = r.search(root)
                if mo or name == ".git":
                    return
            # Mercurial
            if "hg" not in d["-V"]:
                r = re.compile("/.hg$|/.hg/")
                mo = r.search(root)
                if mo or name == ".hg":
                    return
            # RCS
            if "RCS" not in d["-V"]:
                r = re.compile("/RCS$|/RCS/")
                mo = r.search(root)
                if mo or name == "RCS":
                    return
        # Check if we're too many levels deep.  We do this by counting '/'
        # characters.  If root starts with '.', then that's the number of
        # levels deep; otherwise, subtract 1.  Note if isdir is True, then
        # name is another directory name, so we add 1 for that.
        lvl = root.count("/") + isdir
        if root[0] == ".":
            lvl -= 1
        if d["-l"] != -1 and lvl >= d["-l"]:
            return
        if root == ".":
            root = ""
        elif rm_dir_tag and len(root) > 2 and root[:2] == "./":
            root = root[2:]
        s = Normalize(os.path.join(root, name))
        d["search"][s] = isdir
    def Find(dir):
        def RemoveHidden(names):
            '''Unless d["-h"] is set, remove any name that begins with '.'.
            '''
            if not d["-h"]:
                names = [i for i in names if i[0] != "."]
            return names
        pics = set([i[2:] for i in picture_files])
        def RemovePictures(names):
            '''If d["-F"] is True, remove picture file names
            '''
            if d["-F"]:
                keep = []
                for i in names:
                    p = P(i)
                    ext = p.suffix[1:]
                    if ext not in pics:
                        keep.append(i)
                return keep
            return names
        contains = d["regex"].search
        def J(root, name):
            return Normalize(os.path.join(root, name))
        find_files = d["-f"] & ~ d["-d"]
        find_dirs = d["-d"] & ~ d["-f"]
        follow_links = d["-L"]
        for root, dirs, files in os.walk(dir, followlinks=follow_links):
            # If any component of root begins with '.' and it's not '..',
            # ignore unless d["-h"] is set.
            has_dot = any([i.startswith(".") and len(i) > 1 and i != ".."
                        for i in root.split("/")])
            if not d["-h"] and has_dot:
                continue
            files = RemoveHidden(files)
            files = RemovePictures(files)
            dirs = RemoveHidden(dirs)
            if find_files:
                [Join(root, name) for name in files if contains(name)]
            elif find_dirs:
                [Join(root, dir) for dir in dirs
                    if contains(J(root, dir))]
            else:
                [Join(root, name, isdir=True) for name in dirs
                    if contains(J(root, name))]
                [Join(root, name) for name in files if contains(J(root, name))]
            if d["-r"]:  # Not recursive
                # This works because the search is top-down
                break
    def PrintReport():
        'Note we put a "/" after directories to flag them as such'
        D = d["search"]
        if d["-s"]:
            # Print things in sorted form, directories first.
            dirs, files = [], []
            # Organize by directories and files.  Note you need to use keys()
            # to get the original insertion order
            for i in D.keys():
                if D[i]:
                    dirs.append(i)
                else:
                    files.append(i)
            print(f"{t.end}", end="")
            dirs.sort()
            files.sort()
            if not d["-d"] and not d["-f"]:
                # Both directories and files
                for i in dirs:
                    PrintMatches(i + "/",isdir=True)
                for i in files:
                    PrintMatches(i)
            else:
                if d["-d"]:  # Directories only
                    for i in dirs:
                        PrintMatches(i + "/", isdir=True)
                else:  # Files only
                    for i in files:
                        PrintMatches(i)
        else:
            # Print things as encountered by os.walk
            for i in D.keys():
                if (d["-f"] and D[i]) or (d["-d"] and not D[i]):
                    continue
                PrintMatches(i + "/" if D[i] else i, isdir=D[i])
        print(f"{t.end}", end="")
if __name__ == "__main__":
    d = {}  # Settings dictionary
    directories = ParseCommandLine()
    for dir in directories:
        Find(dir)
    PrintReport()

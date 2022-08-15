'''

- TODO
    - Add -t for type

File finding utility
    Similar to UNIX find, but slower.  Easier to use and the matches are
    colorized.

'''
if 1:   # Header
    # Copyright, license
    if 1:
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
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
    # Standard imports
    if 1:
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
        from pprint import pprint as pp
        from itertools import filterfalse as remove
    # Custom imports
    if 1:
        from wrap import wrap, dedent
        from color import Color, TRM as t, RegexpDecorate
        from dbg import Debug
    # Global variables
    if 1:
        #dbg.dbg = True
        Dbg = Debug()
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(f"{t.n}", end="", file=sys.stderr)
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regex [dir1 [dir2...]]
          Finds files using python regular expressions.  If no directories
          are given on the command line, searches at and below the current
          directory.
        Options:
            -c      Turn on color-coding
            -d      Search for directories only
            -f      Search for files only
            -i      Make regex search case-sensitive
            -l n    Limit depth of search to n levels
            -r      Do not do a recursive search
            -t typ  Show indicated type of files (see below)
            --git   Include .git directories
            --hg    Include .hg directories
            --nohiddendirs
                    Remove hidden directories
            --nohiddenfiles
                    Remove hidden files
        File types (more than one -t option allowed)
          doc       Documentation files
          pdf       PDF files
          pic       Picture files
          py        Python source files
          src       Source code files
          zip       Compressed archives
        '''))
        exit(status)
    def ParseCommandLine():
        d["-c"] = False     # Use color coding
        d["-d"] = False     # Show directories only
        d["-f"] = False     # Show files only
        d["-i"] = True      # Ignore case in searches
        d["-l"] = -1        # Limit to this number of levels (-1 is no limit)
        d["-r"] = False     # Don't recurse into directories
        d["-t"] = []        # Type(s) to select
        # Long options
        d["--git"] = False  # Include .git directories
        d["--hg"] = False   # Include .hg directories
        d["--nohiddendirs"] = False
        d["--nohiddenfiles"] = False
        if len(sys.argv) < 2:
            Usage()
        longopts = '''git hg nohiddenfiles nohiddendirs'''.split()
        longnames = ["--" + i for i in longopts]
        try:
            opts, dirs = getopt.getopt(sys.argv[1:], "cdfil:rt:", longopts)
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cdfi"):
                d[o] = not d[o]
            if o in longnames:
                d[o] = not d[o]
            elif o == "-l":
                d[o] = n = int(a)
                if n <= 0:
                    if n != -1:
                        Error('d["-l"] option must be > 0')
            elif o == "-t":
                allowed = "doc pdf pic py src zip".split()
                if a in allowed:
                    d[o].append(a)
                else:
                    Error(f"{a!r} is not a recognized type")
        if d["-t"]:
            # If the -t option is given, no regex is required
            regex = None
            dirs = dirs if dirs else ["."]
        else:
            if not dirs:
                Usage()
            regex = dirs.pop(0)
            if not dirs:
                dirs = ["."]
        # Debug dump of d
        Dbg("Options dictionary:")
        for i in d:
            Dbg(f"    d[{i}] = {d[i]}")
        return regex, dirs
if 1:   # Core functionality
    def ColorCoding():
        'Set up color coding escape sequences'
        cc = d["-c"]
        t.norm = t.n if cc else ""
        e = "\x1b[01;31m"   # This will match grep & ls color for directories
        t.dirs = e if cc else ""
        t.files = t("whtl", "blu") if cc else ""
    def GetDirectories(dir):
        '''Return a list of direcctories as Path instances at and below dir.
            Filter out the things indicated by the options in d.
        '''
        Dbg(f"GetDirectories({dir!r})")
        p = P(dir)
        if not p.exists():
            Error(f"Directory {dir!r} doesn't exist")
        # Get the directories as a sequence of Path instances
        dirs = [i for i in p.rglob("*") if i.is_dir()]
        if 1:   # Filter out unwanted stuff
            if not d["--git"]:
                # Remove .git directories
                def HasGit(item):
                    return ".git" in item.parts
                dirs = remove(HasGit, dirs)
            if not d["--hg"]:
                # Remove .hg directories
                def HasHg(item):
                    return ".hg" in item.parts
                dirs = remove(HasHg, dirs)
            if d["--nohiddendirs"]:
                # Remove hidden directories
                def IsHiddenDir(item):
                    return any(i.startswith(".") for i in item.resolve().parts)
                dirs = remove(IsHiddenDir, dirs)
            if d["-l"] != -1:
                # If only a certain level is wanted, prune out the deeper ones
                N = len(p.parents)
                def TooDeep(item):
                    return len(item.parts) - N > d["-l"]
                dirs = remove(TooDeep, dirs)
        return dirs
    def GetFiles(dir):
        '''Return a list of files as Path instances at and below dir.
            Filter out the things indicated by the options in d.
        '''
        Dbg(f"GetFiles({dir!r})")
        p = P(dir)
        if not p.exists():
            Error(f"Directory {dir!r} doesn't exist")
        # Get the files as a sequence of Path instances
        files = p.glob("*") if d["-r"] else p.rglob("*")
        files = [i for i in files if i.is_file()]
        if 1:   # Filter out unwanted stuff
            if not d["--git"]:
                # Remove .git directories
                def HasGit(item):
                    return ".git" in item.parent.parts
                files = remove(HasGit, files)
            if not d["--hg"]:
                # Remove .hg directories
                def HasHg(item):
                    return ".hg" in item.parent.parts
                files = remove(HasHg, files)
            if d["--nohiddendirs"]:
                # Remove hidden directories
                def IsHiddenDir(item):
                    return any(i.startswith(".") for i in item.resolve().parent.parts)
                files = remove(IsHiddenDir, files)
            if d["--nohiddenfiles"]:
                # Remove hidden files
                def IsHiddenFile(item):
                    return item.name.startswith(".")
                files = remove(IsHiddenFile, files)
            if d["-l"] != -1:
                # If only a certain level is wanted, prune out the deeper ones
                N = len(p.parents)
                def TooDeep(item):
                    return len(item.parents) - N > d["-l"]
                files = remove(TooDeep, files)
        if 0:
            # Dump the files found
            for i in files:
                print(f"+ {i}")
        return list(files)
    def ApplyRegexToFiles(files, regex, keep=True):
        '''Apply the compiled regular expression in regex to the files and
        return them as a list if keep is True; otherwise, remove those
        files and return a list of the remainder.  The original list is not
        modified.
        '''
        if d["-d"]:     # Only operating on directories
            return []
        def IsMatchedFile(file):
            return bool(regex.search(file.name))
        action = filter if keep else remove
        files = list(action(IsMatchedFile, files))
        return files
    def ApplyRegexToDirectories(dirs, regex, keep=True):
        '''Apply the compiled regular expression in regex to the
        directories in dirs and return them as a list if keep is True;
        otherwise, remove those directories and return the list of the
        remainder.  The original list is not modified.
        '''
        if d["-f"]:     # Only operating on files
            return []
        def IsMatchedDir(dir):
            return bool(regex.search(str(dir)))
        action = filter if keep else remove
        dirs = list(action(IsMatchedDir, dirs))
        return dirs
    def PrintDirectories(dirs):
        if not dirs:
            return
        rd = RegexpDecorate()
        rd.register(d["regex"], t.dirs, t.norm) 
        for i in dirs:
            rd(str(i), insert_nl=True)
    def PrintFiles(files):
        if not files:
            return
        rd = RegexpDecorate()
        rd.register(d["regex"], t.files, t.norm) 
        for i in files:
            q = '"' if " " in str(i) else ""
            # Don't print files in current directory with leading './'
            if str(i.parent) != ".":
                print(q + str(i.parent) + "/", end="")
            rd(i.name, insert_nl=False)
            print(q)
    def SelectItems(dirs, files):
        '''Select the desired files and directories as indicated by the
        options and return (dirs, files) where the two items are lists.
        '''
        if not d["-t"]:
            # Simple selection by one regex
            out_dirs = ApplyRegexToDirectories(dirs, d["regex"], keep=True)
            out_files = ApplyRegexToFiles(files, d["regex"], keep=True)
            return out_dirs, out_files
        # Get the relevant file extensions
        ext = []
        for typ in d["-t"]:
            if typ == "py":
                ext.extend("py".split())
            elif typ == "pdf":
                ext.extend("pdf".split())
            elif typ == "pic":
                ext.extend('''bmp clp dib emf eps gif img jpeg jpg pbm pcx pgm
                            png ppm ps psd psp pspimage raw tga tif tiff wmf
                            xbm xpm'''.split())
            elif typ == "doc":
                ext.extend("doc docx odg ods odt xls xlsx".split())
            elif typ == "src":
                ext.extend('''asm awk bas bash bat bsh c c++ cc cpp cxx f f77
                            f90 f95 gcode h hh hxx ino jav java json ksh l lex
                            lib m m4 mk pas perl php pl rb re sh tcl tex tk
                            vim yacc yaml'''.split())
            elif typ == "zip":
                ext.extend("zip rar gz gzip tgz 7z bz bz2 tar.gz".split())
            else:
                raise Exception(f"{typ!r} is a bug:  not allowed for -t option")
        # Create regex for these file types
        ext = [r"\." + i + "$" for i in ext]
        s = '|'.join(ext)
        s = s.replace("+", r"\+")
        if "src" in d["-t"]:
            # Also show makefiles
            s += r"|[mM]akefile$"
        d["regex"] = regex = re.compile(s) if d["-i"] else re.compile(s, re.I)
        # We'll keep only files
        out_dirs = []
        out_files = ApplyRegexToFiles(files, regex, keep=True)
        return out_dirs, out_files

if 0:
    exit()

if __name__ == "__main__":
    d = {}  # Settings dictionary
    regex, directories = ParseCommandLine()
    ColorCoding()
    re_flag = re.I if d["-i"] else 0
    if regex is not None:
        d["regex"] = re.compile(regex, re_flag)
        Dbg(f"regex = {d['regex']!r}")
    dirs, files = [], []
    for dir in directories:
        # Get files
        filelist = GetFiles(dir)
        files.extend(filelist)
        # Get directories
        dirlist = GetDirectories(dir)
        dirs.extend(dirlist)
    dirs, files = SelectItems(dirs, files)
    PrintDirectories(dirs)
    PrintFiles(files)

'''
Given one or more regular expressions on the command line, searches
the PATH for all files that match and prints them out.
'''
if 1:   # Header
    # Copyright, license
    if 1:
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Search PATH for regular expressions
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    # Standard imports
    if 1:
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
        import stat
        from pdb import set_trace as xx
    # Custom imports
    if 1:
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from columnize import Columnize
    # Global variables
    if 1:
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        class g:
            pass
        g.seen_windows = False
        # Store any matches in the matches dictionary so that there are
        # no duplicates.
        matches = {}
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regexp1 [regexp2...]
            Find all files in the PATH directories that match a python regular
            expression.
        Options:
            -c      Print in columns [true]
            -i      Ignore case [true]
            -v      Print whether Windows directory is ignored [false]
            -w      Include C:/WINDOWS if it is in path [false]
            -x      Only show executables [true]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Print in columns
        d["-i"] = True      # Ignore case
        d["-v"] = False     # Verbose
        d["-w"] = False     # Include C:/WINDOWS if it is in path
        d["-x"] = True      # Only show executables
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, regexps = getopt.getopt(sys.argv[1:], "chivwx", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("civwx"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return regexps
if 1:   # Core functionality
    def GetRegexps(regexps):
        '''Return a list of compiled regular expressions.
        '''
        regexp_list = []
        for regex in regexps:
            if d["-i"]:
                regexp_list.append(re.compile(regex, re.I))
            else:
                regexp_list.append(re.compile(regex))
        return regexp_list
    def ForwardSlashes(dir):
        '''Change any backslashes to forward slashes.
        '''
        return dir.replace("\\", "/")
    def GetListOfDirectories():
        # Get a list of the directories in the path
        sep = ":"
        key = "PATH"
        if sys.platform == "win32":
            sep = ";"
        if "HOME" in os.environ.keys():
            home = os.environ["HOME"]
        else:
            home = "/home/Don"
        if key in os.environ.keys():
            PATH = os.environ[key]
            directories = re.split(sep, os.environ[key])
            directories = map(ForwardSlashes, directories)
            directories = [i.replace("\\", "/") for i in directories]
            directories = [i.replace("~", home) for i in directories]
        else:
            Error("No PATH variable in environment")
        # Add in plib
        directories += ["/plib", "/plib/pgm"]
        directories = [i for i in directories if i]     # Remove empty strings
        return directories
    def PrintResults():
        files = list(matches.keys())
        files.sort()
        if d["-c"]:
            for line in Columnize(files):
                print(line.replace("\\", "/"))
        else:
            for file in files:
                print(file.replace("\\", "/"))
    def IsExecutable(file):
        'Return True if the file is executable'
        try:
            s, n = file.lower(), 4
            if sys.platform == "win32":
                # Windows executables can end in .exe or .bat.
                if len(s) > n:
                    if s[-n:] in (".exe", ".bat"):
                        return True
            else:
                if os.path.isfile(file):
                    s = open(file, "rb").read(2)
                    if s == b"#!":
                        return True
                    # Check permissions too
                    st = os.stat(file).st_mode
                    exmask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                    if exmask | st:
                        return True
        except Exception:
            pass
        return False
    def CheckDirectory(dir, regexps):
        '''dir is a directory name, regexps is a list of compiled
        regular expressions.  cd to the indicated directory and
        put any filenames found that match the regexps into the
        matches dictionary.  Note that we don't check to see if
        they're executables or not.
        '''
        global matches
        msg = "Ignoring c:/windows (use -w if you don't want to ignore it)\n"
        if d["-w"]:
            if dir.lower()[:10] == "c:/windows":
                if not g.seen_windows:
                    if d["-v"]:
                        sys.stderr.write(msg)
                    g.seen_windows = True
                return
        currdir = os.getcwd()
        try:
            os.chdir(dir)
            for file in os.listdir(dir):
                if not os.path.isfile(file):
                    continue
                for regexp in regexps:
                    if regexp.search(file) is not None:
                        path = os.path.abspath(os.path.join(dir, file))
                        path = path.replace("\\", "/")
                        if d["-x"]:
                            if IsExecutable(path):
                                matches[path] = ""
                        else:
                            matches[path] = ""
        except FileNotFoundError:
            sys.stderr.write("Warning:  directory '%s' in PATH not found\n" % dir)
        os.chdir(currdir)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    regexp_list = GetRegexps(args)
    directories = GetListOfDirectories()
    for dir in directories:
        if not dir:
            continue
        CheckDirectory(dir, regexp_list)
    PrintResults()

'''
TODO
    * On 21 Jun 2021 I got rid of Walker use and used pathlib.Path.glob
      for recursive file generation.  This may have some remnant effects
      in options not fully tested, so first check that a string
      manipulation is made with str(P()) rather than P() directly.

Recursive grep
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Recursive grep
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx
    from textwrap import dedent
    import getopt
    import os
    import pathlib
    import re
    import sys
if 1:   # Custom imports
    from columnize import Columnize
    from wrap import dedent
    import color as C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    name = sys.argv[0]
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    {name} [options] regexp [dir1 [dir2 ...]]
      Recursively searches the indicated directories for files with
      content that match the given regexp.  If no directories are given,
      searches the current directory.  
    Options (+ means that option can appear more than once):
      -C          Don't use color
      -c          Search C/C++/Arduino source files
      -d regexp + Ignore these directories
      -e          Echo the files that would be searched and exit
      -F          Interpret regexps as plain text
      -f file   + The regexps are in a file, one per line
      -g regexp + Files to search for
      -h          Show hidden files/directories
      -i          Ignore case
      -L          List files that didn't have a match
      -l          List files that had a match
      -n          Show line number of match
      -p          Search python source files
      -q          Exit with status 0 when any match found; otherwise 1
      -r n        Limit recursion to n levels.  n == 0 means regular grep.
      -s          Show messages about nonexistent/nonreadable files
      -V          Include revision control directories in search
      -x regexp + Ignore these file types
      '''))
    exit(status)
def ParseCommandLine(d):
    d["-C"] = False     # Don't use color
    d["-c"] = False     # Find C/C++ source files
    d["-d"] = []        # Ignore these directory regexps
    d["-e"] = False     # Echo files that would be searched
    d["-F"] = False     # Interpret regexp as plain text
    d["-f"] = []        # File(s) containing regexps to use for searching
    d["-g"] = []        # Regexp patterns for files to search
    d["-h"] = False     # Show hidden files/directories
    d["-i"] = False     # Ignore case
    d["-L"] = False     # List files that didn't have a match
    d["-l"] = False     # List files that had a match
    d["-n"] = False     # Show 1-based line number of match
    d["-p"] = False     # Find python source files
    d["-q"] = False     # Exit with status 0 when any match found; otherwise 1
    d["-r"] = None      # Limit recursion level
    d["-s"] = False     # Suppress messages about nonexistent/nonreadable files
    d["-V"] = False     # Search revision control directories
    d["-x"] = []        # Ignore these file regexp patterns
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Ccd:eFf:g:hiLlnpqr:sVx:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    boolean = ["-" + i for i in "CcDeFhiLlnpqsV"]
    for o, a in opts:
        if o in boolean:
            d[o] = not d[o]
        elif o in ("-d", "-f", "-g", "-x"):
            d[o].extend(a.split())
        elif o in ("-r",):      # Limit recursion level
            try:
                d[o] = int(a)
                if d[o] < 0:
                    raise Exception()
            except Exception:
                Error("-r option must be an integer >= 0")
    d["-d"].extend([re.compile(r"__pycache__")])
    if not d["-V"]:
        d["-d"].extend([
            re.compile(r"\.hg"),
            re.compile(r"\.git"),
            re.compile(r"\.bzr"),
            re.compile(r"RCS")])
    if d["-c"]:
        d["-g"].extend(
            [re.compile(r"\.c$", re.I),
             re.compile(r"\.cpp$", re.I),
             re.compile(r"\.h$", re.I),
             re.compile(r"\.hpp$", re.I),
             re.compile(r"\.ino$", re.I),
             re.compile(r"\.pde$", re.I)
            ]
        )
    if d["-p"]:
        d["-g"].extend([re.compile(r"\.py$", re.I)])
    for o in "-d -f -g -x".split():
        d[o] = list(set(d[o]))  # Only keep unique items
    if not args and not d["-e"]:
        Usage(d)
    return args
def GetRegexp(regexp, d):
    '''Return a list of one or more compiled regular expressions.  If -F 
    is True then the list is a set of strings.
    '''
    regexps = []
    if d["-f"]:
        # Regular expressions are in a set of files
        for file in d["-f"]:
            for line in open(file):
                if line[-1] == "\n":
                    line = line[:-1]
                if not line:
                    continue
                if d["-F"]:
                    regexps.append(line)
                else:
                    if d["-i"]:
                        regexps.append(re.compile(line, re.I))
                    else:
                        regexps.append(re.compile(line))
    else:
        if d["-F"]:
            regexps = [regexp]
        elif d["-i"]:
            regexps = [re.compile(regexp, re.I)]
        else:
            regexps = [re.compile(regexp)]
    return regexps
def IsHidden(head, tail):
    '''If the components of head or tail are hidden, return True.  Note we
    assume directory paths are separated by '/' characters.  head is a
    directory entry and tail is a file name.
    '''
    if tail.startswith("."):
        return True
    for dir in head.split("/"):
        if dir.startswith(".") and dir != "." and dir != "..":
            return True
    return False
def FilterRegexps(files, d):
    '''Use the command line options to filter the files and directories to
    get the list of files to process.
    '''
    dregexps = [re.compile(i) for i in d["-d"]]
    xregexps = [re.compile(i) for i in d["-x"]]
    # First, filter out the files and directories we don't want
    filtered = []
    for file in files:
        #head, tail = os.path.split(file)
        head, tail = str(file.parent), file.name
        matched = False
        for r in dregexps:  # Directories to ignore
            if r.search(head):
                matched = True
                break
        for r in xregexps:  # Files to ignore
            if r.search(tail):
                matched = True
                break
        if not d["-h"] and IsHidden(head, tail):
            continue
        if matched:
            continue
        filtered.append(file)
    # In the remaining set of files, keep any specified by d["-g"]
    if d["-g"]:
        new_filtered = []
        gregexps = [re.compile(i) for i in d["-g"]]
        for file in filtered:
            #head, tail = os.path.split(file)
            head, tail = str(file.parent), file.name
            for r in gregexps:  # File types to include
                if r.search(tail):
                    new_filtered.append(file)
                    break
        filtered = new_filtered
    return filtered
def GetFileList(d):
    '''Return a list of the files to search.
    '''
    files = []
    for dir in d["dirs"]:
        p = P(dir)
        for file in p.glob("**/*"):
            if file.is_file():
                files.append(file)
    # Remove or keep files per the options -d, -x, and -h
    files = FilterRegexps(files, d)
    # Remove any './' from the front of the files
    files = [StripCurrDir(i) for i in files]
    d["files"] = files
    if d["-e"]:
        EchoFileList(d)
        exit(0)
def EchoFileList(d):
    '''Print the found file list to stdout and exit.
    '''
    for i in d["files"]:
        print(i)
    exit(0)
def LineMatch(line, regexps):
    '''Return a list of the match objects if there are one or more matches
    with the regexps.  Return an empty list for no matches.
    '''
    mo_list = []
    for r in regexps:
        mo = r.search(line)
        if mo:
            mo_list.append(mo)
    return mo_list
def StripCurrDir(s):
    assert(ii(s, P))
    t = str(s)
    t = t[2:] if t.startswith("./") else t
    return P(t)
def ListFiles(d):
    '''This lists the files that have (d["-l"]) or don't have (d["-L"]) the
    regexps to search for.
    '''
    if d["-l"]:
        # List files that match one or more the regexps
        matches = []    # Store (file, match_count)
        for file in d["files"]:
            try:
                for line in open(file):
                    mo_list = LineMatch(line, d["regexps"])
                    if mo_list:
                        matches.append((file, len(mo_list)))
                        break;
            except Exception as e:
                if d["-s"]:
                    print(f"Can't process file '{file}':", file=sys.stderr)
                continue
        if matches:
            for file, count in matches:
                if d["-c"]:
                    print(f"{file}: {count}")
                else:
                    print(StripCurrDir(file))
    else:
        # List files that don't match any of the regexps
        for file in d["files"]:
            matched = False
            try:
                for line in open(file):
                    mo_list = LineMatch(line, d["regexps"])
                    if mo_list:
                        matched = True
                if not matched:
                    print(StripCurrDir(file))
            except Exception as e:
                if d["-s"]:
                    print(f"Can't process file '{file}':", file=sys.stderr)
                continue
def RmLinefeed(line):
    while line and line[-1] == "\n":
        line = line[:-1]
    return line
def Search(d):
    '''For the given regexps, find matching text lines in the indicated
    files.
    '''
    # The results list will contain (file, lineno, line, match_object) for
    # regex searches or (file, lineno, line, matched_string) for -F plain
    # text searches.
    results = []
    for file in d["files"]:
        try:
            handle = open(file)
            for linenum, line in enumerate(handle):
                if not line:
                    continue
                line = RmLinefeed(line)
                if not line:
                    continue
                for r in d["regexps"]:
                    if d["-F"]:
                        if line.find(r) != 1:
                            results.append((file, linenum, line, r))
                        elif d["-v"]:
                            results.append((file, linenum, line, r))
                    else:
                        mo = r.search(line)
                        if mo:
                            results.append((file, linenum, line, mo))
        except Exception as e:
            if d["-s"]:
                print(f"Can't process file '{file}[{linenum + 1}]':  {e}", 
                      file=sys.stderr)
            continue
    incl_file = len(d["files"]) > 1
    if results:
        for file, linenum, line, mo in results:
            if incl_file:   # Multiple files
                if d["-n"]:
                    print(f"{file}:{linenum}: ", end=" ")
                    if d["-C"]:
                        print(f"{line}")
                    else:
                        C.PrintMatch(line, mo.re)
                else:
                    print(f"{file}: ", end=" ")
                    if d["-C"]:
                        print(f"{line}")
                    else:
                        C.PrintMatch(line, mo.re)
            else:   # Only one file
                if d["-n"]:
                    print(f"{linenum}: ", end=" ")
                    if d["-C"]:
                        print(f"{line}")
                    else:
                        C.PrintMatch(line, mo.re)
                else:
                    if d["-C"]:
                        print(f"{line}")
                    else:
                        C.PrintMatch(line, mo.re)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # regexps will be a list of compiled python regexps to search for
    if not d["-e"]:
        d["regexps"] = GetRegexp(args[0], d)
    if d["-f"] or d["-e"]:
        d["dirs"] = args if args else ["."]
    else:
        d["dirs"] = args[1:] if args[1:] else ["."]
    GetFileList(d)
    # For efficiency, we use different methods to do the searching.
    if d["-l"] or d["-L"]:
        ListFiles(d)
    else:
        Search(d)        

"""
Recursive grep
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Recursive grep
    ##∞what∞#
    ##∞test∞# ["rgrep_test.py"] #∞test∞#
    pass
if 1:  # Imports
    from pdb import set_trace as xx
    from textwrap import dedent
    import getopt
    import os
    import pathlib
    import re
    import sys
    from functools import partial
    from collections import deque
    from pprint import pprint as pp
if 1:  # Custom imports
    from columnize import Columnize
    from wrap import dedent, wrap
    from color import t as T, RegexpDecorate
    from lwtest import run, raises, assert_equal, Assert

    if 0:
        import debug

        debug.SetDebugger()
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance

    class g:  # Global variable container
        pass

    # If stdout is a TTY
    g.istty = sys.stdout.isatty()
    # Identify when we're on a Windows file system
    f = sys.platform.startswith
    g.windows = f("cygwin") or f("win32")
    del f
    # Name of script
    g.name = sys.argv[0]
    g.pgm = f"python {g.name}"
    # Flag for compiling regular expressions
    g.I = 0
    # True for debug output
    g.debug = False
    # Regex decorator
    g.rd = RegexpDecorate()


def EnableColor(state=0):
    """state is 0, 1 or 2.  If 0, color is enabled when stdout is a TTY.
    If 1, color is enabled for all output.  If 2, color is disabled.
    """
    if 0:  # Old color stuff
        C = color.C
        S = color.Style(color.lred, color.black)
        g.PrintMatch = partial(color.PrintMatch, style=S)
    else:

        def Decorate(line, mo):
            """mo will either be a match object with a compiled regexp or a
            string if d['-t'] is True.  Make sure the g.rd object has this
            regex/string's signature in its style dict.
            """
            fg, bg = T("yell"), T.n
            if ii(mo, str):
                g.rd.register(re.compile(mo), fg, bg)
            else:
                if mo not in g.rd._styles:
                    g.rd.register(mo, fg, bg)
            if "\n" not in line:
                g.rd(line + "\n")
            else:
                g.rd(line)

        g.PrintMatch = Decorate
    if state == 0:  # Color if stdout is a TTY

        def f(x):
            return x if g.istty else ""

        if not g.istty:
            g.PrintMatch = lambda x, y: print(x)
    elif state == 1:  # Color always

        def f(x):
            return x
    elif state == 2:  # Color off

        def f(x):
            return ""

        g.PrintMatch = lambda x, y: print(x)
    else:
        raise ValueError("Programming bug:  state has bad value")
    g.fn = f(T("whtl"))  # Match filename color
    g.co = f(T("cynl"))  # Match colon color
    g.ln = f(T("magl"))  # Match line number color
    g.ma = f(T("yell"))  # Match color
    g.ba = f(T("blk"))  # Background color
    g.dbg = f(T("cyn"))  # Debug information color
    g.n = f(T.n)  # Normal printing


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Debug(*m, **kw):
    "Print colored debug information"
    if not g.debug:
        return
    print(f"{g.dbg}", end="")
    m = list(m)
    m.append(f"{g.n}")
    print(*m, **kw)


def Manpage():
    pgm = f"python {g.name}"
    print(
        dedent(
            f"""
 
    Simplest use case
 
      You are probably familiar with the grep tool, which searches for matches
      to a regular expression in a set of files specified on the command line.
      The typical GNU grep has a -r option for recursive searches and for many
      tasks, GNU grep will work well and be faster than a python script.
      However, sometimes it's convenient to have a dedicated tool and I use
      the {g.name} script mostly when working on python files.  I use the -p
      option, which restricts the search to python files and alias the command
      '{g.name} -p' to 'pgrep'.  Then finding the files that contains the
      string 'IsPunctuation' is done by the command
 
        pgrep IsPunctuation
 
      when I'm in the directory of interest.  This shows me all the files that
      have the string and the relevant line with the string highlighted in
      color.
 
    Finding programming symbols
 
      This script is handy in my python directories /plib and /plib/pgm, where
      I keep most of my python modules and utilities.  When I'm working on
      code, I can quickly find all the files that use a particular symbol
      (token).  For example, the module /plib/bidict.py supplies a bidict, a
      bidirectional dictionary.  I can find all uses of 'bidict' in python
      files with the command 'pgrep -l bidict', which is like how you'd use
      grep to do the search in the current directory (i.e., 'grep -l bidict
      *.py').
 
      If you search text files with a particular set of extensions frequently,
      it's easy to add a new option to {name} that will search for files with
      those extensions:  modify the patterns variable in GetFileList() (it
      holds the relevant glob patterns) and add the option in
      ParseCommandLine().  This is useful in software projects where you work
      on a subset of file types a lot.  Python is fast enough for a few
      hundred to a few thousand files and it's easier to tune a python script
      rather than try to build a customized grep from its source code.
 
      Another use case is when you want to have a symbol in all project files
      and you want to find the files that don't have the token.  Use the -L
      option for this case.  For example, management might dictate that all
      project source code files have the copyright string 'Copyright (C) 2020 
      OurCompanyName'.  The command 
 
        {pgm} -L 'Copyright (C) 2020 OurCompanyName'
 
      in the top level project directory would show you the files that need to
      have the message added.
 
    Finding strings
 
      Sometimes we need to look for a string rather than a regular expression
      and the string contains characters that are special to regular expression
      syntax.  For this case, use the -t option, which tells the script to just
      do a string search.  Combine it with the -i option if you want to ignore
      case.
 
    Color output
 
      By default, the strings found in a search that match the regular
      expressions will be highlighted in color, similar to how GNU grep works
      when you turn on coloring.  You can change these colors in the
      EnableColor() function.
 
      Normally, if output is not going to a TTY-type device (e.g., the command
      is in a pipeline), the colorizing is turned off so the escape codes
      don't wind up in a file.  Sometimes you want the escape codes to remain
      so e.g. you can cat the file later; in this case, use the '-C 1' option,
      which always includes the escape codes.  If you never want escape codes
      in the output, use '-C 2'.
 
    Multiple regular expressions
 
      The -f option lets you use a file of regular expressions to search for.
      This is handy when you have a number of programming symbols to find in a
      group of files.
 
      Example:  
          Suppose I'm in my python modules directory /plib.  I've
          changed the symbol names in a module from 
              GetFileLines           to           GetLines
              GetFileLine            to           GetLine
              GetFileNumberedLines   to           GetNumberedLines
          To ensure that all dependent python scripts have had their symbols
          changed to these new names, I put the following lines in the file
          'tokens':
              GetFileLines
              GetFileLine
              GetFileNumberedLines
          I then use the command 
              '{pgm} -l -p -f tokens /plib'
          and if I get any output, those are files that need attention.
 
      Note that the -f option will strip leading and trailing whitespace from
      the regular expressions, as this is typical when searching for
      programming tokens.  If the whitespace is important to keep, use the -F
      option in conjunction with the -f option.
 
    What files to search
 
      The method of finding files is to use pathlib.Path.rglob() to find all
      files in each directory given.  Then this sequence of files is reduced
      by applying the constraints in the options, using regular expressions
      from the python re module.  This has the advantage on case-insensitive
      file systems like Windows, where x.cpp, x.Cpp, x.cPp, etc. can all refer
      to the same file, which is handled by compiling the regular expressions
      to ignore case.  The rglob() command has no option to ignore case.

      The -e option with nothing else prints a list of files that would be
      searched.  If you invoke it with the arguments '-eVh .', you should get
      essentially the same output you'd get with a 'find . -type f' command
      (there may be differences in e.g. the leading strings like './' on
      stuff in the current directory from find because {g.name} strips any
      leading './' strings).
 
    Testing
 
      Here's the scheme I used to test that the script's functionality was
      working.  It may help illuminate how the options work.  This was done on
      a Windows machine running cygwin.
 
      In an empty directory, create the following files:
        .c.py  a  a.py  b  B.PY  y.CpP  z.c ab/x.py
      and initialize a git or Mercurial directory.  Put whatever text you
      like in the files.  I made a and b the same files, except b had one
      extra line.  B.PY was the same as b.  The other files were empty.
 
      {g.pgm} .
        This showed the text of all the non-empty files; the text was
        highlighted in color.  Redirect the output to a file and there should
        be no escape codes in the file.
      {g.pgm} -C 2 .
        Same as previous, but printed with no color.
      {g.pgm} -e .          # Show files that will be searched
        Prints 'a a.py aa b B.PY y.CpP z.c ab/x.py'
      {g.pgm} -x a -e .     # Show files with 'a' in name that will be searched
        Prints 'b B.PY y.CpP z.c ab/x.py'
      {g.pgm} -h -e .       # Same; include hidden file
        Prints '.c.py a a.py aa b B.PY y.CpP z.c ab/x.py'
      {g.pgm} -p -e .       # Show the python files
         Prints 'a.py B.PY ab/x.py'
      {g.pgm} -c -e .       # Show the C/C++/Arduino files
        Prints 'y.CpP z.c'
      {g.pgm} -h -e -V .    # Show all files
        Depends on what files you created.
      {g.pgm} -l xyzzy      # Lists no files, as 'xyzzy' not in any
      {g.pgm} -L xyzzy      # Lists all files, as 'xyzzy' not in any
 
    """,
            n=4,
        )
    )
    exit(0)


def Usage(d, status=1):
    print(
        dedent(f"""
    {g.name} [options] regexp [dir1 [dir2 ...]]
      Recursively searches the indicated directories for files with
      content that match the given regexp.  If no directories are given,
      searches the current directory.  
    Options (+ means that option can appear more than once):
      -?          Show more thoughts on usage
      -C n        n = 0 (default) color if stdout is TTY, 1 = always, 2 = never
      -c          Search C/C++/Arduino source files
      -d regexp + Ignore these matches to the files' directories
      -e          Echo the files that would be searched and exit
      -F          Do not delete leading/trailing whitespace for -f option
      -f file   + The regexps are in a file, one per line (delete whitespace)
      -g regexp + Files to search for.  Removes effect of -p and -c.
      -h          Show hidden files/directories
      -i          Ignore case
      -L          List files that didn't have a match
      -l          List files that had a match
      -n          Show 1-based line number of match
      -p          Search python source files (*.py)
      -q          Exit with status 0 when any match found; otherwise 1
      -t          Interpret regexp (and -f regexps) as plain text
      -V          Include revision control directories in search
      -v          Invert the sense of matching to show non-matching lines
      -x regexp + Ignore these matches to the file names
      """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-C"] = 0  # Don't use color
    d["-c"] = False  # Find C/C++ source files
    d["-D"] = False  # Print debug information
    d["-d"] = []  # Ignore these directory regexps
    d["-e"] = False  # Echo files that would be searched
    d["-F"] = False  # If True, keep whitespace in -f option
    d["-f"] = []  # File(s) containing regexps to use for searching
    d["-g"] = []  # Regexp patterns for files to search
    d["-h"] = False  # Show hidden files/directories
    d["-i"] = False  # Ignore case
    d["-L"] = False  # List files that didn't have a match
    d["-l"] = False  # List files that had a match
    d["-n"] = False  # Show 1-based line number of match
    d["-p"] = False  # Find python source files
    d["-q"] = False  # Exit with status 0 when any match found; otherwise 1
    d["-t"] = False  # Interpret regexp as plain text
    d["-V"] = False  # Search revision control directories
    d["-v"] = False  # Invert match sense to show non-matching lines
    d["-x"] = []  # Ignore these file regexp patterns
    d["--test"] = False  # Run self-tests
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "?C:cDd:eFf:g:hiLlnpqTtVvx:", longopts=["test"]
        )
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "cDeFhiLlnpqTtVv":
            d[o] = not d[o]
        elif o == "-?":
            Manpage()
        elif o == "-C":
            try:
                d[o] = int(a)
                if d[o] not in (0, 1, 2):
                    raise Exception
            except Exception:
                Error("-C argument must be 0, 1, or 2")
        elif o in ("-d", "-f", "-g", "-x"):
            d[o].append(a)
        elif o == "--test":
            d[o] = not d[o]
    d["-d"].extend([r"__pycache__"])
    if not d["-V"]:
        d["-d"].extend([r"\.hg", r"\.git", r"\.bzr", r"RCS"])
    for o in "-d -f -g -x".split():
        d[o] = list(set(d[o]))  # Only keep unique items
    if not args and not d["-e"] and not d["--test"]:
        Usage(d)
    if d["-i"]:
        g.I = re.I
    if d["-D"]:
        g.debug = True
    Debug(f"Command line: '{sys.argv}'")
    return args


def GetRegexp(regexp):
    """regexp is the string that was passed on the command line."""
    regexps = []
    if d["-f"]:
        # Regular expressions are in a set of files
        for file in d["-f"]:
            for line in open(file):
                if line[-1] == "\n":
                    line = line[:-1]
                if not line:
                    continue
                if not d["-F"]:
                    line = line.strip()
                if d["-t"]:
                    regexps.append(line)
                else:
                    if d["-i"]:
                        regexps.append(re.compile(line, re.I))
                    else:
                        regexps.append(re.compile(line))
    else:
        if d["-t"]:
            regexps = [regexp]
        elif d["-i"]:
            regexps = [re.compile(regexp, re.I)]
        else:
            regexps = [re.compile(regexp)]
    return regexps


def IsHidden(head, tail):
    """If the components of head or tail are hidden, return True.  Note we
    assume directory paths are separated by '/' characters.  head is a
    directory entry and tail is a file name.
    """
    if tail.startswith("."):
        return True
    for dir in head.split("/"):
        if dir.startswith(".") and dir != "." and dir != "..":
            return True
    return False


def FilterRegexps(files, d):
    """Use the command line options to filter the files and directories to
    get the list of files to process.
    """
    dregexps = [re.compile(i) for i in d["-d"]]
    xregexps = [re.compile(i) for i in d["-x"]]
    # Filter out the files and directories we don't want
    keep = []
    for file in files:
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
        keep.append(file)
    files = keep
    # In the remaining set of files, keep any specified by d["-g"]
    if d["-g"]:
        keep = []
        gregexps = [re.compile(i, re.I if d["-i"] else 0) for i in d["-g"]]
        for file in files:
            head, tail = str(file.parent), file.name
            for r in gregexps:  # File types to include
                if r.search(tail):
                    keep.append(file)
                    break
        files = keep
    return files


def PrintFilesToBeSearched():
    "Print the files to stdout and exit"
    for i in d["files"]:
        print(i)
    exit(0)


def LineMatch(line, regexps):
    """Return a list of the match objects if there are one or more matches
    with the regexps.  Return an empty list for no matches.
    """
    mo_list = []
    for r in regexps:
        mo = r.search(line)
        if mo:
            mo_list.append(mo)
    return mo_list


def StripCurrDir(s):
    assert ii(s, P)
    t = str(s)
    t = t[2:] if t.startswith("./") else t
    return P(t)


def ListFiles():
    """This lists the files that have (d["-l"]) or don't have (d["-L"]) the
    regexps to search for.
    """
    if d["-l"]:
        # List files that match one or more the regexps
        matches = []  # Store (file, match_count)
        for file in d["files"]:
            try:
                if not file.stat().st_size:
                    continue
                for line in open(file):
                    mo_list = LineMatch(line, d["cmd_regexps"])
                    if mo_list:
                        matches.append((file, len(mo_list)))
                        break
            except Exception as e:
                Debug(f"Exception:  {repr(e)}")
                print(f"Can't process file '{file}':", file=sys.stderr)
                continue
        if matches:
            for file, count in matches:
                print(StripCurrDir(file))
    elif d["-L"]:
        # List files that don't match any of the regexps
        for file in d["files"]:
            matched = False
            try:
                if not file.stat().st_size:
                    # Empty file will always not match
                    matched = True
                else:
                    for line in open(file):
                        mo_list = LineMatch(line, d["cmd_regexps"])
                        if mo_list:
                            matched = True
                if not matched:
                    print(StripCurrDir(file))
            except Exception as e:
                Debug(f"Exception:  {repr(e)}")
                print(f"Can't process file '{file}':", file=sys.stderr)
                continue
    else:
        raise Exception("Programming error")


def RmLinefeed(line):
    while line and line[-1] == "\n":
        line = line[:-1]
    return line


def GetAllFiles():
    """Return a deque of all the files to search.  The -d option will contain
    a list of regexps for directories to ignore, so every file has to be run
    by these regexps.
    """
    files = deque()
    for dir in d["dirs"]:
        p = P(dir)
        if not p.is_dir():
            print(f"'{dir}' is not a directory", file=sys.stderr)
            continue
        for file in p.rglob("*"):
            if file.is_file():
                files.append(file)
    # Remove any './' from the front of the files
    files = deque([StripCurrDir(i) for i in files])
    return files


def CompileRegularExpressions():
    "Compile regular expressions for options"
    d["-d"] = [re.compile(i, g.I) for i in d["-d"]]
    d["-g"] = [re.compile(i, g.I) for i in d["-g"]]
    d["-x"] = [re.compile(i, g.I) for i in d["-x"]]
    if d["-f"]:
        r = open(d["-f"]).read().split("\n")

        def f(x):
            return x if d["-F"] else x.strip()

        d["cmd_regexps"] = [re.compile(f(i), g.I) for i in r]
    # Python files
    d["python_regexps"] = [re.compile(r"\.py$", re.I)]
    # C/C++/Arduino files
    d["C/C++_regexps"] = [
        re.compile(r"\.c$", re.I),
        re.compile(r"\.cpp$", re.I),
        re.compile(r"\.h$", re.I),
        re.compile(r"\.hpp$", re.I),
        re.compile(r"\.ino$", re.I),
    ]


def Remove(files, regexps, dir=False):
    """For the deque files, remove those elements that are matched by any
    regex in regexps.  Return a deque of the remaining files.  If dir is
    True, search on the directory component; otherwise, just search on the
    file name.
    """
    assert ii(files, deque)
    out = deque()
    while files:
        file = files.popleft()
        assert ii(file, P)
        item = str(file.parent) if dir else file.name
        keep_this_file = True
        for r in regexps:
            mo = r.search(item)
            if mo:
                keep_this_file = False
                break
        if keep_this_file:
            out.append(file)
    return out


def Keep(files, regexps):
    """For the deque files, keep those elements that are matched by any
    regex in regexps.  Return a deque of the matched files.  Unlike Remove(),
    only the name part of the path is compared to the regexp.
    """
    assert ii(files, deque)
    out = deque()
    while files:
        file = files.popleft()
        assert ii(file, P)
        item = file.name
        keep_this_file = False
        for r in regexps:
            mo = r.search(item)
            if mo:
                keep_this_file = True
                break
        if keep_this_file:
            out.append(file)
    return out


def FilterFiles():
    """Remove files from d["files"] that aren't germane to the search."""

    def Dump(msg):
        if g.debug:
            Debug(msg)
            for line in Columnize([str(i) for i in d["files"]], indent=" " * 2):
                Debug(f"  {str(line)}")

    assert ii(d["files"], deque)
    Dump("Original list of files:")
    # -g files to keep
    if d["-g"]:
        d["files"] = Keep(d["files"], d["-g"])
        Dump("Files after applying -g")
    else:
        if d["-p"]:  # Python files
            d["files"] = Keep(d["files"], d["python_regexps"])
            Dump("Files after applying -p")
        elif d["-c"]:  # C/C++/Arduino files
            d["files"] = Keep(d["files"], d["C/C++_regexps"])
            Dump("Files after applying -c")
    # -d remove the directory matches
    if d["-d"]:
        d["files"] = Remove(d["files"], d["-d"], dir=True)
        Debug("Applied -d")
    # -x remove the file matches
    if d["-x"]:
        d["files"] = Remove(d["files"], d["-x"], dir=False)
        Debug("Applied -x")
    # -h hidden files
    if not d["-h"]:
        r, out, files = re.compile(r"^\..*$"), deque(), d["files"]
        while files:
            file = files.popleft()
            keep_this_file = True
            for item in file.parts:
                if r.match(item):
                    keep_this_file = False
                    break
            if keep_this_file:
                out.append(file)
        d["files"] = out
    if g.debug:
        Debug("List of files after filtering:")
        for line in Columnize([str(i) for i in d["files"]], indent=" " * 2):
            Debug(f"  {str(line)}")


def Search():
    """For the given regexps, find matching text lines in the indicated
    files.
    """
    # The results list will contain (file, lineno, line, match_object) for
    # regex searches or (file, lineno, line, matched_string) for -t plain
    # text searches.
    results = []
    for file in d["files"]:
        if not file.stat().st_size:
            continue
        try:
            handle = open(file)
            for linenum, line in enumerate(handle):
                if not line:
                    continue
                line = RmLinefeed(line)
                if not line:
                    continue
                for r in d["cmd_regexps"]:
                    if d["-t"]:
                        if d["-i"]:
                            loc = line.lower().find(r.lower())
                        else:
                            loc = line.find(r)
                        if loc == -1 and d["-v"]:
                            results.append((file, linenum, line, r))
                        elif loc != -1 and not d["-v"]:
                            results.append((file, linenum, line, r))
                    else:
                        mo = r.search(line)
                        if mo and not d["-v"]:
                            results.append((file, linenum, line, mo))
                        elif not mo and d["-v"]:
                            results.append((file, linenum, line, mo))
        except UnicodeDecodeError as e:
            print(f"{file!r}:  Unicode error", file=sys.stderr)
            continue
        except Exception as e:
            Debug(f"Exception:  {repr(e)}")
            print(f"Can't process file '{file}[{linenum + 1}]'", file=sys.stderr)
            continue
    include_filename = len(d["files"]) > 1 or d["-g"]
    # Print results
    if results:
        if d["-q"]:
            exit(0)
        for file, linenum, line, mo in results:
            linenum += 1
            if include_filename:  # Multiple files
                if d["-n"]:
                    if d["-v"]:
                        print(f"{file}:{linenum}:{line}")
                    else:
                        print(f"{g.fn}{file}{g.co}:{g.ln}{linenum}{g.co}:{g.n}", end="")
                        g.PrintMatch(line, mo.re)
                else:
                    if d["-v"]:
                        print(f"{file}:{line}")
                    else:
                        print(f"{g.fn}{file}{g.co}:{g.n}", end="")
                        g.PrintMatch(line, mo if d["-t"] else mo.re)
            else:  # Only one file
                if d["-n"]:
                    if d["-v"]:
                        print(f"{linenum}:{line}")
                    else:
                        print(f"{g.ln}{linenum}{g.co}:{g.n}", end="")
                        g.PrintMatch(line, mo if d["-t"] else mo.re)
                else:
                    if d["-v"]:
                        print(f"{line}")
                    else:
                        g.PrintMatch(line, mo if d["-t"] else mo.re)


if __name__ == "__main__":
    d = {}  # Options dictionary
    EnableColor()
    args = ParseCommandLine(d)
    EnableColor(d["-C"])
    CompileRegularExpressions()
    if d["-f"] or d["-F"] or d["-e"]:
        d["dirs"] = args if args else ["."]
    else:
        # Put the first command line argument in d["cmd_regexps"].
        if d["-t"]:
            d["cmd_regexps"] = [args[0]]
        else:
            d["cmd_regexps"] = [re.compile(args[0], g.I)]
        d["dirs"] = args[1:] if args[1:] else ["."]
    d["files"] = GetAllFiles()
    FilterFiles()
    if d["-e"]:
        PrintFilesToBeSearched()
    if d["-l"] or d["-L"]:
        ListFiles()
    else:
        Search()
        if d["-q"]:
            exit(1)  # Success causes Search() to exit with status 0

'''
Front end to the astyle command for indenting C/C++ code.

    This tool is intended to help you indent a set of C/C++ files with 
    a particular indenting style.  There are two use cases:

        * Indent a set of source files by including them on the command
          line or in a file.
        * Indent a set of files defined in a project file.

    The first usage is documented by giving the program no arguments.

    The second usage is gotten by including a single file on the command
    line that has the extension '.proj' (you only need to include the name
    before the .proj extension.  This file includes a single line of the
    form 

        style = xx

    defining the indenting style.  The remaining lines are file names of
    the files included in the project, one line per file.  A leading '#'
    can be used to comment out lines.

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Wrapper program for the astyle tool to indent C/C++ code.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import subprocess
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from color import (C, fg, black, blue,  green,  cyan,  red,  magenta,
        brown,  white, gray,  lblue, lgreen, lcyan, lred, lmagenta, yellow,
        lwhite)
    from cmddecode import CommandDecode
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class g: pass
    g.astyle = "c:/cygwin/home/Don/bin/astyle.exe"
    g.styles = '''
        1tbs allman attach banner break bsd gnu google horstmann java k&r
        k/r knf kr linux lisp mozilla otbs pico ratliff run-in stroustrup
        vtk whitesmith
        '''.split()
    # The following styles are used for the -h option
    g.styles_list = '''
        banner bsd gnu google java kr linux mozilla otbs pico python
        run-in stroustrup vtk whitesmith
    '''.split()
    g.style_aliases = {
        # Use to show synonyms in -h option
        "bsd":     "allman break",
        "java":    "attach",
        "kr":      "k&r k/r",
        "banner":  "ratliff",
        "linux":   "knf",
        "run-in":  "horstmann",
        "otbs":    "1tbs",
        "python":  "lisp",
    }
    g.extension = ".proj"
    g.backup_ext = ".astyle.bak"
    g.default_style = "java"
    g.cmd = CommandDecode(set(g.styles))
    g.sample = dedent('''
    int Function(bool use_bar) {
     if (use_bar) {
      bar();
      return 1;
     } else
      return 0;
    }
    ''')
if 1:   # Utility
    def Dbg(*msg):
        if d["-d"]:
            for i in msg:
                print(f"{g.d}" + i + f"{g.n}")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [style] [file1 [file2 ...]]
                {sys.argv[0]} [options] project_file
          Indent the indicated source code files with astyle (the files
          must be C/C++/ObjC).  The first argument can optionally be one
          of the following indentation styles:
              {' '.join(g.styles_list[:11])}
              {' '.join(g.styles_list[11:])}
          You can use abbreviations for the styles as long they are unique.
          The default style is {g.default_style}.

          The second usage is to give a project file with the extension
          .proj on the command line.  This is a file with the project
          files in it, one file per line.  Include a 'style = xx' in the
          project file to change the indenting style.
        Options:
            -c      Don't use color in output
            -C      Clean out *.bak files in current directory only (unless
                    you use a project file)
            -d      Show debugging output
            -f f    Use the file f as a list of files to format in addition
                    to any given on command line.  One file per line.
            -h      Show samples of the styles to stdout (and aliases)
            -o o    String o holds extra astyle options (put in quotes)
            -t      Show testing suggestions
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Use color
        d["-C"] = False     # Clean out *.bak files
        d["-d"] = False     # Show debugging output
        d["-f"] = None      # File containing files to format
        d["-h"] = False     # Show formatting samples
        d["-o"] = ""        # Extra options for astyle
        d["-t"] = False     # Show testing suggestions
        try:
            opts, files = getopt.getopt(sys.argv[1:], "cCdf:ho:t")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cCdht"):
                d[o] = not d[o]
            elif o in ("-f",):
                d[o] = p = P(a)
                if not p.is_file():
                    Error(f"'{a}' cannot be read")
            elif o in ("-o",):
                d[o] = a
        if d["-h"]:
            ShowExamples()
        if len(sys.argv) < 2 and not d["-f"]:
            Usage()
        if d["-f"]:     # Add -f option files to list
            for line in open(d["-f"]).readlines():
                files.append(line.strip())
        if d["-t"]:
            TestingSuggestions()
        if d["-c"]:
            SetupColor()
        return files
if 1:   # Core functionality
    def SetupColor():
        '''Normally, I'd use sys.stdout.istty() to determine whether to use
        color or not.  Howver, I often want the color output of this
        program put into a file, so the color is on by default and turned
        off by the -c option.
        '''
        global g
        if d["-c"]:
            g.err = C.lred
            g.d = C.cyn
            g.b = fg(lwhite, blue, s=1) # Brace color
            g.m = fg(yellow, s=1)  # Message color showing style
            g.n = C.norm
        else:
            g.err = ""
            g.d = ""
            g.b = ""
            g.m = ""
            g.n = ""
    def TestingSuggestions():
        print(dedent('''
        Here's a suggested way to test this script.  Go to an empty
        directory and create some source code files.  I suggest you use a
        script for this so that they can be created fresh again after
        formatting.  Call the command to execute the script mk.  Remember
        to include a suitable project file with extension '.proj'.
        Include a subdirectory with some source files too.
 
        I remove the leading whitespace on lines so that I can tell the
        difference between a file and its newly indented form.  First 
        indent it to your preferred style, then remove leading whitespace.
        This makes it easy to see the effects of indenting when using a
        tool like WinMerge.  First set Winmerge to ignore all whitespace
        and you should see no lines marked as changed.  Then set whitespace
        to significant and you should see the lines with different
        indentations marked.
 
        Test case:  command line invocation on files
            * Run mk
            * run 'indent *.cpp *.h'
                * You should see 2 files indented with no failures.
            * Verify the indenting 
            * Verify there are the backup files equivalent to the original
              files exclusing of indentation
            * run 'indent -d *.cpp *.h'
            * You should get the same results but see two colored debug
              print lines telling you the files that have been indented.
 
        Test case:  verify -C option works
            * Run 'indent -C'
            * Verify all backup files are gone in current directory but not
              in the subdirectory.
 
        Test case:  verify -f option works
            * Run mk
            * Create a file f with the names of the source files in it.  An
              easy way to do this is 'ls >f' and edit out the non-source
              files.
            * Run 'indent -f f'
            * Verify the indenting worked the same as in the first test
              case
            * Run 'indent -C' to remove backup files.  Note:  you may find
              it convenient to remove them in the mk script.
 
        Test case:  verify -h option works
            * Run 'indent -h' and verify you get a listing of the different
              indentation styles.
 
        Test case:  verify project file works
            * Run 'indent xx' where xx is the filename less the suffix of
              your project file
            * Verify the correct number of files were formatted and that
              they have the new style given in the project file
 
        Test case:  verify -C works with project file
        Test case:  verify -o option passes extra options to astyle
        '''))
        exit(0)
    def Example(style):
        'Print the sample code to stdout with the indicated style'
        file = "indent.data"
        open(file, "w").write(g.sample)
        cmd = [g.astyle, f"--style={style}", "indent.data"]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode:
            raise Exception(f"{g.astyle} returned > 0")
        s = open(file).read()
        Example.counts[style] = len(s.split("\n"))
        # Put in escape codes for color
        s = s.replace("{", f"{g.b}{{{g.n}")
        s = s.replace("}", f"{g.b}}}{g.n}")
        synonyms = ""
        if style in g.style_aliases:
            synonyms = g.style_aliases[style]
        print(f"style = {g.m}{style} {synonyms}{g.n}")
        print(s)
        print("-"*25)
    def ShowExamples():
        SetupColor()
        Example.counts = {}
        print(f"Styles and their aliases in {g.m}this{g.n} color\n")
        for i in g.styles_list:
            Example(i)
        # Show sorted by number of lines
        s = [(j, i) for i, j in Example.counts.items()]
        print("Number of lines in sample by style:")
        for n, style in reversed(sorted(s)):
            print(f"    {style:15s} {n:2d}")
        exit(0)
    def CheckExtensions(files):
        'Check that extensions are allowed and that files exist'
        allowed = set("c cpp h hpp m mm".split())
        for file in files:
            p = P(file)
            ext = p.suffix
            if not ext or ext[0] != ".":
                Error(f"'{file}' has a missing extension")
            if ext[1:] not in allowed:
                Error(f"'{file}' has an illegal extension")
    def IndentFile(file, style):
        Dbg(f"Indenting '{file}'")
        cmd = [g.astyle, f"--style={style}"]
        if d["-o"]:
            e = d["-o"].split()
            cmd.extend(e)
        cmd.append(file)
        Dbg(f"  Command:  {' '.join(cmd)}")
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode:
            print(f"{g.err}'{g.astyle}' failed on file '{file}'{g.n}")
            print(f"  stdout:  {r.stdout.decode()}")
            print(f"  stderr:  {r.stderr.decode()}")
            global failed
            failed += 1
        else:
            global count
            count += 1
    def Stream():
        'Read in stdin, process it through astyle, and send it to stdout'
        xx()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    SetupColor()
    style = g.default_style
    if d["-s"]:
        Stream()
    have_project = False
    if len(files) > 1:
        # See if first one is a style
        lst = g.cmd(files[0])
        if len(lst) == 1:
            style = lst[0]
            files.pop(0)
    elif len(files) == 1:
        p = P(files[0])
        if p.suffix == g.extension:
            have_project = True
        else:
            p = P(files[0] + g.extension)
            if p.exists():
                have_project = True
        if have_project:   # We have a project file
            if d["-f"]:
                Error("-f option not supported with project files")
            project_name = files.pop()
            for line in open(p).readlines():
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                if s.startswith("style ="):
                    # Get the style
                    st = s[7:].strip()
                    sty = g.cmd(st)
                    if len(sty) == 1:
                        style = sty[0]
                    else:
                        Error(f"Style '{st}' not recognized")
                    Dbg(f"Got style '{st}'")
                    continue
                file = line.strip()
                Dbg(f"Got file {g.m}'{file}'{g.d} from project file")
                files.append(file)
    if d["-C"]:
        if have_project:
            # Can delete all the project backup files
            for file in files:
                p = P(file + g.backup_ext)
                if p.exists():
                    p.unlink()
        else:
            # This only works in current directory
            os.system("rm *.bak")
            pass
        exit(0)
    print(f"Using style {g.m}{style}{g.n}")
    CheckExtensions(files)
    count, failed = 0, 0
    for file in files:
        IndentFile(file, style)
    print(f"{count} files indented, {failed} files failed")

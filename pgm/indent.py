r'''
TODO

    * Add -n for dry run (--dry-run for astyle option)
    * Add -v option so that astyle's output is verbose.  Capture output to
      stdout; change \ to / and remove current directory string.  Show the
      files that were changed in green.
    * Add -r that will restore either the *.orig files given
      on the command line or all of the .orig files in current directory.
        * This command writes a suitable shell script to stdout
    * Add usage of a filter with an optional style name so this script can
      be used from within vi.
        * 'indent'
        * 'indent style'
    * The default style is to not give a style on the command line; this
      then uses the ~/.astylerc settings by default.
    * Do not list the built-in styles to astyle, as the user can get them
      by 'astyle -h' or 'indent -H'.
    * Add '-a dir' option that applies all styles to a single source file and
      puts them into a directory named 'dir'.  Each file a.c will be
      renamed to a.style.c to retain the extension.
    * astyle screws up the permissions; make sure they're the same as the
      original file.
    * Important:  --remove-comment-prefix removes the annoying '*'
      characters that many people use for comments, put in by their editor.
    * It is recommended that you read the astyle.html page in detail, as
      there are many settings to let you get code looking the way you
      prefer.
    * Define my custom set of files by using indent.a.style files in
      /plib/pgm.  Some styles:
        * min       Vertically compressed with minimal braces
        * prod      Production code style
        * readable  Opposite of min
        * folding   Based on whitesmith to get minimum folding height
        * Others as needed for special projects

----------------------------------------------------------------------
Front end to the astyle command for indenting C/C++ code.
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
    # Wrapper program for the astyle tool to indent C/C++ code
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import subprocess
    import sys
if 1:   # Custom imports
    from wrap import wrap, dedent
    from color import (C, fg, black, blue, green, cyan, red, magenta,
        brown, white, gray, lblue, lgreen, lcyan, lred, lmagenta, yellow,
        lwhite)
    from cmddecode import CommandDecode
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class g:
        pass
    g.astyle = "c:/cygwin/home/Don/bin/astyle.exe"
    g.styles = '''
        1tbs allman attach banner break bsd gnu google horstmann java k&r
        k/r knf kr linux lisp mozilla otbs pico ratliff run-in stroustrup
        vtk whitesmith
        '''.split()
    g.allowed = set("c cpp h hpp m mm".split())    # Allowed extensions
    # The following styles are used for the -h option
    g.styles_list = '''
        banner bsd gnu google java kr linux mozilla otbs pico python
        run-in stroustrup vtk whitesmith
    '''.split()
    g.style_aliases = {
        # Use to show synonyms in -h option
        "bsd": "allman break",
        "java": "attach",
        "kr": "k&r k/r",
        "banner": "ratliff",
        "linux": "knf",
        "run-in": "horstmann",
        "otbs": "1tbs",
        "python": "lisp",
    }
    g.project_extension = ".proj"
    g.backup_ext = ".astyle.bak"
    g.default_style = None
    g.cmd = CommandDecode(set(g.styles))
    g.sample = dedent('''
    int Function(bool use_other) {
        if (use_other) {
            Other();
            return 1;
        } else
            return 0;
    }
    ''')
if 1:   # Error handling
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
if 1:   # Classes
    class Styles:
        '''Container for styles.  The methods/attributes are containers of
        the various styles that can be used (.x means it's an attribute and
        a tuple):
            .core       These are astyle styles
            aliases     Gives astyle style synonyms dictionary
        '''
        def __init__(self):
            pass
    class FileList:
        '''This is a container for the files given on the command line.
        Globbing symbols are allowed.  This object lets all of the files
        be passed at once to the astyle command for better performance.
        It also allows the permissions to be restored after astyle runs, as
        astyle screws up permissions on Windows.
        '''
        def __init__(self, files):
            self.files = files
            # Container for filenames and starting permissions
            self.filelist = {}
            self.resolve()
        def resolve(self):
            '''Expand self.files into a dict to eliminate globs and capture
            the files' permissions
            '''
            if "**" in self.get_files():
                Error("Cannot use '**' in glob expressions")
            for file in self.files:
                if "*" in file or "?" in file or "[" in file or "]" in file:
                    s = P(".").glob(file)
                    for i in s:
                        self.filelist[i] = os.stat(i).st_mode
                else:
                    p = P(file)
                    self.filelist[file] = os.stat(p).st_mode
        def get(self):
            'Return string for astyle command line'
            return ' '.join(self.files)

if 1:   # Utility
    def Dbg(*msg):
        if d["-d"]:
            for i in msg:
                print(f"{g.d}" + i + f"{g.n}")
    def Usage(status=1):
        e = sys.argv[0]
        print(dedent(f'''
        Usage:  {e} [options] [style] [file1 [file2 ...]]
                {e} [options] project_file
                {e} [options] [style]
          Indent the indicated source code files with astyle (the files
          must be C/C++/ObjC).  The first argument can optionally be one
          of the following indentation styles:
              {' '.join(g.styles_list[:11])}
              {' '.join(g.styles_list[11:])}
          You can use abbreviations for the styles as long they are unique.
          There is no default style except that defined in e.g. your
          .astylerc file.
 
          The second usage is to give a project file with the extension
          .proj on the command line.  This is a file with the project
          files in it, one file per line.  Include a 'style = Xx' in the
          project file to change the indenting style.
 
          The third usage tells the script to act as a filter:  take its
          input from stdin and send the results to stdout.
        Options:
            -c      Don't use color in output
            -e      Allow any file extensions
            -C      Clean out *.bak files in current directory only (unless
                    you use a project file)
            -d      Show debugging output
            -f f    Use the file f as a list of files to format in addition
                    to any given on command line.  One file per line.
            -H      Show astyle 3.1 options
            -h      Show samples of the styles to stdout.  If there is a
                    single source file on the command line, it is used as
                    the example source text.
            -o o    String o holds extra astyle options (put in quotes)
            -t      Show testing suggestions
            --dp    Show my thoughts on indentation
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Use color
        d["-C"] = False     # Clean out *.bak files
        d["-d"] = False     # Show debugging output
        d["-e"] = False     # Allow any file extensions
        d["-f"] = None      # File containing files to format
        d["-H"] = False     # Show astyle 3.1 options
        d["-h"] = False     # Show formatting samples
        d["-o"] = ""        # Extra options for astyle
        d["-t"] = False     # Show testing suggestions
        try:
            opts, files = getopt.getopt(sys.argv[1:], "cCdef:Hho:t", 
                "dp".split())
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cCdeHht"):
                d[o] = not d[o]
            elif o in ("-f",):
                d[o] = p = P(a)
                if not p.is_file():
                    Error(f"'{a}' cannot be read")
            elif o in ("-o",):
                d[o] = a
            elif o == "--dp":
                Comments()
        if d["-h"]:
            if files and len(files) == 1:
                file = files[0]
                CheckExtensions([file])
                ShowExamples(file)
            else:
                ShowExamples(None)
            exit(0)
        if d["-H"]:
            ShowAstyleOptions()
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
    def Comments():
        print(wrap(dedent(f'''
 
        If you work on a software project with a number of people, 
        management people may dictate an
        indentation style.  Then this style is what you use.  
 
        However, most of us have a favorite style with which we like to
        edit code.  If you look at the many options and styles available in
        astyle, it shows how much variety you'll see in real code in the
        wild.  
 
        One of the things this script is intended to do is to let you edit
        code in your preferred style, then change it to a mandated style
        before checking in.  This is most easily done with a project file.
 
        I use multiple styles.  For production code, I'll usually use
        something like the java or bsd style.  When using an editor,
        however, vertical space is the most precious resource so I use a
        style that maximizes the number of lines I'll see on the screen
        (examples are pico and python).  If you're editting C/C++ code, the
        python style will look pretty strange, but if you're also a python
        programmer, it is compact and will allow for easy reading.
 
        To deal with this lack of vertical space, I use the following
        strategies: 
 
            * I use a second monitor that is rotated by a right angle to
              let me see my editor window in portrait mode.
 
            * I'll use an astyle style (like python) that minimizes
              vertical space.
 
            * I delete all blank lines in the file.
 
        Deleting all blank lines in a file is likely to be viewed to be too
        severe by many people, especially those who were born in the last
        30 to 40 years.  People of my generation (born in the 1940's),
        especially technical people, often learned to deal with lots of
        information in densely printed textbooks.  You never see such
        things anymore, as witnessed by the low information density on web
        pages.  Regardless, it doesn't hurt my feelings if someone doesn't
        agree with my tastes -- and a tool like astyle makes it easier to
        view things the way you want them to be.
 
        Here's an interesting observation.  If you look at the line counts
        at the end of the demo report when you use the -h option, you'll
        see pico and python have the least number of lines and whitesmith
        has the most number of lines.  You'd think that the whitesmith
        style would be useless from a minimizing the number of lines in the
        display standpoint.  However, with my folding editor, it's perfect
        when folding by indentation and results in the most compact display
        of all because there are no curly braces in column 1.  Viewing the
        folded forms of a sample C++ file with 134 lines showed that the
        banner style also did a good job at this.  With the whitesmith or
        banner styles, the folded form of the file was 20 lines, making it
        easy to browse to the function of interest.
 
        Thus, my advice is that you experiment to see what works best for
        you under a variety of conditions.
 
        ''')))
        exit(0)
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
            g.b = fg(lwhite, blue, s=1)     # Brace color
            g.m = fg(yellow, s=1)           # Message color showing style
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
            - Run mk
            - run 'indent *.cpp *.h'
                - You should see 2 files indented with no failures.
            - Verify the indenting 
            - Verify there are the backup files equivalent to the original
              files exclusive of indentation
            - run 'indent -d *.cpp *.h'
            - You should get the same results but see two colored debug
              print lines telling you the files that have been indented.
 
        Test case:  verify -C option works
            - Run 'indent -C'
            - Verify all backup files are gone in current directory but not
              in the subdirectory.
 
        Test case:  verify -f option works
            - Run mk
            - Create a file f with the names of the source files in it.  An
              easy way to do this is 'ls >f' and edit out the non-source
              files.
            - Run 'indent -f f'
            - Verify the indenting worked the same as in the first test
              case
            - Run 'indent -C' to remove backup files.  Note:  you may find
              it convenient to remove them in the mk script.
 
        Test case:  verify -h option works
            - Run 'indent -h' and verify you get a listing of the different
              indentation styles.
 
        Test case:  verify project file works
            - Run 'indent XX' where XX is the filename less the suffix of
              your project file
            - Verify the correct number of files were formatted and that
              they have the new style given in the project file
 
        Test case:  verify -C works with project file
        Test case:  verify -o option passes extra options to astyle
        '''))
        exit(0)
    def Example(style, file, maxwidth):
        'Print the sample code to stdout with the indicated style'
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
        print("-"*maxwidth)
    def ShowExamples(sourcefile):
        '''If sourcefile is not None, use it as the sample code to format.
        '''
        SetupColor()
        # Fill the file to indent
        file = P("indent.data")
        if sourcefile is not None:
            input_file = P(sourcefile)
            try:
                s = open(input_file).read()
                open(file, "w").write(s)
            except Exception:
                Error(f"Couldn't write file data to '{file}'")
        else:
            open(file, "w").write(g.sample)
        maxwidth = max([len(line) for line in open(file).readlines()])
        # Generate the examples
        Example.counts = {}
        print(f"Styles and their aliases in {g.m}this{g.n} color\n")
        for i in g.styles_list:
            Example(i, file, maxwidth)
        # Show number of lines in each style
        s = [(j, i) for i, j in Example.counts.items()]
        print("Number of lines in sample by style:")
        for n, style in reversed(sorted(s)):
            print(f"    {style:15s} {n:2d}")
        file.unlink()
        exit(0)
    def CheckExtensions(files):
        'Check that files have allowed extensions'
        for file in files:
            ext = P(file).suffix
            if not ext or ext[0] != ".":
                Error(f"'{file}' has a missing extension")
            if ext[1:].lower() not in g.allowed:
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
    def ShowAstyleOptions():
        print(dedent(f'''
        Disable Formatting
            *INDENT-OFF* and *INDENT-ON*, *NOPAD*
        Brace Style Options
            --style=allman  OR  --style=bsd  OR  --style=break  OR  -A1
            --style=java  OR  --style=attach  OR  -A2
            --style=kr  OR  --style=k&r  OR  --style=k/r  OR  -A3
            --style=stroustrup  OR  -A4
            --style=whitesmith  OR  -A5
            --style=vtk  OR  -A15
            --style=ratliff  OR  --style=banner  OR  -A6
            --style=gnu  OR  -A7
            --style=linux  OR  --style=knf  OR  -A8
            --style=horstmann  OR  --style=run-in  OR  -A9
            --style=1tbs  OR  --style=otbs  OR  -A10
            --style=google  OR  -A14
            --style=mozilla  OR  -A16
            --style=pico  OR  -A11
            --style=lisp  OR  -A12
        Tab Options
            --indent=spaces=#  OR  -s#
            --indent=tab  OR  --indent=tab=#  OR  -t  OR  -t#
            --indent=force-tab=#  OR  -T#
            --indent=force-tab-x=#  OR  -xT#
        Brace Modify Options
            --attach-namespaces  OR  -xn
            --attach-classes  OR  -xc
            --attach-inlines  OR  -xl
            --attach-extern-c  OR  -xk
            --attach-closing-while  OR  -xV
        Indentation Options
            --indent-classes  OR  -C
            --indent-modifiers  OR  -xG
            --indent-switches  OR  -S
            --indent-cases  OR  -K
            --indent-namespaces  OR  -N
            --indent-after-parens  OR  -xU
            --indent-continuation=#  OR  -xt#
            --indent-labels  OR  -L
            --indent-preproc-block  OR  -xW
            --indent-preproc-cond  OR  -xw
            --indent-preproc-define  OR  -w
            --indent-col1-comments  OR  -Y
            --min-conditional-indent=#  OR  -m#
            --max-continuation-indent=#  OR  -M#
        Padding Options
            --break-blocks  OR  -f
            --break-blocks=all  OR  -F
            --pad-oper  OR  -p
            --pad-comma  OR  -xg
            --pad-paren  OR  -P
            --pad-paren-out  OR  -d
            --pad-first-paren-out  OR  -xd
            --pad-paren-in  OR  -D
            --pad-header  OR  -H
            --unpad-paren  OR  -U
            --delete-empty-lines  OR  -xd
            --fill-empty-lines  OR  -E
            --align-pointer=type    OR  -k1
            --align-pointer=middle  OR  -k2
            --align-pointer=name    OR  -k3
            --align-reference=none    OR  -W0
            --align-reference=type    OR  -W1
            --align-reference=middle  OR  -W2
            --align-reference=name    OR  -W3
        Formatting Options
            --break-closing-braces  OR  -y
            --break-elseifs  OR  -e
            --break-one-line-headers  OR  -xb
            --add-braces  OR  -j
            --add-one-line-braces  OR  -J
            --remove-braces  OR  -xj
            --break-return-type       OR  -xB
            --break-return-type-decl  OR  -xD
            --attach-return-type       OR  -xf
            --attach-return-type-decl  OR  -xh
            --keep-one-line-blocks  OR  -O
            --keep-one-line-statements  OR  -o
            --convert-tabs  OR  -c
            --close-templates  OR  -xy
            --remove-comment-prefix  OR  -xp
            --max-code-length=#    OR  -xC#
            --break-after-logical  OR  -xL
            --mode=c
            --mode=java
            --mode=cs
        Objective-C Options
            --pad-method-prefix  OR  -xQ
            --unpad-method-prefix  OR  -xR
            --pad-return-type  OR  -xq
            --unpad-return-type  OR  -xr
            --pad-param-type  OR  -xS
            --unpad-param-type  OR  -xs
            --align-method-colon  OR  -xM
            --pad-method-colon=none    OR  -xP
            --pad-method-colon=all     OR  -xP1
            --pad-method-colon=after   OR  -xP2
            --pad-method-colon=before  OR  -xP3
        Other Options
            --suffix=####
            --suffix=none  OR  -n
            --recursive  OR  -r  OR  -R
            --dry-run
            --exclude=####
            --ignore-exclude-errors  OR  -i
            --ignore-exclude-errors-x  OR  -xi
            --errors-to-stdout  OR  -X
            --preserve-date  OR  -Z
            --verbose  OR  -v
            --formatted  OR  -Q
            --quiet  OR  -q
            --lineend=windows  OR  -z1
            --lineend=linux    OR  -z2
            --lineend=macold   OR  -z3
        Command Line Only
            --options=####, --options=none      Global options file
            --project=####, --project=none      Project file (file only, no path)
            --ascii  OR  -I
            --version  OR  -V
            --help  OR  -h  OR  -?
            --html, OR --html=####, OR  -!
            --stdin=####    Replacement for redirection
            --stdout=####   Replacement for redirection
        '''))
        exit(0)
    def GetStyle(s):
        lst = g.cmd(files[0])
        if len(lst) == 1:
            return lst[0]
        elif len(lst) > 1:
            Error(f"Ambiguous style:  {' '.joint(lst)}")
        return lst[0]

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    SetupColor()
    style = g.default_style
    have_project = False
    if len(files) > 1:
        # See if first one is a style
        s = GetStyle(files[0])
        if s is not None:
            style = s
            files.pop(0)
    elif len(files) == 1:
        p = P(files[0])
        if p.suffix == g.project_extension:
            have_project = True
        else:
            p = P(files[0] + g.project_extension)
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
    if not d["-e"]:
        CheckExtensions(files)
    print(f"Using style {g.m}{style}{g.n}")
    count, failed = 0, 0
    for file in files:
        IndentFile(file, style)
    print(f"{count} files indented, {failed} files failed")

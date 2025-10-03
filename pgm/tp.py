_pgminfo = '''
<oo 
    Tool for working with text files like markdown and LaTeX.  Commands can be put on
    lines that control the output.  The commands are

    .#              Comment line, not sent to stdout
    .on             Output is turned on
    .off            Output is turned off
    .toggle         Output state is toggled
    .include file   Include the text in a file
    .sinclude file  Include the text in a file; no error if file not found

    Macro expansion:
        🟦date    Current date like '13 Jan 2025'
        🟦time    Current time like '09:26:16 am'
        🟦dttm    Current date/time like '01 Oct 2025 09:26:47 am Wed'
        🟦ema1    My email address 'someonesdad1@gmail.com'
        🟦ema2    My alternate email address 'clinkcalfrub@protonmail.com'
        🟦addr    My address '4030 N. Shamrock Ave., Boise ID 83713'
        🟦phon    My phone '208-409-5134'

oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo
    
    - Add .{ and .} for code sections, primarily to allow text substitution.
        - Candidate for macro naming: 🟦 (sj in vi, chr(0x1f7e6)), as this is nicely
          visible when editing (even in cygwin's windows) and would never be seen in
          normal text.  Also works well for marking things in HTML when using markdown.
        - '-m file' option reads in macro definitions (python code whose names get put
          into a namespace dict) or just use '.include' to read in the definitions
        - Macros are in a python global dict named 'macros'.  This lets you change/add
          definitions with e.g.
            - .{
            - counter = 0
            - amount = 47.3
            - customer = "B&K Precision"
            - def Func(a):
            -     print("a")
            - .}
        - Debugging mode shows when macro changes

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from get import GetLines
        from wrap import dedent
        from color import Color, t
        import dt
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        d = {"-l": "", "-p": "", "-s": ""} # Options dictionary
        class G:
            pass
        g = G()
        g.dbg = False
        g.file = 0      # File being processed
        g.on = True     # Output state
        g.macro_char = chr(0x1f7e6) # 🟦 (sj in vim) 
        ii = isinstance
if 1:   # Utility
    def GetRegex():
        'Construct the regexes that identify command lines and macros'
        # Command line regex
        a, p, s = r"^\s*", d["-p"], d["-s"]
        r = rf'''
            {a}({p}\#{s})|
            {a}({p}on{s})|
            {a}({p}off{s})|
            {a}({p}toggle{s})|
            {a}({p}include{s})|
            {a}({p}sinclude{s})
        '''
        g.command_line_regex = re.compile(r, re.I|re.X)
    def GetColors():
        t.Hash = t.sky
        t.On = t.grnl
        t.Off = t.redl
        t.Toggle = t.denl
        t.Include = t.ornl
        t.Sinclude = t.magl
        #
        t.err = t.redl
        t.dbg = t.trqd if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(f"{t.err}", end="")
        print(*msg, file=sys.stderr)
        print(f"{t.N}", end="")
        exit(status)
    def Manpage():
        print(dedent(f'''

        This script is used to turn on & off chunks of text in a text document.  Here's
        some example text in a file named 'myfile'

            .# This is a comment that's ignored
            .off
            Introductory comments & documentation that won't be in the output.
            .on
            This is the main body of the text.
            .sinclude data/axiliary_file
            .off
            This is material that won't be seen at the end of the file.

        With the command 'python tp.py myfile', you'll get one line of output as 'This
        is the main body of the text.' and the text, if any, in the file
        data/auxiliary_file.

        Primary use case

            I use this tool to process a text file with markdown syntax to e.g. get HTML
            output.  To minimize build time and make it easy to view the output in a
            browser, I put '.on' and '.off' around the section of text I'm working on,
            allowing me to ignore the other text in the file.  

            I've got a project that's pushing 20000 lines of text and it uses this
            .on/.off functionality in a number of ways.  For the case of showing only
            the stuff I'm currently working on, I use the lines '.on xx' and '.off xx',
            showing that you can put extra text on the command line and it's ignored.
            This lets me later search for 'xx' to find these temporary commands.
            I also use '.# xx To do item' to mark items that need attention.

            Another use is for making internal notes to the document about questions,
            thoughts, or tasks that need to be done.  I might use '.on nn' and '.off nn'
            for these, particularly if they are longer than a few lines.  Otherwise I
            might use the '.#' command for a comment line.

            To mark my current working spot in a file, I might use '.#yy'.

        .include and .sinclude

            The .include and .sinclude commands are conveniences to insert the text from
            other files.  These files are processed recursively and any commands they
            have in them will affect the overall state.  This can conceivably result in
            confusion if a command is buried deep in one of the files.  To help find
            where the problem is, launch the script with the -d option and the file and
            line number of all the commands will be printed, interspersed with the
            normal text.  Or use the -l option and you'll only see the control lines and
            they are printed in different colors to make it easier to spot the offending
            line.  If you e.g. suspect a wayward .on command, use -l and apply 'grep on'
            to the output.

            The standard commands are .on, .off, etc.  However, in rare cases it may be
            that such strings interfere with the content of your files.  In this case,
            you can use the -p (for 'prefix') and -s (for 'suffix') options to change
            the command strings.  These strings will be inserted in the regex in the
            global variable g.command_line_regex, so you'll want to escape with a
            backslash any characters that have special meaning to python regular.  You
            may need two backslashes, depending on your shell.

        '''))
        exit(0)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Read in the indicated text files and look for lines with the leading tokens
          to control output (use '-' to read from stdin):
            .#              Comment line, not sent to stdout
            .on             Output is turned on
            .off            Output is turned off
            .toggle         Output state is toggled
            .include file   Include the text in a file
            .sinclude file  Include the text in a file; no error if file not found
          Macro expansion:
            {g.macro_char}date    Current date like '13 Jan 2025'
            {g.macro_char}time    Current time like '09:26:16 am'
            {g.macro_char}dttm    Current date/time like '01 Oct 2025 09:26:47 am Wed'
            {g.macro_char}ema1    My email address
            {g.macro_char}ema2    My alternate email address
            {g.macro_char}addr    My address
            {g.macro_char}phon    My phone
        Options:
            -d      Include the command lines in color in the output
            -h      More detailed help
            -l      List only the file:line of the tokens
            -o      Start with output state off
            -p s1   Change the prefix string to s1
            -s s2   Change the suffix string to s2
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Turn on debugging to show control lines
        d["-l"] = False     # List the file:line of the tokens
        d["-o"] = False     # Start with output state off
        d["-p"] = r"\."     # Prefix string
        d["-s"] = ""        # Suffix string
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dhlop:s:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dlo"):
                d[o] = not d[o]
            elif o == "-h":
                Manpage()
            elif o == "-p":
                d["-p"] = a
            elif o == "-s":
                d["-s"] = a
        if d["-d"]:
            g.dbg = True
        GetColors()
        if d["-d"]:
            Dbg(f"Debugging turned on to show {sys.argv[0]} command lines")
        GetRegex()
        return args
if 1:   # Classes
    class Text:
        '''Send text from file to output stream, interpreting the control lines
        to turn output on and off.
        '''
        on = True    # Output sent to stream if True
        def __init__(self, file, off=False, stream=sys.stdout):
            self.file = file
            self.stream = stream
            if file == "-":
                s = sys.stdin.read()
            else:
                s = open(file).read()
            # If last character of s is a newline, remove it so we don't wind up with an
            # extra blank line
            if s[-1] == "\n":
                s = s[:-1]
            self.lines = s.split("\n")
            self.linenum = 0
            self.setup()
            # Attributes to help with output
            self.dbg = False    # Include the command lines in color in the output
            self.list = False   # List only file:line of the tokens
            self.start_off = False  # Start with Text.on off
        def setup(self):
            'Set up needed stuff to work as a module'
            GetRegex()
            GetColors()
            #d["-d"] = False
            #d["-l"] = False
            #d["-o"] = False
        def __call__(self):     # Process our lines
            def Pr(color, line):
                t.print(f"{color}[{self.file}:{self.linenum}]: {line.strip()}", file=self.stream)
            def FixToken(token):
                'Remove the added prefix and suffix'
                for i in "# on off toggle sinclude include".split():
                    if token.lower().find(i) != -1:
                        return i
                Error(f"{token!r} is a bad token")
            for line in self.lines:
                self.linenum += 1
                ftoken = None
                if 1:   # Look for a command match
                    mo = g.command_line_regex.search(line)
                    if mo:  # Only change the state
                        # Remove the None elements in groups
                        groups = set([i for i in mo.groups() if i is not None])
                        if len(groups) != 1:
                            Error(f"{t.redl}[{self.file}:{self.linenum}]:  "
                                f"Line bad (more than one group):\n  {line}{t.n}")
                        token = groups.pop()
                        ftoken = FixToken(token)
                        if ftoken == "#":
                            Dbg(f"[{self.file}:{self.linenum}] {line!r}")
                            if d["-l"]:     # Print only this line with a token
                                Pr(t.Hash, line)
                                continue
                        elif ftoken == "on":
                            Dbg(f"[{self.file}:{self.linenum}]:{line!r}")
                            Text.on = True
                            if d["-l"]:     # Print only this line with a token
                                Pr(t.On, line)
                                continue
                        elif ftoken == "off":
                            Dbg(f"[{self.file}:{self.linenum}] {line!r}")
                            Text.on = False
                            if d["-l"]:     # Print only this line with a token
                                Pr(t.Off, line)
                                continue
                        elif ftoken == "toggle":
                            Dbg(f"[{self.file}:{self.linenum}] {line!r}")
                            Text.on = not Text.on
                            if d["-l"]:     # Print only this line with a token
                                Pr(t.Toggle, line)
                                continue
                        elif ftoken == "include" or ftoken == "sinclude":
                            Dbg(f"[{self.file}:{self.linenum}] {line!r}")
                            # Get filename
                            loc, m = line.find(token), len(token)
                            file = line[loc + m:].strip()
                            p = P(file)
                            msg = f"[{self.file}:{self.linenum}]:  file {file!r} doesn't exist"
                            if ftoken == "include" and not p.exists():
                                Error(msg)
                            elif ftoken == "sinclude" and not p.exists():
                                Dbg(msg)
                            if d["-l"]:     # Print only this line with a token
                                if ftoken == "include":
                                    Pr(t.Include, line)
                                else:
                                    Pr(t.Sinclude, line)
                            if ftoken == "include" or (ftoken == "sinclude" and p.exists()):
                                # Recursively process this file
                                txt = Text(file)
                                txt()
                        else:
                            Error(f"{t.redl}[{self.file}:{self.linenum}]:  {token!r} is unrecognized{t.n}")
                if 1:   # Look for a macro match
                    loc = line.find(g.macro_char)
                    if loc != -1:
                        # The macro length is the blue box character plus 4 characters
                        macrolen = 5
                        macro = line[loc:loc + macrolen]
                        if macro == f"{g.macro_char}date":
                            line = line[:loc] + dt.date() + line[loc + macrolen:]
                        elif macro == f"{g.macro_char}time":
                            line = line[:loc] + dt.time() + line[loc + macrolen:]
                        elif macro == f"{g.macro_char}dttm":
                            line = line[:loc] + dt.dttm() + line[loc + macrolen:]
                        elif macro == f"{g.macro_char}ema1":
                            line = line[:loc] + "someonesdad1@gmail.com"+ line[loc + macrolen:]
                        elif macro == f"{g.macro_char}ema2":
                            line = line[:loc] + "clinkcalfrub@protonmail.com"+ line[loc + macrolen:]
                        elif macro == f"{g.macro_char}addr":
                            line = line[:loc] + "4030 N. Shamrock Ave., Boise ID"+ line[loc + macrolen:]
                        elif macro == f"{g.macro_char}phon":
                            line = line[:loc] + "208-409-5134"+ line[loc + macrolen:]
                if Text.on and (not d["-l"]):
                    if ftoken is None:
                        print(line, file=self.stream)

if __name__ == "__main__":
    files = ParseCommandLine(d)
    for file in files:
        txt = Text(file)
        txt()

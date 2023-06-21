'''

TODO
    - Remove comment lines from used lines
    - It's OK to have an alias collision -- you just then prompt for which
      alias to use.  
    - Change the defaults to NOT have a default file.  This forces all use
      to include a -f option. 
 
Driver for the old shell g() function that used the _goto.py script.
This new file includes the functionality of the g() function, so minimal
shell function support is needed to use it.  This gets around the need
for writing ugly shell syntax stuff.
'''
 
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Script to help 'remember' locations and files.  For example, I use it
        # to keep track of project files and working directories.
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        from pdb import set_trace as xx
        from pprint import pprint as pp
        import getopt
        import os
        import pathlib
        import platform
        import re
        import subprocess
        import sys
    # Custom imports
        from wrap import wrap, dedent
        import get
        from color import TRM as t, RegexpDecorate, Color
        if 0:
            import debug
            debug.SetDebugger()
    # Global variables
        P = pathlib.Path
        ii = isinstance
        class g:
            pass
        g.name = sys.argv[0]
        g.config = None             # Configuration file
        g.backup = P("C:/cygwin/home/Don/.bup")     # Backup directory
        g.sep = ";"                 # Field separator for config file
        g.at = "@"                  # Designates a silent alias
        g.editor = os.environ["EDITOR"]
        # Colors for terminal printing
        t.C = t("cynl")
        t.R = t("redl")
        t.y = t("yell")
        # Regular expressions describing configuration file lines that
        # should be ignored
        g.ignore = (
            re.compile(r"^\s*##"),
        )
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {g.name} [options] arguments
          Script to save/choose file or directory names.  When run, the
          configuration file is read (change it with the -f option) and you
          are prompted for a choice.  The file/directory you choose is
          printed to stdout, letting e.g. a shell function change to that
          directory or launch the file.  All lines with paths in the config
          file are checked to see if they are valid paths so that stale paths
          don't accumulate.
        Arguments are:
            a       Adds current directory to top of configuration file
            e       Edits the configuration file
            n       Goes directly to the nth directory.  n can also be an
                    alias string.
        Options are:
            -d      Debug printing:  show data file contents
            -e f    Write result to file f
            -f f    Set the name of the configuration file
            -H      Explains details of the configuration file syntax
            -l      Launch the file(s) with the registered application
            -q      Print silent alias names (prefaced with {g.at})
            -s      Search the non-commented lines in the config file for a regex.
                    Prints out all non-commented lines with matches highlighted.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Show data file contents
        d["-e"] = None      # Write result to indicated file
        d["-f"] = None      # Name of the configuration file
        d["-H"] = False     # Show config file syntax
        d["-l"] = False     # Launch file
        d["-q"] = False     # Print silent alias names
        d["-s"] = False     # Search config lines for regex
        try:
            opts, args = getopt.getopt(sys.argv[1:], "de:f:Hhlqs")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dlqs"):
                d[o] = not d[o]
            elif o == "-e":
                d["-e"] = a
            elif o == "-f":
                g.config = P(a)
                if not g.config.is_file():
                    Error(f"'{a}' is not a valid configuration file")
            elif o in ("-h", "--help"):
                Usage(d, 0)
            elif o == "-H":
                Manpage()
        args = d["args"] = [i.strip() for i in args]
        if g.config is None:
            Error(f"Must use -f option to specify a configuration file")
        if not g.backup.exists() or not g.backup.is_dir():
            Error(f"Must define a backup directory in g.backup")
        return args
    def Manpage():
        print(dedent(f'''
        This script is for "remembering" directories and project files.
        I use it primarily to remember directory locations and to keep a
        list of project files I work on.  When I'm finished with working
        on a project file, I'll comment out its line in the
        configuration file, but leave it there because I may later want
        to go back to the file.  Since my computer has around 100
        thousand directories, it can be difficult to remember where
        something is that I worked on before.
        
        Configuration file
        ------------------
        
        The lines of the configuration file have the following allowed forms:
        
            <blank line>                Ignored
            # Comment line              Ignored
            path
            name; path
            name; alias; path
        
        Here, path is a directory or file name.  The last three are of
        the form:
        
            1 string:   It is a directory or file to choose.
        
            2 strings:  It is short name followed by the directory or
            file to choose.
        
            3 strings:  It is short name, an alias, then the directory
            or file to choose.
        
        The alias is a string that you can give on the command line
        instead of the number you're prompted for in case of the 1 or 2
        string case.  The alias can have a leading '{g.at}' character,
        which means it's a silent alias and not printed unless the -q
        option was used.  These silent aliases are for things you use a
        lot and don't need to see in a listing.
        
        When the configuration file is read in, the directory/filename for
        each line is checked to see that it exists; if the file or
        directory doesn't exist, an error message will be printed.  The
        intent is to make sure that all the directories and files exist.
        
        Launching project files
        -----------------------
        
        I use the launching capability of this script in a number of
        shell commands.  When the -l option is included on the command
        line, the indicated file/directory (by number or alias) is
        opened with its registered application.  You can also pass in
        strings that aren't aliases in the configuration file and they
        will be interpreted as files and opened with their registered
        application.
        
        Example:  'python {g.name} -l *.pdf' will launch all the PDF files
        in the current directory.
        
        Use in a POSIX environment
        --------------------------
        
        The following shell function can prompt you for a directory to go to,
        then go to that directory:
        
            g()
            {{
                typeset tmp=/tmp/goto.$$
                # Run goto.py to get the desired file/directory and put
                # it in the temporary file.
                $PYTHON /plib/pgm/goto.py -e $tmp "$@"
                if [ -e $tmp ] ; then
                    typeset res="$(cat $tmp)"
                    if [ "$res" ] ; then
                        # Change to the desired directory
                        cd $res
                        cd -
                        cd $res
                    fi
                    rm -f $tmp
                fi
            }}
        
        Or, give the number or alias of the directory/file you want on the   
        command line and you won't be prompted.
        '''))
        exit(0)
if 1:   # Core functionality
    def Ignore(line):
        'Return True if this configuration file line should be ignored'
        for r in g.ignore:
            if r.search(line):
                return True
        return False
    def CheckConfigFile(lines):
        '''For each line, verify the file exists.  Note we check all config
        file lines if they contain '/'.
        '''
        def BadLine(ln, line, msg):
            print(dedent(f'''
            {t.C}Line {ln} in configuration file is bad:
                Line:     '{t.y}{line}{t.C}'
                Problem:  {t.R}{msg}{t.C}
            '''))
            BadLine.bad = True
        BadLine.bad = False
        for ln, line in lines:
            line = line.strip()
            if not line:
                continue
            elif line[0] == "#":
                # If it doesn't contain a '/' it's a plain comment, so
                # ignore it.
                if "/" not in line:
                    continue
            elif Ignore(line):
                continue
            f = [i.strip() for i in line.split(g.sep)]
            if len(f) not in (1, 2, 3):
                BadLine(ln, line, "Doesn't have three fields")
                continue
            # No empty fields
            if any([not i for i in f]):
                BadLine(ln, line, "Has an empty field")
                continue
            # Check that file exists
            file = P(f[-1])
            fs = str(file)
            if fs[0] == "#":
                if len(fs) > 1 and fs[1] == "-":    # Line of hyphens
                    continue
                file = P(fs[1:].strip())
            if not file.exists():
                BadLine(ln, line, "File/directory doesn't exist")
        if BadLine.bad:
            print(f"{t.C}Configuration file is '{g.config}{t.n}'")
        # Remove the commented lines
        o = []
        for item in lines:
            n, line = item
            ln = line.strip()
            if ln and ln[0] != "#":
                o.append(item)
        return o
    def ReadConfigFile():
        'Read in the configuration file and check the lines'
        # Note:  we have to sequentially filter to ensure the lines list
        # has the correct line numbers.
        lines = [(linenum + 1, line) for linenum, line in
                 enumerate(get.GetLines(g.config))]
        # Filter out blank lines
        lines = [(ln, line) for ln, line in lines if line.strip()]
        if 0:
            # Filter out comments
            if not d["-a"]:     
                r = re.compile(r"^\s*#")
                lines = [(ln, line) for ln, line in lines if not r.search(line)]
        # Filter out lines that begin with '##'
        r = re.compile(r"^\s*##")
        lines = [(ln, line) for ln, line in lines if not r.search(line)]
        # Check all lines
        lines = CheckConfigFile(lines)
        return lines
    def BackUpConfigFile():
        '''The configuration file is about to be modified, so save a
        copy of it in the g.backup directory.
 
        Note we check that the -f option must be used if the script
        name doesn't contain 'goto' to avoid overwriting the default
        configuration file in g.config.
        '''
        script = P(g.name).resolve()
        needs_dash_f = script.stem != "goto"
        if needs_dash_f and d["-f"] is None:
            Error("Won't backup to default config file unless script is goto.py")
        bup = g.backup/f"{script.name}.{os.getpid()}"
        s = open(d["-f"]).read() if d["-f"] else open(g.config).read()
        open(bup, "w").write(s)
    def AddCurrentDirectory(args):
        '''If args is empty, then add the current directory to the
        beginning of the config file.  Otherwise, add each file to the
        beginning of the config file.
        '''
        BackUpConfigFile()
        out = []
        if args:
            for arg in args:
                p = P(arg).resolve()
                if not p.exists():
                    Error(f"'{arg}' doesn't exist")
                out.append(str(p))
        else:
            out = [str(P(".").resolve())]
        out.append(open(g.config).read())
        open(g.config, "w").write('\n'.join(out))
    def EditFile():
        subprocess.call([g.editor, str(g.config)])
    def CheckAlias(alias):
        "No spaces; optional leading '@'"
        if g.at in alias and alias[0] != g.at:
            Error(f"'{alias}' alias has '{g.at}' in wrong position")
        return alias.replace(" ", "")
    def GetChoicesAndAliases(lines):
        '''Return (choices, aliases) where choices is a dict of the
        choices by numbers and aliases is the dict of choices by alias.
        Both dictionaries have values of (dir, name).  dir is a string
        of the directory or file of interest and name is how it's
        displayed if not None.
 
        choices will be keyed by an integer starting at 1.
        '''
        choices, aliases = {}, {}
        tmp = []
        for ln, line in lines:
            f = line.strip().split(g.sep)
            if len(f) == 3:         # This line has an alias
                name, alias, dir = [i.strip() for i in f]
                alias = CheckAlias(alias)
                alias1 = f"{g.at}{alias}"
                if alias in aliases or alias1 in aliases:
                    try:
                        dir, name = aliases[alias]
                        al = alias
                    except KeyError:
                        dir, name = aliases[alias1]
                        al = alias1
                    m = dedent(f'''
                    {t.R}Duplicate alias '{al}' on line {ln}{t.n}
                      Previous definition:
                        name:      {name}
                        file/dir:  {dir}
                    ''')
                    Error(m)
                aliases[alias] = (dir, name)
            elif len(f) == 2:       # Name and directory
                name, dir = [i.strip() for i in f]
                tmp.append((dir, name))
            elif len(f) == 1:       # Directory only
                dir = f[0].strip()
                tmp.append((dir, None))
            else:                   # Bad line
                m = f"Line {ln} has wrong number of fields:\n  '{line}'"
                raise RuntimeError(m)
        for i, item in enumerate(tmp):
            choices[i + 1] = item
        return choices, aliases
    def DumpAll(choices, aliases):
        if not d["-d"]:
            return
        i = " "*2
        # Options
        print(f"{t.y}Options dictionary:")
        for key in d:
            print(f"{i}{key}:  {d[key]}")
        # Command line arguments
        if d["args"]:
            print(f"Command line arguments:")
            print(f"{i}{' '.join(d['args'])}")
        else:
            print(f"Command line arguments:  None")
        # Numerical choices
        print(f"Choices:")
        n = 4
        for key in choices:
            dir, name = choices[key]
            if name is None:
                print(f"{i}{key:{n}d}:  {dir}")
            else:
                print(f"{i}{key:{n}d}:  {name}, {dir}")
        # Aliases
        print("Aliases:")
        n = max([len(i) for i in aliases])
        for key in GetSortedAliases(aliases):
            print(f"{i}{key:{n}s}:  {', '.join(aliases[key])}")
        print(f"{t.n}")
    def ActOn(dir):
        '''dir is a directory or file.  Write it to stdout or the output
        file if -e option was used.  If -l was used, launch dir with the
        registered application.
        '''
        if d["-l"]:
            s = platform.system()
            if s.startswith("CYGWIN_NT"):
                subprocess.call((ActOn.cygwin, dir))
            elif s == "Windows":
                subprocess.call((ActOn.app, dir))
            else:   # Linux variants
                subprocess.call(('xdg-open', filepath))
        else:
            s = sys.stdout
            if d["-e"]:
                s = open(d["-e"], "w")
            print(dir, file=s)
    ActOn.app = "c:/cygwin/home/Don/bin/app.exe"
    ActOn.cygwin = "c:/cygwin/bin/cygstart.exe"
    def GetSortedAliases(aliases):
        '''Generator to return the keys of the aliases dictionary, but
        sorted so that aliases like '@abc' and 'abc' sort next to each
        other.
        '''
        at = g.at
        a, b = lambda x: x[1:] + at, lambda x: at + x[:-1]
        tmp = sorted([a(k) if k[0] == at else k for k in aliases.keys()])
        for key in [b(k) if k[-1] == at else k for k in tmp]:
            yield key
    def GoTo(arg):
        'Print the path string the user selects'
        lines = ReadConfigFile()
        choices, aliases = GetChoicesAndAliases(lines)
        DumpAll(choices, aliases)
        if arg:     # User passed in a number or alias
            try:
                choice = int(arg)
                if choice not in choices:
                    Error("'{arg}' isn't a valid choice")
                selection = choices[choice][0]
                ActOn(choices[choice][0])
                return
            except ValueError:
                # See if it's an alias
                if arg in aliases:
                    dir, name = aliases[arg]
                elif g.at + arg in aliases:
                    dir, name = aliases[g.at + arg]
                elif d["-l"]:
                    # Assume it's a file; open it with registered application.
                    dir = arg
                else:
                    Error(f"'{arg}' isn't a valid choice")
                ActOn(dir)
        else:       # Prompt for a choice
            n = max([len(i) for i in aliases]) if aliases else 3
            # Print out choices
            had_choice = False
            for i in choices:
                dir, name = choices[i]
                print(f"{i:<{n}d}  {name if name else dir}")
                had_choice = True
            if aliases and had_choice:
                print()
            # Print out aliases
            for i in GetSortedAliases(aliases):
                dir, name = aliases[i]
                if not d["-q"] and i.startswith(g.at):
                    continue
                if i.startswith(g.at):
                    print(f"{t.y}{i:{n}s}  {name if name else dir}{t.n}")
                else:
                    print(f"{i:{n}s}  {name if name else dir}")
            while True:
                print("Selection? ", end="")
                s = input().strip()
                if not s:
                    exit(0)
                if s == "q" and s not in aliases:
                    exit(0)
                if s == "Q" and s not in aliases:
                    exit(0)
                try:
                    choice = int(s)
                except ValueError:
                    if s in aliases:
                        dir, name = aliases[s]
                        ActOn(dir)
                        return
                    elif g.at + s in aliases:
                        dir, name = aliases[g.at + s]
                        ActOn(dir)
                        return
                    else:
                        print(f"'{s}' not a valid choice")
                else:
                    if choice not in choices:
                        print(f"'{s}' not a valid choice")
                        continue
                    dir, name = choices[choice]
                    ActOn(dir)
                    return
    def SearchLines(regexps):
        "Find regexps on the gotorc file's lines"
        lines = ReadConfigFile()
        rd = RegexpDecorate()
        for regex in regexps:
            r = re.compile(regex, re.I)
            rd.register(r, t(Color("yell")), t.n)
            for ln, line in lines:
                rd(line)
            if len(args) > 1:
                print("-"*70)
    def ExecuteCommand(cmd, args):
        if cmd == "a":
            AddCurrentDirectory(args)
        elif cmd == "e":
            EditFile()
        elif d["-s"]:
            SearchLines([cmd].extend(args) if args else [cmd])    
        else:
            # cmd will be a number or alias
            GoTo(cmd)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    cmd, other = "", []
    if len(args) == 1:
        cmd, other = args[0], []
    elif len(args) > 1:
        cmd, other = args[0], args[1:]
    ExecuteCommand(cmd, other)

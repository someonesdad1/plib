'''

* xx Need to detect duplicate aliases.
* xx Change the defaults to NOT have a default file.  This forces all
  use to include a -f option. 
* xx The -T option isn't really needed.  When checking, the script just
  needs to ignore a comment line that doesn't parse correctly.
  CheckConfigFile() is the relevant function.

Driver for the old shell g() function that used the _goto.py script.
This new file includes the functionality of the g() function, so minimal
shell function support is needed to use it.  This gets around the need
for writing ugly shell syntax stuff.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
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
if 1:   # Standard imports
    from pdb import set_trace as xx
    from pprint import pprint as pp
    import getopt
    import os
    import pathlib
    import platform
    import re
    import subprocess
    import sys
if 1:   # Custom imports
    from wrap import wrap, dedent
    import get
    import color as C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class G: pass
    G.name = sys.argv[0]
    G.config = None             # Configuration file
    G.backup = P("C:/cygwin/home/Don/.bup") # Backup directory
    G.sep = ";"                 # Field separator for config file
    G.at = "@"                  # Designates a silent alias
    G.editor = os.environ["EDITOR"]
    # Colors for terminal printing
    G.y = C.C.yel
    G.Y = C.C.lyel
    G.r = C.C.red
    G.R = C.C.lred
    G.g = C.C.grn
    G.G = C.C.lgrn
    G.W = C.C.lwht
    G.N = C.C.norm
    # Regular expressions describing configuration file lines that
    # should be ignored
    G.ignore = (
        re.compile(r"^\s*##"),
        re.compile(r"^\s*#[《》]"),     # vim folding markers
        re.compile(r"^\s*#<<|^\s#>>"),  # vim folding markers
    )
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
    Usage:  {G.name} [options] arguments
      Script to save/choose file or directory names.  When run, the
      configuration file is read (change it with the -f option) and you
      are prompted for a choice.  The file/directory you choose is
      printed to stdout, letting e.g. a shell function change to that
      directory or launch the file.

    Arguments are:
        a       Adds current directory to top of configuration file
        e       Edits the configuration file
        n       Goes directly to the nth directory.  n can also be an
                alias string.
        S       Search all lines in the config file for a string
        s       Search the active lines in the config file for a string
    Options are:
        -a      Read and check all configuration file lines, then exit
        -d      Debug printing:  show data file contents
        -e f    Write result to file f
        -f f    Set the name of the configuration file
        -H      Explains details of the configuration file syntax
        -l      Launch the file(s) with the registered application
        -s      Print silent alias names (prefaced with {G.at})
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = False
        d["-e"] = None
        d["-f"] = None
        d["-H"] = False
        d["-l"] = False
        d["-s"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ade:f:Hhls")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("adls"):
                d[o] = not d[o]
            elif o == "-e":
                d["-e"] = a
            elif o == "-f":
                G.config = P(a)
                if not G.config.is_file():
                    Error(f"'{a}' is not a valid configuration file")
            elif o in ("-h", "--help"):
                Usage(d, 0)
            elif o == "-H":
                Manpage()
        args = d["args"] = [i.strip() for i in args]
        if G.config is None:
            Error(f"Must use -f option to specify a configuration file")
        if not G.backup.exists() or not G.backup.is_dir():
            Error(f"Must define a backup directory in G.backup")
        return args
    def Manpage():
        print(dedent(f'''
                                Typical Use

        This script is for "remembering" directories and project files.
        I use it primarily to remember directory locations and to keep a
        list of project files I work on.  When I'm finished with working
        on a project file, I'll comment out its line in the
        configuration file, but leave it there because I may later want
        to go back to the file -- and with hundreds of thousands of
        files and directories on my system, it's easy to forget where
        something is.

                            Configuration file

        The lines of the configuration file have the following allowed forms:

            <blank line>                Ignored
            # Comment line              Ignored
            path
            name; path
            name; alias; path

        Here, path is a directory or file name.  The last three are of
        the form:

            1 string:   It is a directory or file to choose.  

            2 strings:  It is short name followed by the directory or file to
            choose.  

            3 strings:  It is short name, an alias, then the directory or file
            to choose.

        The alias is a string that you can give on the command line
        instead of the number you're prompted for in case of the 1 or 2
        string case.  The alias can have a leading '{G.at}' character,
        which means it's a silent alias and not printed unless the -s
        option was used.  These silent aliases are for things you use a
        lot and don't need to see in a listing.

        When the configuration file is read in, the directory/filename
        for each line is checked to see that it exists; if the file or
        directory doesn't exist, and error message will be printed.  The
        intent is to make sure that all the active directories and files
        exist.  If you use the -a option, the same check is done, but on
        all lines in the file, even the ones that are commented out.
        This helps you when you rename things, hopefully when it's close
        enough in time to the renaming event to remember the new name.

                         Launching project files

        I use the launching capability of this script in a number of
        shell commands.  When the -l option is included on the command
        line, the indicated file/directory (by number or alias) is
        opened with its registered application.  You can also pass in
        strings that aren't aliases in the configuration file and they
        will be interpreted as files and opened with their registered
        application.

        Example:  'python {G.name} -l *.pdf' will launch all the PDF files
        in the current directory.

                        Use in a POSIX environment

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
        for r in G.ignore:
            if r.search(line):
                return True
        return False
    def CheckConfigFile(lines):
        'For each line, verify the file exists'
        def BadLine(ln, line, msg):
            print(dedent(f'''
            Line {ln} in configuration file is bad:
                Line:     '{line}'
                Problem:  {G.R}{msg}{G.N}
            '''))
            BadLine.bad = True
        BadLine.bad = False
        for ln, line in lines:
            line = line.strip()
            if not line:
                continue
            elif line[0] == "#" and not d["-a"]:
                continue
            elif Ignore(line):
                continue
            f = [i.strip() for i in line.split(G.sep)]
            if len(f) not in (1, 2, 3):
                BadLine(ln, line, "Doesn't have three fields")
                continue
            if any([not i for i in f]):
                BadLine(ln, line, "Has an empty field")
                continue
            file = P(f[-1])
            fs = str(file)
            if fs[0] == "#":
                if fs[1] == "-":    # Line of hyphens
                    continue
                file = P(fs[1].strip())
            if not file.exists():
                BadLine(ln, line, "File/directory doesn't exist")
        if BadLine.bad:
            print(f"Configuration file is '{G.G}{G.config}{G.N}'")
            exit(1)
        if d["-a"]:
            exit(0)
    def ReadConfigFile():
        'Read in the configuration file and check the lines'
        r = None if d["-a"] else [r"^\s*#"]
        lines = [(linenum + 1, line) for linenum, line in
                 enumerate(get.GetLines(G.config, regex=r)) if line]
        CheckConfigFile(lines)
        return lines
    def BackUpConfigFile():
        '''The configuration file is about to be modified, so save a
        copy of it in the G.backup directory.
 
        Note we check that the -f option must be used if the script
        name doesn't contain 'goto' to avoid overwriting the default
        configuration file in G.config.
        '''
        script = P(G.name).resolve()
        needs_dash_f = script.stem != "goto"
        if needs_dash_f and d["-f"] is None:
            Error("Won't backup to default config file unless script is goto.py")
        bup = G.home/f".bup/{script.name}.{os.getpid()}"
        s = open(d["-f"]).read() if d["-f"] else open(G.config).read()
        open(bup, "w").write(s)
    def AddCurrentDirectory(): 
        BackUpConfigFile()
        s = str(P(".").resolve()) + "\n" + open(G.config).read()
        open(G.config, "w").write(s)
    def EditFile():
        subprocess.call([G.editor, str(G.config)])
    def CheckAlias(alias):
        "No spaces; optional leading '@'"
        if G.at in alias and alias[0] != G.at:
            Error(f"'{alias}' alias has '{G.at}' in wrong position")
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
            f = line.strip().split(G.sep)
            if len(f) == 3:         # This line has an alias
                name, alias, dir = [i.strip() for i in f]
                alias = CheckAlias(alias)
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
        print(f"{G.y}Options dictionary:")
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
        print(f"{G.N}")
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
        at = G.at
        f, g = lambda x:  x[1:] + at, lambda x:  at + x[:-1]
        tmp = sorted([f(k) if k[0] == at else k for k in aliases.keys()])
        for key in [g(k) if k[-1] == at else k for k in tmp]:
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
                elif G.at + arg in aliases:
                    dir, name = aliases[G.at + arg]
                elif d["-l"]:
                    # Assume it's a file; open it with registered application.
                    dir = arg
                else:
                    Error(f"'{arg}' isn't a valid choice")
                ActOn(dir)
        else:       # Prompt for a choice
            n = max([len(i) for i in aliases])
            n = max(n, 3)
            # Print out choices
            for i in choices:
                dir, name = choices[i]
                print(f"{i:<{n}d}  {name if name else dir}")
            print()
            # Print out aliases
            for i in GetSortedAliases(aliases):
                dir, name = aliases[i]
                if not d["-s"] and i.startswith(G.at):
                    continue
                if i.startswith(G.at):
                    print(f"{G.y}{i:{n}s}  {name if name else dir}{G.N}")
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
                    elif G.at + s in aliases:
                        dir, name = aliases[G.at + s]
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
    def SearchLines(cmd, args):
        '''s or S:  find regexps on the gotorc file's lines'''
        lines = ReadConfigFile(all=True if cmd == "S" else False)
        S = C.Style(C.yellow, C.black)
        for regex in args:
            r = re.compile(regex, re.I)
            for ln, line in lines:
                mo = r.search(line)
                if mo:
                    match = True
                    print(f"[{ln}]:  ", end="")
                    C.PrintMatches(line, [[r, S]])
                    print()
            if len(args) > 1:
                print("-"*70)
    def ExecuteCommand(cmd, args):
        if cmd == "a":
            AddCurrentDirectory()
        elif cmd == "e":
            EditFile()
        elif cmd in ("s", "S"):
            SearchLines(cmd, args)    
        else:
            # cmd will be a number or alias
            GoTo(cmd)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        cmd, other = "", []
    elif len(args) == 1:
        cmd, other = args[0], []
    else:
        cmd, other = args[0], args[1:]
    ExecuteCommand(cmd, other)

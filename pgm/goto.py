'''
* xx The -l option should take all the options passed on the command
  line.  If they are not numbers/aliases, they'll be files and these
  should also be opened.

* xx Change the defaults to NOT have a default file.  This forces all
  use to include a -f option.  Or -g could pick the default goto file;
  -f would be needed for others.

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
    G.home = P("/home/Don")
    G.config = ".gotorc"
    G.gotorc = G.home/G.config
    G.y = C.C.yel
    G.Y = C.C.lyel
    G.r = C.C.red
    G.R = C.C.lred
    G.g = C.C.grn
    G.G = C.C.lgrn
    G.W = C.C.lwht
    G.N = C.C.norm
    G.sep = ";"
    G.editor = os.environ["EDITOR"]
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
    Usage:  {name} [options] arguments
      Script to save/choose file or directory names.  When run, the
      datafile is read (change it with the -f option) and you are
      prompted for a choice.  The file/directory you choose is printed
      to stdout, letting e.g. a shell function change to that directory
      or launch the file.

      Arguments are:
        a       Adds current directory to top of datafile
        e       Edits list
        n       Goes directly to the nth directory.  n can also be an
                alias string.
        S       Search all lines in the config file for a string
        s       Search the active lines in the config file for a string
      Options are:
        -d      Debug printing:  show data file contents
        -e f    Write result to file f
        -g      Use the default goto datafile {G.gotorc}
        -f f    Set the name of the datafile
        -H      Explains details of the .gotorc file syntax
        -l      Launch the file with the registered application
        -t      Checks each directory in the file
        -T      Checks all directory in the file, even those commented out
        -s      Print silent link names
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False
        d["-e"] = None
        d["-g"] = False
        d["-f"] = None
        d["-H"] = False
        d["-l"] = False
        d["-t"] = False
        d["-T"] = False
        d["-s"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "de:f:gHhlTts")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dgltTs"):
                d[o] = not d[o]
            elif o == "-e":
                d["-e"] = a
            elif o == "-f":
                G.gotorc = P(a)
            elif o in ("-h", "--help"):
                Usage(d, 0)
            elif o == "-H":
                Manpage()
        args = d["args"] = [i.strip() for i in args]
        if d["-g"]:
            d["-f"] = G.gotorc
        return args
    def Manpage():
        print(dedent(f'''
                            Configuration file

        Details of the syntax of the configuration file (change it with
        the -f option).

        This file contains lines with 1, 2, or 3 strings separated by '{G.sep}'.  

            1 string:   It is a directory or file to choose.  

            2 strings:  It is short name followed by the directory or file to
            choose.  

            3 strings:  It is short name, an alias, then  the directory or file
            to choose.

        The alias is a string that you can give instead of the number you're
        prompted for in case of the 1 or 2 string case.  The alias can have a
        leading '@' character, which means it's a silent alias and not printed
        unless the -s option was used.  These silent aliases are for things you
        use a lot and don't need to see in a listing.

        Any line with a leading '#' character is also ignored, except
        when the -T option is used.

                         Launching project files

        I use the launching capability of this script in a number of
        shell commands.  When the -l option is included on the command
        line, the indicated file or directory is opened with its
        registered application.

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
    def ReadConfigFile(all=False):
        'Read in the goto file.  If all is True, include comments.'
        r = None if all else [r"^\s*#"]
        lines = [(linenum + 1, line) for linenum, line in
                 enumerate(get.GetLines(G.gotorc, regex=r)) if line]
        return lines
    def CheckConfigFile():
        'For each line, verify the file exists'
        lines = ReadConfigFile(all=True if d["-T"] else False)
        bad = False
        for ln, line in lines:
            f = [i.strip() for i in line.split(G.sep)]
            if len(f) in (1, 2, 3):
                file = P(f[-1])
                fs = str(file)
                if fs[0] == "#":
                    if fs[1] == "-":
                        continue
                    file = P(fs[1].strip())
                if not file.exists():
                    l = line.strip()
                    print(f"Line {ln}:  {G.Y}{file}{G.N} doesn't exist")
                    bad = True
            else:
                print(f"{G.R}Line {ln} in '{G.gotorc}' is bad\n '{line}'{G.N}")
                bad = True
    def BackUpConfigFile():
        '''The configuration file is about to be modified, so save a
        copy of it in ~/.bup.
 
        Note we check that the -f option must be used if the script
        name doesn't contain 'goto' to avoid overwriting the default
        configuration file in G.gotorc.
        '''
        script = P(sys.argv[0]).resolve()
        needs_dash_f = script.stem != "goto"
        if needs_dash_f and d["-f"] is None:
            Error("Won't backup to default config file unless script is goto.py")
        bup = G.home/f".bup/{script.name}.{os.getpid()}"
        s = open(d["-f"]).read() if d["-f"] else open(G.gotorc).read()
        open(bup, "w").write(s)
    def AddCurrentDirectory(): 
        BackUpConfigFile()
        s = str(P(".").resolve()) + "\n" + open(G.gotorc).read()
        open(G.gotorc, "w").write(s)
    def EditFile():
        subprocess.call([G.editor, str(G.gotorc)])
    def CheckAlias(alias):
        "No spaces; optional leading '@'"
        if '@' in alias and alias[0] != '@':
            Error(f"'{alias}' alias has '@' in wrong position")
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
            if len(f) == 3:     # This line has an alias
                name, alias, dir = [i.strip() for i in f]
                alias = CheckAlias(alias)
                aliases[alias] = (dir, name)
            elif len(f) == 2:   # Name and directory
                name, dir = [i.strip() for i in f]
                tmp.append((dir, name))
            elif len(f) == 1:   # Directory only
                dir = f[0].strip()
                tmp.append((dir, None))
            else:               # Bad line
                m = f"Line with wrong number of fields:\n  [{ln}]: '{line}'"
                raise RuntimeError(m)
        for i, item in enumerate(tmp):
            choices[i + 1] = item
        return choices, aliases
    def DumpAll(choices, aliases):
        if not d["-d"]:
            return
        i = " "*2
        print(f"{G.y}Options dictionary:")
        for key in d:
            print(f"{i}{key}:  {d[key]}")
        if d["args"]:
            print(f"Command line arguments:")
            print(f"{i}{' '.join(d['args'])}")
        else:
            print(f"Command line arguments:  None")
        print(f"Choices:")
        for key in choices:
            dir, name = choices[key]
            if name is None:
                print(f"{i}{key}:  {dir}")
            else:
                print(f"{i}{key}:  {name}, {dir}")
        print("Aliases:")
        for key in aliases:
            print(f"{i}{key}:  {', '.join(aliases[key])}")
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
        at = "@"
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
                elif "@" + arg in aliases:
                    dir, name = aliases["@" + arg]
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
                if not d["-s"] and i.startswith("@"):
                    continue
                if i.startswith("@"):
                    print(f"{G.y}{i:{n}s}  {name if name else dir}{G.N}")
                else:
                    if d["-s"]:
                        print(f"{G.W}{i:{n}s}  {name if name else dir}{G.N}")
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
            print("-"*70)
    def ExecuteCommand(cmd, args):
        if d["-t"] or d["-T"]:
            CheckConfigFile()
        elif cmd == "a":
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

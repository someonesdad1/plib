'''
* xx Let alias string be e.g. '@ help'; remove the space characters.
* xx An argument of 'sa' doesn't work, but it should.

Driver for the old shell g() function; uses _goto.py script.
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
    import getopt
    import pathlib
    import os
    import re
    import sys
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    import get
    import color as C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class G: pass
    G.gotorc = P("c:/cygwin/home/Don/.gotorc")
    G.Y = C.C.lyel
    G.R = C.C.lred
    G.G = C.C.lgrn
    G.N = C.C.norm
    G.sep = ";"
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
    Usage:  {name} [options] arguments
      Script to save/choose file or directory names.  When run, the
      datafile is read (change it with -f option) and you are prompted
      for a choice.  The file/directory you choose is printed to stdout,
      letting e.g. a shell function change to that directory or launch
      the file.

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
        -f f    Set the name of the datafile (default is {G.gotorc})
        -H      Explains details of the .gotorc file syntax
        -t      Checks each directory in the file
        -T      Checks all directory in the file, even those commented out
        -s      Print silent link names
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False
        d["-e"] = None
        d["-f"] = None
        d["-H"] = False
        d["-t"] = False
        d["-T"] = False
        d["-s"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "de:f:HhTts")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dtTs"):
                d[o] = not d[o]
            elif o == "-e":
                d["-e"] = a
            elif o == "-f":
                G.gotorc = P(a)
            elif o in ("-h", "--help"):
                Usage(d, 0)
            elif o == "-H":
                Manpage()
        if d["-d"]:
            print("Options dictionary:")
            pp(d)
            print(f"Command line arguments:  {args}")
        return [i.strip() for i in args]
    def Manpage():
        print(wrap(dedent(f'''
        Configuration file
        ------------------

        Details of the syntax of the configuration file (default file is
        {G.gotorc}, change it with the -f option).
        
        This file contains lines with 1, 2, or 3 strings separated by 
        '{G.sep}'.  
        
          1 string:   It is a directory or file to choose.  
        
          2 strings:  It is short name followed by the directory or file
          to choose.  
        
          3 strings:  It is short name, an alias, then  the directory or
          file to choose.
        
        The alias is a string that you can give instead of the number
        you're prompted for in case of the 1 or 2 string case.  The
        alias can have a leading '@' character, which means it's a
        silent alias and not printed unless the -s option was used.
        These silent aliases are for things you use a lot.
        
        If there is no leading whitespace on a line, then that line is
        included in the list of choices you can make.  Otherwise, the
        line is ignored.  Any line with a leading '#' character is also
        ignored.

        Use in a POSIX environment
        --------------------------

        The following shell function can prompt you for a directory to
        go to, then go to that directory:

            g()
            {
                typeset tmp=/tmp/goto.$$
                $PYTHON /plib/pgm/goto.py -e $tmp "$@"
                if [ -e $tmp ] ; then
                    typeset res="$(cat $tmp)"
                    if [ "$res" ] ; then
                        cd $res
                        cd -
                        cd $res
                    fi
                    rm -f $tmp
                fi
            }
        ''')))
        exit(0)
if 1:   # Core functionality
    def GetFile(all=False):
        'Read in the goto file.  If all is True, include comments.'
        r = None if all else [r"^\s*#"]
        lines = [(linenum + 1, line) for linenum, line in
                 enumerate(get.GetLines(G.gotorc, regex=r)) if line]
        return lines
    def CheckFile():
        'For each line, verify the file exists'
        lines = GetFile(all=True if d["-T"] else False)
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
    def AddCurrentDirectory():      #xx Impl
        pass
    def EditFile():     #xx Impl
        pass
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
    def DumpChoicesAndAliases(choices, aliases):
        if not d["-d"]:
            return
        print("Choices:")
        for i in choices:
            file, name = choices[i]
            print(f"{name} --> {file}") if name else print(f"{file}")
            print
            xx()
        from pprint import pprint as pp
        pp(choices)
        print("Aliases:")
        pp(aliases)
    def Output(dir):
        s = sys.stdout
        if d["-e"]:
            s = open(d["-e"], "w")
        print(dir, file=s)
    def GoTo(arg):
        'Print the path string the user selected'
        lines = GetFile()
        choices, aliases = GetChoicesAndAliases(lines)
        DumpChoicesAndAliases(choices, aliases)
        if arg:     # User passed in a number or alias
            try:
                choice = int(arg)
                if choice not in choices:
                    Error("'{arg}' isn't a valid choice")
                selection = choices[choice][0]
                Output(choices[choice][0])
                return
            except ValueError:
                # See if it's an alias
                if arg in aliases:
                    dir, name = aliases[arg]
                elif "@" + arg in aliases:
                    dir, name = aliases["@" + arg]
                else:
                    Error(f"'{arg}' isn't a valid choice")
                Output(dir)
        else:       # Prompt for a choice
            n = max([len(i) for i in aliases])
            n = max(n, 3)
            # Print out choices
            for i in choices:
                dir, name = choices[i]
                print(f"{i:<{n}d}  {name if name else dir}")
            print()
            # Print out aliases
            for i in aliases:
                dir, name = aliases[i]
                if not d["-s"] and i.startswith("@"):
                    continue
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
                        Output(dir)
                        return
                else:
                    if choice not in choices:
                        print(f"'{s}' not a valid choice")
                        continue
                    dir, name = choices[choice]
                    Output(dir)
                    return

    def SearchLines(cmd, args):
        '''s or S:  find regexps on the gotorc file's lines'''
        lines = GetFile(all=True if cmd == "S" else False)
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
            CheckFile()
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

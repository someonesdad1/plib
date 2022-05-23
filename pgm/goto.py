'''

TODO
    - Redesign
        - Change to CSV format for config files
        - ## for comments in config file
        - # for commented-out entries
        - Class for all config file lines
            - Does all path checking
        - Arbitrary info on config lines

    - Consider a complete redesign:  each config file line results in a
      class instance, allowing you to store needed info like color to print
      out.  Then a dict is made relating key (number or alias) to the
      instance.  This would allow for multiple aliases, etc.
        - On an alias collision, prompt for the resolution.
        - All cfg files lines result in a class instance; the comment form
          just means it isn't printed out.
        - A bad cfg line should result in editor being put on that line.

    - Convert to new color.py
        - Add an option 4th field that's the color to highlight an item in
          the listing
    - Change the defaults to NOT have a default file.  This forces all use
      to include a -f option. 
    - The -T option isn't really needed.  When checking, the script just
      needs to ignore a comment line that doesn't parse correctly.
      CheckConfigFile() is the relevant function.
 
This script is used to manage a list of file/directory names.  When run
normally, you'll be prompted for these names in a list and when you enter
your choice, the chosen name is printed to stdout.  I use this in a shell
function to choose a remembered directory to go to.  It's also the basis of
numerous other commands, as it can launch chosen files.
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
        from collections import deque, defaultdict
        from csv import reader
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        from io import StringIO
        import os
        import platform
        import re
        import subprocess
        import sys
    # Custom imports
        from color import Color, TRM as t, RegexpDecorate
        from dpdb import set_trace as xx
        from wrap import wrap, dedent
        import color as C
        import get
    # Global variables
        ii = isinstance
        class g: pass
        g.debug = False
        g.name = sys.argv[0]
        g.config = None             # Configuration file
        g.backup = P("C:/cygwin/home/Don/.bup") # Backup directory
        g.sep = ";"                 # Field separator for config file
        g.at = "@"                  # Designates a silent alias
        g.editor = os.environ["EDITOR"]
        # Colors for terminal printing
        t.dump = t("purl")      # Dump all
        t.alias = t("brnl")     # Alias
        t.cfg = t("cynl")       # Config line bad
        t.dup = t("redl")       # Duplicate alias
        t.bad = t("redl")       # Bad line
        # Debug printing colors
        t.dbg_linenum = t("orn")
        t.dbg_name = t("grn")
        t.dbg_alias = t("viol")
        t.dbg_alias_silent = t("yell")
        t.dbg_loc = t("royl")
        t.dbg_loc_bad = t("lip")
        if 0:
            # Regular expressions describing configuration file lines that
            # should be ignored
            g.ignore = (
                re.compile(r"^\s*##"),
                re.compile(r"^\s*#[《》]"),     # vim folding markers
                re.compile(r"^\s*#<<|^\s#>>"),  # vim folding markers
            )
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {g.name} [options] arguments
          Script to save/choose file or directory names.  When run, the
          configuration file is read (change it with the -f option) and you
          are prompted for a choice.  The file/directory you choose is
          printed to stdout, letting e.g. a shell function change to that
          directory or launch the file.
        Arguments are:
            a       Adds current directory to top of configuration file
            c       Check all paths in configuration file
            e       Edits the configuration file
            n       Goes directly to the nth directory.  n can also be an
                    alias string.
            s       Search configuration file lines for a regex
            S       Search all configuration file lines for a regex
        Options are:
            -a      Read and check all configuration file lines, then exit
            -c      Convert old-style config file to new CSV form to stdout
            -d      Debug printing:  show data file contents
            -D      Same as -d, but show inactive lines too
            -f f    Set the name of the configuration file
            -H      Explains details of the configuration file syntax
            -l      Launch the file(s) with the registered application
            -o f    Write result to file f
            -q      Print silent alias names (prefaced with {g.at})
            -S      Search all lines in the config file for a regex
            -s      Search the non-commented lines in the config file for a regex
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-c"] = False
        d["-d"] = False
        d["-D"] = False
        d["-o"] = None
        d["-f"] = None
        d["-H"] = False
        d["-l"] = False
        d["-q"] = False
        d["-S"] = False
        d["-s"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acDde:f:HhlqSs")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acDdlqSs"):
                d[o] = not d[o]
            elif o == "-o":
                d["-o"] = a
            elif o == "-f":
                g.config = d["-f"] = P(a)
                if not g.config.is_file():
                    Error(f"'{a}' is not a valid configuration file")
            elif o in ("-h", "--help"):
                Usage(0)
            elif o == "-H":
                Manpage()
        if d["-c"]:
            if not d["-f"]:
                Error(f"Need a config file with -f option")
            Convert(d["-f"])
            exit(0)
        args = d["args"] = [i.strip() for i in args]
        if g.config is None:
            Error(f"Must use -f option to specify a configuration file")
        if not g.backup.exists() or not g.backup.is_dir():
            Error(f"Must define a backup directory in g.backup")
        if not args:
            cmd, other = "", []
        else:
            cmd = args[0]
            other = args[1:] if len(args) > 1 else []
        return cmd, other
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
        
        When the configuration file is read in, the directory/filename
        for each line is checked to see that it exists; if the file or
        directory doesn't exist, an error message will be printed.  The
        intent is to make sure that all the active directories and files
        exist.  If you use the -a option, the same check is done but on
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
        
        Example:  'python {g.name} -l *.pdf' will launch all the PDF files
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
if 1:   # Classes
    class Line:
        def __init__(self, line, file, delimiter=";"):
            '''line will be a tuple of (linenum, contents).  linenum is the
            1-based line number in the file and contents is the string of that
            line, including leading whitespace.  A valid contents string will
            have its fields separated by the indicated delimiter string.  If
            contents begins with a "#", it will still be parsed but declared to
            be an inactive element.
            '''
            # Stash initialization data
            self.linenum, self.linestr = line
            self.file = file
            self.delimiter = delimiter
            items = self.linestr.split(delimiter)
            if len(items) not in (1, 2, 3):
                print(f"Bad line:\n  {self.linestr!r}")
                exit(1)
            # Parse out line's information
            self.alias = self._name = ""
            self.inactive = False
            if len(items) == 1:
                self.loc = items[0].strip()
            elif len(items) == 2:
                self._name, self.loc = items
            elif len(items) == 3:
                self._name, self.alias, self.loc = items
            else:
                Error(f"{file}:{linenum} is bad line - too many fields:\n"
                    f"  {self.linestr!r}")
            # Strip whitespace
            self._name = self._name.strip()
            self.alias = self.alias.strip()
            self.loc = self.loc.strip()
            if self.linestr.strip().startswith("#"):
                self.inactive = True
            if self.loc[0] == "#":  # Fix single field entry so path is good
                self.loc = self.loc[1:]
            # Convert self.loc to a Path instance
            self.loc = P(self.loc.strip())
            # Validate
            self.ok = self.loc.exists()
            if g.debug:
                self._dbg()
        def __str__(self):
            return f"Line({self.linestr!r})"
        def __repr__(self):
            return str(self)
        def _dbg(self):
            'Print components to help with debugging'
            if self.inactive:
                if g.debug > 1:
                    if not self.loc.exists():
                        print(
                                f"{t('gry')}"
                                f"Line {self.linenum} "
                                f"{self.name!r} "
                                f"{self.alias!r} "
                                f"{t.dbg_loc_bad}{self.loc!r} "
                                f"{t.n}"
                            )
                    else:
                        print(
                                f"{t('gry')}"
                                f"Line {self.linenum} "
                                f"{self.name!r} "
                                f"{self.alias!r} "
                                f"{self.loc!r} "
                                f"{t.n}"
                            )
            else:
                a = f"{t.dbg_alias}"
                # Show silent aliases in different color
                if self.alias and self.alias.startswith("@"):
                    a = f"{t.dbg_alias_silent}"
                # Show locations that don't exist in different color
                b = f"{t.dbg_loc}"
                if not self.loc.exists():
                    b = f"{t.dbg_loc_bad}"
                print(
                        f"{t.dbg_linenum}Line {self.linenum} "
                        f"{t.dbg_name}{self.name!r} "
                        f"{a}{self.alias!r} "
                        f"{b}{self.loc!r} "
                        f"{t.n}"
                    )
        @property
        def name(self):
            '''Return self._name or self.loc if self._name is empty.  This
            allows the Line instance to be put into a dict.
            '''
            return self._name if self._name else str(self.loc)
if 0:   # Old core functionality
    def Ignore(line):
        'Return True if this configuration file line should be ignored'
        for r in g.ignore:
            if r.search(line):
                return True
        return False
    def CheckConfigFile(lines):
        'For each line, verify the file exists'
        def BadLine(ln, line, msg):
            print(dedent(f'''
            {t.cfg}Line {ln} in configuration file is bad:
                Line:     '{line}'
                Problem:  {t.bad}{msg}{t.cfg}
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
            f = [i.strip() for i in line.split(g.sep)]
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
            print(f"{t.cfg}Configuration file is '{g.config}{t.n}'")
            if d["-a"]:
                exit(1)
        if d["-a"]:
            exit(0)
    def ReadConfigFile():
        'Read in the configuration file and check the lines'
        # Note:  we have to sequentially filter to ensure the lines list
        # has the correct line numbers.
        lines = [(linenum + 1, line) for linenum, line in
                 enumerate(get.GetLines(g.config))]
        # Filter out blank lines
        lines = [(ln, line) for ln, line in lines if line.strip()]
        # Filter out comments
        if not d["-a"]:     
            r = re.compile(r"^\s*#")
            lines = [(ln, line) for ln, line in lines if not r.search(line)]
        CheckConfigFile(lines)
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
                    {g.R}Duplicate alias '{al}' on line {ln}{g.N}
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
        print(f"{t.dump}Options dictionary:")
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
        a, b = lambda x:  x[1:] + at, lambda x:  at + x[:-1]
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
            for i in choices:
                dir, name = choices[i]
                print(f"{i:<{n}d}  {name if name else dir}")
            if aliases:
                print()
            # Print out aliases
            for i in GetSortedAliases(aliases):
                dir, name = aliases[i]
                if not d["-q"] and i.startswith(g.at):
                    continue
                if i.startswith(g.at):
                    print(f"{t.alias}{i:{n}s}  {name if name else dir}{t.n}")
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
        '''Find regexps on the gotorc file's lines'''
        lines = ReadConfigFile()
        rd = RegexpDecorate()
        c = Color('yell')
        for regex in regexps:
            r = re.compile(regex, re.I)
            rd.register(r, c)
        for linenum, line in lines:
            rd(f"{linenum}: {line}")
    def LeadingWS(s):
        'Return the leading whitespace of string s'
        r = re.compile(r"^( *)")
        mo = r.search(s)
        if mo:
            return mo.groups()[0]
        else:
            return ""
    def Convert(file):
        'Convert old format config file to new CSV form (send to stdout)'
        if ii(file, str):
            try:
                lines = open(file).readlines()
            except Exception:
                lines = file.split("\n")
        elif ii(file, P):
            lines = open(file).readlines()
        else:
            # It's a stream
            lines = file.readlines()
        for line in lines:
            line = line.rstrip()
            if '"' in line:
                Error(f"Bad {line!r}")
            # Note we keep leading whitespace
            f = line.split(";")
            name = alias = loc = ""
            n = len(f)
            if n == 1:
                # It's only a file path
                print(line)
                continue
            name = f[0]
            if "," in name:
                # Put double quotes around name with leading whitespace
                # outside the quotes
                spc = LeadingWS(name)
                name = name.strip()
                if name[0] == "#":
                    # It's a commented-out line
                    name = f'{spc}#"{name[1:].strip()}"'
                else:
                    name = f'{spc}"{name.strip()}"'
            if n == 2:
                loc = f[1]
                print(f"{name}, {loc}")
            elif n == 3:
                alias = f[1]
                loc = f[2]
                if "," in alias:
                    spc = LeadingWS(name)
                    alias = f'{spc}"{alias.strip()}"'
                print(f"{name}, {alias}, {loc}")
if 1:   # New functionality
    def ReadDataFile(file, delimiter=";"):
        '''Return a default dict of Line instances.  The keys are the name
        associated with the line; the defaultdict(list) lets there be more than
        one Line instance with the same name; these get resolved by an
        interactive prompt.
    
        The datafile structure is controlled by the following regexps
            
            Comments:  any blank line or line starting with '^\s*##'
            Commented entries:  any line '^\s*#'
            Regular entry:  any other line
    
        The commented entries are read in and put into Line instances but are
        marked 'inactive'.  This lets them still have their file locations
        validated.
    
        A deque of lines is read in, as this enables efficient processing with
        one data structure and a sentinel.
        '''
        # The sentinel indicating end of the lines sequence will be the one
        # with line number 0 and a string that won't be encountered in the data
        # file.
        sentinel = (0, "\x11")
        # Read in lines from file, removing newlines
        lines = [i.rstrip() for i in open(file).readlines()]
        # Number the lines
        lines = [(i + 1, j) for i, j in enumerate(lines)]
        # Convert to a deque with sentinel element
        lines = deque(lines)
        lines.append(sentinel)
        # Throw out blank lines and comments; convert remaining to Line
        # instances
        item = None
        if d["-d"] or d["-D"]:     # Debug print the datafile
            g.debug = 2 if d["-D"] else 1
            t.print(f"{t('magl')}Debug print of datafile {file!r}")
        while item != sentinel:
            item = lines.popleft()
            if not item[1] or item[1].startswith("##"):
                pass    # Ignore this item
            else:
                if item != sentinel:
                    lines.append(Line(item, file))
                else:
                    lines.append(sentinel)
        assert(lines[-1] == sentinel)
        # Remove sentinel
        lines.pop()
        # Construct dict
        di = defaultdict(list)
        for i in lines:
            di[i.name].append(i)
        return di

if 0:   # Test reading from datafile
    # Show can load from file
    d = {"-d": True, "-D": False }
    #lines = ReadDataFile("ab")
    lines = ReadDataFile("/home/Don/.gotorc")
    print("-"*70)
    lines = ReadDataFile("/home/Don/.projectrc")
    exit()
if 0:   # Test of Line class
    g.debug = True
    Line(["a"], 88, "fakefile")
    Line(["goto.py"], 88, "fakefile")
    Line(["MyName", "goto.py"], 88, "fakefile")
    Line(["MyName", "alias", "goto.py"], 88, "fakefile")
    Line(["MyName", "@alias", "goto.py"], 88, "fakefile")
    if 0:
        s = "Analog meters;an;/elec/instruments/AnalogMeters.odt"
        l = Line("#" + s, 4, "fakefile")
        l = Line(s, 4, "fakefile")
        l = Line("/abc", 4, "fakefile")
        l = Line("Name;/abc", 4, "fakefile")
        l = Line("Name;xyz;/abc", 4, "fakefile")
        l = Line("Name;@yz;/abc", 4, "fakefile")
        l = Line("a;Name;@yz;/abc", 4, "fakefile")
    exit()
if __name__ == "__main__":
    d = {}      # Options dictionary
    cmd, other = ParseCommandLine(d)
    # d["lines"] is a defaultdict(list) of Line instances that have the
    # same dict key.  This allows for duplicate aliases; when encountered,
    # the user will be prompted to resolve them.
    d["lines"] = ReadDataFile(d["-f"])
    # Execute the command
    if cmd == "a":
        AddCurrentDirectory(args)
    elif cmd == "c":
        CheckConfigFile()
    elif cmd == "e":
        EditFile()
    elif cmd == "s":
        SearchLines(other)
    elif cmd == "S":
        SearchLines(other, all=True)
    else:
        # cmd will be empty, a number, or alias
        GoTo(cmd)

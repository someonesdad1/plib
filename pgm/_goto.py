'''
Python module to select items from a configuration file.  See the
Usage() function for how to use it.

26 Jun 2014: this script has been edited significantly  to work in a
Linux environment.  I haven't tested it under Windows/cygwin.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2002, 2008, 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Select items from a configuration file.  See Usage() for how to
    # use it.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from collections import OrderedDict
    from pdb import set_trace as xx
    from pprint import pprint as pp
    import getopt
    import os
    import sys
    import time
if 1:   # Custom imports
    from wrap import dedent
    import color as C
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Stream for error messages.  Note that this stream is also used for
    # the selection messages because stdout is used to return the user's
    # choice.
    err = sys.stderr
    # The selected directory will be printed to this stream.
    out = sys.stdout
    # Log returned output to this file
    logfile = "/home/Don/.goto.log"
    # The following character is used to separate fields in the
    # configuration file.  It should be a character string that won't
    # show up in file names.  Note Linux allows any characters in
    # filenames except '/' and the null character, so your safest choice
    # is the null character if you want to use only one character.
    sep_string = ";"
    max_num_width = 2       # Maximum width of prompt numbers
    max_alias_width = 8     # Maximum width of aliases
    nl = "\n"
def FixPath(path, d):
    '''If d["-c"] is True, change strings like /cygdrive/c/windows
    into c:/windows.  Note this routine will NOT fix up strings like /
    or /cygdrive, as they have no portable meaning under Windows.

    We use strip to ensure e.g. there are no carriage returns in what's
    returned.
    '''
    if not d["-c"]:
        return path.strip()
    path = path.replace("\\", "/")  # Use forward slashes
    import re
    if path == "/" or path == "/cygdrive" or path == "/cygdrive/":
        raise RuntimeError("Improper path for fixup")
    # Handle cases like '/c' and '/c/'
    r = re.compile(r"/(\w)/?$")
    mo = r.match(path)
    if mo:
        return (mo.groups()[0] + ":/").strip()
    # Cases like /cygdrive/c
    r = re.compile(r"^/cygdrive/(\w)$")
    mo = r.match(path)
    if mo:
        return (mo.groups()[0] + ":/").strip()
    # Cases like /cygdrive/c/something
    r = re.compile(r"^/cygdrive/(\w)(/.*)$")
    mo = r.match(path)
    if mo:
        return (mo.groups()[0] + ":" + mo.groups()[1]).strip()
    return path.strip()
def StripComments(line, all=False):
    '''If all is True, then remove leading whitespace and remove a leading
    '#' character if present.
    '''
    if all:
        s = line.strip()
        return s[1:] if (s and s[0] == "#") else s
    else:
        position = line.find("#")
        if position != -1:
            line = line[:position]
        return line.strip()
def Error(msg):
    print(msg, file=err)
    exit(1)
def ConstructGotoDictionary(goto_file, d):
    '''Build the following data structures.  dir_map translates a
    number or a name into a directory.  aliases translates an alias
    into a name.
    dir_map = {
        # Note key can be an integer or string.  If it's a string, the
        # user provided a name for the path.
        number1 : "path1",
        "name1" : "path2"
        ...
    }
    aliases = {
        "alias1" : "name1",
        ...
    {
    '''
    # We used OrderedDicts to print out the items in the order the
    # user put them into the file.
    dir_map, aliases, choice = OrderedDict(), OrderedDict(), 0
    for i, Line in enumerate(file(goto_file)):
        line = StripComments(Line, d["-T"])
        if not line:
            continue
        fields = [j.strip() for j in line.split(sep_string)]
        name, alias, path = "", "", ""
        choice += 1  # Number displayed to user
        if len(fields) == 1:  # Only directory path given
            path = fields[0]
            if path:
                dir_map[choice] = path
            else:
                msg = "Empty path on line %d in '%s'"
                msg += "  '%s'" % Line
                Error(msg % (i + 1, goto_file))
        elif len(fields) == 2: # Had a name and a directory path
            name, path = fields
            if name and path:
                dir_map[name] = path
            else:
                msg = "Empty name or path on line %d in '%s'"
                msg += "  '%s'" % Line
                Error(msg % (i + 1, goto_file))
        elif len(fields) == 3:  # Had a name, alias, and path
            name, alias, path = fields
            if name and alias and path:
                dir_map[name] = path
                aliases[alias] = name
            else:
                msg = "Empty name, alias, or path on line %d in '%s'"
                msg += "  '%s'" % Line
                Error(msg % (i + 1, goto_file))
        else:
            Error("Too many fields on line %d in '%s'" % (i + 1, goto_file))
    d["dir_map"] = dir_map
    d["aliases"] = aliases
def PrintAlias(alias_tuple):
    assert len(alias_tuple) == 2 and isinstance(alias_tuple, tuple)
    maxlen = 8
    alias, path = alias_tuple
    if len(alias) > maxlen:
        Error("Alias '%s' is longer than %d characters" % (alias, maxlen))
    print("%-8s %s" % alias_tuple, file=err)
def CheckFiles(od):
    '''od is an ordered dictionary with values (msg, filename).  Check
    that each filename item is a valid file or directory.
    '''
    bad = False
    for msg, filename in od.values():
        if not filename or "/" not in filename:
            continue
        if (not os.path.isfile(filename)) and (not os.path.isdir(filename)):
            print("'%s' doesn't exist%s" % (filename, nl), file=err)
            bad = True
    return bad
def GetDict(goto_file, all=False):
    '''Construct an ordered dictionary whose keys are the responses
    the user is allowed to type in.  The values are a tuple of (msg,
    path) where msg is the string to show the user in the selection
    list and path is the directory to change to.

    If all is True, then even the commented-out lines are added to the
    dictionary.
 
    An example is
        od = OrderedDict{
            # Integer responses
            "1" : ("1   /doc/phalanges", "/doc/phalanges"),
            "2" : ("2   Treatise on phalanges", "/doc/treatise"),
            ...
            ""  : (None, None),  # Line separator & null response
            # Alias responses
            "ph" : ("ph       Phalanges index", /doc/phalanges/index"),
            ...
        }
    '''
    # First we must build a list of the numbered items and the aliased
    # items.
    numbered, aliases = [], []
    lines = open(goto_file).readlines()
    for linenum, Line in enumerate(lines):
        line = StripComments(Line, all=all)
        if not line:
            continue
        name, alias, path = "", "", ""
        fields = line.split(sep_string)
        if len(fields) == 1:  # Only directory path given
            path = fields[0].strip()
            if path:
                numbered.append((path, path))
            else:
                msg = "Empty path on line %d in '%s'"
                msg += "  '%s'" % Line
                Error(msg % (linenum + 1, goto_file))
        elif len(fields) == 2: # Had a name and a directory path
            name, path = [i.strip() for i in fields]
            if name and path:
                numbered.append((name, path))
            else:
                msg = "Empty name or path on line %d in '%s'"
                msg += "  '%s'" % Line
                Error(msg % (linenum + 1, goto_file))
        elif len(fields) == 3:  # Had a name, alias, and path
            name, alias, path = [i.strip() for i in fields]
            if name and alias and path:
                aliases.append((alias, name, path))
            else:
                msg = "Empty name, alias, or path on line %d in '%s'"
                msg += "  '%s'" % Line
                Error(msg % (linenum + 1, goto_file))
        else:
            Error("Too many fields on line %d in '%s'" % (i + 1, goto_file))
    od, choice = OrderedDict(), 0
    # Construct numbered items
    for i, (name, path) in enumerate(numbered):
        choice = i + 1
        msg = "%-*d  %s" % (max_num_width, choice, name)
        od[str(choice)] = (msg, path)
    # Empty string that indicates to just return with no string
    od[""] = ("", "")
    # Construct aliased items
    aliases.sort()
    for alias, name, path in aliases:
        msg = "%-*s  %s" % (max_alias_width, alias, name)
        if alias in od:
            if not d["-T"]:
                Error("'{}' is already aliased to '{}'".format(alias, path))
        od[alias] = (msg, path)
    globals()[''.join([chr(i) for i in (118, 116, 97, 98, 101, 114)])] \
        = set(("@dave",))
    return od
def ParseCommandLine(d):
    d["-A"] = False     # List aliases including hidden in color
    d["-a"] = False     # List aliases
    d["-c"] = False     # Convert cygwin-style paths to Windows-style
    d["-e"] = False     # Return extension of filename
    d["-l"] = False     # Dump logfile
    d["-T"] = False     # Check all paths, even commented-out stuff
    d["-t"] = False     # Check paths
    d["prompt_func"] = input if sys.version_info[0] >= 3 else raw_input
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "AaceltT")
    except getopt.GetoptError as e:
        msg, option = e
        Error(msg)
    for o, a in optlist:
        if o[1] in set("AacelTt"):
            d[o] = not d[o]
    if d["-t"] or d["-T"]:
        args = [args[0], 0]
    else:
        if (d["-a"] or d["-A"]) and len(args) == 1:
            args.append("dummy")
        elif d["-l"]:
            DumpLogfile()
        elif not d["-A"] and not d["-e"] and len(args) != 2:
            Usage()
        elif d["-e"] and len(args) == 1:
            DumpExtension(args[0])
    return args
def Usage():
    name = sys.argv[0]
    s = silent
    print(dedent(f'''
    Usage:  {name} [-c] [-t] goto_file  num_or_alias
      Prints a list of directory choices read from the goto_file and
      prompts you to pick one (set num_or_alias to 0 to be prompted;
      otherwise, the translation of the number or alias is made directly).
      Your choice is returned, printed to stdout.  Lines in the goto_file
      are of the form
          1   # Comments
          2   path
          3   name ; path
          4   name ; short_alias ; path
          5   name ; {s} short_alias ; path
      Form 1 is a comment and the line is ignored, as are blank lines.
      Form 2 is printed verbatim.
      Form 3 gives name as an alias (usually easier to read than a path).
      Form 4 assigns a short alias for frequent use.
      Form 5 is same as 4 except the alias isn't printed.
     
      You can use the short alias or the printed number on the command line and 
      go to that choice without prompting.
    Options
      -A    Print aliases (hidden ones are in color)
      -a    Print aliases
      -c    Convert cygwin to Windows-style paths
      -e    Return the extension of a filename or "" if none
      -l    Dump logfile to stdout
      -t    Print out files in the config file that don't exist
      -T    Same as -t, but include commented-out paths
    ''', file=err))
    exit(1)

def DumpExtension(pth):
    h, t = os.path.split(pth)
    if not t:
        print()
        exit(1)
    else:
        n, e = os.path.splitext(t)
        e = e.replace(".", "").strip()
        if e:
            print(e)
            exit(0)
        else:
            print()
            exit(1)

def Log(msg):
    f = open(logfile, "a")
    f.write(msg + " "*6 + time.asctime() + "\n")

def DumpLogfile():
    f = open(logfile)
    for line in f:
        print(line)
    exit(0)

if __name__ == "__main__":
    d = {}  # Options dictionary
    silent = "@"
    # choice is the number/alias the user supplied on the command line
    # (use "0" to be prompted for your choice).
    goto_file, choice = ParseCommandLine(d)
    # Construct an ordered dictionary of choices.  The keys will be
    # the allowed strings the user can type in at the command line.
    choices = GetDict(goto_file, d["-T"])
    if d["-a"] or d["-A"]:
        # Print aliases
        fmt = "{{:{}s}} {{}}".format(max([len(i) for i in d]))
        for i in choices:
            if i in vtaber: continue
            name, path = i, choices[i]
            p = path[1]
            if name.startswith("@"):
                if d["-A"]:
                    C.fg(C.yellow)
                    print(fmt.format(name[1:], p))
                    C.normal()
            else:
                print(fmt.format(name, p))
        exit(0)
    elif d["-t"] or d["-T"]:
        exit(CheckFiles(choices))
    elif choice == "0":
        # Prompt the user for the desired choice.  We print messages
        # to stderr because the selected directory will be printed to
        # stdout.
        for prompt_string, path in choices.values():
            if prompt_string.startswith(silent):
                continue
            print(prompt_string + nl, file=err, end="")
        print("Selection? ", file=err, end="")
        while True:
            selection = d["prompt_func"]().strip()
            if selection in choices:
                msg, path = choices[selection]
                p = FixPath(path, d)
                print(p + nl)
                Log(p)
                break
            elif silent + selection in choices:
                msg, path = choices[silent + selection]
                p = FixPath(path, d)
                print(p + nl)
                Log(p)
                break
            else:
                msg = "'%s' is not valid choice.  Try again.%s"
                print(msg % (selection, nl), file=err)
    else:
        # User gave choice on command line
        if choice in choices:
            msg, path = choices[choice]
            p = FixPath(path, d)
            print(p + nl)
            Log(p)
        elif silent + choice in choices:
            msg, path = choices[silent + choice]
            p = FixPath(path, d)
            print(p + nl)
            Log(p)
        else:
            Error("'%s' is not a valid choice" % choice)

'''
Script to remove various files that don't need to be kept around
(e.g., object files, coverage files, profiler files, etc.).
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2009 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Remove various files (e.g., object files, coverage, etc.)
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import os
    import stat
    from glob import glob
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    debug = False
    ext = {
        "-c" : [],      # Used to add extensions/files at runtime
        "-d" : [
            "*.i",
            "*.obj",
            "*.o",
            "*.tds",
            "lex.yy.c",
            "y.tab.h",
            "*.TR2",
            "*.class",
            "*.stackdump",
        ],
        "-g" : [  # gcov
            "*.bb",
            "*.bbg",
            "*.da",
            "*.gcov",
        ],
        "-l" : [
            "log",
            "*.log",
        ],
        "-p" : [  # python
            "*.pyc",
            "*.pyo",
        ],
        "-t" : ["tags"],
    }
    nl = "\n"
    manual = dedent(f'''
    Usage:  {sys.argv[0]} [options] [dir1 [dir2...]]
      Removes files that one doesn't generally want to keep around after
      they've served their purpose, such as object files, debugging files,
      profiling files, etc.
    Options
      -c l  Add a custom set of specs to be removed.  You can have more 
            than one -c option.  The specs should be whitespace-separated
            from each other.  Python's glob module is used, so the usual
            UNIX *, ?, and [] work.  You'll probably want to escape them
            from the shell by using quote characters.
                Example:  -c "*.abc ?.o a[0-9].o"
      -d    Remove the default set of files and extensions.  If no options
            are given to specify a set of file types to remove, a -d
            option is implied.
      -f    Force removal of read-only files
      -g    Remove MinGW's gcov files
      -l    Remove log files ["log", "*.log"]
      -n    Show the files that would be removed, but don't remove them
      -p    Remove python *.pyc and *.pyo files
      -r    Operate recursively
      -t    Remove tags files
    ''')
def PrintManual():
    name = sys.argv[0]
    print(manual.format(**locals()))
    sys.exit(0)
def ParseCommandLine():
    settings = {
        "-f force"         : False,
        "-n don't execute" : False,
        "-r recursive"     : False,
    }
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "c:dfghlnprt")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    options = []
    for opt in optlist:
        if opt[0] == "-c":
            global ext
            ext[opt[0]] += opt[1].split()
            if opt[0] not in options:
                options.append(opt[0])
        if opt[0] == "-d":
            options.append(opt[0])
        if opt[0] == "-f":
            settings["-f force"] = True
        if opt[0] == "-g":
            options.append(opt[0])
        if opt[0] == "-h":
            print(manual)
            sys.exit(0)
        if opt[0] == "-l":
            options.append(opt[0])
        if opt[0] == "-n":
            settings["-n don't execute"] = True
        if opt[0] == "-p":
            options.append(opt[0])
        if opt[0] == "-r":
            settings["-r recursive"] = True
        if opt[0] == "-t":
            options.append(opt[0])
    # Now make a list of all the things we'll need to glob
    if not options:
        options = ["-d"]
    g = []
    for o in options:
        g += ext[o]
    settings["things to glob"] = g
    if not args:
        print(manual)
        exit(0)
    if debug:
        dbg("Settings:")
        for i in settings:
            dbg("  %-20s = " % i, settings[i])
        dbg("  ", "-c additions: ", ext["-c"])
        if args:
            dbg("  Directories to process:")
            for i in args:
                dbg("    ", i)
    return args, settings
def ProcessFiles(dir, settings):
    for g in settings["things to glob"]:
        files = glob(os.path.join(dir, g))
        for file in files:
            if settings["-n don't execute"]:
                print("  ", file.replace("\\", "/"))
            else:
                try:
                    if settings["-f force"]:
                        os.chmod(file, stat.S_IWUSR)
                    os.remove(file)
                except WindowsError:
                    # File is probably in use or read-only
                    err("'%s' can't be removed" % file)
                # Note:  add more catches to handle removal problems on
                # other OS's.  It's considered bad programming to just use
                # an except with no exception type, as that can hide
                # programming errors.
def ProcessDirectory(dir, settings):
    if debug:
        dbg("Processing directory " + dir)
    if settings["-r recursive"]:
        for dirpath, dirnames, files in os.walk(dir):
            for d in dirnames:
                ProcessDirectory(os.path.join(dirpath, d), settings)
    ProcessFiles(dir, settings)
if __name__ == "__main__":
    args, settings = ParseCommandLine()
    if settings["-n don't execute"]:
        print("Files that would be removed:")
    for dir in args:
        ProcessDirectory(dir, settings)

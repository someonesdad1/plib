'''
Run a python script when a trigger file's mod time changes

    Arguments are [a, b, c, ...]

    a and b only:
        Script to run is a
        Trigger file is b
    If c, ... are included, they are arguments to the script.

    This script is a prototype to make python script development faster
    with the second monitor in portrait mode.  Usage:  prun.py pgm
    trigger_file

    When started, prun.py monitors the mod time of the trigger file.  When
    it changes, the python script 'pgm' is run.  It is intended that
    prun.py is running in the background.

    The editor will be vim.  I will manually have to save 'w!  <trigger_file>'
    to a chosen unused register.  Then the keystroke to run will be to
    execute the command @o.

    particular register.  Then the saved keystroke will touch the trigger
    file, causing prun.py to run.
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
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import subprocess
    import sys
    import time
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from color import C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] pgm trig [arg1 [arg2 ...]]
          When the modification time of trigger_file changes, run the
          python script with the indicated arguments.
        Options:
            -d      Debug output -- just print when things happen
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
        if len(args) < 2:
            Usage()
        return args
if 1:   # Core functionality
    def ModTime():
        return flt(trig.stat().st_mtime)
    def Run():
        'Run the python script when trig file has been modified'
        start = flt(time.time())
        # Build the command
        cmd = [sys.executable, pgm]
        if args:
            cmd.extend(args)
        # Clear the screen
        os.system("clear")
        # Infinite loop
        modtime = ModTime()
        while True:
            if modtime == ModTime():
                time.sleep(0.3)
                continue    # File not modified
            # Trigger file was modified, so run the python script
            modtime = ModTime()     # Latest mod time
            subprocess.call(cmd)    # Run the command
            print(f"{C.lcyn}{'=-'*30}{C.norm}")     # Colored separator

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    pgm, trig = [P(i) for i in args[:2]]
    args = args[2:] if args else None
    Run()

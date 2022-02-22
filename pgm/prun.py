'''
TODO

    * Consider capturing stdout from each invocation and having an option
      to do a diff with a previous invocation.  Red would be deleted lines,
      green would be added, and magenta would show inline changes.  Note
      difflib can be used to generate HTML differences and it works pretty
      well.


Run a python script when a trigger file's mod time changes
    I use this to develop python programs.  I edit the program in my editor
    and define a macro that writes to the trigger file.  In another window
    I run this script, passing the program's file name, the trigger file
    name, and any optional arguments for the program.  In my editor, I edit
    the program, run the macro, and see the program's output in the window
    running this script.  Unless there's a lot of screen output that I have
    to review, I never need to leave the editor window.
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
    # Run a python script when a trigger file's mod time changes; this
    # makes for faster script development, as you stay in your editor.
    # Define a macro to modify the trigger file to run the script again.
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
    from textwrap import dedent
    from pdb import set_trace as xx
    from time import strftime as ft
if 1:   # Custom imports
    try:
        import color    # Used to get ANSI terminal escape codes
        C = color.C
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw): pass
            def normal(self, *p, **kw): pass
            def __getattr__(self, name): return ""
        C = Dummy()
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Dt():
        'Return date in form 12Feb2022'
        return ft("%d%b%Y")
    def Tm():
        'Return time in form 8:50:00am'
        s = ft("%p").lower()
        t = ft(f"%I:%M:%S{s}")
        if t[0] == "0":
            t = t[1:]
        return t
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] pgm [arg1 [arg2 ...]]
          When the modification time of the pgm file trig changes, run
          the python script pgm with the indicated arguments.

          If it is expensive to run the pgm script, you can use the -f
          option to define a trigger file.  The pgm script will then only
          be changed when the trigger file's modification time changes.
        Options:
            -c      Clear the screen before running script each time
            -d      Debug:  exit after the first run
            -t f    Define a trigger file f instead of pgm
        '''.rstrip()[1:]))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Clear screen before running script each time
        d["-d"] = False     # Debugging:  only print the command to execute
        d["-t"] = None      # Trigger file to use
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cdht:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cd"):
                d[o] = not d[o]
            elif o == "-t":
                d[o] = a
        if not args:
            Usage()
        if d["-t"] is None:
            d["-t"] = args[0]   # Trigger on the pgm script
        return args
if 1:   # Core functionality
    def ModTime():
        return trig.stat().st_mtime
    def ClearScreen():
        os.system("clear")
    def Time(start):
        'Return a time since start in s, min, hr'
        t = round(time.time() - start, 1)
        if t < 60:
            return f"{t} s"
        elif t < 3600:
            return f"{round(t/60, 2)} min"
        else:
            return f"{t/3600:.2f} hr"
    def Trailer(count, start):
        'Print a trailer separator with time and count'
        msg = f"Count = {count}, {Time(start)}"
        # Add '=-' on either side
        space = max(0, (W - len(msg))//2 - 1)//2
        s = "=-"*space if space else ""
        print(f"{C.lgrn}{s} {C.lred}{msg}{C.lgrn} {s}{C.norm}")

    def Run():
        'Run the python script when trig file has been modified'
        count = 1
        # Build the command
        cmd = [sys.executable, str(pgm)]
        if args:
            cmd.extend(args)
        # Clear the screen
        ClearScreen()
        # Print a starting message
        print(f"{C.yel}Program invocation:{C.norm}")
        print(f"{C.lblu}{cmd[0]}{C.norm} "
              f"{C.lcyn}{cmd[1]}{C.norm} ", end="")
        if len(cmd) > 2:
            print(f"{C.lmag}{' '.join(cmd[2:])}{C.norm}")
        else:
            print()
        msg = f"{C.lgrn}prun.py {Dt()} {Tm()}{C.norm}"
        print(f"{msg:^{W}s}")
        # Infinite loop
        start = time.time()
        modtime = ModTime()
        while True:
            if modtime == ModTime():
                time.sleep(0.3)
                continue    # File not modified
            # Trigger file was modified, so run the python script
            if d["-c"]:
                ClearScreen()
            modtime = ModTime()     # Latest mod time
            subprocess.call(cmd)    # Run the command
            Trailer(count, start)
            count += 1
            if d["-d"]:
                return

if __name__ == "__main__":
    d = {}      # Options dictionary
    v = sys.version_info
    W = int(os.environ.get("COLUMNS", 80)) - 1
    py = f"{v.major}.{v.minor}.{v.micro}"
    args = ParseCommandLine(d)
    pgm = P(args.pop(0))
    trig = P(d["-t"])
    args = args if args else None
    if not pgm.exists():
        Error(f"'{pgm}' doesn't exist")
    if not trig.exists():
        xx()
        open(trig, "w").write("")
    Run()

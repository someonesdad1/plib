'''
TODO

    * Capture stdout from each invocation and use option -d
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
    from time import strftime as ft, sleep
if 1:   # Custom imports
    import pdiff
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
    def ManPage():
        print(dedent('''
        If you wish to have ANSI escape codes in your output, get the
        library https://github.com/someonesdad1/plib/blob/main/color.py
        and put it in your PYTHONPATH.

        Suppose we're developing a python script named pgm.py.

        The
        common use case for prun.py is to edit pgm.py in one terminal
        window and run the command 

            python prun.py pgm.py

        in another terminal window.  Then every time the pgm.py script is
        saved by your editor, it is run by the prun.py script.  pgm.py's
        output is sent to stdout and stderr as usual.  If you don't want to
        see stderr output, use the -e option.  If you only want to see
        stderr's output, use the -s option.

        If you use the -d option, you'll see the difference between the
        previous run and the current run shown in your web browser.  This
        difference shows both stdout and stderr mixed together as you'd see
        them on your screen unless you used -e or -s.

        WARNING:  the stdout and stderr streams may not be in the same
        order as if you had run pgm.py from the command line.  This happens
        on the python 3.7 version I'm using even with the -u command line
        argument to unbuffer the streams.

            If your script is doing the printing to stderr, you can
            decorate each line of stderr's output with a leading "+" with a
            function such as 

                def err(*p, **kw):
                    print("+", end="", file=sys.stderr)
                    kw["file"] = sys.stderr
                    print(*p, **kw)

        '''.rstrip()[1:]))
        exit(0)
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
          run when the trigger file's modification time changes.
        Options:
            -c      Clear the screen before running script each time
            -d      Show a diff with previous run in web browser
            -e      Omit stderr (will clear the screen)
            -h      Show more detailed examples of use
            -l      Don't display status line
            -o      Once:  exit after the first run
            -s      Omit stdout (will clear the screen)
            -t f    Define a trigger file f instead of pgm
        '''.rstrip()[1:]))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Clear screen before running script each time
        d["-d"] = False     # Display diff with last capture
        d["-e"] = False     # Omit stderr from capture
        d["-l"] = False     # Don't display status line
        d["-o"] = False     # Exit after first run
        d["-s"] = False     # Omit stdout from capture
        d["-t"] = None      # Trigger file to use
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cdehlost:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cdelos"):
                d[o] = not d[o]
            elif o == "-t":
                d[o] = a
            elif o == "-h":
                ManPage()
        if not args:
            Usage()
        if d["-t"] is None:
            d["-t"] = args[0]   # Trigger on the pgm script
        return args
if 1:   # Core functionality
    def ModTime():
        # This will attempt to get the mod time of the file for up to two
        # seconds, as sometimes it fails on only one try.
        count, n = 0, 10
        for i in range(n):
            try:
                s = trig.stat().st_mtime
            except FileNotFoundError:
                sleep(0.2)
                count += 1
        if count > n:
            raise Exception(f"Couldn't stat {trig}")
        return s
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
    def PrintStartMessage(cmd):
        'Print a starting message'
        ClearScreen()
        print(f"{C.yel}Program invocation:{C.norm}")
        print(f"{C.lblu}{cmd[0]}{C.norm} "
              f"{C.lcyn}{cmd[1]}{C.norm} ", end="")
        if len(cmd) > 2:
            print(f"{C.lmag}{' '.join(cmd[2:])}{C.norm}")
        else:
            print()
        msg = f"{C.lgrn}prun.py {Dt()} {Tm()}{C.norm}"
        print(f"{msg:^{W}s}")
    def Run():
        'Run the python script when trig file has been modified'
        count = 1
        last_stdout, last_stderr = "", ""
        delay = 0.3     # How many seconds between inspections of file
        # Build the command
        cmd = [sys.executable, str(pgm)] + (args if args else [])
        PrintStartMessage(cmd)
        start, modtime = time.time(), ModTime()
        while True:     # Infinite loop
            if modtime == ModTime():
                time.sleep(0.3)
                continue    # File not modified
            # Trigger file was modified, so run the python script
            if d["-c"]:
                ClearScreen()
            modtime = ModTime()     # Latest mod time
            if d["-e"] or d["-s"]:  # Don't capture both streams
                so = se = subprocess.PIPE
                if d["-e"]:
                    se = None
                else:
                    so = None
                # Run the command
                r = subprocess.run(cmd, stdout=so, 
                                   stderr=se, encoding="UTF-8")
                ClearScreen()
                print(r.stderr if se else r.stdout, end="")
                stdout = r.stdout
            else:                   # Capture both streams
                # Run the command
                r = subprocess.run(cmd, stdout=subprocess.PIPE, 
                                   stderr=subprocess.STDOUT, 
                                   encoding="UTF-8")
                print(r.stdout, end="")
            if not d["-l"]:
                Trailer(count, start)
            stdout, stderr = r.stdout, r.stderr
            if stdout is None:
                stdout = ""
            if stderr is None:
                stderr = ""
            if d["-d"]:
                # Show a diff with previous
                n = 10
                s = f"{'='*n}"
                sepo = f"{s} stdout {s}\n"
                sepe = sepo.replace("out", "err")
                # Get strings to compare
                old = sepo + last_stdout + sepe + last_stderr
                new = sepo + stdout + sepe + stderr
                pdiff.ShowDifference(old, new)
                last_stdout, last_stderr = stdout, stderr
            count += 1
            if d["-o"]:
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

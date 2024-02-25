'''
Run shellcheck and organize its output
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Run shellcheck and organize its output
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque, defaultdict
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        if 1:
            import debug
            debug.SetDebugger()
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("brnl") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
        t.warn = t("ornl")
        t.note = t("wht")   
        t.ln = t("magl")    # For line numbers in file
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Run shellcheck on each file and present the results.  Only the lines of the highest 
          severity are printed (e.g., if there are errors and warnings, you'll only see the
          errors).  Lines are printed in reverse numerical order so you can fix the last ones in
          the file first, maintaining the line numbering.
        Options:
            -b      Brief output (shows all serverities)
            -c      Don't ignore my referenced shell colors
            -n n    Limit number of output lines to this number
            -s s    Select shell syntax (s = bash, dash, ksh, sh)
            -v      Turn on debugging
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = False     # Brief output
        d["-c"] = True      # Ignore my referenced shell colors
        d["-n"] = 0         # Limit output lines to this number (0 means all)
        d["-s"] = "bash"    # Default shell syntax (bash dash, ksh, sh), None means to infer
        d["-v"] = False     # Debugging
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "bchn:s:v") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("bcv"):
                d[o] = not d[o]
            elif o == "-n":
                d[o] = int(a)
                if d[o] < 0:
                    Error("-n option's value must be integer >= 0")
            elif o == "-s":
                if a not in "bash dash ksh sh".split():
                    Error(f"{a!r} not allowed (must be in 'bash dash ksh sh')")
                d[o] = a
            elif o == "-h":
                Usage(status=0)
        if d["-v"]:
            g.dbg = True
        GetColors()
        g.W, g.L = GetScreen()
        return files
if 1:   # Classes
    class Errorline:
        '''Provide access to fields of an error line.  Typical example:
          'aa:3:7: error: Remove spaces around = to assign. [SC2290]'
        file        File name 'aa'
        line        String of source file's line with problem
        ln          Line number 3
        column      Problem starts at column 7
        severity    'error:' converted to number
        msg         'Remove spaces around = to assign.' message
        errnum      'SC2290'
        '''
        def __init__(self, line, srcline):
            self._linestr = srcline
            self._fields = line.split()
        def __str__(self):
            return f"Errorline({' '.join(self._fields)})"
        def __repr__(self):
            return str(self)
        @property
        def line(self):
            return self._linestr
        @property
        def file(self):
            return self._fields[0].split(":")[0]
        @property
        def ln(self):
            return int(self._fields[0].split(":")[1])
        @property
        def column(self):
            return int(self._fields[0].split(":")[2])
        @property
        def severity(self):
            s = self._fields[1].replace(":", "")
            return {"error": 1, "warning": 2, "note": 3}[s]
        @property
        def msg(self):
            return ' '.join(self._fields[2:-1])
        @property
        def errnum(self):
            return self._fields[-1].replace("[", "").replace("]", "")
    class Output:
        '''This class encapsulates the output of the shellcheck program for a single file (it
        assumes the output format used is 'gcc').  The core data structure is self.lines, a list of
        Errorline objects constructed from each of the error lines from shellcheck.
        '''
        def __init__(self, file, stdout, stderr):
            '''file is the file's Path object; stdout and stderr are the bytestrings for the output
            of the shellcheck command.  This class will parse the command's output for convenient 
            printing of the output.
            '''
            self.file = file
            self.stdout = stdout
            self.stderr = stderr
            # 1-based numbering of file's lines
            self.filelines = [(i + 1, line) for i, line in enumerate(GetLines(file, nonl=True))]
            # Insert a dummy zeroth line to get desired indexing
            self.filelines = ["zeroth line (should never see)"] + self.filelines
            # Number of digits to print line numbers with 
            self.digits = len(str(self.filelines[-1][0]))
            if 0:
                print(f"Lines of file {str(file)!r}")
                for i, line in self.filelines:
                    print(f"{i:3d}:  {line}")
            # self.lines is a list of shellcheck's output lines, each as an Errorline instance
            self.lines = []
            for line in stdout.decode().split("\n"):
                if line.strip():
                    # Get the line number so we can get the source line
                    ln = int(line.split()[0].split(":")[1])
                    srcline = self.filelines[ln][1] # Remove the line number
                    el = Errorline(line, srcline)
                    if d["-c"] and el.errnum == "SC2154":
                        # This handles my scripts where I have a number of escape codes defined as
                        # shell variables in ~/.bashrc
                        c = el.msg.split()[0]
                        ignore = set('''redd red redl ornd orn ornl grnd grn grnl yeld yel yell
                            magd mag magl trqd trq trql blud blu blul cynd cyn cynl
                            whtd wht whtl gryd gry gryl blk norm'''.split())
                        if c in ignore:
                            continue
                    self.lines.append(Errorline(line, srcline))
            if 0:
                print("Grabbed lines:")
                pp(self.lines)

if 1:   # Core functionality
    def CheckFile(file):
        "Run shellcheck on the file (it's a Path instance) and process the output"
        cmd = ["/usr/bin/shellcheck"]
        cmd += ["--color=never"]        # No ANSI color escape codes in output
        cmd += ["--format=gcc"]         # Use gcc-style output
        cmd += ["-x"]                   # Follow external source statements
        if d["-s"]:
            cmd += [f"--shell={d['-s']}"]    # Define the shell syntax
        cmd += [file]                   # File to process
        r = subprocess.run(cmd, capture_output=True)
        if d["-v"]:
            Dbg(f"file = {str(file)!r}")
            Dbg(f"cmd is {cmd}")
            if r.stdout:
                Dbg("stdout:")
                for i in r.stdout.decode().split("\n"):
                    Dbg(" ", i)
            if r.stderr:
                Dbg("stderr:")
                Dbg(r.stderr)
                for i in r.stderr.decode().split("\n"):
                    Dbg(" ", i)
        if not r.returncode:
            return
        if r.returncode != 1:
            print(f"{t.err}shellcheck invoked with bad syntax or bad option{t.N}")
            print(f" Command = {' '.join(cmd)!r}")
            print(f" stderr:")
            for i in r.stderr.decode().split("\n"):
                print(f"   {i}")
            exit(1)
        ProcessOutput(r.stdout, r.stderr, file)
    def ProcessOutput(stdout, stderr, file):
        '''Note that returncode > 0 and stdout/stderr are bytestrings.  Desired output:
        Print last line numbers first so that fixing the first item output doesn't affect the
        numbering of subsequent notes.
        '''
        o = Output(file, stdout, stderr)
        if d["-b"]:
            BriefReport(o)
        else:
            # Organize by severity:  store each item by severity number
            di = defaultdict(list)
            for i in o.lines:
                di[i.severity].append(i)
            if 1 in di:     # Errors
                PrintReport("error", t.err, di[1])
            elif 2 in di:   # Warnings
                PrintReport("warning", t.warn, di[2])
            elif 3 in di:   # Notes
                PrintReport("note", t.note, di[3])
    def BriefReport(o):
        'o is an Output instance'
        # Decorate a list of by line number and print out in reverse order
        errorlines = [(i.ln, i) for i in o.lines]
        indent, count = " "*2, 0
        # How to select colors by severity
        c = {1: t.err, 2: t.warn, 3: t.note}
        for ln, errorline in reversed(errorlines):
            clr = c[errorline.severity]
            file = errorline.file
            ln = errorline.ln
            col = errorline.column
            msg = errorline.msg
            errnum = errorline.errnum
            t.print(f"{clr}{file}[{ln}]: {msg} {errnum}")
            count += 1
            if d["-n"] and count > d["-n"]:
                break
    def PrintLine(linestr, column, indent):
        '''Print the string linestr with the indicated column marked in color to show where the error
        starts.
        '''
        # Get character position.  Subtract 1 because column numbering is 1-based.
        n = column - 1
        print(f"{indent}{t('whtl')}{linestr[:n]}", end="")
        # Print character at n in highlighted color
        t.print(f"{t('whtl', 'blu')}{linestr[n]}{t.n}{t('whtl')}{linestr[n+1:]}")
    def PrintReport(type, color, errorlist):
        '''type is e.g. 'error', color is the escape code to print the line header, and errorlist
        is the list of Errorline objects with this severity.
        '''
        # Decorate a list by line number and print out in reverse order
        o = [(i.ln, i) for i in errorlist]
        indent, count = " "*2, 0
        for ln, errorline in reversed(o):
            t.print(f"{color}{file}[{t('magl')}{ln}{color}] {type}:")
            if errorline.line:
                PrintLine(errorline.line, errorline.column, indent)
            print(f"{indent}{errorline.msg}")
            count += 1
            if d["-n"] and count > d["-n"]:
                break

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for filename in files:
        file = P(filename)
        if not file.exists():
            t.print(f"{t.err}File {filename!r} does not exist")
        CheckFile(file)

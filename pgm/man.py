"""
ToDo
    - Allow multiple commands on the command line and open them with
      'vi -p'

Python script to help viewing manpages.  Features:

    - Look in g.mandir for cached manpage files.  For example, this lets me have an annotated bash
      manpage that lets me get to needed locations quickly.

    - If not cached, the desired commands have 'man' run on them and the output is put into a
      temporary file.

Use case:

    I use this tool to view manpages on my system.  All of the system's manpages are then viewed
    with my editor, vim.  By appending '.man' to the temporary file opened by the editor, I have an
    autocmd that recognizes this suffix and sets the 'q' key to exit, just as if I was viewing the
    file in a pager like less(1).  The two advantages are that 1) I can use the editor to browse
    the manpage and 2) the manpage's text is colorized by vim's man.vim syntax file.

    The following line in my .vimrc file enables the q key to quit vim:

        autocmd BufRead *.man map q :qall!<cr>

    This tool allows me to put custom manpages in my home directory (see 'mandir' below).  These
    are manpages to tools that I don't want to "pollute" the main system manpage directories with.
    The rule for them to be found and opened is that a) the file name must begin with the same
    string as passed as sys.argv[1] and b) there must only be one argument on the command line
    besides sys.argv[0].

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Python script for viewing manpages with vim
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from pathlib import Path as P
        from pdb import set_trace as xx
        import getopt
        import glob
        import os
        import subprocess
        import sys
        import tempfile
    if 1:  # Custom imports
        from color import t
        from wrap import dedent
        from wsl import wsl
        from lwtest import Assert
    if 1:  # Global variables

        class G:  # Storage for global variables as attributes
            pass

        g = G()
        # UNIX man command location
        g.man = "/usr/bin/man"
        # Where special manpages are located
        if wsl:
            g.mandir = P("/home/don/.manpages")
        else:
            g.mandir = P("/home/Don/bin/man.d")
        Assert(g.mandir.exists())
        # Options to be passed to man
        g.manopts = "--nj"  # --nj is no justification ==> ragged right margins
        # Turns on debugging
        g.dbg = False
        # Collects the files to open in editor
        g.files = set()
        # Temporary files to delete at end of execution
        g.tempfiles = set()
        ii = isinstance
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("gry") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")

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
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] cmd1 [cmd2 ...]
          Generates manpages for the commands and opens them in vi.
        Options:
          -h    Print a manpage
          -v    Verbose debugging output
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-v"] = False  # Verbose debugging output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        if d["-v"]:
            g.dbg = True
        GetColors()
        g.W, g.L = GetScreen()
        Dbg(f"Command line:  {' '.join(sys.argv)!r}")
        # Get the editor (must be vim for things to work)
        try:
            g.editor = os.environ["EDITOR"]
        except KeyError:
            print("EDITOR environment variable is not defined", file=sys.stderr)
            exit(1)
        return args


if 1:  # Core functionality

    def GetManpageFile(cmd):
        """Return the file name to open for this command (it must be a Path instance).  Note:  my
        static man pages have .hld as an extension so that they can have their tags in them
        collated into a tags file and I can use them to jump to the desired location in the text.
        """
        # Either 'cmd.hld' is in g.mandir or we use 'man' to get the content in a temporary file
        p = P(str(g.mandir) + f"/{cmd}.hld")
        Dbg(f"Getting man page file for {cmd!r}")
        if p.exists():
            Dbg(f"  {str(p)!r} exists, so have data")
            return p
        else:
            # Open in a temporary file
            p = P(tempfile.mkstemp(".man")[1])
            g.tempfiles.add(p)
            command = f"man {cmd} >{p}"
            Dbg(f"  Running {command!r}")
            r = subprocess.run(command, shell=True)
            Dbg(f"    Returned {r.returncode}")
            if r.returncode:
                print(f"Failed command:  {command!r}")
                exit(1)
            Dbg(f"    Returning tmp file {str(p)!r}")
            return p

    def OpenFiles(files):
        filelist = " ".join(str(i) for i in files)
        # Assumes vim.  -R means open the files readonly; -p means to run one instance and open the
        # files in separate tab pages.
        cmd = f"{g.editor} -R -p {filelist}"
        Dbg(f"\nOpening file(s) in editor:  {cmd!r}")
        if 1:
            r = subprocess.run(cmd, shell=True)
        else:
            r = G()
            r.returncode = 0
        Dbg(f"  Returned {r.returncode}")
        if r.returncode:
            print(f"Failed command:  {cmd!r}")
            exit(1)


if __name__ == "__main__":
    d = {}  # Options dictionary
    try:
        cmds = ParseCommandLine(d)
        for cmd in cmds:
            Dbg(f"Get manpage for {cmd!r}")
            file = GetManpageFile(cmd)
            Dbg(f"  File to open is {str(file)!r}")
            g.files.add(file)
        OpenFiles(g.files)
    finally:
        # Delete any temporary files
        for i in g.tempfiles:
            try:
                Dbg(f"Deleting {str(i)!r}")
                i.unlink()
            except Exception:
                pass

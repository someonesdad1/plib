'''
ToDo
    - Allow multiple commands on the command line and open them with 
      'vi -p'

Python script to help viewing manpages.  Its two main features are:

    - Look in ~/.local/man.d and if there's a manpage file there that
      begins with the string passed in on the command line, send that
      file to the /usr/bin/man command.  There must only be one
      argument on the command line for this to happen (otherwise, the
      whole command line is sent to the man command).

    - Send the output from the man command to a temporary file and
      open that file with the editor instead of the usual pager.
      Append '.man' to the temporary file's name.

Use case:

    I use this tool to view manpages on my system.  All of the
    system's manpages are then viewed with my editor, vim.  By
    appending '.man' to the temporary file opened by the editor, I
    have an autocmd that recognizes this suffix and sets the 'q' key
    to exit, just as if I was viewing the file in a pager like
    less(1).  The two advantages are that 1) I can use the editor to
    browse the manpage and 2) the manpage's text is colorized by vim's
    man.vim syntax file.

    The following line in my .vimrc file enables the q key to quit
    vim:

        autocmd BufRead *.man map q :q!<cr>:unmap q

    This tool allows me to put custom manpages in my ~/bin/man.d
    directory.  These are manpages to tools that I don't want to
    "pollute" the main system manpage directories with.  The rule for
    them to be found and opened is that a) the file name must begin
    with the same string as passed as sys.argv[1] and b) there must
    only be one argument on the command line besides sys.argv[0].
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Python script for viewing manpages with vim
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import glob
    import os
    import sys
    import tempfile
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from wsl import wsl
if 1:   # Global variables
    # UNIX man command location
    man = "/usr/bin/man"
    # Where special manpages are located
    if wsl:
        mandir = "/home/don/.manpages"
    else:
        mandir = "/home/Don/bin/man.d"
    # Options to be passed to man
    manopts = "--nj"    # --nj is no justification ==> ragged right margins
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] cmdname
      Generates a manpage for cmdname and opens it in vi.
    '''))
    exit(status)
def FindMatchingManpage():
    '''Return either the unique matching filename that begins with the
    string in sys.argv[1] or None.
    '''
    assert(len(sys.argv) == 2)
    cmd = sys.argv[1].strip()
    if cmd:
        olddir = os.getcwd()
        os.chdir(mandir)
        files = glob.glob(cmd + "*")
        os.chdir(olddir)
        if len(files) == 1:
            return files[0]
    return None
if __name__ == "__main__": 
    try:
        editor = os.environ["EDITOR"]
    except KeyError:
        print("EDITOR environment variable is not defined", file=sys.stderr)
        exit(1)
    try:
        # Make a tempfile to hold the generated manpage's text
        tmpfile = tempfile.mkstemp(".man")[1]
        cmdlist = []
        if len(sys.argv) == 1:
            Usage()
        elif len(sys.argv) == 2:
            manfile = FindMatchingManpage()
            if manfile is not None:
                cmdlist = [man, manopts, os.path.join(mandir, manfile),
                           ">%s" % tmpfile]
        use_editor = True
        if not cmdlist:
            if sys.argv[1] == "-k":
                use_editor = False
                cmdlist = [man, manopts] + sys.argv[1:]
            else:
                cmdlist = [man, manopts] + sys.argv[1:] + [">%s" % tmpfile]
        status = os.system(' '.join(cmdlist))
        if status:
            print("man command failed")
            exit(1)
        if use_editor:
            cmdlist = [editor, tmpfile]
            os.system(' '.join(cmdlist))
    finally:
        try:
            if os.path.isfile(tmpfile):
                os.unlink(tmpfile)
        except Exception as e:
            msg = str(e)
            print(dedent(f'''
            Couldn't remove tempfile '{tmpfile}':
              '{msg}'
            ''', file=sys.stderr))
            exit(1)
    exit(0)

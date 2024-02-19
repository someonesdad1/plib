'''
TODO

- Vision
    - Primary purpose
        - Quickly get a picture of a git repository directory's state
        - Output looks like that of ls
        - Color is used to flag important facts
            - lip is an uncommitted change
            - grn is a newly-added file
            - trq is a renamed file

    - My main use case for this command is when I'm in a directory of a git repository, I want to
      quickly get a picture of the directory's state:
        - Files in repository:  M, T, A, D, R, C, U letters from status command used to color the
          individual files.  I primarily want to know M A D R.
            - ?     Untracked
            - !     Ignored
            - M     Modified
            - A     Added
            - D     Deleted
            - R     Renamed
            - T     File type changed (regular file, symlink, submodule)
    - Add the -r option to descend into subdirectories
    - I'd also like to see a recursive listing of all untracked files that are not ignored.  This
      is because I could have forgotten to add some to the repository.



Show git repository file status for current directory
    git status:
        -u Show untracked files
        --ignored
    
        -s Short format
    
    Gets XY code:
        ' ' = unmodified
        M = modified
        T = file type changed (regular file, symbolic link or submodule)
        A = added
        D = deleted
        R = renamed
        C = copied (if config option status.renames is set to "copies")
        U = updated but unmerged
    
        X          Y     Meaning
        -------------------------------------------------
                 [AMD]   not updated
        M        [ MTD]  updated in index
        T        [ MTD]  type changed in index
        A        [ MTD]  added to index
        D                deleted from index
        R        [ MTD]  renamed in index
        C        [ MTD]  copied in index
        [MTARC]          index and work tree matches
        [ MTARC]    M    work tree changed since index
        [ MTARC]    T    type changed in work tree since index
        [ MTARC]    D    deleted in work tree
                    R    renamed in work tree
                    C    copied in work tree
        -------------------------------------------------
        D           D    unmerged, both deleted
        A           U    unmerged, added by us
        U           D    unmerged, deleted by them
        U           A    unmerged, added by them
        D           U    unmerged, deleted by us
        A           A    unmerged, both added
        U           U    unmerged, both modified
        -------------------------------------------------
        ?           ?    untracked
        !           !    ignored
        -------------------------------------------------
    ?? means untracked
    !! means ignored

---------------------------------------------------------------------------
Notes from lsg.py outline:

    Script to list status of git repository's files

    - Need a tool for git that lists files like lsh
        - Key states:  clean, modified (staged, not stages), ignored, not
        tracked, deleted, added but not checked in 
        - Color codes the states
        - Default report shows staged, not staged in current directory
            - Need -r to see at and below current directory
        - Branch and root of repository always shown at end
    - Options

        - -a    Show all
        - -i    Show ignored
        - -c    Show unchanged but tracked
        - -r    Recursive
        - -w    Show whole repository state

    - Also use output of 'git shortlog -sn' for repository names
    - Primary use cases
        - Show the untracked files
        - Show directories that have no repository files (one of the
            easiest ways to do this is to put a .git directory in that
            directory; this also makes it trivial to find that it's not
            part of the parent repository).
        - Short listing of types:  M (modified), T (type changed), A
            (added), D (deleted), R (renamed), C (copied), U (updated but
            unmerged)
            - XY table:  M in X position means modified and staged for
                commit (in index); in Y means changed and not in index
    - Root location of repository shown (must be in a subdirectory of
        the directory holding the repository .git directory)
    - 'git status -u --porcelain' shows untracked files and directories
    - 'git status --ignored --porcelain' shows ignored stuff
    - Use --branch to get current branch headers in porcelain format 2
    - Color code the different states
        - red:   deleted
        - orn:   untracked
        - grn:   tracked, unchanged
        - mag:   tracked, changed
        - gryl:  ignored
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
    # Show git repository file status
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    from enum import Enum, auto
    import getopt
    import os
    import pathlib
    import subprocess
    import sys
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from color import TRM as t
    from columnize import Columnize
    from wsl import wsl     # wsl is True if we're running under WSL
    from dpprint import PP
    pp = PP()
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    dbg = False
    class St(Enum):
        # States for git status -s forms
        unmodified = auto()
        modified = auto()
        added = auto()
        deleted = auto()
        renamed = auto()
        unmerged = auto()
        untracked = auto()
        ignored = auto()
    # Map state to name and color
    sc = {
        St.ignored: ["Ignored", t("gry")],          # ?
        St.unmodified: ["Unmodified", t("wht")],    # ''
        St.untracked: ["Untracked", t("ornl")],     # !
        St.unmerged: ["Unmerged", t("cynl")],       # u
        St.renamed: ["Renamed", t("yel")],          # r
        St.added: ["Added", t("mag")],              # a
        St.deleted: ["Deleted", t("lip")],          # d
        St.modified: ["Modified", t("grnl")],       # m
    }
    if wsl:
        git = "/usr/bin/git"
    else:
        git = "c:/bin/git_2_35_1_2/bin/git.exe"     # cygwin's git
if 1:   # Utility
    def NoColor():
        global sc
        sc = {
            St.ignored: ["Ignored", ""],            # ?
            St.unmodified: ["Unmodified", ""],      # ''
            St.untracked: ["Untracked", ""],        # !
            St.unmerged: ["Unmerged", ""],          # u
            St.renamed: ["Renamed", ""],            # r
            St.added: ["Added", ""],                # a
            St.deleted: ["Deleted", ""],            # d
            St.modified: ["Modified", ""],          # m
        }
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [dir]
          If directory dir is in a git repository, show the state of the files
          at and below dir.  dir defaults to '.'.
        Options:
            -a      Show for the whole repository
            -d      Turn on debugging output
            -c      No color escape codes in output
            -h      Print a manpage
            -i      Show ignored files
            -v      Don't show cwd & root
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Allow everything to be shown
        d["-c"] = True      # Color
        d["-d"] = False     # Turn on debugging output
        d["-i"] = False     # Show ignored files
        d["-v"] = True      # Verbose
        try:
            opts, dir = getopt.getopt(sys.argv[1:], "acdhiv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acdiv"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if d["-d"]:
            global dbg
            dbg = True
        dir = dir if dir else "."
        if not d["-c"]:
            NoColor()
        return dir
    def Dbg(*p, **kw):
        if not dbg:
            return
        seq = kw.get("seq", False)
        ind = kw.get("ind", "")
        if "ind" in kw:
            del kw["ind"]
        if seq:
            for i in p[0]:
                print(f"{ind}{t('cyn')}{i}{t.n}")
        else:
            print(f"{t('cyn')}", end="")
            if "end" not in kw:
                kw["end"] = ""
            print(ind, end="")
            print(*p, **kw)
            print(f"{t.n}")
if 1:   # Core functionality
    def GetGitRoot():
        'Return the root of the repository or None'
        # https://stackoverflow.com/questions/15715825/how-do-you-get-the-git-repositorys-name-in-some-git-repository
        cmd = [git, "rev-parse", "--show-toplevel"]
        cp = subprocess.run(cmd, capture_output=True)
        if cp.returncode == 128:
            print(f"Not in a git repository")
            exit(1)
        elif cp.returncode:
            print(f"Git rev-parse command returned {cp.returncode}")
            exit(1)
        s = cp.stdout.decode()
        # Convert to a POSIX name
        if not wsl:
            cmd = ["/usr/bin/cygpath", s]
            cp = subprocess.run(cmd, capture_output=True)
        p = cp.stdout.decode().rstrip()
        return p
    def GetData(dir):
        '''Change to the repository's root directory to run the status command.
        This will result in a list of files relative to the root.  Then select
        only the files that are in dir or below.
        '''
        def Split(s):
            '''Split into two chunks at position 2.  Input is in the form
                'xy name' where x and y are letters or space characters.
            '''
            return s[:2], P(s[2:].strip()).resolve()
        # Change our directory to the repository root so that x.resolve() works
        root = GetGitRoot()
        cwd = os.getcwd()
        os.chdir(root)
        # Run the git status command
        ind = " "*2
        cmd = [git, "status", "-uall", "-s"]
        # The porcelain option intends to keep the output format guaranteed
        # for uniform behavior in scripts.
        cmd = [git, "status", "-uall", "-s", "--porcelain"]
        cmd = [git, "status", "-uall", "-s", "--porcelain", "--ignored"]
        cp = subprocess.run(cmd, capture_output=True)
        if cp.returncode == 128:
            print(f"Not in a git repository")
            exit(1)
        elif cp.returncode:
            print(f"Git status command returned {cp.returncode}")
            exit(1)
        lines = [i.rstrip() for i in cp.stdout.decode().rstrip().split("\n")]
        if dbg:
            Dbg("Raw string")
            Dbg(repr(cp.stdout.decode()), ind=ind)
            Dbg("Raw lines")
            Dbg(lines, seq=True, ind=ind)
        # Each line will be of the form 'XY filename' where XY are the
        # letters in the docstring and note that X can be a space
        # character.  Split into two status letters and an absolute Path
        r = [Split(i) for i in lines]
        if dbg:
            Dbg("After splitting data")
            Dbg(r, seq=True, ind=ind)
        # Change back to original directory
        os.chdir(cwd)
        # Filter out unwanted stuff
        r = [i for i in r if Keep(i)]
        if dbg:
            Dbg("\nAfter filtering")
            Dbg(r, seq=True, ind=ind)
        r = [(i.strip(), j) for i, j in r]
        if dbg:
            Dbg("\nAfter stripping first item")
            Dbg(r, seq=True, ind=ind)
        # Change paths to be relative to dir
        rr = []
        for i, j in r:
            try:
                a = j.relative_to(dir)
                rr.append((i, a))
            except Exception:
                # This means we ignore files e.g. in the parent directory
                pass
        r = rr
        if dbg:
            Dbg(f"\nMade relative to '{dir}'")
            Dbg(r, seq=True, ind=ind)
        return r
    def Keep(x):
        '''x is a tuple of (str, Path).  Return True if the Path should be
        shown in the listing.

        This will be the case if x[1].relative_to(dir) doesn't raise an
        exception.
        '''
        if not ii(x[1], pathlib.Path):
            raise Exception("'{x[1]}' is not a pathlib.Path object")
        p = x[1].resolve()
        # Don't keep directories
        if p.is_dir():
            return False
        # Keep everything if -a option used
        if d["-a"]:
            return True
        # It must be relative to dir
        return str(p).startswith(str(dir))
    def ProcessData(r):
        '''r will be tuples of ("XY", "name").  Return a dict of the changed
        data.  Keys will be the lowercase change code (e.g. "m" for
        modified) and values will be the list of file names.
        '''
        # Put into dict by type
        di = defaultdict(list)
        for code, name in r:
            key = code.lower()
            di[key] += [name]
        if dbg:
            Dbg("\nPut into dict")
            Dbg(di.items(), seq=True)
        # Change the keys to the state enums
        n, remove = {}, []
        for key, val in di.items():
            if not key:
                n[St.unmodified] = val
            elif key[0] == "?":
                n[St.untracked] = val
            elif key[0] == "m":
                n[St.modified] = val
            elif key[0] == "a":
                n[St.added] = val
            elif key[0] == "d":
                n[St.deleted] = val
            elif key[0] == "r":
                n[St.renamed] = val
            elif key[0] == "u":
                n[St.unmerged] = val
            elif key[0] == "!":
                n[St.ignored] = val
            remove.append(key)
        for i in remove:
            del di[i]
        # Make sure we've processed all elements
        assert(not di)
        if 0:
            Dbg("\nContents of n")
            for i in n:
                print(i)
                pp(n[i])
            Dbg()
        return n
    def ShowRoot():
        'Show the repository root and current directory in color'
        w = 20
        print(f"{'Repository root:':{w}s}", end="")
        if d["-c"]:
            print(f"{t('whtl', 'blu')}", end="")
        print(GetGitRoot(), end="")
        if d["-c"]:
            print(f"{t.n}", end="")
        print()
        print(f"{'Current directory:':{w}s}", end="")
        if d["-c"]:
            print(f"{t('whtl', 'red')}", end="")
        print(dir.relative_to(root), end="")
        if d["-c"]:
            print(f"{t.n}", end="")
        print()
    def PrintReport(di):
        for key in sc:  # This gets us the print order we want
            if key in di and len(di[key]):
                if len(di[key]) == 1 and not di[key][0]:
                    continue
                if key == St.ignored and not d["-i"]:
                    continue
                name, clr = sc[key]
                print(f"{clr}{name}")
                try:
                    for i in Columnize(di[key], indent=" "*2):
                        print(i)
                except ValueError:
                    # It's probably a line too long problem, so just
                    # dump the strings; not pretty, but at least it works.
                    for i in di[key]:
                        #print(i, end=" ")
                        print(f"  {i}")
                    print()
                print(f"{t.n}", end="")
if __name__ == "__main__":
    d = {}      # Options dictionary
    if 1:   # Setup
        args = ParseCommandLine(d)
        dir = P(args[0]).resolve()  # First argument on command line (default '.')
        root = GetGitRoot()
        if root is None:
            print("Not in git repository")
            exit(1)
        if d["-v"]:
            ShowRoot()
        Dbg(f"dir = {dir}")
    r = GetData(dir)
    di = ProcessData(r)
    PrintReport(di)

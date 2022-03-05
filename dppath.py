'''
Path utilities (all paths are pathlib.Path objects)
    RemoveDirs      Remove directories from a sequence that match a pattern
    RemoveFiles     Remove filenames from a sequence that match a pattern
    RemoveVCDir     Remove version control directories
    Get             Get all files and directories
    GetFiles        Return a recursive list of files
    GetDirs         Return a recursive list of directories
    KeepOnlyDirs    Keep only the directories in a list
    KeepOnlyFiles   Keep only the files in a list
    IsVCDir         Return True if dir is a version control directory
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> A number of utilities that deal with pathlib Paths
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    from collections import deque, defaultdict
    import pathlib
    import re
    import sys
    from itertools import filterfalse
    from pdb import set_trace as xx 
    from pprint import pprint as pp
if 1:   # Custom imports
    from columnize import Columnize
    if 1:
        import debug
        debug.SetDebugger()
if 1:  # Global variables
    ii = isinstance
    P = pathlib.Path
def Remove(pathseq, match=[], search=[], ic=False, dir=False):
    '''Return the items in the sequence pathseq of pathlib.Path objects
    with the patterns in the lists match and search removed.  Those in
    match must match fully and those in search can match anywhere in the
    path's components.  The patterns are strings and are compiled with
    re.compile().  If ic is True, then they are compiled with re.I to
    ignore case.  A path is removed in pathseq if any match or search
    pattern is a match.  Do not include '^' or '$' anchors in the match
    strings because they will be added.  The matching/searching is only
    done on the directory components of the items in pathseq if dir is
    True; otherwise, the matching is on the file name component only.

    '''
    if not match and not search:
        return pathseq
    # Build our regular expressions
    M, S = "", ""
    if match:
        a = []
        for i in match:
            a.append(f"^{i}$")
        M = re.compile('|'.join(a), re.I if ic else 0)
    if search:
        a = []
        S = re.compile('|'.join(search), re.I if ic else 0)
    input, output = deque(pathseq), deque()
    # Process the sequence
    while input:
        p = input.popleft()
        if not ii(p, P):
            raise ValueError(f"'{p}' is not a pathlib.Path object")
        p = p.resolve()
        if dir:
            parts = p.parts[:-1] if p.is_file() else p.parts
        else:
            if p.is_dir():
                continue
            parts = [p.parts[-1]]   # File name portion
        match_found, search_found = False, False
        if M:
            found = False
            for part in parts:
                if M.match(part):
                    found = True
                    break
            if found:
                continue
        if S:
            found = False
            for part in parts:
                if S.search(part):
                    found = True
                    break
            if found:
                continue
        output.append(p)
    return list(output)
def RemoveDirs(pathseq, match=[], search=[], ic=False):
    'Remove directories using Remove()'
    return Remove(pathseq, match=match, search=search, ic=ic, dir=True)
def RemoveVCDir(pathseq):
    'Remove git, Mercurial, Bazaar, and RCS directories'
    m = ["\\.git", "\\.hg", "\\.bzr", "RCS"]
    return Remove(pathseq, match=m, dir=True)
def RemoveFiles(pathseq, match=[], search=[], ic=False):
    'Remove files using Remove()'
    return Remove(pathseq, match=match, search=search, ic=ic, dir=False)
def Get(*dirs, recursive=False):
    '''Return a list of files and directories from the indicated
    directories.  If recursive is True, do so recursively.  All objects
    returned in the list are pathlib.Path objects.
    '''
    seq = []
    for dir in dirs:
        p = P(dir)
        if not p.is_dir():
            continue
        seq += p.rglob("*") if recursive else p.glob("*")
    return list(sorted(set(seq)))
def GetFiles(*dirs, include_vc=False, recursive=False):
    '''Return a sorted sequence of file objects for the indicated
    directories.  If include_vc is True, include version control
    directories.  If recursive is True, do so recursively.
    '''
    f, g = lambda x: P(x).is_file(), lambda x: list(sorted(set(x)))
    seq = g(filter(f, Get(*dirs, recursive=recursive)))
    return seq if include_vc else RemoveVCDir(seq)
def GetDirs(*dirs, include_vc=False, recursive=False):
    '''Return a sorted sequence of directory objects for the indicated
    directories.  If include_vc is True, include version control
    directories.  If recursive is True, do so recursively.
    '''
    f, g = lambda x: P(x).is_dir(), lambda x: list(sorted(set(x)))
    seq = g(filter(f, Get(*dirs, recursive=recursive)))
    return seq if include_vc else RemoveVCDir(seq)
def KeepOnlyDirs(pathseq):
    return list(filter(lambda x: P(x).is_dir(), pathseq))
def KeepOnlyFiles(pathseq):
    return list(filter(lambda x: P(x).is_file(), pathseq))
def IsVCDir(dir):
    'Return True if dir is in a version control directory tree'
    if not hasattr(IsVCDir, "vc"):
        IsVCDir.vc = set((".bzr", ".git", ".hg", ".svn", "RCS"))
    for i in dir.parts:
        if i in IsVCDir.vc:
            return True
    return False

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    import math
    import os
    from sig import sig
    def Test_GetDirs():
        dirs = GetDirs("/plib")
        Assert(ii(dirs, list))
        # These two directories are present for sure.  Others may be
        # present, but they're aren't core at the moment.
        for i in "/plib/pgm /plib/test".split():
            assert(P(i) in dirs)
        Assert(list(sorted(set(dirs))) == dirs)     # No duplicates
    def Test_GetFiles():
        files = GetFiles("/plib")
        Assert(ii(files, list))
        for i in '''/plib/e.py /plib/sig.py /plib/eia.py /plib/sigfig.py
                    /plib/elliptic.py /plib/sizes.py /plib/enc.py
                    /plib/states.py /plib/enc_codecs.csv'''.split():
            Assert(P(i) in files)
        Assert(list(sorted(set(files))) == files)   # No duplicates
    def Test_Remove():
        pathseq = [P(i) for i in '''/plib/e.py /plib/sig.py /plib/eia.py
                    /plib/sigfig.py /plib/elliptic.py /plib/sizes.py
                    /plib/enc.py /plib/states.py
                    /plib/enc_codecs.csv'''.split()]
        # Remove all items that have a directory that starts with 'p'
        s = RemoveDirs(pathseq, match=["p.*"])
        Assert(not s)
        # Remove files that contain 'i' or 'l'
        s = RemoveFiles(pathseq, search=["i", "l"])
        t = [P(i) for i in '''/plib/e.py /plib/enc.py /plib/states.py
                    /plib/enc_codecs.csv'''.split()]
        Assert(s == t)
    def Test_RemoveVCDir():
        dirs = KeepOnlyDirs(Get("/plib"))
        Assert(P("/plib/.git") in dirs)
        dirs = RemoveVCDir(dirs)
        Assert(P("/plib/.git") not in dirs)
    exit(run(globals(), regexp="^Test", halt=1)[0])

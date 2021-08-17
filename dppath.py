'''
Path utilities
    RemoveDirs      Remove directories from a sequence that match a pattern
    RemoveFiles     Remove filenames from a sequence that match a pattern
    RemoveVCDir     Remove version control directories
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
if 1:  # Global variables
    ii = isinstance
    P = pathlib.Path
def Remove(seq, match=[], search=[], ic=False, dir=False):
    '''Return the items in the sequence seq with the patterns in the lists
    match and search removed.  Those in match must match fully and those in
    search can match anywhere in the path's components.  The patterns are
    strings and are compiled with re.compile().  If ic is True, then they
    are compiled with re.I to ignore case.  A path is removed in seq if any
    match or search pattern is a match.  Do not include '^' or '$' anchors
    in the match strings because they will be added.  The
    matching/searching is only done on the directory components of the
    items in seq if dir is True; otherwise, the matching is on the file
    name component only.
    '''
    if not match and not search:
        return seq
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
    input, output = deque(seq), deque()
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
def RemoveDirs(seq, match=[], search=[], ic=False):
    return Remove(seq, match=match, search=search, ic=ic, dir=True)
def RemoveVCDir(seq):
    'Remove git, Mercurial, Bazaar, and RCS directories'
    m = ["\\.git", "\\.hg", "\\.bzr", "RCS"]
    return Remove(seq, match=m, dir=True)
def RemoveFiles(seq, match=[], search=[], ic=False):
    return Remove(seq, match=match, search=search, ic=ic, dir=False)

if 1:
    f = lambda x:  [str(i) for i in x]
    seq = [i.resolve() for i in P(".").glob("c*")]
    seq = [i for i in seq if i.is_file()]
    m = []
    s = ["or"]
    before = set(f(seq))
    print("Before: ", ' '.join(before))
    t = RemoveFiles(seq, search=s)
    after = set(f(t))
    print("\nAfter: ", ' '.join(after))
    print("\nRemoved: ", ' '.join(before - after))
    exit()

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    import math
    import os
    from sig import sig
    def Test_me():
        pass
    exit(run(globals(), regexp="^Test", halt=1)[0])

'''
Path utilities
    Remove          Remove files from a sequence that match a pattern
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
if 1:  # Global variables
    ii = isinstance
    P = pathlib.Path
def RemoveDir(seq, match=[], search=[], ic=False):
    '''Return the items in the sequence seq with the patterns in the lists
    match and search removed.  Those in match must match fully and those in
    search can match anywhere in the path's components.  The patterns are
    strings and are compiled with re.compile().  If ic is True, then they
    are compiled with re.I to ignore case.  A path is removed in seq if any
    match or search pattern is a match.  Do not include '^' or '$' anchors
    in the match strings because they will be added.  The
    matching/searching is only done on the directory components of the
    items in seq.
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
    while input:
        p = input.popleft()
        if not ii(p, P):
            raise ValueError(f"'{p}' is not a pathlib.Path object")
        p = p.resolve()
        parts = p.parts[:-1] if p.is_file() else p.parts
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
                if M.search(part):
                    found = True
                    break
            if found:
                continue
        output.append(p)
    return list(output)

if 1:
    from columnize import Columnize
    seq = list(P(".").glob("*"))
    seq = [i for i in seq if i.is_dir()]
    from pprint import pprint as pp
    m = ["[t].*"]
    s = []
    t = RemoveDir(seq, match=m, search=s, ic=True)
    for i in Columnize([str(j) for j in t]):
        print(i)
    exit()

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    import math
    import os
    from sig import sig
    def Test_me():
        pass
    exit(run(globals(), regexp="^Test", halt=1)[0])

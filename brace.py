'''
Perform brace expansion similar to that done in modern shells.  Note that
numerical sequences aren't part of the syntax.
'''

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the GNU Free Documentation License 1.2
    #∞license∞#
    #∞what∞#
    # <utility> Function to perform brace expansion similar to modern
    # shells.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
def BraceExpansion(s):
    '''Return a list of the items indicated by the string s.  Examples:
 
    * BraceExpansion("{a,b}/*.{jpg,png}") returns
        ['a/*.jpg', 'a/*.png', ' b/*.jpg', ' b/*.png']
    * BraceExpansion("{,a}/{c,d}") returns
        ['/c', '/d', 'a/c', 'a/d']
    * BraceExpansion(r"{,,a}/{c,d}") returns
        ['/c', '/d', '/c', '/d', 'a/c', 'a/d']
    '''
    # From http://rosettacode.org/wiki/Brace_expansion
    # The web page's content is available under the GNU Free
    # Documentation license 1.2.
    def getitem(s, depth=0):
        out = [""]
        while s:
            c = s[0]
            if depth and (c == ',' or c == '}'):
                return out,s
            if c == '{':
                x = getgroup(s[1:], depth + 1)
                if x:
                    out, s = [a+b for a in out for b in x[0]], x[1]
                    continue
            if c == '\\' and len(s) > 1:
                s, c = s[1:], c + s[1]
            out, s = [a+c for a in out], s[1:]
        return out, s
    def getgroup(s, depth):
        out, comma = [], False
        while s:
            g, s = getitem(s, depth)
            if not s:
                break
            out += g
            if s[0] == '}':
                if comma:
                    return out, s[1:]
                return ['{' + a + '}' for a in out], s[1:]
            if s[0] == ',':
                comma, s = True, s[1:]
        return None
    return getitem(s)[0]

if __name__ == "__main__": 
    from lwtest import run
    from itertools import product
    from pdb import set_trace as xx
    def TestSimple():
        s = ' '.join(BraceExpansion("a{d,c,b}e"))
        t = "ade ace abe"
        assert(s == t)
    def TestCartesianProduct():
        s = ' '.join(BraceExpansion("{a,b,c}{d,e,f}"))
        t = ' '.join([i + j for i, j in product("abc", "def")])
        assert(s == t)
        s = str(BraceExpansion("{a,b}/*.{jpg,png}"))
        t = "['a/*.jpg', 'a/*.png', 'b/*.jpg', 'b/*.png']"
        assert(s == t)
    def TestNested():
        s = ' '.join(BraceExpansion("{,a}{b,{c,d},e}"))
        t = "b c d e ab ac ad ae"
        assert(s == t)
    exit(run(globals())[0])


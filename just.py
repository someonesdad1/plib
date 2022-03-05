'''
TODO

* Need two spaces after ., : and end of quoted sentences like ?",
  .", !", etc.  Need to handle abbreviations for these cases too.

* PNP shows numerous sentence endings or places that would be good for
  an extra space:
    ?"    ."    !"    ,"    .'"    ,'    ;"    :"


Comments:  the algorithm works, but I think I'd rather see random
location of the extra spaces rather than starting at the beginning of
the line.  Justify PNP to 79 spaces and you'll see why.

'''
#∞test∞# ignore #∞test∞#
if 1:
    from pdb import set_trace as xx 
    from collections import deque, defaultdict
    from abbreviations import IsAbbreviation
    from columnize import Columnize
    from dpstr import KeepFilter
    from io import StringIO
    from pprint import pprint as pp
    import string
    import random
    punctuation = set(string.punctuation)
    letters = set(string.ascii_letters)
    letters.update(set("_-"))
    ii = isinstance

def JustifyParagraph(s, L):
    'Block justify string s into length L and return it'  
    # Modified by DP; the original algorithm had a couple of bugs that
    # show up when you test at corner cases like L == 1.  Also added
    # extra stuff for end of sentence and colon.
    # From https://medium.com/@dimko1/text-justification-63f4cda29375
    f = lambda x, y: x.endswith(y)
    out, line, num_of_letters = [], [], 0
    for w in s.split():
        if (not IsAbbreviation(w) and 
                (f(w, ".") or f(w, "!") or f(w, "?") or f(w, ":"))):
            w = w + " "
        if num_of_letters + len(w) + len(line) > L:
            spaces_to_add = max(L - num_of_letters, 0)
            # The following avoids a divide by zero when L is small
            ws_amount = max(len(line) - 1, 1)
            for i in range(spaces_to_add):
                # When L is small, line can be empty and the
                # mod results in an exception
                if line:
                    line[i % ws_amount] += ' '
            out.append(''.join(line))
            line, num_of_letters = [], 0
        line.append(w)
        num_of_letters += len(w)
    # I want last line to not have trailing spaces
    out.append(' '.join(line))
    return '\n'.join(out)
def Justify(s, L, brk="\n\n"):
    '''Block justify the paragraphs in string s and return them.  The
    paragraphs are separated by the string brk.
    '''
    paragraphs = [JustifyParagraph(i, L) for i in s.split(brk)]
    return brk.join(paragraphs)

if 1:
    s = open("pnp").read()
    print(Justify(s, 79000), end="")
    exit()

if 0:
    keep = KeepFilter(punctuation)
    s = open("big.txt").read()
    TokenEnds(s)
    exit()

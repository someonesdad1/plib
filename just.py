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
def Justify1(s, L):
    'Block justify string s into length L'
    # The original algorithm has a couple of bugs that show up when you
    # test at corner cases like L == 1.
    orig = False    # If True, use original algorithm
    # From https://medium.com/@dimko1/text-justification-63f4cda29375
    words = s.split()
    out, line, num_of_letters = [], [], 0
    for word in words:
        if num_of_letters + len(word) + len(line) > L:
            num_of_spaces = L - num_of_letters
            if orig:
                words_amount = len(line) - 1 
            else:
                # The following avoids a divide by zero when L is small
                words_amount = max(len(line) - 1, 1)
            for i in range(num_of_spaces):
                if orig:
                    line[i % words_amount] += ' '
                else:
                    # When L is small, line can be empty and the
                    # original code results in an exception
                    if line:
                        line[i % words_amount] += ' '
            out.append(''.join(line))
            line, num_of_letters = [], 0
        line.append(word)
        num_of_letters += len(word)
    if orig:
        out.append(' '.join(line).ljust(L))
    else:
        # I want last line to not have extra trailing spaces
        out.append(' '.join(line))
    return out
def TokenEnds(s):
    '''Print out the tokens that end in " or '
    '''
    show = set(''' !" ?" ." ," ;"      !' ?' .' ,' ;' '''.split())
    o = defaultdict(list)
    for ln, line in enumerate(s.split("\n")):
        for token in line.split():
            if token.endswith("'") or token.endswith('"'):
                t = deque(token)
                while t and t[0] in letters:
                    t.popleft()
                o[''.join(t)].append(ln + 1)
    for i in o:
        print(f"{i:10s} {o[i][0]}")

class Block:
    def __init__(self, sent=2):
        'sent is the number of spaces at end of sentence'
        self.sent = sent
        self.sentinels = deque([0x204b, 0x2188, 0x2187, 0xbeef, 0x2588])
    def get_sentinel(self, s):
        for sentinel in self.sentinels:
            if chr(sentinel) not in s:
                return chr(sentinel)
        raise ValueError("Can't get sentinel")
    def space_word(self, word):
        '''Return word with a space.  If it's of special type (ending a
        sentence or with a colon), return with two spaces.
        '''
        sp = " "
        wws = word + sp
        if word.endswith(".") and not IsAbbreviation(word) and self.sent > 1:
            return wws + sp
        elif word.endswith(":"):
            return wws + sp
        for k in '''! ? !' ?' !" ?"'''.split():
            if word.endswith(k) and self.sent > 1:
                return wws + sp*(self.sent - 1)
        return wws
    def ln(self, x):
        'Return length of x joined with last word rstripped'
        return len(''.join(x).rstrip())
    def justify_x(self, s, L):
        'Return the string s block justified to width L'
        # Algorithm:  Split s into words and append a space to all words
        # that need it (end with colon, end with period if not an
        # abbreviation, end with !, ?, !", ?", !', or ?').
        words = deque([self.space_word(i) for i in s.split()])
        out, line = deque(), deque()
        while words:
            while self.ln(line) < L:
                next_word_length = len(words[0].rstrip())
                if self.ln(line) + next_word_length <= L:
                    line.append
                if words:
                    word = self.space_word(words.popleft())
                    nxtlen = len(words[0]) + 1
                    if ln(line) + nxtlen < L:
                        word = words.popleft()
                        line.append(word + " ")
                    else:
                        print(''.join(line))
                        line = deque()
                        continue
            while ln(line) < L:
                line.append(" ")
            print(''.join(line))
            line = deque()
    def space_sentinel(self, word, sentinel):
        '''Return word with a sentinel.  If it's of special type (ending a
        sentence or with a colon), return with two or more sentinels if
        self.sent is > 1.
        '''
        wws = word + sentinel
        if word.endswith(".") and not IsAbbreviation(word) and self.sent > 1:
            return wws + sentinel
        elif word.endswith(":"):
            return wws + sentinel
        for k in '''! ? !' ?' !" ?"'''.split():
            if word.endswith(k) and self.sent > 1:
                return wws + sentinel*(self.sent - 1)
        return wws
    def justify(self, s, L):
        'Return the string s block justified to width L'
        # Algorithm:  Construct the string s with proper spaces and no
        # line breaks.  Put sentinel characters in instead of spaces.
        # Then find the next line by chopping at sentinel characters,
        # padding with spaces as needed to get length L.
        sentinel = self.get_sentinel(s)
        words = deque([self.space_sentinel(i, sentinel) for i in s.split()])
        big = ''.join(words)
        pp(big)

if 1:
    s = '''
    It is a truth universally acknowledged, that a Mr. single man: in possession
    of a good fortune, must be in want of a wife.
    '''
    b = Block()
    t = b.justify(s, 20)
    #for line in t.split("\n"):
    #    print(repr(line))
    exit()

if 0:
    keep = KeepFilter(punctuation)
    s = open("big.txt").read()
    TokenEnds(s)
    exit()

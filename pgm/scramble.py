'''

Scramble the letters of plain text.  An option lets you leave the first and
last letters of a word alone.  Each file on the command line is processed
in sequence, sending the processed text to stdout.  If no files are given,
stdin is read.

Algorithm

- Choose a character X not in text to split on
- Read in the string
- Create a list containing (offset, char) for each punctuation/space character.
- Replace each punctuation/space character with X.
- Split into words on X characters.
- Scramble the letters in each word.
- Re-insert the X characters.
- Reinsert the punctuation/space characters.

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Scramble the letters of plain text files.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from pprint import pprint as pp
        import random
        import string
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from asciify import Asciify
        import ruler
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        punctuation = set(string.punctuation + " ")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
          Scramble the letters in words of the text files.  Use '-' to read
          from stdin.
        Options:
            -a      'ASCIIfy' the file by changing Unicode characters to
                    their ASCII equivalents.
            -f      Leave the first and last letters alone.
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # ASCIIfy the input file(s)
        d["-f"] = False     # Leave first and last letters alone
        d["-s"] = None      # Seed for random number generator
        try:
            opts, files = getopt.getopt(sys.argv[1:], "afhs:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("af"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
            elif o == "-s":
                d[o] = a
        if not files:
            Usage()
        return files
if 1:   # Core functionality
    def Scramble(word):
        # If short word, don't bother
        n = 4 if d["-f"] else 3
        if len(word) < n:
            return word
        # OK, needs scrambling
        w = list(word)
        if d["-f"]:
            first, last = w[0], w[-1]
            w = w[1:-1]
        random.shuffle(w)
        if d["-f"]:
            w.insert(0, first)
            w.append(last)
        return ''.join(w)
    def ProcessFile(file):
        s = sys.stdin.read() if file == "-" else open(file).read()
        if d["-a"]:
            s = Asciify(s)
        dbg = True #xx
        if dbg: #xx
            s = '"Yes", said A.'
        N = len(s)  # String length invariant
        # Find a character X that is not in string
        found = False
        #for i in range(0x258f, 0x2587, -1):
        for i in (0xb7, 0xff5c, 0xfe34, 0xfe33, 0x23d0, 0x2307):
            X = chr(i)
            if X not in s:
                found = True
                break
        if not found:
            raise ValueError("Couldn't find Unicode character not in string")
        # Find each punctuation character [(offset, char)]
        pchars, R = [], range(len(s))
        for i in range(len(s)):
            if s[i] in punctuation:
                pchars.append((i, s[i]))
        if dbg:     #xx
            print("Original string:")
            a = ruler.Ruler(0, zb=True)
            r = a(20)
            print(r)
            print(s.strip())
            print("pchars:")
            pp(pchars)
        # Replace each punctuation character with X
        sl = list(s)
        for i, c in pchars:
            sl[i] = X
        pp(''.join(sl))
        # Make new string and split into words
        words = ''.join(sl).split(X)
        if dbg:     #xx
            print(r)
            print(words)
        # Scramble the letters in the words
        for i in range(len(words)):
            words[i] = Scramble(words[i])
        print(''.join(words)) #xx
        exit()
        # Reinsert punctuation
        tl = list(' '.join(words))
        for i, c in pchars:
            tl[i] = c
        pp(tl)

arg = sys.argv[1] if len(sys.argv) > 1 else None
random.seed(arg)

if 0:
    # Demonstrates how to shuffle a substring
    s = list("awordb")
    a = s[1:-1]
    random.shuffle(a)
    print(''.join(a))
    s[1:-1] = a
    print(''.join(s))
    exit()

def Scramble(mystring, punc=None, start_end_const=False):
    '''Return a string with the letters in the words randomly shuffled but
    with the punctuation and whitespace unchanged if punc is None.
 
    Set punc to a different set of punctuation characters if you wish the
    punctuation characters are ignored when shuffling words).  For example,
    you might want to include common Unicode characters included as
    punctuation also.

    If start_end_const is True, then the first and last letters of each
    word are unchanged.

    If you wish to save memory, make mystring a list of individual
    characters; then a copy of the string isn't made.

    Example with random.seed('0'):  
        s = '"Hello there", said John.'
    returns
            '"loeHl eerth", isda noJh.'
    '''
    if punc is None:
        punc = set(string.punctuation + string.whitespace)
    dummy = "."
    prepended = appended = False
    is_string = ii(mystring, str)
    s = list(mystring) if is_string else mystring
    # Add dummy punctuation characters at start and end if needed.  This
    # regularizes the algorithm.
    if s[0] not in punc:
        s.insert(0, dummy)
        prepended = True
    if s[-1] not in punc:
        s.append(dummy)
        appended = True
    # Generate a list of integers showing where punctuation characters are
    loc = []
    for i in range(len(s)):
        if s[i] in punc:
            loc.append(i)
    # Use loc to pick out words and scramble them
    i = 0
    while i < len(loc):
        try:
            start, end = loc[i], loc[i + 1]
            if end - start > 1:  # It's a word, so shuffle its letters
                do_shuffle = True
                if start_end_const:
                    # Need at least 3 characters to shuffle
                    if end - start < 3:
                        do_shuffle = False
                if do_shuffle:
                    if start_end_const:
                        start += 1
                        end -= 1
                    substr = s[start + 1:end]
                    random.shuffle(substr)  # Shuffles sequence in place
                    s[start + 1:end] = substr
            i += 1
        except IndexError:
            break
    # Clean up
    if prepended:
        s.pop(0)
    if appended:
        s.pop(-1)
    # Return scrambled string or list
    return ''.join(s) if is_string else s

def Test():
    r = '''
I couldnt believe that I could actually understand what I was reading.
The phenomenal power of the human mind, according to a researcher at 
Cambridge University, it doesn't matter in what order the letters in a word
are, the only important thing is tht the first and last letter be in the
right place. The rest can be a total mess and you can still read it without
a problem.  This is because the human mind does not read every letter by
itself, but the word as a whole.  Amazing huh?  yeah and I always thought 
spelling was important.'''[1:]
    #r = '"Hello there", said John.'
    print(r)
    print()
    s = Scramble(r, start_end_const=1)
    print(s)

Test(); exit()

if 0:
    # Develop algorithm
    '''
        s = list made from string
        punct = punctuation or space
        - Set prepended = appended = False
        - If s[0] not punct, prepend a punc char, set prepended = True
        - If s[-1] not punct, append a punc char, set appended = True
    '''
    a = ruler.Ruler(0, zb=True)
    punctuation = set(string.punctuation + " ")
    dummy = "."
    prepended = appended = False
    r = 'This is a string.  "Hi", said Bob.'
    q = a(len(r))
    print(q)
    print(r)
    s = list(r)
    print()
    #
    if s[0] not in punctuation:
        s.insert(0, dummy)
        prepended = True
    if s[-1] not in punctuation:
        s.append(dummy)
        appended = True
    # Generate a list of integers showing where punctuation characters are
    loc = []
    for i in range(len(s)):
        if s[i] in punctuation:
            loc.append(i)
    # Use loc to pick out words and scramble them
    i = 0
    while i < len(loc):
        try:
            a, b = loc[i], loc[i + 1]
            if b - a > 1:
                # It is a word, so scramble
                substr = s[a + 1:b]
                random.shuffle(substr)
                s[a + 1:b] = substr
                print(''.join(substr))
            i += 1
        except IndexError:
            break
    print(''.join(s))
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)

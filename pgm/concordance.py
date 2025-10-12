_pgminfo = '''
<oo desc
    Print a word concordance for a file
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - List of todo items here

oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        from collections import defaultdict
        import getopt
        import io
        import math
        import os
        import re
        import sys
    if 1:   # Custom imports
        import get
        from wrap import dedent
        from color import t, RegexpDecorate
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.lines = int(os.environ.get("LINES", "50"))
        g.columns = int(os.environ.get("COLUMNS", "80")) - 1
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file regex1 [regex2...]
          Output a word concordance for the indicated file; the words must match one of
          the regexes.  The output centers the matched word and prints it in color.
        Options:
            -i      Don't ignore case
            -l      Show the found word by line numbers in the file
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = True     # Ignore case
        d["-l"] = False    # Show by lines
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hil") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("il"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        if len(args) < 2:
            Usage()
        return args
if 1:   # Classes
    class Concordance:
        def __init__(self, file):
            self.file = file
            self.contents = open(file).read()
            self.tokens = get.Tokenize(self.contents)
            # The concordance will be keyed by the word; the values will be the index
            # into self.tokens to where that token is.
            self.concordance = defaultdict(list)
            for i, token in enumerate(self.tokens):
                self.concordance[token].append(i)
        def find(self, compiled_regex):
            'Return a list of word tokens that match compiled_regex'
            o = []
            for item in self.concordance:
                if compiled_regex.search(item):
                    o.append(item)
            return o
        def get_context(self, word, length=0):
            '''Return [(pre, word, post), ...], showing the word in context.  length is
            an integer such that len(pre + word + post) <= length.  Set it to 0 and the
            environment's COLMUMNS variable will be used.
            '''
            width, o = length if length else g.columns, []
            halfwidth = (width - len(word))//2
            # Get index i of word and for pre, look at i-1, i-2, ... and join these
            # strings up until their length is >= halfwidth.  Then do the analogous task
            # for the post strings.
            for token_location in self.concordance[word]:
                # Get the pre string
                q, position = [], token_location
                while True:
                    position -= 1
                    if position < 0:
                        break
                    if len(''.join(q) + self.tokens[position]) <= halfwidth:
                        q.append(self.tokens[position])
                    else:
                        break
                q.reverse()
                pre = ''.join(q).replace("\n", " ")
                # Get the post string
                q, position = [], token_location
                while True:
                    position += 1
                    if position > len(self.tokens) - 1:
                        break
                    if len(''.join(q) + self.tokens[position]) <= halfwidth:
                        q.append(self.tokens[position])
                    else:
                        break
                post = ''.join(q).replace("\n", " ")
                o.append((pre, word, post))
            return o
if 1:   # Core functionality
    def MatchWordsWithContext(regexes, concordance):
        for regex in regexes:
            t.print(f"{t.trq}Searching for {t.purl}{regex}")
            matched_words = concordance.find(re.compile(regex, re.I if d["-i"] else 0))
            for matched_word in matched_words:
                for pre, word, post in concordance.get_context(matched_word):
                    s = f"{pre}{t.ornl}{word}{t.n}{post}"
                    while "  " in s:
                        s = s.replace("  ", " ")
                    print(s)
    def MatchWordsByLine(regexes, concordance):
        lines = concordance.contents.split("\n")
        w = math.ceil(math.log10(len(lines) + 1))
        rd = RegexpDecorate()
        for regex in regexes:
            t.print(f"{t.trq}Searching for {t.purl}{regex}{t.n} in '{t.royl}{file}{t.n}':")
            r = re.compile(regex, re.I if d["-i"] else 0)
            rd.register(r, t.ornl, t.n)    # Print matches in light orange on black
            for i, line in enumerate(lines):
                mo = r.search(line)
                if mo:
                    print(f"{i:{w}d}:  ", end="")
                    ss = io.StringIO()
                    rd(line, file=ss, insert_nl=False)
                    print(ss.getvalue())

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    file = args.pop(0)
    concordance = Concordance(file)
    if d["-l"]:
        MatchWordsByLine(args, concordance)
    else:
        MatchWordsWithContext(args, concordance)

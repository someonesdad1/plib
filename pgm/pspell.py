'''
Spell check the strings and comments in a python file.

Use /plib/pgm/spell.py and /plib/pgm/xref.py to spell check all the tokens
in a file.  xref will also split programming tokens and spell check the
individual words.

The use case for this script is to focus on the strings that are output to
the user.  Since the comments in a script are also important for a
programmer to review, these are also checked.

Algorithm:  the tokenize library is used to tokenize the script.

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
        # Spell check strings and comments in a python script.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import defaultdict
        import getopt
        import os
        from pathlib import Path as P
        from pprint import pprint as pp
        import string as String
        import sys
        import token
        import tokenize
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from dpstr import Tokenize
        from get import GetLines
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
            
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1.py [file2.py...]
          Spell check the strings and comments in the indicated python
          scripts.  The line number(s) are printed with the misspelled
          token.  All characters are converted to lowercase and words
          are made up only of ASCII letters.
        Options:
            -c      Don't colorize output
            -k      Don't check comments
            -s      Don't check strings
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Don't use color in output
        d["-k"] = True      # Don't check comments
        d["-s"] = True      # Don't check strings
        try:
            opts, files = getopt.getopt(sys.argv[1:], "cks") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cks"):
                d[o] = not d[o]
        if not files:
            Usage()
        # Set up colorizing
        t.cmt = t("purl") if d["-c"] else ""
        t.str = t("ornl") if d["-c"] else ""
        t.file = t("redl") if d["-c"] else ""
        t.N = t.n if d["-c"] else ""
        return files
if 1:   # Core functionality
    def GetWords():
        'Return the set of words used for spell checking'
        files = '''
                /words/words.ngsl.experimental
                /words/words.additional
        '''.split()
        files = '''
                /words/words.univ
        '''.split()
        words = set()
        for file in files:
            lines = GetLines(file, script=True, ignore_empty=True,
                             strip=True, nonl=True)
            words.update(set(i.lower() for i in lines))
        # Here's a list of other words that are spelled correctly
        e = GetLines("/plib/pgm/pspell.extra", script=True, ignore_empty=True,
                     strip=True, nonl=True)
        words.update(' '.join(i.lower() for i in e).split())
        return words
    def GetLine(mytoken):
        '''Return L (line number) for the token if it's on a single line.
        Otherwise return L1-L2 (line number range) when it's a multiline
        entity.
        '''
        a, b = mytoken.start
        c, d = mytoken.end
        if a == c:
            return f"{a}"
        else:
            return f"{a}-{c}"
    def SpellCheck(string):
        bad = set()
        wordchars = String.ascii_letters
        for word in Tokenize(string, wordchars=wordchars, check=True):
            w = word.lower()
            if not w or len(w) == 1:
                continue
            if w not in mywords:
                bad.add(word)
        return list(sorted(bad, key=str.lower))
    def Process(tokens):
        badwords = []
        for mytoken in tokens:
            bad = SpellCheck(mytoken.string)
            if bad:
                for item in bad:
                    badwords.append((item, mytoken))
        return badwords
    def ProcessFile(file):
        filename = file
        p = P(filename)
        if not p.exists():
            # See if adding '.py' to it works
            filename += ".py"
            p = P(filename)
            if not p.exists():
                Error(f"Cannot find {file!r}")
        # Collect tokens
        comments = []
        strings = []
        try:
            with tokenize.open(filename) as f:
                tokens = tokenize.generate_tokens(f.readline)
                for T in tokens:
                    if d["-s"] and token.tok_name[T.exact_type] == "STRING":
                        strings.append(T)
                    elif d["-k"] and token.tok_name[T.exact_type] == "COMMENT":
                        comments.append(T)
        except tokenize.TokenError:
            Error(f"{file!r} may not be a python script")
        badstrings = Process(strings) if d["-s"] else []
        badcomments = Process(comments) if d["-k"] else []
        if badstrings:
            Report(badstrings, t.str, file, "bad strings")
        if badcomments:
            Report(badcomments, t.cmt, file, "bad comments")
    def Report(items, clrstr, file, mytype):
        '''Condense the items into one line per word with line numbers.
          items     (word, token)
          clrstr    Colorizing escape code or ''
          file      Which file
          mytype    "bad strings", "bad comments", etc.
        '''
        # Collapse line numbers to a single line per word
        lst = defaultdict(list)
        for word, token in items:
            lst[word].append(GetLine(token))
        # Make a sorted list of the words and their line numbers
        out = []
        for word in lst:
            ln = ' '.join(lst[word])
            out.append(f"  {word} {ln}")
        # Print sorted list            
        print(f"{t.file}{file} {mytype}{t.N}")
        for i in sorted(out, key=str.lower):
            print(f"  {clrstr}{i}{t.N}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    mywords = GetWords()
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)

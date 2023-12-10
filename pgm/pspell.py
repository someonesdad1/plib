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
        #from columnize import Columnize
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
        words = set()
        for file in files:
            words.update(set(open(file).read().lower().split("\n")))
        # Here's a list of other words that are spelled correctly
        extra = '''
            blk  blkl  blkd  blkb
            brn  brnl  brnd  brnb
            red  redl  redd  redb
            orn  ornl  ornd  ornb
            yel  yell  yeld  yelb
            grn  grnl  grnd  grnb
            blu  blul  blud  blub
            vio  viol  viod  viob
            gry  gryl  gryd  gryb
            wht  whtl  whtd  whtb
            cyn  cynl  cynd  cynb
            mag  magl  magd  magb
            pnk  pnkl  pnkd  pnkb
            lip  lipl  lipd  lipb
            lav  lavl  lavd  lavb
            lil  lill  lild  lilb
            pur  purl  purd  purb
            roy  royl  royd  royb
            den  denl  dend  denb
            sky  skyl  skyd  skyb
            trq  trql  trqd  trqb
            sea  seal  sead  seab
            lwn  lwnl  lwnd  lwnb
            olv  olvl  olvd  olvb

            abbreviation 
            abs 
            alternate 
            alternating 
            analogous 
            angular 
            anomalous 
            arcmin 
            arcsec 
            argv
            bash 
            bool 
            boolean 
            canonical 
            circular 
            clamp 
            colorize colorizing
            columnize
            com
            constructor 
            cop 
            cuddled 
            cuddling 
            dbg
            debugger 
            deg 
            deque 
            deques 
            disassemble 
            disassembling 
            div 
            don
            dp 
            dq 
            ellipsis 
            emulator 
            en 
            engsic 
            err 
            exponent 
            exponents 
            extraneous 
            fac 
            formatter 
            functionalities
            functionality
            getline
            gmail
            grad 
            gradians 
            hack 
            hacking 
            halfwidth 
            handy 
            header
            hex 
            http
            https
            id 
            ident 
            imaginary 
            improper 
            increment 
            integer 
            integers 
            interpolation 
            interpolations 
            invalid 
            invariants 
            isinf 
            iv 
            keyword 
            len 
            libmpf 
            lill
            locale 
            logarithm 
            million 
            misspelled
            multiline
            multithreading 
            nan 
            ngls
            nonempty 
            num 
            opensource
            optional 
            org 
            overflow 
            override 
            overrides 
            peterson
            pgm
            pickle 
            pickled 
            plib
            prefix 
            prefixes 
            prepend 
            prepended 
            printout 
            py
            python
            quadrant 
            radians 
            radix 
            recursion 
            repeatable 
            repr 
            reset 
            rev 
            rlz 
            roundoff 
            rtdp 
            rtz 
            sentinel 
            sextant 
            sgn 
            shorthand 
            si 
            someonesdad1
            specially 
            sr 
            str
            sys
            takeapart 
            token
            tokenize
            tokens
            truncate 
            underflow 
            underline 
            underlining 
            unrecognized 
            unsupported 
            verbose 
            width 
            xref
            zero 
            zeroes 
            zeros 

        '''.split()
        words.update(extra)
        return words

    def GetLine(mytoken):
        '''Return [L] for the token if it's on a single line.  Otherwise
        return [L1-L2] when it's a multiline entity.
        '''
        a, b = mytoken.start
        c, d = mytoken.end
        if a == c:
            return f"[{a}]"
        else:
            return f"[{a}-{c}]"
    def SpellCheck(string):
        bad = set()
        wordchars = String.ascii_letters
        for word in Tokenize(string, wordchars=wordchars, check=True):
            w = word.lower()
            if not w or len(w) == 1:
                continue
            if w not in mywords:
                bad.add(w)
        return list(sorted(bad))
    def Process(tokens):
        badwords = []
        for mytoken in tokens:
            bad = SpellCheck(mytoken.string)
            if bad:
                for item in bad:
                    badwords.append((item, mytoken))
        return badwords
    def ProcessFile(file):
        # Collect tokens
        comments = []
        strings = []
        with tokenize.open(file) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for T in tokens:
                if d["-s"] and token.tok_name[T.exact_type] == "STRING":
                    strings.append(T)
                elif d["-k"] and token.tok_name[T.exact_type] == "COMMENT":
                    comments.append(T)
        badstrings = Process(strings) if d["-s"] else []
        badcomments = Process(comments) if d["-k"] else []
        if badstrings:
            print(f"{t.file}{file}:  {t.str}bad strings{t.N}")
            for badword, mytoken in badstrings:
                print(f"  {t.str}{badword} {GetLine(mytoken)}{t.N}")
        if badcomments:
            print(f"{t.file}{file}:  {t.cmt}bad comments{t.N}")
            for badword, mytoken in badcomments:
                print(f"  {t.cmt}{badword} {GetLine(mytoken)}{t.N}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    mywords = GetWords()
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)

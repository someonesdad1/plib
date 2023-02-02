'''
IPA pronounciations
'''

# https://en.wikipedia.org/wiki/Template:IPAc-en table's columns:
    #  0  Code
    #  1  Aliases
    #  2  Display text
    #  3  Tooltip
    #  4  Type
table = '''
    b		b	'b' in 'buy'	diaphoneme
    d		d	'd' in 'dye'	diaphoneme
    dj	dy, dʲ	dj	/dj/: 'd' in 'dew'	diaphoneme
    dʒ	dZ, ʤ	dʒ	/dʒ/: 'j' in 'jam'	diaphoneme
    ð	D	ð	/ð/: 'th' in 'this'	diaphoneme
    f		f	'f' in 'find'	diaphoneme
    ɡ	g	ɡ	/ɡ/: 'g' in 'guy'	diaphoneme
    h		h	'h' in 'hi'	diaphoneme
    hw	ʍ	hw	/hw/: 'wh' in 'why'	diaphoneme
    j	y	j	/j/: 'y' in 'yes'	diaphoneme
    k		k	'k' in 'kind'	diaphoneme
    l		l	'l' in 'lie'	diaphoneme
    lj	ly, lʲ	lj	/lj/: 'l' in 'lute'	diaphoneme
    m		m	'm' in 'my'	diaphoneme
    n		n	'n' in 'nigh'	diaphoneme
    nj	ny, nʲ	nj	/nj/: 'n' in 'new'	diaphoneme
    ŋ	N, ng	ŋ	/ŋ/: 'ng' in 'sing'	diaphoneme
    p		p	'p' in 'pie'	diaphoneme
    r	ɹ, ɻ	r	'r' in 'rye'	diaphoneme
    s		s	's' in 'sigh'	diaphoneme
    sj	sy, sʲ	sj	/sj/: 's' in 'consume'	diaphoneme
    ʃ	S, sh	ʃ	/ʃ/: 'sh' in 'shy'	diaphoneme
    t		t	't' in 'tie'	diaphoneme
    tj	ty, tʲ	tj	/tj/: 't' in 'tune'	diaphoneme
    tʃ	tS, ʧ, ch	tʃ	/tʃ/: 'ch' in 'China'	diaphoneme
    θ	T	θ	/θ/: 'th' in 'thigh'	diaphoneme
    θj	θy, θʲ	θj	/θj/: 'th' in 'enthuse'	diaphoneme
    v		v	'v' in 'vie'	diaphoneme
    w		w	'w' in 'wind'	diaphoneme
    z		z	'z' in 'zoom'	diaphoneme
    zj	zy, zʲ	zj	/zj/: 'Z' in 'Zeus'	diaphoneme
    ʒ	Z, zh	ʒ	/ʒ/: 's' in 'pleasure'	diaphoneme
    ɑː	A:, ɑ:, aː, a:	ɑː	/ɑː/: 'a' in 'father'	diaphoneme
    ɑːr	ɑɹ, aːr, a:r, ɑ:r, ɑr	ɑːr	/ɑːr/: 'ar' in 'far'	diaphoneme
    ɒ	Q	ɒ	/ɒ/: 'o' in 'body'	diaphoneme
    ɒr	Qr	ɒr	/ɒr/: 'or' in 'moral'	diaphoneme
    æ	ae, {	æ	/æ/: 'a' in 'bad'	diaphoneme
    ær	aer, &r, æɹ	ær	/ær/: 'arr' in 'marry'	diaphoneme
    aɪ	ai, aI	aɪ	/aɪ/: 'i' in 'tide'	diaphoneme
    aɪər	aɪr, aIr, aɪə	aɪər	/aɪər/: 'ire' in 'fire'	diaphoneme
    aʊ	au, aU	aʊ	/aʊ/: 'ou' in 'mouth'	diaphoneme
    aʊər	aʊr, aUr, aʊə, aur	aʊər	/aʊər/: 'our' in 'hour'	diaphoneme
    ɛ	E	ɛ	/ɛ/: 'e' in 'dress'	diaphoneme
    ɛr	Er	ɛr	/ɛr/: 'err' in 'merry'	diaphoneme
    eɪ	ei, eI, eː, e:	eɪ	/eɪ/: 'a' in 'face'	diaphoneme
    ɛər	eir, eIr, e@r, E@r, ɛɪɹ, eɪr, eːr, e:r, ɛəɹ, ɛə, ɛːr, ɛ:r, ɛː, ɛ:, E:, E:r	ɛər	/ɛər/: 'are' in 'bare'	diaphoneme
    ɛəˈr	ɛə'r, eəˈr, eə'r, e@'r, E@'r, ɛːˈr, E:'r	ɛəˈr	/ɛəˈr/: 'ere' in 'thereof'	diaphoneme
    ɛəˌr	ɛə,r, eəˌr, eə,r, E@,r, E@%r, e@,r, e@%r, ɛːˌr, E:,r, E:%r	ɛəˌr	/ɛəˌr/: 'ere' in 'thereof'	diaphoneme
    ɪ	I, ᵻ	ɪ	/ɪ/: 'i' in 'kit'	diaphoneme
    ɪr		ɪr	/ɪr/: 'irr' in 'mirror'	diaphoneme
    iː	i:	iː	/iː/: 'ee' in 'fleece'	diaphoneme
    ɪər	i:r, iːr, I@r, i@r, ɪəɹ, iːɹ, ɪə	ɪər	/ɪər/: 'ear' in 'near'	diaphoneme
    ɪəˈr	ɪə'r, I@'r	ɪəˈr	/ɪəˈr/: 'er' in 'spheroidal'	diaphoneme
    ɪəˌr	ɪə,r, I@,r, I@%r	ɪəˌr	/ɪəˌr/: 'er' in 'spheroidal'	diaphoneme
    oʊ	o:, oː, ou, oU, @u, @U, əʊ, əu, oʊ-	oʊ	/oʊ/: 'o' in 'code'	diaphoneme
    ɔː	O, O:, ɔ:, ɒː, Q:	ɔː	/ɔː/: 'au' in 'fraud'	diaphoneme
    ɔːr	Or, ɔɹ, ɔ(r), ɔr, ɔər, oUr, ɔəɹ, ɔʊɹ, oʊɹ, oʊr, oːr, o:r, ɔə, ɔə(r)	ɔːr	/ɔːr/: 'ar' in 'war'	diaphoneme
    ɔɪ	oj, ɔj, oi, oɪ, ɔi, OI, oy	ɔɪ	/ɔɪ/: 'oi' in 'choice'	diaphoneme
    ɔɪər	ɔɪr, oyr, ɔɪə	ɔɪər	/ɔɪər/: 'oir' in 'coir'	diaphoneme
    ʊ	U, ᵿ	ʊ	/ʊ/: 'u' in 'push'	diaphoneme
    ʊr	Ur	ʊr	/ʊr/: 'our' in 'courier'	diaphoneme
    uː	u:	uː	/uː/: 'oo' in 'goose'	diaphoneme
    ʊər	u:r, uːr, u@r, U@r, ʊəɹ, ʊə	ʊər	/ʊər/: 'our' in 'tour'	diaphoneme
    ʊəˈr	ʊə'r, U@'r	ʊəˈr	/ʊəˈr/: 'ur' in 'plurality'	diaphoneme
    ʊəˌr	ʊə,r, U@,r, U@%r	ʊəˌr	/ʊəˌr/: 'ur' in 'plurality'	diaphoneme
    ʌ	V	ʌ	/ʌ/: 'u' in 'cut'	diaphoneme
    ʌr	Vr, ʌɹ	ʌr	/ʌr/: 'urr' in 'hurry'	diaphoneme
    ɜːr	ɝː, ɝ, 3r, 3:r, əːr, @:r, ɜɹ, ɜ(r), ɜr	ɜːr	/ɜːr/: 'ur' in 'fur'	diaphoneme
    ə	@	ə	/ə/: 'a' in 'about'	diaphoneme
    ər	ɚ, @r, əɹ, ə(r)	ər	/ər/: 'er' in 'letter'	diaphoneme
    əl	@l, ᵊl, l̩	əl	/əl/: 'le' in 'bottle'	diaphoneme
    ən	@n, ᵊn, n̩	ən	/ən/: 'on' in 'button'	diaphoneme
    əm	@m, ᵊm, m̩	əm	/əm/: 'm' in 'rhythm'	diaphoneme
    i		i	/i/: 'y' in 'happy'	diaphoneme
    u		u	/u/: 'u' in 'influence'	diaphoneme
    x	kh	x	/x/: 'ch' in 'loch'	diaphoneme
    ʔ	?	ʔ	/ʔ/: the catch in 'uh-oh'	diaphoneme
    ɒ̃	ɑ̃, ɒ~, ɑ~, Q~	ɒ̃	/ɒ̃/: nasal 'an' in 'vin blanc'	diaphoneme
    æ̃	ae~, {~, ã, a~	æ̃	/æ̃/: nasal 'in' in 'vin blanc'	diaphoneme
    ɜː	3, 3:, ɜ:, ɜ, əː, @:	ɜː	/ɜː/: r-less 'ur' in 'nurse'	diaphoneme
    ˈ	', "	ˈ	/ˈ/: primary stress follows	diaphoneme
    ˌ	,, %	ˌ	/ˌ/: secondary stress follows	diaphoneme
    .	·	.	/./: syllable break	diaphoneme
    #		#	/#/: morpheme break	diaphoneme
    !		|	/: prosodic break (minor)	diaphoneme
    !!	‖	‖	/‖/: prosodic break (major)	diaphoneme
    _				separator
    nbsp	&nbsp;			separator
    ,_		,		separator
    -	–	-		separator
    (		(		separator
    )		)		separator
    ...		 ... 		separator
    juː		juː	/juː/: 'u' in 'cute'	diaphoneme
    jʊər		jʊər	/jʊər/: 'ure' in 'cure'	diaphoneme
'''.strip()

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
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from columnize import Columnize
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        r = re.compile("'(.*)' in '(.*)'")
        t.hi = t("whtl", "blu", "bold")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def GetString(a, b):
        '''Return a string with color coding
        '''
        a = a.replace("/", "")
        mo = r.search(b)
        if mo:
            c, d = mo.groups()
            f = d.replace(c, f"{t.hi}{c}{t.n}", 1)
            if "vin" in d:
                f = " " + f
            return f"{a:6s}{f}"
        else:
            if "prosodic" in b or "separator" in b:
                return None
            if a == "ˈ":
                b = "stress1"
            elif a == "ˌ":
                b = "stress2"
            elif a == ".":
                b = "syllable"
            elif a == "ʔ":
                b = "'uh-oh' catch"
            elif a == "#":
                b = "morpheme"
            elif a == " " or a == "‖":
                return None
            return f"{a:4s}  {b}"
    def PrintTable():
        out = []
        for line in table.split("\n"):
            f = [i.strip() for i in line.split("\t")]
            # Parse out field 3
            s = f[3]
            if ":" in s:
                a, b = s.split(":")
            else:
                a = f[0]
                b = s
            a, b = [i.strip() for i in (a, b)]
            if "separator" in f[4]:
                continue
            t = GetString(a, b)
            if t:
                out.append(t)
        for i in Columnize(out, columns=3):
            print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    PrintTable()

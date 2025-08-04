'''
IPA pronunciations
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # IPA pronunciations
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from columnize import Columnize
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        r = re.compile("'(.*)' in '(.*)'")
if 1:  # Data
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
        ə	@	ə	/ə/: 'a' in 'about'	diaphoneme
        æ	ae, {	æ	/æ/: 'a' in 'bad'	diaphoneme
        ɑːr	ɑɹ, aːr, a:r, ɑ:r, ɑr	ɑːr	/ɑːr/: 'ar' in 'far'	diaphoneme
        ɒ	Q	ɒ	/ɒ/: 'o' in 'body'	diaphoneme
        ɒr	Qr	ɒr	/ɒr/: 'or' in 'moral'	diaphoneme
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
    if 0:
        # This table has had field 3 from above extracted, modified for uniformity,
        # some lines deleted, and had things moved around.
        for line in table.split("\n"):
            if "separator" in line or "prosodic" in line:
                continue
            f = line.split("\t")
            s = f[3]
            if ":" not in s:
                u = s.split()[0].replace("'", "/")
                s = f"{u}: {s}"
            # Change ':' to tab
            s = s.replace(": ", "\t")
            print(s)
        exit()
    # 4th column from table at https://en.wikipedia.org/wiki/Template:IPAc-en,
    # modified for uniformity and the lines containing "separator" or
    # "prosodic" eliminated.  I've moved the order around and denoted column
    # headers with '+'.
    table = '''
        Consonants	+
        /b/	'b' in 'buy'
        /d/	'd' in 'dye'
        /dj/	'd' in 'dew'
        /f/	'f' in 'find'
        /ɡ/	'g' in 'guy'
        /h/	'h' in 'hi'
        /dʒ/	'j' in 'jam'
        /k/	'k' in 'kind'
        /l/	'l' in 'lie'
        /lj/	'l' in 'lute'
        /m/	'm' in 'my'
        /n/	'n' in 'nigh'
        /nj/	'n' in 'new'
        /ŋ/	'ng' in 'sing'
        /p/	'p' in 'pie'
        /r/	'r' in 'rye'
        /s/	's' in 'sigh'
        /sj/	's' in 'consume'
        /ʃ/	'sh' in 'shy'
        /ʒ/	's' in 'pleasure'
        /t/	't' in 'tie'
        /tj/	't' in 'tune'
        /ð/	'th' in 'this'
        /tʃ/	'ch' in 'China'
        /θ/	'th' in 'thigh'
        /θj/	'th' in 'enthuse'
        /v/	'v' in 'vie'
        /w/	'w' in 'wind'
        /hw/	'wh' in 'why'
        /j/	'y' in 'yes'
        /z/	'z' in 'zoom'
        /zj/	'Z' in 'Zeus'
        
        --Vowel a	+
        /ɑː/	'a' in 'father'
        /ɒ/	'o' in 'body'
        /ə/	'a' in 'about'
        /æ/	'a' in 'bad'
        /eɪ/	'a' in 'face'
        /ɑːr/	'ar' in 'far'
        /ɒr/	'or' in 'moral'
        /ær/	'arr' in 'marry'
        
        --Vowel e	+
        /ɛ/	'e' in 'dress'
        /ɛr/	'err' in 'merry'
        /ɛər/	'are' in 'bare'
        /ɛəˈr/	'ere' in 'thereof'
        /ɛəˌr/	'ere' in 'thereof'
        /iː/	'ee' in 'fleece'
        /ɪəˈr/	'er' in 'spheroidal'
        /ɪəˌr/	'er' in 'spheroidal'
        /i/	'y' in 'happy'
        
        --Vowel i	+
        /aɪ/	'i' in 'tide'
        /aɪər/	'ire' in 'fire'
        /ɪ/	'i' in 'kit'
        /ɪr/	'irr' in 'mirror'
        
        --Vowel o	+
        /aʊ/	'ou' in 'mouth'
        /aʊər/	'our' in 'hour'
        /ɪər/	'ear' in 'near'
        /oʊ/	'o' in 'code'
        /ɔː/	'au' in 'fraud'
        /ɔːr/	'ar' in 'war'
        /ɔɪ/	'oi' in 'choice'
        /ɔɪər/	'oir' in 'coir'
        
        --Vowel u	+
        /u/	'u' in 'influence'
        /juː/	'u' in 'cute'
        /ʊ/	'u' in 'push'
        /ʊr/	'our' in 'courier'
        /uː/	'oo' in 'goose'
        /ʊər/	'our' in 'tour'
        /ər/	'er' in 'letter'
        /ʊəˈr/	'ur' in 'plurality'
        /ʊəˌr/	'ur' in 'plurality'
        /ʌ/	'u' in 'cut'
        /ʌr/	'urr' in 'hurry'
        /ɜːr/	'ur' in 'fur'
        /ɜː/	r-less 'ur' in 'nurse'
        /əl/	'le' in 'bottle'
        /ən/	'on' in 'button'
        /əm/	'm' in 'rhythm'
        /jʊər/	'ure' in 'cure'
        
        --Other	+
        /x/	'ch' in 'loch'
        /ʔ/	catch in 'uh-oh'
        /ɒ̃/	nasal 'an' in 'vin blanc'
        /æ̃/	nasal 'in' in 'vin blanc'
        /ˈ/	primary stress follows
        /ˌ/	secondary stress follows
        /./	syllable break
        /#/	morpheme break
    '''.strip()
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] 
          Print out a table of IPA symbols.
        Options:
            -c      Don't use ANSI color in output
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True  # Print in color
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ch", ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        SetupColor()
        return args
if 1:  # Core functionality
    def SetupColor():
        t.hi = t("whtl", "blud") if d["-c"] else ""
        t.hdr = t("ornl") if d["-c"] else ""
        t.ti = t("yell") if d["-c"] else ""
        t.N = t.n if d["-c"] else ""
    def GetString(a, b):
        '''Return a string with color coding'''
        a = a.replace("/", "")
        mo = r.search(b)
        if mo:
            c, d = mo.groups()
            f = d.replace(c, f"{t.hi}{c}{t.N}", 1)
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
            if not line.strip():
                continue
            a, b = [i.strip() for i in line.split("\t")]
            if b == "+":
                out.append(f"{t.hdr}{a.replace('-', ' ')}{t.N}")
            else:
                s = GetString(a, b)
                out.append(s)
        t.print(f"{t.ti}IPA symbols\n")
        for i in Columnize(out, width=W):
            print(i)
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    PrintTable()

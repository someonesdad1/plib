'''
Tool to build a transliteration table for ASCII characters.
 
The strategy used is to create a set of all valid Unicode codepoints and
remove things like combining characters, tags, and non-English language
codepoints.  A decomposition from the Unicode Character Database (see
ucd.py) is used if it exists; these usually translate characters with
accents or other modifiers.  Then the Unicode string descriptions of
each character are searched for key words to select the set of
characters wanted for each of the above ASCII characters.  The result is
a dictionary named keep that contains each ASCII character as a key and
the set of Unicode characters that should be transliterated to that
ASCII character.
 
A guiding factor in my selection of the characters to transliterate is
that they must look like the corresponding ASCII character, regardless
of the semantic content.  Thus, U+01c3 looks like an exclamation mark,
but has the name of "LATIN LETTER RETROFLEX CLICK".  The alternate name
is "LATIN LETTER EXCLAMATION MARK", so it is reasonable that it be
translated to !, U+0021.  In other words, syntax and not semantic
content is the driving force behind this transliteration, primarily
because I am not a linguist.
'''

import unicodedata as U
import re
import pickle
import string
import sys
import time
import getopt
import os
from ucd import ucd
from textwrap import dedent
from itertools import combinations, chain
from columnize import Columnize
from pprint import pprint as pp
from collections import defaultdict
from pdb import set_trace as xx 
if 0:
    import debug
    debug.SetDebugger()

def ShowAll(cpset, arg="all"):
    '''Print all codepoints in cpset to stdout that contain the regular
    expression arg.  Use "all" for arg to print all characters.
    '''
    r = re.compile(arg, re.I)
    for cp in sorted(cpset, reverse=True):
        descr = U.name(chr(cp))
        if arg == "all" or r.search(descr):
            print(f"{cp:06x} {chr(cp)} {descr}")

def Debug(*p, **kw):
    print(*p, **kw, file=sys.stderr)

def PrintCP(cp, indent=""):
    c = chr(cp)
    print(f"{indent}{cp:05X} {chr(cp):^3s} {U.name(c)}", file=stream)

def GetWorkingSet(file="asciify_make.pickle", build=False):
    '''Return (cpset, keep) where cpset is the working set of Unicode
    codepoints and keep is a defaultdict of lists.
    
    It takes about 1.6 s to build the set and about half of this time to
    read it in from disk.  Thus, we pickle the data to disk.  The file
    is only built if the pickled data cannot be read or build is True.
    '''
    def RemoveInvalid(cpset):
        'Remove codepoint values that cause an exception'
        remove = set()
        for cp in cpset:
            try:
                U.name(chr(cp))
            except ValueError:
                remove.add(cp)
        Debug(fmt.format("  Invalid codepoints", -len(remove)))
        cpset -= remove
    def RemoveMisc(cpset):
        'Remove TAG and COMBINING characters'
        remove = set()
        cpset -= set(range(0xe0020, 0xe007f))   # Remove TAGS
        cpset -= set((0x0fdfc,))                # Special character
        combine = re.compile(r"^COMBINING\b|\bCOMBINING\b")
        for cp in cpset:
            descr = U.name(chr(cp))
            if combine.search(descr):
                remove.add(cp)
        Debug(fmt.format("  Tag, combining", -len(remove)))
        cpset -= remove
    def RemoveNotEnglish(cpset):
        '''Remove the codepoints from cpset whose Unicode
        description string contains one of the following languages,
        as they don't share symbols with English.
        '''
        languages = set('''
            adlam admetos aegean afghani ahom anatolian arabian
            arabic armenian avestan balinese bamum bassa batak
            bengali bhaiksuki bopomofo brahmi buginese buhid
            byzantine canadian carian caucasian chakma cham cherokee
            cjk coptic cuneiform cypriot cyrillic deseret devanagari
            dogra duployan egyptian egyptological elbasan ethiopic
            ewa functional georgian geta glagolitic grantha greek
            gujarati gunjala gurmukhi halfwidth hangul hangzhou
            hanifi hanunoo hatran hebrew hentaigana hexagram
            hieroglyph hiragana hom hungarian ideogram ideograph
            ideographic imperial indic inscriptional interlinear
            japanese javanese kaithi kangxi kannada katakana kayah
            kharoshthi khmer khojki khudawadi korean lao lepcha
            limbu linear lisu lycian lydian mahajani mahjong makasar
            malayalam mandaic manichaean marchen masaram mayan
            medefaidrin meetei mende meroitic miao modi mongolian
            mro multani myanmar nabataean nandinagari newa nko
            nomisma nushu nyiakeng object ogham ogonek ol oriya
            osage osmanya pahawh pahlavi palmyrene parthian pau
            permic persian phags-pa phaistos philippine phoenician
            psalter rejang rumi runic samaritan saurashtra sesame
            shakti sharada shavian siddham sinhala slavonic sogdian
            sora soyombo sundanese svasti syloti syriac tagalog
            tagbanwa tai takri tamil tangut telugu tetragram thaana
            thai tibetan tifinagh tirhuta turkic ugaritic vai vedic
            wancho warang xiangqi yi zanabazar
 
            alchemical astrological bottom dentistry digram domino
            element emoji face input integral person recycling
            shorthand sideways signwriting symbol
        '''.upper().split())
        l = [rf"\b{i}\b" for i in languages]  # Add word boundaries
        ignore = re.compile('|'.join(l))
        remove = set()
        # Japanese special characters
        remove.update(set(range(0x3300, 0x3358)))
        remove.update(range(0x337b, 0x3380))
        for cp in cpset:
            descr = U.name(chr(cp))
            if ignore.search(descr):
                remove.add(cp)
        Debug(fmt.format("  Non-English codepoints", -len(remove)))
        cpset -= remove
    def RemoveGroups(cpset):
        '''Remove general categories (ucd calls them groups) that
        are known to not contain characters we want.
 
        Cf = TAG, format control characters
        Lo = Other letters from foreign languages
        Mn = Combining, etc.
        Ps = Open punctuation
        '''
        gc_to_ignore = "Cf Lo Mn Ps"
        ignore = set(gc_to_ignore.split())
        remove = set()
        for cp in cpset:
            try:
                group, data = ucd["chars"][cp]
                g = ucd["groups"][group]
                gc = g["gc"]    # General category
                if gc in ignore:
                    remove.add(cp)
            except KeyError:
                continue
        Debug(fmt.format(f"  Remove gc '{gc_to_ignore}'", -len(remove)))
        cpset -= remove
    try:
        if build or d["-f"]:
            raise Exception()
        # Read in the pickled data
        f = open(file, "rb")
        cpset = pickle.load(f)
    except Exception:
        # Construct the pickle file
        cpset = set(range(0x110000))    # 1114112 codepoints
        Debug(f"Started with {len(cpset)} codepoints")
        RemoveInvalid(cpset)
        RemoveGroups(cpset)
        RemoveMisc(cpset)
        RemoveNotEnglish(cpset)
        f = open(file, "wb")
        pickle.dump(cpset, f)
        Debug(f"Left with {len(cpset)} valid codepoints")
    return cpset, defaultdict(set)

if 1:   # Handling the codepoints
    def Quotes(cpset, keep):
        def GetDoubleQuotes():
            get = ["quot", "prime"]
            remove = [
                "single",
                "syllable",
                r"\bapl\b",
                "^prime$",
                "^reversed prime$",
                "^modifier letter prime$",
                "^heavy left-pointing angle",
                "^heavy right-pointing angle",
            ]
            Extract(cpset, keep, get, remove, '"', verbose="Double quotes")
        def GetSingleQuotes():
            get = ["quot", "prime"]
            remove = [
                "double",
                "syllable",
                "triple",
                "quadruple",
                r"\bapl\b",
                "^quotation mark$",
                "^fullwidth quotation mark$",
                "^heavy left-pointing angle",
                "^heavy right-pointing angle",
            ]
            Extract(cpset, keep, get, remove, "'", verbose="Single quotes")
        def GetBackQuote():
            get = ["grave accent", "reversed.*prime"]
            remove = ["letter", "quotation"]
            Extract(cpset, keep, get, remove, "`", verbose="Back quote")
        if not select:
            GetSingleQuotes()
            GetDoubleQuotes()
            GetBackQuote()

    def Brackets(cpset, keep):
        def GetLeftParenthesis():
            get = ["parenthesis"]
            remove = ["right", "hook", "extension", "top", "vertical"]
            Extract(cpset, keep, get, remove, "(", verbose="Left parenthesis")
        def GetRightParenthesis():
            get = ["parenthesis"]
            remove = ["left", "hook", "extension", "top", "vertical"]
            Extract(cpset, keep, get, remove, ")", verbose="Right parenthesis")
        def GetLessThan():
            get = ["less-than"]
            remove = ["equal", "with", "and", "or", "not", "above",
                "nested", "arc", "closed", "lap", "double", "beside", "arrow" ]
            Extract(cpset, keep, get, remove, "<", verbose="Less-than")
        def GetGreaterThan():
            get = ["greater-than"]
            remove = ["equal", "with", "and", "or", "not", "above",
                "nested", "arc", "closed", "lap", "double", "beside", "arrow" ]
            Extract(cpset, keep, get, remove, ">", verbose="Greater-than")
        def GetLeftBracket():
            get = ["bracket"]
            remove = ["right", "curly", "hook", "extension", "top",
                "vertical", "paraphrase", "angle", "substitution",
                "transposition", "omission", "letter", "arc", "z notation",]
            Extract(cpset, keep, get, remove, "[", verbose="Left bracket")
        def GetRightBracket():
            get = ["bracket"]
            remove = ["left", "curly", "hook", "extension", "top",
                "vertical", "paraphrase", "angle", "substitution",
                "transposition", "omission", "letter", "arc", "z notation",]
            Extract(cpset, keep, get, remove, "]", verbose="Right bracket")
        def GetLeftCurly():
            get = ["curly"]
            remove = ["right", "square", "hook", "middle", "loop",
                "extension", "logical", "vertical", "top"]
            Extract(cpset, keep, get, remove, "{", verbose="Left curly bracket")
        def GetRightCurly():
            get = ["curly"]
            remove = ["left", "square", "hook", "middle", "loop",
                "extension", "logical", "vertical", "top"]
            Extract(cpset, keep, get, remove, "}", verbose="Right curly bracket")
        if not select:
            GetLeftParenthesis()
            GetRightParenthesis()
            GetLessThan()
            GetGreaterThan()
            GetLeftBracket()
            GetRightBracket()
            GetLeftCurly()
            GetRightCurly()

    def Punctuation(cpset, keep):
        def GetApostrophe():
            get = ["apostrophe", "prime"]
            remove = ["reversed", "double", "triple", "quadruple", "letter"]
            Extract(cpset, keep, get, remove, "'", verbose="Apostrophe")
        def GetExclamation():
            get = ["exclamation"]
            remove = "question squared arrow".split()
            Extract(cpset, keep, get, remove, "!", verbose="Exclamation")
        def GetComma():
            get = ["comma"]
            remove = ["digit", "double", "letter", "quotation"]
            Extract(cpset, keep, get, remove, ",", verbose="Comma")
        def GetDash():
            get = ["hyphen", "dash"]
            remove = ["triangle", "harpoon", "vertical", "arrow",
                "overline", "low line", "logical", "oblique", "diaeresis",
                "subset"]
            Extract(cpset, keep, get, remove, "-", verbose="Hyphen, dash")
        def GetPeriod():
            get = ["stop"]
            remove = ["digit", "number", "glottal", "watch", "bus",
                "square", ]
            Extract(cpset, keep, get, remove, ".", verbose="Period")
        def GetSemicolon():
            get = ["semicolon"]
            remove = []
            Extract(cpset, keep, get, remove, ";", verbose="Semicolon")
        def GetColon():
            get = ["colon"]
            remove = ["semicolon", "sign", "equal", "tri"]
            Extract(cpset, keep, get, remove, ":", verbose="Colon")
        def GetQuestion():
            get = ["question"]
            remove = ["than", "equal", "double", "exclamation"]
            Extract(cpset, keep, get, remove, "?", verbose="Question")
        def GetSpace():
            get = ["space"]
            remove = ["monospace"]
            Extract(cpset, keep, get, remove, " ", verbose="Space")
        if not select:
            GetApostrophe()
            GetComma()
            GetDash()
            GetPeriod()
            GetSemicolon()
            GetColon()
            GetQuestion()
            GetSpace()
            GetExclamation()

    def Slash_bar(cpset, keep):
        def GetSlash():
            get = ["solidus", "slash"]
            remove = ["reverse", "back", "falling", "set", "letter"]
            Extract(cpset, keep, get, remove, "/", verbose="Slash")
        def GetBackslash():
            get = ["reverse solidus", "backslash"]
            remove = ["set",]
            Extract(cpset, keep, get, remove, "\\", verbose="Backslash")
        def GetVerticalLine():
            get = ["vertical line"]
            remove = []
            Extract(cpset, keep, get, remove, "|", verbose="Vertical line")
        if not select:
            GetSlash()
            GetBackslash()
            GetVerticalLine()

    def OtherCharacters(cpset, keep):
        def GetNumberSign():
            get = ["number sign"]
            remove = []
            Extract(cpset, keep, get, remove, "#", verbose="Number sign")
        def GetDollarSign():
            get = ["dollar sign"]
            remove = []
            Extract(cpset, keep, get, remove, "$", verbose="Dollar sign")
        def GetPercentSign():
            get = ["percent sign"]
            remove = []
            Extract(cpset, keep, get, remove, "%", verbose="Percent sign")
        def GetAmpersand():
            get = ["ampersand"]
            remove = []
            Extract(cpset, keep, get, remove, "&", verbose="Ampersand")
        def GetAsterisk():
            get = ["asterisk"]
            remove = ["two", "equal"]
            Extract(cpset, keep, get, remove, "*", verbose="Asterisk")
        def GetPlusSign():
            get = ["plus sign"]
            remove = ["with", "or", "equal", "set", "circle", "triangle"]
            Extract(cpset, keep, get, remove, "+", verbose="Plus sign")
        def GetEqualSign():
            get = ["equals sign"]
            remove = ["above", "parallel", "dot", "infinity"]
            Extract(cpset, keep, get, remove, "=", verbose="Equal sign")
        def GetAtSign():
            get = ["commercial at"]
            remove = []
            Extract(cpset, keep, get, remove, "@", verbose="At sign")
        def GetCircumflex():
            get = ["circumflex"]
            remove = ["letter", "with"]
            Extract(cpset, keep, get, remove, "^", verbose="Circumflex")
        def GetUnderscore():
            get = ["low line"]
            remove = ["vertical"]
            Extract(cpset, keep, get, remove, "_", verbose="Underscore")
        def GetTilde():
            get = ["tilde"]
            remove = "letter with vertical equal set arrow not minus".split()
            Extract(cpset, keep, get, remove, "~", verbose="Tilde")
        if not select:
            GetNumberSign()
            GetDollarSign()
            GetPercentSign()
            GetAmpersand()
            GetAsterisk()
            GetPlusSign()
            GetEqualSign()
            GetAtSign()
            GetCircumflex()
            GetUnderscore()
            GetTilde()

    def Digits(cpset, keep):
        if not select:
            for n, s in (
                ("0", "Zero"),
                ("1", "One"),
                ("2", "Two"),
                ("3", "Three"),
                ("4", "Four"),
                ("5", "Five"),
                ("6", "Six"),
                ("7", "Seven"),
                ("8", "Eight"),
                ("9", "Nine")):
                get = [f"digit {s}", f"superscript {s}", f"subscript {s}",
                    f"double-struck digit {s}"]
                remove = "rod fraction".split()
                Extract(cpset, keep, get, remove, n, verbose=f"{s}")

    def Letters(cpset, keep):
        d = "double-struck"
        # Dict for superscripts & subscripts
        s = "I:ⁱᵢ N:ⁿₙ J:ⱼ T:ₜ S:ₛ P:ₚ M:ₘ L:ₗ K:ₖ H:ₕ X:ₓ O:ₒ E:ₑ A:ₐ V:ᵥ U:ᵤ R:ᵣ"
        ss = dict([i.split(":") for i in s.split()])
        if not select:
            for i in string.ascii_uppercase:
                get = [f"letter {i}$|letter {i} ", 
                    f"{d} .* {i} |{d} .* {i}$"]
                # Upper case
                remove = "small schwa".split()
                Extract(cpset, keep, get, remove, i, verbose=f"{i}")
                # Lower case
                other = set([ord(j) for j in ss[i]]) if i in ss else None
                remove = "capital schwa".split()
                Extract(cpset, keep, get, remove, i.lower(),
                    verbose=f"{i.lower()}", other=other)

    def Miscellaneous(cpset, keep):
        # Note:  set show_orig to True to print out the characters extracted
        # using regexps.  
        show_orig = True
        show_orig = False
        def Ligatures():
            if show_orig:
                get = ["ligature"]
                remove = []
                Extract(cpset, keep, get, remove, "xxLigatures", verbose="Ligatures")
                for cp in keep["xxLigatures"]:
                    print(cp, chr(cp), U.name(chr(cp)))
            else:
                keep["oe"] = set((0xa7f9,))
                # I've chosen to ignore the ligatures 128624 to 128627
        def MultipleLetters():
            if show_orig:
                get = ["letter [A-Z]{2,2} |letter [A-Z]{2,2}$", "digraph"]
                remove = ["old italic",]
                Extract(cpset, keep, get, remove, "xxMultiple_letters", verbose="Multiple letters")
            else:
                s = '''
                    Ȣ:OU ȣ:ou Ꜩ:TZ ʪ:ls ʫ:lz ꜩ:tz Ꜳ:AA ꜳ:aa Ꜵ:AO ꜵ:ao Ꜷ:AU
                    ꜷ:au ȸ:db ꜹ:av ȹ:qp Ꜹ:AV Ꜻ:AV ꜻ:av Ꜽ:AY ꜽ:ay Ꝏ:OO ꝏ:oo
                    ꭐ:ui Ꝡ:VY ꝡ:vy ꭣ:uo ᵫ:ue Ꝭ:IS ꝭ:is ꝸ:um ᵺ:th Ǽ:AE ǽ:ae
                '''
                for i in s.split():
                    c, e = i.split(":")
                    keep[e].update([ord(c)])
        def DigitStop():
            get = ["digit.*stop"]
            remove = []
            Extract(cpset, keep, get, remove, "xxDigit_stop", verbose="Digit stop")
        def DigitComma():
            get = ["digit.*comma"]
            remove = []
            Extract(cpset, keep, get, remove, "xxDigit_comma", verbose="Digit comma")
        def QuestionExcl():
            get = ["question exclamation", "exclamation question"]
            remove = []
            Extract(cpset, keep, get, remove, "xx?!", verbose="Quest. Excl.")
        def Fraction():
            get = ["fraction"]
            remove = ["slash"]
            Extract(cpset, keep, get, remove, "xxFraction", verbose="Fraction")
        def Ring():
            other = set((0xB0, 0x2DA, 0x1424, 0x18DE, 0x2218))
            if show_orig:
                get = ["ring operator", "ring point"]
                remove = []
                Extract(cpset, keep, get, remove, "xxRing", verbose="Ring", other=other)
            else:
                for cp in other:
                    keep["deg"].add(cp)
                keep["."].add(0x2e30)
        def Interrobang():
            if show_orig:
                get = ["interrobang"]
                remove = []
                Extract(cpset, keep, get, remove, "xxInterrobang", verbose="Interrobang")
            else:
                for cp in (8253, 11800, 128633, 128634, 128635):
                    keep["?!"].add(cp)
        def Plus():
            get = []
            remove = []
            other = set((
                0x016ED, 0x0271A, 0x0271B, 0x0271C, 0x1F540, 0x1F541,
                0x1F542, 0x1F7A1, 0x1F7A2, 0x1F7A3, 0x1F7A4, 0x1F7A5,
                0x1F7A6, 0x1F7A7, 0x002D6, 0x01429, 0x02064, 0x0207A,
                0x0208A, 0x02214, 0x02295, 0x0229E, 0x02795, 0x02A01,
                0x02A25, 0x02A28, 0x02A2D, 0x02A2E, 0x02A39, 0x0FE62,
                0x0FF0B))
            Extract(cpset, keep, get, remove, "+", verbose="Plus", other=other)
            keep["++"].add(0x29fa)
            keep["+++"].add(0x29fb)
        def Cross():
            get = []
            remove = []
            other = set((
                0x002DF, 0x02573, 0x26CC, 0x02694, 0x02720, 0x0274C, 0x0274E,
                0x0292B, 0x0292C, 0x02A2F))
            Extract(cpset, keep, get, remove, "x", verbose="Cross", other=other)
        def Precedes():
            if show_orig:
                get = ["precedes", "succeeds"]
                remove = ["above", "or", "not", "relation"]
                Extract(cpset, keep, get, remove, "xxPrecedes", verbose="Precedes")
            else:
                for i in "≻:> ≺:< ⪻:<< ⪼:>>".split():
                    c, e = i.split(":")
                    keep[e].update([ord(c)])
        def Square():
            s = '''
                ㏿:gal ㏟:A/m ㏞:V/m ㏝:Wb ㏜:Sv ㏛:sr ㏙:ppm ㏘:p.m. ㏗:pH
                ㏖:mol ㏕:mil ㏔:mb ㏓:lx ㏒:log ㏑:ln ㏐:lm ㏏:kt ㏌:in
                ㏋:HP ㏊:ha ㏉:GY ㏈:dB ㏇:Co. ㏆:C/kg ㏅:cd ㏄:cc ㏃:Bq
                ㏂:a.m. ㏁:Mohm ㏀:kohm ㎿:MW ㎾:kW ㎽:mW ㎼:uW ㎻:nW ㎺:pW
                ㎹:MV ㎸:kV ㎷:mV ㎶:uV ㎵:nV ㎴:pV ㎳:ms ㎲:us ㎱:ns ㎰:ps
                ㎯:rad/s^2 ㎮:rad/s ㎭:rad ㎬:GPa ㎫:MPa ㎪:kPa ㎩:Pa
                ㎨:m/s^2 ㎧:m/s ㎦:km^3 ㎥:m^3 ㎤:cm^3 ㎣:mm^3 ㎢:km^2
                ㎡:m^2 ㎠:cm^2 ㎟:mm^2 ㎞:km ㎝:cm ㎜:mm ㎛:um ㎚:nm ㎙:fm
                ㎘:kL ㎗:dL ㎖:mL ㎕:uL ㎔:THz ㎓:GHz ㎒:MHz ㎑:kHz ㎐:Hz
                ㎏:kg ㎎:mg ㎍:ug ㎌:uF ㎋:nF ㎊:pF ㎉:kcal ㎈:cal ㎇:GB
                ㎆:MB ㎅:kB ㎄:kA ㎃:mA ㎂:uA ㎁:nA ㎀:pA ㍹:dm^3 ㍸:dm^2
                ㍷:dm ㍶:pc ㍵:oV ㍴:bar ㍳:AU ㍲:da ㍱:hPa
            '''
            for i in s.split():
                c, t = i.split(":")
                keep[t].add(ord(c))
        def Other():
            keep["||"].add(0x23f8)
            keep["c/o"].add(0x2105)
            keep["c/u"].add(0x2106)
            keep["K"].add(0x212a)
            keep["degF"].add(ord("℉"))
            keep["degC"].add(ord("℃"))
            keep["(C)"].add(ord("©"))
            keep["(R)"].add(ord("®"))
            keep["+/-"].add(ord("±"))
            keep["-/+"].add(ord("∓"))
            # Superscripts & subscripts
            keep["+"].update((ord("⁺"), ord("₊")))
            keep["-"].update((ord("⁻"), ord("₋")))
            keep["="].update((ord("⁼"), ord("₌")))
            keep["("].update((ord("⁽"), ord("₍")))
            keep[")"].update((ord("⁾"), ord("₎")))
            # Math symbols
            keep["::"].add(ord("∷"))
            keep[":"].add(ord("∶"))
            keep["-:"].add(ord("∹"))
            s = '''⊘:/ ⊗:x ⊖:- ⊕:+ ⊛:* ⊠:x ⊟:- ⊞:+ ⊝:- ⊜:= ∿:~ ∾:~ ∽:~ ∼:~
                ∞:oo ∗:* ∖:\\ ∕:/ ∓:-/+ −:- ∣:| ≫:>> ≪:<< ⋙:>>> ⋘:<<<'''
            for i in s.split():
                c, t = i.split(":")
                keep[t].add(ord(c))
            # Currency
            s = '''
                ₡:<Colon> ₢:<Cruzeiro> ₣:<Franc> ₤:<Lira> ₧:<Peseta>
                ₨:<Rupee> €:<Euro> ₯:<Drachma> ₱:<Peso> ₹:<Rupee> ₽:<Ruble>
                ₿:<Bitcoin>'''
            for i in s.split():
                c, t = i.split(":")
                keep[t].add(ord(c))
            # Modifiers
            s = '''
                ʰ:h ʱ:h ʲ:j ʳ:r ʴ:r ʵ:r ʶ:R ʷ:w ʸ:y ʹ:' ʺ:" ʻ:' ʼ:' ʽ:' ˂:<
                ˃:> ˄:^ ˅:v ˆ:^ ˈ:| ˊ:' ˋ:` ˌ:| ˍ:_ ˎ:' ˏ:` ˖:+ ˗:- ˜:~ ˝:"
                ˟:x ˡ:l ˢ:s ˣ:x ˮ:" ˴:` ˵:`` ˶:" ˷:~ ꜝ:! ꜞ:! ꜟ:!'''
            for i in s.split():
                c, t = i.split(":")
                keep[t].add(ord(c))
            keep[":"].add(ord("ː"))
            keep[":"].add(ord("˸"))
        if not select:
            Ligatures()
            MultipleLetters()
            DigitStop()
            DigitComma()
            QuestionExcl()
            Fraction()
            Ring()
            Interrobang()
            Plus()
            Cross()
            Precedes()
            Square()
            Other()

def Check(cpset, keep):
    '''Verify there's no overlap between the sets in keep.
    '''
    for a, b in combinations(keep, 2):
        setA, setB = keep[a], keep[b]
        assert(not (setA & setB))
        assert(not (cpset & setA))
        assert(not (cpset & setB))

def GetAliases(cp):
    '''Return a list of the aliases of the indicated codepoint.
    '''
    if not ucd:
        return []
    try:
        group, data = ucd["chars"][cp]
    except KeyError:
        return []
    aliases = []
    if "na1" in data:
        aliases.append(data["na1"])
    if cp in ucd["aliases"]:
        for a in ucd["aliases"][cp]:
            aliases.append(a["alias"])
    return aliases

def Get(cpset, build, remove, other=None):
    '''Return (local, remove_set) where local is the set of characters
    described by the sequence of regular expressions in build and
    remove_set is the set of characters in local that were removed
    because they matched the regular expressions in the sequence remove.
    Any characters in local must not be in the dictionary decomp because
    they have already been handled.
    '''
    assert(isinstance(cpset, set))
    assert(isinstance(build, (list, tuple)))
    assert(isinstance(remove, (list, tuple)))
    if other is not None:
        assert(isinstance(other, set))
    # Compile regular expressions
    bld = [re.compile(i, re.I) for i in build]
    rem = [re.compile(i, re.I) for i in remove]
    # Build our local maximal set (cache descr for later loop)
    local = []
    for cp in cpset:
        if cp in decomp:    # It's already been handled
            continue
        c = chr(cp)
        # Check the U database's description
        descr = U.name(c)
        for b in bld:
            if b.search(descr):
                local.append((cp, descr))
        # Check aliases
        for alias in GetAliases(cp):
            for b in bld:
                if b.search(alias):
                    local.append((cp, alias))
    # Remove the indicated chars
    remove_set = set()
    for cp, descr in local:
        for r in rem:
            if r.search(descr):
                remove_set.add(cp)
    # Change local to a set of cp and don't keep any ASCII characters
    local = set(i[0] for i in local if i[0] >= 0x80)
    if other:
        local.update(other)
    local -= remove_set
    return local, remove_set

def Extract(cpset, keep, build, remove, key, verbose="", other=None):
    '''For the set of codepoints cpset, put the subset defined by build
    and remove into the keep dictionary under the indicated key.
        cpset    set of codepoints
        keep     dict{key:set(equivalent_codepoints)}
        build    list[regex]:  extract these matches from cpset
        remove   list[regex]:  remove these matches from build
        key      single character
    keep[key] = build - remove 
 
    other is a set of characters that should be kept but aren't easy to
    find with regex searches.
   
    If verbose is not the empty string and dbg is True, it is printed
    out as a header, then the removed and kept sets are printed, along
    with keep: keep[key].  This lets you see what's kept & not.
    '''
    assert(isinstance(key, str))
    assert(isinstance(verbose, str))
    local, remove_set = Get(cpset, build, remove, other=other)
    # Update sets
    if local:
        keep[key].update(local)
        cpset -= local
        # Show the results
        if dbg and verbose:
            # dbg == 1:  only print ASCII_char tab codepoints
            # dbg == 2:  Print all data
            if dbg > 1:
                print(verbose, file=stream)
                print("  Characters removed:", file=stream)
                for cp in sorted(remove_set, reverse=True):
                    PrintCP(cp, indent=" "*4)
                print("  Characters kept:", file=stream)
                for cp in sorted(local, reverse=True):
                    PrintCP(cp, indent=" "*4)
                print("  Result:", file=stream)
            c = ''.join(chr(i) for i in sorted(local))
            if dbg == 1:
                print(f"{key}\t{c}", file=stream)
            else:
                print(f"    {key}\t{c}", file=stream)
            if dbg > 1:
                n = ', '.join(f"0x{i:x}" for i in sorted(local))
                print(f"    {key}\t[{n}]", file=stream)
                print(file=stream)

def MakeScript(file, keep):
    '''Write the kept data in a form suitable for a python script's 
    str.translate use.
    '''
    f = open(file, "w")
    print(dedent(f'''
    # Constructed {time.asctime()} by {sys.argv[0]}
 
    # This dictionary can be used by str.translate to "asciify" Unicode
    # text by converting non-7-bit Unicode characters to their (rough)
    # ASCII equivalents.
 
    ascii_translate = {{'''[1:]), file=f)
    s = []
    for c in keep:
        for cp in keep[c]:
            s.append((cp, repr(c)))
    for cp in decomp:
        s.append((cp, repr(decomp[cp])))
    for cp, c in sorted(s):
        print(f"    0x{cp:x}: {c},", file=f)
    print(f'''}}
if __name__ == "__main__": 
    import sys
    s = sys.stdin.read()
    print(s.translate(ascii_translate))
''', file=f)
    print(f"Wrote '{file}'", file=sys.stderr)

def MakeTestFile(file, keep):
    '''This function writes the data in keep to file, which can be used
    to test the transliteration facilities.  The output format is the
    key ASCII character, followed by a tab, followed by the Unicode
    characters that should be mapped to it.  After the transliteration,
    the line should contain all the same characters with one tab
    character.
    '''
    f = open(file, "w")
    for key in decomp:
        keep[decomp[key]].add(key)
    for key in keep:
        u = ''.join([chr(i) for i in keep[key]])
        print(f"{key}\t{u}", file=f)
    print(f"Wrote '{file}'", file=sys.stderr)

def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] [output_file]
 
    -d dbg      Debug level
    -f          Force a rebuild
    -s          Set select to True
    '''[1:-1]))
    exit(status)

def ParseCommandLine(d):
    d["-d"] = 0
    d["-f"] = False
    d["-s"] = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:fhs")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("fs"):
            d[o] = not d[o]
        if o == "-d":
            d[o] = int(a)
        elif o == "-h":
            Usage(d)
    return args

def IsASCII(s):
    '''Return True if string s is composed of all ASCII characters.
    Note it returns True for the empty string.
    '''
    return all(ord(i) < 0x80 for i in s)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

def Decompose(char):
    '''Return the decomposed string or '' if there is no suitable one.
    '''
    # Make a dictionary to translate some of the strings like "⁄"
    T = {
        0x2044: "/",
        0x2215: "/",
        0x03A9: "ohm",
        0x0301: "'",
        0x0327: ",",
    }
    for cp in range(768, 880):      # Remove combining characters
        T[cp] = None
    s = char
    while s and not IsASCII(s):
        t = []
        for c in s:
            if IsASCII(c):
                t.append(c)
            else:
                d = U.decomposition(c)
                if not d:
                    continue
                f = d.split()
                if f[0].startswith("<"):
                    f = f[1:]
                t.append(chr(int(i, 16)).translate(T) for i in f)
        s = ''.join(flatten(t))
    # Manual fixes:  there are some characters that should have ''
    # returned because the above routine returns e.g. ' ' for them, but
    # they are not space-like characters.
    not_ok = set((
        0x203e, 0x2017, 0x2dd, 0x2dc, 0x2da, 0x2d9, 0x2d8, 0xb8, 0xb4,
        0xaf, 0xa8
    ))
    if s == " " and ord(char) in not_ok: 
        return ""
    elif char in set("℉℃₨"):
        return ""
    return s

def Decomp(cpset, decomp):
    '''Use decomposition to construct conversions.  decomp is a
    dictionary to store the codepoints and their conversions in.
    '''
    remove = set()
    for cp in sorted(cpset, reverse=1):
        if cp < 0x80:
            continue
        t = Decompose(chr(cp))
        if t:
            decomp[cp] = t
            remove.add(cp)
    cpset -= remove

def GetTranslations():
    cpset, keep = GetWorkingSet()
    Decomp(cpset, decomp)
    # Build keep dictionary
    Quotes(cpset, keep)
    Brackets(cpset, keep)
    Punctuation(cpset, keep)
    Slash_bar(cpset, keep)
    OtherCharacters(cpset, keep)
    Digits(cpset, keep)
    Letters(cpset, keep)
    Miscellaneous(cpset, keep)
    # Make sure all items in keep are sets
    for i in keep:
        assert(isinstance(keep[i], set))
    # Output data
    MakeScript("asciify.script", keep)
    MakeTestFile("asciify.test", keep)

if __name__ == "__main__": 
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    decomp = {} # Codepoints that could be decomposed
    trans = {}  # Contains the final translate dictionary
    fmt = "  {:30s} {:8d}" # Used for debug printing to stderr
    # If select is True, only do the tasks currently being worked on
    select = True if d["-s"] else False
    # Set to 0 for no debug output, 1 for only title & result, 2 for all
    dbg = d["-d"]
    #stream = open(args[0], "w") if args else sys.stdout
    stream = sys.stdout
    GetTranslations()

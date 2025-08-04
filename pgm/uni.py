'''
TODO

    - Add -u option that prints out all non-7-bit ASCII characters from
      stdin.
    - Add an option that prints out all characters that can be used as
      python symbols.
      
Utility to look up Unicode characters

----------------------------------------------------------------------
Overview of program structure

cpset is a set of integers of all valid codepoints
If you give symbol x on command line, Lookup('x', d) is called
For codepoint cp:
    PrintCodepointDetails(cp, d)
    
'''
if 1:   # Header
    # Copyright (C) 2019 Don Peterson
    # Contact:  gmail.com@someonesdad1
    #
    # Licensed under the Open Software License version 3.0.
    # See http://opensource.org/licenses/OSL-3.0.
    #
    if 1:   # Standard imports
        import bisect
        import getopt
        from pprint import pprint as pp
        import pathlib
        import re
        import sys
        import unicodedata
        from collections import defaultdict
        from textwrap import dedent
    if 1:   # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
        # Color coding
        try:
            from color import PrintMatch, lred, black, Style
            MatchStyle = Style(lred, black)
        except ImportError:
            MatchStyle = None
            def PrintMatch(text, regexp, style):
                print(text)
        # Unicode Character Database (http://www.unicode.org/reports/tr44/) 
        #
        # Note the UCD version may be different than the Unicode version python is
        # using.  Download the latest Unicode UCD from
        # http://www.unicode.org/Public/UCD/latest/ucdxml.  I recommend you keep the
        # latest version on-hand, as it will work fine with older python unicodedata
        # modules.
        try:
            from ucd import ucd
        except ImportError:
            ucd = None
def GetCharacterSet(d):
    'Return the set of integers cpset, representing the valid Unicode codepoints'
    # 0x110000 is 1,114,112 and 0x10000 is 65536 == 2**16
    maxcp = 0x110000 if d["-a"] else 0x10000
    cpset = set(range(maxcp))
    # Remove invalid codepoints
    remove = set()
    for cp in cpset:
        try:
            unicodedata.name(chr(cp))
        except ValueError:
            remove.add(cp)
    cpset -= remove
    if d["-e"]:  # Remove non-English characters
        languages = list(set('''
 
            adlam admetos aegean afghani ahom anatolian arabian arabic armenian avestan
            balinese bamum bassa batak bengali bhaiksuki bopomofo brahmi buginese buhid
            byzantine canadian carian caucasian chakma cham cherokee cjk coptic
            cuneiform cypriot cyrillic deseret devanagari dogra duployan egyptian
            egyptological elbasan ethiopic ewa functional georgian geta glagolitic
            grantha greek gujarati gunjala gurmukhi halfwidth hangul hangzhou hanifi
            hanunoo hatran hebrew hentaigana hexagram hieroglyph hiragana hom hungarian
            ideogram ideograph ideographic imperial indic inscriptional interlinear
            japanese javanese kaithi kangxi kannada katakana kayah kharoshthi khmer
            khojki khudawadi korean lao lepcha limbu linear lisu lycian lydian mahajani
            mahjong makasar malayalam mandaic manichaean marchen masaram mayan
            medefaidrin meetei mende meroitic miao modi mongolian mro multani myanmar
            nabataean nandinagari nko nomisma nushu nyiakeng object ogham ogonek ol
            oriya osage osmanya pahawh pahlavi palmyrene parthian pau permic persian
            phags-pa phaistos philippine phoenician psalter rejang rumi runic samaritan
            saurashtra shakti sharada shavian siddham sinhala slavonic sogdian sora
            soyombo sundanese svasti syloti syriac tagalog tagbanwa tai takri tamil
            tangut telugu tetragram thaana thai tibetan tifinagh tirhuta turkic ugaritic
            vai vedic wancho warang xiangqi yi zanabazar newa
 
        '''.upper().split()))
        l = [r"\b" + i + r"\b" for i in languages]  # Add word boundaries
        ignore = re.compile("|".join(l))
        remove = set()
        # Also remove some Japanese special characters
        sq = set(range(0x3300, 0x3358))
        sq.update(range(0x337B, 0x3380))
        remove.update(sq)
        for cp in cpset:
            descr = unicodedata.name(chr(cp))
            if ignore.search(descr):
                remove.add(cp)
        cpset -= remove
    if d["-v"]:
        mn, mx = min(cpset), max(cpset)
        print(dedent(f'''
        Unicode database version = {unicodedata.unidata_version}
          {len(cpset)} characters in codepoint set
          min = {mn} = 0x{mn:X}, max = {mx} = 0x{mx:X}
        '''))
    return cpset
def ASCII_name(cp):
    assert 0 <= cp < 0x20
    s = (
        "NULL",
        "START OF HEADING",
        "START OF TEXT",
        "END OF TEXT",
        "END OF TRANSMISSION",
        "ENQUIRY",
        "ACKNOWLEDGE",
        "BELL",
        "BACKSPACE",
        "CHARACTER TABULATION",
        "LINE FEED",
        "LINE TABULATION",
        "FORM FEED",
        "CARRIAGE RETURN",
        "SHIFT OUT",
        "SHIFT IN",
        "DATA LINK ESCAPE",
        "DEVICE CONTROL ONE",
        "DEVICE CONTROL TWO",
        "DEVICE CONTROL THREE",
        "DEVICE CONTROL FOUR",
        "NEGATIVE ACKNOWLEDGE",
        "SYNCHRONOUS IDLE",
        "END OF TRANSMISSION BLOCK",
        "CANCEL",
        "END OF MEDIUM",
        "SUBSTITUTE",
        "ESCAPE",
        "INFORMATION SEPARATOR FOUR",
        "INFORMATION SEPARATOR THREE",
        "INFORMATION SEPARATOR TWO",
        "INFORMATION SEPARATOR ONE",
    )
    return f"ASCII CONTROL {s[cp]}"
def ASCII_symbol(cp):
    assert 0 <= cp < 0x20
    s = '''nul soh stx etx eot enq ack bel bs ht lf vt ff cr so si
           dle dc1 dc2 dc3 dc4 nak syn etb can em sub esc fs gs rs
           us'''.split()
    return "<" + s[cp] + ">"
def GetBlockName(cp):
    # Construct three equal-length arrays for the start cp, end cp,
    # and name.
    starts, ends, names = [], [], []
    for s, e, n in ucd["blocks"]:
        starts.append(s)
        ends.append(e)
        names.append(n)
    # Note they must be sorted in increasing starts order for this to
    # work.
    index = find_le(starts, cp)
    if index is None:
        return None
    assert starts[index] <= cp
    if ends[index] < cp:
        return "None"
    return names[index]
def find_le(a, x):
    '''Return the index of the rightmost value <= x.  Adapted from the
    recipe in python's documentation on the bisect module.
    '''
    index = bisect.bisect_right(a, x)
    if index:
        return index - 1
    return None
def PrintUCDData(cp, d):
    if not ucd:
        return
    try:
        group, data = ucd["chars"][cp]
    except KeyError:
        return
    print(f"  Data from Unicode Character Database {ucd['version']}")
    g = ucd["groups"][group]
    c, i = chr(cp), " " * 4
    if cp in (10, 11, 12, 13):
        c = " "
    if "na1" in data:
        print(f"{i}Alternate name = {data['na1']}")
    if cp in ucd["aliases"]:
        for a in ucd["aliases"][cp]:
            alias, typ = a["alias"], a["type"]
            print(f"{i}Alias = {alias} (type = {typ})")
    if "age" in g:
        print(f"{i}Age = {g['age']}")
    print(f"{i}Category = {g['gc']}")
    block = GetBlockName(cp)
    if block is not None:
        print(f"{i}Block = {block}")
def GetDecomp(cp):
    try:
        decomp = unicodedata.decomposition(chr(cp))
        f, t = decomp.split(), ""
        if f[0].startswith("<"):
            t, f = f[0], f[1:]
        t += " ".join(chr(int(i, 16)) for i in f)
        return t
    except Exception:
        return ""
def IsPythonSymbol(cp):
    "Return True if codepoint is allowed in python symbol"
    try:
        if cp in set((9, 12, 32, 35)):  # tab, formfeed, space, comment
            return False
        else:
            # '_' is used first so the character can e.g. be a digit
            exec(f"_{chr(cp)} = 0")
            return True
    except Exception:
        return False
def PrintCodepointDetails(cp, d):
    c = chr(cp)
    sym = "yes" if IsPythonSymbol(cp) else "no"
    if 0 <= cp < 0x20:
        # Handle the ASCII control characters specially because
        # the unicodedata module doesn't contain them.
        c = ASCII_symbol(cp)
        name = ASCII_name(cp)
    else:
        name = unicodedata.name(c)
    print(
        f'''
Data on codepoint U+{cp:0X} = character {c}
  Decimal = {cp}, octal = {cp:o}, binary = {cp:b}
  Name = {name}
  Allowed in python symbol = {sym}'''[1:]
    )
    decomp = unicodedata.decomposition(c)
    if decomp:
        try:
            f = decomp.split()
            if f[0][0] == "<":
                f = f[1:]
            t = " ".join(chr(int(i, 16)) for i in f)
            print(f"  Decomposition = {decomp} = {t}")
        except Exception:
            pass
    print("  Encodings:")
    # Print a form that can be pasted into C/C++ code
    print("    C/C++    ", end="")
    print(f'"', end="")
    for b in chr(cp).encode("utf-8"):
        print(f"\\x{b:0x}", end="")
    print(f'"')
    for enc in ("utf-8", "utf-16", "utf-32"):
        print(f"    {enc:8s} ", end="")
        for b in chr(cp).encode(enc):
            print(f"{b:02x} ", end="")
        print()
    PrintUCDData(cp, d)  # Print data from Unicode Character Database
    if d["-v"] and not (0 <= cp < 0x20):
        # Print extra data from unicodedata
        s, n = " " * 4, 18
        print("  Extra unicodedata information:")
        try:
            print(f"{s}{'Decimal':{n}s}", unicodedata.decimal(c))
        except ValueError:
            print(f"{s}{'Decimal':{n}s}", "not a decimal")
        try:
            print(f"{s}{'Digit':{n}s}", unicodedata.digit(c))
        except ValueError:
            print(f"{s}{'Digit':{n}s}", "not a digit")
        try:
            print(f"{s}{'Numeric':{n}s}", unicodedata.numeric(c))
        except ValueError:
            print(f"{s}{'Numeric':{n}s}", "not a numeric")
        print(f"{s}{'Category':{n}s}", unicodedata.category(c))
        print(f"{s}{'Bidirectional':{n}s}", unicodedata.bidirectional(c))
        print(f"{s}{'Combining':{n}s}", unicodedata.combining(c))
        print(f"{s}{'East Asian width':{n}s}", unicodedata.east_asian_width(c))
        print(f"{s}{'Mirrored':{n}s}", unicodedata.mirrored(c))
        print(f"{s}{'Decomposition':{n}s}", unicodedata.decomposition(c))
        print(f"{s}Normalization:")
        for form in "NFC NFKC NFD NFKD".split():
            print(f"{s}  {form:^4s}", unicodedata.normalize(form, c))
    if len(d["args"]) > 1 and not d["last"]:
        # Print a newline to separate grouped lines
        print()
def PrintByGroup(d):
    s = '''
    Lu :Uppercase_Letter :an uppercase letter
    Ll :Lowercase_Letter :a lowercase letter
    Lt :Titlecase_Letter :a digraphic character, with first part uppercase
    LC :Cased_Letter :Lu, Ll, Lt
    Lm :Modifier_Letter :a modifier letter
    Lo :Other_Letter :other letters, including syllables and ideographs
    L :Letter :Lu, Ll, Lt, Lm, Lo
    Mn :Nonspacing_Mark :a nonspacing combining mark (zero advance width)
    Mc :Spacing_Mark :a spacing combining mark (positive advance width)
    Me :Enclosing_Mark :an enclosing combining mark
    M :Mark :Mn, Mc, Me
    Nd :Decimal_Number :a decimal digit
    Nl :Letter_Number :a letterlike numeric character
    No :Other_Number :a numeric character of other type
    N :Number :Nd, Nl, No
    Pc :Connector_Punctuation :a connecting punctuation mark, like a tie
    Pd :Dash_Punctuation :a dash or hyphen punctuation mark
    Ps :Open_Punctuation :an opening punctuation mark (of a pair)
    Pe :Close_Punctuation :a closing punctuation mark (of a pair)
    Pi :Initial_Punctuation :an initial quotation mark
    Pf :Final_Punctuation :a final quotation mark
    Po :Other_Punctuation :a punctuation mark of other type
    P :Punctuation :Pc, Pd, Ps, Pe, Pi, Pf, Po
    Sm :Math_Symbol :a symbol of mathematical use
    Sc :Currency_Symbol :a currency sign
    Sk :Modifier_Symbol :a non-letterlike modifier symbol
    So :Other_Symbol :a symbol of other type
    S :Symbol :Sm, Sc, Sk, So
    Zs :Space_Separator :a space character (of various non-zero widths)
    Zl :Line_Separator :U+2028 LINE SEPARATOR only
    Zp :Paragraph_Separator :U+2029 PARAGRAPH SEPARATOR only
    Z :Separator :Zs, Zl, Zp
    Cc :Control :a C0 or C1 control code
    Cf :Format :a format control character
    Cs :Surrogate :a surrogate code point
    Co :Private_Use :a private-use character
    Cn :Unassigned :a reserved unassigned code point or a noncharacter
    '''.strip().split("\n")
    # Put this data into a dictionary for group header information
    gcdata = {}
    for line in s:
        gc, long, descr = [i.strip() for i in line.split(":")]
        long = long.replace("_", " ")
        gcdata[gc] = f"{long} ({descr})"
    no_category = ""
    gcdata[no_category] = "No general category available"
    # Construct a dictionary indexed by category with each codepoint it
    # contains.
    G = defaultdict(list)  # Dictionary to organize by group
    for cp in cpset:
        try:
            group, data = ucd["chars"][cp]
            g = ucd["groups"][group]
            gc = g["gc"]  # General category
            G[gc].append(cp)
        except KeyError:
            G[no_category].append(cp)
    # Now print out by categories
    for gc in sorted(G):
        s = "" if gc == "" else gc + " "
        print(f"{s}{gcdata[gc]}")
        for cp in G[gc]:
            PrintCP(cp, indent=" " * 2, decomp=True)
        print()
def DumpBlocks(args, d):
    '''Dump the common blocks; if -a is True, then dump all the blocks.
    If args is not empty, print out all the characters in the blocks
    that match these regular expressions.
    '''
    # Note:  these block names came from UCD version 12.1.0.
    common = set()
    for i in '''
        Alchemical_Symbols Alphabetic_Presentation_Forms Arrows
        Basic_Latin Block_Elements Box_Drawing Braille_Patterns
        Chess_Symbols Combining_Diacritical_Marks
        Combining_Diacritical_Marks_Extended
        Combining_Diacritical_Marks_Supplement
        Combining_Diacritical_Marks_for_Symbols Control_Pictures
        Counting_Rod_Numerals Currency_Symbols Dingbats Domino_Tiles
        Emoticons Enclosed_Alphanumeric_Supplement
        Enclosed_Alphanumerics General_Punctuation Geometric_Shapes
        Geometric_Shapes_Extended IPA_Extensions Latin-1_Supplement
        Latin_Extended-A Latin_Extended-B Latin_Extended-C
        Latin_Extended-D Latin_Extended-E Latin_Extended_Additional
        Letterlike_Symbols Mahjong_Tiles
        Mathematical_Alphanumeric_Symbols Mathematical_Operators
        Miscellaneous_Mathematical_Symbols-A
        Miscellaneous_Mathematical_Symbols-B Miscellaneous_Symbols
        Miscellaneous_Symbols_and_Arrows
        Miscellaneous_Symbols_and_Pictographs Miscellaneous_Technical
        Musical_Symbols Number_Forms Optical_Character_Recognition
        Ornamental_Dingbats Phonetic_Extensions
        Phonetic_Extensions_Supplement Playing_Cards
        Shorthand_Format_Controls Spacing_Modifier_Letters
        Superscripts_and_Subscripts Supplemental_Arrows-A
        Supplemental_Arrows-B Supplemental_Arrows-C
        Supplemental_Mathematical_Operators Supplemental_Punctuation
        Supplemental_Symbols_and_Pictographs Sutton_SignWriting
        Symbols_and_Pictographs_Extended-A Transport_and_Map_Symbols
        '''.split():
        common.add(i.replace("_", " "))
    other = set()
    for i in '''
        Adlam Aegean_Numbers Ahom Anatolian_Hieroglyphs
        Ancient_Greek_Musical_Notation Ancient_Greek_Numbers
        Ancient_Symbols Arabic Arabic_Extended-A
        Arabic_Mathematical_Alphabetic_Symbols
        Arabic_Presentation_Forms-A Arabic_Presentation_Forms-B
        Arabic_Supplement Armenian Avestan Balinese Bamum
        Bamum_Supplement Bassa_Vah Batak Bengali Bhaiksuki Bopomofo
        Bopomofo_Extended Brahmi Buginese Buhid
        Byzantine_Musical_Symbols CJK_Compatibility
        CJK_Compatibility_Forms CJK_Compatibility_Ideographs
        CJK_Compatibility_Ideographs_Supplement CJK_Radicals_Supplement
        CJK_Strokes CJK_Symbols_and_Punctuation CJK_Unified_Ideographs
        CJK_Unified_Ideographs_Extension_A
        CJK_Unified_Ideographs_Extension_B
        CJK_Unified_Ideographs_Extension_C
        CJK_Unified_Ideographs_Extension_D
        CJK_Unified_Ideographs_Extension_E
        CJK_Unified_Ideographs_Extension_F Carian Caucasian_Albanian
        Chakma Cham Cherokee Cherokee_Supplement Combining_Half_Marks
        Common_Indic_Number_Forms Coptic Coptic_Epact_Numbers Cuneiform
        Cuneiform_Numbers_and_Punctuation Cypriot_Syllabary Cyrillic
        Cyrillic_Extended-A Cyrillic_Extended-B Cyrillic_Extended-C
        Cyrillic_Supplement Deseret Devanagari Devanagari_Extended Dogra
        Duployan Early_Dynastic_Cuneiform
        Egyptian_Hieroglyph_Format_Controls Egyptian_Hieroglyphs Elbasan
        Elymaic Enclosed_CJK_Letters_and_Months
        Enclosed_Ideographic_Supplement Ethiopic Ethiopic_Extended
        Ethiopic_Extended-A Ethiopic_Supplement Georgian
        Georgian_Extended Georgian_Supplement Glagolitic
        Glagolitic_Supplement Gothic Grantha Greek_Extended
        Greek_and_Coptic Gujarati Gunjala_Gondi Gurmukhi
        Halfwidth_and_Fullwidth_Forms Hangul_Compatibility_Jamo
        Hangul_Jamo Hangul_Jamo_Extended-A Hangul_Jamo_Extended-B
        Hangul_Syllables Hanifi_Rohingya Hanunoo Hatran Hebrew
        High_Private_Use_Surrogates High_Surrogates Hiragana
        Ideographic_Description_Characters
        Ideographic_Symbols_and_Punctuation Imperial_Aramaic
        Indic_Siyaq_Numbers Inscriptional_Pahlavi Inscriptional_Parthian
        Javanese Kaithi Kana_Extended-A Kana_Supplement Kanbun
        Kangxi_Radicals Kannada Katakana Katakana_Phonetic_Extensions
        Kayah_Li Kharoshthi Khmer Khmer_Symbols Khojki Khudawadi Lao
        Lepcha Limbu Linear_A Linear_B_Ideograms Linear_B_Syllabary Lisu
        Low_Surrogates Lycian Lydian Mahajani Makasar Malayalam Mandaic
        Manichaean Marchen Masaram_Gondi Mayan_Numerals Medefaidrin
        Meetei_Mayek Meetei_Mayek_Extensions Mende_Kikakui
        Meroitic_Cursive Meroitic_Hieroglyphs Miao Modi
        Modifier_Tone_Letters Mongolian Mongolian_Supplement Mro Multani
        Myanmar Myanmar_Extended-A Myanmar_Extended-B NKo Nabataean
        Nandinagari New_Tai_Lue Newa Nushu Nyiakeng_Puachue_Hmong Ogham
        Ol_Chiki Old_Hungarian Old_Italic Old_North_Arabian Old_Permic
        Old_Persian Old_Sogdian Old_South_Arabian Old_Turkic Oriya Osage
        Osmanya Ottoman_Siyaq_Numbers Pahawh_Hmong Palmyrene Pau_Cin_Hau
        Phags-pa Phaistos_Disc Phoenician Private_Use_Area
        Psalter_Pahlavi Rejang Rumi_Numeral_Symbols Runic Samaritan
        Saurashtra Sharada Shavian Siddham Sinhala
        Sinhala_Archaic_Numbers Small_Form_Variants Small_Kana_Extension
        Sogdian Sora_Sompeng Soyombo Specials Sundanese
        Sundanese_Supplement Supplementary_Private_Use_Area-A
        Supplementary_Private_Use_Area-B')) Syloti_Nagri Syriac
        Syriac_Supplement Tagalog Tagbanwa Tags Tai_Le Tai_Tham Tai_Viet
        Tai_Xuan_Jing_Symbols Takri Tamil Tamil_Supplement Tangut
        Tangut_Components Telugu Thaana Thai Tibetan Tifinagh Tirhuta
        Ugaritic Unified_Canadian_Aboriginal_Syllabics
        Unified_Canadian_Aboriginal_Syllabics_Extended Vai
        Variation_Selectors Variation_Selectors_Supplement
        Vedic_Extensions Vertical_Forms Wancho Warang_Citi Yi_Radicals
        Yi_Syllables Yijing_Hexagram_Symbols Zanabazar_Square
        '''.split():
        other.add(i.replace("_", " "))
    # Get the set of block names to use
    blocks = (common | other) if d["-a"] else common
    u = ucd["blocks"]
    b = "(decimal)" if d["-d"] else "(hex)"
    if args:
        # Print the characters in the indicated blocks
        blocklist = []
        for regex in args:
            r = re.compile(regex, re.I)
            for start, end, name in u:
                if r.search(name):
                    blocklist.append((start, end, name))
        for start, end, name in blocklist:
            print(f"Block:  {name}")
            for cp in range(start, end + 1):
                if cp in cpset:
                    PrintCP(cp, indent=" " * 2)
    else:
        print(f"Block definitions {b}:")
        for start, end, name in u:
            if name in blocks:
                if d["-d"]:  # Use decimal numbers
                    print(f"  {start:7d} {end:7d}  {name}")
                else:  # Use hex numbers
                    print(f"  U+{start:06X} U+{end:06X}  {name}")
def PrintCP(cp, regex=None, indent="", decomp=False):
    '''Print the indicated codepoint.  If regex is not None, it is the
    regular expression that matched the description.  If decomp is True,
    append the decomposition if it is available.
    '''
    if 0 <= cp < 0x20:
        c = ASCII_symbol(cp)
        descr = ASCII_name(cp)
    else:
        c = chr(cp)
        try:
            descr = unicodedata.name(c)
        except ValueError:
            descr = "<no name for U+{cp:04X}>"
    if d["-d"]:  # Use decimal numbers
        if d["-a"]:  # Full set of codepoints
            print(f"{indent} {cp:6d} {c:^5s}", end=" ")
        else:
            print(f"{indent} {cp:5d} {c:^5s}", end=" ")
    else:  # Use U+ (hex) notation
        if d["-a"]:
            print(f"{indent}U+{cp:05X} {c:^5s}", end=" ")
        else:
            print(f"{indent}U+{cp:04X} {c:^5s}", end=" ")
    if decomp:
        dc = GetDecomp(cp)
        if dc:
            descr = f"{descr} [{dc}]"
    if regex is None:
        print(descr)
    else:
        if d["-c"] and sys.stdout.isatty():
            PrintMatch(descr, regex, MatchStyle)
        else:
            print(descr)
def GetAliases(cp):
    '''Return a list of the aliases of the indicated codepoint.'''
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
def LookUp(expr, d):
    '''If expr is a number (hex or base 10), print out the
    characteristics of the Unicode codepoint.  expr can be two numbers
    separated by a hyphen, giving a range of codepoints to print.
    Otherwise, expr is interpreted as a regular expression that is used
    to search the Unicode names; matches are printed to stdout.  If expr
    is a single character, look up that character.
    '''
    if not expr:
        return
    def Int(x):
        return int(x) if d["-d"] else int(x, 16)
    # If expr contains a '-' character, see if it can be interpreted as
    # a range of integers.
    if len(expr) > 1 and "-" in expr and not d["-t"]:
        try:
            start, end = [Int(i) for i in expr.split("-")]
            if start > end:
                start, end = end, start
            for cp in reversed(range(start, end + 1)):
                if cp in cpset or (0 <= cp < 0x20):
                    PrintCP(cp, None)
            return
        except Exception:
            pass
    # If expr contains a ':' character, see if it can be interpreted as
    # two integers.
    if len(expr) > 1 and ":" in expr and not d["-t"]:
        try:
            start, num = [Int(i) for i in expr.split(":")]
            for cp in reversed(range(start, start + num)):
                if cp in cpset or (0 <= cp < 0x20):
                    PrintCP(cp, None)
            return
        except Exception:
            pass
    try:
        if d["-t"]:  # Force a regular expression search
            raise Exception()
        if len(expr) == 1:
            if ord(expr) in cpset:
                # Show details on this character
                PrintCodepointDetails(ord(expr), d)
            else:
                raise Exception()
        else:
            if expr.upper().startswith("U+") and len(expr) > 2:
                h = int(expr[2:], 16)
                PrintCodepointDetails(h, d)
            else:
                PrintCodepointDetails(Int(expr), d)
    except Exception:  # Regular expression search
        r = re.compile(expr, re.I)
        for cp in sorted(cpset, reverse=True):
            descr = unicodedata.name(chr(cp))
            if r.search(descr):
                PrintCP(cp, r)
                continue
            # Also check alternate descriptions
            for descr in GetAliases(cp):
                if r.search(descr):
                    PrintCP(cp, r)
                    break
def ParseCommandLine(d):
    d["-a"] = False  # Generate all characters
    d["-b"] = False  # Dump block information
    d["-c"] = True  # Use color
    d["-D"] = False  # Print all characters
    d["-d"] = False  # Decimal numbers
    d["-e"] = False  # Remove non-English characters
    d["-g"] = False  # Like -D, but print by group (general category)
    d["-P"] = False  # Print python symbols
    d["-p"] = False  # Print python symbols (limited)
    d["-s"] = False  # Print data on command line strings
    d["-t"] = False  # Force text
    d["-v"] = False  # Verbose
    try:
        opts, args = getopt.getopt(sys.argv[1:], "abcDdegPpstv")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("abcDdegPpstv"):
            d[o] = not d[o]
    if (
        not d["-D"]
        and not d["-b"]
        and not d["-g"]
        and not d["-P"]
        and not d["-p"]
        and not args
    ):
        Usage(d, status=0)
    if d["-D"] or d["-g"]:
        d["-a"] = True
    return args
def Usage(d, status=1):
    name = pathlib.PurePath(sys.argv[0]).name
    eng = ("Don't r" if d["-e"] else "R") + "emove non-English characters."
    col = ("Don't p" if d["-c"] else "P") + "rint in color."
    print(
        f'''
Usage:  {name} [options] r1 [r2 ...]
  Look up r1 in the Unicode character database.  If r1 is a codepoint
  number (hex by default; use -d for decimal), then print out data on
  that character.  Otherwise, it's a python regular expression to search
  for Unicode characters whose description matches that expression (if
  it's a single character, look up that character's data).  Repeat for
  other arguments.  If the argument contains a hyphen, a range of
  codepoints is printed; a colon means to start at the first codepoint
  and print the second number of codepoints.  Searches are
  case-insensitive.
  
  Version data:
    ucd.py's data:      {ucd["version"].replace("Unicode", "")}
    Python unicodedata:  {unicodedata.unidata_version}
    
Examples:
  python {name} α β ɣ
      Show details on the first three Greek lower-case letters.
  python {name} -d 10:4
      Show the four characters starting at ASCII 10 (line feed).
      Note the lowest codepoint is printed last.
  python {name} 'digit one'
      Show characters whose descriptions contain 'digit one'.
  python {name} -e 'digit one'
      Same except remove non-English languages.
  python {name} -D 
      Show all valid Unicode characters.
  python {name} -s √αβɣδ café
      Show names for the indicated characters in the words.
Options:
  -a  Use all valid Unicode characters.  The default set uses the
      Basic Multilingual Plane up to U+FFFF.
'''[:-1]
    )
    if ucd is not None:
        print("  -b  Dump block information")
    print(
        f'''
  -c  {col}
  -D  Print the descriptions of all valid Unicode characters.
  -d  Numbers on command line are decimal (hex is the default).
  -e  {eng}
  -g  Like -D, but organize by category
  -P  Print out characters that are valid python symbols
  -p  Print out characters that are valid python symbols (<U+03E2)
  -s  Print the data on the characters in the command line strings
  -t  Force a textual lookup (e.g., without this 'face' is
      interpreted as a hex number).
  -v  Verbose printing (show database characteristics and extra help).
  
Some useful Unicode characters:
  ¹/₁₆ ¹/₈ ³/₁₆ ¹/₄ ⁵/₁₆ ³/₈ ⁷/₁₆ ¹/₂ ⁹/₁₆ ⁵/₈ ¹¹/₁₆ ³/₄ ¹³/₁₆ ⁷/₈ ¹⁵/₁₆ 
  ¹/₃₂ ³/₃₂ ⁵/₃₂ ⁷/₃₂ ⁹/₃₂ ¹¹/₃₂ ¹³/₃₂ ¹⁵/₃₂ ¹⁷/₃₂ ¹⁹/₃₂ ²¹/₃₂ ²³/₃₂ ²⁵/₃₂
  ²⁷/₃₂ ²⁹/₃₂ ³¹/₃₂     ¹/₆₄ ³/₆₄ ⁵/₆₄ ⁷/₆₄ ⁹/₆₄ ¹¹/₆₄ ¹³/₆₄ ¹⁵/₆₄ ¹⁷/₆₄
  ¹⁹/₆₄ ²¹/₆₄ ²³/₆₄ ²⁵/₆₄ ²⁷/₆₄ ²⁹/₆₄ ³¹/₆₄ ³³/₆₄ ³⁵/₆₄ ³⁷/₆₄ ³⁹/₆₄ ⁴¹/₆₄
  ⁴³/₆₄ ⁴⁵/₆₄ ⁴⁷/₆₄ ⁴⁹/₆₄ ⁵¹/₆₄ ⁵³/₆₄ ⁵⁵/₆₄ ⁵⁷/₆₄ ⁵⁹/₆₄ ⁶¹/₆₄ ⁶³/₆₄ 
  ° Ω θ μ π · × ÷ √ α β ɣ δ Δ ɛ ϵ ϶ ν ξ ψ φ ϕ ζ λ ρ σ τ χ ω Γ Φ Ξ Λ Σ ♠ ♣ ♥ ♦
  ± ∞ ∂ ∫ ∼ ∝ ∓ ∍ ∊ ∈ ∉ ∅ ∃ « » ∀ ∡ ∠ ∟ ∥ ∦ ℝ ℂ ℤ ℕ ℚ ℐ ℛ ⊙ ⊗ ⊕ ⊉ ⊈ ⊇ ⊆ ⊅ ⊄ ⊃ ⊂
  ≅ ≤ ≥ ≪ ≫ ≈ ≠ ≡ ≢ ≝ ≟ ∧ ∨ ∩ ∪ ∴ ⅛ ¼ ⅜ ½ ⅝ ¾ ⅞ ⍈ █ ∎
  © ® ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↺ ↻ ⇐ ⇑ ⇒ ⇓ ⇔ ⇦ ⇧ ⇨ ⇩ ⭍ ⭠ ⭡ ⭢ ⭣ ⭤ ⭥ ⭮ ⭯ ￪ ￬
  Superscripts: ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱⁿ
  Subscripts:   ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓᵦᵩ
'''[1:-1]
    )
    '''
    https://www.unicode.org/reporting.html  unicode@unicode.org On 28
    May 2021 I subscribed to the Unicode mailing list.  When I am
    confirmed, submit an enhancement request for all letters, numbers,
    and punctuation symbols as subscripts and superscripts.  I've been
    wanting this for years, as I am unable to properly display physical
    units.
    '''
    if not d["-v"]:
        exit(status)
    print(
        dedent(
            f'''
            
    - You'll get extra information on characters if you download and
      install the Unicode Character Database, but it's not required.
      See the instructions in the ucd.py module included with this
      script.
      
      - If you do download the UCD, you'll find more characters with
        regular expression searches because the alternate names for the
        characters are searched as well.  For example, if you search for
        exclamation points with 'exclamation' as the regular expression,
        you'll also get the character U+001C3 printed out even though it
        doesn't have the regexp in the main description.
        
    - Consult the Unicode documentation for the definitions of the terms
      used.  Unfortunately, this documentation can be technical,
      complicated, and scattered.
      
    - Regular expression searches start at U+0020 because python's
      unicodedata module doesn't support name lookups for smaller
      codepoints.
      
    - The only characters used in the descriptions are A-Z, digits 0-9,
      and the hyphen character.
      
    - Recent versions of python support about 5000 valid codepoints in
      the Basic Multilingual Plane and a bit over 9000 if you use the -a
      option.  The -D option will yield about 130,000 valid codepoints.
      
    - Combining forms:  these are Unicode characters that are combined
      with other characters.  They may print in unusual ways.
      
    - Tools:  It can be challenging to work with Unicode because
      software tools support different Unicode versions.  For example,
      the python version I'm using supports Unicode 11.0.0, python 3.8
      supports 12.1.0.  My primary editor is 4 years old at this writing
      and supports Unicode quite well; my alternate editor is less than
      6 months old but doesn't support Unicode as well as my primary
      editor.  A month ago I upgraded my terminal to the latest version
      (also less than 6 months old and it has pretty good Unicode
      support too).  It's hit or miss with the other command line tools
      I use.'''[1:]
        )
    )
    exit(status)
def PythonSymbols(d):
    "Print allowed python symbols"
    i = 0
    for cp in sorted(cpset, reverse=True):
        allowed = IsPythonSymbol(cp)
        if allowed:
            if d["-p"] and cp > 0x3E1:
                continue
            # PrintCP(cp)
            if i and not (i % 60):
                print()
            print(chr(cp), end="")
            i += 1
    print()

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = d["args"] = ParseCommandLine(d)
    cpset = GetCharacterSet(d)
    if d["-D"]:  # Print all valid characters
        for cp in sorted(cpset, reverse=True):
            PrintCP(cp)
    elif d["-g"]:  # Print all valid characters by group
        PrintByGroup(d)
    elif d["-p"] or d["-P"]:  # Print valid python symbols
        PythonSymbols(d)
    elif d["-b"] and ucd is not None:
        DumpBlocks(args, d)
    elif d["-s"]:  # Print data on command line strings
        for arg in args:
            for c in arg:
                PrintCP(ord(c))
            print()
    else:  # Look up as a regular expression, number, range
        for i, r in enumerate(args):
            d["last"] = i == len(args) - 1
            LookUp(r, d)

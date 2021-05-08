'''
Make this into a utility encoding tool.  Given a file, read it in as
binary and try to determine its encoding by finding what decoder works
on it.  Use '-o num' to choose an output encoding.

Of course, it doesn't make sense to have all the encodings available, as
I'd only practically use a few; choose this small set to be the standard
and add an option that lets you expand the set of codecs.

Here's a book that does a pretty good job of explaining Unicode and some
problems (written by a non-native English speaker):
https://unicodebook.readthedocs.io/index.html

'''

# Copyright (C) 2019 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
if 1:   # Imports & globals
    import getopt
    import os
    import sys
    import textwrap
    from collections import defaultdict
    from pprint import pprint as pp
    from pdb import set_trace as xx
    # Non-standard libraries
    from columnize import Columnize
    # Debugging stuff
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
    dedent = textwrap.dedent
    # Note:  'encodings' and 'priorities' were produced by the
    # ConstructEncodingData function.  You may wish to edit it to your own
    # tastes.
    # Note:  'encodings' and 'priorities' were produced by the
    # ConstructEncodingData function.  You may wish to edit it to your own
    # tastes.
    encodings = {
        # Key:  encoding_name, Value: (aliases, languages)
        # Note:  encoding names and aliases are from python 3.7.4 codecs
        # module documentation, "Standard Encodings" section.
        "ascii": "('646, us-ascii', 'English')",
        "utf_8": "('U8, UTF, utf8', 'All')",
        "latin_1": "('iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1', 'West Europe')",
        "iso8859_2": "('iso-8859-2, latin2, L2', 'Central and Eastern Europe')",
        "cp1252": "('windows-1252', 'Western Europe')",
        "utf_16": "('U16, utf16', 'All')",
        "utf_32": "('U32, utf32', 'All')",
        "cp437": "('437, IBM437', 'English (orig IBM PC)')",
        "cp037": "('IBM037, IBM039', 'English (EBCDIC Latin-1)')",
        "utf_8_sig": "('', 'All (e.g. Notepad)')",
        "utf_32_be": "('UTF-32BE', 'All')",
        "utf_32_le": "('UTF-32LE', 'All')",
        "utf_16_be": "('UTF-16BE', 'All')",
        "utf_16_le": "('UTF-16LE', 'All')",
        "utf_7": "('U7, unicode-1-1-utf-7', 'All')",
        "cp65001": "('', 'Windows UTF-8 (CP_UTF8)')",
        "cp500": "('EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500', 'Western Europe')",
        "cp850": "('850, IBM850', 'Western Europe')",
        "cp852": "('852, IBM852', 'Central and Eastern Europe')",
        "cp858": "('858, IBM858', 'Western Europe')",
        "cp1140": "('ibm1140', 'Western Europe')",
        "cp1250": "('windows-1250', 'Central and Eastern Europe')",
        "iso8859_15": "('iso-8859-15, latin9, L9', 'Western Europe')",
        "iso8859_16": "('iso-8859-16, latin10, L10', 'South-Eastern Europe')",
        "mac_latin2": "('maclatin2, maccentraleurope', 'Central and Eastern Europe')",
        "mac_roman": "('macroman, macintosh', 'Western Europe')",
        "big5": "('big5-tw, csbig5', 'Traditional Chinese')",
        "big5hkscs": "('big5-hkscs, hkscs', 'Traditional Chinese')",
        "cp950": "('950, ms950', 'Traditional Chinese')",
        "gb2312": "('chinese, csiso58gb231280, euc-cn, euccn, eucgb2312-cn, gb2312-1980, gb2312-80, iso-ir-58', 'Simplified Chinese')",
        "gbk": "('936, cp936, ms936', 'Unified Chinese')",
        "gb18030": "('gb18030-2000', 'Unified Chinese')",
        "hz": "('hzgb, hz-gb, hz-gb-2312', 'Simplified Chinese')",
        "cp932": "('932, ms932, mskanji, ms-kanji', 'Japanese (aka Windows-31J)')",
        "euc_jp": "('eucjp, ujis, u-jis', 'Japanese')",
        "euc_jis_2004": "('jisx0213, eucjis2004', 'Japanese')",
        "euc_jisx0213": "('eucjisx0213', 'Japanese')",
        "iso2022_jp": "('csiso2022jp, iso2022jp, iso-2022-jp', 'Japanese')",
        "iso2022_jp_1": "('iso2022jp-1, iso-2022-jp-1', 'Japanese')",
        "iso2022_jp_2": "('iso2022jp-2, iso-2022-jp-2', 'Japanese, Korean, Simplified Chinese, Western Europe, Greek')",
        "iso2022_jp_2004": "('iso2022jp-2004, iso-2022-jp-2004', 'Japanese')",
        "iso2022_jp_3": "('iso2022jp-3, iso-2022-jp-3', 'Japanese')",
        "iso2022_jp_ext": "('iso2022jp-ext, iso-2022-jp-ext', 'Japanese')",
        "shift_jis": "('csshiftjis, shiftjis, sjis, s_jis', 'Japanese')",
        "shift_jis_2004": "('shiftjis2004, sjis_2004, sjis2004', 'Japanese')",
        "shift_jisx0213": "('shiftjisx0213, sjisx0213, s_jisx0213', 'Japanese')",
        "cp949": "('949, ms949, uhc', 'Korean')",
        "iso2022_kr": "('csiso2022kr, iso2022kr, iso-2022-kr', 'Korean')",
        "johab": "('cp1361, ms1361', 'Korean')",
        "euc_kr": "('euckr, korean, ksc5601, ks_c-5601, ks_c-5601-1987, ksx1001, ks_x-1001', 'Korean')",
        "cp855": "('855, IBM855', 'Bulgarian, Byelorussian, Macedonian, Russian, Serbian')",
        "cp866": "('866, IBM866', 'Russian')",
        "cp1251": "('windows-1251', 'Bulgarian, Byelorussian, Macedonian, Russian, Serbian')",
        "iso8859_5": "('iso-8859-5, cyrillic', 'Bulgarian, Byelorussian, Macedonian, Russian, Serbian')",
        "koi8_r": "('', 'Russian')",
        "mac_cyrillic": "('maccyrillic', 'Bulgarian, Byelorussian, Macedonian, Russian, Serbian')",
        "ptcp154": "('csptcp154, pt154, cp154, cyrillic-asian', 'Kazakh')",
        "cp775": "('IBM775', 'Baltic languages')",
        "cp1257": "('windows-1257', 'Baltic languages')",
        "iso8859_4": "('iso-8859-4, latin4, L4', 'Baltic languages')",
        "iso8859_13": "('iso-8859-13, latin7, L7', 'Baltic languages')",
        "cp1125": "('1125, ibm1125, cp866u, ruscii', 'Ukrainian')",
        "koi8_u": "('', 'Ukrainian')",
        "kz1048": "('kz_1048, strk1048_2002, rk1048', 'Kazakh')",
        "cp737": "('', 'Greek')",
        "cp869": "('869, CP-GR, IBM869', 'Greek')",
        "cp875": "('', 'Greek')",
        "cp1253": "('windows-1253', 'Greek')",
        "iso8859_7": "('iso-8859-7, greek, greek8', 'Greek')",
        "mac_greek": "('macgreek', 'Greek')",
        "cp857": "('857, IBM857', 'Turkish')",
        "cp1026": "('ibm1026', 'Turkish')",
        "cp1254": "('windows-1254', 'Turkish')",
        "iso8859_9": "('iso-8859-9, latin5, L5', 'Turkish')",
        "mac_turkish": "('macturkish', 'Turkish')",
        "cp424": "('EBCDIC-CP-HE, IBM424', 'Hebrew')",
        "cp856": "('', 'Hebrew')",
        "cp862": "('862, IBM862', 'Hebrew')",
        "cp1255": "('windows-1255', 'Hebrew')",
        "iso8859_8": "('iso-8859-8, hebrew', 'Hebrew')",
        "cp720": "('', 'Arabic')",
        "cp864": "('IBM864', 'Arabic')",
        "cp1256": "('windows-1256', 'Arabic')",
        "iso8859_6": "('iso-8859-6, arabic', 'Arabic')",
        "cp861": "('861, CP-IS, IBM861', 'Icelandic')",
        "mac_iceland": "('maciceland', 'Icelandic')",
        "cp874": "('', 'Thai')",
        "iso8859_11": "('iso-8859-11, thai', 'Thai languages (aka Windows-874, TIS-620)')",
        "cp273": "('273, IBM273, csIBM273', 'German')",
        "cp860": "('860, IBM860', 'Portuguese')",
        "cp863": "('863, IBM863', 'French Canadian')",
        "cp865": "('865, IBM865', 'Danish, Norwegian')",
        "cp1006": "('', 'Urdu (Pakistan, northern India')",
        "cp1258": "('windows-1258', 'Vietnamese')",
        "iso8859_3": "('iso-8859-3, latin3, L3', 'Esperanto, Maltese')",
        "iso8859_10": "('iso-8859-10, latin6, L6', 'Nordic languages')",
        "iso8859_14": "('iso-8859-14, latin8, L8', 'Celtic languages')",
        "koi8_t": "('', 'Tajik (in Afghanistan, Tajikistan, Uzbekistan))')",
    }
    priorities = {
        # Key:  integer, Value: tuple of encodings
        # Highest priority is lowest integer
        0: ('utf_8', 'latin_1', 'ascii'),
        1: ('cp1251', 'cp1252', 'shift_jis', 'gb2312', 'euc_kr', 'euc_jp', 'iso8859_2', 'gbk', 'cp1250', 'big5', 'iso8859_9', 'iso8859_15'),
        2: ('cp1254', 'cp1256', 'iso8859_11', 'cp1255', 'iso8859_11', 'iso8859_7', 'cp1253', 'utf_16', 'koi8_r', 'cp1257', 'gb18030', 'utf_7', 'cp932', 'iso8859_8', 'iso8859_5', 'iso8859_4', 'iso8859_6', 'koi8_u', 'iso2022_jp', 'iso8859_13', 'iso8859_16', 'iso8859_3', 'cp949', 'iso8859_10', 'cp1258', 'iso8859_11', 'iso8859_14', 'cp850'),
        3: ('mac_latin2', 'cp875', 'cp1125', 'cp856', 'cp1006', 'cp863', 'mac_roman', 'cp865', 'cp500', 'cp852', 'koi8_t', 'cp866', 'cp855', 'mac_iceland', 'cp1140', 'shift_jis_2004', 'shift_jisx0213', 'cp862', 'iso2022_kr', 'utf_32', 'utf_32_le', 'cp950', 'iso2022_jp_ext', 'utf_16_le', 'cp874', 'cp1026', 'iso2022_jp_1', 'euc_jis_2004', 'utf_8_sig', 'cp857', 'cp775', 'iso2022_jp_3', 'cp864', 'cp737', 'hz', 'mac_turkish', 'cp869', 'utf_16_be', 'ptcp154', 'mac_cyrillic', 'iso2022_jp_2004', 'cp437', 'cp424', 'johab', 'kz1048', 'cp858', 'iso2022_jp_2', 'cp720', 'cp860', 'utf_32_be', 'cp65001', 'big5hkscs', 'euc_jisx0213', 'cp037', 'mac_greek', 'cp273', 'cp861'),
    }
    # Build set of valid encoding names
    valid_encodings = set()
    for i in encodings:
        valid_encodings.add(i.lower())
        valid_encodings.update(set([j.lower() for j in encodings[i][0]]))

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def ConstructEncodingData():
    '''This function can be called to print a dict to stdout that builds
    the dictionary to use for doing decoding.  The keys are integers
    that give the order that the encodings should be tried.
 
    Here's a URL that puports to have studied the frequencies of
    encodings used on web pages:
    https://w3techs.com/technologies/overview/character_encoding.  I've
    used this page's data to determine the encoding priority by this
    script.  Here are the frequencies in %:
 
        Web page's name   Frequency      Python codec name
        ---------------   ---------      -----------------
        UTF-8                94.3%          utf_8
        ISO-8859-1           2.8%           latin_1
        Windows-1251         0.9%           cp1251
        Windows-1252         0.5%           cp1252
        Shift JIS            0.3%           shift_jis
        GB2312               0.2%           gb2312
        EUC-KR               0.2%           euc_kr
        EUC-JP               0.1%           euc_jp
        ISO-8859-2           0.1%           iso8859_2
        GBK                  0.1%           gbk
        Windows-1250         0.1%           cp1250
        Big5                 0.1%           big5
        ISO-8859-9           0.1%           iso8859_9
        ISO-8859-15          0.1%           iso8859_15
 
    In my experience, the only other encoding I encounter on a regular
    basis is ISO-8859-1 (Latin-1).
 
    The following encodings are used in less than 0.1%:
 
        Web page's name                  Python codec name
        -------------------              -----------------
        Windows-1254                        cp1254
        Windows-1256                        cp1256
        Windows-874                         iso8859_11
        US-ASCII                            ascii
        Windows-1255                        cp1255
        TIS-620                             iso8859_11
        ISO-8859-7                          iso8859_7
        Windows-1253                        cp1253
        UTF-16                              utf_16
        KOI8-R                              koi8_r
        Windows-1257                        cp1257
        GB18030                             gb18030
        KS C 5601                           euc_kr
        UTF-7                               utf_7
        Windows-31J                         cp932
        ISO-8859-8                          iso8859_8
        ISO-8859-5                          iso8859_5
        ISO-8859-4                          iso8859_4
        ANSI_X3.110-1983                    ?
        ISO-8859-6                          iso8859_6
        KOI8-U                              koi8_u
        ISO-2022-JP                         iso2022_jp
        ISO-8859-13                         iso8859_13
        ISO-8859-16                         iso8859_16
        ISO-8859-3                          iso8859_3
        Big5 HKSCS                          big5
        Windows-949                         cp949
        ISO-8859-10                         iso8859_10
        Windows-1258                        cp1258
        ISO-8859-11                         iso8859_11
        ISO-8859-14                         iso8859_14
        IBM850                              cp850
 
    '''
    encodings = {
        # These encodings are listed on the codec documentation page for
        # python 3.7.4.  The key is the primary encoding name.  Values are
        # (pri, alt, lang) where pri is an integer indicating the priority
        # to use (0 being highest), alt is a set of aliases and lang are the
        # languages supported.
 
        # English
        "ascii":           ("646, us-ascii", "English"),
        "utf_8":           ("U8, UTF, utf8", "All"),
 
        "latin_1":         ("iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1", "West Europe"),
        "iso8859_2":       ("iso-8859-2, latin2, L2", "Central and Eastern Europe"),
        "cp1252":          ("windows-1252", "Western Europe"),
 
        "utf_16":          ("U16, utf16", "All"),
        "utf_32":          ("U32, utf32", "All"),
 
        "cp437":           ("437, IBM437", "English (orig IBM PC)"),
        "cp037":           ("IBM037, IBM039", "English (EBCDIC Latin-1)"),
 
        "utf_8_sig":       ("", "All (e.g. Notepad)"),
        "utf_32_be":       ("UTF-32BE", "All"),
        "utf_32_le":       ("UTF-32LE", "All"),
        "utf_16_be":       ("UTF-16BE", "All"),
        "utf_16_le":       ("UTF-16LE", "All"),
        "utf_7":           ("U7, unicode-1-1-utf-7", "All"),
        "cp65001":         ("", "Windows UTF-8 (CP_UTF8)"),
 
        # European
        "cp500":           ("EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500", "Western Europe"),
        "cp850":           ("850, IBM850", "Western Europe"),
        "cp852":           ("852, IBM852", "Central and Eastern Europe"),
        "cp858":           ("858, IBM858", "Western Europe"),
        "cp1140":          ("ibm1140", "Western Europe"),
        "cp1250":          ("windows-1250", "Central and Eastern Europe"),
        "iso8859_15":      ("iso-8859-15, latin9, L9", "Western Europe"),
        "iso8859_16":      ("iso-8859-16, latin10, L10", "South-Eastern Europe"),
        "mac_latin2":      ("maclatin2, maccentraleurope", "Central and Eastern Europe"),
        "mac_roman":       ("macroman, macintosh", "Western Europe"),
 
        # Chinese
        "big5":            ("big5-tw, csbig5", "Traditional Chinese"),
        "big5hkscs":       ("big5-hkscs, hkscs", "Traditional Chinese"),
        "cp950":           ("950, ms950", "Traditional Chinese"),
        "gb2312":          ("chinese, csiso58gb231280, euc-cn, euccn, eucgb2312-cn, gb2312-1980, gb2312-80, iso-ir-58", "Simplified Chinese"),
        "gbk":             ("936, cp936, ms936", "Unified Chinese"),
        "gb18030":         ("gb18030-2000", "Unified Chinese"),
        "hz":              ("hzgb, hz-gb, hz-gb-2312", "Simplified Chinese"),
 
        # Japanese
        "cp932":           ("932, ms932, mskanji, ms-kanji", "Japanese (aka Windows-31J)"),
        "euc_jp":          ("eucjp, ujis, u-jis", "Japanese"),
        "euc_jis_2004":    ("jisx0213, eucjis2004", "Japanese"),
        "euc_jisx0213":    ("eucjisx0213", "Japanese"),
        "iso2022_jp":      ("csiso2022jp, iso2022jp, iso-2022-jp", "Japanese"),
        "iso2022_jp_1":    ("iso2022jp-1, iso-2022-jp-1", "Japanese"),
        "iso2022_jp_2":    ("iso2022jp-2, iso-2022-jp-2", "Japanese, Korean, Simplified Chinese, Western Europe, Greek"),
        "iso2022_jp_2004": ("iso2022jp-2004, iso-2022-jp-2004", "Japanese"),
        "iso2022_jp_3":    ("iso2022jp-3, iso-2022-jp-3", "Japanese"),
        "iso2022_jp_ext":  ("iso2022jp-ext, iso-2022-jp-ext", "Japanese"),
        "shift_jis":       ("csshiftjis, shiftjis, sjis, s_jis", "Japanese"),
        "shift_jis_2004":  ("shiftjis2004, sjis_2004, sjis2004", "Japanese"),
        "shift_jisx0213":  ("shiftjisx0213, sjisx0213, s_jisx0213", "Japanese"),
 
        # Korean
        "cp949":           ("949, ms949, uhc", "Korean"),
        "iso2022_kr":      ("csiso2022kr, iso2022kr, iso-2022-kr", "Korean"),
        "johab":           ("cp1361, ms1361", "Korean"),
        "euc_kr":          ("euckr, korean, ksc5601, ks_c-5601, ks_c-5601-1987, ksx1001, ks_x-1001", "Korean"),
        
        # Russian & Baltic
        "cp855":           ("855, IBM855", "Bulgarian, Byelorussian, Macedonian, Russian, Serbian"),
        "cp866":           ("866, IBM866", "Russian"),
        "cp1251":          ("windows-1251", "Bulgarian, Byelorussian, Macedonian, Russian, Serbian"),
        "iso8859_5":       ("iso-8859-5, cyrillic", "Bulgarian, Byelorussian, Macedonian, Russian, Serbian"),
        "koi8_r":          ("", "Russian"),
        "mac_cyrillic":    ("maccyrillic", "Bulgarian, Byelorussian, Macedonian, Russian, Serbian"),
        "ptcp154":         ("csptcp154, pt154, cp154, cyrillic-asian", "Kazakh"),
        "cp775":           ("IBM775", "Baltic languages"),
        "cp1257":          ("windows-1257", "Baltic languages"),
        "iso8859_4":       ("iso-8859-4, latin4, L4", "Baltic languages"),
        "iso8859_13":      ("iso-8859-13, latin7, L7", "Baltic languages"),
        "cp1125":          ("1125, ibm1125, cp866u, ruscii", "Ukrainian"),
        "koi8_u":          ("", "Ukrainian"),
        "kz1048":          ("kz_1048, strk1048_2002, rk1048", "Kazakh"),
 
        # Greek
        "cp737":           ("", "Greek"),
        "cp869":           ("869, CP-GR, IBM869", "Greek"),
        "cp875":           ("", "Greek"),
        "cp1253":          ("windows-1253", "Greek"),
        "iso8859_7":       ("iso-8859-7, greek, greek8", "Greek"),
        "mac_greek":       ("macgreek", "Greek"),
 
        # Turkish
        "cp857":           ("857, IBM857", "Turkish"),
        "cp1026":          ("ibm1026", "Turkish"),
        "cp1254":          ("windows-1254", "Turkish"),
        "iso8859_9":       ("iso-8859-9, latin5, L5", "Turkish"),
        "mac_turkish":     ("macturkish", "Turkish"),
 
        # Hebrew
        "cp424":           ("EBCDIC-CP-HE, IBM424", "Hebrew"),
        "cp856":           ("", "Hebrew"),
        "cp862":           ("862, IBM862", "Hebrew"),
        "cp1255":          ("windows-1255", "Hebrew"),
        "iso8859_8":       ("iso-8859-8, hebrew", "Hebrew"),
 
        # Arabic
        "cp720":           ("", "Arabic"),
        "cp864":           ("IBM864", "Arabic"),
        "cp1256":          ("windows-1256", "Arabic"),
        "iso8859_6":       ("iso-8859-6, arabic", "Arabic"),
 
        # Icelandic
        "cp861":           ("861, CP-IS, IBM861", "Icelandic"),
        "mac_iceland":     ("maciceland", "Icelandic"),
 
        # Thai
        "cp874":           ("", "Thai"),
        "iso8859_11":      ("iso-8859-11, thai", "Thai languages (aka Windows-874, TIS-620)"),
 
        # Others
        "cp273":           ("273, IBM273, csIBM273", "German"),
        "cp860":           ("860, IBM860", "Portuguese"),
        "cp863":           ("863, IBM863", "French Canadian"),
        "cp865":           ("865, IBM865", "Danish, Norwegian"),
        "cp1006":          ("", "Urdu (Pakistan, northern India"),
        "cp1258":          ("windows-1258", "Vietnamese"),
        "iso8859_3":       ("iso-8859-3, latin3, L3", "Esperanto, Maltese"),
        "iso8859_10":      ("iso-8859-10, latin6, L6", "Nordic languages"),
        "iso8859_14":      ("iso-8859-14, latin8, L8", "Celtic languages"),
        "koi8_t":          ("", "Tajik (in Afghanistan, Tajikistan, Uzbekistan))"),
    }
    # Priorities for trying an encoding
    high = "utf_8 latin_1 ascii".split()
    medium = '''
        cp1251 cp1252 shift_jis gb2312 euc_kr euc_jp iso8859_2 gbk
        cp1250 big5 iso8859_9 iso8859_15
        '''.split()
    low = '''
        cp1254 cp1256 iso8859_11 cp1255 iso8859_11 iso8859_7
        cp1253 utf_16 koi8_r cp1257 gb18030 utf_7 cp932 iso8859_8
        iso8859_5 iso8859_4 iso8859_6 koi8_u iso2022_jp iso8859_13
        iso8859_16 iso8859_3 cp949 iso8859_10 cp1258 iso8859_11
        iso8859_14 cp850
        '''.split()
    # Build the dictionary
    key, d, remainder = 0, defaultdict(list), set(encodings)
    for s in (high, medium, low):
        for i in s:
            d[key].append(i)
        d[key] = tuple(d[key])
        key += 1
        remainder = remainder - set(s)
    for i in remainder:
        d[key].append(i)
    d[key] = tuple(d[key])
    # Check for no overlap
    A, B, C, D = set(high), set(medium), set(low), remainder
    assert(A | B | C | D == set(encodings))
    assert(not(A & B) and not(A & C) and not(A & D) and not(B & C) and 
           not(B & D) and not(C & D))
    # Dump data to stdout
    print(dedent('''
    # Note:  'encodings' and 'priorities' were produced by the
    # ConstructEncodingData function.  You may wish to edit it to your own
    # tastes.
    
    encodings = {
        # Key:  encoding_name, Value: (aliases, languages)
        # Note:  encoding names and aliases are from python 3.7.4 codecs
        # module documentation, "Standard Encodings" section.'''[1:]))
    for i in encodings:
        print(f'    "{i}": "{encodings[i]}",')
    print("}")
    print('''priorities = {
    # Key:  integer, Value: tuple of encodings
    # Highest priority is lowest integer''')
    for i in d:
        print(f'    {i}: {d[i]},')
    print("}")

def Usage(d, status=1):
    name = sys.argv[0]
    print(f'''
Usage:  {name} [options] file1 [file2 ...]
  Try to identify the encoding of the file(s) on the command line.  This
  is done by finding which python codecs module encodings don't raise an
  exception.  Note there is no way in general to determine the encoding 
  of a file.

  Use the -o option to change the encoding of a file.

Options (case of enc string is ignored):
  -a 
    Try all encodings.
  -d
    Construct the encoding data as used by the script.  You may want to
    edit this function to your tastes.
  -i enc
    Use the indicated encoding on file1 to decode it.
  -l
    List the allowed encoding strings.        
  -o enc
        Encode file1 (only one argument allowed) with the indicated
        encoding and send the data to stdout.
'''[1:-1])
    exit(status)

def ParseCommandLine(d):
    d["-a"] = False
    d["-i"] = None
    d["-l"] = False
    d["-o"] = None
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "adi:lo:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("al"):
            d[o] = not d[o]
        elif o in ("-d",):
            ConstructEncodingData()
            exit(0)
        elif o in ("-i", "-o"):
            e = a.lower()
            if e not in valid_encodings:
                Error(f"'{a}' not a recognized encoding")
            d[o] = e
    if d["-o"] is not None and len(args) != 2:
        Error(f"Need input and output file with -o option")
    return args

def GetEncoding(byts, enc_seq):
    enc = []
    for e in enc_seq:
        try:
            s = byts.decode(e)
            enc.append(e)
        except (UnicodeDecodeError, LookupError):
            pass
    return enc

def CheckEncoding(file):
    Priorities = priorities.keys() if d["-a"] else (0, 1)
    byts = open(file, "rb").read()
    enc = []
    for p in Priorities:
        enc.extend(GetEncoding(byts, priorities[p]))
    if enc:
        print(f"{file} possible encodings:")
        for e in Columnize([i for i in enc if i], indent=" "*4, sep=" "*4):
            print(e)

def Encode(files):
    '''Encode the input file to the encoding specified by the -o option.
    '''
    ifile, ofile = files
    if d["-i"] is not None:
        s = open(ifile, "rb").read().decode(d["-i"])
    else:
        s = open(ifile, "r").read()
    open(ofile, "wb").write(s.encode(d["-o"]))

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if d["-o"]:
        Encode(files)
    elif d["-l"]:
        s = []
        plist = priorities.keys() if d["-a"] else (0, 1)
        for p in plist:
            s.extend(priorities[p])
        for i in Columnize(s):
            print(i)
    else:
        for file in files:
            CheckEncoding(file)

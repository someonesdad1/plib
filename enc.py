'''
Utility encoding tool
    Given a file, read it in as binary and try to determine its encoding
    by finding what decoder works on it.  Use '-o num' to choose an
    output encoding.
   
    It doesn't make sense to have all the encodings available, as I'd
    only practically use a few; choose this small set to be the standard
    and add an option that lets you expand the set of codecs.
  
    Here's a book that does a fairly good job of explaining Unicode and
    some problems (written by a non-native English speaker):
    https://unicodebook.readthedocs.io/index.html
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞# <utility> Utility encoding tool.  It reads a file and
    # decodes it with various codecs; the ones that don't raise an
    # exception are possible encodings.  Also lets you change a file's
    # encoding like iconv.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import csv
    import getopt
    import os
    import pathlib
    import sys
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    P = pathlib.Path
    # This list comes from the most frequently used web page encodings.
    # I've kept English and western European codecs, getting rid of
    # Asian, Turkish, Russian, etc. encodings.  ASCII is detected
    # separately.
    use_first = '''utf_8 latin_1 cp1252 iso8859_2 cp1250 iso8859_15'''.split()
    aliases, primary = None, None
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] file1 [file2 ...]
          Try to identify the encoding of the file(s) on the command line.  This
          is done by finding which python codecs module encodings don't raise an
          exception.  Note there is no way in general to determine the encoding
          of a file.
          
          Use the -o option to change the encoding of a file.
           
          Other tools handy to deal with encodings are the UNIX file
          command (uses heuristics to identify file types) and the iconv
          encoding/decoding tool.
          
        Options (case of enc string is ignored):
          -a        Try all encodings
          -d enc    Use the indicated encoding on file1 to decode it
          -h        Show some usage hints
          -l        List the allowed encoding strings
          -o enc    Encode file1 with the indicated encoding and write
                    it to the second file on the command line.
          -x        Show the non-ASCII characters in the file.  Decodes
                    with UTF-8 unless you give a -d option.  The
                    characters are sorted.
          -X        Same as -x, but show codepoints
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Try all encodings
        d["-d"] = None      # Which encoding to use
        d["-l"] = False     # List allowed encodings
        d["-o"] = None      # Encode file on command line with this encoding
        d["-x"] = False     # Show the non-ASCII characters in the file
        d["-X"] = False     # Same as -x, but show codepoints
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:hlo:xX", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("alxX"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                UsageHints()
            elif o in ("-d", "-o"):
                if a.lower() not in valid_encodings:
                    Error(f"'{a}' is not a recognized encoding")
                d[o] = a
        if d["-o"] is not None and len(args) != 2:
            Error(f"Two arguments needed with -o option")
        return args
def ConstructEncodingData():
    '''This function can be called to print a dict to stdout that builds
    the dictionary to use for doing decoding.  The keys are integers
    that give the order that the encodings should be tried.
 
    Here's a URL that purports to have studied the frequencies of
    encodings used on web pages:
    https://w3techs.com/technologies/overview/character_encoding.  I've
    used this page's data to determine the encoding priority by this
    script.  Here are the frequencies in %:
 
    Data from 9 Jun 2021:
        Web page's name   Frequency      Python codec name
        ---------------   ---------      -----------------
        UTF-8                96.9%          utf_8
        ISO-8859-1           1.3%           latin_1
        Windows-1251         0.8%           cp1251
        Windows-1252         0.3%           cp1252
        GB2312               0.2%           gb2312
        Shift JIS            0.1%           shift_jis
        ISO-8859-9           0.1%           iso8859_9
        Windows-1254         0.1%           cp1250
        EUC-KR               0.1%           euc_kr
        GBK                  0.1%           gbk
        EUC-JP               0.1%           euc_jp
 
    Data from 2019:
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
def GetEncoding(mybytes, seq):
    '''For mybytes object, try to decode with the codec names in
    seq.  Return a list of the codecs that didn't have an exception.
    '''
    enc = []
    for e in seq:
        try:
            s = mybytes.decode(e)
            enc.append(e)
        except (UnicodeDecodeError, LookupError):
            pass
    return enc
def IsASCII(mybytes):
    '''Return True if the set of bytes are 7 bit, meaning it's likely
    the encoding was ASCII.
    '''
    return max(set(mybytes)) < 0x80
def CheckEncoding(file):
    mycodecs = primary if d["-a"] else use_first
    mybytes = open(file, "rb").read()
    if IsASCII(mybytes):
        print(f"'{file}' is 7-bit ASCII text")
        return
    enc = []
    enc.extend(GetEncoding(mybytes, mycodecs))
    if enc:
        print(f"'{file}' possible encodings:")
        for line in Columnize([i for i in enc if i], indent=" "*2):
            print(line)
def Encode(files):
    '''Encode the input file to the encoding specified by the -o option.
    '''
    ifile, ofile = files
    if d["-d"] is not None:
        s = open(ifile, "rb").read().decode(d["-d"])
    else:
        s = open(ifile, "r").read()
    open(ofile, "wb").write(s.encode(d["-o"]))
def BuildAliasDict():
    '''Return (aliases, primary) where aliases is a dictionary of
    aliases recognized by the codecs module.  Keys and values are all
    lowercase, as the case of the codec name isn't important.  primary
    is a set of the main codec names, which is also the set of values of
    aliases.
    '''
    # The enc_codecs.csv file was made by importing the HTML page of the
    # python version 3.7.4 codecs documentation and copying the codecs
    # table to a spreadsheet, saving it in CSV form.
    lines = [i.rstrip() for i in open("enc_codecs.csv").readlines()][2:]
    r, aliases, primary = csv.reader(lines), {}, set()
    for row in r:
        name, other = row
        name = name.lower()
        primary.add(name)
        other = [i.lower() for i in other.split(",")]
        if 0:
            print(f"{red}{row}{norm}")
            print(f"  {grn}{name}{norm}  {cyn}{other}{norm}")
        for key in other:
            if not key:
                continue
            if key in aliases:
                m = f"{key} already in aliases"
                raise ValueError(m)
            else:
                aliases[key] = name
    return (aliases, primary)
def ShowNonASCII(files):
    decode = d["-d"] if d["-d"] else "utf-8"
    for file in files:
        f = P(file)
        if f.is_dir():
            print(f"'{file}' is a directory", file=sys.stderr)
            continue
        try:
            s = open(file, "rb").read().decode(decode)
        except UnicodeDecodeError:
            print(f"Can't decode '{file}'")
            continue
        characters = set(s)
        if d["-X"]:
            t1 = sorted([ord(i) for i in characters if ord(i) >= 0x80])
            t2 = [f"U+{hex(i)[2:]}" for i in t1]
            s = ' '.join(t2)
        else:
            u = [i for i in characters if ord(i) >= 0x80]
            s = ' '.join(sorted(u))
        if s:
            print(f"{file}:  {s}")
def Decode(files):
    success, failure = [], []
    for file in files:
        f = P(file)
        if f.is_dir():
            print(f"'{file}' is a directory", file=sys.stderr)
            continue
        try:
            open(file, "rb").read().decode(d["-d"])
            success.append(file)
        except (UnicodeDecodeError, LookupError):
            failure.append(file)
    if files:
        print(f'''Using '{d["-d"]}' codec for decoding''')
        if success:
            print(f"Successfully decoded:")
            for line in Columnize(success, indent=" "*2):
                print(line)
        if failure:
            print(f"Failed to decode:")
            for line in Columnize(failure, indent=" "*2):
                print(line)
def UsageHints():
    name = "python " + sys.argv[0]
    print(dedent(f'''
    Show the common encodings that can decode a file:
        {name} file
    Show all encodings that can decode a file:
        {name} -a file
    Show all the ASCII and non-ASCII files in the current directory:
        {name} -d ascii *
    Change an ISO8859_1 file to UTF_8 encoding:
        {name} -d iso8859_1 -o utf_8 file output_file
    Show the non-ASCII characters in all files in the directory:
        {name} -x *
    '''))
if __name__ == "__main__":
    aliases, primary = BuildAliasDict()
    valid_encodings = set()
    valid_encodings.update(primary)
    valid_encodings.update(aliases)
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if d["-o"]:
        Encode(files)
    elif d["-d"]:
        Decode(files)
    elif d["-x"] or d["-X"]:
        ShowNonASCII(files)
    elif d["-l"]:
        print("Aliases for the primary codec names:")
        for line in Columnize(sorted(aliases), indent=" "*2):
            print(line)
        print("Primary codec names:")
        for line in Columnize(sorted(primary), indent=" "*2):
            print(line)
    else:
        for file in files:
            CheckEncoding(file)

'''
Classifies the characters in one or more files by type (e.g., lowercase
letters, digits, etc.) and prints out a table of the characters present
in the file(s).  Reads stdin if no files are given on the command line.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
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
if 1:   # Imports
    import sys
    import os
    import getopt
    import string
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent, wrap
    from color import Color, Trm
    t = Trm()
if 1:   # Global variables
    ii = isinstance
    enc = "UTF-8"
    encodings = '''
        1125 273 437 646 850 852 855 857 858 860 861 862 863 865 866 869
        8859 932 936 949 950 CP-GR CP-IS EBCDIC-CP-BE EBCDIC-CP-CH
        EBCDIC-CP-HE IBM037 IBM039 IBM273 IBM424 IBM437 IBM500 IBM775
        IBM850 IBM852 IBM855 IBM857 IBM858 IBM860 IBM861 IBM862 IBM863
        IBM864 IBM865 IBM866 IBM869 L1 L10 L2 L3 L4 L5 L6 L7 L8 L9 U16 U32
        U7 U8 UTF UTF-16BE UTF-16LE UTF-32BE UTF-32LE arabic ascii big5
        big5-hkscs big5-tw big5hkscs chinese cn cp037 cp1006 cp1026 cp1125
        cp1140 cp1250 cp1251 cp1252 cp1253 cp1254 cp1255 cp1256 cp1257
        cp1258 cp1361 cp154 cp273 cp424 cp437 cp500 cp65001 cp720 cp737
        cp775 cp819 cp850 cp852 cp855 cp856 cp857 cp858 cp860 cp861 cp862
        cp863 cp864 cp865 cp866 cp866u cp869 cp874 cp875 cp932 cp936 cp949
        cp950 csIBM273 csbig5 csiso2022jp csiso2022kr csiso58gb231280
        csptcp154 csshiftjis cyrillic cyrillic-asian euc- euc_jis_2004
        euc_jisx0213 euc_jp euc_kr euccn eucgb2312-cn eucjis2004
        eucjisx0213 eucjp euckr gb18030 gb18030-2000 gb2312 gb2312-1980
        gb2312-80 gbk greek greek8 hebrew hkscs hz hz-gb hz-gb-2312 hzgb
        ibm1026 ibm1125 ibm1140 ir-58 iso- iso-2022-jp iso-2022-jp-1
        iso-2022-jp-2 iso-2022-jp-2004 iso-2022-jp-3 iso-2022-jp-ext
        iso-2022-kr iso-8859-1 iso-8859-10 iso-8859-13 iso-8859-14
        iso-8859-15 iso-8859-16 iso-8859-2 iso-8859-3 iso-8859-4 iso-8859-5
        iso-8859-6 iso-8859-7 iso-8859-8 iso-8859-9 iso2022_jp iso2022_jp_1
        iso2022_jp_2 iso2022_jp_2004 iso2022_jp_3 iso2022_jp_ext iso2022_kr
        iso2022jp iso2022jp-1 iso2022jp-2 iso2022jp-2004 iso2022jp-3
        iso2022jp-ext iso2022kr iso8859-1 iso8859_10 iso8859_13 iso8859_14
        iso8859_15 iso8859_16 iso8859_2 iso8859_3 iso8859_4 iso8859_5
        iso8859_6 iso8859_7 iso8859_8 iso8859_9 jisx0213 johab koi8_r
        koi8_u korean ks_c-5601 ks_c-5601-1987 ks_x-1001 ksc5601 ksx1001
        latin latin1 latin10 latin2 latin3 latin4 latin5 latin6 latin7
        latin8 latin9 latin_1 mac_cyrillic mac_greek mac_iceland mac_latin2
        mac_roman mac_turkish maccentraleurope maccyrillic macgreek
        maciceland macintosh maclatin2 macroman macturkish ms-kanji ms1361
        ms932 ms936 ms949 ms950 mskanji pt154 ptcp154 ruscii s_jis
        s_jisx0213 shift_jis shift_jis_2004 shift_jisx0213 shiftjis
        shiftjis2004 shiftjisx0213 sjis sjis2004 sjis_2004 sjisx0213 u-jis
        uhc ujis unicode-1-1-utf-7 us-ascii utf16 utf32 utf8 utf_16
        utf_16_be utf_16_le utf_32 utf_32_be utf_32_le utf_7 utf_8
        utf_8_sig windows-1250 windows-1251 windows-1252 windows-1253
        windows-1254 windows-1255 windows-1256 windows-1257 windows-1258
    '''
    # Construct a dictionary containing the encodings we'll allow and their
    # standard names.
    allowed = {}
    replace1 = lambda x: x.replace("_", "")
    replace2 = lambda x: x.replace("-", "")
    replace = lambda x: replace1(replace2(x))
    for word in encodings.lower().split():
        try:
            ' '.encode(word)
        except LookupError:
            pass
        else:
            # It's an allowed coding
            allowed[word] = word
            allowed[replace1(word)] = word
            allowed[replace2(word)] = word
            allowed[replace(word)] = word
def GetEncoding(encoding):
    '''Return an allowed encoding name for a string identifying one of
    python's supported encodings.  These can be the standard names in
    the documentation but with hyphens and/or underscores optionally
    removed.  Case is ignored.  None is returned if the encoding name
    isn't recognized.
    '''
    e = encoding.lower()
    if e in allowed:
        return allowed[e]
    return None
    return replace(encoding.lower()) in allowed
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def GetCharacterCounts():
    '''Read in all the characters and construct a dictionary that
    contains the Unicode codepoint values as keys and counts as values.
    '''
    characters = []
    # To accumulate data, use a bytearray for binary data; list of
    # strings otherwise.
    characters = bytearray() if d["-b"] else []
    for file in d["files"]:
        if file == "-":  # Read stdin
            characters = sys.stdin.read()
            if d["-b"]:
                characters = bytearray(characters, d["-e"])
        else:
            try:
                if d["-b"]:     # Read as plain binary data
                    characters += open(file, "rb").read()
                else:           # Read as encoded Unicode
                    characters.append(open(file, "r",
                                    encoding=d["-e"]).read())
            except UnicodeError:
                msg = ("'{0}' is not a valid {1} text file".
                    format(file, d["-e"]))
                print(msg, file=sys.stderr)
                exit(1)
    if not d["-b"]:
        characters = ''.join(characters)
    d["characters"] = characters
    for char in characters:
        if d["-b"]:
            d["char_counts"][char] += 1
        else:
            d["char_counts"][ord(char)] += 1
def Categorize():
    '''Compute a dictionary d["cat"] containing the category number
    of each of the characters in the string d["characters"].
    '''
    d["cat"] = cat = defaultdict(set)
    for char in d["characters"]:
        if d["-b"]:
            if isinstance(char, int):
                char = chr(char)
        if char in string.whitespace:
            cat[0].add(char)
        elif ord(char) in d["ctrl"]:
            cat[1].add(char)
        elif char in string.ascii_lowercase:
            cat[2].add(char)
        elif char in string.ascii_uppercase:
            cat[3].add(char)
        elif char in string.digits:
            cat[4].add(char)
        elif char in string.punctuation:
            cat[5].add(char)
        elif ord(char) < 0x80:
            cat[6].add(char)
        else:
            if ord(char) < 0x100:
                cat[7].add(char)
            else:
                cat[8].add(char)
def PrintCounts():
    C, D = d["char_counts"], d["ctrl"]
    chars = list(C.keys())
    chars.sort()
    print(dedent('''
      Codepoint             Count
    Decimal   Hex      Decimal    Hex      Character
    -------  ------ ---------- ---------   ---------
    '''))
    for c in chars:
        char, count = D[c] if c in D else chr(c), C[c]
        print(f"{c:7d}{c:8x}{count:11}{count:10x}{char:^18s}")
def Translate(chars):
    '''Convert any control characters in chars into their symbolic
    form.
    '''
    out = []
    for c in chars:
        if ord(c) in d["ctrl"]:
            out.append(d["ctrl"][ord(c)])
        else:
            out.append(c)
    return ' '.join(out)
def PrintCharacters(characters, indent):
    '''Fit the characters in the existing line width; wrap to the next
    lines if needed.  indent is the number of spaces to indent.
    '''
    s = ""
    maxwidth = d["width"] - len(indent) - 1
    for c in characters.split():
        if len(s + " " + c) <= maxwidth:
            s += " " + c
            continue
        else:
            print(s)
            print(indent, end=" ")
            s = ""
    if s:
        print(s)
def PrintResults():
    res = []
    for key, val in d["cat"].items():
        cat = d["categories"][key]
        chars = list(val)
        chars.sort()
        res.append((key, cat, ''.join(chars)))
    res.sort()
    w = max([len(i[1]) for i in res])
    C = {
        0 : "trq",      # Whitespace
        1 : "roy",      # Ctrl
        2 : "cynl",     # Lowercase
        3 : "ornl",     # Uppercase
        4 : "lwnl",     # Decimal digits
        5 : "magl",     # Punctuation
        6 : "wht",      # Remaining 7-bit characters
        7 : "yell",     # 8-bit with high bit set
        8 : "purl",     # Other Unicode
    }
    for i, cat, chars in res:
        characters = Translate(chars)
        if d["-a"] and cat in ("Unicode", "8bit"):
            continue
        if d["-C"]:
            print(f"{t(C[i])}", end="")
        print("{cat:{w}} ".format(**locals()), end="")
        PrintCharacters(characters, " "*w)
        if d["-C"]:
            print(f"{t.n}", end="")
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [file1 [file2...]]
      Lists the characters used in the indicated files.  Use - as a file
      name to read stdin.  Assumes text files are encoded in {enc}; use -b
      option to read the files in binary.
     
    Options:
        -a      Limit printout to 7-bit ASCII characters
        -b      Read files as binary
        -C      Don't use colorized printing
        -c      Print out counts
        -E      Show allowed encodings
        -e enc  Set the encoding method for text files.  You can use any
                encoding method supported by your python version.  Case is
                not important and hyphens and underscores in the name can
                be removed.  Defaults to {d["-e"]}.
    '''))
    exit(status)
def ParseCommandLine():
    d["-a"] = False
    d["-b"] = False
    d["-C"] = True
    d["-c"] = False
    d["-e"] = "UTF-8"
    d["7-bit clean"] = True
    d["char_counts"] = defaultdict(int)
    d["ctrl"] = {   # ASCII control code names
        0: "nul", 1: "soh", 2: "stx", 3: "etx", 4: "eot", 5: "enq", 6:
        "ack", 7: "bel", 8: "bs", 9: "ht", 10: "lf", 11: "vt", 12: "ff",
        13: "cr", 14: "so", 15: "si", 16: "dle", 17: "dc1", 18: "dc2",
        19: "dc3", 20: "dc4", 21: "nak", 22: "syn", 23: "etb", 24:
        "can", 25: "em", 26: "sub", 27: "esc", 28: "fs", 29: "gs", 30:
        "rs", 31: "us", 32: "sp", 127: "del"
    }
    d["categories"] = {
        0: "Whtspc",     # Whitespace
        1: "Ctrl",       # Control characters in d["ctrl"]
        2: "Lower",      # Lowercase ASCII letters (97-122)
        3: "Upper",      # Uppercase ASCII letters (97-122)
        4: "Digits",     # Decimal digits
        5: "Punct",      # Punctuation
        6: "Other7",     # Remaining 7-bit characters
        7: "8bit",       # 8-bit character with high bit set
        8: "Unicode",    # Other Unicode
    }
    # Get width of screen
    if "COLUMNS" in os.environ:
        d["width"] = max(10, int(os.environ["COLUMNS"]) - 1)
    else:
        d["width"] = 79
    try:
        opts, args = getopt.getopt(sys.argv[1:], "abCcEe:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("abCc"):
            d[o] = not d[o]
        elif o in ("-E",):
            print(dedent(f'''
            Allowed encodings:
            {wrap(encodings)}'''))
            exit(0)
        elif o in ("-e",):
            d["-e"] = GetEncoding(a)
            if d["-e"] is None:
                Error("'{0}' encoding not recognized".format(a))
    if not args:
        Usage()
    return args
if __name__ == "__main__":
    d = {}  # Options dictionary
    d["files"] = ParseCommandLine()
    GetCharacterCounts()
    if d["-c"]:
        PrintCounts()
    else:
        Categorize()
        PrintResults()

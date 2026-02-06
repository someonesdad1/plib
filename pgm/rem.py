'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Remove character classes oo>
        <oo desc ∞ Description oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 

                - Todo items

        oo>
    '''
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        # List of python codecs from the 3.12.2 documentation
        g.codecs = set('''
            1125 273 437 646 850 852 855 857 858 860 861 862 863 865 866 869 8859 932
            936 949 950 CP-GR CP-IS EBCDIC-CP-BE EBCDIC-CP-CH EBCDIC-CP-HE IBM037 IBM039
            IBM273 IBM424 IBM437 IBM500 IBM775 IBM850 IBM852 IBM855 IBM857 IBM858 IBM860
            IBM861 IBM862 IBM863 IBM864 IBM865 IBM866 IBM869 L1 L10 L2 L3 L4 L5 L6 L7 L8
            L9 U16 U32 U7 U8 UTF UTF-16BE UTF-16LE UTF-32BE UTF-32LE arabic ascii big5
            big5-hkscs big5-tw big5hkscs chinese cp037 cp1006 cp1026 cp1125 cp1140
            cp1250 cp1251 cp1252 cp1253 cp1254 cp1255 cp1256 cp1257 cp1258 cp1361 cp154
            cp273 cp424 cp437 cp500 cp65001 cp720 cp737 cp775 cp819 cp850 cp852 cp855
            cp856 cp857 cp858 cp860 cp861 cp862 cp863 cp864 cp865 cp866 cp866u cp869
            cp874 cp875 cp932 cp936 cp949 cp950 csIBM273 csbig5 csiso2022jp csiso2022kr
            csiso58gb231280 csptcp154 csshiftjis cyrillic cyrillic-asian euc-cn
            euc_jis_2004 euc_jisx0213 euc_jp euc_kr euccn eucgb2312-cn eucjis2004
            eucjisx0213 eucjp euckr gb18030 gb18030-2000 gb2312 gb2312-1980 gb2312-80
            gbk greek greek8 hebrew hkscs hz hz-gb hz-gb-2312 hzgb ibm1026 ibm1125
            ibm1140 iso-2022-jp iso-2022-jp-1 iso-2022-jp-2 iso-2022-jp-2004
            iso-2022-jp-3 iso-2022-jp-ext iso-2022-kr iso-8859-1 iso-8859-10 iso-8859-11
            iso-8859-13 iso-8859-14 iso-8859-15 iso-8859-16 iso-8859-2 iso-8859-3
            iso-8859-4 iso-8859-5 iso-8859-6 iso-8859-7 iso-8859-8 iso-8859-9 iso-ir-58
            iso2022_jp iso2022_jp_1 iso2022_jp_2 iso2022_jp_2004 iso2022_jp_3
            iso2022_jp_ext iso2022_kr iso2022jp iso2022jp-1 iso2022jp-2 iso2022jp-2004
            iso2022jp-3 iso2022jp-ext iso2022kr iso8859-1 iso8859_10 iso8859_11
            iso8859_13 iso8859_14 iso8859_15 iso8859_16 iso8859_2 iso8859_3 iso8859_4
            iso8859_5 iso8859_6 iso8859_7 iso8859_8 iso8859_9 jisx0213 johab koi8_r
            koi8_t koi8_u korean ks_c-5601 ks_c-5601-1987 ks_x-1001 ksc5601 ksx1001
            kz1048 kz_1048 latin latin1 latin10 latin2 latin3 latin4 latin5 latin6
            latin7 latin8 latin9 latin_1 mac_centeuro mac_cyrillic mac_greek mac_iceland
            mac_latin2 mac_roman mac_turkish maccentraleurope maccyrillic macgreek
            maciceland macintosh maclatin2 macroman macturkish ms-kanji ms1361 ms932
            ms936 ms949 ms950 mskanji pt154 ptcp154 rk1048 ruscii s_jis s_jisx0213
            shift_jis shift_jis_2004 shift_jisx0213 shiftjis shiftjis2004 shiftjisx0213
            sjis sjis2004 sjis_2004 sjisx0213 strk1048_2002 thai u-jis uhc ujis
            unicode-1-1-utf-7 us-ascii utf16 utf32 utf8 utf_16 utf_16_be utf_16_le
            utf_32 utf_32_be utf_32_le utf_7 utf_8 utf_8_sig windows-1250 windows-1251
            windows-1252 windows-1253 windows-1254 windows-1255 windows-1256
            windows-1257 windows-1258'''.split())
if 1:   # Utility
    def GetColors():
        t.bin = t.cynl
        t.emph = t.purl
        t.err = t.redl
        t.dbg = t.sky if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
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
    def Manpage():
        print(dedent(f'''

        This tool is intended to be used to modify text files in various ways.  All of
        the operations except A remove specified characters from the input.  All of the
        operations except for A and 8 will work on binary input.  If you're getting
        results you don't expect, make sure you're using appropriate operations on the
        type of files/data used for input (the problem can probably be fixed by using or
        not using the -b and/or the -e options).

        '''))
    def Usage(status=0):
        e, b, n = t.purl, t.sky, t.n
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] letters [file1 [file2...]]
          Remove character classes from the files, as indicated by the letters.{e}
          The files are treated as UTF-8 text files{n} unless you change the encoding with
          the -e option or use -b.  Use '-' for stdin.  The letters are:{b}
            A   Convert Unicode characters to rough ASCII equivalents{n}
            a   Remove characters above 0x7f (i.e., keep only 7-bit characters)
            B   Remove characters under 0x20 except newline
            b   Remove characters under 0x20
            d   Remove characters that are ASCII digits (∈ string.digits)
            h   Remove characters that are hex digits (∈ string.hexdigits)
            l   Remove lower case letters (∈ string.ascii_lowercase)
            o   Remove characters that are octal digits (∈ string.octdigits)
            P   Remove non-printable characters (∉ string.printable)
            p   Remove punctuation (∈ string.punctuation)
            W   Remove whitespace except newlines
            w   Remove whitespace (∈ string.whitespace)
            u   Remove upper case letters (∈ string.ascii_uppercase){b}
            8   Remove all non-8-bit characters (if char > 0xff){n}
          The letter lines {b}in this color{n} are those that can only be used on text
          files, as they have no meaning on binary files.
        Options:
          -b    Treat the files as binary, not text
          -e e  Change the encoding used (names from the python codecs module)
          -H    Print a manpage
          -l    Convert all text to lower case
          -u    Convert all text to upper case
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = False     # Binary file input
        d["-e"] = False     # Binary file input
        d["-l"] = False     # Convert to lower case
        d["-u"] = False     # Convert to upper case
        if len(sys.argv) < 2:
            GetColors()
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)

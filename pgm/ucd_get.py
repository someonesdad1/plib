'''
Extract and print the valid codepoints from ucd.all.grouped.ver16.xml
'''
from util import Ranges
import re
import sys
from color import t
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()
t.title = t.purl
t.ucd = t.skyl
def GetXMLFileName(version):
    '''Return the URL of the indicated version, where version is an int.
    Example:  GetXMLFileName(version) returns 
    https://www.unicode.org/Public/14.0.0/ucdxml/ucd.nounihan.grouped.zip.
    The returned URL gives a zip file that contains the ucd files in /plib/pgm.
    '''
    # Get URL of file
    versions = {
        6: "6.3.0",
        7: "7.0.0",
        8: "8.0.0",
        9: "9.0.0",
        10: "10.0.0",
        11: "11.0.0",
        12: "12.1.0",
        13: "13.0.0",
        14: "14.0.0",
        15: "15.1.0",
        16: "1k.0.0",
    }
    head = "https://www.unicode.org/Public"
    file = "ucd.nounihan.grouped.zip"
    ver = versions[version]
    url = f"{head}/{ver}/ucdxml/{file}"
    return url
def ShowURLs():
    t.print(f"{t.title}Zipped XML data files for UCD nounihan, grouped:")
    for i in range(6, 17):
        print(f"  {i:2d}   {GetXMLFileName(i)}")
def GetCodepoints(file):
    '''Return a list of valid codepoints as integers.  The method is to read the
    indicated XML file (download from https://www.unicode.org/versions/).  Note the 
    downloaded files are the nounihan versions.
    '''
    r = re.compile(r'<char cp="([0123456789ABCDEF]*?)"')
    codepoints = []
    with open(file) as f:
        for line in f:
            mo = r.search(line.strip())
            if mo:
                codepoints.append(int(mo.groups()[0], 16))
    return codepoints
def Len(i):
    if isinstance(i, int):
        return 1
    else:
        return i[1] - i[0]
def Pct(n, total, digits=0):
    return f"{100*n/total:.{digits}f}"
def DumpCodepoints(file, codepoints):
    t.print(f"  {t.ucd}{file}")
    cp = codepoints
    n = len(cp)
    N = max(cp)
    acp = set(range(N + 1))
    print(f"    N = max codepoint = {N:6d} = {hex(N)}")
    print(f"    n = |cp|          = {n:6d} = {hex(n)}")
    p = 100*n/N
    p1 = 100 - p
    print(f"    % used = {Pct(n, N)}%")
def ShowBasicStatistics():
    t.print(f"{t.title}UCD files in /plib/pgm:")
    files = '''
        /plib/pgm/ucd.nounihan.grouped.ver11.xml
        /plib/pgm/ucd.nounihan.grouped.ver12.1.xml
        /plib/pgm/ucd.nounihan.grouped.ver13.xml
        /plib/pgm/ucd.nounihan.grouped.ver14.xml
        /plib/pgm/ucd.nounihan.grouped.ver16.xml
    '''
        #ucd.all.grouped.ver16.xml
    for file in files.split():
        codepoints = GetCodepoints(file)
        DumpCodepoints(file, codepoints)
    # Results
    '''
        /plib/pgm/ucd.nounihan.grouped.ver11.xml
        N = max codepoint = 917999 = 0xe01ef
        n = |cp|          =  49645 = 0xc1ed
        % used = 5%
        /plib/pgm/ucd.nounihan.grouped.ver12.1.xml
        N = max codepoint = 917999 = 0xe01ef
        n = |cp|          =  50200 = 0xc418
        % used = 5%
        /plib/pgm/ucd.nounihan.grouped.ver13.xml
        N = max codepoint = 917999 = 0xe01ef
        n = |cp|          =  51161 = 0xc7d9
        % used = 6%
        /plib/pgm/ucd.nounihan.grouped.ver14.xml
        N = max codepoint = 917999 = 0xe01ef
        n = |cp|          =  51990 = 0xcb16
        % used = 6%
        /plib/pgm/ucd.nounihan.grouped.ver16.xml
        N = max codepoint = 917999 = 0xe01ef
        n = |cp|          =  57487 = 0xe08f
        % used = 6%
        ucd.all.grouped.ver16.xml
        N = max codepoint = 917999 = 0xe01ef
        n = |cp|          = 155063 = 0x25db7
        % used = 17%

    Conclusions
        - Always use direct set of valid codepoints
    '''

if __name__ == "__main__":  
    ShowURLs()
    ShowBasicStatistics()

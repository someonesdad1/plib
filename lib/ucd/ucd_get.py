'''
https://www.unicode.org/Public provides XML files that give the details of the Unicode
Character Database.  These files are downloaded and stored in the /plib/lib/ucd  directory 
and are named as ucd.nounihan.grouped.verXXX.xml, where XXX is a string like "14" (or
"15.1" for the first revision of the version 15 major revision number).
    
This file builds the "ucd.XXX.pickle" files, where XXX match the above XXX revision
number.  This pickle file is then loaded by /plib/ucd.py to provide the ucd dictionary,
which lets e.g. /plib/pgm/uni.py to be a tool to look up information on Unicode
characters.
    
Extract and print the valid codepoints from ucd.all.grouped.ver16.xml
'''
if 1:   # Header
    if 1:   # Standard imports
        #import re
        import pickle
        import sys
        import xml.etree.ElementTree as ET
        from pathlib import Path
        from time import asctime
    if 1:   # Custom imports
        #from util import Ranges
        from color import t
        from wrap import dedent
        if len(sys.argv) > 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()     # Instance to hold global variables
        # Which XML file to get our data from
        g.input_file = ""
        # Where to write our pickled ucd dictionary
        g.pickle_file = ""
        # Colors for printing output
        t.title = t.purl
        t.ucd = t.skyl
        # The ucd dictionary
        ucd = {}
        # Describe the ucd dictionary's structure
        doc = dedent('''
            Structure of data in the python ucd dictionary constructed on
            %s
                Types:
                    .i = integer
                    .s = string
                    .d = dict keyed by a string and whose values are strings
                cp = codepoint = integer
                attributes will be a dictionary keyed by strings with string values
                (i.e., they're the attrib attribute of the XML Element objects).
            ucd = {
                "namespace" : "http://www.unicode.org/ns/2003/ucd/1.0",
                "version" : "Unicode x.x.x",
                "groups" : {
                    groupID.i : {attributes.d},
                    ...
                },
                "chars" : {
                    cp : [groupID.i, attributes.d],
                    ...
                },
                "blocks" : [  # Note blocks are not contiguous
                    # A block is a group of codepoints with sequential numbers.
                    [cp_start.i, cp_end.i, name.s],
                    ...
                ],
                "named-sequences" : [
                    [name.s, (cp0.i, cp1.i, ...)],
                    ...
                ],
                "reserved" : {
                    # Some groups will have reserved intervals.  Example:  see the
                    # Greek codepoints around 0370.
                    groupID.i : [attributes0.d, ...],
                    ...
                },
                "aliases" : {
                    # Some codepoints have aliases.
                    cp : [attributes0.d, attributes1.d, ...],
                    ...
                },
                # Note:  the following are left in pretty much the raw data form
                # because I don't have any use for them.
                "normalization-corrections" : [   # size = 6
                    {data0},
                    {data1},
                    ...
                ],
                "standardized-variants" : [   # size = 1309
                    {data0},
                    {data1},
                    ...
                ],
                "cjk-radicals" : [   # size = 239
                    {data0},
                    {data1},
                    ...
                ],
                "emoji-sources" : [   # size = 722
                    {data0},
                    {data1},
                    ...
                ],
            }''' % asctime())
#if 0:   # Original file stuff; need to refactor & cleanse
#    def GetXMLFileName(version):
#        '''Return the URL of the indicated version, where version is an int.
#        Example:  GetXMLFileName(version) returns 
#        https://www.unicode.org/Public/14.0.0/ucdxml/ucd.nounihan.grouped.zip.
#        The returned URL gives a zip file that contains the ucd files in /plib/pgm.
#        '''
#        # Get URL of file
#        versions = {
#            6: "6.3.0",
#            7: "7.0.0",
#            8: "8.0.0",
#            9: "9.0.0",
#            10: "10.0.0",
#            11: "11.0.0",
#            12: "12.1.0",
#            13: "13.0.0",
#            14: "14.0.0",
#            15: "15.1.0",
#            16: "16.0.0",
#        }
#        head = "https://www.unicode.org/Public"
#        file = "ucd.nounihan.grouped.zip"
#        ver = versions[version]
#        url = f"{head}/{ver}/ucdxml/{file}"
#        return url
#    def ShowURLs():
#        t.print(f"{t.title}Zipped XML data files for UCD nounihan, grouped:")
#        for i in range(6, 17):
#            print(f"  {i:2d}   {GetXMLFileName(i)}")
#    def GetCodepoints(file):
#        '''Return a list of valid codepoints as integers.  The method is to read the
#        indicated XML file (download from https://www.unicode.org/versions/).  Note the 
#        downloaded files are the nounihan versions.
#        '''
#        r = re.compile(r'<char cp="([0123456789ABCDEF]*?)"')
#        codepoints = []
#        with open(file) as f:
#            for line in f:
#                mo = r.search(line.strip())
#                if mo:
#                    codepoints.append(int(mo.groups()[0], 16))
#        return codepoints
#    def Len(i):
#        if isinstance(i, int):
#            return 1
#        else:
#            return i[1] - i[0]
#    def Pct(n, total, digits=0):
#        return f"{100*n/total:.{digits}f}"
#    def DumpCodepoints(file, codepoints):
#        t.print(f"  {t.ucd}{file}")
#        cp = codepoints
#        n = len(cp)
#        N = max(cp)
#        acp = set(range(N + 1))
#        print(f"    N = max codepoint = {N:6d} = {hex(N)}")
#        print(f"    n = |cp|          = {n:6d} = {hex(n)}")
#        p = 100*n/N
#        p1 = 100 - p
#        print(f"    % used = {Pct(n, N)}%")
#    def ShowBasicStatistics():
#        t.print(f"{t.title}UCD files in /plib/pgm:")
#        files = '''
#            /plib/pgm/ucd.nounihan.grouped.ver11.xml
#            /plib/pgm/ucd.nounihan.grouped.ver12.1.xml
#            /plib/pgm/ucd.nounihan.grouped.ver13.xml
#            /plib/pgm/ucd.nounihan.grouped.ver14.xml
#            /plib/pgm/ucd.nounihan.grouped.ver16.xml
#        '''
#            #ucd.all.grouped.ver16.xml
#        for file in files.split():
#            codepoints = GetCodepoints(file)
#            DumpCodepoints(file, codepoints)
#        # Results
#        '''
#            /plib/pgm/ucd.nounihan.grouped.ver11.xml
#            N = max codepoint = 917999 = 0xe01ef
#            n = |cp|          =  49645 = 0xc1ed
#            % used = 5%
#            /plib/pgm/ucd.nounihan.grouped.ver12.1.xml
#            N = max codepoint = 917999 = 0xe01ef
#            n = |cp|          =  50200 = 0xc418
#            % used = 5%
#            /plib/pgm/ucd.nounihan.grouped.ver13.xml
#            N = max codepoint = 917999 = 0xe01ef
#            n = |cp|          =  51161 = 0xc7d9
#            % used = 6%
#            /plib/pgm/ucd.nounihan.grouped.ver14.xml
#            N = max codepoint = 917999 = 0xe01ef
#            n = |cp|          =  51990 = 0xcb16
#            % used = 6%
#            /plib/pgm/ucd.nounihan.grouped.ver16.xml
#            N = max codepoint = 917999 = 0xe01ef
#            n = |cp|          =  57487 = 0xe08f
#            % used = 6%
#            ucd.all.grouped.ver16.xml
#            N = max codepoint = 917999 = 0xe01ef
#            n = |cp|          = 155063 = 0x25db7
#            % used = 17%
#    
#        Conclusions
#            - Always use direct set of valid codepoints
#        '''
if 1:   # Functions moved to here from ucd.py
    def RemoveNS(s):
        loc = s.find("}")
        return s if loc == -1 else s[loc + 1 :]
    def Blocks(child, ucd):
        ucd["blocks"] = d = []
        for i in child:
            a = i.attrib
            e = tuple([int(a["first-cp"], 16), int(a["last-cp"], 16), a["name"]])
            d.append(e)
        ucd["blocks"] = tuple(ucd["blocks"])
    def NamedSequences(child, ucd):
        ucd["named-sequences"] = d = []
        for i in child:
            a = i.attrib
            e = tuple([a["cps"], a["name"]])
            d.append(e)
        ucd["named-sequences"] = tuple(ucd["named-sequences"])
    def StandardizedVariants(child, ucd):
        ucd["standardized-variants"] = d = []
        for i in child:
            a = i.attrib
            e = tuple([a["cps"], a["desc"], a["when"]])
            d.append(e)
        ucd["named-sequences"] = tuple(ucd["named-sequences"])
    def GetNamespace(tag):
        '''tag is the root node's tag and contains the namespace; e.g.
        '{http://www.unicode.org/ns/2003/ucd/1.0}ucd'.  Parse it out and
        return it.
        '''
        s = tag[tag.find("{") + 1 :]
        return s[: s.find("}")]
    def GetItem(name, parent, ucd):
        "Return the item in a sequence with no further interpretation."
        ucd[name] = d = []
        for child in parent:
            d.append(child.attrib)
        ucd[name] = tuple(ucd[name])
    def Group(group, parent, ucd):
        '''group is an integer, parent is the XML branch of characters, ucd
        is the database dictionary.
        '''
        ucd["groups"][group] = parent.attrib
        for child in parent:
            d = child.attrib
            try:
                cp = int(d["cp"], 16)
                ucd["chars"][cp] = (group, d)
                # In Unicode 7.0.0, the only children of child have
                # name-alias tags.
                for i in child:
                    if cp not in ucd["aliases"]:
                        ucd["aliases"][cp] = []
                    ucd["aliases"][cp].append(i.attrib)
            except KeyError:
                # It must be a reserved interval in this group
                if group not in ucd["reserved"]:
                    ucd["reserved"][group] = []
                ucd["reserved"][group].append(d)
    def BuildDataFile(input_file, pickle_file, dbg=False):
        global ucd
        tag_warning = False
        if dbg:
            input_file = input_file + ".shortened"
        tree = ET.parse(input_file)
        root = tree.getroot()
        tags = set(
            (  # Allowed keys for ucd dictionary
                "blocks",
                "cjk-radicals",
                "description",
                "emoji-sources",
                "named-sequences",
                "normalization-corrections",
                "repertoire",
                "standardized-variants",
                "provisional-named-sequences",
            )
        )
        ucd["doc"] = doc
        ucd["xml_file"] = str(input_file)
        ucd["namespace"] = GetNamespace(root.tag)
        ucd["reserved"] = {}
        ucd["aliases"] = {}
        no_process = set(
            (
                "cjk-radicals",
                "emoji-sources",
                "normalization-corrections",
                "standardized-variants",
            )
        )
        for child in root:
            tag = RemoveNS(child.tag)
            if tag not in tags:
                if not tag_warning:
                    t.print(f"  {t.redl}{tag!r} is unrecognized tag")
                    tag_warning = True
                continue
            if tag == "blocks":
                Blocks(child, ucd)
            elif tag in no_process:
                GetItem(tag, child, ucd)
            elif tag == "description":
                ucd["version"] = child.text
            elif tag == "named-sequences":
                NamedSequences(child, ucd)
            elif tag == "repertoire":
                ucd["chars"] = {}
                ucd["groups"] = {}
                for i, group in enumerate(child):
                    Group(i, group, ucd)
        # Construct ucd["codepoints"], which is a set of valid integer values for the
        # codepoints in this version
        ucd["codepoints"] = set(ucd["chars"].keys())
        # ucd["n"] is the number of valid codepoints
        ucd["n"] = n = len(ucd["codepoints"])
        print(f"  ucd dictionary constructed from {g.input_file}")
        print(f"  {n} = {hex(n)} codepoints")
    def BuildPickleFiles():
        t.print(f"{t.sky}Processing", g.input_file)
        BuildDataFile(g.input_file, g.pickle_file)
        with open(g.pickle_file, "wb") as f:
            pickle.dump(ucd, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    # Run as a script:  build the pickle files for the xml files
    def GetXMLFileName(version):
        'Return the XML file name to open for the given integer version'
        s, x = "ucd.nounihan.grouped.ver", ".xml"
        d = {
            11: f"{s}11{x}",
            12: f"{s}12.1{x}",
            13: f"{s}13{x}",
            14: f"{s}14{x}",
            15: f"{s}15.1{x}",
            16: f"{s}16{x}",
        }
        return d[version]
    overwrite = True if len(sys.argv) > 1 else False
    for version in range(11, 17):
        g.input_file = GetXMLFileName(version)
        g.pickle_file = f"ucd.{version}.pickle"
        if Path(g.pickle_file).exists() and not overwrite:
            continue
        BuildPickleFiles()
else:
    # Loaded as module:  load the ucd dictionary
    with open(g.pickle_file, "rb") as f:
        ucd = pickle.load(f)

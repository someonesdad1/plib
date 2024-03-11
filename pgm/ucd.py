'''
Provide the ucd dictionary, a container of the Unicode Character Database (UCD)
'''

# Copyright (C) 2014, 2019 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import xml.etree.ElementTree as ET
import pickle
from time import asctime
import os
from pathlib import Path as P
import re
import sys
import unicodedata
from collections import OrderedDict
from pprint import pprint as pp
if 0:
    import debug
    debug.SetDebugger()

__all__ = ["ucd"]

# This must be one of the grouped XML files at http://www.unicode.org/Public/UCD/latest/ucdxml (for
# other versions start at https://www.unicode.org/Public/).  I recommend the non-Unihan file unless
# you need the extra Chinese characters.  The documentation for the contents of this file is in UAX
# #42 http://www.unicode.org/reports/tr42.  This grouped file results in a data file size about an
# order of magnitude less than the flat XML file.

def GetVersion():
    '''Build the pickled data file.  If you pass in a string as an
    argument on the command line, the latest XML file will be used.
    Otherwise, the datafile's version will match the one python is
    using.
    '''
    if len(sys.argv) > 1:
        return P("ucd.nounihan.grouped.ver13.xml")
    else:
        v = unicodedata.unidata_version
        if v == "11.0.0":
            return P("ucd.nounihan.grouped.ver11.xml")
        elif v == "12.0.0":
            return P("ucd.nounihan.grouped.ver12.1.xml")
        elif v == "13.0.0":
            return P("ucd.nounihan.grouped.ver13.xml")
        elif v == "14.0.0":
            return P("ucd.nounihan.grouped.ver14.xml")
        else:
            raise ValueError(f"{v} is unsupported Unicode version")
input_file = GetVersion()

# The pickle file will contain the persisted UCD dictionary in ucd.
pickle_file = P("/plib/pgm/ucd.pickle")

# The UCD dictionary.
ucd = {}

how_to_get_datafile = '''
  Download the ucd.nounihan.grouped.xml file from
  http://www.unicode.org/Public/UCD/latest/ucdxml/.  Change the 
  global variable input_file to point to this file.
'''[1:-1]

# Description of the data structure we will construct (it's stored in the ucd dictionary)
doc = '''
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
}
''' % asctime()

def RemoveNS(s):
    loc = s.find("}")
    return s if loc == -1 else s[loc + 1:]

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
    s = tag[tag.find("{") + 1:]
    return s[:s.find("}")]

def GetItem(name, parent, ucd):
    'Return the item in a sequence with no further interpretation.'
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
    if dbg:
        input_file = input_file + ".shortened"
    tree = ET.parse(input_file)
    root = tree.getroot()
    tags = set((    # Allowed keys for ucd dictionary
        "blocks",
        "cjk-radicals",
        "description",
        "emoji-sources",
        "named-sequences",
        "normalization-corrections",
        "repertoire",
        "standardized-variants",
        "provisional-named-sequences",
    ))
    ucd["doc"] = doc
    ucd["xml_file"] = str(input_file)
    ucd["namespace"] = GetNamespace(root.tag)
    ucd["reserved"] = {}
    ucd["aliases"] = {}
    no_process = set((
        "cjk-radicals",
        "emoji-sources",
        "normalization-corrections",
        "standardized-variants",
    ))
    for child in root:
        tag = RemoveNS(child.tag)
        if tag not in tags:
            raise ValueError("Unrecognized tag")
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
    print("ucd dictionary constructed from %s" % input_file)

def BuildPickleFile():
    BuildDataFile(input_file, pickle_file)
    with open(pickle_file, 'wb') as f:
        pickle.dump(ucd, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    try:
        os.remove(pickle_file)
    except FileNotFoundError:
        pass
    BuildPickleFile()
else:
    with open(pickle_file, 'rb') as f:
        ucd = pickle.load(f)

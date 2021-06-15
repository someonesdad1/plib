'''
Create an index of picture files
    The index file is pickled, then you can quickly search for file
    names with regular expressions.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Create an index of picture files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import pathlib
    import pickle
    import re
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    bitmap_extensions = set('''
        .pspimage .jfif .gif .tif .tiff .png .jpg .ppm .ps .eps .bmp
        .emf .jls .jp2 .jpc .j2k .jpf .jpg .jpeg .jpe .kdc .pbm .pcd
        .pcx .pgm .psd .ras .sun .raw .sgi .rgb .sfw .wmf .xbm .xpm
    '''.split())
    video_extensions = set('''
        .swf .flv .avi .mpg .mpe .mpeg .mov .wmv .ogg
    '''.split())
    directories_to_index = set('''
        /cygdrive/d/pictures
        /doc
        /ebooks
        /elec
        /help
        /help1
        /home/Don
        /math
        /pylib
        /science
        /shop
        /tools
        '''.split())
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        s = print(dedent(f'''
        Usage:  {name} [options] regex1 [regex2 ...]
          Search for bitmap files whose name matches the given regular
          expression(s).
        
        Options:
            -I      Perform indexing of the hard disk
            -v      Search for video files instead of bitmaps
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-I"] = False     # Perform indexing
        d["-v"] = False     # Find video files
        d["bitmaps"] = []
        d["videos"] = []
        try:
            opts, args = getopt.getopt(sys.argv[1:], "Iv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Iv"):
                d[o] = not d[o]
        # Get index file name
        p = pathlib.Path(sys.argv[0]).resolve()
        pp = p.parts[-1].replace(".py", ".data")
        d["index_file"] = p.with_name(pp)
        # Index things if indicated
        if d["-I"]:
            GenerateIndex()
            exit(0)
        else:
            # Print usage if missing arguments
            if len(sys.argv) < 2:
                Usage(d)
            # Read in the index
            fp = open(d["index_file"], "rb")
            d["bitmaps"] = pickle.load(fp)
            d["videos"] = pickle.load(fp)
        return args
def GenerateIndex():
    print(f"Updating index file {d['index_file']}")
    # Search all files
    b = d["bitmaps"]
    v = d["videos"]
    for dir in directories_to_index:
        for p in pathlib.Path(dir).glob("**/*"):
            s = p.suffix
            if s and s.lower() in bitmap_extensions:
                b.append(p)
            elif s and s.lower() in video_extensions:
                v.append(p)
    if 0:   # Debug print the data
        print("Bitmaps")
        for i in b:
            print("  ", i)
        print("Videos")
        for i in v:
            print("  ", i)
    # Store the data
    fp = open(d["index_file"], "wb")
    pickle.dump(b, fp)
    pickle.dump(v, fp)
def Search(regexps):
    for r in regexps:
        for file in d["videos"] if d["-v"] else d["bitmaps"]:
            mo = r.search(str(file))
            if mo:
                print(file)
if __name__ == "__main__":
    d = {}      # Options dictionary
    regexps = [re.compile(i, re.I) for i in ParseCommandLine(d)]
    Search(regexps)

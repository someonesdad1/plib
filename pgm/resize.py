'''
Resize a set of images
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014, 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Resize a set of images
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx
    import getopt
    import pathlib
    import sys
if 1:   # Custom imports
    from wrap import dedent
    from PIL import Image, __version__ as pversion
    from color import C
if 1:   # Global variables
    class g: pass
    P = pathlib.Path
    g.err = C.lred
    g.n = C.norm
    g.dbg = C.yel
    g.dbg_file = C.lmag
    g.debug = False
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Debug(*msg, **kw):
    if g.debug:
        print(f"{g.dbg}", end="")
        print(*msg, **kw)
        print(f"{g.n}", end="")
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] p% file1 [file2...]
      Resize image files (uses PILLOW {pversion}) to be p% of the original size.
      Formats that can be read and written are:
          bmp eps gif ico jpeg pcx png ppm tga tiff 
      You can also write to a PDF file.
    Options:
      -D    Turn on debug printing
      -d d  Specify a directory d where the new files should be put.  The old
            files are not changed.
      -e e  Change the extension of the file
      -o    Force overwriting of the existing files.  You must use this option
            even if there is no -d option.
        '''))
    exit(status)
def ParseCommandLine():
    d["-d"] = None      # Output directory
    d["-e"] = None      # New extension
    d["-o"] = False     # Overwrite existing file
    d["-p"] = 100       # Scaling factor in %
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "Dd:e:o")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "o":
            d[o] = not d[o]
        elif o == "-D":
            g.debug = True
        elif o == "-d":
            d[o] = P(a)
        elif o == "-e":
            s = "bmp eps gif ico jpg jpeg pcx png ppm tga tiff pdf"
            allowed = set(s.split())
            if a.lower() not in s:
                Error(f"'{a}' is an unsupported format")
            d[o] = "." + a
        elif o == "-o":
            d[o] = True
        elif o == "-p":
            d[o] = float(a)
            if d[o] <= 0:
                Error("-p option must be > 0")
    if len(args) < 2:
        Usage()
    # Get scaling percentage
    try:
        d["-p"] = Int(float(args[0]))
    except Exception:
        Error(f"'{args[0]}' is a bad percentage")
    if g.debug:
        Debug(dedent(f'''
        Command line:  '{" ".join(sys.argv[1:])}'
            d["-d"] = '{d["-d"]}'
            d["-e"] = {d["-e"]}
            d["-o"] = {d["-o"]}
            Scaling percentage = {Int(d["-p"])}%
        '''))
    return args[1:]
def Int(x):
    return int(x) if x == int(x) else x
def ProcessFile(file):
    assert(isinstance(file, pathlib.Path))
    Debug(f"{g.dbg_file}Processing '{file}' "
          f"(size = {file.stat().st_size}){g.dbg}")
    new_name = file
    if d["-e"]:
        new_name = P(new_name.stem + d["-e"])
        Debug(f"  New name with extension is '{new_name}'")
    if d["-d"]:
        new_name = d["-d"]/file
        Debug(f"  Will be written to '{new_name}'")
    if new_name == file:
        # Wants to overwrite the existing file
        if not d["-o"]:
            Error("Need to use -o option for overwriting an existing file")
        else:
            new_name = None
            Debug(f"  Will overwrite the old file")
    ResizeFile(file, d["-p"], new_name=new_name)
def ResizeFile(file, percentage, new_name=None):
    '''Resizes the image in file and saves it to new_name.  If new_name
    is None, the original file will be overwritten.  percentage must be a
    floating point number greater than zero.
    '''
    assert(isinstance(file, pathlib.Path))
    if percentage <= 0:
        raise Exception("percentage must be a positive floating point number")
    im = Image.open(file)
    Debug("  Original size =", im.size)
    new_size = tuple([int(i*percentage/100) for i in im.size])
    Debug("  New size      =", new_size)
    im = im.resize(new_size)
    if new_name is not None:
        assert(isinstance(new_name, pathlib.Path))
        file = new_name
    im.save(file)
    Debug(f"  Saved to '{file}' (size = {file.stat().st_size})")
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine()
    for file in files:
        p = P(file)
        if not p.exists():
            print(f"{g.err}'{file}' doesn't exist{g.n}")
            continue
        ProcessFile(p)

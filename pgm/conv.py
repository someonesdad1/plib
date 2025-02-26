"""
Convert *.bmp files to *.png files.  This is intended to be used with
the B&K data recorders like the DAS220.  Copy the VNC screen to the
clipboard and use -v or -x to trim off the excess stuff.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # B&K DAS220 data recorder bitmap utility from VNC screenshots
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from PIL import Image, ImageGrab


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
      Change Windows bitmaps (*.bmp) to PNG files.  You can also pass in a
      *.png file and use -x.
    
    Options
      -g n  Copy from clipboard and given name n
      -v    Trim to VNC plot dimensions
      -x    Trim to XY plot dimensions
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-g"] = None  # Get from clipboard
    d["-v"] = False  # Trim to VNC
    d["-x"] = False  # Trim to XY
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg:vx")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "vx":
            d[o] = not d[o]
        elif o == "-g":
            d[o] = a
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args


def TrimVNCBanner(im):
    size = im.size
    # Trim off VNC banner
    right, lower = size
    left, upper = 0, 134
    im = im.crop((left, upper, right, lower))
    # Resize the image to be the same as the DAS220
    im = im.resize((1024, 600))
    return im


def TrimXY(im):
    size = im.size
    # Must be a DAS220 image size
    assert size == (1024, 600)
    # Trim to XY plot dimensions
    left, upper = 0, 59
    right, lower = 575, size[1]
    im = im.crop((left, upper, right, lower))
    return im


def HandleFile(file=None):
    """If file is None, then the desired image is on the clipboard."""
    if not file:
        if not d["-g"]:
            Error("Must give a file name")
        name = d["-g"]
        im = ImageGrab.grabclipboard()
        if not isinstance(im, Image.Image):
            Error("No image in clipboard")
    else:
        p = pathlib.Path(file).resolve()
        s = p.suffix.lower()
        if s == ".png":
            t = input("Do you want to overwrite the file? [n] ")
            if t.lower() != "y":
                exit(1)
            name = str(p)
        elif s == ".bmp":
            parent, stem = p.parent, p.stem
            name = parent / (stem + ".png")
        else:
            print("'{file}' not a bitmap", file=sys.stderr)
            return
    im = Image.open(p)
    if d["-v"]:
        im = TrimVNCBanner(im)
    if d["-x"]:
        im = TrimXY(im)
    im.save(name)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    if d["-g"]:
        HandleFile(None)
    for file in files:
        HandleFile(file)

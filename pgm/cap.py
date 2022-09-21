'''
This script will use the PIL (Python Imaging Library) to get an image
from the clipboard and save it to a file whose name is given on the
command line. 
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Save screen captures to file.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from PIL import Image, ImageGrab
        from wrap import dedent
        from f import flt
    if 1:   # Global variables
        ii = isinstance
        # Bitmap file Extensions PIL can write
        extensions = set(["." + i for i in "jpg png bmp gif ppm tif tiff".split()])
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] filename
        Copies the bitmap in the clipboard to the indicated file.  If you don't
        include an extension on the filename, it will default to '.png'. 
        Options:
            -l      Capture only the landscape monitor image
            -p      Capture only the portrait monitor image
            -r p    Resize image to p% of original
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-l"] = False     # Capture only the landscape screen
        d["-p"] = False     # Capture only the portrait screen
        d["-r"] = 1         # Resize fraction
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hlpr:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("lp"):
                d[o] = not d[o]
            if o == "-r":
                d[o] = abs(flt(a)/100)
                if not d[o]:
                    Error("-p option must be > 0")
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if len(args) > 1:
            Usage(d)
        if d["-l"] and d["-p"]:
            Error("Can't use both -l and -p")
        return args[0]
if 1:   # Core functionality
    def GetImageFromClipboard():
        # Note grabclipboard only works under Windows
        im = ImageGrab.grabclipboard()
        if not isinstance(im, Image.Image):
            Error("No image in clipboard")
        # Make sure it's 6000x3840; otherwise, the cropping options won't work
        w, h = im.size
        if w != 6000 or h != 3840:
            Error("Clipboard image isn't 6000x3840 pixels")
        return im
    def ResizeImage(im, size_fraction):
        r = abs(d["-r"])
        assert(r > 0)
        w, h = im.size
        W, H = int(r*w), int(r*h)
        im = im.resize((W, H))
    def SaveFile(im, p):
        '''im is Image object, p is a pathlib.Path object.  Write the image
        to this file.
        '''
        print(f"Image size = {im.size}, mode = {im.mode}")
        im.save(p)
    def GetLandscape(im):
        im = im.crop((2156, 309, 6000, 2413))
        return im
    def GetPortrait(im):
        im = im.crop((0, 0, 2142, 3840))
        return im
if __name__ == "__main__":
    d = {}      # Options dictionary
    filename = ParseCommandLine(d)
    p = P(filename)
    if not p.suffix:
        p = P(filename + ".png")
    else:
        if p.suffix not in extensions:
            Error(f"{p.suffix!r} not recognized image format")
    im = GetImageFromClipboard()
    if d["-l"]:         # Crop the landscape monitor part
        im = im.crop((2156, 309, 6000, 2413))
    elif d["-p"]:       # Crop the portrait monitor part
        im = im.crop((0, 0, 2142, 3840))
    if d["-r"] != 1:    # Resize the image
        r = abs(d["-r"])
        assert(r > 0)
        w, h = im.size
        W, H = int(r*w), int(r*h)
        im = im.resize((W, H))
    # Save the file
    print(f"Image size = {im.size}, mode = {im.mode}")
    im.save(p)

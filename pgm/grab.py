'''
This script will use the PIL to grab an image from the clipboard and
save it to a file whose name is given on the command line.  It was
originally written for the B&K daq project so I could capture the VNC
screenshots to a file for documentation.  
 
This won't work under the cygwin python installation, but it will if you
use a Winpython installation.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Copy image from clipboard to file
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import pathlib
    import subprocess
    import sys
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from PIL import Image, ImageGrab
    from wrap import dedent
    # Try to import the color.py module; if not available, the script
    # will still work (you'll just get uncolored output).
    try:
        import color as C
        _have_color = True
    except ImportError:
        class Dummy:    # Make a dummy color object to swallow function calls
            def fg(self, *p, **kw):
                pass
            def normal(self, *p, **kw):
                pass
            def __getattr__(self, name):
                pass
        C = Dummy()
        _have_color = False
if 1:   # Global variables
    # Extensions we can write
    dot_extensions = tuple(["." + i for i in 
            "jpg png bmp gif ppm tif tiff".split()])
    # Image size for VNC screen captures
    daq = (2308, 1489)
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] c1 [c2 c3 ... ext]
      Assumes an image has been copied to the clipboard.  Copies the image to
      the indicated file.  The file name to be copied to is constructed from
      the c? and ext elements on the command line.
    Options:
      -B      Same as -b but causes script to exit without writing file
      -b      For B&K DAQ project:  prints a warning message if the image
              size isn't {daq}, which comes from the VNC client using 
              100% for the screen size.  Note the VNC banner will be removed.
      -c s    Separator string s [\"{d["-c"]}\"].  The resulting file name
              will be 'c1{{sep}}c2{{sep}}c3.ext'.
      -o      Open the output file in IrfanView
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-B"] = False     # For B&K DAQ project (exit without writing)
    d["-b"] = False     # For B&K DAQ project (give warning)
    d["-c"] = "."       # Separator string
    d["-o"] = False     # Open in IrfanView
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Bbc:ho")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("Bbo"):
            d[o] = not d[o]
        elif o == "-c":
            d["-c"] = a
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args
def Warning():
    C.fg(C.lred)
    print("Warning:  not a VNC screenshot for the B&K DAQ project")
    C.normal()
def GetFilename(args):
    '''Construct the filename from the strings on the command line and
    returns a Pathlib object.
    '''
    if len(args) == 1:
        e = args[0]
        p = pathlib.Path(e)
        ext = p.suffix
        if ext.lower() not in dot_extensions:
            Error(f"'{e}' is not a valid image filename")
        return p
    else:
        e = args[-1]
        remainder = args[:-1]
        ext = e if e[0] == "." else "." + e
        if ext.lower() not in dot_extensions or not remainder:
            Error(f"'{e}' is not an allowed extension")
        return pathlib.Path(d["-c"].join(remainder) + ext)
def GetImage():
    im = ImageGrab.grabclipboard()
    if not isinstance(im, Image.Image):
        Error("No image in clipboard")
    return im
def SaveFile(im, p):
    '''im is Image object.  p is a pathlib.Path object; write the image
    to this file.
    '''
    size = im.size
    print(f"Image size = {size}, mode = {im.mode}")
    if d["-b"] or d["-B"]:
        if size != daq:
            Warning()
            if d["-B"]:
                exit(1)
        # Remove the VNC client banner
        right, lower = size
        left, upper = 0, 134
        new_im = im.crop((left, upper, right, lower))
        im = new_im
        # Resize the image to be the same as the DAS220
        im.resize((1024, 600))
        print(f"  --> Cropped and resized to {im.size} for DAQ project")
    im.save(p)
    print(f"Wrote to {p}")
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    im = GetImage()
    p = GetFilename(args)
    SaveFile(im, p)
    if d["-o"]:
        iv = "c:\\Program Files\\IrfanView\\i_view64.exe"
        subprocess.Popen([iv, str(p)])

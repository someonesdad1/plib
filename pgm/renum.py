'''
Rename picture files
'''
import glob
import string
import sys
import os
import getopt

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def Usage(status=1):
    name = sys.argv[0]
    print('''Usage {name} [options] dir [prefix]
  Rename the JPG files in a directory.
Options
    -p
        Rename the picture files ending with PNG.
'''[:-1].format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-p"] = False
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hp")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-p":
            d["-p"] = True
        if opt[0] == "-h":
            Usage(status=0)
            sys.exit(0)
    if len(args) < 1:
        Usage()
    return args

def ProcessDirectory(dir, new_dir_name, ext):
    print("Processing", dir)
    currdir = os.getcwd()
    os.chdir(dir)
    files = glob.glob("*." + ext)
    numfiles = len(files)
    if numfiles < 10:
        fmt = "%d"
    elif numfiles < 100:
        fmt = "%02d"
    elif numfiles < 1000:
        fmt = "%03d"
    elif numfiles < 10000:
        fmt = "%04d"
    elif numfiles < 100000:
        fmt = "%05d"
    else:
        fmt = "%d"
    num = 1
    for file in files:
        p = os.path.splitext(file)
        name = p[0].lower()
        ex = p[1].lower()
        assert(ex[1:] == ext)
        newname = fmt % num + "." + ext
        while os.path.exists(newname):
            num = num + 1
            newname = fmt % num + "." + ext
        os.rename(file, new_dir_name + newname)
        num = num + 1
    os.chdir(currdir)

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    dir = args[0]
    if len(args) == 2:
        new_dir_name = args[1]
    else:
        new_dir_name = ""
    ext = "jpg"
    if d["-p"]:
        ext = "png"
    if os.path.isdir(dir):
        ProcessDirectory(dir, new_dir_name, ext)
        exit(0)
    else:
        sys.stderr.write("'" + dir + "' not found")
        exit(1)

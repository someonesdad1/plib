'''
Script to describe Mercurial files relative to a particular directory.
Use the -h option for a help message.
 
Note:  My primary use case for this script is to show me the state of
files _in_the_current_directory_.  Mercurial's status command shows
the state of all files in the repository, not just the ones in the
current directory.
'''
 
# Copyright (C) 2011 Don Peterson
# Contact:  gmail.com@someonesdad1
# Updated 28 Jun 2020 to python 3 only and uses pathlib.
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
import os
import pathlib
import sys
import getopt
import functools
import subprocess
import itertools
import collections
import color as c
from pprint import pprint as pp
from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

debug = 0   # Turns on debug printing
nl = "\n"

# Set to the Mercurial command's location
#hg = "d:/bin/TortoiseHg104/hg.exe"
#hg = "/usr/bin/hg"
hg = "/cygdrive/c/bin/mercurial/hg.exe"
# Holds the root directory of the repository
root = None
# Holds the directory of interest
cwd = None
# The directory to print relative to
reldir = os.getcwd()

# Colors for output; colors available are:
#   black   gray
#   blue    lblue
#   green   lgreen
#   cyan    lcyan
#   red     lred
#   magenta lmagenta
#   brown   yellow
#   white   lwhite
(black, blue, green, cyan, red, magenta, brown, white, gray, lblue,
 lgreen, lcyan, lred, lmagenta, yellow, lwhite) = (
    c.black, c.blue, c.green, c.cyan, c.red, c.magenta, c.brown,
    c.white, c.gray, c.lblue, c.lgreen, c.lcyan, c.lred, c.lmagenta,
    c.yellow, c.lwhite)

def StreamOut(stream, *s, **kw):
    k = kw.setdefault
    # Process keyword arguments
    sep = k("sep", "")
    auto_nl = k("auto_nl", True)
    prefix = k("prefix", "")
    convert = k("convert", str)
    # Convert position arguments to strings
    strings = map(convert, s)
    # Dump them to the stream
    stream.write(prefix + sep.join(strings))
    # Add a newline if desired
    if auto_nl:
        stream.write(nl)

out = functools.partial(StreamOut, sys.stdout)
outs = functools.partial(StreamOut, sys.stdout, sep=" ")
dbg = functools.partial(StreamOut, sys.stdout, sep=" ", prefix="+ ")
err = functools.partial(StreamOut, sys.stderr)

def Dbg(msg, no_newline=0):
    if debug:
        err(msg)
        if not no_newline:
            err(nl)

def Error(msg):
    err(msg)
    exit(1)

def Usage(status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] [dir]
  Lists files in . (or dir if given) that are not being tracked by
  Mercurial.  Note this is different than the normal "hg status" command
  in that only files that are in the indicated directory are shown.

  Shows modified and untracked files by default.

Options
    -a  Show all files in a readable format
    -c  Show clean files (tracked files without changes)
    -h  Show this help
    -i  Show ignored files
    -m  Show modified files
    -M  Show missing files
    -r  "recursive"  Show for files at and below the directory
'''[1:-1]
#   Codes for an hg status listing are:
#       M = modified
#       A = added
#       R = removed
#       C = clean
#       ! = missing (deleted by non-Mercurial command, but still tracked)
#       ? = not tracked
#       I = ignored
    out(s.format(**locals()))
    sys.exit(status)

def ParseCommandLine(d):
    d["-a"] = False     # Show all files
    d["-c"] = False     # Show clean files
    d["-i"] = False     # Show ignored files
    d["-m"] = False     # Show modified files
    d["-M"] = False     # Show missing files
    d["-R"] = False     # Recursive at and below the directory
    d["-r"] = False     # Show removed files
    d["dir"] = "."
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "acihmMr")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        sys.exit(1)
    for opt in optlist:
        ltr = opt[0][1]
        if ltr in "acimMRr":
            d[opt[0]] = not d[opt[0]]
        if opt[0] == "-h":
            Usage(0)
    if args:
        if len(args) > 1:
            Usage()
        d["dir"] = args[0]
    d["home"] = os.getcwd()

def GetRoot():
    '''Returns the root directory of the Mercurial repository we're
    currently in.
    '''
    p = subprocess.PIPE
    s = subprocess.Popen((hg, "root"), stdout=p, stderr=p)
    errlines = s.stderr.readlines()
    if errlines:
        # Had an error, so print error message and exit
        err("Error:")
        for i in errlines:
            err("  ", i)
        exit(1)
    lines = [i.strip() for i in s.stdout.readlines()]
    assert len(lines) == 1
    global root
    root = lines[0].decode("UTF8").replace("\\", "/")
    root = pathlib.Path(lines[0].decode("UTF8").replace("\\", "/"))
    # Fix problematical stuff on cygwin under Windows
    s = "C:/cygwin"
    if str(root).startswith(s):
        root = pathlib.Path(str(root)[len(s):])

def IsContained(file):
    '''Return True if file is in a subdirectory of the current directory.
    '''
    if 0:
        cwd = os.getcwd()
        f = os.path.join(root, file)
        loc = f.find(cwd)
        return True if loc == 0 else False
    else:
        p = root/pathlib.Path(file)
        parent = p.parent
        cwd = p.cwd()
        return True if str(parent).startswith(str(cwd)) else False

def GetFiles(d):
    '''Get the full output of an 'hg status -A' command, then filter the
    list by the given options.
    '''
    try:
        # Change to the directory we're interested in
        p = pathlib.Path(d["dir"])
        os.chdir(p)
        global cwd
        cwd = p.cwd()
    except Exception:
        Error("Couldn't cd to '%s'" % d["dir"])
    GetRoot()
    p = subprocess.PIPE
    s = subprocess.Popen((hg, "status", "-A"), stdout=p)
    results = [i.strip() for i in s.stdout.readlines()]
    # results now is a list of bytestrings of the form e.g.
    # b'C software\\ShopCalculator\\water.cpp.orig'.  Convert these to 
    # strings and replace '\' with '/'.
    results = [i.decode("UTF8").replace("\\", "/") for i in results]
    # Make a dictionary containing the relevant files keyed by the
    # Mercurial status codes
    files = collections.defaultdict(list)
    for line in results:
        files[line[0]].append(line[2:])
    # For each key, only keep those directories in the list that are a
    # subdirectory of the current directory.
    for key in files:
        if 1:
            keep = []
            for item in files[key]:
                if IsContained(item):
                    keep.append(item)
            files[key] = keep
        else:
            files[key] = list(filter(IsContained, files[key]))
    return files

def Out(s):
    s = s.replace("\\", "/")
    out(s)

def PrintItems(itemlist, name, d):
    num_lines, e = [0], os.environ
    page = int(e["LINES"]) - 1 if "LINES" in e else 25
    def Page(num_lines):
        num_lines[0] += 1
        if num_lines[0] % page == 0:
            s = raw_input()
            if s in ("q", "Q", "\x1b"):
                exit(0)
    # First, find out if there are any files to be printed in the
    # current directory.
    has_files = False
    for item in itemlist:
        p = os.path.join(root, item)
        try:
            p = os.path.relpath(p, cwd)
        except ValueError:
            continue
        dir, filename = os.path.split(p)
        if not dir:
            has_files = True
            break
    if not has_files:
        return
    out(name)
    #Page(num_lines)
    for item in itemlist:
        p = os.path.join(root, item)
        try:
            p = os.path.relpath(p, cwd)
        except ValueError:
            Out("  nul " + "<" + "-"*20)
            #Page(num_lines)
            continue
        if d["-R"]:
            Out("  " + p)
            #Page(num_lines)
        else:
            # Only print this file if it's in the current directory
            dir, filename = os.path.split(p)
            if not dir:
                Out("  " + p)
                #Page(num_lines)

def PrintResults(files, d):
    '''files is a dictionary keyed by Mercurial status letter.  d is the
    options dictionary.
    '''
    assert len(files) > 0
    normal = (white, black)
    names = {
        "A": ("Added files:",     (lgreen, black)),
        "C": ("Clean files:",     (white, black)),
        "I": ("Ignored files:",   (cyan, black)),
        "M": ("Modified files:",  (yellow, black)),
        "R": ("Removed files:",   (lwhite, red)),
        "!": ("Missing files:",   (lmagenta, black)),
        "?": ("Untracked files:", (lred, black)),
    }
    for key in "ICRAM!?":
        color = names[key][1]
        c.fg(color)
        if key in files and files[key]:
            PrintItems(files[key], names[key][0], d)
        c.fg(normal)
    c.fg(normal)

if __name__ == "__main__":
    d = {}  # Options dictionary
    ParseCommandLine(d)
    files = GetFiles(d)
    if not files:
        out("No Mercurial files found in %s" % d["dir"])
        exit(0)
    # Winnow out the files we don't want
    keep = {}
    if d["-a"]:
        # Print all
        keep = files
    elif d["-c"]:
        # Print clean files
        keep["C"] = files["C"]
    elif d["-i"]:
        # Print ignored files
        keep["I"] = files["I"]
    elif d["-m"]:
        # Print modified files
        keep["M"] = files["M"]
    elif d["-M"]:
        # Print missing files
        keep["!"] = files["!"]
    elif d["-r"]:
        # Print removed files
        keep["R"] = files["R"]
    else:
        keep["!"] = files["!"]  # Missing
        keep["A"] = files["A"]  # Added
        keep["?"] = files["?"]  # Untracked
        keep["M"] = files["M"]  # Modified
        keep["R"] = files["R"]  # Removed
    PrintResults(keep, d)

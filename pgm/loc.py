'''
This script indexes my hard disk directories and stores the output
in an index file.  A regex on the command line can be searched for and
the matches will be highlighted in color.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2016, 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Locate files on hard disk using an index
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import pathlib
    import re
    import subprocess
    import sys
    import time
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import color as C
    from get import GetLines
    from columnize import Columnize
class FileInfo:
    def __init__(s, file):
        s.file = file
        s.abs = pathlib.Path(file).resolve()
        st = os.stat(file)
        s.perm = oct(st.st_mode & 0o777)
        s.inode = hex(st.st_ino)
        s.dev = hex(st.st_dev)
        s.nlinks = st.st_nlink
        s.uid = st.st_uid
        s.gid = st.st_gid
        s.size = st.st_size
        s._atime = st.st_atime
        s._mtime = st.st_mtime
        s._ctime = st.st_ctime
        s.atime = s.Tm(st.st_atime)
        s.mtime = s.Tm(st.st_mtime)
        s.ctime = s.Tm(st.st_ctime)
    def Tm(self, x):
        s = "%Y%b%d:%H%M%S"     # 2018Jul27:153416
        s = "%d%b%Y-%H:%M:%S"   # 27Jul2018-15:34:16
        return time.strftime(s, time.localtime(x))
    def __str__(s):
        return f"FileInfo({s.file})"
    def __repr__(s):
        return f"FileInfo({s.abs}, {s.perm}, {s.size}B, {s.mtime})"
def GetFileInfo(file):
    '''file can either be a string or a sequence and this function will
    return either a single FileInfo object or a list of them for the
    corresponding files.
    '''
    f = FileInfo
    return f(file) if isinstance(file, str) else [f(i) for i in file]
def Now():
    'Convenience function to return time.time().'
    return time.time()
def Error(msg, status=1, file=sys.stderr):
    print(msg, file=file)
    exit(status)
def CheckSettings(d):
    '''Check the settings for consistency.
    '''
    if d["-d"] and d["-f"]:
        Error("Can't use -d with -f")
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] regex1 [regex2...]
      Locate my files or directories that match regular expressions.  For
      system files, use the 'locate' command (update locate's data with
      'updatedb').  Main directory trees searched are:'''))
    for i in Columnize(d["directories_to_search"], indent=" "*5):
        print(i)
    print(dedent(f'''
      Note the output has '//' between the file's directory and its file
      name; directories end with '//'.
    Options
      -c      Don't use color in output.  Note color escape sequences won't
              be present if output isn't to a terminal.
      -d      Only show directories
      -f      Only show files
      -I      Construct the index
      -i      Don't ignore case
      -p      Ignore picture, sound, & video files
      -r      Include source code repositories (.hg .git .bzr)
      -s      Use a pure python search.  This is about 10 times slower, but
              -d and -f work as expected and -X works.  For speed, egrep is
              used to find the patterns if you don't use -s and it should be
              reasonable for most uses.
      -X re   Ignore directory names that match re regex (more than one -X OK)
      -x re   Ignore file names that match re regex (more than one -x OK)
      -v      Show index file's data
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = False     # Don't use color in output
    d["-d"] = False     # Only show directories
    d["-f"] = False     # Only show files
    d["-I"] = False     # Index the hard disk
    d["-i"] = False     # Don't ignore case
    d["-p"] = True      # Show picture, sound, video files
    d["-r"] = False     # Include source code repositories
    d["-s"] = False     # Use pure python search (good but 10 times slower)
    d["-v"] = False     # Show index file data
    d["-X"] = []        # Directories to ignore (list of regexs)
    d["-x"] = []        # File names to ignore (list of regexs)
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, regexs = getopt.getopt(sys.argv[1:], "cdfIiprsvX:x:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    bools = ["-" + i for i in list("cdfIiprsv")]
    for o, a in opts:
        if o in bools:
            d[o] = not d[o]
        elif o in ("-X",):
            d[o].append(a)
        elif o in ("-x",):
            d[o].append(a)
    if d["-v"]:
        ShowIndexFileData(d)
    CheckSettings(d)
    if not regexs and not d["-I"]:
        Usage(d)
    d["regexs"] = regexs
def GetFilesAndDirectories(dir):
    '''Return two sets containing the file names and directory that are
    under the indicated directory.
    '''
    J = lambda root, name:  os.path.join(root, name)
    Dirs, Files = set(), set()
    for root, dirs, files in os.walk(dir):
        f = [J(root, i) for i in files]
        Files.update(f)
        d = [J(root, i) for i in dirs]
        Dirs.update(d)
    return Dirs, Files
def GenerateIndex(opts):
    '''Create the index file.
    '''
    s = sys.stdout if opts["-I"] else sys.stderr
    print("Updating the index file", file=s) 
    datafile = opts["datafile"]
    # Main sets of files & directories
    Dirs, Files = set(), set()
    start = time.time()
    for dir in opts["directories_to_search"]:
        d, f = GetFilesAndDirectories(dir)
        Dirs.update(d)
        Files.update(f)
    # Write directories
    stream = open(datafile, "w")
    stream.write("\n".join(sorted([i + "//" for i in list(Dirs)])))
    stream.write("\n")
    # Write files.  Note the file's name is separated from the directory
    # path by '//' to facilitate parsing.
    f = []
    for file in Files:
        t = file.split("/")
        f.append('/'.join(t[:-1]) + "//" + t[-1])
    stream = open(datafile, "a")
    stream.write("\n".join(sorted(f)))
    stream.write("\n")
    et = time.time() - start
    print(f"   {len(Dirs)} directories, {len(Files)} files (took {et:.1f} s)", file=s)
def IndexFileStale(d):
    '''Returns True if the index file is too much out of date.
    '''
    f = GetFileInfo(d["datafile"])
    days_elapsed = abs(Now() - f._mtime)/(24*3600)
    return days_elapsed > d["stale_days"]
def ShowIndexFileTime(d):
    f, s = GetFileInfo(d["datafile"]), sys.stderr
    print(f"Index file = {f.abs} [{f.mtime}]", file=s)
def MakeSuffixes(d):
    'Construct list of suffixes for -p option'
    s = d["suffixes"] = set()
    pictures = ["." + i for i in '''
        bmp clp dib emf eps gif img jpeg jpg pbm pcx pgm png ppm ps psd
        psp pspimage raw tga tif tiff wmf xbm xpm
        '''.split()]
    s.update(pictures)
    # Video list from https://en.wikipedia.org/wiki/Video_file_format
    video = ["." + i for i in '''
        3g2 3gp amv avi f4a f4b f4p f4v flv m2v m4p m4v mkv mov mp2 mp4
        mpe mpeg mpg mpv ogg ogv qt rm rmvb svi vob webm wmv
        '''.split()]
    s.update(video)
    # Audio list from https://en.wikipedia.org/wiki/Audio_file_format
    audio = ["." + i for i in '''
        3gp 8svx aa aac aax act aiff alac amr ape au awb cda dct dss dvf
        flac gsm m4a m4b m4p mmf mogg mp3 mpc msv nmf nsf oga ogg opus
        ra raw rf64 rm sln tta voc vox wav webm wma wv
        '''.split()]
    s.update(audio)
def PerformSearch(d):
    '''Construct a grep pipeline to perform the search.  This is fast,
    but it's not as specific as the pure python solution.
  
    Bug:  If you invoke with '-f calipers', you'll still see files in 
    a directory named calipers because the grep is for an ending '//'.
    To better address this, the set of lines could be processed first to
    break the filenames into (dir, name) and do the search only on name.
    It would probably make most sense to do this with e.g. a new -F
    option.
    '''
    g = "/bin/egrep "
    grep = g if d["-c"] else g + "--color=auto "
    regexs = d["regexs"]
    # Construct a suitable pipeline to get the desired subset of lines
    file = d["datafile"]
    pipeline = ["/bin/cat {}".format(file)]
    if d["-d"]:         # Directories only
        pipeline.append(grep + "//$")
    elif d["-f"]:       # Files only
        pipeline.append(grep + "-v //$")
    if not d["-p"]:         # Don't ignore pictures, sound, video
        s = ["-e '\\" + i + "$'" for i in d["suffixes"]]
        pipeline.append(grep + "-v " + ' '.join(s))
    if not d["-r"]:     # Include repositories
        pipeline.append(grep + "-v -e '/.bzr/' -e '/.git/' -e '/.hg/'")
    if d["-x"]:         # Regexps to ignore
        s = []
        for regex in d["-x"]:
            s.append("-e '{}' ".format(regex))
        pipeline.append(grep + "-v " + ' '.join(s))
    ic = " " if d["-i"] else "-i "      # Whether to ignore case
    s = [grep + ic]
    for regex in d["regexs"]:
        s.append("-e '{}' ".format(regex))
    pipeline.append(' '.join(s))
    cmd = ' | '.join(pipeline)
    if 0:
        print("Command pipeline:")
        for i in pipeline:
            print(i)
        exit()
    subprocess.call(cmd, shell=True)
def PerformSearchPurePython(d):
    '''Read the datafile in and do the search.  This is a pure python
    solution without using grep.
    '''
    S = C.Style(C.lred, C.black)
    def SearchDirs(dirs, r):
        for dir in dirs:
            s = dir.replace("//", "")
            mo = r.search(s)
            if mo:
                C.PrintMatch(s, r, style=S)
    # Read in the directories and files.  Note the files' names are
    # split on '//' so that the files list contains elements of 
    # the form [/aaa/bbb, ccc.ddd].
    dirs, files = [], []
    for line in GetLines(d["datafile"]):
        if line.endswith("//"):
            dirs.append(line)
        else:
            if line.strip():
                dir, name = line.split("//")
                files.append([dir, name])
    if not d["-r"]:
        # Get rid of git/Mercurial/Bazaar repository components
        for i in reversed(range(len(dirs))):
            s = dirs[i].split("/")
            if ".git" in s or ".hg" in s or ".bzr" in s:
                del dirs[i]
        for i in reversed(range(len(files))):
            if not files[i]:
                del files[i]
                continue
            dir, name = files[i]
            s = dir.split("/")
            if ".git" in s or ".hg" in s or ".bzr" in s:
                del files[i]
    if d["-X"]:
        # Remove regexs from directory parts
        for regex in d["-X"]:
            r = re.compile(regex) if d["-i"] else re.compile(regex, re.I)
            for i in reversed(range(len(dirs))):
                s = dirs[i]
                mo = r.search(s)
                if mo:
                    del dirs[i]
            for i in reversed(range(len(files))):
                dir, name = files[i]
                mo = r.search(dir)
                if mo:
                    del files[i]
    if d["-x"]:
        # Remove regexs from file parts
        for regex in d["-X"]:
            r = re.compile(regex) if d["-i"] else re.compile(regex, re.I)
            for i in reversed(range(len(files))):
                dir, name = files[i]
                mo = r.search(name)
                if mo:
                    del files[i]
    if d["-p"]:
        # Remove picture, sound, video files
        for i in reversed(range(len(files))):
            dir, name = files[i]
            p = pathlib.PurePath(name)
            for suffix in d["suffixes"]:
                if suffix == p.suffix:
                    del files[i]
                    break
    # Apply each of the regexs on the command line
    for regex in d["regexs"]:
        r = re.compile(regex) if d["-i"] else re.compile(regex, re.I)
        if d["-d"]:
            SearchDirs(dirs, r)
        elif d["-f"]:
            for dir, file in files:
                mo = r.search(file)
                if mo:
                    print(dir, end="")
                    C.PrintMatch(file, r, style=S)
        else:
            SearchDirs(dirs, r)
            for dir, file in files:
                s = dir + "//" + file
                mo = r.search(s)
                if mo:
                    C.PrintMatch(s, r, style=S)
def ShowIndexFileData(d):
    df = d["datafile"]
    lc = len(open(df).readlines())
    p = pathlib.Path(df)
    st = p.stat()
    print(f"Datafile stats ({df}):")
    print(f"  Number of files indexed   {lc}")
    print(f"  Number of Mbytes          {round(st.st_size/1e6, 2)}")
    struct_time = time.localtime(st.st_mtime)
    h = time.strftime("%I", struct_time)
    ms = time.strftime("%M:%S %p", struct_time).lower()
    t = time.strftime("%d%b%Y-", struct_time)
    h = h[1:] if h[0] == "0" else h
    modtime = f"{t}{h}:{ms}"
    now = time.time()
    days = (now - st.st_mtime)/(24*3600)
    print(f"  Last indexing time        {modtime} ({round(days, 1)} days ago)")
    exit(0)
if __name__ == "__main__":
    grep = "egrep --color=auto "
    d = {       # Options dictionary
        "directories_to_search": [
            "/d",
            "/doc",
            "/ebooks",
            "/elec",
            "/help",
            "/home/Don",
            "/math",
            "/pylib",
            "/science",
            "/shop",
            "/tools",
            ],
        "datafile": "/home/donp/bin/data/loc.main",
        "stale_days": 3,
    }
    if 1:
        # Include files on d:/
        d["directories_to_search"].extend([
            "/cygdrive/d/d",
            "/cygdrive/d/Don_old",
            "/cygdrive/d/movies",
            "/cygdrive/d/pictures",
            "/cygdrive/d/uecide-0.11.0-beta-3",
        ])
    MakeSuffixes(d)
    ParseCommandLine(d)
    ShowIndexFileTime(d)
    if IndexFileStale(d):
        print("** Index file is out of date **")
    if d["-I"]:
        GenerateIndex(d)
        exit(0)
    if d["-s"]:
        PerformSearchPurePython(d)
    else:
        PerformSearch(d)

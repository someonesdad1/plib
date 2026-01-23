'''

∞∞2
    - Eliminate use of os stuff; rewrite using pathlib
    - Eliminate -b option.  Calculate hash from 4096 bytes and if they are the same,
      calculate for whole file (first compare size, as that's the fastest).

Finds duplicate files in directory trees
    The algorithm used is to walk the directory tree(s) using os.walk().
    The files found then have their (hash, size) saved in a dictionary
    whose elements are lists.  The default hash size is 4 kbytes, which
    is a typical block size for a filesystem.  Files that have the same
    dictionary (hash, size) keys are likely to be identical files and
    are so reported.  Use the '-b 0' option to calculate the hash for
    all the bytes in the file to be more sure of identity -- the
    tradeoff is that this can increase the time the program runs by
    about an order of magnitude.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Find duplicate files in directory trees
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from pathlib import Path as P
        import sys
        import os
        import getopt
        import hashlib
        import stat
        import re
        from collections import defaultdict
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
        from dpseq import DupNodupHashable
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        # Hashing method to use on files
        hash = hashlib.sha1
if 1:  # Classes
    class IgnoreThisFile(Exception):
        pass
if 1:  # Utility
    def GetColors():
        t.file = t.yel
        t.dup = t.sky
        t.inode = t.ornl
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=1):
        name = sys.argv[0]
        dashb = d["-b"]
        print(
            dedent(f'''
        Usage:  {name} dir1 [dir2...]
          Display duplicate files in directories.  In the output, 1: means
          dir1, 2: means dir2, etc.  Hard links are reported (turn off with
          -L); use -l to have soft links reported also.
        
          For speed, only the first {dashb} bytes of a file are read to
          calculate the hash.  Thus, two files that are reported to be the
          same are probably the same, but it's not guaranteed.  Use '-b 0' to
          hash all of the files' bytes (takes longer to process).
        Options
          -b s    Read s bytes to compute hash.  0 = compare all bytes
          -d      Debug output 
          -F      Same as -f, but print full path to file
          -f      Find duplicate file names (implies -r)
          -g      Include git directories in the search
          -h      Include hidden directories (implies -g and -m)
          -L      Don't report hard links
          -l      Follow symbolic links
          -m      Include Mercurial directories
          -r      Act recursively
          -t n    Ignore files <= n bytes (OK to append k, M, G, T)
          -x re   Ignore specified file regexp.  Can have multiple -x's.
          -X re   Ignore specified directory regexp.  Can have multiple -X's.
          -z      Do not ignore zero-length files
        ''')
        )
        exit(status)
    def ParseCommandLine():
        d["-b"] = 4096   # Bytes to read to compute hash
        d["-c"] = True   # Use color if True
        d["-d"] = False  # Show debug information
        d["-F"] = False  # Find duplicate file names, print full path
        d["-f"] = False  # Find duplicate file names
        d["-g"] = False  # Do not ignore git directories
        d["-h"] = False  # Do not ignore hidden directories
        d["-L"] = False  # Do not report hard links
        d["-l"] = False  # Dereference symbolic links
        d["-m"] = False  # Do not ignore Mercurial directories
        d["-r"] = False  # Enable recursion
        d["-t"] = -1     # Threshold for size, in bytes
        d["-x"] = []     # File regexps to ignore
        d["-X"] = []     # Directory regexps to ignore
        d["-z"] = False  # Do not ignore zero-length files
        if 1:   # Ignore some common files I use
            d["-x"].append(re.compile(r"^\.vi$|^\.z$|^\.todo$|^z$|^a$|^b$"))
        if 1:   # Ignore some common directories
            d["-X"].append(re.compile(r"\.ruff_cache"))
            d["-X"].append(re.compile(r"\.cache"))
            d["-X"].append(re.compile(r"\.gnupg"))
            d["-X"].append(re.compile(r"\.local"))
            d["-X"].append(re.compile(r"\.ssh"))
            d["-X"].append(re.compile(r"\.vimfiles"))
        try:
            optlist, dirs = getopt.getopt(sys.argv[1:], "b:cdFfghLlmrt:x:X:z")
        except getopt.GetoptError as str:
            msg, option = str
            sys.stderr.write(msg + nl)
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "cdFfgLlmrz":
                d[o] = not d[o]
            elif o == "-b":
                try:
                    d[o] = int(a)
                except Exception:
                    Error(f"{a!r} is a bad integer for {o} option")
                if d[o] < 0:
                    Error(f"{o} option's argument must be >= 0")
            elif o == "-h":
                d["-h"] = d["-g"] = d["-m"] = True
            elif o == "-t":
                d["-t"] = GetSize(opt[1])
            elif o == "-x":
                try:
                    d["-x"].add(re.compile(opt[1]))
                except Exception:
                    Error("'%s' is a bad regular expression" % opt[1])
            elif o == "-X":
                try:
                    d["-X"].add(re.compile(opt[1]))
                except Exception:
                    Error("'%s' is a bad regular expression" % opt[1])
        if d["-d"]:
            g.dbg = True
        if d["-f"] or d["-F"]:
            d["-r"] = True
        GetColors()
        if not dirs:
            Usage(1)
        if d["-d"]:
            Dbg("Options set from command line:")
            for k in d.keys():
                Dbg(f"  {k:4s} {d[k]}")
        return dirs
if 1:  # Core functionality
    def GetSize(s):
        '''Return the size in bytes from the string s.  Note s can have k,
        M, G, or T appended (interpret as decimal SI prefixes).
        '''
        msg = f"{s!r} is a bad threshold specification"
        si = {"k": 3, "M": 6, "G": 9, "T": 12}
        s, factor = s.replace(" ", ""), 1
        if s[-1] in si:
            factor = int(10**si[s[-1]])
            s = s[:-1]
        try:
            i = float(s)
        except Exception:
            Error(msg)
        return int(factor*i)
    def ProcessDir(dirnum, dir):
        '''Return a dictionary containing the information on the files in
        the directory dir.  dirnum is an integer indicating the order on
        the command line.  dir is a single directory as a Pathlib.  
        
        The returned dictionary has the form (s=string, i=integer, b=bool):
        {
            (hash1, size1) : [
                (filename(s), inode(i), dirnum(i), islink(b)),
                ...
            ],
            (hash2, size2) : [
                (filename(s), inode(i), dirnum(i), islink(b)),
                ...
            ],
            ...
        }
        '''
        if not dir.exists():
            print(f"{t.redl}Directory {str(dir)!r} doesn't exist", file=sys.stderr)
            return
        # Get a list of all the files
        files = []
        pattern = "**/*" if d["-r"] else "*"
        for file in dir.glob(pattern):
            if file.is_dir():
                continue
            dir_fields = file.parts[:-1]  # :-1 gets rid of the file name
            if any(".ruff_cache" in i for i in dir_fields):
                continue
            try:
                for regex in d["-X"]:
                    for field in dir_fields:
                        if regex.search(field):
                            raise IgnoreThisFile()
            except IgnoreThisFile:
                Dbg("Ignoring file because it has an ignored directory (-X):  ", file)
                continue
            dir_fields = set(dir_fields)
            if 1:   # Check for directories that we'll ignore by default
                if ".hg" in dir_fields and not d["-m"]:
                    Dbg("Ignoring Mercurial directory:  ", file)
                    continue  # Ignore Mercurial directories
                if ".git" in dir_fields and not d["-g"]:
                    Dbg("Ignoring git directory:  ", file)
                    continue  # Ignore Mercurial directories
                def dotted(x):
                    x.startswith(".") and x != "."
                if any([dotted(i) for i in dir_fields]) and not d["-h"]:
                    Dbg("Ignoring hidden directory:  ", file)
                    continue  # Ignore hidden directories
            if 1:   # Check if it's a soft link
                if file.is_symlink() and not d["-l"]:
                    Dbg("Ignoring soft link:  ", file)
                    continue
            if 1:   # Check for d["-x"] matching
                found = False
                for regex in d["-x"]:
                    if regex.search(file.name):
                        found = True
                        break
                if not found:
                    files.append(file)
                else:
                    Dbg("Ignoring file (-x):  ", str(file))
        if d["-f"]:     # Look for duplicate names
            filedict = defaultdict(list)
            for file in files:
                filedict[file.name] += [file.parent]
            return filedict
        else:
            # Create a dictionary with the file's (hashlib.sha1 value, size) as the key.
            # The values are (filename, inode_number, dirnum, is_softlink).
            hashdict = defaultdict(list)
            count = 0
            for file in files:
                count += 1
                m = hashlib.sha1()
                try:
                    if d["-b"]:
                        m.update(open(file, "rb").read(d["-b"]))
                    else:
                        m.update(open(file, "rb").read())
                except IOError:
                    # Either the file isn't readable or it's an orphaned soft link
                    t.print(f"{t.redl}Couldn't open '%s'" % file, file=sys.stderr)
                    continue
                st = file.stat() if d["-l"] else file.lstat()
                size = st[stat.ST_SIZE]
                digest = m.hexdigest()
                inode = st[stat.ST_INO]
                is_softlink = file.is_symlink()
                key = (digest, size)
                value = (file, inode, dirnum, is_softlink)
                if 0:
                    Dbg(key, value)
                if not size:
                    # Zero-length file
                    if d["-z"] and size > d["-t"]:
                        hashdict[key].append(value)
                    else:
                        Dbg("Ignoring zero-length file:  ", file)
                else:
                    if size > d["-t"]:  # Greater than size threshold
                        hashdict[key].append(value)
                    else:
                        Dbg("Ignoring file below size threshold:  ", file)
            return hashdict
    def GetColor(size):
        '''Return a color indicating file size.'''
        if size < 10**5:
            return t.wht
        elif size < 10**6:
            return t.yell
        else:
            return t.redl
    def PrintSize(size, stream):
        t.print(f"{GetColor(size)}{size}", file=stream, end="")
    def ReportDuplicate(item, stream):
        '''item is a list of tuples (length > 1) that contain duplicated
        information.  Print this information.
            item = [
                (filename, lstat_info, dirnumber, islink),
                ...
            ]
        Note the lstat() info is stat() instead if the -l option is used
        because -l means to follow symbolic links.
        '''
        if not d["-L"]:
            # Get a list of hard links (soft links also look like hard
            # links if the -l option was used).
            links = defaultdict(list)
            for filename, inode, dirnumber, islink in item:
                links[inode].append((filename, dirnumber, islink))
            for inode in links:
                if len(links[inode]) > 1:
                    size = os.stat(links[inode][0][0]).st_size
                    if d["-l"]:
                        print(f"{t.yell}Hard-linked{t.n} [{t.inode}inode{t.n}] or soft-linked "
                              f"<{t.inode}inode{t.n}> files (-l option used) (", file=stream, end="")
                    else:
                        print(f"{t.yell}Hard-linked files{t.n} [{t.inode}inode number{t.n}] (",
                              file=stream, end="")
                    PrintSize(size, stream)
                    print(" bytes):")
                    for filename, dirnumber, islink in links[inode]:
                        li = (dirnumber, inode, filename)
                        if islink:
                            print(f"  %d:<{t.inode}%d{t.n}>:  %s" % li, file=stream)
                        else:
                            print(f"  %d:[{t.inode}%d{t.n}]:  %s" % li, file=stream)
        # Print out the true duplicates
        size = os.stat(item[0][0]).st_size
        print(f"{t.dup}Duplicate files ", file=stream, end="")
        t.print("(", file=stream, end="")
        # Set color of size number based on size
        PrintSize(size, stream)
        print(" bytes):", file=stream)
        for filename, lstat_info, dirnumber, islink in item:
            print("  %d:  %s" % (dirnumber, filename), file=stream)
        if 0:   # Blank line to separate duplicate information
            print("", file=stream)
    def ReportDuplicates(stream=sys.stdout):
        '''g.fileinfo is a dictionary with keys (hashlib.sha1 value, size) and values
        that are a list of tuples(filename, lstat_info, dirnumber).  d is the options
        dictionary.  stream is where to print the results.
        
        If a value list contains more than one tuple, this is duplicated
        information.  It can be due to either a copy of a file or a hard
        link.
        '''
        for i in g.fileinfo:
            if len(g.fileinfo[i]) > 1:
                ReportDuplicate(g.fileinfo[i], stream)
    def ReportDuplicateFilenames(stream=sys.stdout):
        duplicates = []
        for key, value in g.fileinfo.items():
            if len(value) > 1:
                duplicates.append((key, value))
        duplicates.sort()
        for name, files in duplicates:
            if d["-F"]:
                for i in files:
                    print(f"{t.file}{i.absolute()}", file=stream)
            else:
                t.print(f"{t.file}{name!r}{t.dup} is duplicated in directories:", file=stream)
                for i in files:
                    print(f"    {i if i else '.'}", file=stream)

if __name__ == "__main__":
    d = {}  # Options dictionary
    dirs = ParseCommandLine()
    # Remove any duplicates in dirs
    dup, nodup = DupNodupHashable(dirs)
    g.fileinfo = defaultdict(list)
    for dirnum, dir in enumerate(nodup):
        di = ProcessDir(dirnum + 1, P(dir))
        if di:
            for key, value in di.items():
                g.fileinfo[key] += value
    if d["-f"]:
        ReportDuplicateFilenames()
    else:
        ReportDuplicates()

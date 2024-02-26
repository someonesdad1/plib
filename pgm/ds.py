'''

ToDo
    - Store the datafiles in the directories they index.  
        - What is benefit of pickling?  The basic datastructure is a set of file names.
    - My storage directories like /ebooks are bloated.  To keep things but allow me to see fewer
      selections, change this program so that older stuff can be moved to a directory named 'old'.
      Then this script will not enter and index such a directory.
    - Change default behavior
        - Command line becomes 're1 re1 ...'
            - This means find documents with re1, then refine the set by
              including only those with re2
            - To get current behavior, use 're1 | re2'
            - You can use either one such string or 
            - You'll have to escape '|' from the shell
    - Get help with -h
    - If no args on command line, prompt the user

Open a document file
    File is opened if it's the only match to the regexp on the command
    line.  Otherwise print out the matches.  Example:
 
        ds 3456
 
    will prompt you for manuals/datasheets/catalogs that contain the
    string 3456.

    Current --exec options support datasheets (ds), ebooks (eb), and HP
    Journal articles (hpj).  For the HP Journal stuff, use the -j
    option.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Datasheet utility to open a document file
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import glob
        import os
        import pathlib
        import pickle
        import re
        import subprocess
        import sys
        from time import time
        from itertools import filterfalse
        from os.path import join, isfile, split
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from selection import Select
        from dirfiles import Dirfiles
        from wsl import wsl
        from timer import GetET
        from f import flt
        from color import t
    if 1:   # Global variables
        class G: # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        # If the following is True, pickle the datafiles.  Comment:  the datafiles are a set of
        # file names, so in reality the easiest way to store the data is as a list of files, one
        # file per line.  This lets the thing be edited if needed.
        g.pickle = False
        # app to open a file with registered application
        if wsl:
            g.app = "explorer.exe"          # Linux under WSL
        else:                               # Windows
            g.app = "d:/cygwin64/bin/cygstart.exe" 
        # Index files hold the files to be searched.  These are stored in files
        # because caching on my system doesn't work well for the d:/ drive.  Indexing performs well
        # in cygwin, but is 5-10 times slower under WSL when indexing the Windows file system.
        # The index files used to be stored in /plib/pgm, but 26 Feb 2024 I decided to store them 
        # in the directories themselves.  I also removed the BK stuff.
        g.index_files = {
            #"bk": "/plib/pgm/ds.bk.index", 
            "ds": "/manuals/ds.ds.index", 
            "eb": "/ebooks/ds.eb.index", 
            "hpj": "/ebooks/hpj/ds.hpj.index", 
        }
        # Colors for output
        t.dir = t("sky")        # Contrast for directory portion
        t.match = t("ornl")     # Color for matches
if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stderr   # Debug printing to stderr by default
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        name = d["--exec"]
        print(dedent(f'''
        Usage:  {name} [options] regexp [re1 re2...]
          Open a document if it's the only match to the regexp.  Otherwise print
          out the matches and choose which ones to display.  When choosing, you
          can select multiple numbers by separating them with spaces or commas.
          Ranges like 5-8 are recognized.
    
          If re2 etc. are present, they are other regexps to additionally
          search for in the results; they are ORed together.
        Options
          -I    Generate the index
          -i    Make the search case sensitive
          -j    Search HP Journal and Bench Brief files (note:  consider
                using the hpj.py script for such searches)
          -x    Generate the index (print debug info)
        Long options
          --exec n
            Name of index file for usage statement.  Choices are:
              {' '.join(g.index_files.keys())}
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-I"] = d["-x"] = False     # If True, then generate indexes
        d["-i"] = False     # If True, then case-sensitive search
        d["-j"] = False     # Show HPJ matches
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "hIijx", ["exec="])
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in list("Iijx"):
                d[o] = not d[o]
            elif o == "--exec":
                d["--exec"] = a
                if a not in g.index_files:
                    Error("'{a}' not an index")
            elif o == "-h":
                Usage(d, 0)
        if d["-I"] or d["-x"]:
            if d["-x"]:
                g.dbg = True
            GenerateIndexFiles(d)
        if d["-j"]:
            d["--exec"] = "hpj"
        if not args:
            Usage(d)
        return args
if 1:   # Core functionality
    def GenerateIndexFiles(d):
        'Generate all of the index files at once'
        # On 26 Feb 2024, I decided to 1) stop using pickling and just store the filenames in the
        # index files and 2) store the files in the same directory where they were indexed, as this
        # keeps the index files accessible to both cygwin and WSL as they're not in a git
        # repository that can be out of sync.
        name_ignore = set('''
            .vi .gitignore .z z tags a b aa bb
        '''.split())
        suffix_ignore = set('''
            .zip .bak
        '''.split())
        def DumpIndexFile(name, df):
            if g.pickle:
                with open(name, "wb") as fp:
                    pickle.dump(df.files, fp)
            else:
                with open(name, "w") as fp:
                    for i in sorted(df.files):
                        if i.name in name_ignore or i.suffix in suffix_ignore:
                            continue
                        s = str(i)
                        # WSL puts on an unneeded mount point which will foul up cygwin
                        if s.startswith("/mnt/d"):
                            s = s.replace("/mnt/d", 1)
                        fp.write(f"{s}\n")
        et = flt(0)
        if 0:   # B&K
            Dbg("Indexing B&K:", end="  ")
            start = flt(time())
            df = Dirfiles("/manuals/manuals/bk", clear=True)
            df.add("**/*")
            if 1:
                # Filter out stuff not wanted
                pass
            tm = time() - start
            et += tm
            Dbg(f"{len(df.files)} files ({tm} s)")
            DumpIndexFile(g.index_files["bk"], df)
        if 1:   # ebooks
            Dbg("Indexing ebooks:", end="  ")
            start = flt(time())
            df = Dirfiles("/ebooks", clear=True)
            df.add("**/*")
            if 1:
                # Filter out stuff not wanted
                df.rm("kindle")
                df.rm("hpj")
                df.rm("wxPython")
                df.rm("prog/scipy/scipy-html")
            tm = time() - start
            et += tm
            Dbg(f"{len(df.files)} files ({tm} s)")
            DumpIndexFile(g.index_files["eb"], df)
        if 1:   # Datasheets
            Dbg("Indexing manuals & datasheets:", end="  ")
            start = flt(time())
            df = Dirfiles("/manuals", clear=True)
            df.add("**/*")
            if 1:
                # Filter out stuff not wanted
                pass
            tm = time() - start
            et += tm
            Dbg(f"{len(df.files)} files ({tm} s)")
            DumpIndexFile(g.index_files["ds"], df)
        if 1:   # HP Journal
            Dbg(f"Indexing HPJ", end="  ")
            start = flt(time())
            if wsl:
                df = Dirfiles("/mnt/d/ebooks/hpj", clear=True)
            else:
                df = Dirfiles("/cygdrive/d/ebooks/hpj", clear=True)
            df.add("**/*")
            tm = time() - start
            et += tm
            Dbg(f"{len(df.files)} files ({tm} s)")
            DumpIndexFile(g.index_files["hpj"], df)
        print(f"Indexing time = {GetET(et)}")
        exit(0)
    def GetChoices(matches):
        '''Return a set of integers representing the user's choices.
        '''
        while True:
            answer = input("? ").strip()
            if not answer or answer == "q":
                exit(0)
            n = len(matches) + 1
            found, not_found = Select(answer, range(1, n + 1))
            if found:
                break
        if not_found:
            s = ' '.join([str(i) for i in not_found])
            print(f"Selections not found:  {s}")
        return found
    def OpenFile(app, matches, choice):
        'Open indicated choice (subtract 1 first)'
        file = matches[choice - 1][0]
        if wsl:
            if 0:
                # Use wslpath.exe to convert the file name to a Windows path
                cmd = ["/usr/bin/wslpath", "-w", file]
                r = subprocess.run(cmd, capture_output=True)
                file = r.stdout.decode()
            else:
                # Use the ~/.0rc/bin/expl script to open a file with Explorer.  This script first
                # cd's to the file's directory, as otherwise Explorer doesn't work.  
                r = subprocess.run(f"/home/don/.0rc/bin/expl {file}", shell=True)
        else:
            if 0:
                # Old method on older Linux
                # Send stderr to /dev/null because some apps on Linux have annoying
                # bug messages sent to the console.
                subprocess.Popen([app, matches[choice - 1][0]],
                                stderr=subprocess.DEVNULL)
            else:
                subprocess.run([app, file])
    def PrintMatch(num, path, start, end, d):
        '''For the match in path, print things out in the appropriate colors.
        Note start and end are the indices into just the file part of the
        whole path name.
        '''
        print("%3d  " % num, end="")
        s = str(path)
        dir, file = split(s[len(d["root"]) + 1:])  # Gets rid of leading stuff
        dir += "/"
        print(f"{t.dir}{dir}{t.n}", end="")
        print(file[:start], end="")
        print(f"{t.match}{file[start:end]}{t.n}{file[end:]}")
    def PrintChoices(matches, d):
        print("Choose which file(s) to open:")
        for num, data in enumerate(matches):
            file, mo = data
            PrintMatch(num + 1, file, mo.start(), mo.end(), d)
    def GetMatches(regexp, d, regexps):
        '''regexp is the first regex on the command line.  d is the options
        dict and regexps are any other regexes give on the command line.
        '''
        r = re.compile(regexp) if d["-i"] else re.compile(regexp, re.I)
        matches = []
        for i in d["files"]:
            # Only search for match in file name
            dir, file = split(i)
            mo = r.search(file)
            if mo:
                # Decorate with string first for sorting output
                matches.append([str(i), i, mo])
        # Refine by regexps
        if regexps:
            filtered_matches = []
            res = [re.compile(i) if d["-i"] else re.compile(i, re.I) for i in regexps]
            for r in res:
                for i in matches:
                    p = i[1]    # This is the file's Path object
                    name = p.name
                    mo = r.search(name)
                    if mo and i not in filtered_matches:
                        filtered_matches.append(i)
            matches = filtered_matches
        if matches:
            # Sort by whole path name (first element), then toss out first element
            matches = [(i[1], i[2]) for i in list(sorted(matches))]
        if 0:
            pp(matches)
            exit()
        return matches
    def ReadIndexFile(d):
        'Read the index file keyed by d["--exec"]'
        key = d["--exec"]
        if g.pickle:
            with open(g.index_files[key], "rb") as fp:
                    d["files"] = pickle.load(fp)
        else:
            with open(g.index_files[key], "r") as fp:
                d["files"] = set(fp.read().split("\n"))
        # Set d["root"] which is the files' prefix to remove
        root = {
            "bk": "/manuals/manuals",
            "ds": "/manuals",
            "eb": "/ebooks",
            "hpj": "/cygdrive/d/ebooks",
        }
        d["root"] = root[key]
    def OpenMatches(matches, d):
        '''Each match item will be (full_filename, match_object) where
        match_object is the mo for _only_ the actual file name (not the
        path).
        '''
        if len(matches) > 1:
            PrintChoices(matches, d)
            for choice in GetChoices(matches):
                OpenFile(g.app, matches, choice)
        elif len(matches) == 1:
            OpenFile(g.app, matches, 0)
        else:
            print("No matches")

if __name__ == "__main__":
    d = {   # Options dictionary
        "--exec": "ds",
    }
    regexps = ParseCommandLine(d)
    regexp = regexps[0]
    regexps.pop(0)
    ReadIndexFile(d)    # Get list of the files to search
    matches = GetMatches(regexp, d, regexps)
    OpenMatches(matches, d)

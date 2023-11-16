'''
Provides DetectUTF8(*files), which returns a list of the files that are not
UTF-8 encoded.
'''
'''
Description of program
'''
if 1:   # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Module to find files that aren't encoded as UTF-8.  Run as script
    # for command line tool.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Global variables
    __all__ = ["DetectUTF8"]
if 1:   # Core functionality
    def DetectUTF8(*files, show_unreadable=False, ignore_common=False):
        '''Returns (a, b, c) where 
        a   = List of the file in the arguments that are not UTF-8
        b   = List of files that couldn't be opened
        c   = List of files that were ignored (ignore_common must be True)
    
        If show_unreadable is True, then the unreadable files are sent to
        stderr.

        Files with common extensions known not to be UTF-8 are ignored.
        '''
        if not hasattr(DetectUTF8, "ignore"):
            DetectUTF8.ignore = set('''
                .7z .z .bz .bz2 .gz .rar .tar .tgz .zip
                .odt .ods .doc .docx .rtf .xls .xlsx .xltx .odp .ppt .odg .svg .ps .ts
                .bmp .gif .jpeg .jpg .png .ppm .tif .tiff .web .webm .wmv .pspimage
                .aac .au .avi .mid .midi .mp3 .mp4 .mpc .ogg .wav .hmi .mov
                .o .obj .pyc .pyo
                .pdf
                .pickle
                .dll .so .a
            '''.split())
        if not hasattr(DetectUTF8, "show_ignored"):
            DetectUTF8.show_ignored = False
        t.err = t("redl")
        t.ign = t("yel")
        def Error(msg, color=t.err):
            t.print(f"{color}{msg}", file=sys.stderr)
        not_utf8, not_readable, ignored = [], [], []
        for file in files:
            p = P(file)
            # See if its extension means it's to be ignored
            ext = p.suffix.lower()
            if ext in DetectUTF8.ignore:
                if DetectUTF8.show_ignored :
                    Error(f"{file!r} ignored as common file", t.ign)
                ignored.append(file)
                continue
            if not p.exists():
                if show_unreadable:
                    Error(f"{file!r} not found")
                not_readable.append(file)
                continue
            if p.is_dir():
                if show_unreadable:
                    Error(f"{file!r} is a directory")
                not_readable.append(file)
                continue
            try:
                s = open(file, "rb").read()
            except Exception as e:
                if show_unreadable:
                    Error(f"{file!r} open() exception: {e}")
                not_readable.append(file)
                continue
            try:
                s.decode()
            except UnicodeDecodeError:
                not_utf8.append(file)
        return not_utf8, not_readable, ignored
            
if __name__ == "__main__":
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dir glob1 [glob2]
          For the current directory, show the files that match the globbing
          pattern(s) that are not UTF-8 encoded.  Common files like
          bitmaps, documents, PDFs, etc. are ignored.
        Options:
            -d dir  Define directory to search (don't need dir on command line)
            -h      Print a manpage
            -r      Recurse into dir
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hr") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("r"):
                d[o] = not d[o]
            elif o == "-d":
                args.insert(P(a), 0)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
    d = {}      # Options dictionary
    globs = ParseCommandLine(d)
    dir = globs.pop(0)
    cwd = os.getcwd()
    os.chdir(dir)
    if files:
        not_utf8, not_readable, ignored = DetectUTF8(*globs,
            show_unreadable=True, ignore_common=True)
        for file in not_utf8:
            print(file)
    os.chdir(cwd)

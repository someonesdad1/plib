'''
Provides DetectUTF8(*glob_patterns), which returns a list of files that are not
UTF-8 encoded.
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
    # <programming> Module to find files that aren't encoded as UTF-8.  Run
    # as a script for a command line tool.  The algorithm is to read the
    # whole file in as binary, then try to decode it as UTF-8.  If there's
    # an exception, the file is not encoded UTF-8.  This may be inefficient
    # for lots of large files, but it's the only method guaranteed to work.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Global variables
    __all__ = ["DetectUTF8"]
if 1:   # Core functionality
    def DetectUTF8(*globs, show_unreadable=False, ignore_common=False):
        '''Returns (a, b, c) where 
        globs are file globbing patterns
        a = List of the file in the arguments that are not UTF-8
        b = List of files that couldn't be opened (or were directories)
        c = List of files that were ignored (ignore_common must be True)
    
        If show_unreadable is True, then the unreadable files are sent to
        stderr.
 
        Files with common extensions known not to be UTF-8 are ignored.
        '''
        if not hasattr(DetectUTF8, "ignore"):
            DetectUTF8.ignore = set('''
                .7z .z .bz .bz2 .gz .rar .tar .tgz .zip
                .odt .ods .doc .docx .rtf .xls .xlsx .xltx .odp .ppt .odg .svg .ps .ts .pdf
                .bmp .gif .jpeg .jpg .png .ppm .tif .tiff .web .webm .wmv .pspimage
                .aac .au .avi .mid .midi .mp3 .mp4 .mpc .ogg .wav .hmi .mov
                .o .obj .pyc .pyo .dll .so .a
                .exe .swp .pickle
            '''.split())
        if not hasattr(DetectUTF8, "show_ignored"):
            DetectUTF8.show_ignored = False
        t.err = t("redl")
        t.ign = t("yel")
        def CError(msg, color=t.err):
            t.print(f"{color}{msg}", file=sys.stderr)
        not_utf8, not_readable, ignored = [], [], []
        for glob in globs:
            # Get files to process
            if d["-r"]:
                files = P(".").rglob(glob)
            else:
                files = P(".").glob(glob)
            for file in files:
                # Ignore Mecurial and git directories
                if ".hg" in str(file) or ".git" in str(file):
                    continue
                p = P(file)
                # See if its extension means it's to be ignored
                ext = p.suffix.lower()
                if ext in DetectUTF8.ignore:
                    if DetectUTF8.show_ignored :
                        CError(f"{file!r} ignored as common file", t.ign)
                    ignored.append(file)
                    continue
                if not p.exists():
                    if show_unreadable:
                        CError(f"{file!r} not found")
                    not_readable.append(file)
                    continue
                if p.is_dir():
                    try:
                        d   # Detect if the dict d is defined
                    except NameError:
                        pass
                    else:
                        if show_unreadable and d["-e"]:
                            CError(f"{file!r} is a directory")
                    not_readable.append(file)
                    continue
                try:
                    s = open(file, "rb").read()
                except Exception as e:
                    if show_unreadable:
                        CError(f"{file!r} open() exception: {e}")
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
        Usage:  {sys.argv[0]} [options] glob1 [glob2]
          For the current directory, show the files that match the globbing
          pattern(s) that are not UTF-8 encoded.  Common file types like bitmaps,
          documents, PDFs, etc. are ignored.
 
          The method used is to read each file's contents as binary and try to decode
          it as UTF-8.  If an exception occurs, the file is not UTF-8.  Though this
          is inefficient for lots of large files, it's the only method guaranteed to
          work.
        Options:
            -d dir  Define directory to search
            -e      Show glob items that are directories to stderr
            -r      Recursive behavior
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = P(".")    # Directory to search
        d["-e"] = False     # Show glob items that are directories to stderr
        d["-r"] = False     # Recursive behavior
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:ehr") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("er"):
                d[o] = not d[o]
            elif o == "-d":
                d[o] = P(a)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
    d = {}      # Options dictionary
    globs = ParseCommandLine(d)
    cwd = os.getcwd()
    os.chdir(d["-d"])
    if globs:
        not_utf8, not_readable, ignored = DetectUTF8(*globs,
            show_unreadable=True, ignore_common=True)
        for file in not_utf8:
            print(file)
    os.chdir(cwd)

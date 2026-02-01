if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ DetectUTF8() --> list of files that are not UTF-8 oo>
        <oo desc ∞ 

            Run as a script for a command line tool.  Algorithm:  read the file in as
            binary, then try to decode it as UTF-8.  If there's an exception, the file
            is not encoded UTF-8.  Can be inefficient, but it's the only method
            guaranteed to work.

        oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ prog oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        from pathlib import Path as P
    if 1:  # Global variables
        __all__ = ["DetectUTF8"]
if 1:  # Core functionality
    def DetectUTF8(*globs, **kw):
        '''Returns (a, b, c) where globs are file globbing patterns and
          a = List of the file in the arguments that are not UTF-8
          b = List of files that couldn't be opened or were directories
          c = List of files that were ignored
        Keywords
          show_unreadable   Unreadable files are sent to stderr [False]
          ignore_common     Ignore files with common extensions [True]
          recursive         Recurse into directories
          verbose           Print each file examined with a leading '+ ' [False]
        Note .git and .hg directories are ignored and are not printed even
        if verbose is True.
        '''
        if not hasattr(DetectUTF8, "ignore"):
            DetectUTF8.ignore = set(
                '''
                .7z .z .bz .bz2 .gz .rar .tar .tgz .zip
                .odt .ods .doc .docx .rtf .xls .xlsx .xltx .odp .ppt .odg .svg .ps .ts .pdf
                .bmp .gif .jpeg .jpg .png .ppm .tif .tiff .web .webm .wmv .pspimage
                .aac .au .avi .mid .midi .mp3 .mp4 .mpc .ogg .wav .hmi .mov
                .o .obj .pyc .pyo .dll .so .a
                .exe .swp .pickle
            '''.split()
            )
        if not hasattr(DetectUTF8, "show_ignored"):
            DetectUTF8.show_ignored = False
        def Error(msg):
            print(f"{msg}", file=sys.stderr)
        # Get keywords
        #ignore_common = kw.get("ignore_common", True)
        show_unreadable = kw.get("show_unreadable", True)
        recursive = kw.get("recursive", False)
        verbose = kw.get("verbose", False)
        # Start processing
        not_utf8, not_readable, ignored = [], [], []
        for glob in globs:
            # Get files to process
            files = list(P(".").rglob(glob) if recursive else P(".").glob(glob))
            for file in files:
                # Ignore Mecurial and git directories
                parts = file.parts
                if ".." in parts or ".hg" in parts or ".git" in parts:
                    continue
                # Show name if verbose is True
                if verbose:
                    print(f"+ {file}")
                # See if it's an ignored file
                ext = file.suffix.lower()  # Specific to Windows
                if ext in DetectUTF8.ignore:
                    if DetectUTF8.show_ignored:
                        print(f"{file!r} ignored as common file")
                    ignored.append(file)
                    continue
                # Non-existent file?
                if not file.exists():
                    if show_unreadable:
                        print(f"{file!r} not found", file=sys.stderr)
                    not_readable.append(file)
                    continue
                if file.is_dir():
                    try:
                        d  # Detect if the dict d is defined
                    except NameError:
                        pass
                    else:
                        if show_unreadable:
                            dir = str(file)
                            print(f"{dir!r} is a directory", file=sys.stderr)
                    not_readable.append(file)
                    continue
                # See if we can read its bytes
                try:
                    s = open(file, "rb").read()
                except Exception as e:
                    if show_unreadable:
                        print(f"{file!r} open() exception: {e}", file=sys.stderr)
                    not_readable.append(file)
                    continue
                # See if we can decode it as UTF-8
                try:
                    s.decode("UTF-8")
                except UnicodeDecodeError:
                    not_utf8.append(file)
        return not_utf8, not_readable, ignored
if __name__ == "__main__":
    if 1:  # Standard imports
        import getopt
        import os
        import sys
    if 1:  # Custom imports
        from wrap import dedent
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] glob1 [glob2]
          For the current directory, show the files that match the globbing
          pattern(s) that are not UTF-8 encoded.  Common file types like
          bitmaps, documents, PDFs, etc. are ignored.  Note:  you'll have
          to escape the glob patterns from the shell.
        Options:
            -d dir  Define directory to search
            -e      Show glob items that are directories to stderr
            -r      Recursive behavior
            -v      Show files examined
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = P(".")  # Directory to search
        d["-r"] = False  # Recursive behavior
        d["-v"] = False  # Verbose:  show files examined
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:ehrv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("erv"):
                d[o] = not d[o]
            elif o == "-d":
                d[o] = P(a)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
    d = {}  # Options dictionary
    globs = ParseCommandLine(d)
    cwd = os.getcwd()
    os.chdir(d["-d"])
    if globs:
        # Get function's keywords
        kw = {
            "recursive": d["-r"],
            "verbose": d["-v"],
            "show_unreadable": True,
            "ignore_common": True,
        }
        not_utf8, not_readable, ignored = DetectUTF8(*globs, **kw)
        for file in not_utf8:
            print(file)
    os.chdir(cwd)

'''
Construct a tags file for a directory with *.hld files.  These are used for my vim-based help
files, allowing me to use vim to browse the set of help files.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Construct tags file for my vim-based help files oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2024 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import pathlib
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        import dpprint
        import dpseq
        import lwtest
        import trm
        import wrap
        t = trm.Trm()
    if 1:  # Import symbols
        Path = pathlib.Path
        #
        IsIterable = dpseq.IsIterable
        Assert = lwtest.Assert
        dedent = wrap.dedent
        PP = dpprint.PP
    if 1:  # Global variables
        pp = PP()
        class G: # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
if 1:  # Utility
    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Describe this option
        d["-d"] = 3  # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:  # Core functionality
    def BuildTagsFile(dir, files, verbose=False, dbg=False):
        '''Construct a tags file for the indicated directory.
          dir       Directory where the files reside
          files     Sequence of file names
          verbose   If True, print where tags file constructed
          
        For vim's help files, this is done by searching for text between two asterisk characters
        and extracting the tag.  This is written to the tags file in the form
        
            symbol\tsymbol.hld\t/*symbol*
            
        and the file is sorted on these lines.  The first line of the file must be
        'help-tags\ttags\t1'.
        '''
        if not files:
            if verbose:
                print(
                    "BuildTagsFile:  no files found in files sequence", file=sys.stderr
                )
            return
        # Make sure dir is a string or a Path instance
        Assert(isinstance(dir, (str, Path)))
        # Make sure files is an iterable
        Assert(IsIterable(files))
        # Make sure each item in files is a string or Path instance
        Assert(all(isinstance(i, (str, Path)) for i in files))
        # Our working directory is an invariant
        cwd = os.getcwd()
        # regex is a C-type token name between asterisks
        r = re.compile(r"\*([A-Za-z_][A-Za-z0-9_]*)\*")
        tags = ["help-tags\ttags\t1"]
        # Change to the output directory so there will be no directory names in the file's name
        os.chdir(dir)
        for file in files:
            p = Path(file) if isinstance(file, str) else file
            for line in p.open().readlines():
                line = line.rstrip()
                mo = r.search(line)
                if mo:
                    for tag in mo.groups():
                        t = f"{tag}\t{file}\t/*{tag}*"
                        tags.append(t)
                    if dbg:
                        print(f"tag(s) found in [{file}]:  {line!r}")
        # Get rid of duplicates
        tags = list(sorted(list(set(tags))))
        n = len(tags) - 1
        # Write the tags file
        tagsfile = Path("tags")
        with tagsfile.open("w") as f:
            f.write("\n".join(tags))
            f.write("\n")
        if verbose:
            print(f"{n} tags constructed in {tagsfile.absolute()}")
        # Go back to the directory we started from
        os.chdir(cwd)
if __name__ == "__main__":
    from lwtest import run
    def Test_BuildTagsFile():
        '''Test this in my ~/.manpages directory where there is a collection of *.hld files.
        Manual verification has proven the method works, so now running this file is the way to
        rebuild my ~/.manpages directory's tags file.
        '''
        dir = Path("/home/don/.manpages")
        files = list(dir.glob("*.hld"))
        BuildTagsFile(dir, files, dbg=False)
    exit(run(globals(), halt=True)[0])

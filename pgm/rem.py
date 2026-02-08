'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Remove character classes oo>
        <oo desc ∞ Description oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 

                - For command arguments, use '---' to force stdin to be read as
                  binary:  sys.stdin.buffer.read()

        oo>
    '''
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        import constant
        import dpseq
        import dpstr
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables

        # The following readonly container will hold global variables.  If you need to
        # change a constant's value, use 
        #     with g:
        #         g.name = value
        # Note only hashable items will be readonly.
        g = constant.Constant()
        with g:
            g.dbg = True
            g.dbg = False
if 1:   # Utility
    def GetColors():
        t.bin = t.cynl
        t.emph = t.purl
        t.err = t.redl
        t.dbg = t.sky if g.dbg else ""
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
    def Manpage():
        print(dedent(f'''

        This tool is intended to be used to modify text files in various ways.  All of
        the operations except 'A' remove specified characters from the input.  All of
        the operations except for 'A' will work on binary input.  If you're getting
        results you don't expect, make sure you're using appropriate operations on the
        type of files/data used for input (the problem can probably be fixed by using or
        not using the -b and/or the -e options).

        If you input binary data, it will be written back to stdout in binary form, so
        you'll e.g. want to be careful if you're writing to the console.  If you're not
        sure what the form of the input is, you can use the -a option to switch to
        binary input if reading a text file fails for a Unicode decoding error.
        However, this isn't much use if there are multiple input files and it happens on
        files other than the first, as you may get a mix of text and binary output.  In
        such a case, you'll probably want to not use -a and, if you see a Unicode
        decoding error, switch to binary mode with -b.

        Some examples of use

        - Text comparison:  I use the text of "Pride and Prejudice" for numerous text
          testing tasks (it's about 0.68 MB and 120 kwords).  I have two forms of this
          text file:  one with the lines wrapped at 75 characters and the other with the
          lines not wrapped.  If I compare them with my GUI differencing tool, there are
          nearly continuous differences.  However, if both are treated with this
          script's W operation (remove all whitespace), they compare identically.  I've
          used similar techniques to compare open source licenses to see how some have
          changed over a decade or so.

        - Security questions:  If I want to be able to prove my authorship of a
          document, I put a few (5 to 10) questions into the document that I (mostly)
          would be the only person who would know all the answers.

        '''))
    def Usage(status=0):
        e, b, n = t.purl, t.sky, t.n
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] letters [file1 [file2...]]
          Remove character classes from the files, as indicated by the letters, then
          print the results to stdout.
        
          {e}The files are treated as UTF-8 text files{n} unless you change the
          encoding with the -e option or use -b.  Use '-' for stdin ('--' to read stdin
          as binary).  The letters are:{b}

            A   Convert Unicode characters to rough ASCII equivalents{n}
            B   Remove characters under 0x20
            b   Remove characters under 0x20 except newline
            d   Remove characters that are ASCII digits (∈ string.digits)
            h   Remove characters that are hex digits (∈ string.hexdigits)
            l   Remove lower case letters (∈ string.ascii_lowercase)
            n   Remove punctuation (∈ string.punctuation)
            o   Remove characters that are octal digits (∈ string.octdigits)
            p   Remove non-printable characters (∉ string.printable)
            u   Remove upper case letters (∈ string.ascii_uppercase)
            W   Remove whitespace (∈ string.whitespace)
            w   Remove whitespace except newlines
            7   Remove characters above 0x7f (i.e., keep only 7-bit characters)
            8   Remove characters above 0xff (i.e., keep only 8-bit characters)
          A letter line {b}in this color{n} is one that can only be used on text
          files, as the transformation has no meaning on binary files.
        Options:
          -a    If reading text fails, automatically switch to binary
          -b    Treat the files as binary, not text
          -d    Turn on debug printing
          -e e  Change the encoding used (names from the python codecs module)
          -H    Print a manpage
          -l    Convert all text to lower case
          -u    Convert all text to upper case
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Switch to binary if not text
        d["-b"] = False     # Binary file input
        d["-d"] = False     # Debug printing
        d["-e"] = "UTF-8"   # Decoding method
        d["-l"] = False     # Convert to lower case
        d["-u"] = False     # Convert to upper case
        if len(sys.argv) < 2:
            GetColors()
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "abde:hlu") 
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            exit(1)
        for o, a in opts:
            if o[1] in list("abdlu"):
                d[o] = not d[o]
            elif o == "-e":     # Encoding method
                d[o] = a
            elif o == "-h":
                Usage()
        GetColors()
        if d["-d"]:
            with g:
                g.dbg = True
            GetColors()
            Dbg(f"argv:  {sys.argv}")
            for i in d:
                Dbg(f"  d[{i}] = {d[i]}")
        if len(args) < 2:
            Usage()
        if 1:   # Get the transformation letters
            with g:
                g.letters = ''.join(dpseq.NodupHashable(args.pop(0)))
            Dbg(f"g.letters = {g.letters!r}")
        return args
if 1:   # Core functionality
    def GetFileData(file):
        'file is a string; return either text or bytes as appropriate'
        if 1:   # Always get the data in binary form
            if file == "-" or file == "--":
                s = sys.stdin.buffer.read()
                # Note this returns bytes
                b = eval(f"s.encode(d['-e'])")
            else:
                p = Path(file)
                if p.is_dir():
                    Error(f"{file!r} is a directory")
                elif p.is_file():
                    if not p.exists():
                        Error(f"{file!r} does not exist")
                b = p.read_bytes()
        if 1:   # Decide on text or bytes
            if d["-b"]:     # Bytes if d["-b"] set
                is_text = False
                data = b
            else:           # Text otherwise
                is_text = True
                decoded_OK = False
                try:
                    data = b.decode(d["-e"])
                    decoded_OK = True
                except UnicodeDecodeError:
                    if d["-a"]:     # Use binary if text decoding fails
                        data = b
                        is_text = False
                    else:
                        raise
        if 1:   # -u and -l transformations
            if d["-u"]:
                data = data.upper()
            if d["-l"]:
                data = data.lower()
        if 1:   # Dbg output
            n = len(data)
            m = 256
            if is_text:
                Dbg(f"Data:  read in {n} characters as {t.redl}text")
                Dbg(f"Data (first {m} characters/bytes) =", repr(data[:m]))
            else:
                Dbg(f"Data:  read in {n} bytes as {t.redl}binary")
                u = repr(data[:m])
                Dbg(f"Data (first {m} characters/bytes) = {u}")
        return data
    def Process(file):
        'Process file (a Path instance) and send the results to stdout'
        data = GetFileData(file)
        if (type(data) is bytes and "A" in g.letters):
            Error("'A' cannot be used on binary data")
        output = dpstr.RemoveCharClass(data, keys=g.letters) 
        if isinstance(output, str):
            print(output, end="")
        else:
            sys.stdout.buffer.write(output)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        Process(file)

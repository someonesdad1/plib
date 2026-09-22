'''
Generate an HTML difference of two files and launch in browser
    Note the tempfile used is not cleaned up.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Two file HTML difference oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import difflib
        import getopt
        import sys
        import tempfile
    if 1:  # Custom imports
        from launch import Launch
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def ShowDifference(old_str, new_str):
        h = difflib.HtmlDiff()
        s = h.make_file(old_str.split("\n"), new_str.split("\n"))
        fd, name = tempfile.mkstemp(suffix=".html", dir="/tmp/dontmp")
        open(name, "w").write(s)
        Launch(name)
        # This leaves the temporary file because there's no easy way to
        # determine when the browser is finished looking at it.

if __name__ == "__main__":
    from wrap import dedent
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 file2
          Show an HTML difference between the two files in a browser.
        Options:
          -i   Ignore case
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if len(args) != 2:
            Usage(d)
        return args
    def GetFile(file):
        s = open(file, "rb").read()
        if isinstance(s, bytes):
            s = s.decode()
        assert isinstance(s, str)
        return s
    d: dict[object, object] = {}  # Options dictionary
    file1, file2 = ParseCommandLine(d)
    old, new = GetFile(file1), GetFile(file2)
    if d["-i"]:
        old = old.lower()
        new = new.lower()
    ShowDifference(old, new)

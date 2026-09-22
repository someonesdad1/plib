'''
This module gets the text of various software licenses.  They are
encapsulated using the License class, which provides various features.

Note the licenses' text is in /pylib/licenses.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Encapsuate text of software licenses oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014, 2021 Don Peterson oo>
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
        import collections
        import pathlib
        import requests
        import sys
    if 1:  # Custom imports
        if len(sys.argv) > 1:
            import debug
            debug.SetDebugger()
        from textcompare import TextCompare
    if 1:  # Global variables
        pass
if 1:  # Classes
    class License:
        'Container for license text'
        def __init__(self, header, text=None, url=None):
            '''If text is None, the whole license is in header.  If url is
            not None, it's a location that the text file can be gotten for
            validation.
            '''
            self._text = self.strip_comments(text) if text else None
            self.header = header
            self.url = url
        def is_valid(self):
            "Download text from url and compare"
            if self.url is None:
                raise ValueError("No url given")
            r = requests.get(self.url)
            new_text = r.content
            if isinstance(new_text, bytes):
                new_text = new_text.decode()
            c = TextCompare(self.text, new_text)
            return c.equal
        def strip_comments(self, s):
            nl = "\n"
            t, d = [], collections.deque(s.split(nl))
            while d:
                u = d.popleft()
                if u and u[0] == "#":
                    continue
                t.append(u)
            return nl.join(t).strip()
        @property
        def text(self):
            return self.header if self._text is None else self._text
if 1:  # Core functionality
    # This dictionary uses keys like "apache2" to hold the License objects
    # containing the text and headers of the various licenses.
    licenses = {}
    urls = {
        "apache2": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        "ccsa4": "https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt",
    }
    # Fill licenses from the licenses directory
    P = pathlib.Path
    p = P("/plib/lib/licenses")
    def get(x):
        with open(x) as fp:
            s = fp.read()
        return s
    for h in p.glob("*.header"):
        header = get(h)
        f = P(str(h).replace(".header", ""))
        key = f.name
        text = get(f) if f.exists() else None
        L = License(header, text=text, url=urls.get(key, None))
        licenses[key] = L
    if 0:
        from pprint import pprint as pp
        pp(licenses)

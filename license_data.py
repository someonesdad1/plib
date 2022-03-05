'''
This module contains the text of various software licenses.  They are
encapsulated using the License class, which provides various features.
'''
#∞test∞# ignore #∞test∞#
import collections
import difflib
import hashlib
import pathlib
import requests
import io
import sys
from pdb import set_trace as xx

# Custom modules
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()
from textcompare import TextCompare

class License:
    'Container for license text'
    def __init__(self, header, text=None, url=None):
        '''If text is None, the whole license is in header.  If url is
        None, it's a location that the text file can be gotten for
        validation.
        '''
        self._text = self.strip_comments(text) if text else None
        self.header = header
        self.url = url
    def is_valid(self):
        'Download text from url and compare'
        if self.url is None:
            raise ValueError("No url given")
        r = requests.get(self.url)
        new_text = r.content
        if type(new_text) == type(b''):
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

# This dictionary uses keys like "apache2" to hold the License objects
# containing the text and headers of the various licenses.
licenses = {}

urls = {
    "apache2": "https://www.apache.org/licenses/LICENSE-2.0.txt",
    "ccsa4": "https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt",
}

# Fill licenses from the licenses directory
P = pathlib.Path
p = P("/pylib/licenses")
get = lambda x: open(x).read()
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

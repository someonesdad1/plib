'''
Provides a debug printing class Debug that is called like print()
    Typical usage:
        from dbg import Debug
        Dbg = Debug()       # Get a class instance
        Debug.dbg = True    # Enable debug printing
        Dbg("This is a debugging message")
        # Debug print in a different color
        Dbg("In a different color", color=t.grn)
    Run this script for a demo.
    
    Since Debug is a class, you can have multiple instances that can
    print messages in different colors.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Provides a debug printing class Debug that is called like print() oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2022 Don Peterson oo>
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
        import sys
    if 1: # Custom imports
        from color import t
    if 1: # Global variables
        __all__ = "Debug".split()
if 1:  # Core functionality
    class Debug:
        dbg = False  # Debug printing is off by default
        def __init__(self, fg="cyn", bg=None, attr=None, leader="", file=sys.stdout):
            self.fg = fg
            self.bg = bg
            self.attr = attr
            self.leader = leader
            self.file = file
            self.esc = t(fg, bg, attr)
            self.color = t(fg, bg, attr)  # Generates needed escape codes
        def __bool__(self):
            "Return True if printing is on"
            return bool(Debug.dbg)
        def __call__(self, *p, **kw):
            '''Print to the debug stream if the Debug.dbg class variable is
            True.  The syntax is the same as print() except there's an
            additional keyword 'color' which must be a color instance; if
            it's present, it changes the color printed.
            '''
            if not Debug.dbg:
                return
            # Make a copy of kw so we don't change user's copy
            kwc = kw.copy()
            clr = self.esc
            # If user passed in a color keyword, it must be an escape
            # string.
            if "color" in kwc:
                clr = kwc["color"]
                assert isinstance(clr, str)
                del kwc["color"]
            print(f"{clr}", file=self.file, end="")
            print(self.leader, file=self.file, end="")
            print(*p, **kwc)
            print(f"{t.n}", file=self.file, end="")

if __name__ == "__main__":
    # Dbg demo
    D = Debug()
    Debug.dbg = False
    D("You shouldn't see this message")
    Debug.dbg = True
    D("You should see this message")
    D = Debug("ornl", None, "it")
    D("This should be in orange italics")

'''
Provides a debug printing function Dbg that is called like print()
    Typical usage:
        import dbg
        dbg.dbg = True          # Enable debug printing
        Dbg = dbg.GetDbg()      # Get the default Dbg function
        Dbg("This is a debugging message")
    Run this script for a demo.
'''
if 1:   # Header
    # Copyright, license
    if 1:
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Dbg() debug printing function
        #∞what∞#
        #∞test∞# None #∞test∞#
        pass
    # Standard imports
    if 1:
        from pathlib import Path as P
        import sys
    # Custom imports
    if 1:
        from color import Color, TRM as t
    # Global variables
    if 1:
        ii = isinstance
        dbg = False
        __all__ = "GetDbg dbg".split()
if 1:   # Core functionality
    class Debug:
        def __init__(self, fg="lill", bg=None, attr=None, leader="", file=sys.stdout):
            self.fg = fg
            self.bg = bg
            self.attr = attr
            self.leader = leader
            self.file = file
            self.esc = t(fg, bg, attr)
            self.color = t(fg, bg, attr)   # Generates needed escape codes
        def __call__(self, *p, **kw):
            '''Print to the debug stream if the dbg global variable is
            True.  The syntax is the same as print() except there's an
            additional keyword 'color' which must be a color instance; if
            it's present, it changes the color printed.
            '''
            if not dbg:
                return
            kwc = kw.copy()
            clr = self.esc
            # If user passed in a color keyword, it must be an escape
            # string.
            if "color" in kwc:
                clr = kwc["color"]
                assert(ii(clr, str))
                del kwc["color"]
            print(f"{clr}", file=self.file, end="")
            print(self.leader, file=self.file, end="")
            print(*p, **kwc)
            print(f"{t.n}", file=self.file, end="")

    def GetDbg(fg="lill", bg=None, attr=None, leader="", file=sys.stdout):
        '''Call this function to set up the printing style you want for the
        Dbg() calls.   A Debug instance is returned.
        The parameters are:
            fg      String to identify foreground color
            bg      String to identify background color
            attr    String to identify printing attributes
            color   List of three strings to define a color & style using 
                    the color.t instance of color.TRM.
            leader  Leading string of debug printing
            file    Stream to send the output from Dbg
        Some style strings are:
            it      Italic
            bl      Blink
            rb      Rapid blink
            bo      Bold
            ul      Underline
            rv      Reverse
        '''
        debug = Debug(fg=fg, bg=bg, attr=attr, leader=leader, file=file)
        return debug
    def Dbg(*p, **kw):
        '''Print to the debug stream (set with GetDbg) if the dbg global
        variable is True.  The syntax is the same as print().
        '''
        if not dbg:
            return
        print(Dbg.color, file=Dbg.file, end="")
        print(Dbg.leader, file=Dbg.file, end="")
        print(*p, **kw)
        print(f"{t.n}", file=Dbg.file, end="")

if __name__ == "__main__":
    # Dbg demo
    D = GetDbg()
    dbg = False
    D("You shouldn't see this")
    dbg = True
    D("You should see this")
    D = GetDbg(["ornl", None, "it"])
    D("This should be in orange italics")

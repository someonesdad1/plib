'''
Provides a debug printing class Debug that is called like print()
    Typical usage:
        from dbg import Debug
        Dbg = Debug()       # Get a class instance
        Debug.dbg = True    # Enable debug printing
        Dbg("This is a debugging message")
        # Debug print in a different color
        Dbg("In a different color", color=t("grn"))
    Run this script for a demo.
 
    Since Debug is a class, you can have multiple instances that can
    print messages in different colors.
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
        __all__ = "Debug".split()
if 1:   # Core functionality
    class Debug:
        dbg = False     # Debug printing is off by default
        def __init__(self, fg="cyn", bg=None, attr=None, leader="", file=sys.stdout):
            self.fg = fg
            self.bg = bg
            self.attr = attr
            self.leader = leader
            self.file = file
            self.esc = t(fg, bg, attr)
            self.color = t(fg, bg, attr)   # Generates needed escape codes
        def __bool__(self):
            'Return True if printing is on'
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
                assert(isinstance(clr, str))
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

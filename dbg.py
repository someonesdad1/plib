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
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
    if 1:
        from wrap import wrap, dedent
        from color import Color, TRM as t
    # Global variables
    if 1:
        dbg = False
        __all__ = "GetDbg dbg".split()
if 1:   # Core functionality
    def GetDbg(color=["skyl", None, None], leader="", file=sys.stdout):
        '''Call this function to set up the printing style you want for the
        Dbg() calls.   The function returned is the debug printing
        function.  The parameters are:
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
        Dbg.color = t(*color)   # Generates needed escape codes
        Dbg.file = file
        Dbg.leader = leader
        return Dbg
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

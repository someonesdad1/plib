"""
Provides SetDebugger.  Use this module when debugging things like color.py,
which will cause a circular import if you try to call debug.SetDebugger().
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2009, 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <programming> SetDebugger() from debug.py to avoid circular
    # import from color.py.
    ##∞what∞#
    ##∞test∞# ignore #∞test∞#
    # Standard imports
    import sys
    import traceback as TB
    import bdb
    import pdb


def TraceInfo(type, value, traceback):
    """Start the debugger after an uncaught exception.  From Thomas
    Heller's post on 22 Jun 2001 http://code.activestate.com/recipes/65287
    Also see page 435 of "Python Cookbook".
    """
    # Updated first test logic from https://gist.github.com/rctay/3169104
    if (
        hasattr(sys, "ps1")
        or not sys.stderr.isatty()
        or not sys.stdout.isatty()
        or not sys.stdin.isatty()
        or issubclass(type, bdb.BdbQuit)
        or issubclass(type, SyntaxError)
    ):
        # You are in interactive mode or don't have a tty-like device,
        # so call the default hook.
        sys.__excepthook__(type, value, traceback)
    else:
        # You are not in interactive mode; print the exception.
        TB.print_exception(type, value, traceback)
        print()
        # Now start the debugger
        pdb.pm()


def SetDebugger():
    """If you execute this function, TraceInfo() will be called when
    you get an unhandled exception and you'll be dumped into the
    debugger.
    """
    sys.excepthook = TraceInfo

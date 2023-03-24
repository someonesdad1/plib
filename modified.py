'''
This script provides Modified(), which prints a colored string to stderr
to notify of a change in a file.

    Use case:  If you're working on a modification to a core library file,
    it's common to put mainline test code in to test your changes, often
    followed by an exit() call.  However, this then breaks a lot of scripts
    that depend on this library.  If you use e.g.
    Modified(Path(Path("myscript.py"), "Working on bug fix")) just before
    the exit() call, the message will be seen when other code tries to use
    that library and you'll be able to fix things.

Example usage:

    from modified import Modified, Path
    Modified(Path("myscript.py"))
    exit()

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <utility> Print warning message to stderr about a library file
        # being modified.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path
    if 1:   # Custom imports
        from color import t
if 1:   # Core functionality
    def Modified(file, msg=None):
        '''file must be a valid Path object.  Prints msg in color to stderr if
        it's present.
        '''
        assert(isinstance(file, Path))
        if msg is None:
            t.print(f"{t('redl')}{file.resolve()} is modified")
        else:
            t.print(f"{t('magl')}{file.resolve()} {msg}")

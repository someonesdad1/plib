'''
Provides the function PP which returns a form of the pprint.pprint function
with a width argument set to the desired width.
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Provides pp, a pprint aware of the screen width
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard imports
        import os
        from functools import partial
        from pprint import pprint
    # Global variables 
        __all__ = ["PP"]
def PP(width=None):
    '''Returns pprint.pprint with a width parameter set to one less than
    the current screen width if the parameter width is None.  Otherwise,
    it's a number converted to a positive integer that must be nonzero.
    '''
    columns = int(os.environ.get("COLUMNS", 80)) - 1
    if width is not None:
        try:
            columns = int(abs(width))
            if not columns:
                raise ValueError("PP():  width parameter must not be zero")
        except Exception as e:
            print(e)
            exit(1)
    return partial(pprint, width=columns)

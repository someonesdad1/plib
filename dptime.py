"""
This is a module with functions to return the datea and time as I like to see them.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Provides dptime(), a function that returns the date and time as I like to see it.
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import time
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert

        if 0:
            import debug

            debug.SetDebugger()
if 1:  # Core functionality

    def dpdate():
        "Return the date in a format like '1 Jan 2025'"
        s = time.strftime("%d %b %Y")
        if s[0] == "0":
            s = s[1:]
        return s

    def dptime():
        "Return the time in a format like '7:14:16 am'"
        ampm = time.strftime(f"%p").lower()
        s = time.strftime(f"%I:%M:%S {ampm}")
        if s[0] == "0":
            s = s[1:]
        return s

    def dpdatetime():
        return dpdate() + " " + dptime()


if __name__ == "__main__":
    print(f"dpdate() returns:  {dpdate()!r}")
    print(f"dptime() returns:  {dptime()!r}")
    print(f"dpdatetime() returns:  {dpdatetime()!r}")

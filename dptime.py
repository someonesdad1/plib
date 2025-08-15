'''
This is a module with functions to return the date and time as I like to see them 
and handy time formatting stuff.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Provides dptime(), a function that returns the date and time as I like to see it.
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import time
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from u import u
        from roundoff import RoundOff
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
    def NiceET(seconds, digits=4):
        '''Return an elapsed time in seconds in friendly units so that scientific 
        display is not needed.  The used units will be ns, μs, ms, s, min, hr, day,
        month, yr.  Longer intervals will be in yr with an SI prefix.
        '''
        sec = flt(seconds)
        with sec:
            sec.N = digits
            if sec < 1:
                return f"{sec.engsi}s"
            elif sec < u("minute"):
                return f"{sec} s"
            elif sec < u("hour"):
                use = "min"
                return f"{sec/u(use)} {use}"
            elif sec < u("day"):
                use = "hr"
                return f"{sec/u(use)} {use}"
            elif sec < u("month"):
                use = "days"
                return f"{sec/u(use)} {use}"
            elif sec < u("year"):
                use = "months"
                return f"{sec/u(use)} {use}"
            else:
                use = "yr"
                y = sec/u(use)
                if y < 1000:
                    return f"{y} {use}"
                else:
                    return f"{y.engsi}{use}"

if __name__ == "__main__":
    print(f"dpdate() returns:  {dpdate()!r}")
    print(f"dptime() returns:  {dptime()!r}")
    print(f"dpdatetime() returns:  {dpdatetime()!r}")

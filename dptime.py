'''
This is a module with functions to return the date and time as I like to see them 
and handy time formatting stuff.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Date and time in formats I like oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2024 Don Peterson oo>
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
        import time
    if 1:  # Custom imports
        from f import flt
        from u import u
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
        ampm = time.strftime("%p").lower()
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

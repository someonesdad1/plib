'''
Date/time strings for now() I use a lot
'''
if 1:   # Header
    _pgminfo = '''
        <oo gist ∞ oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ time oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
            - ∞∞2 Combine with dptime.py
        oo>
    '''
    if 1:   # Standard imports
        from time import strftime
    if 1:   # Custom imports
        pass
if 1:   # Core functionality
    def Date():
        'Date = 12Feb2022'
        s = strftime("%d%b%Y")
        if s[0] == "0":
            s = s[1:]
        return s
    def date():
        'date = 12 Feb 2022'
        s = strftime("%d %b %Y")
        if s[0] == "0":
            s = s[1:]
        return s
    def Time():
        'Time = 8:50:00am'
        s = strftime("%p").lower()
        t = strftime(f"%I:%M:%S{s}")
        if t[0] == "0":
            t = t[1:]
        return t
    def time():
        'time = 8:50:00 am'
        s = strftime("%p").lower()
        t = strftime(f"%I:%M:%S {s}")
        if t[0] == "0":
            t = t[1:]
        return t
    def Dttm():
        'Date/time = 12Feb2022-8:50:00am'
        return f"{Date()}-{Time()}"
    def dttm():
        'Date/time = 12 Feb 2022 8:50:00 am'
        return f"{date()} {time()}"
    def tm24():
        'Time in 24 hour mode'
        return strftime("%H:%M:%S")
    def Dttm24():
        'Date/time in 24 hr mode = 12Feb2022-08:50:00'
        return f"{Date()}-{tm24()}"
    def dttm24():
        'Date/time in 24 hr mode = 12Feb2022 08:50:00'
        return f"{date()} {tm24()}"

if __name__ == "__main__":
    print(f"Date() = {Date()}, date() = {date()}")
    print(f"Time() = {Time()}, time() = {time()}")
    print(f"Date/time (Dttm()) = {Dttm()}")
    print(f"Date/time (dttm()) = {dttm()}")
    print(f"Time in 24 hr mode (tm24()) = {tm24()}")
    print(f"Date/time in 24 hr mode (Dttm24()) = {Dttm24()}")
    print(f"Date/time in 24 hr mode (dttm24()) = {dttm24()}")

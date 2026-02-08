if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Shop utilities (obsolete) oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ shop oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - ∞∞1 See if GetDouble, GetInt, GetChoice can be moved to a different
              module, such as get.py. 
            - Update to python 3 semantics where needed
            - This is for old /shop scripts.  This functionality should be in get.py.
            - Once done, this module can be eliminated.
        
        oo>
    '''
    if 1:  # Standard imports
        import math
    if 1:  # Custom imports
        from f import flt
    if 1:  # Global variables
        debug = 0
if 1:  # Core functionality
    def GetDouble(prompt, default, low, high):
        if debug:
            return flt(default)
        str = ""
        while True:
            str = input(prompt + " [" + default + "] ").strip()
            if str == "":
                return flt(default)
            elif str == "q":
                exit(0)
            try:
                choice = flt(eval(str))
                if choice < low or choice > high:
                    raise Exception()
                return choice
            except Exception:
                print(
                    ("'%s' not an acceptable number.  Must lie between %f " + "and %f.")
                    % (str, low, high)
                )
    def GetInt(prompt, default, low, high):
        if debug:
            return default
        str = ""
        while True:
            str = input(prompt + " [" + repr(default) + "] ").strip()
            if not str:
                return default
            elif str == "q":
                exit(0)
            try:
                choice = int(eval(str))
                if choice < low or choice > high:
                    raise Exception()
                return choice
            except Exception:
                print(
                    ("'%s' not an acceptable integer.  Must lie between %d " + "and %d.")
                    % (str, low, high)
                )
    def GetChoice(prompt, default, choices, quit="q"):
        if debug:
            return default
        ok = False
        while not ok:
            choice = input(prompt + " [" + default + "] ").strip()
            if choice == "":
                return default
            elif choice == quit:
                exit(0)
            if choice in choices:
                ok = True
            else:
                print(
                    "Not a valid answer.  Must be one of the following\n"
                    + "  "
                    + repr(choices)
                )
        return choice

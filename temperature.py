if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Temperature conversions oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2025 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ math oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        pass
    if 1:  # Custom imports
        from f import flt
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def ConvertTemperature(T, uin, uout, rettype=flt, strict=False):
        '''Convert temperature T in input units uin to output units uout.  Return a numerical type
        of rettype.  The temperature units can be k c f r K C F R (i.e., case doesn't matter).  The
        function works by converting the input temperature to K, then converting it to the given
        output unit:
        
            k K     Kelvin
            c C     °C (Celsius or centigrade)
            f F     °F (Fahrenheit)
            r R     °R (Rankine)
        If strict is True, any temperature T that is less than 0 K raises a ValueError.
        
        Example:  ConvertTemperature(0, "c", "k") returns 273.15.
        '''
        units = set("kcfr")
        if uin.lower() not in units:
            raise ValueError(f"uin = {uin!r} not a recognized temperature unit")
        if uout.lower() not in units:
            raise ValueError(f"uout = {uout!r} not a recognized temperature unit")
        # Conversion constants
        R = rettype
        k0 = R("273.15")  # 0 °C in K
        p0 = R("9")/R("5")  # Number of °F in K
        c0 = R("32")  # Freezing point of water in °F
        r0 = R("459.67")  # 0 °C in °R
        # Create functions to convert from a given unit to K
        toK = {
            "k": lambda k: R(k),
            "c": lambda c: c + k0,
            "f": lambda f: (f - c0)/p0 + k0,
            "r": lambda r: (r - r0 - c0)/p0 + k0,
        }
        fromK = {
            "k": lambda k: R(k),
            "c": lambda c: c - k0,
            "f": lambda f: (f - k0)*p0 + c0,
            "r": lambda r: (r - k0)*p0 + c0 + r0,
        }
        # Perform the conversion
        if not T and (
            (uin.lower() == "k" and uout.lower() == "r")
            or (uin.lower() == "r" and uout.lower() == "k")
        ):
            Tout = 0  # Handles e.g. where 0 K rounds to 5.68e-14 °R
        else:
            Tin = toK[uin.lower()](T)  # Convert T in uin to K
            if strict and Tin < 0:
                raise ValueError(f"Input temperature T = {T} is less than 0 K")
            Tout = fromK[uout.lower()](Tin)  # Convert Tin in K to uout
        return R(Tout)

if __name__ == "__main__":
    if 1:  # Standard imports
        from fractions import Fraction
        from decimal import Decimal
    if 1:  # Custom imports
        from lwtest import Assert, assert_equal, run, raises
    try:
        from mpmath import mpf
        have_mpmath = True
    except ImportError:
        have_mpmath = False
    CT = ConvertTemperature
    def TestConversions():
        k0 = 273.15  # 0 °C in K
        c0 = 32  # Freezing point of water in °F
        r0 = 459.67  # 0 °C in °R
        reltol = 1e-13
        # To K
        Assert(CT(0, "c", "k") == k0)
        Assert(CT(c0, "f", "k") == k0)
        Assert(CT(c0 + r0, "r", "k") == k0)
        # From K
        Assert(CT(k0, "k", "c") == 0)
        Assert(CT(k0, "k", "f") == c0)
        Assert(CT(k0, "k", "r") == c0 + r0)
        # Identity transformations
        T = 1
        for u in list("kcfr"):
            assert_equal(T, CT(T, u, u), reltol=reltol)
        # Test strict
        raises(ValueError, CT, -1, "k", "k", strict=True)
        # Unknown unit raises exception
        raises(ValueError, CT, 1, "z", "k")
        raises(ValueError, CT, 1, "k", "z")
    def TestConversionTypes():
        "Show that we can utilize other number types"
        tc, tf = 100, 212
        # Complex
        T = complex(tc, 0)
        Tf = CT(T, "c", "f", rettype=complex)
        Assert(Tf == tf)
        Assert(isinstance(Tf, complex))
        # Fraction
        T = Fraction(tc, 1)
        Tf = CT(T, "c", "f", rettype=Fraction)
        Assert(Tf == tf)
        Assert(isinstance(Tf, Fraction))
        # Decimal
        T = Decimal(str(tc))
        Tf = CT(T, "c", "f", rettype=Decimal)
        Assert(Tf == tf)
        Assert(isinstance(Tf, Decimal))
        # mpmath
        if have_mpmath:
            T = mpf(str(tc))
            Tf = CT(T, "c", "f", rettype=mpf)
            Assert(Tf == tf)
            Assert(isinstance(Tf, mpf))
    exit(run(globals(), halt=True)[0])

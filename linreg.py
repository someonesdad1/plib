if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Linear regression for y = m*x + b oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2020 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ math oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - ∞∞2 Move to dpmath
        
        oo>
    '''
    if 1:  # Standard imports
        pass
    if 1:  # Custom imports
        from f import flt
    if 1:  # Global variables
        pass
if 1:  # Simple linear regression
    def LinearRegression(x, y):
        "Return (m, b, Rsquared) for a simple linear regression"
        if len(x) != len(y):
            raise ValueError("x and y are not same length")
        n, sx, sy = len(x), sum(x), sum(y)
        sXX = sum([i*i for i in x])
        sYY = sum([i*i for i in y])
        sXY = sum([i*j for i, j in zip(x, y)])
        m = flt((n*sXY - sx*sy)/(n*sXX - sx**2))
        b = flt((sy - m*sx)/n)
        Rsquared = flt((n*sXY - sx*sy)**2/((n*sXX - sx**2)*(n*sYY - sy**2)))
        return (m, b, Rsquared)

if __name__ == "__main__":
    from lwtest import run, Assert
    def Test_LinearRegression():
        # Test case checked against HP-42s
        x = [1, 2, 3]
        y = [1, 2, 3.1]
        m, b, Rsq = LinearRegression(x, y)
        Assert(m == 1.0500000000000018)
        Assert(b == -0.06666666666667058)
        Assert(Rsq == 0.9992447129909383)
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

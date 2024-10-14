# vi: wm=0 tw=0
'''
Mean, variance, covariance data of proposed CIE 10° tristimulus functions

    Data from I. Nimeroff, J. Rosenblatt, M. Dannemiller, "Variability of
    Spectral Tristimulus Values", J. Research of the NBS A, 65A(6) 475-483,
    Nov-Dec 1961.

    Observations from the paper:

    - The data came from two independent investigations 
        - Burch & Stiles 1959: sample size of 53 British observers
        - Speranskaya 1958:  sample size of 27 Russian observers
        - The covariance data are estimated only on the basis of the Burch &
          Stiles paper. [pg 475]

    - The data were proposed CIE 10° observer tristimulus functions.

    - The standard deviations of these independent investigations are
      essentially the same order of magnitude and range from 10 to 20 percent
      of the mean function. [pg 479]  As the within-observer variances are
      relatively small, the estimated between-observer variances are only
      slightly overstated.

    - Figures 2, 3, and 4 are semilog plots (the y-axis is the red/green/blue
      primary responses and standard deviations and is the log axis; the x axis
      is the wavelength in nm) and allow comparison of the means and standard
      deviations of the two experiments.  The standard deviations are
      reasonably close except for the > 500 nm data for the blue primary.  
        - The authors give two possible reasons for this discrepancy, both due
          to experimental methods.
        - The figures show interesting heteroscedastic behavior that might be
          clues to how the human visual system works.  

    This module provides two tuples of the data:  table3 and table4.  The
    floating point values are given as f.flt objects.

'''
from f import flt
from wrap import dedent
from pdb import set_trace as xx 
#----------------------------------------------------------------------------
# Table 3 in Nimeroff, pg 482.  This is the proposed CIE tristimulus
# functions for a 10° observer with variances and covariances.
#   λ =  wavelength in nm
#   v(x) = variance of x (these are between-observer variances)
#   c(x, y) = covariance of x, y
#   x = xbar (mean)
#   y = xbar (mean)
#   z = xbar (mean)

# It is difficult to assign degrees of freedom to these data, as the paper
# is not specific enough and I didn't look at the original experimental
# papers.  At the top of page 481 is mentioned a total of 80 observers, so
# this might be a reasonable number for d.f.

# 0      1          2          3          4            5          6                 7             8                9
# λ      x          y          z         v(x)         v(y)       v(z)            c(x, y)       c(x, z)          c(y, z)
table3_data = '''
    400 0.0191097  0.0020044  0.0860109   0.000126    0.00000118   0.00256         +0.0000104    +0.000568        +0.0000467
    410 0.084736   0.008756   0.389366    0.000661    0.0000110    0.0132          +0.0000708    +0.00294         +0.000321
    420 0.204492   0.021391   0.972542    0.000937    0.0000262    0.0193          +0.0000731    +0.00421         +0.000350
    430 0.314679   0.038676   1.55348     0.000737    0.0000671    0.0154          +0.000106     +0.00329         +0.000509
    440 0.383734   0.062077   1.96728     0.000385    0.0000448    0.00978         +0.0000816    +0.00189         +0.000355
    450 0.370702   0.089456   1.99480     0.000353    0.0000561    0.00815         +0.0000413    +0.00161         +0.000185
    460 0.302273   0.128201   1.74537     0.00109     0.0000995    0.0206          -0.0000151    +0.00454         +0.000136
    470 0.195618   0.185190   1.31756     0.00110     0.000272     0.0180          -0.000101     +0.00423         -0.000131
    480 0.080507   0.253589   0.772125    0.000716    0.000602     0.00606         -0.000108     +0.00182         -0.00000827
    490 0.016172   0.339133   0.415254    0.000675    0.00105      0.00234         -0.0000633    +0.000973        +0.0000759
    500 0.003816   0.460777   0.218502    0.000414    0.00129      0.000593        +0.000000553  +0.000279        -0.000245
    510 0.037465   0.606741   0.112044    0.000325    0.000829     0.000190        +0.000884     +0.000112        -0.0000999
    520 0.117749   0.761757   0.060709    0.000183    0.000457     0.0000649       +0.000109     +0.0000325       -0.0000185
    530 0.236491   0.875211   0.030451    0.000143    0.000253     0.0000271       +0.000100     +0.00000547      -0.00000204
    540 0.376772   0.961988   0.013676    0.000622    0.000590     0.0000431       +0.00301      +0.0000133       -0.0000285
    550 0.529826   0.991761   0.003988    0.00143     0.000668     0.000105        +0.000528     +0.0000531       -0.0000700
    560 0.705224   0.997340   0.000000    0.00283     0.000847     0.000100        +0.000960     +0.000102        -0.0000513
    570 0.878655   0.955552   0.000000    0.00437     0.000998     0.0000942       +0.00142      +0.000147        -0.0000107
    580 1.01416    0.868934   0.000000    0.00569     0.00113      0.0000778       +0.00181      +0.000184        +0.0000381
    590 1.11852    0.777405   0.000000    0.00588     0.000947     0.0000652       +0.00194      +0.000194        +0.0000806
    600 1.12399    0.658341   0.000000    0.00493     0.000731     0.0000379       +0.00170      +0.000148        +0.0000720
    610 1.03048    0.527963   0.000000    0.00324     0.000475     0.0000248       +0.00116      +0.000102        +0.0000518
    620 0.856297   0.398057   0.000000    0.00159     0.000240     0.0000123       +0.000601     +0.0000449       +0.0000222
    630 0.647467   0.283493   0.000000    0.000575    0.0000918    0.00000587      +0.000226     +0.0000120       +0.00000591
    640 0.431567   0.179828   0.000000    0.0000750   0.0000127    0.000000280     +0.0000305    +0.000000138     +0.000000067
    650 0.268329   0.107633   0.000000    0.0000470   0.00000794   0.000000050     +0.0000191    +0.000000052     +0.000000032
    660 0.152568   0.060281   0.000000    0.0000458   0.00000713   0.000000043     +0.0000179    +0.000000166     +0.000000091
    670 0.0812606  0.0318004  0.000000    0.0000129   0.00000192   0.000000016     +0.00000492   +0.000000084     +0.000000044
    680 0.0408508  0.0159051  0.000000    0.00000427  0.000000619  0.0000000017    +0.00000161   +0.000000013     +0.0000000077
    690 0.0199413  0.0077488  0.000000    0.000000894 0.000000128  0.00000000043   +0.000000335  +0.0000000030    +0.0000000016
    700 0.00957688 0.00371774 0.000000    0.000000366 0.000000052  0.00000000016   +0.000000137  +0.00000000088   +0.00000000049
    710 0.00455263 0.00176847 0.000000    0.000000114 0.000000016  0.000000000039  +0.000000042  +0.00000000012   +0.000000000086
    720 0.00217496 0.00084619 0.000000    0.000000019 0.0000000026 0.0000000000043 +0.0000000069 +0.0000000000027 +0.0000000000051
'''[1:-1]

data3 = []
for line in table3_data.split("\n"):
    f = [flt(i) for i in line.split()]
    f[0] = int(f[0])
    data3.append(tuple(f))
data3 = tuple(data3)

#----------------------------------------------------------------------------
# Table 4 in Nimeroff, pg 483
# Within-observer variances in xbar, ybar, zbar.  These are about 32 times
# smaller than those in table 3.
# v(x) = variance of xbar
# v(y) = variance of ybar
# v(z) = variance of zbar
table4_data = '''
    400 0.00000390     0.0000000364    0.0000788
    410 0.0000204      0.000000338     0.000407
    420 0.0000288      0.000000806     0.000595
    430 0.0000227      0.00000207      0.000475
    440 0.0000119      0.00000138      0.000301
    450 0.0000109      0.00000173      0.000251
    460 0.0000337      0.00000306      0.000635
    470 0.0000340      0.00000837      0.000556
    480 0.0000220      0.0000185       0.000187
    490 0.0000208      0.0000322       0.0000720
    500 0.0000128      0.0000396       0.0000183
    510 0.0000100      0.0000255       0.00000587
    520 0.00000562     0.0000141       0.00000200
    530 0.00000440     0.00000779      0.000000834
    540 0.0000192      0.0000182       0.00000133
    550 0.0000441      0.0000206       0.00000324
    560 0.0000871      0.0000261       0.00000309
    570 0.000135       0.0000307       0.00000290
    580 0.000172       0.0000347       0.00000240
    590 0.000181       0.0000292       0.00000201
    600 0.000152       0.0000225       0.00000117
    610 0.0000999      0.0000146       0.000000764
    620 0.0000489      0.00000740      0.000000380
    630 0.0000177      0.00000283      0.000000181
    640 0.00000231     0.000000391     0.00000000862
    650 0.00000145     0.000000245     0.00000000154
    660 0.00000141     0.000000220     0.00000000132
    670 0.000000398    0.0000000591    0.000000000493
    680 0.000000131    0.0000000191    0.0000000000524
    690 0.0000000275   0.00000000394   0.0000000000132
    700 0.0000000113   0.00000000160   0.00000000000493
    710 0.00000000351  0.000000000493  0.00000000000120
    720 0.000000000585 0.0000000000801 0.000000000000132
'''[1:-1]

data4 = []
for line in table4_data.split("\n"):
    f = [flt(i) for i in line.split()]
    f[0] = int(f[0])
    data4.append(tuple(f))
data4 = tuple(data4)

if __name__ == "__main__": 
    # When run as a script, this prints out the data in a more digestible
    # form.  
    from clr import Clr
    from rgb import ColorNum
    from fpformat import FPFormat
    c = Clr(always=True)
    c.r, c.g, c.b = c("lred"), c("lgrn"), c("lblu")
    FP = True
    if FP:
        # Use FPFormat for formatting to line up decimal places
        N, M = 4, 2
        fp = FPFormat(num_digits=N)
        fp2 = FPFormat(num_digits=M)
    def wl2rgb(nm, gamma=0.8):
        '''Convert nm (light wavelength in nm) into a ColorNum object using a
        linear approximation.  The ColorNum object represents an RGB color.
        gamma is used for a gamma adjustment.  nm must be on [380, 780].
        '''
        # Translation of Dan Bruton's FORTRAN code from
        # http://www.physics.sfasu.edu/astro/color/spectra.html into python.
        # Also see http://www.midnightkite.com/color.html.
        if 380 <= nm <= 440:
            a = (440 - nm)/(440 - 380), 0, 1
        elif 440 <= nm <= 490:
            a = 0, (nm - 440)/(490 - 440), 1
        elif 490 <= nm <= 510:
            a = 0, 1, (510 - nm)/(510 - 490)
        elif 510 <= nm <= 580:
            a = (nm - 510)/(580 - 510), 1, 0
        elif 580 <= nm <= 645:
            a = 1, (645 - nm)/(645 - 580), 0
        elif 645 <= nm <= 780:
            a = 1, 0, 0
        else:
            raise ValueError(f"Wavelength {nm} is not in [380, 780] nm")
        if gamma < 0:
            raise ValueError(f"gamma must be >= 0")
        # Intensity i falls off near vision limits
        i, u, v = 1, 0.3, 0.7
        if nm > 700:
            i = u + v*(780 - nm)/(780 - 700)
        elif nm < 420:
            i = u + v*(nm - 380)/(420 - 380)
        # Scale the RGB components by i and raise to the gamma power if gamma
        # is nonzero.
        if gamma:
            b = [float((i*j)**gamma) for j in a]
        else:
            b = [float(i) for i in a]
        # Make sure the numbers are on [0, 1]
        assert(all([0 <= i <=1 for i in b]))
        return ColorNum(b)
    def SummarizeTable3():
        def SummarizeTable3Line(line):
            def S(variance, mean):
                if mean:
                    return 100*variance**(1/2)/mean
                else:
                    return flt(0)
            assert(len(line) == 10)
            (  λ,
            x, y, z,
            vx, vy, vz,
            cxy, cxz, cyz) = line
            m = x, y, z
            v = vx, vy, vz
            C = cxy, cxz, cyz
            cn = wl2rgb(λ)
            print(f" {c(cn.rgbhex)}{λ:3d}{c.n} ", end="")
            if FP:
                # Use fpformat printing to line up decimal points
                w = 10
                f = lambda x:  fp.dp(x, width=w)
                print(f"{c.r}{f(m[0]):{w}s}{c.n} ", end="")
                print(f"{c.g}{f(m[1]):{w}s}{c.n} ", end="")
                if m[2]:
                    print(f"{c.b}{f(m[2]):{w}s}{c.n} ", end="")
                else:
                    print(f"{c.b}{'   0':{w}s}{c.n} ", end="")
            else:
                # Use regular printing
                print(f"{c.r}{m[0]:10.3f}{c.n} ", end="")
                print(f"{c.g}{m[1]:10.3f}{c.n} ", end="")
                print(f"{c.b}{m[2]:10.3f}{c.n} ", end="")
            if not FP:
                print(" "*6, end="")
            # Standard deviation:  take square root of variance to get standard
            # deviation, print to 2 figures.
            s = [flt(i**(1/2)) for i in v]
            with flt(0):
                flt(0).n = 2
                if FP:
                    # Use fpformat printing to line up decimal points
                    def F(x):
                        try:
                            s = fp2.dp(x, width=w, dpoint=3)
                            if "-.-" in s:
                                return f"{x:{w}.2g}"
                            return s
                        except Exception:
                            return f"{x:{w}.2g}"
                    w = 9
                    print(f"{c.r}{F(s[0]):{w}s}{c.n} ", end="")
                    print(f"{c.g}{F(s[1]):{w}s}{c.n} ", end="")
                    print(f"{c.b}{F(s[2]):{w}s}{c.n} ", end="")
                else:
                    print(f"{c.r}{s[0]!s:^9s}{c.n} ", end="")
                    print(f"{c.g}{s[1]!s:^9s}{c.n} ", end="")
                    print(f"{c.b}{s[2]!s:^9s}{c.n} ", end="")
            print()
        msg1 = f"(to {N} figures)" if FP else ""
        msg2 = f"(to {M} figures)" if FP else ""
        print(dedent(f'''
        Table 3:  10° CIE Color Matching Functions
        From I. Nimeroff, J. Rosenblatt, M. Dannemiller, "Variability of
        Spectral Tristimulus Values", J. Res. NBS A, 65A(6) 475-483, 1961
        {c.r}x -> red   at 645.2 nm{c.n}
        {c.g}y -> green at 526.3 nm{c.n}
        {c.b}z -> blue  at 444.4 nm{c.n}
        xbar, ybar, zbar are mean CMFs {msg1}
        s = standard deviation in same units as mean {msg2}
        Nominal d.f. approximately 80
        '''))
        if FP:
            print(f"λ, nm   {c.r}xbar{c.n}       {c.g}ybar{c.n}       {c.b}zbar{c.n}        ", end="")
            print(f"{c.r}sx{c.n}        {c.g}sy{c.n}        {c.b}sz{c.n}")
        else:
            print(f"λ, nm     {c.r}xbar{c.n}       {c.g}ybar{c.n}       {c.b}zbar{c.n}           ", end="")
            print(f"{c.r}sx{c.n}       {c.g}sy{c.n}         {c.b}sz{c.n}")
        for line in data3:
            SummarizeTable3Line(line)
    def SummarizeTable4():
        print(dedent('''

        Within-observer standard deviations
        d.f. approximately 7
 
        '''))
        print(f"λ, nm", end=" "*5)
        w = 8
        i = " "*9
        print(f"{c.r}sx{c.n}{i}{c.g}sy{c.n}{i}{c.b}sz{c.n}")
        i = " "*2
        for line in data4:
            assert(len(line) == 4)
            λ, vx, vy, vz = line
            v = vx, vy, vz
            cn = wl2rgb(λ)
            s = [flt(i**(1/2)) for i in v]
            print(f" {c(cn.rgbhex)}{λ:3d}{c.n}  ", end="")
            print(f"{c.r}{s[0]:{w}.4f}{c.n} ", end=f"{i}")
            print(f"{c.g}{s[1]:{w}.4f}{c.n} ", end=f"{i}")
            print(f"{c.b}{s[2]:{w}.4f}{c.n} ")
    SummarizeTable3()
    SummarizeTable4()

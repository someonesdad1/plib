"""

ToDo:
    - Default units metric, -p for lbf
    - Samson 3/8" stable braid has min 4.8 klb breaking with a mean of 5.6
      klb, so mean is about 15% more than minimum.  Assuming a normal
      distribution with the minimum being minus three standard deviations,
      this means the standard deviation of the strength is about 5%.

---------------------------------------------------------------------------

Print rope data
"""

# ∞test∞# ignore #∞test∞#
if 1:  # Header
    # Standard imports
    import getopt
    import sys
    from fractions import Fraction
    from pprint import pprint as pp

    # Custom imports
    from wrap import dedent
    from f import flt
    from get import GetFraction
    from color import TRM as t
    from fraction import FormatFraction

    if 1:
        import debug

        debug.SetDebugger()
    # Global variables
    t.title = t("trq")
    t.d25 = t("purl")
    t.d38 = t("yell")
    t.d5 = t("magl")
    t.d75 = t("ornl")

    class G:
        pass

    g = G()
    g.mm_to_frac = {}
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [arg]
          If arg is empty, print strength data.  If arg is given, plot the
          rope strength as a function of nylon's strength.
        Options:
            -a      Show sizes over 1 inch diameter
            -f      Used fixed decimal point display
            -d      Number of digits in numbers [{d["-d"]}]
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Print all sizes
        d["-d"] = 3  # Number of digits in numbers
        d["-f"] = False  # Fixed decimal point display
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:fh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("af"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d["-d"] = n = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                    flt(0).N = n
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        return args


if 1:  # Samson data

    def GetSamsonData():
        """Return a list of
        (
            diameter_mm,
            mass_density_g_per_m,
            average_strength_N,
            minimum_strength_N
        )
        """
        # These are the data from the Samson website
        dia_in = """1/4 5/16 3/8 7/16 1/2 9/16 5/8 3/4 7/8 1 1-1/8 1-1/4 1-5/16
                    1-1/2 1-5/8 1-3/4 2 2-1/8 2-1/4 2-1/2 2-5/8 2-3/4 3 3-1/4
                    3-5/8 4 4-1/4 4-5/8 5""".split()
        wt_100_ft_lb = """2.1 3.2 4.5 6.1 8.2 11 14 18 27.1 34 45.3 53.9 60.8 73.3
                       85.9 104 124 147 173 196 225 246 300 375 450 525 589 689
                       788""".split()
        strength_avg_klb = """2.3 3.6 5.6 7.7 10.4 13.3 16.3 20.4 29.9 39.2 48.2
                              57.3 64.7 75.1 87.2 104 124 145 166 190 212 234
                              278 343 407 470 533 616 698""".split()
        strength_min_klb = """2 3.1 4.8 6.5 8.8 11.3 13.9 17.3 25.4 33.3 41 48.7 55
                              63.8 74.1 88.4 105 123 141 162 180 199 236 292
                              346 400 453 524 593""".split()
        # Get diameter in mm
        dia_mm = []
        for i in dia_in:
            f = GetFraction(i)
            mm = flt(round(f.numerator / f.denominator * 25.4, 4))
            dia_mm.append(mm)
            g.mm_to_frac[mm] = FormatFraction(f, unicode=False)
        # Get linear mass density in g/m
        g_per_m = []
        for i in wt_100_ft_lb:
            c = flt(14.8816)  # Converts lbm/100 ft to g/m
            g_per_m.append(flt(round(float(i) * c, 2)))
        # Get average strength in N
        strength_avg_N = []
        for i in strength_avg_klb:
            c = flt(4448.22)  # Converts klbf to N
            strength_avg_N.append(flt(round(float(i) * c, 0)))
        # Get average strength in N
        strength_min_N = []
        for i in strength_min_klb:
            c = flt(4448.22)  # Converts klbf to N
            strength_min_N.append(flt(round(float(i) * c, 0)))
        data = list(zip(dia_mm, g_per_m, strength_avg_N, strength_min_N))
        return data

    def PrintSamsonTableMetric(data, all=False):
        """data is a list of (dia_mm, g_per_m, strength_avg_N,
        strength_min_N) entries.
        """
        if 1:  # Set up flt formatting
            x = flt(0)
            x.N = d["-d"]
            x.rtz = False
            x.rtdp = True
        n = len(data) if all else 10
        w = 7, 6, 8, 8, 10
        # Header
        print("Samson double-braided polyester rope breaking strengths")
        print(
            f"{'Diameter':^{w[0] + w[1] + 1}s} "
            f"{'Strength, kN':^{w[2] + w[3] + 1}s} "
            f"{'Mass':^{w[4]}s}"
        )
        print(
            f"{'in':^{w[0]}s} "
            f"{'mm':^{w[1]}s} "
            f"{'Min':^{w[2]}s} "
            f"{'Avg':^{w[3]}s} "
            f"{'g/m':^{w[4]}s}"
        )
        k = 2
        print(
            f"{'-' * (w[0] - k):^{w[0]}s} "
            f"{'-' * (w[1] - k):^{w[1]}s} "
            f"{'-' * (w[2] - k):^{w[2]}s} "
            f"{'-' * (w[3] - k):^{w[3]}s} "
            f"{'-' * (w[4] - k):^{w[4]}s}"
        )
        # Print rows
        for dia_mm, g_per_m, strength_avg_N, strength_min_N in data[:n]:
            if d["-f"]:  # Print with fixed decimal places
                print(
                    f"{g.mm_to_frac[dia_mm]:^{w[0]}s} "
                    f"{dia_mm:^{w[1]}.1f} "
                    f"{strength_min_N / 1000:^{w[2]}.1f} "
                    f"{strength_avg_N / 1000:^{w[3]}.1f} "
                    f"{g_per_m:^{w[4]}.1f}"
                )
            else:  # Print desired number of figures
                print(
                    f"{g.mm_to_frac[dia_mm]:^{w[0]}s} "
                    f"{dia_mm!s:^{w[1]}s} "
                    f"{strength_min_N / 1000!s:^{w[2]}s} "
                    f"{strength_avg_N / 1000!s:^{w[3]}s} "
                    f"{g_per_m / 1000!s:^{w[4]}s}"
                )
        print(
            dedent("""

            Minimum strength is about 15% below average.  If strength is
            assumed to be a normal distribution and the minimum is 3σ below 
            the mean, then the standard deviation is about 5% of the mean.
        """)
        )

    def PrintSamsonTablePounds(data, all=False):
        """data is a list of (dia_mm, g_per_m, strength_avg_N,
        strength_min_N) entries.
        """
        if 1:  # Set up flt formatting
            x = flt(0)
            x.N = d["-d"]
            x.rtz = False
            x.rtdp = True
        n = len(data) if all else 10
        w = 7, 6, 8, 8, 10
        # Header
        print("Samson double-braided polyester rope breaking strengths")
        print(
            f"{'Diameter':^{w[0] + w[1] + 1}s} "
            f"{'Strength, klbf':^{w[2] + w[3] + 1}s} "
            f"{'Mass':^{w[4]}s}"
        )
        print(
            f"{'in':^{w[0]}s} "
            f"{'mm':^{w[1]}s} "
            f"{'Min':^{w[2]}s} "
            f"{'Avg':^{w[3]}s} "
            f"{'lbm/100 ft':^{w[4]}s}"
        )
        k = 2
        print(
            f"{'-' * (w[0] - k):^{w[0]}s} "
            f"{'-' * (w[1] - k):^{w[1]}s} "
            f"{'-' * (w[2] - k):^{w[2]}s} "
            f"{'-' * (w[3] - k):^{w[3]}s} "
            f"{'-' * (w[4] - k):^{w[4]}s}"
        )
        # Print rows
        for dia_mm, g_per_m, strength_avg_N, strength_min_N in data[:n]:
            lb_per_100_ft = flt(0.0671969 * g_per_m)
            strength_avg_klbf = flt(strength_avg_N * 0.000224809)
            strength_min_klbf = flt(strength_min_N * 0.000224809)
            if d["-f"]:  # Print with fixed decimal places
                print(
                    f"{g.mm_to_frac[dia_mm]:^{w[0]}s} "
                    f"{dia_mm:^{w[1]}.1f} "
                    f"{strength_min_klbf:^{w[2]}.1f} "
                    f"{strength_avg_klbf:^{w[3]}.1f} "
                    f"{lb_per_100_ft:^{w[4]}.1f}"
                )
            else:  # Print desired number of figures
                print(
                    f"{g.mm_to_frac[dia_mm]:^{w[0]}s} "
                    f"{dia_mm!s:^{w[1]}s} "
                    f"{strength_min_klbf!s:^{w[2]}s} "
                    f"{strength_avg_klbf!s:^{w[3]}s} "
                    f"{lb_per_100_ft!s:^{w[4]}s}"
                )


if 1:  # Generic data

    def GetGenericData():
        # From U.S. Naval Institute and Wall Rope Works, Inc., NY
        # Breaking strength in klb
        data = [["Dia", "Manila", "Sisal", "Nylon", "Dacron", "PE", "PP", "PEst"]]
        other = [
            [0.188, 0.45, 0.36, 1, 0.85, 0.7, 0.8, 0.72],
            [0.25, 0.6, 0.48, 1.5, 1.38, 1.2, 1.2, 1.15],
            [0.312, 1, 0.8, 2.5, 2.15, 1.75, 2.1, 1.75],
            [0.375, 1.35, 1.08, 3.5, 3, 2.5, 3.1, 2.45],
            [0.438, 1.75, 1.4, 4.8, 4.5, 3.4, 3.7, 3.4],
            [0.5, 2.65, 2.12, 6.2, 5.5, 4.1, 4.2, 4.4],
            [0.562, 3.45, 2.76, 8.3, 7.3, 4.6, 5.1, 5.7],
            [0.625, 4.4, 3.52, 10.5, 9.5, 5.2, 5.8, 7.3],
            [0.75, 5.4, 4.32, 14, 12.5, 7.4, 8.2, 9.5],
            [0.875, 7.7, 5.7, 20, 17.5, 10.4, 11.5, 13.5],
            [1, 9, 7.2, 24, 20, 12.6, 14, 16.5],
        ]
        for item in other:
            # Convert to flt, make first element a Fraction
            item = [flt(i) for i in item]
            item[0] = Fraction(item[0]).limit_denominator(16)
            data.append(item)
        return data

    def PrintGenericTable(data):
        """This information was online at one time, but I cannot find a
        link for it anymore.  Wall Rope Works apparently has been defunct
        for a number of decades.
        """
        digits = 2
        if 1:  # Table in klbf
            print(f"Generic rope data breaking strength to {digits} digits")
            print(f"  Strength in klb and diameter in inches")
            print(f"  Source:  U.S. Naval Institute and Wall Rope Works, NY")
            print(f"  PE = polyethylene, PP = polypropylene, PEst = polyester")
            print()
            x = flt(0)
            with x:
                x.N = digits
                n, m, w = 8, 12, 6
                for i in range(m):
                    item = data[i]
                    if not i:
                        # Header row
                        for j in range(n):
                            k = 0 if j == n - 1 else 2
                            print(f"{item[j]:^{w}s}", end=" " * k)
                        print()
                        for j in range(n):
                            k = 0 if j == n - 1 else 2
                            print(f"{'-' * w:^{w}s}", end=" " * k)
                        print()
                    else:
                        out = [FormatFraction(item[0], unicode=False)]
                        out += [str(i) for i in item[1:]]
                        for i, x in enumerate(out):
                            print(f"{x:^{w}s}", end=" " * 2)
                        print()
        if 1:  # Table in kN
            print()
            print(f"Generic rope data breaking strength to {digits} digits")
            print(f"  Strength in kN and diameter in inches")
            print(f"  Source:  U.S. Naval Institute and Wall Rope Works, NY")
            print(f"  PE = polyethylene, PP = polypropylene, PEst = polyester")
            print()
            x = flt(0)
            with x:
                x.N = digits
                n, m, w = 8, 12, 6
                for i in range(m):
                    item = data[i]
                    if not i:
                        # Header row
                        for j in range(n):
                            k = 0 if j == n - 1 else 2
                            print(f"{item[j]:^{w}s}", end=" " * k)
                        print()
                        for j in range(n):
                            k = 0 if j == n - 1 else 2
                            print(f"{'-' * w:^{w}s}", end=" " * k)
                        print()
                    else:
                        out = [FormatFraction(item[0], unicode=False)]
                        # Convert klbf to kN by multiplying by 4.44822
                        out += [str(i * flt(4.44822)) for i in item[1:]]
                        for i, x in enumerate(out):
                            print(f"{x:^{w}s}", end=" " * 2)
                        print()

    def ChainData():
        """
        https://www.uscargocontrol.com/blogs/blog/working-load-limits-chain
        """
        data = [
            # Working load limit in klbf as function of grade & size
            ("Size", 30, 43, 80, 100),
            ("1/4", 1.3, 2.6, 3.5, 4.3),
            ("5/16", 1.9, 3.9, 4.5, 5.7),
            ("3/8", 2.65, 5.4, 7.1, 8.8),
            ("1/2", 4.5, 9.2, 12, 15),
            ("5/8", 6.9, 13, 18.1, 22.6),
        ]
        lbf_to_kN = flt(4.44822)
        w = 8
        # Pound data
        print(f"Working load limit in klbf for steel chain vs. grade")
        for i in data:
            if i[0] == "Size":
                print(
                    f"{i[0]:^{w}s} {i[1]:^{w}d} {i[2]:^{w}d} {i[3]:^{w}d} {i[4]:^{w}d}"
                )
            else:
                print(
                    f"{i[0]:^{w}s} "
                    f"{flt(i[1])!s:^{w}s} "
                    f"{flt(i[2])!s:^{w}s} "
                    f"{flt(i[3])!s:^{w}s} "
                    f"{flt(i[4])!s:^{w}s}"
                )
        print(
            dedent("""

        Grade 30:  economical, light duty
        Grade 43:  towing & logging duty
        Grade 80:  Heat-treated alloy chain for lifting
        Grade 100: Heat-treated alloy chain for lifting
        """)
        )
        # Metric data
        print(f"\nWorking load limit in kN for steel chain vs. grade")
        for i in data:
            if i[0] == "Size":
                print(
                    f"{i[0]:^{w}s} {i[1]:^{w}d} {i[2]:^{w}d} {i[3]:^{w}d} {i[4]:^{w}d}"
                )
            else:
                print(
                    f"{i[0]:^{w}s} "
                    f"{flt(i[1]) * lbf_to_kN!s:^{w}s} "
                    f"{flt(i[2]) * lbf_to_kN!s:^{w}s} "
                    f"{flt(i[3]) * lbf_to_kN!s:^{w}s} "
                    f"{flt(i[4]) * lbf_to_kN!s:^{w}s}"
                )

    def PlotData():
        """Fields are:
            Dia, inches
            Manila
            Sisal
            Nylon
            Dacron
            Polyethylene
            Polypropylene
            Polyester
        The numbers are breaking strength in klbf.
        """
        data = """
            0.188  0.45   0.36  1    0.85  0.7   0.8  0.72
            0.25   0.6    0.48  1.5  1.38  1.2   1.2  1.15
            0.312  1      0.8   2.5  2.15  1.75  2.1  1.75
            0.375  1.35   1.08  3.5  3     2.5   3.1  2.45
            0.412  1.75   1.4   4.8  4.5   3.4   3.7  3.4
            0.5    2.65   2.12  6.2  5.5   4.1   4.2  4.4
            0.562  3.45   2.76  8.3  7.3   4.6   5.1  5.7
            0.625  4.4    3.52  10.5 9.5   5.2   5.8  7.3
            0.75   5.4    4.32  14   12.5  7.4   8.2  9.5
            0.875  7.7    5.7   20   17.5  10.4  11.5 13.5
            1      9      7.2   24   20    12.6  14   16.5
        """
        dia, manila, sisal, nylon, dacron, polye, polyp, polyester = (
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        )
        o = []
        for line in data.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            d, m, s, n, da, pe, pp, py = [float(i) for i in line.split()]
            dia.append(d)
            manila.append(m)
            sisal.append(s)
            nylon.append(n)
            dacron.append(da)
            polye.append(pe)
            polyp.append(pp)
            polyester.append(py)
        from numpy import array
        from pylab import plot, show, grid, legend, clf
        from pylab import title, xlabel, ylabel, savefig

        dia = array(dia)
        manila = array(manila)
        sisal = array(sisal)
        nylon = array(nylon)
        dacron = array(dacron)
        polye = array(polye)
        polyp = array(polyp)
        polyester = array(polyester)
        # Plot breaking strengths
        plot(dia, nylon, ".-", label="Nylon")
        plot(dia, dacron, ".-", label="Dacron")
        plot(dia, polyester, ".-", label="Polyester")
        plot(dia, polyp, ".-", label="Polypropylene")
        plot(dia, polye, ".-", label="Polyethylene")
        plot(dia, manila, ".-", label="Manila")
        plot(dia, sisal, ".-", label="Sisal")
        title("Rope Breaking Strengths")
        xlabel("Diameter, inches")
        ylabel("Breaking strength, klbf")
        grid()
        legend()
        showme = 0
        if showme:
            show()
        else:
            savefig("rope_strength.png")
        # Plot breaking strengths relative to nylon
        clf()
        plot(dia, dacron / nylon, ".-", label="Dacron")
        plot(dia, polyester / nylon, ".-", label="Polyester")
        plot(dia, polyp / nylon, ".-", label="Polypropylene")
        plot(dia, polye / nylon, ".-", label="Polyethylene")
        plot(dia, manila / nylon, ".-", label="Manila")
        plot(dia, sisal / nylon, ".-", label="Sisal")
        title("Rope Breaking Strengths Relative to Nylon")
        xlabel("Diameter, inches")
        ylabel("Relative breaking strength")
        grid()
        legend()
        if showme:
            show()
        else:
            savefig("rope_str_rel_nylon.png")

    def PrintTypeTable():
        """These data came from
        https://atlanticbraids.com/double-braid-versus-3-strand-twisted-rope/
        """
        w = 8
        print(
            dedent(f"""
        Minimum tensile strength ratio for db/3str where db means double
        braided rope and 3str means three-strand:
                       Nylon              Polyester
            1/4"        {flt(21 / 17)!s:{w}s}            {flt(24 / 11.2)!s:{w}s}
            1/2"        {flt(83 / 59.5)!s:{w}s}            {flt(90 / 36.5)!s:{w}s}
            1"          {flt(31 / 22)!s:{w}s}            {flt(34 / 12.6)!s:{w}s}
            2"          {flt(118 / 81.4)!s:{w}s}            {flt(106 / 48.6)!s:{w}s}
        """)
        )

    def Notes():
        print(
            dedent(f"""
        Notes:
            - Published rope tensile strength data easily varies by 20% or
              more and the typical web author doesn't 1) attribute their data
              nor 2) specify the manufacturer/material/construction.  
            - Most web pages are written by amateurs who do not have a
              technical background, so vet their data carefully (or,
              better, don't use it).
        """)
        )


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if args:
        PlotData()
    else:
        data = GetGenericData()
        PrintGenericTable(data)
        print()
        PrintTypeTable()
        print()
        Notes()
        print()
        ChainData()
        print()
        data = GetSamsonData()
        PrintSamsonTablePounds(data, all=d["-a"])
        print()
        PrintSamsonTableMetric(data, all=d["-a"])

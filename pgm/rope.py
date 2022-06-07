'''
Print table of strength of Samson double braid polyester rope
'''
#∞test∞# ignore #∞test∞#
if 1:   # Header
    # Standard imports
        import sys
        from fractions import Fraction
    # Custom imports
        from wrap import dedent
        from f import flt
        from get import GetFraction
        from color import TRM as t
    # Global variables
        t.title = t("yel")
        t.d25 = t("pnk")
        t.d38 = t("grn")
        t.d5 = t("yel")
        t.d75 = t("mag")
if 1:   # Samson data
    def GetSamsonData(metric=False, use_fractions=False, all=False):
        '''Return a list of 
        [
            diameter_inches,
            mass_lbm_per_100_feet,
            average_strength_klb,
            minimum_strength_klb
        ]
        If use_fractions is True, the diameter_inches will be a fraction.
        Otherwise, it will be a floating point number rounded to two decimal
        places.
        
        If metric is True, return the list
        [
            diameter_mm,
            weight_lb_per_100_feet,
            mass_kg_per_100_m,
            average_strength_kN,
            minimum_strength_kN
        ]
     
        If all is True, return all the sizes; otherwise, just return sizes up
        to 1 inch diameter.
        '''
        dia_in = '''1/4 5/16 3/8 7/16 1/2 9/16 5/8 3/4 7/8 1 1-1/8 1-1/4 1-5/16
                    1-1/2 1-5/8 1-3/4 2 2-1/8 2-1/4 2-1/2 2-5/8 2-3/4 3 3-1/4
                    3-5/8 4 4-1/4 4-5/8 5'''.split()
        wt_100_ft_lb = '''2.1 3.2 4.5 6.1 8.2 11 14 18 27.1 34 45.3 53.9 60.8 73.3
                       85.9 104 124 147 173 196 225 246 300 375 450 525 589 689
                       788'''.split()
        strength_avg_klb = '''2.3 3.6 5.6 7.7 10.4 13.3 16.3 20.4 29.9 39.2 48.2
                              57.3 64.7 75.1 87.2 104 124 145 166 190 212 234
                              278 343 407 470 533 616 698'''.split()
        strength_min_klb = '''2 3.1 4.8 6.5 8.8 11.3 13.9 17.3 25.4 33.3 41 48.7 55
                              63.8 74.1 88.4 105 123 141 162 180 199 236 292
                              346 400 453 524 593'''.split()
        if not all:
            n = 10
            dia_in = dia_in[:n]
            wt_100_ft_lb = [flt(i) for i in wt_100_ft_lb[:n]]
            strength_avg_klb = [flt(i) for i in strength_avg_klb[:n]]
            strength_min_klb = [flt(i) for i in strength_min_klb[:n]]
        data = list(zip(dia_in, wt_100_ft_lb, strength_avg_klb, strength_min_klb))
        # Convert first term to a fraction
        for i, item in enumerate(data):
            item = list(item)
            a = item[0]
            item[0] = GetFraction(a)
            if item[0] is None:
                item[0] = Fraction(int(a), 1)
            for j in range(1, 4):
                item[j] = flt(item[j])
            data[i] = item
        flt(0).rtz = flt(0).rtdp = True
        # Convert first element to decimal inches if wanted
        if not use_fractions:
            for i in range(len(data)):
                data[i][0] = flt(round(data[i][0], 2))
        # Convert to metric if wanted
        if metric:
            for i in range(len(data)):
                data[i][0] = flt(round(float(data[i][0])*25.4, 1))
                data[i][1] = flt(round(float(data[i][1])*0.453592, 2))
                data[i][2] = flt(round(float(data[i][2])*4.44822, 2))
                data[i][3] = flt(round(float(data[i][3])*4.44822, 2))
        return data
    def PrintSamsonTable(data):
        lbf2N = 4.44822
        lb2kg = 0.453592
        data = GetSamsonData(use_fractions=True)
        t.print(f"{t.title}Samson double-braided polyester rope")
        print(dedent('''
                      Linear mass density
          Diameter      per 100 ft or m      Minimum breaking strength
        inch     mm       lb      kg            klbf   kN    kgf
        -----------     -----   -----           ----  ----  -----'''))
        for line in data:
            dia, wt, avg, min = line
            di = flt(dia)    # Diameter in inches
            # Diameter
            Di = FormatFraction(dia)
            dm = di*25.4
            with dm:
                dm.n = 2
                Dm = f"{dm}"
            c = ""  # Color for most-used
            if Di == "1/4":
                c = t.d25
            elif Di == "3/8":
                c = t.d38
            elif Di == "1/2":
                c = t.d5
            elif Di == "3/4":
                c = t.d75
            print(f"{c}{Di:^5s} {Dm:>5s}", end=" "*4)
            # Linear mass density
            si = wt
            sm = wt*lb2kg
            w = 6
            print(f" {si!s:^{w}s}  {sm!s:^{w}s}", end=" "*10)
            # Minimum breaking strength
            bi = min
            bm = bi*lbf2N
            bk = bi*lb2kg
            w = 5
            print(f"{bi!s:^{w}s} {bm!s:^{w}s} {bk!s:^{w}s}{t.n if c else ''}")
    def FormatFraction(x):
        assert(x <= 1)
        return "1" if x == 1 else f"{x.numerator}/{x.denominator}"
if 1:   # Generic data
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
        t.print(f"{t.title}Generic rope data breaking strength")
        print(f"  Strength in klb and diameter in inches")
        print(f"  Source:  U.S. Naval Institute and Wall Rope Works, NY")
        print(f"  PE = polyethylene, PP = polypropylene, PEst = polyester")
        print()
        x = flt(0)
        with x:
            x.n = 2
            n, m, w = 8, 12, 6
            for i in range(m):
                item = data[i]
                if not i:
                    # Header row
                    for j in range(n):
                        k = 0 if j == n - 1 else 2
                        print(f"{item[j]:^{w}s}", end=" "*k)
                    print()
                    for j in range(n):
                        k = 0 if j == n - 1 else 2
                        print(f"{'-'*w:^{w}s}", end=" "*k)
                    print()
                else:
                    out = [FormatFraction(item[0])]
                    Di = out[0]
                    out += [str(i) for i in item[1:]]
                    for i, x in enumerate(out):
                        c = ""  # Color for most-used
                        if Di == "1/4":
                            c = t.d25
                        elif Di == "3/8":
                            c = t.d38
                        elif Di == "1/2":
                            c = t.d5
                        elif Di == "3/4":
                            c = t.d75
                        print(f"{c}{x:^{w}s}", end=" "*2)
                    print(f"{t.n if c else ''}")

if __name__ == "__main__": 
    data = GetSamsonData(use_fractions=True)
    PrintSamsonTable(data)
    print()
    data = GetGenericData()
    PrintGenericTable(data)
# vim: tw=83

'''

TODO
    - Make -t give table showing factor back in time.  For example, the
      entry X under 1960 would show how many 2022 dollars are equal to $1 in
      1960.  Then the interpretation is that $1 in 1960 was X times more
      valuable than it is today.  Make the current -t table shown under -T.
    - In table, remove $ and leading 0.  Show year in color.

Consumer price index utility.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Consumer price index utility
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import os
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import dedent
        from f import flt
        from columnize import Columnize
        from color import t
    if 1:   # Global variables
        # The following CPI data came from the cpi_data.py script.
        CPI = {
            2023: flt(304.7),   2000: flt(172.2),   1978: flt(65.2),    1956: flt(27.2),    1934: flt(13.4),
            2022: flt(292.7),   1999: flt(166.6),   1977: flt(60.6),    1955: flt(26.8),    1933: flt(13),
            2021: flt(271),     1998: flt(163),     1976: flt(56.9),    1954: flt(26.9),    1932: flt(13.7),
            2020: flt(258.8),   1997: flt(160.5),   1975: flt(53.8),    1953: flt(26.7),    1931: flt(15.2),
            2019: flt(255.7),   1996: flt(156.9),   1974: flt(49.3),    1952: flt(26.5),    1930: flt(16.7),
            2018: flt(251.1),   1995: flt(152.4),   1973: flt(44.4),    1951: flt(26),      1929: flt(17.1),
            2017: flt(245.1),   1994: flt(148.2),   1972: flt(41.8),    1950: flt(24.1),    1928: flt(17.1),
            2016: flt(240),     1993: flt(144.5),   1971: flt(40.5),    1949: flt(23.8),    1927: flt(17.4),
            2015: flt(237),     1992: flt(140.3),   1970: flt(38.8),    1948: flt(24.1),    1926: flt(17.7),
            2014: flt(236.7),   1991: flt(136.2),   1969: flt(36.7),    1947: flt(22.3),    1925: flt(17.5),
            2013: flt(233),     1990: flt(130.7),   1968: flt(34.8),    1946: flt(19.5),    1924: flt(17.1),
            2012: flt(229.6),   1989: flt(124),     1967: flt(33.4),    1945: flt(18),      1923: flt(17.1),
            2011: flt(224.9),   1988: flt(118.3),   1966: flt(32.4),    1944: flt(17.6),    1922: flt(16.8),
            2010: flt(218.1),   1987: flt(113.6),   1965: flt(31.5),    1943: flt(17.3),    1921: flt(17.9),
            2009: flt(214.5),   1986: flt(109.6),   1964: flt(31),      1942: flt(16.3),    1920: flt(20),
            2008: flt(215.3),   1985: flt(107.6),   1963: flt(30.6),    1941: flt(14.7),    1919: flt(17.3),
            2007: flt(207.3),   1984: flt(103.9),   1962: flt(30.2),    1940: flt(14),      1918: flt(15.1),
            2006: flt(201.6),   1983: flt(99.6),    1961: flt(29.9),    1939: flt(13.9),    1917: flt(12.8),
            2005: flt(195.3),   1982: flt(96.5),    1960: flt(29.6),    1938: flt(14.1),    1916: flt(10.9),
            2004: flt(188.9),   1981: flt(90.9),    1959: flt(29.1),    1937: flt(14.4),    1915: flt(10.1),
            2003: flt(184),     1980: flt(82.4),    1958: flt(28.9),    1936: flt(13.9),    1914: flt(10),
            2002: flt(179.9),   1979: flt(72.6),    1957: flt(28.1),    1935: flt(13.7),    1913: flt(9.9),
            2001: flt(177.1),
        }
        ref_year = max(CPI)
        min_year = min(CPI)
        min_digits, max_digits = 1, 8
        t.ref = t("ornl")
if 1:  # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        In 1970 I lived with 2 friends in an apartment.  We ate relatively simply and found we
        could be comfortable on $5 per week for food.  What is that equivalent to in 2023 costs?
            arguments:  '1970 5'
        Results show this was 53 years before and $5 in 1970 is equivalent to $39.3 in 2023.

        Tables:  The argument '-t' produces the table

            A cost of 1 in 2023 is equivalent to about how much in other years?
            1913   0.0325      1941   0.0482      1969   0.12        1997   0.527
            1914   0.0328      1942   0.0535      1970   0.127       1998   0.535
            1915   0.0331      1943   0.0568      1971   0.133       1999   0.547
            ...
            1938   0.0463      1966   0.106       1994   0.486       2022   0.961
            1939   0.0456      1967   0.11        1995    0.5        2023     1
            1940   0.0459      1968   0.114       1996   0.515

        Thus, $1 in 2023 buys something that would have cost about 5 cents during World War 2.

        The argument '-T' produces the table

            A cost of 1 in 2023 is equivalent to about how much in other years?
            1913   30.8       1941   20.7       1969    8.3       1997    1.9
            1914   30.5       1942   18.7       1970   7.85       1998   1.87
            1915   30.2       1943   17.6       1971   7.52       1999   1.83
            ...
            1938   21.6       1966    9.4       1994   2.06       2022   1.04
            1939   21.9       1967   9.12       1995     2        2023     1
            1940   21.8       1968   8.76       1996   1.94

        These entries are the reciprocals of the -t argument.  The 1941/1942 years show that
        things were about 20 times cheaper in WW2 than in 2023.

        The -y option lets you change the reference year.  Let's use 1970 as the reference year to
        get with '-t -y 1970'

            A cost of 1 in 1970 is equivalent to about how much in other years?
            1913   0.255      1941   0.379      1969   0.946      1997   4.14
            1914   0.258      1942   0.42       1970     1        1998    4.2
            1915   0.26       1943   0.446      1971   1.04       1999   4.29
            1916   0.281      1944   0.454      1972   1.08       2000   4.44
            1917   0.33       1945   0.464      1973   1.14       2001   4.56
            1918   0.389      1946   0.503      1974   1.27       2002   4.64
            1919   0.446      1947   0.575      1975   1.39       2003   4.74
            1920   0.515      1948   0.621      1976   1.47       2004   4.87
            1921   0.461      1949   0.613      1977   1.56       2005   5.03
            1922   0.433      1950   0.621      1978   1.68       2006    5.2
            1923   0.441      1951   0.67       1979   1.87       2007   5.34
            1924   0.441      1952   0.683      1980   2.12       2008   5.55
            1925   0.451      1953   0.688      1981   2.34       2009   5.53
            1926   0.456      1954   0.693      1982   2.49       2010   5.62
            1927   0.448      1955   0.691      1983   2.57       2011    5.8
            1928   0.441      1956   0.701      1984   2.68       2012   5.92
            1929   0.441      1957   0.724      1985   2.77       2013   6.01
            1930   0.43       1958   0.745      1986   2.82       2014    6.1
            1931   0.392      1959   0.75       1987   2.93       2015   6.11
            1932   0.353      1960   0.763      1988   3.05       2016   6.19
            1933   0.335      1961   0.771      1989    3.2       2017   6.32
            1934   0.345      1962   0.778      1990   3.37       2018   6.47
            1935   0.353      1963   0.789      1991   3.51       2019   6.59
            1936   0.358      1964   0.799      1992   3.62       2020   6.67
            1937   0.371      1965   0.812      1993   3.72       2021   6.98
            1938   0.363      1966   0.835      1994   3.82       2022   7.54
            1939   0.358      1967   0.861      1995   3.93       2023   7.85
            1940   0.361      1968   0.897      1996   4.04

        Thus, WW2 costs were about 1/3 of 1970's, which 2023's costs are nearly 8 times as much.
        '''))
        exit(0)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] yr [amount1 amount2 ...]
          Print approximately what something cost in year yr compared to
          today ({ref_year}).  If amounts are included, they are scaled to
          both years.  Based on the consumer price index.
        Options:
          -d n      Set the number of significant digits.  [{d["-d"]}]
          -h        Print a manpage
          -T        Print a CPI table relative to the reference year, but the shown
                    numbers are the inverse of the -t output
          -t        Print a CPI table relative to the reference year
          -y yr     Define the reference year.  [{ref_year}]
        Examples:
          '-t -y 2018'
            Shows a table of 
                
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of significant digits
        d["-p"] = False     # If True, plot the data
        d["-r"] = 1         # Reference amount
        d["-T"] = False     # If True, print inverse table
        d["-t"] = False     # If True, print table
        d["-y"] = ref_year  # Today reference year
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hpr:Tty:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "pTt":
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (min_digits <= d[o] <= max_digits):
                        raise ValueError()
                except ValueError:
                    Error("-d option's argument must be an integer between "
                        f"{min_digits} and {max_digits}")
            elif o == "-h":
                Manpage()
            elif o == "-r":
                d[o] = flt(a)
                if d[o] <= 0:
                    Error("-r option's argument must be > 0")
            elif o == "-y":
                d["-y"] = GetYear(a)
        if d["-p"]:
            PlotTable(args, d)
        elif d["-t"] or d["-T"]:
            PrintTable(args, d)
        if not args:
            Usage(d)
        flt(0).N = d["-d"]
        return args
if 1:  # Core functionality
    def GetYear(s):
        try:
            y = int(s)
            if not (min_year <= y <= ref_year):
                raise ValueError()
            return y
        except ValueError:
            msg = f"A year must be between {min_year} and {ref_year}"
            Error(msg)
    def PlotTable(args, d):
        from pylab import plot, show, grid, title, xlabel, ylabel, text
        years, cpi = CPI.keys(), CPI.values()
        ref_year = years[-1]
        if args:
            # First item is reference year
            ref_year = GetYear(args[0])
        ref_cpi = CPI[ref_year]
        cpi_rel = [i/ref_cpi for i in cpi]
        plot(years, cpi_rel)
        grid()
        title("Relative US Consumer Price Index 1913-2021\n"
            "(Relative to {}, CPI = {})".format(ref_year, round(ref_cpi, 2)))
        xlabel("Year")
        ylabel("Consumer Price Index")
        show()
    def PrintTable(args, d):
        ref_year = d["-y"]
        ref_amt = d["-r"]
        print(f"A cost of {ref_amt} in {t.ref}{ref_year}{t.n} is equivalent to about how much in other years?")
        ref_cpi = CPI[ref_year]
        ref_cpi.N = d["-d"]
        out = []
        w = d["-d"] + 2
        for yr, cpi in sorted(CPI.items()):
            c = t.ref if yr == ref_year else ""
            e = t.n if yr == ref_year else ""
            x = ref_amt*cpi/ref_cpi
            if d["-T"]:
                x = 1/x
            out.append(f"{c}{yr}   {x!s:^{w}s}{e}")
        for i in Columnize(out, columns=4, sep=" "*6):
            print(i)
        exit(0)
    def rdp(x):
        '''If x is a flt with str interpolation with a trailing decimal point,
        remove the decimal point.
        '''
        s = str(x)
        if s[-1] == ".":
            return s[:-1]
        return s

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    ref_year = d["-y"]
    # Print percentages
    year = GetYear(args[0])
    cpi, ref_cpi = CPI[year], CPI[ref_year]
    print("Year = {}, reference year = {}, difference = {} years".format(
          year, ref_year, abs(year - ref_year)))
    ratio = ref_cpi/cpi
    print(f"Ratio for year/ref = {ratio}") 
    print(f"Ratio for ref/year = {1/ratio}")
    if len(args) > 1:
        s = "Amounts" if len(args[1:]) > 1 else "Amount"
        a = f"in {year}"
        b = f"in {ref_year}"
        m, n = 12, 20
        print(f"{s:^{m}s}   {a:^{n}s}   {b:^{n}s}")
        print(f"{'-'*m:^{m}s}   {'-'*n:^{n}s}   {'-'*n:^{n}s}")
        for x in [float(j) for j in args[1:]]:
            a = f"${rdp(x*ratio)} in {ref_year}"
            b = f"${rdp(x/ratio)} in {year}"
            print(f"{rdp(x):^{m}s}   {a:^{n}s}   {b:^{n}s}")

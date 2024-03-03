'''

TODO
    - Make -t give table showing factor back in time.  For example, the
      entry X under 1960 would show how many 2022 dollars are equal to $1 in
      1960.  Then the interpretation is that $1 in 1960 was X times more
      valuable than it is today.  Make the current -t table shown under -T.
    - In table, remove $ and leading 0.  Show year in color.

Consumer price index utility.
'''
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
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] yr [amount1 amount2 ...]
      Print approximately what something cost in year yr compared to
      today ({ref_year}).  If amounts are included, they are scaled to
      both years.  Based on the consumer price index.
    Options:
      -d n      Set the number of significant digits.  [{d["-d"]}]
      -t        Print a CPI table relative to the reference year
      -y yr     Define the reference year.  [{ref_year}]
    '''))
    exit(status)
def GetYear(s):
    try:
        y = int(s)
        if not (min_year <= y <= ref_year):
            raise ValueError()
        return y
    except ValueError:
        msg = f"A year must be between {min_year} and {ref_year}"
        Error(msg)
def ParseCommandLine(d):
    d["-d"] = 3         # Number of significant digits
    d["-p"] = False     # If True, plot the data
    d["-r"] = 1         # Reference amount
    d["-t"] = False     # If True, print table
    d["-y"] = ref_year  # Today reference year
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:pr:ty:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "pt":
            d[o] = not d[o]
        elif o == "-d":
            try:
                d[o] = int(a)
                if not (min_digits <= d[o] <= max_digits):
                    raise ValueError()
            except ValueError:
                Error("-d option's argument must be an integer between "
                      f"{min_digits} and {max_digits}")
        elif o == "-r":
            d[o] = flt(a)
            if d[o] <= 0:
                Error("-r option's argument must be > 0")
        elif o == "-y":
            d["-y"] = GetYear(a)
    if d["-p"]:
        PlotTable(args, d)
    elif d["-t"]:
        PrintTable(args, d)
    if not args:
        Usage(d)
    flt(0).N = d["-d"]
    return args
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
        out.append(f"{c}{yr}   {(ref_amt*cpi/ref_cpi)!s:^{w}s}{e}")
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

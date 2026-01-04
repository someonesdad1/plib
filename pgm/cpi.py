'''

TODO
    - Make -t give table showing factor back in time.  For example, the
      entry X under 1960 would show how many 2022 dollars are equal to $1 in
      1960.  Then the interpretation is that $1 in 1960 was X times more
      valuable than it is today.  Make the current -t table shown under -T.
    - In table, remove $ and leading 0.  Show year in color.
    
Consumer price index utility
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Consumer price index utility
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import getopt
        import os
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from f import flt
        from columnize import Columnize
        from color import t
        from months import months
    if 1:  # Global variables
        # The needed inflation information is in the CPI dictionary, which maps integer
        # year to CPI values.
        from cpi_data import cpi_data as CPI
        # Get some summary statistics
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
        In 1970, 3 friends lived in an apartment.  They ate simply and found they could
        be comfortable on $5 per week for food.  What is that equivalent to in 2025
        dollars?  Run the script with arguments:  '1970 5'.  The results are

            Year = 1970, reference year = 2025, difference = 55 years
            Ratio for year/ref = 8.3
            Ratio for ref/year = 0.121
            Amount            in 1970                in 2025       
            ------------   --------------------   --------------------
                $5.0          $41.5 in 2025          $0.603 in 1970   
        
        Is this projection reasonable?  Could three people living in an apartment in
        2025 live comfortably on about $160 per month per person for food?  I'd answer a
        tentative yes, but you'd be on a budget, wouldn't eat in restaurants at all, and 
        you'd be buying mostly inexpensive foods.  

        The script uses the US consumer price index numbers to scale a cost from one
        year to another.  It's only relevant to the US and it's the usual bureaucratic
        mess with changes in definitions over time and politicians wanting to make it
        favor their own agenda.
        '''))
        exit(0)
    def Usage(d, status=0):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] Y [amount1 amount2 ...]
          Print approximately what something cost in year Y compared to today
          ({ref_year}).  If amounts are included, they are scaled to both years.  Based
          on the consumer price index.
        Options:
          -d n      Set the number of significant digits.  [{d["-d"]}]
          -h        Print a manpage
          -m        Show minimum wage changes in decimal years
          -T        Print a CPI table relative to the reference year, but the shown
                    numbers are the inverse of the -t output
          -t        Print a CPI table relative to the reference year
          -y yr     Define the reference year.  [{ref_year}]
        Examples:
          '-t -y 1970'
            Shows a table of how a unit cost of 1 in 1970 compares to other years.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3  # Number of significant digits
        d["-p"] = False  # If True, plot the data
        d["-r"] = 1  # Reference amount
        d["-T"] = False  # If True, print inverse table
        d["-t"] = False  # If True, print table
        d["-y"] = ref_year  # Today reference year
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hmpr:Tty:")
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
                    Error(
                        "-d option's argument must be an integer between "
                        f"{min_digits} and {max_digits}"
                    )
            elif o == "-h":
                Manpage()
            elif o == "-m":
                MinimumWage()
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
        cpi_rel = [i / ref_cpi for i in cpi]
        plot(years, cpi_rel)
        grid()
        title(
            "Relative US Consumer Price Index 1913-2021\n"
            "(Relative to {}, CPI = {})".format(ref_year, round(ref_cpi, 2))
        )
        xlabel("Year")
        ylabel("Consumer Price Index")
        show()
    def PrintTable(args, d):
        ref_year = d["-y"]
        ref_amt = d["-r"]
        print(
            f"A cost of {ref_amt} in {t.ref}{ref_year}{t.n} is equivalent to about how much in other years?"
        )
        ref_cpi = CPI[ref_year]
        ref_cpi.N = d["-d"]
        out = []
        w = d["-d"] + 2
        for yr, cpi in sorted(CPI.items()):
            c = t.ref if yr == ref_year else ""
            e = t.n if yr == ref_year else ""
            x = ref_amt * cpi / ref_cpi
            if d["-T"]:
                x = 1 / x
            out.append(f"{c}{yr}   {x!s:^{w}s}{e}")
        for i in Columnize(out, columns=4, sep=" " * 6):
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
    def MinimumWage():
        '''Print minimum wage table.  Data from
        https://www.dol.gov/agencies/whd/minimum-wage/history/chart
        '''
        data = '''
            Oct 24, 1938 $0.25  
            Oct 24, 1939 $0.30  
            Oct 24, 1945 $0.40  
            Jan 25, 1950 $0.75  
            Mar 1, 1956 $1.00  
            Sep 3, 1961 $1.15
            Sep 3, 1963 $1.25  
            Sep 3, 1964  $1.15 
            Sep 3, 1965  $1.25 
            Feb 1, 1967 $1.40
            Feb 1, 1968 $1.60
            Feb 1, 1969   $1.30
            Feb 1, 1970   $1.00
            Feb 1, 1971   $1.60
            May 1, 1974 $2.00
            Jan 1, 1975 $2.10
            Jan 1, 1976 $2.30
            Jan 1, 1977 $2.30
            Jan 1, 1978 $2.65 
            Jan 1, 1979 $2.90 
            Jan 1, 1980 $3.10 
            Jan 1, 1981 $3.35 
            Apr 1, 1990 $3.80
            Apr 1, 1991 $4.25
            Oct 1, 1996 $4.75
            Sep 1, 1997 $5.15
            Jul 24, 2007 $5.85
            Jul 24, 2008 $6.55
            Jul 24, 2009 $7.25
        '''
        mw = []
        for line in data.split("\n"):
            if not line.strip():
                continue
            date, wage = line.split("$")
            month, day, year = date.split()
            month = months(month)
            day = int(day.strip()[:-1])
            year = int(year)
            if day > 15:
                month += 1
            month = month % 12
            year = float(year + month / 12)
            mw.append(f"{year:.1f}   ${float(wage):.2f}")
        print("US Minimum Wage")
        for i in Columnize(mw, col_width=20, indent=" " * 2):
            print(i)
        exit(0)
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    ref_year = d["-y"]
    # Print percentages
    year = GetYear(args[0])
    cpi, ref_cpi = CPI[year], CPI[ref_year]
    print(
        f"Year = {year}, reference year = {ref_year}, difference = {abs(year - ref_year)} years"
    )
    ratio = ref_cpi / cpi
    print(f"Ratio for year/ref = {ratio}")
    print(f"Ratio for ref/year = {1 / ratio}")
    if len(args) > 1:
        s = "Amounts" if len(args[1:]) > 1 else "Amount"
        a = f"in {year}"
        b = f"in {ref_year}"
        m, n = 12, 20
        print(f"{s:^{m}s}   {a:^{n}s}   {b:^{n}s}")
        print(f"{'-' * m:^{m}s}   {'-' * n:^{n}s}   {'-' * n:^{n}s}")
        for x in [float(j) for j in args[1:]]:
            a = f"${rdp(x * ratio)} in {ref_year}"
            b = f"${rdp(x / ratio)} in {year}"
            print(f"{'$' + rdp(x):^{m}s}   {a:^{n}s}   {b:^{n}s}")

'''
Month names and numbers
    Use DaysPerMonth() to get the number of days in a month.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Month names and numbers oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import datetime
    if 1:  # Custom imports
        from dptypes import Bidict as bidict
    if 1:  # Global variables
        class G:
            pass
        g = G()
        # Names of the months
        s = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"
        Months = set(s.split())
        Months_lc = set(s.lower().split())
        Months_uc = set(s.upper().split())
        # Bi-directional mappings between month number and 3-letter string name
        g.months = bidict({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})
        # The following uses upper case letters
        g.months_uc = bidict({1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
                7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"})
        # The following uses lower case letters
        g.months_lc = bidict({1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
                7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec" })
if 1:  # Core functions
    def DaysPerMonth(month, leap_year=False):
        days_per_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31}
        if isinstance(month, str):
            n = g.months_lc(month[:3].lower())
        elif isinstance(month, int):
            n = month
        return days_per_month[n] + bool(leap_year)
    def GetDate(s):
        'Return a date.Date object given the string s in the form 11Feb2023'
        u = s.replace(" ", "")
        u = "0" + u if len(u) == 8 else u
        day = int(u[:2])
        month = g.months(u[2:5])
        year = int(u[5:])
        return datetime.date(year, month, day)

if __name__ == "__main__":
    from lwtest import run, Assert
    def Test():
        Assert(g.months[1] == "Jan")
        Assert(g.months[2] == "Feb")
        Assert(g.months[3] == "Mar")
        Assert(g.months[4] == "Apr")
        Assert(g.months[5] == "May")
        Assert(g.months[6] == "Jun")
        Assert(g.months[7] == "Jul")
        Assert(g.months[8] == "Aug")
        Assert(g.months[9] == "Sep")
        Assert(g.months[10] == "Oct")
        Assert(g.months[11] == "Nov")
        Assert(g.months[12] == "Dec")
        #
        Assert(g.months("Jan") == 1)
        Assert(g.months("Feb") == 2)
        Assert(g.months("Mar") == 3)
        Assert(g.months("Apr") == 4)
        Assert(g.months("May") == 5)
        Assert(g.months("Jun") == 6)
        Assert(g.months("Jul") == 7)
        Assert(g.months("Aug") == 8)
        Assert(g.months("Sep") == 9)
        Assert(g.months("Oct") == 10)
        Assert(g.months("Nov") == 11)
        Assert(g.months("Dec") == 12)
        # Days per month
        Assert(DaysPerMonth("Jan") == 31)
        Assert(DaysPerMonth("Feb") == 28)
        Assert(DaysPerMonth("Feb", leap_year=True) == 29)
        Assert(DaysPerMonth("Mar") == 31)
        Assert(DaysPerMonth("Apr") == 30)
        Assert(DaysPerMonth("may") == 31)
        Assert(DaysPerMonth("juN") == 30)
        Assert(DaysPerMonth("Jul") == 31)
        Assert(DaysPerMonth("Aug") == 31)
        Assert(DaysPerMonth("Sep") == 30)
        Assert(DaysPerMonth("oct") == 31)
        Assert(DaysPerMonth("nov") == 30)
        Assert(DaysPerMonth("dec") == 31)
        #
        Assert(DaysPerMonth(1) == 31)
        Assert(DaysPerMonth(2) == 28)
        Assert(DaysPerMonth(2, leap_year=True) == 29)
        Assert(DaysPerMonth(3) == 31)
        Assert(DaysPerMonth(4) == 30)
        Assert(DaysPerMonth(5) == 31)
        Assert(DaysPerMonth(6) == 30)
        Assert(DaysPerMonth(7) == 31)
        Assert(DaysPerMonth(8) == 31)
        Assert(DaysPerMonth(9) == 30)
        Assert(DaysPerMonth(10) == 31)
        Assert(DaysPerMonth(11) == 30)
        Assert(DaysPerMonth(12) == 31)
        #
        Assert(GetDate("11Feb2023") == datetime.date(2023, 2, 11))
    exit(run(globals(), halt=1)[0])

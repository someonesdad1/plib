'''
Month names and numbers
    Use DaysPerMonth() to get the number of days in a month.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Month names and numbers in dictionary form.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import datetime
    import string
    from bidict import bidict
if 1:   # Global variables
    # Names of the months
    Months = set(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
        "Aug", "Sep", "Oct", "Nov", "Dec"))
    Months_lc = set(("jan", "feb", "mar", "apr", "may", "jun", "jul",
        "aug", "sep", "oct", "nov", "dec"))
    Months_uc = set(("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL",
        "AUG", "SEP", "OCT", "NOV", "DEC"))
    # Bi-directional mappings between month number and 3-letter string name
    months = bidict({
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    })
    # The following uses upper case letters
    months_uc = bidict({
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC",
    })
    # The following uses lower case letters
    months_lc = bidict({
        1: "jan",
        2: "feb",
        3: "mar",
        4: "apr",
        5: "may",
        6: "jun",
        7: "jul",
        8: "aug",
        9: "sep",
        10: "oct",
        11: "nov",
        12: "dec",
    })
if 1:   # Core functions
    def DaysPerMonth(month, leap_year=False):
        days_per_month = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        if isinstance(month, str):
            n = months_lc(month[:3].lower())
        elif isinstance(month, int):
            n = month
        return days_per_month[n] + bool(leap_year)
    def GetDate(s):
        '''Return a date.Date object given the string s in the form
        11Feb2023.
        '''
        u = s.replace(" ", "")
        u = "0" + u if len(u) == 8 else u
        day = int(u[:2])
        month = months(u[2:5])
        year = int(u[5:])
        return datetime.date(year, month, day)

if __name__ == "__main__": 
    from lwtest import run
    def Test():
        assert months[1] == "Jan"
        assert months[2] == "Feb"
        assert months[3] == "Mar"
        assert months[4] == "Apr"
        assert months[5] == "May"
        assert months[6] == "Jun"
        assert months[7] == "Jul"
        assert months[8] == "Aug"
        assert months[9] == "Sep"
        assert months[10] == "Oct"
        assert months[11] == "Nov"
        assert months[12] == "Dec"
        #
        assert months("Jan") == 1
        assert months("Feb") == 2
        assert months("Mar") == 3
        assert months("Apr") == 4
        assert months("May") == 5
        assert months("Jun") == 6
        assert months("Jul") == 7
        assert months("Aug") == 8
        assert months("Sep") == 9
        assert months("Oct") == 10
        assert months("Nov") == 11
        assert months("Dec") == 12
        # Days per month
        assert DaysPerMonth("Jan") == 31
        assert DaysPerMonth("Feb") == 28
        assert DaysPerMonth("Feb", leap_year=True) == 29
        assert DaysPerMonth("Mar") == 31
        assert DaysPerMonth("Apr") == 30
        assert DaysPerMonth("may") == 31
        assert DaysPerMonth("juN") == 30
        assert DaysPerMonth("Jul") == 31
        assert DaysPerMonth("Aug") == 31
        assert DaysPerMonth("Sep") == 30
        assert DaysPerMonth("oct") == 31
        assert DaysPerMonth("nov") == 30
        assert DaysPerMonth("dec") == 31
        #
        assert DaysPerMonth(1) == 31
        assert DaysPerMonth(2) == 28
        assert DaysPerMonth(2, leap_year=True) == 29
        assert DaysPerMonth(3) == 31
        assert DaysPerMonth(4) == 30
        assert DaysPerMonth(5) == 31
        assert DaysPerMonth(6) == 30
        assert DaysPerMonth(7) == 31
        assert DaysPerMonth(8) == 31
        assert DaysPerMonth(9) == 30
        assert DaysPerMonth(10) == 31
        assert DaysPerMonth(11) == 30
        assert DaysPerMonth(12) == 31
        #
        assert GetDate("11Feb2023") == datetime.date(2023, 2, 11)
    exit(run(globals(), halt=1)[0])

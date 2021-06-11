'''
Month names and numbers
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
    # Month names and numbers
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    from bidict import bidict
if 1:   # Global variables
    # Names of the months
    Months = set(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
        "Aug", "Sep", "Oct", "Nov", "Dec"))
    Months_lc = set(("jan", "feb", "mar", "apr", "may", "jun", "jul",
        "aug", "sep", "oct", "nov", "dec"))
    Months_uc = set (("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL",
        "AUG", "SEP", "OCT", "NOV", "DEC"))
    # Bi-directional mappings between month number and 3-letter string name
    months = bidict({
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "Apr",
        5 : "May",
        6 : "Jun",
        7 : "Jul",
        8 : "Aug",
        9 : "Sep",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec",
    })

    # The following uses upper case letters
    months_uc = bidict({
        1 : "JAN",
        2 : "FEB",
        3 : "MAR",
        4 : "APR",
        5 : "MAY",
        6 : "JUN",
        7 : "JUL",
        8 : "AUG",
        9 : "SEP",
        10 : "OCT",
        11 : "NOV",
        12 : "DEC",
    })

    # The following uses lower case letters
    months_lc = bidict({
        1 : "jan",
        2 : "feb",
        3 : "mar",
        4 : "apr",
        5 : "may",
        6 : "jun",
        7 : "jul",
        8 : "aug",
        9 : "sep",
        10 : "oct",
        11 : "nov",
        12 : "dec",
    })
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
    exit(run(globals(), halt=1)[0])

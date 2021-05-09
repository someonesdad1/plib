'''
Provides a bi-directional mapping for month number to/from month name.

Examples:
    months[1] -> "Jan"
    months("Jan") -> 1
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
from bidict import bidict

# Names of the months
Months = set("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())
Months_lc = set([i.lower() for i in Months])
Months_uc = set([i.upper() for i in Months])

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
    print("months[1] =", months[1])
    print('months("Jan") =', months("Jan"))
    print("months_lc[1] =", months_lc[1])
    print('months_lc("jan") =', months_lc("jan"))
    print("months_uc[1] =", months_uc[1])
    print('months_uc("JAN") =', months_uc("JAN"))

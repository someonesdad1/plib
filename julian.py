'''
Julian day routines from Meeus, "Astronomical Formulae for Calculators".
The routines are:

    Julian(month, day, year)            Integer Julian day number
    Julian1(datestring)                 Integer Julian day number, but
                                        takes string arg "YYYYMMDD"
    JulianAstro(month, day, year)       Astronomical Julian day number
    JulianToDate(julian_day)            Returns month, day, year tuple
    DayOfWeek(month, day, year)         0 = Sunday
    DayOfYear(month, day, year)         1 to 365 (366 in leap year)
    IsValidDate(month, day, year)       Returns True if date is valid Gregorian
    IsLeapYear(year)                    Returns True if year is leap year
    NumDaysInMonth(month, year)

The JulianAstro function returns the astronomical form and is returned
as a floating point number.  The astronomical Julian day begins at
Greenwich mean noon.  The Julian() function returns the more usual
Julian day as an integer; it is gotten from the astronomical form by
adding 0.55 and taking the integer part.
'''

# Copyright (C) 1998 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

def NumDaysInMonth(month, year):
    if month == 2:
        return 29 if IsLeapYear(year) else 28
    elif month in set((4, 6, 9, 11)):
        return 30
    elif month in set((1, 3, 5, 7, 8, 10, 12)):
        return 31
    else:
        raise ValueError("Bad month")

def DecodeDay(day):
    '''Return a tuple of (hr, min, sec) given a decimal day.  Example:
    DecodeDay(1.5) returns (12, 0, 0.0).
 
    Important:  this is conventional time, not Julian astronomical type
    days.
    '''
    fp = day - int(day)
    hr = int(24*fp)
    fp -= hr/24
    min = int(24*60*fp)
    fp -= min/(24*60)
    sec = 24*3600*fp
    return (hr, min, sec)

def JulianToDate(julian_day):
    '''From Meeus, "Astronomical Algorithms", pg 63.
    '''
    if julian_day < 0:
        raise ValueError("Bad input value")
    jd = julian_day + 0.5
    Z = int(jd)
    F = jd - Z
    A = Z
    if Z >= 2299161:
        alpha = int((Z - 1867216.26)/36254.25)
        A = Z + 1 + alpha - alpha//4
    B = A + 1524
    C = int((B - 122.1)/365.25)
    D = int(365.25 * C)
    E = int((B - D)/30.6001)
    day = B - D - int(30.6001 * E) + F
    if E < 13.5:
        month = int(E - 1)
    else:
        month = int(E - 13)
    if month > 2.5:
        year = int(C - 4716)
    else:
        year = int(C - 4715)
    hr, min, sec = DecodeDay(day)
    return month, day, year, hr, min, sec

def DayOfYear(month, day, year):
    if IsLeapYear(year):
        n = int((275*month)//9 - ((month + 9)//12) + int(day) - 30)
    else:
        n = int((275*month)//9 - 2*((month + 9)//12) + int(day) - 30)
    assert(1 <= n <= 366)
    return n

def DayOfWeek(month, day, year):
    julian = int(JulianAstro(month, int(day), year) + 1.5)
    return julian % 7

def IsLeapYear(year):
    # Ref. Meeus pg 62
    return (True if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
            else False)

def IsValidDate(month, day, year):
    '''Returns True if the year is later than 1752 and the month and day
    numbers are valid.
    '''
    if ((month < 1 or month > 12) or (int(month) != month) or
            (year < 1753) or (day < 1)):
        return False
    if isinstance(day, float):
        if month == 2:
            if IsLeapYear(year):
                if day >= 30:
                    return False
            else:
                if day >= 29:
                    return False
        elif month in (4, 6, 9, 11):
            if day >= 31:
                return False
        else:
            if day >= 32:
                return False
    else:
        assert(isinstance(day, int))
        if month == 2:
            if IsLeapYear(year):
                if day > 29:
                    return False
            else:
                if day > 28:
                    return False
        elif month in (4, 6, 9, 11):
            if day > 30:
                return False
        else:
            if day > 31:
                return False
    return True

def JulianAstro(month, day, year):
    '''Returns the Julian astronomical day number; it's always a
    floating point number.  month must be an integer from 1 to 12, day
    can be an integer or float, and year must be an integer.  Note that
    day 1.0 means 12 noon on the first day of the month; 1.5 means
    midnight.
    '''
    assert(isinstance(month, int) and 1 <= month <= 12)
    assert(isinstance(day, (int, float)) and 1 <= day < 32)
    assert(isinstance(year, int))
    if month < 3:
        year = year - 1
        month = month + 12
    # Meeus pg 60 warns that the int() function from some programming
    # languages doesn't behave as needed; hence, we define Int such that
    # Int(-7.5) == -8.
    Int = lambda x:  int(x) if x >= 0 else int(x) - 1
    julian = Int(365.25*year) + Int(30.6001*(month + 1)) + day + 1720994.5
    tmp = year + month/100 + day/10000
    if tmp >= 1582.1015:
        A = year//100
        B = 2 - A + A//4
        julian += B
    return float(julian)

def Julian(month, day, year):
    '''Returns the integer Julian day for the given date.
    '''
    return int(JulianAstro(month, day, year) + 0.55)

def Julian1(s):
    '''Returns the integer Julian date when given a string s in the form
    YYYYMMDD.
    '''
    assert(len(s) == 8)
    year, month, day = int(s[0:4]), int(s[4:6]), int(s[6:8])
    return Julian(month, day, year)


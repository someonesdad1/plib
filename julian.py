'''
Julian day routines 
    From Meeus, "Astronomical Formulae for Calculators"

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

    The JulianAstro function returns the astronomical form and is
    returned as a floating point number.  The astronomical Julian day
    begins at Greenwich mean noon.  The Julian() function returns the
    more usual Julian day as an integer; it is gotten from the
    astronomical form by adding 0.55 and taking the integer part.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 1998 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <science> Julian day routines from Meeus, "Astronomical Formulae
    # for Calculators".
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
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
if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal
    from pdb import set_trace as xx
    def TestJulian():
        assert_equal(Julian(12, 31, 1989), 2447892)
        assert_equal(Julian1("19891231"), 2447892)
        assert_equal(Julian(1, 1, 1990), 2447893)
        assert_equal(Julian1("19900101"), 2447893)
        assert_equal(Julian(7, 4, 1776), 2369916)
        assert_equal(Julian1("17760704"), 2369916)
        assert_equal(Julian(2, 29, 2000), 2451604)
        assert_equal(Julian1("20000229"), 2451604)
    def TestJulianAstro():
        assert_equal(JulianAstro(1, 27.5, 333), 1842713.0)
        assert_equal(JulianAstro(10, 4.81, 1957), 2436116.31)
    def TestDayOfWeek():
        assert_equal(DayOfWeek(11, 13, 1949), 0)
        assert_equal(DayOfWeek(5, 30, 1998), 6)
        assert_equal(DayOfWeek(6, 30, 1954), 3)
    def TestDayOfYear():
        assert_equal(DayOfYear(11, 14, 1978), 318)
        assert_equal(DayOfYear(4, 22, 1980), 113)
    def TestJulianToDate():
        eps = 1e-5
        month, day, year, hr, min, sec = JulianToDate(2436116.31)
        assert_equal(month, 10)
        assert_equal(year, 1957)
        assert_equal(abs(day), 4.81, abstol=eps)
        #
        month, day, year, hr, min, sec = JulianToDate(1842713.0)
        assert_equal(month, 1)
        assert_equal(year, 333)
        assert_equal(abs(day), 27.5, abstol=eps)
        #
        month, day, year, hr, min, sec = JulianToDate(1507900.13)
        assert_equal(month, 5)
        assert_equal(year, -584)
        assert_equal(abs(day), 28.63, abstol=eps)
    def TestNumDaysInMonth():
        yr = 1999
        DIM = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for mo, dim in enumerate(DIM):
            assert(NumDaysInMonth(mo + 1, yr) == dim)
        yr = 2000
        DIM = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for mo, dim in enumerate(DIM):
            assert(NumDaysInMonth(mo + 1, yr) == dim)
    def TestNumericalInit():
        data = (
            # Test vectors from Meeus pg 61 & 62
            #  y,    m,     d,     jd
            (1957, 10,  4.81, 2436116.31),
            (333,  1,  27.5, 1842713.0),
            (2000,  1,   1.5, 2451545.0),
            (1999,  1,   1.0, 2451179.5),
            (1988,  6,  19.5, 2447332.0),
            (1600,  1,   1.0, 2305447.5),
            (1600, 12,  31.0, 2305812.5),
            (-123,  12,  31.0, 1676496.5),
            (-122,   1,   1.0, 1676497.5),
            (-1000,  2,  29.0, 1355866.5),
            (-4712,  1,   1.5, 0.0),
        )
        for y, m, d, jd in data:
            jul = JulianAstro(m, d, y)
            assert(jd - jul == 0)
    def TestStringInit():
        data = (
            # Test points from Meeus pg 62
            ("4Oct1957:19:26:24", 2436116.31),
            ("27Jan333:12",       1842713.0),
            ("1.5jan2000",        2451545.0),
            ("1.0jan1999",        2451179.5),
            ("19.5JUN1988",       2447332.0),
            ("1.0jan1600",        2305447.5),
            ("31.0Dec1600",       2305812.5),
            ("31.0Dec-123",       1676496.5),
            ("1.0jan-122",        1676497.5),
            ("29Feb-1000",        1355866.5),
            ("1.5Jan-4712",       0.0),
        )
    def TestDecodeDay():
        assert(DecodeDay(1.5) == (12, 0, 0))
    def TestNumDaysInMonth():
        y = 2000
        months = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            assert(NumDaysInMonth(m, y) == days)
        y = 2001
        months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            assert(NumDaysInMonth(m, y) == days)
    def TestIsLeapYear():
        for y in (1700, 1800, 1900, 2100, 2001):
            assert(not IsLeapYear(y))
        for y in (1600, 2000, 2400, 2004):
            assert(IsLeapYear(y))
    def TestIsValidDate():
        for m, d, y in (
            (1,  1, 1753),
            (12, 31, 1753),
            (1, 1, 2000),
        ):
            assert(IsValidDate(m, d, y))
        # Invalid dates for year 2001, a non-leap year
        for m, d in (
            (1, 0),
            (1, 0.999),
            (1, 32),
            (2, 29),
            (3, 32),
            (4, 31),
            (5, 32),
            (6, 31),
            (7, 32),
            (8, 32),
            (9, 31),
            (10, 32),
            (11, 31),
            (12, 32),
        ):
            assert(not IsValidDate(m, d, 2001))
    exit(run(globals(), halt=1)[0])

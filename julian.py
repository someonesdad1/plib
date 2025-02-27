"""
Julian day routines
    From Meeus, "Astronomical Formulae for Calculators"

    Julian(month, day, year)            Integer Julian day number
    Julian1(datestring)                 Integer Julian day number, but
                                        takes string arg "YYYYMMDD"
    JulianAstro(month, day, year)       Astronomical Julian day number
    Also:
            JulianAstroDateTime(year, month, day, hour, minute, second)
            JulianAstroDT(datetime.datetime_instance)

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

    DecodeDateString() is used to decode date strings of the form
    '24Mar2023:20:33:18.0'.  These are used by the hc.py calculator
    program for date arithmetic.

"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 1998 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <science> Julian day routines from Meeus, "Astronomical Formulae
    # for Calculators".
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    # Standard libraries
    import datetime
    import math
    import re

    # Custom libraries
    import months
    import iso
    from lwtest import Assert

    # Global variables
    ii = isinstance


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
    """Return a tuple of (hr, min, sec) given a decimal day.  Example:
    DecodeDay(1.5) returns (12, 0, 0.0).

    Important:  this is conventional time, not Julian astronomical type
    days.
    """
    fp = day - int(day)
    hr = int(24 * fp)
    fp -= hr / 24
    min = int(24 * 60 * fp)
    fp -= min / (24 * 60)
    sec = 24 * 3600 * fp
    return (hr, min, sec)


def JulianToDate(julian_day):
    """From Meeus, "Astronomical Algorithms", pg 63."""
    if julian_day < 0:
        raise ValueError("Bad input value")
    jd = julian_day + 0.5
    Z = int(jd)
    F = jd - Z
    A = Z
    if Z >= 2299161:
        alpha = int((Z - 1867216.26) / 36254.25)
        A = Z + 1 + alpha - alpha // 4
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
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
        n = int((275 * month) // 9 - ((month + 9) // 12) + int(day) - 30)
    else:
        n = int((275 * month) // 9 - 2 * ((month + 9) // 12) + int(day) - 30)
    Assert(1 <= n <= 366)
    return n


def DayOfWeek(month, day, year):
    julian = int(JulianAstro(month, int(day), year) + 1.5)
    return julian % 7


def IsLeapYear(year):
    # Ref. Meeus pg 62
    return True if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0) else False


def IsValidDate(month, day, year):
    """Returns True if the year is later than 1752 and the month and day
    numbers are valid.
    """
    if (month < 1 or month > 12) or (int(month) != month) or (year < 1753) or (day < 1):
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
        Assert(isinstance(day, int))
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
    """Returns the Julian astronomical day number; it's always a
    floating point number.  month must be an integer from 1 to 12, day
    can be an integer or float, and year must be an integer.  Note that
    day 1.0 means 12 noon on the first day of the month; 1.5 means
    midnight.  Here, the time is Greenwich mean time (GMT).

    Note:  because of the PITA of dealing with daylight saving time and
    local times, this day parameter assumes it's a day for GMT.  When
    calculating time differences in days, this distinction doesn't matter,
    but if you want correct astronomical Julian day numbers, you must
    convert local time to GMT.
    """
    Assert(isinstance(month, int) and 1 <= month <= 12)
    Assert(isinstance(day, (int, float)) and 1 <= day < 32)
    Assert(isinstance(year, int))
    if month < 3:
        year = year - 1
        month = month + 12
    julian = (
        math.floor(365.25 * year) + math.floor(30.6001 * (month + 1)) + day + 1720994.5
    )
    tmp = year + month / 100 + day / 10000
    if tmp >= 1582.1015:
        A = year // 100
        B = 2 - A + A // 4
        julian += B
    return float(julian)


def JulianAstroDateTime(year, month, day, hour, minute, second):
    """Same as JulianAstro.  All arguments must be integers.  hour must be
    on [0, 24).
    """
    for x in (year, month, day, hour, minute):
        Assert(ii(x, int))
    Assert(ii(second, (int, float)))
    Assert(0 <= hour < 24)
    if ii(second, float):
        s = int(second)
        microsecond = int((second - s) * 1e6)
    else:
        s = int(second)
        microsecond = 0
    dt = datetime.datetime(year, month, day, hour, minute, second, microsecond)
    return JulianAstroDT(dt)


def JulianAstroDT(datetime_instance):
    """Same as JulianAstro but uses a datetime.datetime instance to define
    the time.  This is a convenience because you just construct a normal
    date/time object without fiddling with the astronomical time.
    """
    dt = datetime_instance
    Assert(ii(dt, datetime.datetime))
    mo, d, y = dt.month, dt.day, dt.year
    h, m, s = dt.hour, dt.minute, dt.second
    # Get midnight Julian day number as an integer
    jdi = Julian(mo, d, y)
    # Add in the fraction of a day
    day_fraction = (h + m / 60 + s / 3600) / 24
    # day_fraction must be 0 for 12 noon, so subtract 0.5 day
    day_fraction -= 0.5
    jdi += day_fraction
    return jdi


def Julian(month, day, year):
    """Returns the integer Julian day for the given date."""
    return int(JulianAstro(month, day, year) + 0.55)


def Julian1(s):
    """Returns the integer Julian date when given a string s in the form
    YYYYMMDD.
    """
    Assert(len(s) == 8)
    year, month, day = int(s[0:4]), int(s[4:6]), int(s[6:8])
    return Julian(month, day, year)


def JulianNow():
    "Return Julian astronomical day number for now in current local time"
    tm = iso.time()
    i = iso.ISO()
    i.set(iso.localtime(tm))
    tm = str(i)
    dt, tm = tm.split("-")
    jd = Julian1(dt)
    h, m, s = [int(i) for i in tm.split(":")]
    jd += (h + (m + s / 60) / 60) / 24
    return jd


def JulianToday():
    "Return Julian astronomical day number for beginning of today"
    return int(JulianNow())


def DecodeDateString(s):
    """The string s can have the following forms:
        '24Mar2023'
        '24Mar2023@20:33:18.0'
        '@20:33:18.0'
    These are converted to an astronomical Julian day number.  Returns None
    if s is not a suitable date string.
    """

    def DecodeDate(dt):
        Assert(len(dt) > 4)
        digits = set("0123456789")
        d = list(dt)
        # Get day
        s = d.pop(0)
        if d[0] in digits:
            s += d.pop(0)
        day = int(s)
        Assert(d[0] not in digits)
        # Get month
        s = "".join(d[:3]).lower()
        month = months.months_lc(s)
        # Get year
        year = int("".join(d[3:]))
        return (year, month, day)

    def DecodeTime(tm):
        "Return number of days of the time on [0.5, 1.5)"
        try:
            f = tm.split(":")
            Assert(f)
            hours = int(f.pop(0))
            if f:
                minutes = int(f.pop(0))
                hours += minutes / 60
            if f:
                seconds = float(f.pop(0))  # Seconds
                hours += seconds / 3600
            Assert(0 <= hours < 24)
            # Subtract 12 hours because noon is 0.5 day
            hours -= 12
            return hours / 24 + 0.5
        except Exception:
            return None

    s = s.strip().lower()
    if not s:
        return None
    if s[0] == "@":
        # '@20:33:18.0' form
        days = DecodeTime(s[1:])
        if days is None:
            return None
        # Add it to today's date
        jd = JulianToday()
        return jd + days
    elif "@" in s:
        # '24Mar2023@20:33:18.0' form
        dt, tm = s.split("@")
        days = DecodeTime(tm)
        year, month, day = DecodeDate(dt)
        jd = Julian(month, day, year)
        return jd + days
    else:
        # '24Mar2023' form
        year, month, day = DecodeDate(s)
        return Julian(month, day, year)


if 0 and __name__ == "__main__":
    # Test area
    month, day, year = 4, 24, 2023
    hour, minute, second = 13, 7, 0
    dt = datetime.datetime(year, month, day, hour, minute, second)
    print(JulianAstroDT(dt))
    print(JulianAstroDateTime(year, month, day, hour, minute, second))
    print(JulianNow())
    exit()


if __name__ == "__main__":
    from lwtest import run, raises, assert_equal
    from pdb import set_trace as xx
    import sys

    def TestDecodeDateString():
        x = DecodeDateString("24Mar2023")
        assert_equal(x, 2460028)
        x = DecodeDateString("24Mar2023@17:38")
        expected = 0.734722222
        assert_equal(round(x - 2460028, 9), expected)
        x = DecodeDateString("@17:38")
        now = JulianToday()
        assert_equal(round(x - now, 9), expected)

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
        # Test case, pg 61 of Meeus:  27 Jan 333 at 12 pm == 1842713.0
        expected = 1842713.0
        assert_equal(JulianAstro(1, 27.5, 333), expected)
        if 1:  # Same case, different functions
            # Note the following also checks JulianAstroDT()
            year, month, day, hour, minute, second = 333, 1, 27, 12, 0, 0
            jadt = JulianAstroDateTime(year, month, day, hour, minute, second)
            assert_equal(jadt, expected)
        # Test case, pg 61 of Meeus:  4.81 Oct 1957 (Sputnik I launch) == 2436116.31
        expected = 2436116.31
        assert_equal(JulianAstro(10, 4.81, 1957), expected)
        if 1:  # Other test cases from pg 62
            cases = (
                ("2000 1  1.5", 2451545.0),
                ("1999 1  1.0", 2451179.5),
                ("1987 1 27.0", 2446822.5),
                #
                ("-123 12 31.0", 1676496.5),
                ("-122 1   1.0", 1676497.5),
                #
                ("-1000 7 12.5", 1356001.0),
                ("-1000 2 29.0", 1355866.5),
                ("-1001 8 17.9", 1355671.4),
                ("-4712 1  1.5", 0.0),
            )
            for s, expected in cases:
                y, m, d = s.split()
                year, month = int(y), int(m)
                day = float(d)
                assert_equal(JulianAstro(month, day, year), expected)

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
            Assert(NumDaysInMonth(mo + 1, yr) == dim)
        yr = 2000
        DIM = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for mo, dim in enumerate(DIM):
            Assert(NumDaysInMonth(mo + 1, yr) == dim)

    def TestNumericalInit():
        data = (
            # Test vectors from Meeus pg 61 & 62
            #  y,    m,     d,     jd
            (1957, 10, 4.81, 2436116.31),
            (333, 1, 27.5, 1842713.0),
            (2000, 1, 1.5, 2451545.0),
            (1999, 1, 1.0, 2451179.5),
            (1988, 6, 19.5, 2447332.0),
            (1600, 1, 1.0, 2305447.5),
            (1600, 12, 31.0, 2305812.5),
            (-123, 12, 31.0, 1676496.5),
            (-122, 1, 1.0, 1676497.5),
            (-1000, 2, 29.0, 1355866.5),
            (-4712, 1, 1.5, 0.0),
        )
        for y, m, d, jd in data:
            jul = JulianAstro(m, d, y)
            Assert(jd - jul == 0)

    def TestStringInit():
        data = (
            # Test points from Meeus pg 62
            ("4Oct1957:19:26:24", 2436116.31),
            ("27Jan333:12", 1842713.0),
            ("1.5jan2000", 2451545.0),
            ("1.0jan1999", 2451179.5),
            ("19.5JUN1988", 2447332.0),
            ("1.0jan1600", 2305447.5),
            ("31.0Dec1600", 2305812.5),
            ("31.0Dec-123", 1676496.5),
            ("1.0jan-122", 1676497.5),
            ("29Feb-1000", 1355866.5),
            ("1.5Jan-4712", 0.0),
        )

    def TestDecodeDay():
        Assert(DecodeDay(1.5) == (12, 0, 0))

    def TestNumDaysInMonth():
        y = 2000
        months = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            Assert(NumDaysInMonth(m, y) == days)
        y = 2001
        months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            Assert(NumDaysInMonth(m, y) == days)

    def TestIsLeapYear():
        for y in (1700, 1800, 1900, 2100, 2001):
            Assert(not IsLeapYear(y))
        for y in (1600, 2000, 2400, 2004):
            Assert(IsLeapYear(y))

    def TestIsValidDate():
        for m, d, y in (
            (1, 1, 1753),
            (12, 31, 1753),
            (1, 1, 2000),
        ):
            Assert(IsValidDate(m, d, y))
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
            Assert(not IsValidDate(m, d, 2001))

    if len(sys.argv) > 1:
        print(f"{JulianNow()}")
    else:
        exit(run(globals(), halt=1)[0])

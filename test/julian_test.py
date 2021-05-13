from lwtest import run, raises, assert_equal
from julian import *
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

if __name__ == "__main__":
        run(globals(), halt=1)

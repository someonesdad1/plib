'''
Module to perform various navigation tasks 
  Reference:  Aviation Formulary V1.20 by Ed Williams
  Definitions:
    1 degree of arc along a great circle is 60 nm
    TC = true course = course angle measured clockwise from a meridian
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2002 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    from math import pi, log, sin, cos, tan, atan2, sqrt
if 1:  # Global variables
    _tol = sqrt(1e-15)
def TrueCourseAndDistance(lat1, lon1, lat2, lon2):
    '''Calculates the true course (rhumbline direction) and distance
    between two points on earth's surface.  Returns a list consisting
    of the true course and the distance, both in radians.  All arguments
    are expected to be in radians.
    '''
    two_pi, pi_4 = 2*pi, pi/4
    dlon_W = (lon2 - lon1) % two_pi
    dlon_E = (lon1 - lon2) % two_pi
    dphi = log(tan(lat2/2 + pi_4)/tan(lat1/2 + pi_4))
    s = lat2 - lat1
    q = cos(lat1) if abs(s) < _tol else s/dphi
    if dlon_W < dlon_E:
        # Westerly rhumb line is the shortest
        tc = atan2(-dlon_W, dphi) % two_pi
        d = sqrt(q*q*dlon_W*dlon_W + s*s)
    else:
        tc = atan2(dlon_E, dphi) % two_pi
        d = sqrt(q*q*dlon_E*dlon_E + s*s)
    return tc, d
def FindRhumblineDestination(tc, d, lat0, lon0):
    '''Will return the tuple (lat, lon) that gives the position of the
    point that will be reached on a true course of tc for a distance
    of d starting from (lat0, lon0).  All arguments are expected to
    be in radians.
    '''
    lat = lat0 + d*cos(tc)
    dphi = log(tan(lat/2 + pi/4)/tan(lat0/2 + pi/4))
    s = lat - lat0
    q = cos(lat0) if abs(s) < _tol else s/dphi
    dlon = -d*sin(tc)/q
    lon = ((lon0 + dlon + pi) % (2*pi)) - pi
    return lat, lon
def GreatCircleDistance(lat1, lon1, lat2, lon2):
    '''Returns the great circle distance between two points.  All
    numbers are in radians.
    '''
    return acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1-lon2))
def InitialCourseBetweenPoints(lat1, lon1, lat2, lon2):
    x = sin(lon1 - lon2)*cos(lat2)
    y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon1 - lon2)
    tc = atan2(x, y) % (2*pi)
    return tc
def CalcUnknownWindDirection(course, heading, tas, gs):
    '''Returns the wind direction (from) and speed given the other
    factors.  Speed units must be the same but are otherwise arbitrary.
    The angles are measured in radians.  tas is true airspeed, gs is
    ground speed, and ws is wind speed.
    '''
    dt, dh, s, tpi = tas - gs, heading - course, sin(dh/2), 2*pi
    ws = sqrt(dt*dt + 4*tas*gs*s*s)
    wd = course + atan2(tas*sin(dh), tas*cos(dh) - gs)
    if wd < 0:
        wd = wd + tpi
    elif wd > 2*pi:
        wd = wd - tpi
    return wd, ws
if __name__ == "__main__": 
    from lwtest import run
    tol = 1e-15
    two_pi = 2*pi
    pi_4   = pi/4
    def TestTrueCourseAndDistance():
        # Test TrueCourseAndDistance()
        deg2rad = pi/180
        lat1 = 42.5*deg2rad
        lon1 = 116*deg2rad
        lat2 = 43*deg2rad
        lon2 = 115*deg2rad
        tc, d = TrueCourseAndDistance(lat1, lon1, lat2, lon2)
        # Convert to degrees
        tc = tc/deg2rad
        dtc = abs(tc - 55.748832629)
        # Convert to nautical miles (1 nm = 1 minute of arc)
        nm = d/deg2rad*60.0
        dd = abs(nm - 53.3028423162)
        assert(dtc <= 1e-8 and dd <= 1e-8)
    def TestFindRhumblineDestination():
        lat, lon = FindRhumblineDestination(1.38446, 0.62965, 0.592539, 2.06647)
        dlat = abs(lat - 0.709187891592)
        dlon = abs(lon - 1.28776164456)
        assert(dlat <= 1e-10 and dlon <= 1e-10)
    def TestInitialCourseBetweenPoints():
        tc = InitialCourseBetweenPoints(0.592539, 2.06647, 0.709186, 1.287762)*180/pi
        assert(abs(tc - 65.892091214) <= 1e-10)
    exit(run(globals())[0])

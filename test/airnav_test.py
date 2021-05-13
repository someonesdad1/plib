import math
from lwtest import run
from airnav import TrueCourseAndDistance, FindRhumblineDestination
from airnav import InitialCourseBetweenPoints

tol = 1e-15
pi = math.pi
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

if __name__ == "__main__":
    exit(run(globals())[0])

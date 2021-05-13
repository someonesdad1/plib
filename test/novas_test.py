import sys
from lwtest import run, assert_equal
from novas import *

def Test():
    '''This is the file checkout-st.c file from the original NOVAS-C
    package translated to a python script.
    '''
    N_STARS = 3
    N_TIMES = 4
    error = 0
    deltat = 60.0
    tjd = [2450203.5, 2450203.5, 2450417.5, 2450300.5]
    ra = [0.0]
    dec = [0.0]
    stars = [
        {
            "catalog"        : "FK5",
            "starname"       : "POLARIS",
            "starnumber"     : 0,
            "ra"             : 2.5301955556,
            "dec"            : 89.2640888889,
            "promora"        : 19.8770,
            "promodec"       : -1.520,
            "parallax"       : 0.0070,
            "radialvelocity" : -17.0,
        },
        {
            "catalog"        : "FK5",
            "starname"       : "Delta ORI",
            "starnumber"     : 1,
            "ra"             : 5.5334438889,
            "dec"            : -0.2991333333,
            "promora"        : 0.0100,
            "promodec"       : -0.220,
            "parallax"       : 0.0140,
            "radialvelocity" : 16.0,
        },
        {
            "catalog"        : "FK5",
            "starname"       : "Theta CAR",
            "starnumber"     : 2,
            "ra"             : 10.7159355556,
            "dec"            : -64.3944666667,
            "promora"        : -0.3480,
            "promodec"       : 1.000,
            "parallax"       : 0.0000,
            "radialvelocity" : 24.0,
        },
    ]
    geo_loc = {
        "latitude"    : 45.0,
        "longitude"   : -75.0,
        "height"      : 0.0,
        "temperature" : 10.0,
        "pressure"    : 1010.0,
    }
    earth = {
        "type"   : 0,
        "number" : 0,
        "name"   : "",
    }
    error = set_body(0, 3, "Earth", earth)
    if error:
        raise ValueError("Error '{}' from set_body".format(error))
    out = []
    log = out.append
    for i in range(N_TIMES):
        for j in range(N_STARS):
            error = topo_star(tjd[i], earth, deltat,
                              stars[j], geo_loc, ra, dec)
            if error:
                m = "Error %d from topo_star. Star %d  Time %d"
                raise ValueError(m.format(error, j, i))
            else:
                log("JD = {:f}  Star = {}".format(tjd[i], stars[j]["starname"]))
                log("RA = {:12.9f}  Dec = {:12.8f}".format(ra[0], dec[0]))
                log("")
        log("")
    expected = [
        'JD = 2450203.500000  Star = POLARIS',
        'RA =  2.446916265  Dec =  89.24633852',
        '',
        'JD = 2450203.500000  Star = Delta ORI',
        'RA =  5.530109345  Dec =  -0.30575219',
        '',
        'JD = 2450203.500000  Star = Theta CAR',
        'RA = 10.714516141  Dec = -64.38132162',
        '',
        '',
        'JD = 2450203.500000  Star = POLARIS',
        'RA =  2.446916265  Dec =  89.24633852',
        '',
        'JD = 2450203.500000  Star = Delta ORI',
        'RA =  5.530109345  Dec =  -0.30575219',
        '',
        'JD = 2450203.500000  Star = Theta CAR',
        'RA = 10.714516141  Dec = -64.38132162',
        '',
        '',
        'JD = 2450417.500000  Star = POLARIS',
        'RA =  2.509407657  Dec =  89.25195435',
        '',
        'JD = 2450417.500000  Star = Delta ORI',
        'RA =  5.531194826  Dec =  -0.30305771',
        '',
        'JD = 2450417.500000  Star = Theta CAR',
        'RA = 10.714434953  Dec = -64.37368326',
        '',
        '',
        'JD = 2450300.500000  Star = POLARIS',
        'RA =  2.481107884  Dec =  89.24253162',
        '',
        'JD = 2450300.500000  Star = Delta ORI',
        'RA =  5.530371408  Dec =  -0.30235140',
        '',
        'JD = 2450300.500000  Star = Theta CAR',
        'RA = 10.713566017  Dec = -64.37969000',
        '',
        '',
    ]
    assert(out == expected)

if __name__ == "__main__":
    failed, messages = run(globals())

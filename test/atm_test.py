import math
import os
import subprocess
import sys
from time import sleep
from lwtest import run, assert_equal, raises
from atm import P0, T0, rho0, atm
from win import on_windows
from pdb import set_trace as xx

def GetReferenceData():
    '''Return the altitude in km, along with sigma = reduced density,
    delta = reduced pressure, theta = reduced temperature (reduced means
    relative to the sea level values.
 
    The expected form of the output data of the atm command is:
        NASA reference atmosphere function by R. Carmichael
        Reduced atmosphere values at    5.00000000     km
        sigma = reduced density     =  0.601166010    
        delta = reduced pressure    =  0.533414602    
        theta = reduced temperature =  0.887300014    
    '''
    # Note:  this script used to run the atm command, which was the atm.f90
    # code.  Now it just returns the above numbers.
    if 0:
        if on_windows:
            dir = "c:/cygwin/pylib/test"
            make = "c:/cygwin/bin/make.exe >nul 2>&1"
            print("atm_test.py failed:  need FORTRAN compiler for atm.f90")
            exit(1)
        else:
            dir = "/pylib/test"
            make = "/usr/bin/make >/dev/null 2>&1"
        os.chdir(dir)
        os.system(make)
        sleep(0.1)
        # Note:  the atm command is the compiled form of atm.f90, so you need a
        # FORTRAN compiler to run this test.
        s = subprocess.Popen(os.path.join(dir, "atm"), stdout=subprocess.PIPE)
        lines = [i.decode("utf8") for i in s.stdout.readlines()]
        h_km = float(lines[1].split()[4])
        f = lambda line_num: float(lines[line_num].split()[5])
        sigma = f(2)
        delta = f(3)
        theta = f(4)
    h_km, sigma, delta, theta = 5, 0.601166010, 0.533414602, 0.887300014
    return h_km, sigma, delta, theta

def Test():
    altitude_km, sigma, delta, theta = GetReferenceData()
    d = atm(altitude_km)
    rho = sigma*rho0
    P = delta*P0
    T = theta*T0
    if 0:
        print("Density =", rho)
        print("Pressure =", P)
        print("Temperature =", T)
        from pprint import pprint as pp
        pp(d)
    eps = 1e-6
    assert_equal(rho, d["density"], reltol=eps)
    assert_equal(P, d["pressure"], reltol=eps)
    assert_equal(T, d["temperature"], reltol=eps)

if __name__ == "__main__":
    exit(run(globals())[0])

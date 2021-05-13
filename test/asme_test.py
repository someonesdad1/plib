from asme import UnifiedThread
from lwtest import run

def Test_asme():
    eps = 0.0001
    # Check the formulas on a 1/4-20 thread
    u = UnifiedThread(1/4, 20, Class=1)
    assert(abs(u.Class2PDtol() - 0.00373) <= eps)
    assert(abs(u.Allowance() - 0.0011) <= eps)
    # Class 1 thread
    assert(abs(u.Dmin() - 0.2367) <= eps)
    assert(abs(u.Dmax() - 0.2489) <= eps)
    assert(abs(u.Emin() - 0.2108) <= eps)
    assert(abs(u.Emax() - 0.2164) <= eps)
    assert(abs(u.dmin() - 0.1959) <= eps)
    assert(abs(u.dmax() - 0.2074) <= eps)
    assert(abs(u.emin() - 0.2175) <= eps)
    assert(abs(u.emax() - 0.2248) <= eps)
    # Class 2 thread
    u.Class = 2
    assert(abs(u.Dmin() - 0.2408) <= eps)
    assert(abs(u.Dmax() - 0.2489) <= eps)
    assert(abs(u.Emin() - 0.2127) <= eps)
    assert(abs(u.Emax() - 0.2164) <= eps)
    assert(abs(u.dmin() - 0.1959) <= eps)
    assert(abs(u.dmax() - 0.2074) <= eps)
    assert(abs(u.emin() - 0.2175) <= eps)
    assert(abs(u.emax() - 0.2223) <= eps)
    # Class 3 thread
    u.Class = 3
    assert(abs(u.Dmin() - 0.2419) <= eps)
    assert(abs(u.Dmax() - 0.2500) <= eps)
    assert(abs(u.Emin() - 0.2147) <= eps)
    assert(abs(u.Emax() - 0.2175) <= eps)
    assert(abs(u.dmin() - 0.1959) <= eps)
    assert(abs(u.dmax() - 0.2067) <= eps)
    assert(abs(u.emin() - 0.2175) <= eps)
    assert(abs(u.emax() - 0.2211) <= eps)
    # Other
    assert(abs(u.TapDrill(percent_thread=75) - 0.2013) <= eps)
    assert(abs(u.SellersRecommendedTPI() - 20.2) <= 0.01)
    assert(abs(u.DoubleDepth() - 0.065) <= eps)

if __name__ == "__main__":
    exit(run(globals())[0])

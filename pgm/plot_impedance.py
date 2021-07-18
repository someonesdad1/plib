'''
Plot impedance as a function of angular frequency
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from math import atan2
if 1:   # Custom imports
    import pylab as p
    from wrap import dedent
def PlotImpedance(Z, freq1, freq2, logfreq=True, logz=True, npoints=10000):
    '''The impedance Z in ohms must be a function that takes an
    angular frequency omega in radians/s as an argument and returns a
    complex number that is the impedance in ohms.  freq1 and freq2 are
    in Hz.  If logfreq is True, use a log axis for frequency.  If logz
    is True, use a log axis for the magnitude of Z. npoints is the
    number of points to plot.
    '''
    if not freq1 or not freq2 or freq1 >= freq2:
        raise ValueError("Bad frequency arguments")
    df = (freq2 - freq1)/npoints
    f = p.arange(freq1, freq2, df)
    W = 2*p.pi*f
    mag, phase = [], []
    for w in W:
        z = Z(w)
        mag.append(abs(z))
        phase.append(atan2(z.imag, z.real)*180/p.pi)
    # Plot the magnitude
    c = "b"
    if logfreq:
        if logz:
            p.loglog(f, mag, c)
        else:
            p.semilogx(f, mag, c)
    else:
        if logz:
            p.semilogy(f, mag, c)
        else:
            p.plot(f, mag, c)
    p.xlabel("Frequency, Hz")
    p.ylabel("|Z|, ohms")
    p.title("Impedance magnitude (blue) and phase (red)")
    p.grid()
    # Plot the phase on the right-hand axis
    ax = p.twinx()
    c = "r"
    p.plot(f, phase, c)
    p.ylabel('Phase, degrees')
    ax.yaxis.tick_right()
if __name__ == "__main__":
    # The following example is a real one where the model of a 1/3 hp
    # motor's winding is a resistor in series with a parallel L and C.
    # This model explained some LCR meter measurements where the
    # inductance went negative at 100 kHz; the capacitance is the
    # interwinding capacitance and becomes important at higher
    # frequencies (of course, you'd never see any issues with this at
    # line frequency operation of the motor).
    R = 6.1     # ohms
    L = 18e-3   # H
    C = 1e-9    # F
    def Z(w):
        return R + 1/(1/(1j*w*L) + 1/(1/(1j*w*C)))
    PlotImpedance(Z, 1e2, 1e6, logfreq=True, logz=True)
    p.show()

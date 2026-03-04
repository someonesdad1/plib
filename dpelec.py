
if 1:   # From util.py
    def AWG(n):
        '''Returns the wire diameter in inches given the AWG (American Wire Gauge) number (also known
        as the Brown and Sharpe gauge).  Use negative numbers as follows:
        
            00    -1
            000   -2
            0000  -3
            
        Reference:  the units.dat file with version 1.80 of the GNU units program gives the following
        statement:
        
            American Wire Gauge (AWG) or Brown & Sharpe Gauge appears to be the most important gauge.
            ASTM B-258 specifies that this gauge is based on geometric interpolation between gauge
            0000, which is 0.46 inches exactly, and gauge 36 which is 0.005 inches exactly.  Therefore,
            the diameter in inches of a wire is given by the formula
                    1|200 92^((36-g)/39).
            Note that 92^(1/39) is close to 2^(1/6), so diameter is approximately halved for every 6
            gauges.  For the repeated zero values, use negative numbers in the formula.  The same
            document also specifies rounding rules which seem to be ignored by makers of tables.
            Gauges up to 44 are to be specified with up to 4 significant figures, but no closer than
            0.0001 inch.  Gauges from 44 to 56 are to be rounded to the nearest 0.00001 inch.
            
        An equivalent formula is 0.32487/1.12294049**n where n is the gauge number (works for n >= 0).
        '''
        if n < -3 or n > 56:
            raise ValueError("AWG argument out of range")
        diameter = 92.0**((36 - n)/39)/200
        if n <= 44:
            return round(diameter, 4)
        return round(diameter, 5)
    def Ampacity(dia_mm, insul_degC=60, ambient_degC=30):
        '''Return the NEC-allowed current in a copper conductor at the indicated ambient temperature
        and with the indicated insulation temperature rating.
        
        The data from table 310-16 in the 1998 NEC was fitted to cubic polynomials, so the table data
        won't be reproduced exactly.  Thus, the intended use is to estimate safe currents for a given
        wire size, particularly smaller wires than are in the table.  To get the ampacity of a smaller
        wire, the constant term of the regression was set to zero.
        
        The data and regressions are in /elec/projects/current_capacity.
        '''
        def AmbientCorrection(ambient_degC, insul_degC):
            if insul_degC not in (60, 75, 90):
                raise ValueError("insul_degC must be 60, 75, or 90 °C")
            if insul_degC == 60:
                i = 0
            elif insul_degC == 75:
                i = 1
            elif insul_degC == 90:
                i = 2
            T = int(ambient_degC)
            if not (21 <= T <= 80):
                raise ValueError("ambient_degC must be between 21 and 80 °C")
            if 21 <= T <= 25:
                return (1.08, 1.05, 1.04)[i]
            elif 26 <= T <= 30:
                return 1
            elif 31 <= T <= 35:
                return (0.91, 0.94, 0.96)[i]
            elif 36 <= T <= 40:
                return (0.82, 0.88, 0.91)[i]
            elif 41 <= T <= 45:
                return (0.71, 0.82, 0.87)[i]
            elif 46 <= T <= 50:
                return (0.58, 0.75, 0.82)[i]
            elif 51 <= T <= 55:
                return (0.41, 0.67, 0.76)[i]
            elif 56 <= T <= 60:
                return (0, 0.58, 0.71)[i]
            elif 61 <= T <= 70:
                return (0, 0.33, 0.58)[i]
            elif 71 <= T <= 80:
                return (0, 0, 0.41)[i]
        max_dia_mm = 11.68
        if not (0 < dia_mm <= max_dia_mm):
            raise ValueError("dia_mm must be in (0, 11.68 mm]")
        if insul_degC not in (60, 75, 90):
            raise ValueError("insul_degC must be 60, 75, or 90 °C")
        constants = {
            60: (10.6841, 0.667284, -0.014032),
            75: (11.0919, 1.25111, -0.0445333),
            90: (12.9412, 1.30463, -0.0441503),
        }
        b1, b2, b3 = constants[insul_degC]
        correction = AmbientCorrection(ambient_degC, insul_degC)
        if correction:
            return correction*(b1*dia_mm + b2*dia_mm**2 + b3*dia_mm**3)
        else:
            raise ValueError("ambient_degC out of range")

if __name__ == "__main__":  
    import dpmath
    from lwtest import run, raises, Assert
    def Test_AWG():
        Assert(dpmath.AlmostEqual(AWG(12), 0.0808, 8e-4))
    def Test_Ampacity():
        dia_mm = 11.68
        i = Ampacity(dia_mm, insul_degC=60, ambient_degC=30)
        Assert(i == 193.46399267737598)
        i = Ampacity(dia_mm, insul_degC=75, ambient_degC=30)
        Assert(i == 229.27285356605438)
        i = Ampacity(dia_mm, insul_degC=90, ambient_degC=30)
        Assert(i == 258.78428183511033)
        # Test a derated value
        i = Ampacity(dia_mm, insul_degC=90, ambient_degC=21)
        Assert(i == 1.04*258.78428183511033)
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

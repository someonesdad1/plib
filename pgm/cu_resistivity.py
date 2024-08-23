'''
Plot the resistivity of copper as a function of temperature
'''
from pylab import *

rho0 = 17.241   # nΩ·m, internationally agreed to in early 1900's
T0 = 273.15     # 0 °C in K
if 0:
    # Print a table
    def Lin(T):
        return 5.3348e-2*T - 1.0205e-1
    def Rho(T):
        return 1.5699e-5*T**2 + Lin(T)
    T = 20 + 273.15
    print(f"{T:8.2f}   {Lin(T):6.3f}   {Rho(T):6.3f}")
    for T in range(300, 1360, 50):
        print(f"{T:8d}   {Lin(T):6.3f}   {Rho(T):6.3f}")
else:
    # Plot the resistivity
    #
    # Quadratic approximation from R. Berning and M. Coppinger, "An Exploding-Wire Circuit Model",
    # ARL-TR-8983, June 2020 (Weapons and Materials Research Directorate, CCDC Army Research
    # Laboratory)
    rho, rho_linear, T = [], [], []
    α = 0.00393
    for t in [298] + list(range(300, 1360, 10)):
        T.append(t - T0)
        rho.append(1.5699e-5*t**2 + 5.3348e-2*t - 1.0205e-1)
        rho_linear.append(rho0*(1 + α*(t - (T0 + 20))))
    plot(T, rho, "b-", label="Quadratic")
    # Linear model with temp coeff of 0.00393/K
    plot(T, rho_linear, "r-", label="Linear with α = 3.93/kK")
    legend(loc="lower right")
    grid()
    title("Resistivity of copper from 20 °C to melting point\n" 
          "/plib/pgm/cu_resistivity.py")
    xlabel("Temperature, °C")
    ylabel("Resistivity, nΩ·m")
    #text(100, 82, "ρ = 1.5699e-5*T² + 5.3348e-2*T - 1.0205e-1")
    text(100, 88, "At 20 °C, ρ = 17.241 nΩ·m"
        "\nρ = 0.000015699*T² + 0.053348*T - 0.10205"
        "\nT in K")
    if 0:
        show()
    else:
        savefig("copper_resistivity.png", dpi=200)

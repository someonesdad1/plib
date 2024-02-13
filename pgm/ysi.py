'''
Calculates temperature given the resistance in kΩ of the YSI
precision thermistor.  Accuracy is within 0.1 °C from -40 to 
108 °C and 0.33 °C from 109 °C to 150 °C.
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import thermistor
import sys

def PrintTemp(Rstr, resistance_kohm):
    R = resistance_kohm
    if not 0.551 <= R <= 885:
        print(f"Resistance needs to be in the range 0.551 kΩ to 883 kΩ")
        return
    th = thermistor.Thermistor()
    T_C = th.R_to_C(resistance_kohm)
    T_F = T_C*1.8 + 32
    T_K = T_C + 273.15
    T_R = T_C + 491.67
    sp = " "*4
    print(f"{R:6.2f} kΩ{sp}{T_C:5.1f} °C{sp}{T_F:5.1f} °F{sp}{T_K:5.1f} K{sp}{T_R:5.1f} °R")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"{sys.argv[0]} R1 [R2...]")
        for i in __doc__.strip().split("\n"):
            print(f"  {i}")
        exit(1)
    for resistance_kohm in sys.argv[1:]:
        PrintTemp(resistance_kohm, float(resistance_kohm))

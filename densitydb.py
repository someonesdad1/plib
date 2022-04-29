'''

- TODO
    - Use data from AIP Handbook
    - Provide page numbers for el and other references that are missing
      page numbers.
    - Make sure that categories can be gotten by typing in any suitable
      abbreviation of the string

    ----------------------------------------------------------------------
    Module to provide density data

    - Design goals
        - Default units kg/m3
        - Divide up into sets by reference
        - All entries are attributed
        - Include documentation
        - Density class?
            - Derive from float or flt
            - Nominal value is middle of range
            - Consider using interval arithmetic in class
            - Class variable 'sort' is a string which determines which
              attribute to sort on
        - You can decide at runtime which set of data you wish to have by
          calling SelectDensities()
            - List of reference strings to include in output.  density
              structure is then a tuple of density instances.

    - Notes
        - The references dictionary keys are strings like 'asm', 'aes',
          etc.  These are the reference materials I used in compiling these
          data.

'''

if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2005, 2013, 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Density of materials database
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard imports
        import sys
        import os
        import getopt
        import re
        from collections import defaultdict
        from pdb import set_trace as xx 
        from pprint import pprint as pp
    # Custom imports
        from wrap import dedent, wrap
        from f import flt
        from bidict import bidict
        from u import u, to, fromto, ParseUnit
        if len(sys.argv) > 1:
            import debug
            debug.SetDebugger()
        from get import GetLines
    # Global variables
        ii = isinstance
        class g:  pass      # Convenience to hold globals
if 1:   # Density information
    # The following density information came from a variety of sources.
    # See the material following this table for the details on the
    # references.
    g.raw_data = '''
    # Name                                           g/cc          Ref

    category = metal
    Alnico                                         ; 6.9-7.2     ; aes 308
    Alnico I                                       ; 6.89        ; asm 52
    Aluminum                                       ; 2.64        ; glo 390
    Aluminum                                       ; 2.698       ; tel 12
    Aluminum                                       ; 2.7         ; pht
    Aluminum                                       ; 2.70        ; aes 117
    Aluminum                                       ; 2.70        ; mhb 2270
    Aluminum bronze (3-10% Al)                     ; 7.7-8.7     ; sim
    Aluminum foil                                  ; 2.7-2.75    ; sim
    Aluminum, 2024 alloy                           ; 2.77        ; asm 52
    Aluminum, 5052 alloy                           ; 2.68        ; asm 52
    Aluminum, 6061 alloy                           ; 2.70        ; asm 52
    Aluminum, 99.996%                              ; 2.6989      ; asm 52
    Aluminum, liquid at melting point              ; 2.39        ; hcp B263
    Aluminum, melted                               ; 2.56-2.64   ; sim
    Antimony                                       ; 6.618       ; mhb 2270
    Antimony                                       ; 6.62        ; asm 52
    Antimony                                       ; 6.69        ; aes 117
    Antimony                                       ; 6.691       ; tel 16
    Antimony, cast                                 ; 6.696       ; sim
    Antimony, cast                                 ; 6.7         ; glo 390
    Babbitt                                        ; 7.272       ; sim
    Babbitt                                        ; 7.28        ; glo 390
    Babbitt, lead-based, SAE 13                    ; 10.24       ; asm 52
    Barium                                         ; 3.594       ; tel 24
    Barium                                         ; 3.78        ; glo 390
    Barium                                         ; 3.78        ; mhb 2270
    Barium                                         ; 3.78        ; sim
    Beryllium                                      ; 1.84        ; sim
    Beryllium                                      ; 1.8477      ; tel 28
    Beryllium                                      ; 1.848       ; asm 52
    Beryllium                                      ; 1.85        ; aes 117
    Beryllium copper                               ; 8.1-8.25    ; sim
    Beryllium copper                               ; 8.25        ; aes 118
    Beryllium wire                                 ; 1.85        ; aes 182
    Beryllium-copper                               ; 8.23        ; asm 52
    Bismuth                                        ; 9.747       ; tel 30
    Bismuth                                        ; 9.75        ; aes 117
    Bismuth                                        ; 9.781       ; mhb 2270
    Bismuth                                        ; 9.787       ; sim
    Bismuth                                        ; 9.79        ; glo 390
    Bismuth                                        ; 9.80        ; asm 52
    Boron                                          ; 2.535       ; mhb 2270
    Brass                                          ; 8.56        ; glo 390
    Brass, 50 Cu, 50 Zn                            ; 8.20        ; mhb 2270
    Brass, 60 Cu, 40 Zn                            ; 8.36        ; mhb 2270
    Brass, 70 Cu, 30 Zn                            ; 8.44        ; mhb 2270
    Brass, 80 Cu, 20 Zn                            ; 8.60        ; mhb 2270
    Brass, cartridge 70%                           ; 8.53        ; asm 52
    Brass, cast                                    ; 8.4-8.7     ; sim
    Brass, leaded free-machining                   ; 8.50        ; asm 52
    Brass, naval                                   ; 8.44        ; asm 52
    Brass, red (cast)                              ; 8.7         ; aes 118
    Brass, red 85%                                 ; 8.75        ; asm 52
    Brass, rolled and drawn                        ; 8.43-8.73   ; sim
    Brass, yellow (high brass)                     ; 8.47        ; aes 118
    Bronze                                         ; 8.16        ; glo 390
    Bronze (8-14% tin)                             ; 7.4-8.9     ; sim
    Bronze, 90 Cu, 10 Sn                           ; 8.78        ; mhb 2270
    Bronze, lead                                   ; 7.7-8.7     ; sim
    Bronze, phosphor                               ; 8.88        ; mar 6-7
    Bronze, phosphor, 8%                           ; 8.80        ; asm 52
    Bronze, phosphorous                            ; 8.78-8.92   ; sim
    Cadmium                                        ; 8.648       ; mhb 2270
    Cadmium                                        ; 8.65        ; aes 117
    Cadmium                                        ; 8.65        ; asm 52
    Cadmium                                        ; 8.65        ; glo 390
    Cadmium                                        ; 8.65        ; sim
    Cadmium                                        ; 8.650       ; tel 36
    Calcium                                        ; 1.54        ; mhb 2270
    Calcium                                        ; 1.55        ; asm 52
    Calcium                                        ; 1.550       ; tel 40
    Cerium                                         ; 6.771       ; aes 129
    Cerium (alpha)                                 ; 8.240       ; tel 46
    Cerium (beta)                                  ; 6.749       ; tel 46
    Cerium (delta)                                 ; 6.700       ; tel 46
    Cerium (gamma)                                 ; 6.773       ; tel 46
    Cesium                                         ; 1.873       ; tel 38
    Cesium                                         ; 1.903       ; asm 52
    Chrome, liquid at melting point                ; 6.46        ; hcp B263
    Chromel (90Ni-10Cr)                            ; 8.5         ; wkp
    Chromium                                       ; 6.856       ; sim
    Chromium                                       ; 6.86        ; glo 390
    Chromium                                       ; 6.93        ; mhb 2270
    Chromium                                       ; 7.19        ; asm 52
    Chromium                                       ; 7.190       ; tel 50
    Chromium                                       ; 7.2         ; aes 117
    Chromium                                       ; 7.20        ; aes 120
    Cobalt                                         ; 8.71        ; mhb 2270
    Cobalt                                         ; 8.746       ; sim
    Cobalt                                         ; 8.75        ; glo 390
    Cobalt                                         ; 8.85        ; asm 52
    Cobalt                                         ; 8.9         ; aes 117
    Cobalt                                         ; 8.9         ; aes 120
    Cobalt                                         ; 8.900       ; tel 52
    Cobalt, liquid at melting point                ; 7.67        ; hcp B263
    Constantan                                     ; 8.9         ; asm 52
    Constantan (cupronickel 55-45)                 ; 8.9         ; aes 118
    Copper                                         ; 8.89        ; mhb 2270
    Copper                                         ; 8.91        ; aes 118
    Copper                                         ; 8.93        ; sim
    Copper                                         ; 8.96        ; aes 117
    Copper                                         ; 8.96        ; pht
    Copper                                         ; 8.960       ; tel 54
    Copper ore, pyrites                            ; 4.1-4.3     ; mar 6-7
    Copper, OFHC (oxygen-free high conductivity)   ; 8.94        ; web
    Copper, cast                                   ; 8.69        ; glo 390
    Copper, cast or rolled                         ; 8.8-8.95    ; mar 6-7
    Copper, liquid at melting point                ; 7.94        ; hcp B263
    Copper, pure                                   ; 8.96        ; asm 52
    Copper, rolled                                 ; 8.91        ; glo 390
    Curium                                         ; 13.300      ; tel 56
    Delta metal (brass alloy:  55 Cu, 42 Zn, 2 Fe) ; 8.6         ; sim
    Dysprosium                                     ; 8.540       ; aes 129
    Dysprosium                                     ; 8.550       ; tel 58
    Electrum (40-50% gold, balance mostly silver)  ; 8.4-8.9     ; sim
    Erbium                                         ; 9.045       ; aes 129
    Erbium                                         ; 9.066       ; tel 62
    Europium                                       ; 5.243       ; tel 64
    Europium                                       ; 5.253       ; aes 129
    Gadolinium                                     ; 7.898       ; aes 129
    Gadolinium                                     ; 7.9004      ; tel 72
    Galena (lead ore, PbS)                         ; 7.3-7.6     ; mar 6-7
    Gallium                                        ; 5.907       ; asm 52
    Gallium                                        ; 5.907       ; tel 74
    German silver (nickel silver)                  ; 8.58        ; mar 6-7
    Germanium                                      ; 5.323       ; asm 52
    Gold                                           ; 19.3        ; mhb 2270
    Gold                                           ; 19.3        ; pht
    Gold                                           ; 19.32       ; aes 117
    Gold                                           ; 19.32       ; asm 52
    Gold                                           ; 19.32       ; sim
    Gold                                           ; 19.320      ; tel 78
    Gold coin, US                                  ; 17.18-17.2  ; mar 6-7
    Gold, liquid at melting point                  ; 17.3        ; hcp B263
    Gold, pure                                     ; 19.29       ; glo 390
    Hafnium                                        ; 13.1        ; asm 52
    Hafnium                                        ; 13.3        ; aes 120
    Hafnium                                        ; 13.310      ; tel 80
    Holmium                                        ; 8.781       ; aes 129
    Holmium                                        ; 8.795       ; tel 84
    Inconel X (Ni-Cr-Fe alloy)                     ; 8.30        ; asm 52
    Inconel(Ni-Cr-Fe alloy)                        ; 8.51        ; asm 52
    Indium                                         ; 7.31        ; asm 52
    Indium                                         ; 7.310       ; tel 88
    Iridium                                        ; 22.15       ; sim
    Iridium                                        ; 22.16       ; glo 390
    Iridium                                        ; 22.4        ; aes 120
    Iridium                                        ; 22.4        ; pht
    Iridium                                        ; 22.42       ; aes 117
    Iridium                                        ; 22.42       ; mhb 2270
    Iridium                                        ; 22.420      ; tel 82
    Iridium                                        ; 22.5        ; asm 52
    Iron                                           ; 7.85        ; sim
    Iron                                           ; 7.87        ; aes 117
    Iron                                           ; 7.87        ; aes 120
    Iron                                           ; 7.87        ; pht
    Iron                                           ; 7.874       ; tel 84
    Iron, cast                                     ; 6.8-7.8     ; sim
    Iron, cast                                     ; 7.03-7.73   ; mhb 2270
    Iron, cast                                     ; 7.2         ; aes 118
    Iron, cast                                     ; 7.21        ; glo 390
    Iron, cast gray                                ; 6.95-7.35   ; asm 52
    Iron, gray cast                                ; 7.03-7.13   ; mar 6-7
    Iron, ingot                                    ; 7.866       ; asm 52
    Iron, liquid at melting point                  ; 7.03        ; hcp B263
    Iron, malleable                                ; 7.2-7.34    ; asm 52
    Iron, malleable                                ; 7.32        ; aes 118
    Iron, pure                                     ; 7.874       ; asm 52
    Iron, wrought                                  ; 7.77        ; glo 390
    Iron, wrought                                  ; 7.80-7.90   ; mhb 2270
    Kovar (29% Ni, 17% Co, bal. Fe)                ; 8.36        ; hcp F159
    Lanthanum                                      ; 6.145       ; tel 98
    Lanthanum                                      ; 6.166       ; aes 129
    Lead                                           ; 11.34       ; mar 6-7
    Lead                                           ; 11.34       ; sim
    Lead                                           ; 11.342      ; mhb 2270
    Lead                                           ; 11.35       ; aes 117
    Lead                                           ; 11.35       ; pht
    Lead                                           ; 11.350      ; tel 102
    Lead 99.9%                                     ; 11.34       ; asm 52
    Lead, antimonial (hard)                        ; 10.9        ; aes 118
    Lead, cast                                     ; 11.35       ; glo 390
    Lead, chemical                                 ; 11.35       ; aes 118
    Lead, hard 4% Sb                               ; 11.04       ; asm 52
    Lead, hard 6% Sb                               ; 10.88       ; asm 52
    Lead, hard 8% Sb                               ; 10.74       ; asm 52
    Lead, hard 9% Sb                               ; 10.66       ; asm 52
    Lead, liquid at melting point                  ; 10.678      ; hcp B263
    Lead, rolled                                   ; 11.39       ; glo 390
    Lead, rolled                                   ; 11.39       ; sim
    Lithium                                        ; .534        ; tel 104
    Lithium                                        ; 0.534       ; asm 52
    Lithium                                        ; 0.534       ; pht
    Lutetium                                       ; 9.835       ; aes 129
    Lutetium                                       ; 9.840       ; tel 106
    Magnesium                                      ; 1.738       ; tel 108
    Magnesium                                      ; 1.738       ; sim
    Magnesium                                      ; 1.74        ; aes 117
    Magnesium                                      ; 1.741       ; mhb 2270
    Magnesium                                      ; 1.75        ; glo 390
    Magnesium, liquid at melting point             ; 1.57        ; hcp B263
    Manganese                                      ; 7.3         ; mhb 2270
    Manganese                                      ; 7.42        ; mar 6-7
    Manganese                                      ; 7.43        ; asm 52
    Manganese                                      ; 7.440       ; tel 110
    Manganese                                      ; 7.609       ; sim
    Manganese                                      ; 7.61        ; glo 390
    Manganese (3 allotropes)                       ; 7.21-7.44   ; aes 117
    Mercury                                        ; 13.546      ; aes 117
    Mercury                                        ; 13.546      ; asm 52
    Mercury                                        ; 13.546      ; tel 114
    Mercury                                        ; 13.59       ; sim
    Mercury                                        ; 13.594      ; pht
    Mercury (-10 °C)                               ; 13.6202     ; hcp F4
    Mercury (0 °C)                                 ; 13.5955     ; hcp F4
    Mercury (10 °C)                                ; 13.5708     ; hcp F4
    Mercury (100 °C)                               ; 13.352      ; asm 1215
    Mercury (100 °C)                               ; 13.3522     ; hcp F4
    Mercury (15 °C)                                ; 13.5585     ; hcp F4
    Mercury (200 °C)                               ; 13.1148     ; hcp F4
    Mercury (200 °C)                               ; 13.115      ; asm 1215
    Mercury (25 °C)                                ; 13.5340     ; hcp F4
    Mercury (30 °C)                                ; 13.5217     ; hcp F4
    Mercury (300 °C)                               ; 12.8806     ; hcp F4
    Mercury (300 °C)                               ; 12.881      ; asm 1215
    Mercury (35 °C)                                ; 13.5095     ; hcp F4
    Mercury (40 °C)                                ; 13.4973     ; hcp F4
    Mercury (50 °C)                                ; 13.4729     ; hcp F4
    Mercury (68 F)                                 ; 13.546      ; mhb 2270
    Mercury 20 °C                                  ; 13.5462     ; hcp F4
    Mercury 25 °C                                  ; 13.633      ; aes 90
    Mercury at 0 deg °C                            ; 13.61       ; glo 390
    Molybdenum                                     ; 10.19       ; glo 390
    Molybdenum                                     ; 10.19       ; sim
    Molybdenum                                     ; 10.2        ; mhb 2270
    Molybdenum                                     ; 10.22       ; aes 117
    Molybdenum                                     ; 10.22       ; asm 52
    Molybdenum                                     ; 10.220      ; tel 116
    Molybdenum, liquid at melting point            ; 9.33        ; hcp B263
    Molydenum                                      ; 10.2        ; aes 120
    Monel (Ni-Cu alloy)                            ; 8.36-8.84   ; sim
    Monel (Ni-Cu alloy)                            ; 8.47        ; aes 118
    Monel (Ni-Cu alloy)                            ; 8.84        ; asm 52
    Monel (Ni-Cu alloy), cast                      ; 8.63        ; asm 52
    Monel, rolled                                  ; 8.97        ; mar 6-7
    Mu metal (high-permeability alloy)             ; 8.58        ; hcp E121
    Neodymium                                      ; 7.003       ; aes 129
    Neodymium                                      ; 7.007       ; tel 118
    Nichrome, 80 Ni, 20 Cr, 108 uohm-cm            ; 8.4         ; asm 52
    Nickel                                         ; 8.8         ; mhb 2270
    Nickel                                         ; 8.8         ; sim
    Nickel                                         ; 8.89        ; aes 118
    Nickel                                         ; 8.9         ; aes 120
    Nickel                                         ; 8.9         ; mar 6-7
    Nickel                                         ; 8.9         ; pht
    Nickel                                         ; 8.90        ; aes 117
    Nickel                                         ; 8.902       ; tel 124
    Nickel silver                                  ; 8.4-8.9     ; sim
    Nickel silver                                  ; 8.442       ; sim
    Nickel silver                                  ; 8.45        ; glo 390
    Nickel silver                                  ; 8.8         ; aes 118
    Nickel silver, 55-18                           ; 8.70        ; asm 52
    Nickel silver, 65-18                           ; 8.73        ; asm 52
    Nickel silver, Cu-Ni-Zn alloy                  ; 8.58        ; mar 6-7
    Nickel, liquid at melting point                ; 7.78        ; hcp B263
    Nickel, rolled                                 ; 8.666       ; sim
    Nickel, rolled                                 ; 8.67        ; glo 390
    Niobium                                        ; 8.57        ; aes 117
    Niobium                                        ; 8.57        ; aes 120
    Niobium                                        ; 8.57        ; asm 52
    Niobium                                        ; 8.57        ; web
    Niobium                                        ; 8.570       ; tel 126
    Osmium                                         ; 22.5        ; pht
    Osmium                                         ; 22.57       ; aes 117
    Osmium                                         ; 22.583      ; asm 52
    Osmium                                         ; 22.590      ; tel 132
    Osmium                                         ; 22.6        ; aes 120
    Palladium                                      ; 12.0        ; aes 120
    Palladium                                      ; 12.02       ; asm 52
    Palladium                                      ; 12.020      ; tel 136
    Permalloy 45 (high-permeability alloy)         ; 8.17        ; hcp E121
    Platinum                                       ; 21.37       ; mhb 2270
    Platinum                                       ; 21.4        ; sim
    Platinum                                       ; 21.45       ; aes 117
    Platinum                                       ; 21.45       ; asm 52
    Platinum                                       ; 21.45       ; pht
    Platinum                                       ; 21.450      ; tel 140
    Platinum                                       ; 21.5        ; aes 120
    Platinum                                       ; 21.51       ; glo 390
    Platinum - 10% Rh (thermocouple material)      ; 19.97       ; asm 52
    Platinum - 3.5% Rh (thermocouple material)     ; 20.9        ; asm 52
    Plutonium                                      ; 19.8        ; sim
    Plutonium                                      ; 19.84       ; aes 117
    Plutonium                                      ; 19.84       ; asm 52
    Plutonium                                      ; 19.840      ; tel 142
    Plutonium, alpha                               ; 19.86       ; pht
    Potassium                                      ; .86         ; aes 117
    Potassium                                      ; .862        ; tel 146
    Potassium                                      ; .870        ; mhb 2270
    Potassium                                      ; 0.86        ; asm 52
    Praseodymium                                   ; 6.772       ; aes 129
    Praseodymium                                   ; 6.773       ; tel 148
    Rhenium                                        ; 21.0        ; aes 120
    Rhenium                                        ; 21.020      ; tel 158
    Rhenium                                        ; 21.04       ; asm 52
    Rhodium                                        ; 12.4        ; aes 120
    Rhodium                                        ; 12.41       ; aes 117
    Rhodium                                        ; 12.410      ; tel 160
    Rhodium                                        ; 12.44       ; asm 52
    Rubidium                                       ; 1.532       ; tel 162
    Ruthenium                                      ; 12.2        ; asm 52
    Ruthenium                                      ; 12.370      ; tel 164
    Ruthenium                                      ; 12.4        ; aes 120
    Samarium                                       ; 7.520       ; tel 166
    Samarium                                       ; 7.537       ; aes 129
    Scandium                                       ; 2.989       ; aes 129
    Scandium                                       ; 2.989       ; tel 168
    Selenium                                       ; 4.79        ; asm 52
    Selenium                                       ; 4.790       ; tel 170
    Selenium                                       ; 4.8         ; aes 117
    Silicon                                        ; 2.329       ; tel 172
    Silicon                                        ; 2.33        ; aes 117
    Silicon                                        ; 2.33        ; asm 52
    Silicon, liquid at melting point               ; 2.52        ; hcp B263
    Silver                                         ; 10.42-10.53 ; mhb 2270
    Silver                                         ; 10.46       ; glo 390
    Silver                                         ; 10.49       ; asm 52
    Silver                                         ; 10.49       ; pht
    Silver                                         ; 10.49       ; sim
    Silver                                         ; 10.50       ; aes 117
    Silver                                         ; 10.500      ; tel 174
    Silver, liquid at melting point                ; 9.33        ; hcp B263
    Sodium                                         ; .97         ; aes 117
    Sodium                                         ; .971        ; tel 176
    Sodium                                         ; .9712       ; mhb 2270
    Sodium                                         ; .977        ; sim
    Sodium                                         ; .98         ; glo 390
    Sodium                                         ; 0.97        ; asm 52
    Sodium, liquid at melting point                ; .938        ; hcp B263
    Solder, 35 Sn, 65 Pb                           ; 9.50        ; mhb 2196
    Solder, 50 Sn, 50 Pb                           ; 8.85        ; mhb 2196
    Solder, 50-50                                  ; 8.89        ; aes 118
    Solder, 63 Pb, 37 Sn eutectic                  ; 8.42        ; asm 52
    Solder, 63 Pb, 37 Sn eutectic                  ; 8.40        ; mhb 2196
    Solder, 70 Sn, 30 Pb                           ; 8.32        ; mhb 2196
    Steel, 304 stainless                           ; 8.02        ; aes 118
    Steel, cast                                    ; 7.85        ; glo 390
    Steel, low-carbon Cr-Mo                        ; 7.86        ; asm 52
    Steel, plain carbon, 1020                      ; 7.86        ; aes 118
    Steel, rolled                                  ; 7.85        ; sim
    Steel, rolled                                  ; 7.93        ; glo 390
    Steel, stainless                               ; 7.48-8.     ; sim
    Steel, stainless, 17-4PH                       ; 7.8         ; asm 52
    Steel, stainless, 303 & 304                    ; 7.9         ; asm 52
    Steel, stainless, 316                          ; 8.0         ; asm 52
    Steel, stainless, 440                          ; 7.7         ; asm 52
    Steel, tool, M2 (high-speed steel)             ; 8.16        ; asm 52
    Strontium                                      ; 2.540       ; tel 178
    Tantalum                                       ; 16.6        ; aes 117
    Tantalum                                       ; 16.6        ; aes 120
    Tantalum                                       ; 16.6        ; asm 52
    Tantalum                                       ; 16.6        ; mhb 2270
    Tantalum                                       ; 16.654      ; tel 182
    Tellurium                                      ; 6.240       ; tel 186
    Tellurium                                      ; 6.25        ; mhb 2270
    Terbium                                        ; 8.229       ; tel 188
    Terbium                                        ; 8.234       ; aes 129
    Thallium                                       ; 11.85       ; asm 52
    Thallium                                       ; 11.850      ; tel 190
    Thorium                                        ; 11.7        ; aes 117
    Thorium                                        ; 11.7        ; aes 120
    Thorium                                        ; 11.72       ; asm 52
    Thorium                                        ; 11.720      ; tel 182
    Thulium                                        ; 9.314       ; aes 129
    Thulium                                        ; 9.321       ; tel 194
    Tin                                            ; 7.28        ; sim
    Tin                                            ; 7.29        ; mhb 2270
    Tin                                            ; 7.31        ; aes 117
    Tin (alpha)                                    ; 5.750       ; tel 196
    Tin (beta) (common form)                       ; 7.310       ; tel 196
    Tin, cast                                      ; 7.36        ; glo 390
    Tin, liquid at melting point                   ; 7.0         ; hcp B263
    Tin, pure                                      ; 7.3         ; asm 52
    Titanium                                       ; 4.5         ; mhb 2270
    Titanium                                       ; 4.5         ; pht
    Titanium                                       ; 4.5         ; sim
    Titanium                                       ; 4.54        ; aes 117
    Titanium                                       ; 4.54        ; aes 120
    Titanium                                       ; 4.540       ; tel 198
    Titanium, 99.9%                                ; 4.507       ; asm 52
    Titanium, commercial                           ; 5.          ; aes 118
    Tungsten                                       ; 18.6-19.1   ; mhb 2270
    Tungsten                                       ; 19.3        ; aes 117
    Tungsten                                       ; 19.3        ; aes 120
    Tungsten                                       ; 19.3        ; asm 52
    Tungsten                                       ; 19.3        ; pht
    Tungsten                                       ; 19.300      ; tel 200
    Tungsten                                       ; 19.6        ; sim
    Tungsten                                       ; 19.62       ; glo 390
    Tungsten, filament                             ; 19.3        ; aes 182
    Uranium                                        ; 18.7        ; mhb 2270
    Uranium                                        ; 18.8        ; aes 117
    Uranium                                        ; 18.9        ; sim
    Uranium                                        ; 18.950      ; tel 202
    Uranium                                        ; 19.05       ; pht
    Uranium                                        ; 19.07       ; asm 52
    Vanadium                                       ; 5.494       ; sim
    Vanadium                                       ; 5.50        ; glo 390
    Vanadium                                       ; 5.6         ; mhb 2270
    Vanadium                                       ; 6.1         ; aes 117
    Vanadium                                       ; 6.1         ; aes 120
    Vanadium                                       ; 6.1         ; asm 52
    Vanadium                                       ; 6.110       ; tel 204
    Ytterbium                                      ; 6.965       ; tel 208
    Ytterbium                                      ; 6.972       ; aes 129
    Yttrium                                        ; 4.457       ; aes 129
    Yttrium                                        ; 4.469       ; tel 210
    Zinc                                           ; 7           ; aes 117
    Zinc                                           ; 7.04-7.16   ; mhb 2270
    Zinc                                           ; 7.133       ; tel 212
    Zinc                                           ; 7.135       ; sim
    Zinc                                           ; 7.14        ; aes 118
    Zinc                                           ; 7.14        ; pht
    Zinc, cast                                     ; 7.05        ; glo 390
    Zinc, commercial rolled                        ; 7.14        ; asm 52
    Zinc, liquid at melting point                  ; 6.64        ; hcp B263
    Zinc, pure                                     ; 7.133       ; asm 52
    Zirconium                                      ; 6.5         ; asm 52
    Zirconium                                      ; 6.506       ; tel 214
    Zirconium                                      ; 6.53        ; aes 120
    Zirconium, commercial                          ; 6.5         ; aes 118

    category = liquid
    1,1,2-Trichlorotrifluoroethane 25 °C            ; 1.564       ; sim
    1,2,4-Trichlorobenzene 20 °C                    ; 1.454       ; sim
    1,4-Dioxane 20 °C                               ; 1.034       ; sim
    2-Methoxyethanol 20 °C                          ; .9646       ; sim
    Acetic acid                                    ; 1.049       ; aes 90
    Acetic acid 25 °C                               ; 1.049       ; sim
    Acetic acid, 100%                              ; 1.06        ; ceh 3-83
    Acetic acid, 15%                               ; 1.0213      ; aes 370
    Acetic acid, 30%                               ; 1.0403      ; aes 370
    Acetic acid, 35%                               ; 1.0457      ; aes 370
    Acetic acid, 4%                                ; 1.0058      ; aes 370
    Acetic acid, 8%                                ; 1.0115      ; aes 370
    Acetic acid, 90%                               ; 1.06        ; glo 390
    Acetone                                        ; .787        ; aes 90
    Acetone                                        ; .79         ; aes 353
    Acetone                                        ; 0.79        ; pht
    Acetone 25 °C                                   ; .7846       ; sim
    Acetonitrile 20 °C                              ; .7822       ; sim
    Acid, acetic (CH₃COOH)                         ; 1.05        ; pht
    Acid, sulfuric (H₂SO₄)                         ; 1.39        ; pht
    Air (liquid, bp = 79 K)                        ; .875        ; aes 97
    Alcohol, butyl                                 ; .81         ; aes 353
    Alcohol, denatured (methanol)                  ; .79         ; aes 353
    Alcohol, ethyl                                 ; .787        ; aes 90
    Alcohol, ethyl                                 ; .789        ; glo 390
    Alcohol, ethyl                                 ; .789        ; mar 6-7
    Alcohol, ethyl (grain)                         ; 0.7892      ; pht
    Alcohol, ethyl 25 °C                            ; .7851       ; sim
    Alcohol, isopropyl (2-propanol)                ; .79         ; aes 353
    Alcohol, isopropyl (rubbing)                   ; 0.7854      ; pht
    Alcohol, methyl                                ; .789        ; aes 90
    Alcohol, methyl                                ; .791        ; glo 390
    Alcohol, methyl                                ; .796        ; mar 6-7
    Alcohol, methyl (methanol)                     ; .79         ; aes 353
    Alcohol, methyl (wood)                         ; 0.7913      ; pht
    Alcohol, methyl 25 °C                           ; .7865       ; sim
    Alcohol, propyl                                ; .802        ; aes 90
    Alcohol, propyl 25 °C                           ; .8          ; sim
    Alcohol, wood (methanol)                       ; .79         ; aes 353
    Ammonia                                        ; 0.771       ; pht
    Ammonia (aqua) 25 °C                            ; .8234       ; sim
    Amyl acetate (banana oil)                      ; .88         ; aes 353
    Analine 25 °C                                   ; 1.019       ; sim
    Argon (liquid, bp = 87 K)                      ; 1.403       ; aes 97
    Automobile oils 15 °C                           ; .88-.94     ; sim
    Beer (varies) 10 °C                             ; 1.01        ; sim
    Beer, pilsner, 4 °C                             ; 1.008       ; pht
    Benzene                                        ; .876        ; aes 90
    Benzene                                        ; 0.87        ; pht
    Benzene 25 °C                                   ; .8738       ; sim
    Benzil 25 °C                                    ; 1.08        ; sim
    Blood                                          ; 1.035       ; pht
    Bromine 25 °C                                   ; 3.12        ; sim
    Butane                                         ; 0.551       ; pht
    Butane 25 °C                                    ; .5991       ; sim
    Butyric acid 20 °C                              ; .959        ; sim
    Caproic acid 25 °C                              ; .9211       ; sim
    Carbolic acid 15 °C                             ; .9563       ; sim
    Carbon disulfide                               ; 1.265       ; aes 90
    Carbon disulfide 25 °C                          ; 1.261       ; sim
    Carbon tetrachloride                           ; 1.59        ; aes 90
    Carbon tetrachloride 25 °C                      ; 1.584       ; sim
    Carene 25 °C                                    ; .857        ; sim
    Castor oil                                     ; .96         ; aes 90
    Castor oil 25 °C                                ; .9561       ; sim
    Chloride 25 °C                                  ; 1.56        ; sim
    Chlorobenzene 20 °C                             ; 1.106       ; sim
    Chloroform                                     ; 1.47        ; aes 90
    Chloroform                                     ; 1.500       ; mar 6-7
    Chloroform                                     ; 1.52        ; glo 390
    Chloroform                                     ; 1.522       ; sim
    Chloroform 20 °C                                ; 1.489       ; sim
    Chloroform 25 °C                                ; 1.465       ; sim
    Citric acid 25 °C                               ; 1.66        ; sim
    Coconut oil 15 °C                               ; .9243       ; sim
    Corn syrup                                     ; 1.38        ; pht
    Cotton seed oil 15 °C                           ; .9259       ; sim
    Creosote 15 °C                                  ; 1.067       ; sim
    Cresol 25 °C                                    ; 1.024       ; sim
    Crude oil                                      ; .76-.85     ; hep 43
    Crude oil, 32.6 deg API 60 F                   ; .862        ; sim
    Crude oil, 35.6 deg API 60 F                   ; .847        ; sim
    Crude oil, 40 deg API 60 F                     ; .825        ; sim
    Crude oil, 48 deg API 60 F                     ; .79         ; sim
    Crude oil, California 60 F                     ; .915        ; sim
    Crude oil, Mexican 60 F                        ; .973        ; sim
    Crude oil, Texas 60 F                          ; .873        ; sim
    Cumene 25 °C                                    ; .8602       ; sim
    Cyclohexane 20 °C                               ; .7785       ; sim
    Cyclopentane 20 °C                              ; .7454       ; sim
    Decane                                         ; .728        ; aes 90
    Decane 25 °C                                    ; .7263       ; sim
    Dichloromethane 20 °C                           ; 1.326       ; sim
    Diesel                                         ; 0.8         ; pht
    Diesel fuel oil 20 to 60 15 °C                  ; .82-.95     ; sim
    Diesel oil, #1                                 ; .875        ; aes 389
    Diesel oil, #2                                 ; .920        ; aes 389
    Diesel oil, #4                                 ; .960        ; aes 389
    Diethyl ether 20 °C                             ; .714        ; sim
    Diethylene glycol 15 °C                         ; 1.12        ; sim
    Dimethyl acetamide 20 °C                        ; .9415       ; sim
    Dimethyl sulfoxide 20 °C                        ; 1.1         ; sim
    Dodecane 25 °C                                  ; .7546       ; sim
    Ethane (liquid, bp = 185 K)                    ; .548        ; aes 97
    Ethane -89 °C                                   ; .5703       ; sim
    Ether                                          ; .715        ; aes 90
    Ether                                          ; .736        ; mar 6-7
    Ether                                          ; .737        ; sim
    Ether                                          ; .74         ; glo 390
    Ethyl acetate 20 °C                             ; .9006       ; sim
    Ethyl alcohol 20 °C                             ; .7892       ; sim
    Ethyl ether 20 °C                               ; .7133       ; sim
    Ethylamine 16 °C                                ; .6808       ; sim
    Ethylene dichloride 20 °C                       ; 1.253       ; sim
    Ethylene glycol                                ; 1.100       ; aes 90
    Ethylene glycol 25 °C                           ; 1.097       ; sim
    Fish oil                                       ; .93         ; aes 353
    Fluorine (liquid, bp = 85 K)                   ; 1.50        ; aes 97
    Fluorine refrigerant R-12 25 °C                 ; 1.311       ; sim
    Formaldehyde                                   ; 1.13        ; pht
    Formaldehyde 45 °C                              ; .8121       ; sim
    Formic acid 10% concentration 20 °C             ; 1.025       ; sim
    Formic acid 80% concentration 20 °C             ; 1.221       ; sim
    Freon - 11 21 °C                                ; 1.49        ; sim
    Freon - 21 21 °C                                ; 1.37        ; sim
    Freon 12, liquid                               ; 1.311       ; pht
    Fuel oil 60 F                                  ; .8901       ; sim
    Furan 25 °C                                     ; 1.416       ; sim
    Furforol 25 °C                                  ; 1.155       ; sim
    Gas oils 60 F                                  ; .89         ; sim
    Gasoline                                       ; .68-.72     ; hep 43
    Gasoline                                       ; .71-.77     ; wkp
    Gasoline                                       ; 0.803       ; pht
    Gasoline, natural 60 F                         ; .7112       ; sim
    Gasoline, vehicle 60 F                         ; .7372       ; sim
    Glucose 60 F                                   ; 1.35-1.44   ; sim
    Glycerin (glycerol) 25 °C                       ; 1.259       ; sim
    Glycerin (glycerol)                            ; 1.26        ; hep 43
    Glycerin (glycerol)                            ; 1.26        ; pht
    Glycerin (glycerol) 25 °C                       ; 1.126       ; sim
    Glyme 20 °C                                     ; .8691       ; sim
    Helium 3 (liquid, bp = 3.2 K)                  ; .0589       ; aes 97
    Helium 4 (liquid, bp = 4.215 K)                ; .125        ; aes 97
    Helium, liquid, 4 K                            ; 0.147       ; pht
    Heptane 25 °C                                   ; .6795       ; sim
    Hexane 25 °C                                    ; .6548       ; sim
    Hexanol 25 °C                                   ; .8105       ; sim
    Hexene 25 °C                                    ; .6712       ; sim
    Honey                                          ; 1.42        ; pht
    Hydrazine 25 °C                                 ; .7945       ; sim
    Hydrochloric acid 40%                          ; 1.201       ; sim
    Hydrochloric acid, 15%                         ; 1.0746      ; aes 370
    Hydrochloric acid, 30%                         ; 1.1510      ; aes 370
    Hydrochloric acid, 35%                         ; 1.1759      ; aes 370
    Hydrochloric acid, 4%                          ; 1.0198      ; aes 370
    Hydrochloric acid, 40%                         ; 1.2         ; glo 390
    Hydrochloric acid, 40%                         ; 1.2         ; mar 6-7
    Hydrochloric acid, 8%                          ; 1.0395      ; aes 370
    Hydrogen (H2), liquid, 17 K                    ; 0.071       ; pht
    Hydrogen (liquid, bp = 20 K)                   ; .071        ; aes 97
    Hydrogen (solid < 14 K)                        ; .086        ; wkp
    Iodine 25 °C                                    ; 4.927       ; sim
    Ionene 25 °C                                    ; .9323       ; sim
    Iso-octane 20 °C                                ; .6919       ; sim
    Isobutyl alcohol 20 °C                          ; .8016       ; sim
    Isopropyl alcohol 20 °C                         ; .7854       ; sim
    Isopropyl myristate 20 °C                       ; .8532       ; sim
    Kerosene                                       ; .78-.82     ; mar 6-7
    Kerosene                                       ; .823        ; aes 90
    Kerosene                                       ; .825        ; aes 389
    Kerosene                                       ; 0.81        ; pht
    Kerosene 60 F                                  ; .8171       ; sim
    Linolenic acid 25 °C                            ; .8986       ; sim
    Linseed (flax) oil, boiled                     ; .95         ; aes 353
    Linseed (flax) oil, brown                      ; .97         ; aes 353
    Linseed (flax) oil, raw                        ; .93         ; aes 353
    Linseed oil                                    ; .93         ; aes 90
    Linseed oil 25 °C                               ; .9291       ; sim
    Lye, 66% solution in water                     ; 1.70        ; mar 6-7
    Machine oil                                    ; .9          ; hep 43
    Methane (liquid, bp = 111 K)                   ; .424        ; aes 97
    Methane -164 °C                                 ; .4645       ; sim
    Methane, liquid, -90 °C                         ; 0.162       ; pht
    Methanol 20 °C                                  ; .7913       ; sim
    Methyl ethyl ketone (MEK) 20 °C                 ; .8049       ; sim
    Methyl ethyl ketone (MEK) 25 °C                 ; .8025       ; sim
    Methyl isoamyl ketone 20 °C                     ; .888        ; sim
    Methyl isobutyl ketone 20 °C                    ; .8008       ; sim
    Methyl n-propyl ketone 20 °C                    ; .8082       ; sim
    Methyl t-butyl ether 20 °C                      ; .7405       ; sim
    Milk 15 °C                                      ; 1.02-1.05   ; sim
    Milk of average fat content                    ; 1.03        ; hep 43
    Milk, cow, heavy cream                         ; 0.994       ; pht
    Milk, cow, light cream                         ; 1.012       ; pht
    Milk, cow, skim                                ; 1.033       ; pht
    Milk, cow, whole                               ; 1.03        ; pht
    Mineral spirits (Stoddard solvent)             ; .66         ; aes 353
    N,N-Dimethylformamide 20 °C                     ; .9487       ; sim
    N-Methylpyrrolidone 20 °C                       ; 1.03        ; sim
    NaCl in water (salt brine), 15%                ; 1.1105      ; aes 370
    NaCl in water (salt brine), 25%                ; 1.1909      ; aes 370
    NaCl in water (salt brine), 4%                 ; 1.0286      ; aes 370
    NaCl in water (salt brine), 8%                 ; 1.0578      ; aes 370
    NaCl in water 20 °C (salt brine), 0.5%          ; 1.0036      ; hcp D299
    NaCl in water 20 °C (salt brine), 1%            ; 1.0071      ; hcp D299
    NaCl in water 20 °C (salt brine), 10%           ; 1.0726      ; hcp D300
    NaCl in water 20 °C (salt brine), 11%           ; 1.0801      ; hcp D300
    NaCl in water 20 °C (salt brine), 12%           ; 1.0876      ; hcp D300
    NaCl in water 20 °C (salt brine), 13%           ; 1.0952      ; hcp D300
    NaCl in water 20 °C (salt brine), 14%           ; 1.1028      ; hcp D300
    NaCl in water 20 °C (salt brine), 15%           ; 1.1105      ; hcp D300
    NaCl in water 20 °C (salt brine), 16%           ; 1.1182      ; hcp D300
    NaCl in water 20 °C (salt brine), 17%           ; 1.1260      ; hcp D300
    NaCl in water 20 °C (salt brine), 18%           ; 1.1339      ; hcp D300
    NaCl in water 20 °C (salt brine), 19%           ; 1.1418      ; hcp D300
    NaCl in water 20 °C (salt brine), 2%            ; 1.0143      ; hcp D299
    NaCl in water 20 °C (salt brine), 20%           ; 1.1498      ; hcp D300
    NaCl in water 20 °C (salt brine), 21%           ; 1.1579      ; hcp D300
    NaCl in water 20 °C (salt brine), 22%           ; 1.1660      ; hcp D300
    NaCl in water 20 °C (salt brine), 23%           ; 1.1742      ; hcp D300
    NaCl in water 20 °C (salt brine), 24%           ; 1.1825      ; hcp D300
    NaCl in water 20 °C (salt brine), 25%           ; 1.1909      ; hcp D300
    NaCl in water 20 °C (salt brine), 26%           ; 1.1993      ; hcp D300
    NaCl in water 20 °C (salt brine), 3%            ; 1.0214      ; hcp D299
    NaCl in water 20 °C (salt brine), 4%            ; 1.0286      ; hcp D300
    NaCl in water 20 °C (salt brine), 5%            ; 1.0358      ; hcp D300
    NaCl in water 20 °C (salt brine), 6%            ; 1.0431      ; hcp D300
    NaCl in water 20 °C (salt brine), 7%            ; 1.0504      ; hcp D300
    NaCl in water 20 °C (salt brine), 8%            ; 1.0578      ; hcp D300
    NaCl in water 20 °C (salt brine), 9%            ; 1.0651      ; hcp D300
    Naphtha 15 °C (lighter fluid, camp stove fuel)  ; .6648       ; sim
    Naphtha, wood 25 °C                             ; .9595       ; sim
    Naptha, aromatic (lighter fluid)               ; .85         ; aes 353
    Napthalene 25 °C                                ; .8201       ; sim
    Neon (liquid, bp = 111 K)                      ; 1.205       ; aes 97
    Nitric acid, 15%                               ; 1.0861      ; aes 370
    Nitric acid, 30%                               ; 1.1822      ; aes 370
    Nitric acid, 35%                               ; 1.2158      ; aes 370
    Nitric acid, 4%                                ; 1.0219      ; aes 370
    Nitric acid, 8%                                ; 1.0446      ; aes 370
    Nitric acid, 91%                               ; 1.5         ; mar 6-7
    Nitric acid, 91%                               ; 1.506       ; sim
    Nitric acid, 91%                               ; 1.51        ; glo 390
    Nitrobenzene                                   ; 1.2         ; hep 43
    Nitrogen (liquid, bp = 77.4 K)                 ; .810        ; aes 97
    Nitrogen, liquid, 74 K                         ; 0.808       ; pht
    Ocimene 25 °C                                   ; .7977       ; sim
    Octane                                         ; .701        ; aes 90
    Octane 15 °C                                    ; .9179       ; sim
    Oil, SAE10W, 15 deg °C                          ; 0.870       ; aes 624
    Oil, SAE10W-30, 15 deg °C                       ; 0.876       ; aes 624
    Oil, SAE30, 15 deg °C                           ; 0.891       ; aes 624
    Oil, gear, SAE90, 15 deg °C                     ; 0.930       ; aes 624
    Oil, linseed                                   ; .94         ; glo 390
    Oil, linseed                                   ; .942        ; sim
    Oil, mineral, lubricant                        ; .88-.94     ; mar 6-7
    Oil, petroleum                                 ; .88         ; glo 390
    Oil, petroleum                                 ; .881        ; sim
    Oil, transmission, 15 deg °C                    ; 0.887       ; aes 624
    Oil, vegetable                                 ; .91-.94     ; mar 6-7
    Oil, vegetable, coconut                        ; 0.924       ; pht
    Oil, vegetable, corn                           ; 0.922       ; pht
    Oil, vegetable, olive                          ; 0.918       ; pht
    Oil, vegetable, palm                           ; 0.915       ; pht
    Oil, vegetable, peanut                         ; 0.914       ; pht
    Oil, vegetable, soya                           ; 0.927       ; pht
    Olive oil 20 °C                                 ; .8-.92      ; sim
    Oxygen (liquid) -183 °C                         ; 1.14        ; sim
    Oxygen, liquid, 87 K                           ; 1.155       ; pht
    Palmitic acid 25 °C                             ; .8506       ; sim
    Pentane 20 °C                                   ; .6262       ; sim
    Pentane 25 °C                                   ; .6248       ; sim
    Perchlorethylene                               ; 1.6         ; pht
    Petroleum                                      ; .87         ; mar 6-7
    Petroleum ether 20 °C                           ; .64         ; sim
    Phenol 25 °C                                    ; 1.072       ; sim
    Phosgene 0 °C                                   ; 1.378       ; sim
    Phytadiene 25 °C                                ; .8234       ; sim
    Pinene 25 °C                                    ; .857        ; sim
    Pitch                                          ; 1.07        ; aes 178
    Pitch                                          ; 1.07-1.15   ; mar 6-7
    Pitch                                          ; 1.15        ; glo 390
    Pitch                                          ; 1.153       ; sim
    Propane (liquid)                               ; .495        ; aes 90
    Propane (liquid, bp = 231 K)                   ; .582        ; aes 97
    Propane -40 °C                                  ; .5831       ; sim
    Propane, R-290 25 °C                            ; .4935       ; sim
    Propanol 25 °C                                  ; .8041       ; sim
    Propylene (liquid)                             ; .514        ; aes 90
    Propylene (liquid, bp = 225 K)                 ; .614        ; aes 97
    Propylene 25 °C                                 ; .5144       ; sim
    Propylene carbonate 20 °C                       ; 1.201       ; sim
    Propylene glycol                               ; .968        ; aes 90
    Propylene glycol 25 °C                          ; .9653       ; sim
    Pyridine 25 °C                                  ; .9787       ; sim
    Pyrrole 25 °C                                   ; .9659       ; sim
    Rape seed oil 20 °C                             ; .92         ; sim
    Resorcinol 25 °C                                ; 1.269       ; sim
    Rosin oil 15 °C                                 ; .98         ; sim
    Sabiname 25 °C                                  ; .8121       ; sim
    Sea water                                      ; 1.03        ; aes 90
    Sea water 25 °C                                 ; 1.025       ; sim
    Sewage, sludge                                 ; .72         ; glo 390
    Silane 25 °C                                    ; .7176       ; sim
    Silicone                                       ; 0.993       ; pht
    Sodium hydroxide (caustic soda) 15 °C           ; 1.25        ; sim
    Sorbaldehyde 25 °C                              ; .8954       ; sim
    Soya bean oil 15 °C                             ; .924-.928   ; sim
    Soybean oil                                    ; .93         ; aes 353
    Stearic acid 25 °C                              ; .8906       ; sim
    Styrene 25 °C                                   ; .9034       ; sim
    Sugar solution 68 Brix 15 °C                    ; 1.338       ; sim
    Sulfuric acid 100% conc.                       ; 1.839       ; hcp F8
    Sulfuric acid 95% conc. 20 °C                   ; 1.839       ; sim
    Sulfuric acid, 15%                             ; 1.1039      ; aes 370
    Sulfuric acid, 30%                             ; 1.2206      ; aes 370
    Sulfuric acid, 35%                             ; 1.2620      ; aes 370
    Sulfuric acid, 4%                              ; 1.0269      ; aes 370
    Sulfuric acid, 8%                              ; 1.0540      ; aes 370
    Sulfuric acid, 87%                             ; 1.79        ; glo 390
    Sulfuric acid, 87%                             ; 1.8         ; mar 6-7
    Sunflower oil  20 °C                            ; .92         ; sim
    Tar                                            ; 1.02        ; aes 178
    Tar                                            ; 1.15        ; glo 390
    Terpinene 25 °C                                 ; .8474       ; sim
    Tetrahydrofuran 20 °C                           ; .888        ; sim
    Tobacco seed oil                               ; .92         ; aes 353
    Toluene (toluol)                               ; .865        ; aes 90
    Toluene (toluol)                               ; .87         ; aes 353
    Toluene (toluol) 20 °C                          ; .8669       ; sim
    Toluene (toluol) 25 °C                          ; .8623       ; sim
    Trichloroethylene                              ; 1.46        ; aes 353
    Triethylamine 20 °C                             ; .7276       ; sim
    Trifluoroacetic acid 20 °C                      ; 1.489       ; sim
    Tung oil                                       ; .94         ; aes 353
    Turpentine                                     ; .85         ; aes 353
    Turpentine                                     ; .865        ; sim
    Turpentine                                     ; .87         ; aes 90
    Turpentine                                     ; .87         ; glo 390
    Turpentine 25 °C                                ; .8682       ; sim
    Water (4 °C)                                    ; 1.00        ; aes 90
    Water (4 °C)                                    ; 1.00        ; glo 390
    Water, (0 °C & 1 atm)                           ; 0.9999      ; aes 89
    Water, (10 °C & 1 atm)                          ; .9997       ; aes 89
    Water, (100 °C & 1 atm)                         ; .9584       ; aes 89
    Water, (15 °C & 1 atm)                          ; .9992       ; aes 89
    Water, (20 °C & 1 atm)                          ; .9982       ; aes 89
    Water, (25 °C & 1 atm)                          ; .9970       ; aes 89
    Water, (30 °C & 1 atm)                          ; .9957       ; aes 89
    Water, (35 °C & 1 atm)                          ; .9941       ; aes 89
    Water, (40 °C & 1 atm)                          ; .9922       ; aes 89
    Water, (45 °C & 1 atm)                          ; .9903       ; aes 89
    Water, (5 °C & 1 atm)                           ; 1.0000      ; aes 89
    Water, (50 °C & 1 atm)                          ; .9881       ; aes 89
    Water, (55 °C & 1 atm)                          ; .9857       ; aes 89
    Water, (60 °C & 1 atm)                          ; .9832       ; aes 89
    Water, (65 °C & 1 atm)                          ; .9806       ; aes 89
    Water, (70 °C & 1 atm)                          ; .9778       ; aes 89
    Water, (75 °C & 1 atm)                          ; .9749       ; aes 89
    Water, (80 °C & 1 atm)                          ; .9718       ; aes 89
    Water, (85 °C & 1 atm)                          ; .9687       ; aes 89
    Water, (90 °C & 1 atm)                          ; .9653       ; aes 89
    Water, (95 °C & 1 atm)                          ; .9619       ; aes 89
    Water, heavy (deuterium oxide)                 ; 1.1086      ; hep 43
    Water, ice                                     ; .88-.92     ; mar 6-7
    Water, liquid, 0 °C                             ; 0.99984     ; pht
    Water, liquid, 10 °C                            ; 0.9997      ; pht
    Water, liquid, 100 °C                           ; 0.9584      ; pht
    Water, liquid, 20 °C                            ; 0.99821     ; pht
    Water, liquid, 30 °C                            ; 0.99565     ; pht
    Water, liquid, 4 °C                             ; 0.99998     ; pht
    Water, liquid, 50 °C                            ; 0.98803     ; pht
    Water, pure                                    ; 1.          ; sim
    Water, pure 4 °C                                ; 1.          ; sim
    Water, saline (0.9 % NaCl)                     ; 1.004       ; pht
    Water, saturated (0 °C & 0.00603 atm)           ; .9998       ; aes 18
    Water, saturated (100 °C & 1 atm)               ; .9581       ; aes 18
    Water, saturated (20 °C & 0.023 atm)            ; .9983       ; aes 18
    Water, saturated (50 °C & 0.123 atm)            ; .9880       ; aes 18
    Water, sea                                     ; 1.025       ; pht
    Water, sea                                     ; 1.026       ; sim
    Water, sea                                     ; 1.03        ; aes 90
    Water, sea                                     ; 1.03        ; glo 390
    Water, sea 77 F                                ; 1.022       ; sim
    Water, tap, 20 °C                               ; .9982       ; web
    Whale oil 15 °C                                 ; .925        ; sim
    Xylene                                         ; .89         ; aes 353
    Xylene (ortho) 20 °C                            ; .8802       ; sim
    n-Butyl acetate 20 °C                           ; .8796       ; sim
    n-Butyl alcohol 20 °C                           ; .8097       ; sim
    n-Butyl chloride 20 °C                          ; .8862       ; sim
    n-Propyl alcohol 20 °C                          ; .8037       ; sim
    o-Dichlorobenzene 20 °C                         ; 1.306       ; sim

    category = misc
    Aerographite                                   ; .00018      ; wkp
    Aerogel, silica                                ; .11         ; aes 177
    Alabaster, carbonate                           ; 2.69-2.78   ; aes 178
    Alabaster, sulfate                             ; 2.26-2.32   ; aes 178
    Alfalfa, ground                                ; .256        ; sim
    Alfalfa, ground                                ; .26         ; glo 390
    Alum, lumpy                                    ; .88         ; glo 390
    Alum, lumpy                                    ; .881        ; sim
    Alum, pulverized                               ; .753        ; sim
    Amatol 50-50 (explosive)                       ; 1.5         ; aes 399
    Amatol 80-20 (explosive)                       ; 1.4         ; aes 399
    Amber                                          ; 1.06-1.11   ; aes 178
    Ammonium nitrate                               ; .73         ; sim
    Ammonium sulfate                               ; .83         ; glo 390
    Ammonium sulphate, dry                         ; 1.13        ; sim
    Ammonium sulphate, wet                         ; 1.29        ; sim
    Aniline                                        ; 1.02        ; hep 43
    Apples                                         ; .64         ; glo 390
    Apples                                         ; .641        ; sim
    Arsenic                                        ; 5.67        ; glo 390
    Arsenic                                        ; 5.671       ; sim
    Asbestos                                       ; 2.0-2.8     ; aes 178
    Asbestos millboard                             ; 1.0         ; aes 177
    Asbestos rock                                  ; 1.6         ; sim
    Asbestos slate                                 ; 1.8         ; aes 178
    Asbestos, cement board                         ; 1.4         ; aes 177
    Asbestos, shredded                             ; .32-.4      ; sim
    Asbestos, shredded                             ; .35         ; glo 390
    Asbestos, solid                                ; 2.45        ; glo 390
    Ashes                                          ; .66         ; glo 390
    Ashes, dry                                     ; .57-.65     ; sim
    Ashes, wet                                     ; .73-.89     ; sim
    Asphalt                                        ; 1.1         ; aes 177
    Asphalt                                        ; 1.1-1.5     ; aes 178
    Asphalt, crushed                               ; .72         ; glo 390
    Asphalt, crushed                               ; .721        ; sim
    Bagasse (sugar cane fiber)                     ; .12         ; sim
    Baking powder                                  ; .72         ; glo 390
    Baking powder                                  ; .721        ; sim
    Balsam wool (chemically-treated wood fiber)    ; .035        ; hcp E5
    Barley                                         ; .609        ; sim
    Barley                                         ; .61         ; glo 390
    Barley, bulk                                   ; .62         ; mar 6-7
    Basalt                                         ; 2.4-3.1     ; aes 178
    Beans, castor                                  ; .577        ; sim
    Beans, castor                                  ; .58         ; glo 390
    Beans, cocoa                                   ; .59         ; glo 390
    Beans, cocoa                                   ; .593        ; sim
    Beans, navy                                    ; .8          ; glo 390
    Beans, navy                                    ; .801        ; sim
    Beans, soy                                     ; .72         ; glo 390
    Beans, soy                                     ; .721        ; sim
    Beeswax                                        ; .95         ; aes 177
    Beeswax                                        ; .96         ; glo 390
    Beeswax                                        ; .96-.97     ; aes 178
    Beeswax                                        ; .961        ; sim
    Beets                                          ; .72         ; glo 390
    Beets                                          ; .721        ; sim
    Bicarbonate of soda (NaHCO₃)                   ; .689        ; sim
    Bicarbonate of soda (NaHCO₃)                   ; .69         ; glo 390
    Black powder (KNO₃, charcoal, S)               ; 1.74        ; aes 399
    Blood                                          ; 1.06        ; web
    Body fat                                       ; 0.918       ; pht
    Bone                                           ; 1.7-2.0     ; aes 178
    Bone                                           ; 1.9         ; pht
    Bones, pulverized                              ; .88         ; glo 390
    Bones, pulverized                              ; .881        ; sim
    Boron fiber                                    ; 2.3         ; aes 182
    Bran                                           ; .256        ; sim
    Bran                                           ; .26         ; glo 390
    Brewers grain                                  ; .43         ; glo 390
    Brewers grain                                  ; .432        ; sim
    Brick                                          ; 1.4-2.2     ; aes 178
    Brick, chrome                                  ; 2.803       ; sim
    Brick, common                                  ; 1.75        ; aes 177
    Brick, common red                              ; 1.92        ; glo 390
    Brick, common red                              ; 1.922       ; sim
    Brick, fire clay                               ; 2.40        ; glo 390
    Brick, fire clay                               ; 2.403       ; sim
    Brick, hard                                    ; 1.8-2.3     ; mar 6-7
    Brick, hard                                    ; 2.0         ; aes 177
    Brick, magnesia                                ; 2.563       ; sim
    Brick, medium                                  ; 1.5-2       ; mar 6-7
    Brick, silica                                  ; 2.05        ; sim
    Brick, soft                                    ; 1.4-1.9     ; mar 6-7
    Broadcloth                                     ; .25         ; hep 45
    Buckwheat                                      ; .657        ; sim
    Buckwheat                                      ; .66         ; glo 390
    Bullseye smokeless powder                      ; .4          ; aes 399
    Butter                                         ; .86-.87     ; aes 178
    Butter                                         ; .865        ; sim
    Butter                                         ; .87         ; glo 390
    Butter                                         ; 0.911       ; pht
    Calamime                                       ; 4.1-4.5     ; aes 178
    Calcium carbide (CaC₂)                         ; 1.20        ; glo 390
    Calcium carbide (CaC₂)                         ; 1.201       ; sim
    Calcium carbide (CaC₂)                         ; 2.22        ; aes 183
    Camel hair                                     ; 1.32        ; aes 172
    Camphor                                        ; .99         ; aes 178
    Carbon                                         ; 2.25        ; pht
    Carbon dioxide, solid (sublimes at 195 K)      ; 1.56        ; aes 97
    Carbon, porous                                 ; 1.04        ; aes 180
    Carbon, powdered                               ; .08         ; glo 390
    Carbon, powdered                               ; .08         ; sim
    Carbon, refractory brick                       ; 1.63        ; aes 180
    Carbon, solid                                  ; 2.146       ; sim
    Carbon, solid                                  ; 2.15        ; glo 390
    Cardboard                                      ; .689        ; sim
    Cardboard                                      ; .69         ; aes 178
    Cardboard                                      ; .69         ; glo 390
    Celluloid                                      ; 1.4         ; aes 178
    Celotex (sugar cane fiber)                     ; .21-.24     ; hcp E5
    Cement - clinker                               ; 1.29-1.54   ; sim
    Cement, Portland                               ; 1.505       ; sim
    Cement, Portland                               ; 1.506       ; sim
    Cement, Portland                               ; 1.6         ; glo 390
    Cement, Portland                               ; 3.1-3.2     ; mar 6-7
    Cement, mortar                                 ; 2.16        ; glo 390
    Cement, mortar                                 ; 2.162       ; sim
    Cement, set                                    ; 2.7-3.0     ; aes 178
    Cement, slurry                                 ; 1.44        ; glo 390
    Cement, slurry                                 ; 1.442       ; sim
    Cement, stone and sand                         ; 2.2-2.4     ; mar 6-7
    Charcoal                                       ; .208        ; sim
    Charcoal                                       ; .21         ; glo 390
    Charcoal, oak                                  ; .57         ; aes 178
    Charcoal, pine                                 ; .28-.44     ; aes 178
    Charcoal, wood                                 ; .4          ; aes 177
    Chocolate, powder                              ; .64         ; glo 390
    Chocolate, powder                              ; .641        ; sim
    Chrome carbide (Cr₃C₂)                         ; 6.7         ; aes 183
    Chrome carbide (Cr7C₃)                         ; 6.92        ; aes 183
    Chromic acid, flake                            ; 1.201       ; sim
    Cinders, Coal, ash                             ; .641        ; sim
    Cinders, coal, ash                             ; .64         ; glo 390
    Cinders, furnace                               ; .91         ; glo 390
    Cinders, furnace                               ; .913        ; sim
    Clay                                           ; 1.8-2.6     ; aes 178
    Clay and gravel, dry                           ; 1.6         ; mar 6-7
    Clay, compacted                                ; 1.746       ; sim
    Clay, compacted                                ; 1.75        ; glo 390
    Clay, damp, plastic                            ; 1.76        ; mar 6-7
    Clay, dry                                      ; 1           ; mar 6-7
    Clay, dry excavated                            ; 1.089       ; sim
    Clay, dry excavated                            ; 1.09        ; glo 390
    Clay, dry lump                                 ; 1.07        ; glo 390
    Clay, dry lump                                 ; 1.073       ; sim
    Clay, fire                                     ; 1.36        ; glo 390
    Clay, fire                                     ; 1.362       ; sim
    Clay, wet excavated                            ; 1.826       ; sim
    Clay, wet excavated                            ; 1.83        ; glo 390
    Clay, wet lump                                 ; 1.60        ; glo 390
    Clay, wet lump                                 ; 1.602       ; sim
    Clover seed                                    ; .769        ; sim
    Clover seed                                    ; .77         ; glo 390
    Coal, anthracite                               ; 1.4-1.8     ; aes 178
    Coal, anthracite                               ; 1.5         ; aes 177
    Coal, anthracite, broken                       ; 1.11        ; glo 390
    Coal, anthracite, solid                        ; 1.51        ; glo 390
    Coal, bituminous                               ; 1.2         ; aes 177
    Coal, bituminous                               ; 1.2-1.5     ; aes 178
    Coal, bituminous, broken                       ; .83         ; glo 390
    Coal, bituminous, solid                        ; 1.35        ; glo 390
    Coca cola                                      ; 1.042       ; web
    Coca cola, diet                                ; 0.997       ; web
    Cocoa butter                                   ; .89-.91     ; aes 178
    Coconut, meal                                  ; .51         ; glo 390
    Coconut, meal                                  ; .513        ; sim
    Coconut, shredded                              ; .35         ; glo 390
    Coconut, shredded                              ; .352        ; sim
    Coffee beans, fresh                            ; .56         ; glo 390
    Coffee beans, roasted                          ; .43         ; glo 390
    Coffee, fresh beans                            ; .561        ; sim
    Coffee, roast beans                            ; .432        ; sim
    Coke                                           ; .42         ; glo 390
    Coke                                           ; .57-.65     ; sim
    Coke                                           ; 1.0-1.7     ; aes 178
    Comets                                         ; 0.3-0.6     ; wkp
    Concrete, dry                                  ; 1.6         ; hep 45
    Concrete, gravel                               ; 2.40        ; glo 390
    Concrete, gravel                               ; 2.403       ; sim
    Concrete, light                                ; 1.4         ; aes 177
    Concrete, limestone w/ Portland cement         ; 2.37        ; glo 390
    Concrete, reinforced, 8% moist. by wt          ; 2.2         ; hep 45
    Concrete, stone                                ; 2.2         ; aes 177
    Concrete, w/crushed rock, 8% moist. by wt      ; 2.0         ; hep 45
    Concrete, wet                                  ; 2.2-2.4     ; web
    Copper sulfate, ground                         ; 3.604       ; sim
    Copper sulphate, ground                        ; 3.6         ; glo 390
    Copra, expeller cake chopped (dried coconut)   ; .465        ; sim
    Copra, expeller cake ground (dried coconut)    ; .513        ; sim
    Copra, meal, ground (dried coconut)            ; .641        ; sim
    Copra, medium size (dried coconut)             ; .529        ; sim
    Cork                                           ; .22-.26     ; aes 178
    Cork                                           ; .22-.26     ; mar 6-7
    Cork linoleum                                  ; .54         ; aes 178
    Cork, ground                                   ; .16         ; glo 390
    Cork, ground                                   ; .16         ; sim
    Cork, solid                                    ; .24         ; glo 390
    Cork, solid                                    ; .24         ; sim
    Corkboard                                      ; .2          ; aes 177
    Corn or rye, bulk                              ; .73         ; mar 6-7
    Corn starch, loosely packed                    ; 0.54        ; pht
    Corn starch, tightly packed                    ; 0.630       ; pht
    Corn, grits                                    ; .67         ; glo 390
    Corn, grits                                    ; .673        ; sim
    Corn, on the cob                               ; .72         ; glo 390
    Corn, on the cob                               ; .721        ; sim
    Corn, shelled                                  ; .72         ; glo 390
    Corn, shelled                                  ; .721        ; sim
    Cotton                                         ; 1.54        ; aes 172
    Cotton, flax, hemp                             ; 1.47-1.5    ; mar 6-7
    Cottonseed, cake, lumpy                        ; .673        ; sim
    Cottonseed, dry, de-linted                     ; .561        ; sim
    Cottonseed, dry, delinted                      ; .56         ; glo 390
    Cottonseed, dry, not de-linted                 ; .32         ; sim
    Cottonseed, dry, not delinted                  ; .32         ; glo 390
    Cottonseed, hulls                              ; .19         ; glo 390
    Cottonseed, hulls                              ; .192        ; sim
    Cottonseed, meal                               ; .59         ; glo 390
    Cottonseed, meal                               ; .593        ; sim
    Cottonseed, meats                              ; .64         ; glo 390
    Cottonseed, meats                              ; .641        ; sim
    Cottonwood                                     ; .416        ; sim
    Earth (dirt), dense                            ; 2.0         ; glo 390
    Earth (dirt), dense                            ; 2.002       ; sim
    Earth (dirt), dry                              ; 1.4         ; aes 177
    Earth (dirt), dry, loose                       ; 1.2         ; mar 6-7
    Earth (dirt), dry, packed                      ; 1.5         ; mar 6-7
    Earth (dirt), loam, dry, excavated             ; 1.249       ; sim
    Earth (dirt), loam, dry, excavated             ; 1.25        ; glo 390
    Earth (dirt), moist, excavated                 ; 1.44        ; glo 390
    Earth (dirt), moist, excavated                 ; 1.442       ; sim
    Earth (dirt), moist, loose                     ; 1.3         ; mar 6-7
    Earth (dirt), moist, packed                    ; 1.6         ; mar 6-7
    Earth (dirt), mud, flowing                     ; 1.7         ; mar 6-7
    Earth (dirt), mud, packed                      ; 1.8         ; mar 6-7
    Earth (dirt), packed                           ; 1.52        ; glo 390
    Earth (dirt), packed                           ; 1.522       ; sim
    Earth (dirt), soft loose mud                   ; 1.73        ; sim
    Earth (dirt), soft, loose mud                  ; 1.73        ; glo 390
    Earth (dirt), wet, excavated                   ; 1.60        ; glo 390
    Earth (dirt), wet, excavated                   ; 1.602       ; sim
    Earth (planet), mean density                   ; 5.514       ; wkp
    Earth, Fuller's, raw                           ; .67         ; glo 390
    Earth, Fuller's, raw                           ; .673        ; sim
    Ebonite                                        ; 1.15        ; aes 178
    Fats                                           ; .9-.97      ; mar 6-7
    Felted cattle hair                             ; .18-.21     ; hcp E5
    Fertilizer, acid phosphate                     ; .96         ; glo 390
    Fertilizer, acid phosphate                     ; .961        ; sim
    Firebrick                                      ; 2.1         ; aes 177
    Fish, meal                                     ; .59         ; glo 390
    Fish, meal                                     ; .593        ; sim
    Fish, scrap                                    ; .72         ; glo 390
    Fish, scrap                                    ; .721        ; sim
    Flax                                           ; 1.5         ; aes 182
    Flax                                           ; 1.52        ; aes 172
    Flaxseed, whole                                ; .72         ; glo 390
    Flaxseed, whole                                ; .721        ; sim
    Flour, loose                                   ; .4-.5       ; mar 6-7
    Flour, pressed                                 ; .7-.8       ; mar 6-7
    Flour, wheat                                   ; .59         ; glo 390
    Flour, wheat                                   ; .593        ; sim
    Flue dust                                      ; 1.45-2.02   ; sim
    Foam, formaldehyde-urea (mipora)               ; .02         ; hep 45
    Fuller's Earth - raw or burnt                  ; .57-.73     ; sim
    Garbage                                        ; .48         ; glo 390
    Garbage, household rubbish                     ; .481        ; sim
    Gelatin                                        ; 1.27        ; aes 178
    Glass - broken or cullet                       ; 1.29-1.94   ; sim
    Glass fiber                                    ; 2.5         ; aes 182
    Glass wool (Pyrex, curled)                     ; .064-.16    ; hcp E5
    Glass, common                                  ; 2.4-2.8     ; aes 178
    Glass, common                                  ; 2.4-2.8     ; mar 6-7
    Glass, crystal                                 ; 2.9-3       ; mar 6-7
    Glass, flint                                   ; 2.9-5.9     ; aes 178
    Glass, flint                                   ; 3.2-4.7     ; mar 6-7
    Glass, plate or crown                          ; 2.45-2.72   ; mar 6-7
    Glass, silica                                  ; 2.55        ; aes 182
    Glass, window                                  ; 2.5         ; aes 177
    Glass, window                                  ; 2.579       ; sim
    Glass, window                                  ; 2.58        ; glo 390
    Glue                                           ; 1.27        ; aes 178
    Glue, animal, flaked                           ; .56         ; glo 390
    Glue, animal, flaked                           ; .561        ; sim
    Glue, vegetable, powdered                      ; .64         ; glo 390
    Glue, vegetable, powdered                      ; .641        ; sim
    Gluten, meal (protein from wheat)              ; .625        ; sim
    Gluten, meal (protein from wheat)              ; .63         ; glo 390
    Grain, barley                                  ; .6          ; sim
    Grain, barley                                  ; 0.62        ; pht
    Grain, corn, ear                               ; 0.9         ; pht
    Grain, corn, shelled                           ; 0.72        ; pht
    Grain, flax                                    ; 0.77        ; pht
    Grain, maize                                   ; .76         ; sim
    Grain, millet                                  ; .76-.8      ; sim
    Grain, millet                                  ; 0.64        ; pht
    Grain, oats                                    ; 0.41        ; pht
    Grain, rice, hulled                            ; 0.75        ; pht
    Grain, rice, rough                             ; 0.58        ; pht
    Grain, rye                                     ; 0.72        ; pht
    Grain, wheat                                   ; .78-.8      ; sim
    Grain, wheat                                   ; 0.77        ; pht
    Graphite (hexagonal sheet form of carbon)      ; 2.30-2.72   ; aes 178
    Graphite whisker                               ; 1.7         ; aes 182
    Graphite, brick                                ; 1.56        ; aes 180
    Graphite, fine grain premium                   ; 1.73        ; aes 180
    Graphite, flake                                ; .64         ; glo 390
    Graphite, flake                                ; .641        ; sim
    Graphite, plates                               ; 1.70        ; aes 180
    Graphite, porous                               ; 1.04        ; aes 180
    Gravel, dry 1/4 to 2 inch                      ; 1.682       ; sim
    Gravel, dry, 1/4 to 2 inch                     ; 1.68        ; glo 390
    Gravel, loose, dry                             ; 1.52        ; glo 390
    Gravel, loose, dry                             ; 1.522       ; sim
    Gravel, w/sand, natural                        ; 1.92        ; glo 390
    Gravel, wet 1/4 to 2 inch                      ; 2.002       ; sim
    Gravel, wet, 1/4 to 2 inch                     ; 2.00        ; glo 390
    Gravel, with sand, natural                     ; 1.922       ; sim
    Gum arabic                                     ; 1.3-1.4     ; aes 178
    Gypsum board (drywall)                         ; .8          ; aes 177
    Hair felt                                      ; .1          ; aes 177
    Hairinsul (50% hair, 50% jute)                 ; .098        ; hcp E5
    Hairinsul (75% hair, 25% jute)                 ; .1          ; hcp E5
    Hay and straw, bales                           ; .32         ; mar 6-7
    Hay, compressed                                ; .1          ; hep 45
    Hay, fresh mown                                ; .05         ; hep 45
    Hay, loose                                     ; .08         ; glo 390
    Hay, pressed                                   ; .38         ; glo 390
    Hemp                                           ; 1.48        ; aes 172
    Hemp                                           ; 1.5         ; aes 182
    Hops, moist                                    ; .56         ; glo 390
    Ice                                            ; .917        ; aes 178
    Ice, 0 °C                                      ; .9          ; aes 177
    Ice, crushed                                   ; .59         ; glo 390
    Ice, crushed                                   ; .593        ; sim
    Ice, solid                                     ; .919        ; sim
    Ice, solid                                     ; .92         ; glo 390
    Iron carbide (Fe₃C)                            ; 7.69        ; aes 183
    Iron oxide pigment                             ; .4          ; glo 390
    Iron oxide pigment                             ; .4          ; sim
    Iron sulphate - pickling tank - dry            ; 1.2         ; sim
    Iron sulphate - pickling tank - wet            ; 1.29        ; sim
    Iron whisker                                   ; 7.8         ; aes 182
    Ivory                                          ; 1.83-1.92   ; aes 178
    Ivory                                          ; 1.84        ; glo 390
    Ivory                                          ; 1.842       ; sim
    Jupiter (planet), mean density                 ; 1.326       ; wkp
    Jute (vegetable fiber)                         ; 1.5         ; aes 172
    Kapok between burlap or paper                  ; .016-.032   ; hcp E5
    Lanolin, refined                               ; .94         ; aes 159
    Lard                                           ; .919        ; pht
    Lead azide (explosive)                         ; 3.8         ; aes 399
    Lead, red (Pb₃O₄ or 2 PbO*PbO₂)                ; 3.684       ; sim
    Lead, red (Pb₃O₄ or 2 PbO*PbO₂)                ; 3.69        ; glo 390
    Lead, white pigment ((PbCO₃)2*Pb(OH)₂)         ; 4.085       ; sim
    Lead, white pigment ((PbCO₃)2*Pb(OH)₂)         ; 4.09        ; glo 390
    Leather                                        ; .86-1.02    ; mar 6-7
    Leather                                        ; .945        ; sim
    Leather                                        ; .95         ; glo 390
    Leather, dry                                   ; .86         ; aes 178
    Leather, dry                                   ; .9          ; aes 177
    Lignite, dry (fuel between coal and peat)      ; .801        ; sim
    Lime, hydrated (Ca(OH)₂)                       ; .48         ; glo 390
    Lime, hydrated (Ca(OH)₂)                       ; .481        ; sim
    Lime, quick, fine (CaO)                        ; 1.20        ; glo 390
    Lime, quick, fine (CaO)                        ; 1.201       ; sim
    Lime, quick, lump (CaO)                        ; .849        ; sim
    Lime, quick, lump (CaO)                        ; .85         ; glo 390
    Lime, slaked (Ca(OH)₂)                         ; 1.3-1.4     ; aes 178
    Lime, stone, large                             ; 2.69        ; glo 390
    Lime, stone, lump                              ; 1.54        ; glo 390
    Lime, wet or mortar                            ; 1.54        ; sim
    Linofelt (flax fibers between paper)           ; .074        ; hcp E5
    Linoleum                                       ; 1.18        ; aes 178
    Linseed, meal                                  ; .51         ; glo 390
    Linseed, meal                                  ; .513        ; sim
    Linseed, whole                                 ; .75         ; glo 390
    Linseed, whole                                 ; .753        ; sim
    Lithium 6 deuteride                            ; 0.82        ; pht
    Lungs                                          ; 0.40        ; pht
    Magnesium oxide                                ; 1.94        ; sim
    Magnesium sulfate, crystal                     ; 1.12        ; glo 390
    Magnesium sulphate, crystal                    ; 1.121       ; sim
    Magnesium titanate                             ; 3.6         ; aes 262
    Malt                                           ; .336        ; sim
    Malt                                           ; .34         ; glo 390
    Manganese oxide                                ; 1.92        ; glo 390
    Manganese oxide                                ; 1.922       ; sim
    Manure                                         ; .4          ; glo 390
    Manure                                         ; .4          ; sim
    Marl, wet, excavated                           ; 2.24        ; glo 390
    Mars (planet), mean density                    ; 3.933       ; wkp
    Mayonnaise, light                              ; 1.0         ; pht
    Mayonnaise, traditional                        ; 0.91        ; pht
    Meerschaum (hydrated magnesium silicate)       ; .99-1.28    ; aes 178
    Mercury (planet), mean density                 ; 5.427       ; wkp
    Milk, powdered                                 ; .449        ; sim
    Milk, powdered                                 ; .45         ; glo 390
    Mineral wool blanket                           ; .1          ; aes 177
    Mohair (hair of Angora goat)                   ; 1.32        ; aes 172
    Molybdenum carbide (Mo₂C)                      ; 9.0         ; aes 183
    Molybdenum carbide (MoC)                       ; 8.2         ; aes 183
    Monosodium glutamate                           ; 1.62        ; pht
    Mortar, Portland cement                        ; 2.08-2.25   ; mar 6-7
    Mortar, wet                                    ; 2.40        ; glo 390
    Mortar, wet                                    ; 2.403       ; sim
    Mud, fluid                                     ; 1.73        ; glo 390
    Mud, fluid                                     ; 1.73        ; sim
    Mud, packed                                    ; 1.906       ; sim
    Mud, packed                                    ; 1.91        ; glo 390
    Neptune (planet), mean density                 ; 1.638       ; wkp
    Oats                                           ; .43         ; glo 390
    Oats                                           ; .432        ; sim
    Oats, bulk                                     ; .41         ; mar 6-7
    Oats, rolled                                   ; .3          ; glo 390
    Oats, rolled                                   ; .304        ; sim
    Ochre (pigment)                                ; 3.5         ; aes 178
    Oil cake (remains from pressing seeds for oil) ; .785        ; sim
    Oyster shells                                  ; .8          ; sim
    Oyster shells, ground                          ; .849        ; sim
    Oyster shells, ground                          ; .85         ; glo 390
    PETN (explosive)                               ; 1.6         ; aes 399
    Paper                                          ; .7-1.15     ; aes 178
    Paper                                          ; .7-1.15     ; mar 6-7
    Paper                                          ; .9          ; aes 177
    Paper, standard                                ; 1.2         ; glo 390
    Paper, standard                                ; 1.201       ; sim
    Paraffin                                       ; .72         ; glo 390
    Paraffin                                       ; .87-.91     ; aes 178
    Paraffin wax                                   ; .87-.91     ; mar 6-7
    Paraffin wax                                   ; .9          ; aes 177
    Peanuts, not shelled                           ; .27         ; glo 390
    Peanuts, not shelled                           ; .272        ; sim
    Peanuts, shelled                               ; .64         ; glo 390
    Peanuts, shelled                               ; .641        ; sim
    Peas                                           ; .7          ; hep 45
    Peat blocks                                    ; .84         ; aes 178
    Peat, dry                                      ; .4          ; sim
    Peat, dry                                      ; .40         ; glo 390
    Peat, moist                                    ; .8          ; glo 390
    Peat, moist                                    ; .801        ; sim
    Peat, wet                                      ; 1.12        ; glo 390
    Peat, wet                                      ; 1.121       ; sim
    Phenol (carbolic acid C₆H₅OH)                  ; 1.071       ; aes 90
    Phosphorus                                     ; 2.339       ; sim
    Phosphorus                                     ; 2.34        ; glo 390
    Plaster                                        ; .849        ; sim
    Plaster                                        ; .85         ; glo 390
    Plaster, light                                 ; .7          ; aes 177
    Plaster, sand                                  ; 1.8         ; aes 177
    Pluto                                          ; 1.9         ; pht
    Porcelain                                      ; 2.3-2.5     ; aes 178
    Porcelain                                      ; 2.4         ; glo 390
    Porcelain                                      ; 2.403       ; sim
    Porcelain                                      ; 2.5         ; aes 177
    Potash (unspecified potassium salt)            ; 1.28        ; glo 390
    Potassium chloride                             ; 2.0         ; glo 390
    Potassium chloride                             ; 2.002       ; sim
    Potatoes                                       ; .67         ; hep 45
    Potatoes, piled                                ; .67         ; mar 6-7
    Potatoes, white                                ; .769        ; sim
    Potatoes, white                                ; .77         ; glo 390
    Regranulated cork, 4-5 mm particles            ; .13         ; hcp E5
    Regranulated cork, fine particles              ; .15         ; hcp E5
    Resin                                          ; 1.07        ; aes 178
    Resin, synthetic, crushed                      ; .56         ; glo 390
    Resin, synthetic, crushed                      ; .561        ; sim
    Rice grits                                     ; .689        ; sim
    Rice grits                                     ; .69         ; glo 390
    Rice, hulled                                   ; .75         ; glo 390
    Rice, hulled                                   ; .753        ; sim
    Rice, rough                                    ; .577        ; sim
    Rice, rough                                    ; .58         ; glo 390
    Rip-rap (broken rock used to line shorelines)  ; 1.6         ; sim
    Rip-rap, limestone (rock along shorelines)     ; 1.3-1.4     ; mar 6-7
    Rip-rap, sandstone (rock along shorelines)     ; 1.4         ; mar 6-7
    Rip-rap, shale (broken rock lines shorelines)  ; 1.7         ; mar 6-7
    Rock wool, loose                               ; .096        ; hcp E5
    Rock wool, sheet form, felted                  ; .16         ; hcp E5
    Rosin (pine resin)                             ; 1.07        ; glo 390
    Rosin (pine resin)                             ; 1.073       ; sim
    Rubber goods                                   ; 1-2         ; mar 6-7
    Rubber, Buna N                                 ; 1.0         ; aes 156
    Rubber, Buna S                                 ; 1.0         ; aes 156
    Rubber, Butyl                                  ; .95         ; aes 156
    Rubber, EPDM                                   ; .86         ; aes 156
    Rubber, Hypalon                                ; 1.2         ; aes 156
    Rubber, Neoprene                               ; 1.25        ; aes 156
    Rubber, Polymethane                            ; 1.2         ; aes 156
    Rubber, Silastic                               ; 1.0         ; aes 156
    Rubber, Thiokol                                ; 1.4         ; aes 156
    Rubber, Viton                                  ; 1.85        ; aes 156
    Rubber, butadiene                              ; 1.0         ; aes 156
    Rubber, caoutchouc (natural rubber)            ; .92-.96     ; mar 6-7
    Rubber, caoutchouc (natural rubber)            ; .945        ; sim
    Rubber, ground scrap                           ; .48         ; glo 390
    Rubber, ground scrap                           ; .481        ; sim
    Rubber, hard                                   ; 1.19        ; aes 178
    Rubber, manufactured                           ; 1.52        ; glo 390
    Rubber, manufactured                           ; 1.522       ; sim
    Rubber, natural                                ; .93         ; aes 156
    Rubber, soft, commercial                       ; 1.1         ; aes 178
    Rubber, soft, pure gum                         ; .91-.93     ; aes 178
    Rye                                            ; .705        ; sim
    Rye                                            ; .71         ; glo 390
    Salt (sodium chloride)                         ; 2.165       ; pht
    Salt, coarse (NaCl)                            ; .80         ; glo 390
    Salt, fine (NaCl)                              ; 1.2         ; glo 390
    Salt, granulated, piled (NaCl)                 ; .77         ; mar 6-7
    Saltpeter (KNO₃)                               ; 1.2         ; glo 390
    Saltpeter (KNO₃)                               ; 1.201       ; sim
    Saltpeter (KNO₃)                               ; 2.11        ; mar 6-7
    Sand, silica, 20 grains per inch, +/-0.05 g/cc ; 1.31        ; msa
    Sand and gravel, dry                           ; 1.73        ; glo 390
    Sand and gravel, wet                           ; 2.0         ; glo 390
    Sand with gravel, dry                          ; 1.65        ; sim
    Sand with gravel, wet                          ; 2.02        ; sim
    Sand, dry                                      ; 1.60        ; glo 390
    Sand, dry                                      ; 1.602       ; sim
    Sand, gravel, dry, loose                       ; 1.4-1.7     ; mar 6-7
    Sand, gravel, dry, packed                      ; 1.6-1.9     ; mar 6-7
    Sand, gravel, wet                              ; 1.89-2.16   ; mar 6-7
    Sand, loose                                    ; 1.44        ; glo 390
    Sand, loose                                    ; 1.442       ; sim
    Sand, rammed                                   ; 1.68        ; glo 390
    Sand, rammed                                   ; 1.682       ; sim
    Sand, water filled                             ; 1.92        ; glo 390
    Sand, water filled                             ; 1.922       ; sim
    Sand, wet                                      ; 1.92        ; glo 390
    Sand, wet                                      ; 1.922       ; sim
    Sand, wet, packed                              ; 2.08        ; glo 390
    Sand, wet, packed                              ; 2.082       ; sim
    Saturn (planet), mean density                  ; 0.687       ; wkp
    Sawdust                                        ; .15         ; aes 177
    Sawdust                                        ; .21         ; sim
    Sawdust                                        ; .27         ; glo 390
    Sawdust, redwood                               ; .175        ; hcp E5
    Sawdust, various woods                         ; .19         ; hcp E5
    Serpentine (hydrated metamorphic rock)         ; 2.50-2.65   ; aes 178
    Sewage, sludge                                 ; .721        ; sim
    Sil-o-cel powdered diatomaceous earth          ; .17         ; hcp E5
    Silicon                                        ; 2.33        ; pht
    Silicon carbide (SiC)                          ; 3.22        ; aes 183
    Silicon carbide whisker                        ; 3.2         ; aes 182
    Silk                                           ; 1.25        ; aes 172
    Sisal (fiber from agave plant)                 ; 1.49        ; aes 172
    Skin                                           ; 1.05        ; pht
    Slag (by-product of smelting ore)              ; 2.0-3.9     ; aes 178
    Slag, broken                                   ; 1.76        ; glo 390
    Slag, broken                                   ; 1.762       ; sim
    Slag, crushed 1/4 inch                         ; 1.19        ; glo 390
    Slag, crushed, 1/4 inch                        ; 1.185       ; sim
    Slag, furnace granulated                       ; .96         ; glo 390
    Slag, furnace granulated                       ; .961        ; sim
    Slag, solid                                    ; 2.114       ; sim
    Slag, solid                                    ; 2.12        ; glo 390
    Snow, compacted                                ; .48         ; glo 390
    Snow, compacted                                ; .481        ; sim
    Snow, freshly fallen                           ; .16         ; glo 390
    Snow, freshly fallen                           ; .16         ; sim
    Soap powder                                    ; .37         ; glo 390
    Soap, chips                                    ; .16         ; sim
    Soap, chips or flakes                          ; .16         ; glo 390
    Soap, flakes                                   ; .16         ; sim
    Soap, powdered                                 ; .368        ; sim
    Soap, solid                                    ; .8          ; glo 390
    Soap, solid                                    ; .801        ; sim
    Soda ash, heavy (Na₂CO₃, washing soda)         ; .96         ; glo 390
    Soda ash, heavy (Na₂CO₃, washing soda)         ; 1.08        ; sim
    Soda ash, light (Na₂CO₃, washing soda)         ; .43         ; glo 390
    Soda ash, light (Na₂CO₃, washing soda)         ; .432        ; sim
    Sodium aluminate, ground                       ; 1.153       ; sim
    Sodium bicarbonate                             ; 2.2         ; pht
    Sodium bicarbonate (baking soda) NaHCO₃        ; 2.2         ; wkp
    Sodium carbonate (washing soda) Na₂CO₃         ; 2.25-2.54   ; wkp
    Sodium carbonate (washing soda) Na₂CO₃*10H₂O   ; 1.44        ; hcp B165
    Sodium nitrate, ground (NaNO₃)                 ; 1.20        ; glo 390
    Sodium nitrate, ground (NaNO₃)                 ; 1.201       ; sim
    Sodium thiosulfate (hypo) Na₂S₂O₃              ; 1.667       ; web
    Soy beans, whole                               ; .753        ; sim
    Soybeans, whole                                ; .75         ; glo 390
    Spermaceti (wax from sperm whale's head)       ; .95         ; aes 178
    Starch                                         ; 1.53        ; aes 178
    Starch                                         ; 1.53        ; mar 6-7
    Starch, powdered                               ; .56         ; glo 390
    Starch, powdered                               ; .561        ; sim
    Sugar                                          ; 1.59        ; aes 178
    Sugar, brown                                   ; .72         ; glo 390
    Sugar, brown                                   ; .721        ; sim
    Sugar, granulated                              ; .849        ; sim
    Sugar, granulated                              ; .85         ; glo 390
    Sugar, powdered                                ; .80         ; glo 390
    Sugar, powdered                                ; .801        ; sim
    Sugar, raw cane                                ; .96         ; glo 390
    Sugar, raw cane                                ; .961        ; sim
    Sugar, sucrose                                 ; 1.55        ; pht
    Sugarbeet pulp, dry                            ; .208        ; sim
    Sugarbeet pulp, dry                            ; .21         ; glo 390
    Sugarbeet pulp, wet                            ; .21         ; glo 390
    Sugarbeet pulp, wet                            ; .561        ; sim
    Sugarcane                                      ; .27         ; glo 390
    Sugarcane                                      ; .272        ; sim
    Sulfur                                         ; 1.93-2.07   ; mar 6-7
    Sulfur, lump                                   ; 1.31        ; glo 390
    Sulfur, pulverized                             ; .96         ; glo 390
    Sulfur, solid                                  ; 2.0         ; glo 390
    Sun (mean solar density)                       ; 1.4         ; pht
    TNT (explosive)                                ; 1.55        ; aes 399
    Tallow (rendered beef or mutton fat)           ; .94         ; aes 178
    Tanbark, ground (bark used in tanning hides)   ; .88         ; glo 390
    Tanbark, ground (bark used in tanning hides)   ; .881        ; sim
    Tantalum carbide (TaC)                         ; 14.1        ; aes 183
    Tar                                            ; 1.153       ; sim
    Thermofelt (felted jute and asbestos fibers)   ; .125-.16    ; hcp E5
    Thermofill, powdered gypsum                    ; .42-.54     ; hcp E5
    Titania TiO₂ (rutile)                          ; 4.0         ; aes 262
    Titanium carbide (TiC)                         ; 4.9         ; aes 183
    Tobacco                                        ; .32         ; glo 390
    Tobacco                                        ; .32         ; sim
    Torpex (explosive)                             ; 1.7         ; aes 399
    Tungsten carbide (W₂C)                         ; 17.3        ; aes 183
    Tungsten carbide (WC)                          ; 15.2        ; aes 183
    Turf (lawn)                                    ; .4          ; sim
    Turf (lawn)                                    ; .40         ; glo 390
    Uranus (planet), mean density                  ; 1.27        ; wkp
    Vaseline                                       ; 0.9         ; web
    Vanadium carbide (VC)                          ; 5.8         ; aes 183
    Venus (planet), mean density                   ; 5.243       ; wkp
    Water, fresh-fallen snow                       ; .125        ; mar 6-7
    Water, ice, -100 °C                             ; 0.927       ; pht
    Water, ice, -50 °C                              ; 0.922       ; pht
    Water, ice, 0 °C                                ; 0.916       ; pht
    Wax, bayberry (myrtle)                         ; .93         ; aes 159
    Wax, carnauba (palm) from Brazil               ; 1.00        ; aes 159
    Wax, sealing                                   ; 1.8         ; aes 178
    Wax, yellow beeswax                            ; .96         ; aes 159
    Wheat                                          ; .769        ; sim
    Wheat                                          ; .77         ; glo 390
    Wheat, bulk                                    ; .77         ; mar 6-7
    Wheat, cracked                                 ; .67         ; glo 390
    Wheat, cracked                                 ; .673        ; sim
    Wood shavings, planer                          ; .14         ; hcp E5
    Wool (fiber from sheep)                        ; 1.31        ; glo 390
    Wool (fiber from sheep)                        ; 1.314       ; sim
    Wool (fiber from sheep)                        ; 1.32        ; mar 6-7
    Wool, cloth (fiber from sheep)                 ; .24         ; hep 45
    Wool, felt (fiber from sheep)                  ; .3          ; aes 177
    Wool, felt (fiber from sheep)                  ; .30         ; hep 45
    Wool, fiber (from sheep)                       ; 1.32        ; aes 172
    Wool, loose (fiber from sheep)                 ; .1          ; aes 177
    Zinc oxide                                     ; .4          ; sim
    Zinc oxide                                     ; .40         ; glo 390
    Zirconium carbide (ZrC)                        ; 6.7         ; aes 183

    category = plastic
    ABS (acrylonitrile butadiene styrene)          ; 1.06-1.08   ; aes 137
    Acetal (polyoxymethylene)                      ; 1.43        ; aes 137
    Acrylic (Plexiglas, methylmethacrylate)        ; 1.18-1.20   ; aes 137
    Alkyd resins                                   ; 1.24-2.6    ; aes 137
    Bakelite (phenol formaldehyde resin)           ; 1.36        ; glo 390
    Bakelite, solid (phenol formaldehyde resin)    ; 1.362       ; sim
    Cellulose acetate                              ; 1.27-1.34   ; aes 137
    Cellulose acetate butyrate                     ; 1.15-1.22   ; aes 137
    Epoxy                                          ; 1.115       ; aes 137
    Epoxy w/38% by vol carbon filaments            ; 1.42        ; aes 149
    Epoxy w/65% by wt glass cloth                  ; 2.0         ; aes 149
    Kapton polyimide                               ; 1.42        ; aes 152
    Kel-F polychlorotrifluoroethylene polymer      ; 2.10        ; aes 152
    Melamine formaldehyde, cellulose filled        ; 1.47-1.52   ; aes 137
    Melamine formaldehyde, mineral filled          ; 1.78        ; aes 137
    Mylar polyester                                ; 1.395       ; aes 152
    Nylon (polyamide)                              ; 1.13-1.15   ; aes 137
    Nylon (polyamide)                              ; 1.07        ; aes 182
    Nylon 6/6 w/40% by wt 1/4" glass fibers        ; 1.41        ; aes 149
    PVC, polyvinyl chloride, rigid                 ; 1.4         ; pvc
    PVC, polyvinyl chloride                        ; 1.25        ; aes 152
    PVC, polyvinyl chloride, plasticized           ; 1.15-1.35   ; aes 137
    PVC, polyvinyl chloride, unmodified            ; 1.36-1.4    ; aes 137
    Phenolic w/65% by wt glass cloth               ; 1.9         ; aes 149
    Plastics, foamed                               ; .2          ; aes 177
    Plastics, solid                                ; 1.2         ; aes 177
    Polycarbonate                                  ; 1.2         ; aes 137
    Polyester                                      ; 1.5-2.1     ; aes 137
    Polyester w/45% wt chopped glass strands       ; 1.6         ; aes 149
    Polyester w/65% by wt glass cloth              ; 1.8         ; aes 149
    PET, polyester terephthalate                   ; 1.38        ; wkp
    Polyethylene                                   ; .93         ; aes 152
    Polyethylene, high density                     ; .941-.965   ; aes 137
    Polyethylene, low density                      ; .91-.925    ; aes 137
    Polyethylene, medium density                   ; .926-.941   ; aes 137
    Polypropylene                                  ; .90         ; aes 137
    Polypropylene                                  ; .905        ; aes 152
    Polystyrene                                    ; 1.04-1.08   ; aes 137
    Polystyrene foam (Styrofoam)                   ; .04         ; wkp
    Polystyrene-acrylonitrile                      ; 1.05-1.1    ; aes 137
    Polytetrafluoroethylene (Teflon)               ; 2.1-2.3     ; aes 137
    Polytrifluorochloroethylene                    ; 2.1-2.3     ; aes 137
    Silicones                                      ; 1.8-2.8     ; aes 137
    Stryofoam                                      ; .04         ; wkp
    Teflon, FEP                                    ; 2.15        ; aes 152
    Teflon, FEP w/glass cloth                      ; 2.2         ; aes 152
    Teflon, TFE                                    ; 2.15        ; aes 152
    Teflon, TFE w/glass cloth                      ; 2.2         ; aes 152
    Urea formaldehyde                              ; 1.47-1.52   ; aes 137

    category = wood
    Afromosia (African teak)                       ; .705        ; sim
    Alder                                          ; .42-.68     ; aes 178
    Apple (wood)                                   ; .66-.84     ; aes 178
    Apple (wood)                                   ; .71         ; glo 390
    Apple (wood)                                   ; .66-.74     ; mar 6-7
    Apple (wood)                                   ; .66-.83     ; sim
    Ash (wood)                                     ; .65-.85     ; aes 178
    Ash (wood)                                     ; .85         ; aes 178
    Ash, black (wood)                              ; .54         ; glo 390
    Ash, black (wood)                              ; .54         ; sim
    Ash, black (wood)                              ; .55         ; mar 6-7
    Ash, white (wood)                              ; .67         ; glo 390
    Ash, white (wood)                              ; .64-.71     ; mar 6-7
    Ash, white (wood)                              ; .67         ; sim
    Aspen                                          ; .42         ; glo 390
    Aspen                                          ; .42         ; sim
    Balsa                                          ; .11-.14     ; aes 178
    Balsa                                          ; .17         ; sim
    Bamboo                                         ; .31-.40     ; aes 178
    Bamboo                                         ; .3-.4       ; sim
    Bark (wood)                                    ; .24         ; glo 390
    Bark, wood refuse                              ; .24         ; sim
    Basswood                                       ; .32-.59     ; aes 178
    Beech (wood)                                   ; .70-.90     ; aes 178
    Birch (wood)                                   ; .51-.77     ; aes 178
    Birch (British)                                ; .67         ; sim
    Birch plywood, 1/4" thick                      ; .345        ; msa
    Birch, sweet, yellow                           ; .71-.72     ; mar 6-7
    Birch, yellow                                  ; .71         ; glo 390
    Blue gum (wood)                                ; 1.0         ; aes 178
    Boxwood                                        ; .95-1.16    ; aes 178
    Butternut (wood)                               ; .38         ; aes 178
    Cedar (wood)                                   ; .49-.57     ; aes 178
    Cedar, red                                     ; .38         ; sim
    Cedar, red                                     ; .38         ; glo 390
    Cedar, white, red                              ; .35         ; mar 6-7
    Cherry (wood)                                  ; .56         ; glo 390
    Cherry (wood)                                  ; .7-.9       ; aes 178
    Cherry (wood)                                  ; .43         ; mar 6-7
    Chestnut (wood)                                ; .48         ; glo 390
    Chestnut (wood)                                ; .48         ; mar 6-7
    # Measured chopped blue spruce branches 8 Sep 2016:  107 g in about 600
    # ml cup.  I rounded up from 0.18 because there was a group of needles
    # that hadn't been chopped up in the cup.
    Chopped pine/spruce branches                   ; .2          ; msa
    Cottonwood                                     ; .42         ; glo 390
    Cypress (wood)                                 ; .51         ; glo 390
    Cypress (wood)                                 ; .45-.48     ; mar 6-7
    Cypress (wood)                                 ; .51         ; sim
    Dogwood                                        ; .76         ; aes 178
    Douglas Fir                                    ; .53         ; sim
    Ebony wood                                     ; .96         ; glo 390
    Ebony wood                                     ; .96-1.12    ; sim
    Ebony wood                                     ; 1.11-1.33   ; aes 178
    Elm                                            ; .54-.60     ; aes 178
    Elm                                            ; .56         ; glo 390
    Elm (English)                                  ; .6          ; sim
    Elm (Rock)                                     ; .815        ; sim
    Elm (Wych)                                     ; .69         ; sim
    Elm, white                                     ; .56         ; mar 6-7
    Fiberboard, light                              ; .24         ; aes 177
    Fiberboard, medium density (MDF)               ; .5-1        ; wkp
    Fir, Douglas                                   ; .53         ; glo 390
    Fir, Douglas                                   ; .48-.55     ; mar 6-7
    Fir, balsam                                    ; .4          ; mar 6-7
    Hardboard, fiber                               ; 1.1         ; aes 177
    Hardboard, high density (e.g. Masonite)        ; .8-1.04     ; wkp
    Hemlock (wood)                                 ; .4          ; glo 390
    Hemlock (wood)                                 ; .45-.5      ; mar 6-7
    Hickory (wood)                                 ; .60-.93     ; aes 178
    Hickory (wood)                                 ; .85         ; glo 390
    Hickory (wood)                                 ; .74-.8      ; mar 6-7
    Holly (wood)                                   ; .76         ; aes 178
    Iroko (African hardwood)                       ; .655        ; sim
    Juniper (wood)                                 ; .56         ; aes 178
    Larch (wood)                                   ; .50-.56     ; aes 178
    Larch (wood)                                   ; .59         ; sim
    Lignum Vitae (wood)                            ; 1.28-1.37   ; sim
    Lignum vitae (wood)                            ; 1.17-1.33   ; aes 178
    Lignum vitae (wood)                            ; 1.28        ; glo 390
    Locust (wood)                                  ; .67-.71     ; aes 178
    Locust (wood)                                  ; .71         ; glo 390
    Locust (wood)                                  ; .67-.77     ; mar 6-7
    Locust, dry (wood)                             ; .705        ; sim
    Mahogany (wood)                                ; .56-.85     ; mar 6-7
    Mahogany, African                              ; .495-.85    ; sim
    Mahogany, Honduras                             ; .545        ; sim
    Mahogany, Honduras                             ; .54         ; glo 390
    Mahogany, Honduras                             ; .66         ; aes 178
    Mahogany, Spanish                              ; .85         ; glo 390
    Mahogany, Spanish                              ; .85         ; aes 178
    Maple (wood)                                   ; .62-.75     ; aes 178
    Maple (wood)                                   ; .71         ; glo 390
    Maple (wood)                                   ; .755        ; sim
    Maple, sugar (wood)                            ; .68         ; mar 6-7
    Maple, white (wood)                            ; .53         ; mar 6-7
    Oak (wood)                                     ; .60-.90     ; aes 178
    Oak (wood)                                     ; .59-.93     ; sim
    Oak, chestnut                                  ; .74         ; mar 6-7
    Oak, live                                      ; .95         ; glo 390
    Oak, live                                      ; .87         ; mar 6-7
    Oak, red                                       ; .71         ; glo 390
    Oak, red                                       ; .705        ; sim
    Oak, red, black                                ; .64-.71     ; mar 6-7
    Oak, white                                     ; .77         ; mar 6-7
    Particle board, flat pressed                   ; .75         ; web
    Particle board, high density                   ; .75-1.3     ; web
    Particle board, low density                    ; .25-.45     ; web
    Particle board, medium density                 ; .55-.7      ; web
    Pear (wood)                                    ; .61-.73     ; aes 178
    Pecan (wood)                                   ; .75         ; glo 390
    Pecan (wood)                                   ; .753        ; sim
    Pine, Canadian                                 ; .35-.56     ; sim
    Pine, Oregon                                   ; .53         ; sim
    Pine, Parana                                   ; .56         ; sim
    Pine, Red                                      ; .37-.66     ; sim
    Pine, Norway                                   ; .55         ; mar 6-7
    Pine, Oregon                                   ; .51         ; mar 6-7
    Pine, Southern                                 ; .61-.67     ; mar 6-7
    Pine, pitch                                    ; .83-.85     ; aes 178
    Pine, red                                      ; .48         ; mar 6-7
    Pine, white                                    ; .35-.5      ; aes 178
    Pine, white                                    ; .42         ; glo 390
    Pine, white                                    ; .43         ; mar 6-7
    Pine, yellow                                   ; .37-.60     ; aes 178
    Pine, yellow, northern                         ; .54         ; glo 390
    Pine, yellow, southern                         ; .72         ; glo 390
    Plum (wood)                                    ; .66-.78     ; aes 178
    Plywood, general                               ; .45-.53     ; web
    Poplar (wood)                                  ; .35-.5      ; aes 178
    Poplar (wood)                                  ; .43         ; mar 6-7
    Pressed wood, pulp board                       ; .19         ; aes 178
    Redwood (American)                             ; .45         ; sim
    Redwood (European)                             ; .51         ; sim
    Redwood, California                            ; .45         ; glo 390
    Redwood, California                            ; .42         ; mar 6-7
    Satinwood                                      ; .95         ; aes 178
    Spruce (wood)                                  ; .48-.70     ; aes 178
    Spruce, Canadian                               ; .45         ; sim
    Spruce, Sitka                                  ; .45         ; sim
    Spruce, California                             ; .45         ; glo 390
    Spruce, white, red                             ; .45         ; mar 6-7
    Sycamore (wood)                                ; .40-.60     ; aes 178
    Sycamore (wood)                                ; .59         ; glo 390
    Sycamore (wood)                                ; .59         ; sim
    Teak (wood)                                    ; .63-.72     ; sim
    Teak, African                                  ; .98         ; aes 178
    Teak, African                                  ; .99         ; mar 6-7
    Teak, Indian                                   ; .66-.88     ; aes 178
    Teak, Indian                                   ; .66-.88     ; mar 6-7
    Walnut (wood)                                  ; .64-.70     ; aes 178
    Walnut, black (wood)                           ; .61         ; glo 390
    Walnut, black (wood)                           ; .59         ; mar 6-7
    Walnut, black, dry (wood)                      ; .609        ; sim
    Water gum (wood)                               ; 1.0         ; aes 178
    Willow (wood)                                  ; .4-.6       ; aes 178
    Willow (wood)                                  ; .42         ; glo 390
    Willow (wood)                                  ; .42         ; sim
    Willow (wood)                                  ; .42-.5      ; mar 6-7
    Wood chips, dry                                ; .24-.52     ; sim
    Wood refuse                                    ; .24         ; glo 390

    category = mineral
    Agate                                          ; 2.5-2.7     ; aes 178
    Alumina Al₂O₃                                  ; 3.68        ; aes 193
    Alumina, 99.7% Al₂O₃                           ; 3.9         ; aes 262
    Aluminum oxide                                 ; 1.52        ; glo 390
    Aluminum oxide                                 ; 1.522       ; sim
    Andesite, solid                                ; 2.771       ; sim
    Asbestos                                       ; 2.1-2.8     ; mar 6-7
    Barite, crushed (BaSO₄)                        ; 2.883       ; sim
    Barium titanate                                ; 5.5         ; aes 262
    Baryte (BaSO₄, barite)                         ; 4.5         ; mar 6-7
    Basalt (igneous rock)                          ; 2.7-3.2     ; mar 6-7
    Basalt, broken (igneous rock)                  ; 1.954       ; sim
    Basalt, broken (igneous rock)                  ; 1.96        ; glo 390
    Basalt, solid (igneous rock)                   ; 3.01        ; glo 390
    Basalt, solid (igneous rock)                   ; 3.011       ; sim
    Bauxite (aluminum ore)                         ; 2.55        ; mar 6-7
    Bauxite, crushed (aluminum ore)                ; 1.28        ; glo 390
    Bauxite, crushed (aluminum ore)                ; 1.281       ; sim
    Bentonite (type of clay)                       ; .59         ; glo 390
    Bentonite (type of clay)                       ; .593        ; sim
    Beryllia BeO (beryllium oxide)                 ; 3.08        ; aes 262
    Beryllium oxide BeO                            ; 3.04        ; aes 193
    Borax (hydrated Na₂B₄O₇)                       ; 1.7-1.8     ; mar 6-7
    Borax, fine (hydrated Na₂B₄O₇)                 ; .849        ; sim
    Borax, fine (hydrated Na₂B₄O₇)                 ; .85         ; glo 390
    Calcium oxide CaO                              ; 3.20        ; aes 193
    Calcspar (calcite CaCO₃)                       ; 2.6-2.8     ; aes 178
    Caliche (deposit of calcium carbonate)         ; 1.442       ; sim
    Chalk (sedimentary rock, CaCO₃)                ; 1.8-2.8     ; mar 6-7
    Chalk (sedimentary rock, CaCO₃)                ; 1.9-2.8     ; aes 178
    Chalk (sedimentary rock, CaCO₃)                ; 2.0         ; aes 177
    Chalk, fine (sedimentary rock, CaCO₃)          ; 1.12        ; glo 390
    Chalk, fine (sedimentary rock, CaCO₃)          ; 1.121       ; sim
    Chalk, lumpy (sedimentary rock, CaCO₃)         ; 1.44        ; glo 390
    Chalk, lumpy (sedimentary rock, CaCO₃)         ; 1.442       ; sim
    Chalk, solid (sedimentary rock, CaCO₃)         ; 2.499       ; sim
    Chalk, solid (sedimentary rock, CaCO₃)         ; 2.5         ; glo 390
    Chromium ore                                   ; 2.162       ; sim
    Cinnabar (mercury ore, HgS)                    ; 8.12        ; aes 178
    Coal, anthracite                               ; 1.4-1.8     ; mar 6-7
    Coal, anthracite, broken                       ; 1.105       ; sim
    Coal, anthracite, solid                        ; 1.506       ; sim
    Coal, bituminous                               ; 1.2-1.5     ; mar 6-7
    Coal, bituminous, broken                       ; .833        ; sim
    Coal, bituminous, solid                        ; 1.346       ; sim
    Cobaltite (CoAsS + Fe, Ni)                     ; 6.295       ; sim
    Copper ore                                     ; 1.94-2.59   ; sim
    Corundum (crystalline Al2O₃)                   ; 3.9-4.0     ; aes 178
    Corundum, 90% Al2O₃                            ; 3.20        ; aes 193
    Cryolite (Na₃AlF6)                             ; 1.6         ; glo 390
    Cryolite (Na₃AlF6)                             ; 1.602       ; sim
    Cullet (scraps of broken glass)                ; 1.602       ; sim
    Culm (waste from coal preparation)             ; .753        ; sim
    Diamond (allotrope of carbon)                  ; 3.01-3.52   ; aes 178
    Dolomite (CaMg(C)₃)₂)                          ; 2.84        ; aes 178
    Dolomite (CaMg(C)₃)₂)                          ; 2.9         ; mar 6-7
    Dolomite, lumpy (CaMg(C)₃)₂)                   ; 1.52        ; glo 390
    Dolomite, lumpy (CaMg(C)₃)₂)                   ; 1.522       ; sim
    Dolomite, pulverized (CaMg(C)₃)₂)              ; .737        ; sim
    Dolomite, pulverized (CaMg(C)₃)₂)              ; .74         ; glo 390
    Dolomite, solid (CaMg(C)₃)₂)                   ; 2.899       ; sim
    Dolomite, solid (CaMg(C)₃)₂)                   ; 2.9         ; glo 390
    Emery (usually mostly Al2O₃)                   ; 4.0         ; aes 178
    Emery (usually mostly Al2O₃)                   ; 4.005       ; sim
    Emery (usually mostly Al2O₃)                   ; 4.01        ; glo 390
    Feldspar (common crustal rock)                 ; 2.55-2.75   ; aes 178
    Feldspar, pulverized (common crustal rock)     ; 1.23        ; glo 390
    Feldspar, pulverized (common crustal rock)     ; 1.233       ; sim
    Feldspar, solid (common crustal rock)          ; 2.56        ; glo 390
    Feldspar, solid (common crustal rock)          ; 2.563       ; sim
    Ferrofluids                                    ; .9-1.7      ; aes 312
    Flint                                          ; 2.63        ; aes 178
    Flint, silica                                  ; 1.39        ; sim
    Fluorite (CaF₂)                                ; 3.18        ; aes 178
    Fluorspar, lumps (CaF₂)                        ; 1.6         ; glo 390
    Fluorspar, lumps (CaF₂)                        ; 1.602       ; sim
    Fluorspar, pulverized (CaF₂)                   ; 1.44        ; glo 390
    Fluorspar, pulverized (CaF₂)                   ; 1.442       ; sim
    Fluorspar, solid (CaF₂)                        ; 3.204       ; sim
    Fluorspar, solid (CaF₂)                        ; 3.21        ; glo 390
    Forsterite 2MgO*SiO₂                           ; 2.56        ; aes 193
    Galena (lead ore) PbS                          ; 7.3-7.6     ; aes 178
    Galena (lead ore) PbS                          ; 7.4-7.6     ; sim
    Garnet (variety of silicate minerals)          ; 3.15-4.3    ; aes 178
    Gneiss, bed in place (metamorphic rock)        ; 2.867       ; sim
    Gneiss, broken (metamorphic rock)              ; 1.858       ; sim
    Granite (igneous rock)                         ; 2.6-2.7     ; mar 6-7
    Granite (igneous rock)                         ; 2.64-2.76   ; aes 178
    Granite, broken (igneous rock)                 ; 1.65        ; glo 390
    Granite, broken (igneous rock)                 ; 1.65        ; sim
    Granite, solid (igneous rock)                  ; 2.69        ; glo 390
    Granite, solid (igneous rock)                  ; 2.691       ; sim
    Graphite (carbon allotrope)                    ; 1.64-2.7    ; mar 6-7
    Gummite (uranium ore)                          ; 3.89-6.4    ; sim
    Gypsum CaSO₄*2H₂0                              ; 2.30-2.37   ; hcp B222
    Gypsum CaSO₄*2H₂0                              ; 2.31-2.33   ; aes 178
    Gypsum, broken                                 ; 1.29-1.6    ; sim
    Gypsum, broken                                 ; 1.81        ; glo 390
    Gypsum, crushed                                ; 1.60        ; glo 390
    Gypsum, crushed                                ; 1.602       ; sim
    Gypsum, pulverized                             ; 1.12        ; glo 390
    Gypsum, pulverized                             ; 1.121       ; sim
    Gypsum, solid                                  ; 2.787       ; sim
    Gypsum, solid                                  ; 2.79        ; glo 390
    Halite (NaCl salt), broken                     ; 1.506       ; sim
    Halite (NaCl salt), solid                      ; 2.323       ; sim
    Hematite (iron ore)                            ; 4.9-5.3     ; aes 178
    Hematite (iron ore)                            ; 5.095-5.205 ; sim
    Hematite (iron ore)                            ; 5.2         ; mar 6-7
    Hematite (iron ore), broken                    ; 3.22        ; glo 390
    Hematite (iron ore), solid                     ; 4.90        ; glo 390
    Hemimorphite (zinc ore)                        ; 3.395-3.49  ; sim
    Hornblende (complex series of minerals)        ; 3.0         ; aes 178
    Ilmenite (FeTiO₃)                              ; 2.307       ; sim
    Iron ore, crushed                              ; 2.1-2.9     ; sim
    Iron pyrite (FeS₂)                             ; 2.4         ; sim
    Kaolin, green crushed (Al₂Si₂O₅(OH)₄)          ; 1.025       ; sim
    Kaolin, pulverized (Al₂Si₂O₅(OH)₄)             ; .352        ; sim
    Lime, stone, large                             ; 2.691       ; sim
    Lime, stone, lump                              ; 1.538       ; sim
    Limestone (sedimentary rock CaCO₃)             ; 2.1-2.86    ; mar 6-7
    Limestone (sedimentary rock CaCO₃)             ; 2.5         ; aes 177
    Limestone (sedimentary rock CaCO₃)             ; 2.68-2.76   ; aes 178
    Limestone, broken (sedimentary rock CaCO₃)     ; 1.55        ; glo 390
    Limestone, broken (sedimentary rock CaCO₃)     ; 1.554       ; sim
    Limestone, pulverized (sedimentary rock CaCO₃) ; 1.394       ; sim
    Limestone, pulverized (sedimentary rock CaCO₃) ; 1.55        ; glo 390
    Limestone, solid (sedimentary rock CaCO₃)      ; 2.61        ; glo 390
    Limestone, solid (sedimentary rock CaCO₃)      ; 2.611       ; sim
    Limonite (iron ore)                            ; 2.467       ; mar 6-7
    Limonite (iron ore), broken                    ; 2.467       ; sim
    Limonite (iron ore), solid                     ; 3.796       ; sim
    Magnesia (85%)                                 ; .25         ; aes 177
    Magnesia MgO                                   ; 3.36        ; aes 193
    Magnesite (MgCO₃)                              ; 3.0         ; mar 6-7
    Magnesite, solid (MgCO₃)                       ; 3.011       ; sim
    Magnesium oxide MgO                            ; 2.80        ; aes 193
    Magnetite (Fe₃O₄), broken                      ; 3.284       ; sim
    Magnetite (Fe₃O₄), solid                       ; 5.046       ; sim
    Magnetite Fe₃O₄                                ; 4.9-5.2     ; aes 178
    Malachite (copper ore)                         ; 3.7-4.1     ; aes 178
    Malachite (copper ore)                         ; 3.75-3.96   ; sim
    Marble (metamorphic rock)                      ; 2.6         ; aes 177
    Marble (metamorphic rock)                      ; 2.6-2.84    ; aes 178
    Marble (metamorphic rock)                      ; 2.6-2.86    ; mar 6-7
    Marble, broken (metamorphic rock)              ; 1.57        ; glo 390
    Marble, broken (metamorphic rock)              ; 1.57        ; sim
    Marble, solid (metamorphic rock)               ; 2.56        ; glo 390
    Marble, solid (metamorphic rock)               ; 2.563       ; sim
    Marl, wet, excavated                           ; 2.243       ; sim
    Mica                                           ; 2.6-3.2     ; aes 178
    Mica                                           ; 2.7         ; aes 177
    Mica, broken                                   ; 1.60        ; glo 390
    Mica, broken                                   ; 1.602       ; sim
    Mica, flake                                    ; .52         ; sim
    Mica, powder                                   ; .986        ; sim
    Mica, solid                                    ; 2.88        ; glo 390
    Mica, solid                                    ; 2.883       ; sim
    Molybdenum ore                                 ; 1.6         ; sim
    Mullite 3Al₂O₃*SiO₂                            ; 2.56        ; aes 193
    Muscovite (common mica, isinglass)             ; 2.76-3.00   ; aes 178
    Nickel ore                                     ; 1.6         ; sim
    Opal                                           ; 2.2         ; aes 178
    Perlite (Home Depot bag Sep 2016)              ; .09         ; msa
    Perlite (hydrated phyllosilicate)              ; .03-.15     ; wkp
    Phosphate rock, broken                         ; 1.762       ; sim
    Platinum ore                                   ; 2.6         ; sim
    Porphyry (low-grade copper ore)                ; 2.6-2.9     ; mar 6-7
    Porphyry, broken (low-grade copper ore)        ; 1.65        ; sim
    Porphyry, solid (low-grade copper ore)         ; 2.547       ; sim
    Potash (various potassium salts)               ; 1.281       ; sim
    Pumice stone (volcanic rock)                   ; .64         ; glo 390
    Pumice stone (volcanic rock)                   ; .641        ; sim
    Pumice, natural (volcanic rock)                ; .37-.9      ; mar 6-7
    Pyrite (fool's gold, FeS₂)                     ; 2.4-5.015   ; sim
    Pyrite (fool's gold, FeS₂)                     ; 4.95-5.1    ; aes 178
    Quartz (SiO₂)                                  ; 2.65        ; aes 178
    Quartz sand (SiO₂)                             ; 1.201       ; sim
    Quartz whisker (SiO₂)                          ; 2.65        ; aes 182
    Quartz, clear fused (SiO₂)                     ; 2.2         ; aes 187
    Quartz, flint                                  ; 2.5-2.8     ; mar 6-7
    Quartz, lump (SiO₂)                            ; 1.55        ; glo 390
    Quartz, lump (SiO₂)                            ; 1.554       ; sim
    Quartz, sand (SiO₂)                            ; 1.20        ; glo 390
    Quartz, solid (SiO₂)                           ; 2.64        ; glo 390
    Quartz, solid (SiO₂)                           ; 2.643       ; sim
    Road mix (sand, dirt, small rocks)             ; 1.57        ; msa
    Rock salt (NaCl, halide)                       ; 2.18        ; aes 178
    Rock, soft, dug with shovel                    ; 1.6-1.78    ; sim
    Salt cake (Na₂SO₄)                             ; 1.442       ; sim
    Salt, coarse (NaCl, halide)                    ; .801        ; sim
    Salt, fine (NaCl, halide)                      ; 1.201       ; sim
    Salt, table                                    ; 2.17        ; wkp
    Sandstone (sedimentary rock)                   ; 2-2.5       ; mar 6-7
    Sandstone (sedimentary rock)                   ; 2.14-2.36   ; aes 178
    Sandstone (sedimentary rock)                   ; 2.3         ; aes 177
    Sandstone, broken (sedimentary rock)           ; 1.37-1.45   ; sim
    Sandstone, broken (sedimentary rock)           ; 1.51        ; glo 390
    Sandstone, solid (sedimentary rock)            ; 2.32        ; glo 390
    Sandstone, solid (sedimentary rock)            ; 2.323       ; sim
    Sapphire or Al₂0₃ whisker                      ; 4.0         ; aes 182
    Shale, broken (sedimentary rock)               ; 1.586       ; sim
    Shale, broken (sedimentary rock)               ; 1.59        ; glo 390
    Shale, slate (sedimentary rock)                ; 2.6-2.9     ; mar 6-7
    Shale, solid (sedimentary rock)                ; 2.675       ; sim
    Shale, solid (sedimentary rock)                ; 2.68        ; glo 390
    Silica SiO₂                                    ; 1.76        ; aes 193
    Silica, fused translucent (SiO₂)               ; 2.07        ; aes 178
    Silica, fused transparent (SiO₂)               ; 2.21        ; aes 178
    Silicon carbide SiC                            ; 2.72        ; aes 193
    Silicon dioxide (quartz)                       ; 2.6         ; pht
    Slate (metamorphic rock)                       ; 2.6-3.3     ; aes 178
    Slate, broken (metamorphic rock)               ; 1.29-1.45   ; sim
    Slate, broken (metamorphic rock)               ; 1.67        ; glo 390
    Slate, pulverized (metamorphic rock)           ; 1.36        ; glo 390
    Slate, pulverized (metamorphic rock)           ; 1.362       ; sim
    Slate, solid (metamorphic rock)                ; 2.69        ; glo 390
    Slate, solid (metamorphic rock)                ; 2.691       ; sim
    Smithsonite (zinc ore)                         ; 4.3         ; sim
    Soapstone (steatite, metamorphic rock)         ; 2.6-2.8     ; aes 178
    Soapstone, talc (steatite, metamorphic rock)   ; 2.4         ; sim
    Soapstone, talc (steatite, metamorphic rock)   ; 2.6-2.8     ; mar 6-7
    Sodium silicate (Na₂SiO₃)                      ; 2.61        ; wkp
    Spinel MgAl₂O₄                                 ; 3.6-4.1     ; wkp
    Spinel MgO*Al₂O₃                               ; 3.52        ; aes 193
    Stone (common, generic)                        ; 2.515       ; sim
    Stone, crushed                                 ; 1.6         ; glo 390
    Stone, crushed                                 ; 1.602       ; sim
    Sulfur, lump                                   ; 1.314       ; sim
    Sulfur, pulverized                             ; .961        ; sim
    Sulfur, solid                                  ; 2.002       ; sim
    Taconite (iron-bearing sedimentary rock)       ; 2.803       ; sim
    Talc (magnesium silicate)                      ; 2.7-2.8     ; aes 178
    Talc, broken (magnesium silicate)              ; 1.746       ; sim
    Talc, broken (magnesium silicate)              ; 1.75        ; glo 390
    Talc, solid (magnesium silicate)               ; 2.69        ; glo 390
    Talc, solid (magnesium silicate)               ; 2.691       ; sim
    Tar, bituminous                                ; 1.2         ; mar 6-7
    Titanium oxide TiO₂                            ; 4.17        ; aes 193
    Topaz (silicate mineral)                       ; 3.5-3.6     ; aes 178
    Tourmaline (boron silicate mineral)            ; 3.0-3.2     ; aes 178
    Trap rock (e.g. basalt), broken                ; 1.746       ; sim
    Trap rock (e.g. basalt), solid                 ; 2.883       ; sim
    Vermiculite (hydrated phyllosilicate)          ; .13         ; aes 177
    Zircon ZrO₂*SiO₂                               ; 3.52        ; aes 193
    Zirconium oxide ZrO₂                           ; 5.77        ; aes 193

    category = gas
    Acetylene C₂H₂ (20 °C & 1 atm)                  ; 0.001084    ; aes 38
    Air (20 °C & 1 atm)                             ; 0.001204    ; aes 38
    Air, 100 K & 1 atm                             ; 0.003556    ; pht
    Air, 1000 K & 1 atm                            ; 0.000340    ; pht
    Air, 200 K & 1 atm                             ; 0.001746    ; pht
    Air, 293 K & 1 atm                             ; 0.001207    ; pht
    Air, 300 K & 1 atm                             ; 0.001161    ; pht
    Air, 500 K & 1 atm                             ; 0.000696    ; pht
    Ammonia, anhydrous NH₃ (20 °C & 1 atm)          ; 0.0007104   ; aes 38
    Argon (20 °C & 1 atm)                           ; 0.0007104   ; aes 38
    Argon, gas, ~300 K                             ; 0.001449    ; pht
    Argon, liquid, 87 K                            ; 0.00143     ; pht
    Butane (20 °C & 1 atm)                          ; 0.002492    ; aes 38
    Carbon dioxide (20 °C & 1 atm)                  ; 0.00183     ; aes 38
    Carbon dioxide, gas, +25 °C                     ; 1.799       ; pht
    Carbon dioxide, solid, -78 °C                   ; 1.562       ; pht
    Carbon monoxide (20 °C & 1 atm)                 ; 0.001164    ; aes 38
    Carbon, diamond                                ; 3.539       ; pht
    Chlorine (20 °C & 1 atm)                        ; 0.00295     ; aes 38
    Ethane (20 °C & 1 atm)                          ; 0.001252    ; aes 38
    Fluorine (20 °C & 1 atm)                        ; 0.001577    ; aes 38
    Fluorocarbon CCl₃F, Refrig. 11 (20 °C & 1 atm)  ; 0.005707    ; aes 38
    Freon 12, vapor                                ; 0.003683    ; pht
    Helium (20 °C & 1 atm)                          ; 0.0001662   ; aes 38
    Helium, gas, ~300 K                            ; 0.000164    ; pht
    Hydrogen (20 °C & 1 atm)                        ; 0.00008429  ; aes 38
    Hydrogen (H₂), gas, 300 K                      ; 0.000082    ; pht
    Hydrogen chloride (20 °C & 1 atm)               ; 0.001517    ; aes 38
    Hydrogen sulfide (20 °C & 1 atm)                ; 0.001421    ; aes 38
    Krypton (20 °C & 1 atm)                         ; 0.00348     ; aes 38
    Laughing gas N₂O (20 °C & 1 atm)                ; 0.00183     ; aes 38
    Methane (20 °C & 1 atm)                         ; 0.0006671   ; aes 38
    Methyl chloride (20 °C & 1 atm)                 ; 0.002095    ; aes 38
    Natural gas (16% methane) (20 °C & 1 atm)       ; 0.000722    ; aes 389
    Neon (20 °C & 1 atm)                            ; 0.0008393   ; aes 38
    Nitric oxide NO (20 °C & 1 atm)                 ; 0.001252    ; aes 38
    Nitrogen (20 °C & 1 atm)                        ; 0.001164    ; aes 38
    Nitrogen (N₂), gas, ~300 K                     ; 0.001145    ; pht
    Oxygen (20 °C & 1 atm)                          ; 0.001331    ; aes 38
    Oxygen, gas, ~300 K                            ; 0.001308    ; pht
    Ozone (20 °C & 1 atm)                           ; 0.001999    ; aes 38
    Propane (20 °C & 1 atm)                         ; 0.00183     ; aes 38
    Steam (H₂O) saturated (0 °C & 0.00603 atm)      ; 0.000004847 ; aes 18
    Steam (H₂O) saturated (100 °C & 1 atm)          ; 0.0005977   ; aes 18
    Steam (H₂O) saturated (150 °C & 4.70 atm)       ; 0.002548    ; aes 18
    Steam (H₂O) saturated (20 °C & 0.023 atm)       ; 0.00001729  ; aes 18
    Steam (H₂O) saturated (200 °C & 15.34 atm)      ; 0.007864    ; aes 18
    Steam (H₂O) saturated (250 °C & 39.25 atm)      ; 0.02000     ; aes 18
    Steam (H₂O) saturated (300 °C & 84.80 atm)      ; 0.04619     ; aes 18
    Steam (H₂O) saturated (350 °C & 163.19 atm)     ; 0.1136      ; aes 18
    Steam (H₂O) saturated (50 °C & 0.123 atm)       ; 0.00008302  ; aes 18
    Sulfur dioxide (20 °C & 1 atm)                  ; 0.002661    ; aes 38
    Tungsten hexafluoride                          ; 0.0124      ; wkp
    Xenon (20 °C & 1 atm)                           ; 0.005455    ; aes 38
    '''
if 1:   # Quick list
    g.quick_list = dedent('''
        Aluminum                                       ; 2.70        ; aes 117
        Brass, leaded free-machining                   ; 8.50        ; asm 52
        Bronze, phosphor                               ; 8.88        ; mar 6-7
        Copper                                         ; 8.91        ; aes 118
        Iron, cast                                     ; 7.2         ; aes 118
        Lead                                           ; 11.35       ; aes 117
        Magnesium                                      ; 1.74        ; aes 117
        Mercury                                        ; 13.546      ; aes 117
        Monel (Ni-Cu alloy)                            ; 8.47        ; aes 118
        Nichrome, 80 Ni, 20 Cr, 108 uohm-cm            ; 8.4         ; asm 52
        Silver                                         ; 10.50       ; aes 117
        Solder, 63 Pb, 37 Sn eutectic                  ; 8.42        ; asm 52
        Steel, 304 stainless                           ; 8.02        ; aes 118
        Steel, plain carbon, 1020                      ; 7.86        ; aes 118
        Tin                                            ; 7.31        ; aes 117
        Titanium                                       ; 4.54        ; aes 117
        Zinc                                           ; 7.14        ; aes 118
 
        Acetone                                        ; .787        ; aes 90
        Alcohol, isopropyl (2-propanol)                ; .79         ; aes 353
        Alcohol, methyl (methanol)                     ; .79         ; aes 353
        Crude oil                                      ; .76-.85     ; hep 43
        Diesel oil, #2                                 ; .920        ; aes 389
        Ether                                          ; .715        ; aes 90
        Ethylene glycol                                ; 1.100       ; aes 90
        Gasoline                                       ; .71-.77     ; wkp
        Kerosene                                       ; .825        ; aes 389
        Mineral spirits (Stoddard solvent)             ; .66         ; aes 353
        Oil, SAE30, 15 °C                              ; 0.891       ; aes 624
        Propane (liquid)                               ; .495        ; aes 90
        Water, liquid, 20 °C                           ; 0.99821     ; pht
 
        Ashes, dry                                     ; .57-.65     ; sim
        Brick                                          ; 1.4-2.2     ; aes 178
        Cardboard                                      ; .69         ; aes 178
        Charcoal                                       ; .21         ; glo 390
        Concrete, reinforced, 8% moist. by wt          ; 2.2         ; hep 45
        Cork                                           ; .22-.26     ; aes 178
        Earth (dirt), dry                              ; 1.4         ; aes 177
        Earth (dirt), moist, excavated                 ; 1.44        ; glo 390
        Earth (dirt), packed                           ; 1.52        ; glo 390
        Glass, window                                  ; 2.5         ; aes 177
        Gypsum board (drywall)                         ; .8          ; aes 177
        Ice, solid                                     ; .92         ; glo 390
        Leather                                        ; .95         ; glo 390
        Paper                                          ; .7-1.15     ; aes 178
        Paraffin wax                                   ; .9          ; aes 177
        Rubber, Buna N                                 ; 1.0         ; aes 156
        Salt, granulated, piled (NaCl)                 ; .77         ; mar 6-7
        Sand, dry                                      ; 1.60        ; glo 390
        Sand, wet                                      ; 1.92        ; glo 390
        Sawdust                                        ; .15         ; aes 177
        Soap, solid                                    ; .8          ; glo 390
        Sugar, granulated                              ; .85         ; glo 390
        Turf (lawn)                                    ; .40         ; glo 390
        Wool, felt (fiber from sheep)                  ; .3          ; aes 177
 
        Acrylic (Plexiglas, methylmethacrylate)        ; 1.18-1.20   ; aes 137
        Epoxy                                          ; 1.115       ; aes 137
        Nylon (polyamide)                              ; 1.13-1.15   ; aes 137
        PVC, polyvinyl chloride                        ; 1.25        ; aes 152
        Polycarbonate                                  ; 1.2         ; aes 137
        Polyethylene, medium density                   ; .926-.941   ; aes 137
        Polystyrene                                    ; 1.04-1.08   ; aes 137
        Teflon, TFE                                    ; 2.15        ; aes 152
 
        Fir, Douglas                                   ; .53         ; glo 390
        Hardboard, high density (e.g. Masonite)        ; .8-1.04     ; wkp
        Maple, sugar (wood)                            ; .68         ; mar 6-7
        Oak (wood)                                     ; .60-.90     ; aes 178
        Particle board, medium density                 ; .55-.7      ; web
        Pine, white                                    ; .35-.5      ; aes 178
        Plywood, general                               ; .45-.53     ; web
        Redwood, California                            ; .45         ; glo 390
 
        Basalt (igneous rock)                          ; 2.7-3.2     ; mar 6-7
        Bentonite (type of clay)                       ; .59         ; glo 390
        Chalk, solid (sedimentary rock, CaCO₃)         ; 2.5         ; glo 390
        Granite, solid (igneous rock)                  ; 2.69        ; glo 390
        Marble, solid (metamorphic rock)               ; 2.56        ; glo 390
        Pumice stone (volcanic rock)                   ; .64         ; glo 390
        Quartz (SiO₂)                                  ; 2.65        ; aes 178
        Sandstone (sedimentary rock)                   ; 2.14-2.36   ; aes 178
        Shale, solid (sedimentary rock)                ; 2.68        ; glo 390
        Slate, solid (metamorphic rock)                ; 2.69        ; glo 390
        Stone, crushed                                 ; 1.6         ; glo 390
 
        Air (20 °C & 1 atm)                            ; 0.001207    ; pht
        Argon (20 °C & 1 atm)                          ; 0.0007104   ; aes 38
        Carbon dioxide (20 °C & 1 atm)                 ; 0.00183     ; aes 38
        Hydrogen (20 °C & 1 atm)                       ; 0.00008429  ; aes 38
        Helium (20 °C & 1 atm)                         ; 0.0001662   ; aes 38
        Methane (20 °C & 1 atm)                        ; 0.0006671   ; aes 38
        Nitrogen (20 °C & 1 atm)                       ; 0.001164    ; aes 38
        Oxygen (20 °C & 1 atm)                         ; 0.001331    ; aes 38
        Propane (20 °C & 1 atm)                        ; 0.00183     ; aes 38
        Steam (H₂O) saturated (100 °C & 1 atm)         ; 0.0005977   ; aes 18
    ''')
if 1:   # PowderHandling data
    # From https://www.powderhandling.com.au/bulk-density-chart/
    # Downloaded Thu 28 Apr 2022 09:42:56 AM
    # Fixed a few spelling mistakes and converted to US English.
    # Units are kg/m3
    g.pwd_data = dedent('''
        Abrasive compound                              ; 2371        ; pwd
        Abrasive mix                                   ; 2451        ; pwd
        Acetate                                        ; 561         ; pwd
        Acetate flakes                                 ; 336         ; pwd
        Acrylic fibers                                 ; 144         ; pwd
        Acrylic resin                                  ; 513         ; pwd
        Activated aluminum                             ; 240         ; pwd
        Activated carbon                               ; 320         ; pwd
        Adipic acid                                    ; 641         ; pwd
        Alcanol                                        ; 625         ; pwd
        Alfalfa leaf meal                              ; 240         ; pwd
        Alfalfa meal                                   ; 272         ; pwd
        Alfalfa meal, fine ground                      ; 304         ; pwd
        Alfalfa pellets                                ; 673         ; pwd
        Alfalfa seed                                   ; 737         ; pwd
        Alumina                                        ; 641         ; pwd
        Alumina powder                                 ; 288         ; pwd
        Alumina, activated                             ; 769         ; pwd
        Alumina, calcined                              ; 1009        ; pwd
        Alumina, metal grade                           ; 1073        ; pwd
        Aluminum flake                                 ; 2403        ; pwd
        Aluminum fluoride                              ; 881         ; pwd
        Aluminum magnesium silicate                    ; 336         ; pwd
        Aluminum oxide                                 ; 1282        ; pwd
        Aluminum powder                                ; 705         ; pwd
        Aluminum silicate                              ; 529         ; pwd
        Aluminum sulfate                               ; 1041        ; pwd
        Ammonium bromide                               ; 1218        ; pwd
        Ammonium chloride                              ; 609         ; pwd
        Ammonium nitrate                               ; 785         ; pwd
        Ammonium nitrate pills                         ; 609         ; pwd
        Ammonium perchloride                           ; 993         ; pwd
        Ammonium phosphate                             ; 881         ; pwd
        Ammonium sulfate                               ; 1105        ; pwd
        Amorphous silica                               ; 176         ; pwd
        Anthracite, powdered                           ; 561         ; pwd
        Antimony oxide                                 ; 705         ; pwd
        Antioxidant (granules)                         ; 657         ; pwd
        Antioxidant (powder)                           ; 449         ; pwd
        Apple slices diced                             ; 240         ; pwd
        Aquafloc                                       ; 160         ; pwd
        Arsenic trioxide                               ; 657         ; pwd
        Asbestos                                       ; 352         ; pwd
        Asbestos fiber                                 ; 320         ; pwd
        Asbestos powder                                ; 449         ; pwd
        Ascorbic acid (coarse)                         ; 721         ; pwd
        Ascorbic acid (fine)                           ; 513         ; pwd
        Ash, ground                                    ; 1682        ; pwd
        Ashes, dry loose                               ; 609         ; pwd
        Ashes, wet loose                               ; 753         ; pwd
        Baking powder                                  ; 897         ; pwd
        Barbasco root                                  ; 529         ; pwd
        Barites                                        ; 1922        ; pwd
        Barium carbonate                               ; 881         ; pwd
        Barium oxide                                   ; 1009        ; pwd
        Barium stearate                                ; 208         ; pwd
        Barium sulfate                                 ; 961         ; pwd
        Barley (whole)                                 ; 641         ; pwd
        Barley meal                                    ; 449         ; pwd
        Barley, fine ground                            ; 737         ; pwd
        Barley, ground                                 ; 400         ; pwd
        Barley, malted                                 ; 481         ; pwd
        Barley, rolled                                 ; 368         ; pwd
        Barley, scoured                                ; 657         ; pwd
        Bauxite                                        ; 721         ; pwd
        Beans (soya)                                   ; 737         ; pwd
        Beans, white                                   ; 721         ; pwd
        Beet pulp                                      ; 288         ; pwd
        Bentonite                                      ; 801         ; pwd
        Bicarbonate of soda                            ; 993         ; pwd
        Bleach compound                                ; 961         ; pwd
        Blood flour                                    ; 481         ; pwd
        Blood meal                                     ; 617         ; pwd
        Bone meal loose                                ; 881         ; pwd
        Bone, ground dry                               ; 1202        ; pwd
        Borax                                          ; 961         ; pwd
        Boric acid                                     ; 865         ; pwd
        Bran                                           ; 561         ; pwd
        Brass powder                                   ; 1602        ; pwd
        Bread crumbs                                   ; 96          ; pwd
        Brewers grains (dry)                           ; 256         ; pwd
        Bronze powder                                  ; 1250        ; pwd
        Buckwheat (whole)                              ; 609         ; pwd
        Buckwheat bran                                 ; 256         ; pwd
        Buckwheat flour                                ; 657         ; pwd
        Buckwheat hulls                                ; 208         ; pwd
        Buckwheat middlings                            ; 352         ; pwd
        Buttermilk dried                               ; 497         ; pwd
        Cake mix                                       ; 705         ; pwd
        Calcium                                        ; 481         ; pwd
        Calcium borate                                 ; 977         ; pwd
        Calcium carbide, crushed                       ; 1282        ; pwd
        Calcium carbonate                              ; 705         ; pwd
        Calcium chloride                               ; 961         ; pwd
        Calcium fluoride                               ; 1634        ; pwd
        Calcium hydroxide                              ; 641         ; pwd
        Calcium phosphate                              ; 769         ; pwd
        Calcium silicate                               ; 160         ; pwd
        Calcium stearate                               ; 320         ; pwd
        Calcium sulfate                                ; 721         ; pwd
        Cane seed                                      ; 657         ; pwd
        Carbon (pelletized)                            ; 673         ; pwd
        Carbon activated                               ; 272         ; pwd
        Carbon black                                   ; 561         ; pwd
        Carbon black (beads)                           ; 304         ; pwd
        Carbon black (pelletized)                      ; 352         ; pwd
        Carbon black graphite                          ; 721         ; pwd
        Carbon crystallized                            ; 929         ; pwd
        Carbon dust                                    ; 609         ; pwd
        Carbon granules                                ; 945         ; pwd
        Casein                                         ; 577         ; pwd
        Caustic soda                                   ; 497         ; pwd
        Cellulose acetate                              ; 160         ; pwd
        Cement                                         ; 1362        ; pwd
        Cement (Portland)                              ; 1506        ; pwd
        Cement (Portland) clinker                      ; 1522        ; pwd
        Cement dust                                    ; 801         ; pwd
        Ceramic compound                               ; 1362        ; pwd
        Cereal mix                                     ; 689         ; pwd
        Charcoal (powder)                              ; 384         ; pwd
        Chemco burnishing compound                     ; 561         ; pwd
        Chicory                                        ; 545         ; pwd
        Chicory (powder)                               ; 481         ; pwd
        Chili spice                                    ; 721         ; pwd
        Chlorine compound                              ; 449         ; pwd
        Chlorine powder                                ; 577         ; pwd
        Chocolate drink mix                            ; 417         ; pwd
        Chromic acid powder                            ; 1602        ; pwd
        Cinders, blast furnace                         ; 913         ; pwd
        Cinders, coal, ashes & clinker                 ; 641         ; pwd
        Cinnamon powder                                ; 561         ; pwd
        Citric acid                                    ; 769         ; pwd
        Clay                                           ; 801         ; pwd
        Clay (bentonite)                               ; 801         ; pwd
        Clay (calcined)                                ; 481         ; pwd
        Clay (fine)                                    ; 993         ; pwd
        Clay (fines)                                   ; 1121        ; pwd
        Clay (granite)                                 ; 513         ; pwd
        Clay (kaolin)                                  ; 769         ; pwd
        Clinker dust                                   ; 1442        ; pwd
        Clover seed                                    ; 769         ; pwd
        Coagulant                                      ; 577         ; pwd
        Coal (granules)                                ; 833         ; pwd
        Coal (pulverized)                              ; 561         ; pwd
        Coal anthracite                                ; 929         ; pwd
        Coal bituminous                                ; 641         ; pwd
        Coal dust                                      ; 561         ; pwd
        Coal powder                                    ; 641         ; pwd
        Cobalt carbonate                               ; 961         ; pwd
        Cobalt fines                                   ; 4101        ; pwd
        Cocoa                                          ; 561         ; pwd
        Cocoa flavoring                                ; 881         ; pwd
        Cocoa shells                                   ; 481         ; pwd
        Coconut chips                                  ; 609         ; pwd
        Coffee (instant)                               ; 304         ; pwd
        Coffee, green (beans)                          ; 609         ; pwd
        Coffee, roasted (beans)                        ; 368         ; pwd
        Coke (granules)                                ; 833         ; pwd
        Coke dust                                      ; 240         ; pwd
        Coke fines                                     ; 625         ; pwd
        Coke, calcined (course)                        ; 897         ; pwd
        Coke, calcined (fines)                         ; 945         ; pwd
        Coke, calcined (intermediate)                  ; 945         ; pwd
        Coke, pulverized                               ; 721         ; pwd
        Copper (fines)                                 ; 1618        ; pwd
        Copper hydroxide                               ; 400         ; pwd
        Copper sulfate                                 ; 833         ; pwd
        Copra meal, loose                              ; 433         ; pwd
        Cork, solid                                    ; 240         ; pwd
        Corn bran                                      ; 208         ; pwd
        Corn flour                                     ; 817         ; pwd
        Corn germ meal                                 ; 561         ; pwd
        Corn gluten feed                               ; 465         ; pwd
        Corn gluten meal                               ; 593         ; pwd
        Corn grits                                     ; 673         ; pwd
        Corn mash                                      ; 721         ; pwd
        Corn meal                                      ; 641         ; pwd
        Corn oil meal                                  ; 545         ; pwd
        Corn starch                                    ; 673         ; pwd
        Corn, (whole shelled)                          ; 721         ; pwd
        Corn, chops (coarse)                           ; 673         ; pwd
        Corn, chops (fine)                             ; 609         ; pwd
        Corn, chops (medium)                           ; 641         ; pwd
        Corn, cracked (coarse)                         ; 641         ; pwd
        Corn, ground                                   ; 561         ; pwd
        Corn, hominy feed                              ; 433         ; pwd
        Corn, kibbled                                  ; 336         ; pwd
        Cottonseed cake                                ; 673         ; pwd
        Cottonseed delinted                            ; 481         ; pwd
        Cottonseed flour                               ; 897         ; pwd
        Cottonseed hulls                               ; 192         ; pwd
        Cottonseed meats                               ; 641         ; pwd
        Cryolite                                       ; 1378        ; pwd
        Detergent (flake)                              ; 513         ; pwd
        Detergent (powder)                             ; 609         ; pwd
        Dextrose                                       ; 577         ; pwd
        Diammonium phosphate                           ; 801         ; pwd
        Diatomaceous earth                             ; 256         ; pwd
        Diatomite                                      ; 224         ; pwd
        Dicalite                                       ; 192         ; pwd
        Dielectric compound                            ; 721         ; pwd
        Distillers grains                              ; 288         ; pwd
        Dolomite                                       ; 865         ; pwd
        Dolomite lime                                  ; 737         ; pwd
        Egg yoke powder                                ; 368         ; pwd
        Eggs (powdered)                                ; 352         ; pwd
        Electrolyte                                    ; 961         ; pwd
        Epoxy powder                                   ; 785         ; pwd
        Ferric chloride                                ; 689         ; pwd
        Ferric sulfate                                 ; 977         ; pwd
        Ferro silicate                                 ; 1250        ; pwd
        Ferro silicon                                  ; 1394        ; pwd
        Ferrous carbonate                              ; 1394        ; pwd
        Fiberglass                                     ; 352         ; pwd
        Filter cake (centrifuge)                       ; 641         ; pwd
        Fish meal                                      ; 609         ; pwd
        Flaxseed                                       ; 705         ; pwd
        Flint                                          ; 1554        ; pwd
        Floc                                           ; 208         ; pwd
        Floc (solka)                                   ; 144         ; pwd
        Flour                                          ; 769         ; pwd
        Flour (barley malt)                            ; 721         ; pwd
        Flour (barley)                                 ; 609         ; pwd
        Flour (corn)                                   ; 625         ; pwd
        Flour (rye)                                    ; 673         ; pwd
        Flour (soy)                                    ; 705         ; pwd
        Flour (soya)                                   ; 641         ; pwd
        Flour (wheat)                                  ; 673         ; pwd
        Fluorite                                       ; 1250        ; pwd
        Fluorspar                                      ; 1794        ; pwd
        Flux                                           ; 2323        ; pwd
        Fly ash                                        ; 1041        ; pwd
        Fullers earth                                  ; 561         ; pwd
        Fumaric acid                                   ; 641         ; pwd
        Garlic (flakes)                                ; 352         ; pwd
        Garlic (powder)                                ; 320         ; pwd
        Gelatine                                       ; 721         ; pwd
        Glass (ground)                                 ; 1650        ; pwd
        Glass (powder)                                 ; 1650        ; pwd
        Glass beads                                    ; 1602        ; pwd
        Glass microspheres                             ; 993         ; pwd
        Gold powder                                    ; 849         ; pwd
        Grain                                          ; 577         ; pwd
        Granite, crushed                               ; 1554        ; pwd
        Graphite                                       ; 769         ; pwd
        Graphite (flakes)                              ; 673         ; pwd
        Graphite (granules)                            ; 1089        ; pwd
        Graphite (powder)                              ; 561         ; pwd
        Graphite (pulverized)                          ; 352         ; pwd
        Gravel                                         ; 1762        ; pwd
        Grinding compound                              ; 1586        ; pwd
        Ground bone                                    ; 801         ; pwd
        Gum base                                       ; 673         ; pwd
        Gum granules                                   ; 577         ; pwd
        Gum resin                                      ; 513         ; pwd
        Gypsum                                         ; 865         ; pwd
        Gypsum (calcined)                              ; 881         ; pwd
        Gypsum (ground)                                ; 673         ; pwd
        Ice, crushed                                   ; 641         ; pwd
        Iron chromite                                  ; 1826        ; pwd
        Iron fillings                                  ; 2884        ; pwd
        Iron ore                                       ; 2595        ; pwd
        Iron oxide                                     ; 1282        ; pwd
        Iron oxide (black)                             ; 2579        ; pwd
        Iron oxide (red)                               ; 1105        ; pwd
        Iron powder                                    ; 2804        ; pwd
        Iron sulfate                                   ; 1282        ; pwd
        Kaolin                                         ; 785         ; pwd
        Kaolin clay                                    ; 801         ; pwd
        Latex powder                                   ; 1426        ; pwd
        Lead arsenate                                  ; 1442        ; pwd
        Lead carbonate                                 ; 1298        ; pwd
        Lead chloride crystals                         ; 1153        ; pwd
        Lead oxide                                     ; 1009        ; pwd
        Lead stabilizer                                ; 689         ; pwd
        Ligno sulfinate                                ; 481         ; pwd
        Lignone                                        ; 577         ; pwd
        Lignosol                                       ; 384         ; pwd
        Lime                                           ; 561         ; pwd
        Lime (dolomitic)                               ; 673         ; pwd
        Lime (granular)                                ; 1282        ; pwd
        Lime (hydrated)                                ; 641         ; pwd
        Lime (pebble)                                  ; 721         ; pwd
        Lime (pulverized quick)                        ; 961         ; pwd
        Lime (quick)                                   ; 881         ; pwd
        Limestone                                      ; 961         ; pwd
        Limestone (ground)                             ; 945         ; pwd
        Limestone (pulverized)                         ; 1089        ; pwd
        Limestone dust                                 ; 1105        ; pwd
        Limestone filler                               ; 1009        ; pwd
        Limestone flour                                ; 1105        ; pwd
        Linseed meal                                   ; 400         ; pwd
        Liquorice powder                               ; 449         ; pwd
        Magnesia                                       ; 1250        ; pwd
        Magnesite                                      ; 433         ; pwd
        Magnesite light                                ; 641         ; pwd
        Magnesium carbonate                            ; 192         ; pwd
        Magnesium chips                                ; 961         ; pwd
        Magnesium chloride                             ; 192         ; pwd
        Magnesium hydroxide                            ; 625         ; pwd
        Magnesium oxide                                ; 1041        ; pwd
        Magnesium silicate                             ; 929         ; pwd
        Magnesium stearate                             ; 336         ; pwd
        Magnesium sulfate                              ; 833         ; pwd
        Magnetite                                      ; 2643        ; pwd
        Malted barley flour                            ; 641         ; pwd
        Malted wheat flour                             ; 657         ; pwd
        Manganese dioxide                              ; 1121        ; pwd
        Manganese ore                                  ; 1762        ; pwd
        Mannitol                                       ; 609         ; pwd
        Marble (granular)                              ; 1282        ; pwd
        Marble (ground)                                ; 1490        ; pwd
        Meat meal                                      ; 593         ; pwd
        Melamine                                       ; 721         ; pwd
        Melamine powder                                ; 513         ; pwd
        Metallic flakes                                ; 561         ; pwd
        Metallic powder                                ; 2643        ; pwd
        Metasol                                        ; 609         ; pwd
        Mica (flakes)                                  ; 160         ; pwd
        Mica (powder)                                  ; 657         ; pwd
        Milk (powdered whole)                          ; 561         ; pwd
        Milk (powdered)                                ; 208         ; pwd
        Milk (whole)                                   ; 513         ; pwd
        Millet                                         ; 641         ; pwd
        Milo, ground                                   ; 545         ; pwd
        Molasses feed                                  ; 352         ; pwd
        Molding sand                                   ; 1202        ; pwd
        Molybdenum disulfide                           ; 705         ; pwd
        Molybdenum oxide                               ; 1570        ; pwd
        Molybdi oxide                                  ; 256         ; pwd
        Monosodium phosphate                           ; 881         ; pwd
        Naphthalene flakes                             ; 577         ; pwd
        Natrosol                                       ; 449         ; pwd
        Nickel                                         ; 961         ; pwd
        Nickel oxide                                   ; 449         ; pwd
        Nickel powder                                  ; 1202        ; pwd
        Nuts (almond)                                  ; 465         ; pwd
        Nuts (cashews)                                 ; 497         ; pwd
        Nuts (peanuts)                                 ; 529         ; pwd
        Nylon fibers                                   ; 160         ; pwd
        Nylon flakes                                   ; 513         ; pwd
        Nylon pellets (1/8")                           ; 561         ; pwd
        Nylon powder                                   ; 625         ; pwd
        Oat flour                                      ; 529         ; pwd
        Oat middlings                                  ; 609         ; pwd
        Oats                                           ; 433         ; pwd
        Oats (ground)                                  ; 465         ; pwd
        Oats (rolled)                                  ; 352         ; pwd
        Oats groats (whole)                            ; 745         ; pwd
        Oats, hulls                                    ; 128         ; pwd
        Onions (chopped)                               ; 224         ; pwd
        Onions (minced)                                ; 128         ; pwd
        Onions (powdered)                              ; 400         ; pwd
        Oxalic acid                                    ; 833         ; pwd
        Oxychloride                                    ; 577         ; pwd
        Oyster shell (ground, about 1/2")              ; 849         ; pwd
        Peanut brittle                                 ; 577         ; pwd
        Peanut meal                                    ; 449         ; pwd
        Peanuts (shelled)                              ; 689         ; pwd
        Peanuts (unshelled)                            ; 336         ; pwd
        Peat moss                                      ; 160         ; pwd
        Peppermint powder                              ; 545         ; pwd
        Peppers (chopped)                              ; 336         ; pwd
        Peppers (whole)                                ; 256         ; pwd
        Perlite                                        ; 240         ; pwd
        Perlite filter aid                             ; 128         ; pwd
        Perlite ore                                    ; 1041        ; pwd
        Petroleum coke                                 ; 881         ; pwd
        Petroleum coke dust                            ; 400         ; pwd
        Phenofil                                       ; 481         ; pwd
        Phenol formaldehyde                            ; 481         ; pwd
        Phenolic powder                                ; 513         ; pwd
        Phosphate                                      ; 1282        ; pwd
        Phosphate rock crushed                         ; 1105        ; pwd
        Phosphate rock dust                            ; 1442        ; pwd
        Phosphate rock ground                          ; 1121        ; pwd
        Plaster of paris                               ; 785         ; pwd
        Plastic (beads)                                ; 737         ; pwd
        Plastic (cubes)                                ; 609         ; pwd
        Plastic (flakes)                               ; 769         ; pwd
        Plastic (pellets)                              ; 721         ; pwd
        Plastic powder                                 ; 673         ; pwd
        Plastic resin                                  ; 641         ; pwd
        Polyamide resin                                ; 497         ; pwd
        Polycarbonate resin                            ; 705         ; pwd
        Polyester adhesive powder                      ; 481         ; pwd
        Polyester flakes                               ; 433         ; pwd
        Polyester resin                                ; 545         ; pwd
        Polyethylene                                   ; 689         ; pwd
        Polyethylene beads                             ; 673         ; pwd
        Polyethylene film                              ; 128         ; pwd
        Polyethylene flakes                            ; 96          ; pwd
        Polyethylene granular                          ; 481         ; pwd
        Polyethylene pellets                           ; 561         ; pwd
        Polyethylene powder                            ; 561         ; pwd
        Polyhedral alcohol                             ; 593         ; pwd
        Polymer                                        ; 320         ; pwd
        Polymer reagent                                ; 625         ; pwd
        Polymer resin                                  ; 609         ; pwd
        Polypropylene                                  ; 481         ; pwd
        Polypropylene pellets                          ; 513         ; pwd
        Polypropylene powder                           ; 529         ; pwd
        Polypropylene flakes                           ; 352         ; pwd
        Polystyrene beads                              ; 641         ; pwd
        Polystyrene pellets                            ; 609         ; pwd
        Polystyrene powder                             ; 529         ; pwd
        Polyurethane pellets                           ; 721         ; pwd
        Polyvinyl acetate                              ; 625         ; pwd
        Polyvinyl alcohol                              ; 625         ; pwd
        Polyvinyl chloride                             ; 657         ; pwd
        Polyvinyl chloride pellets                     ; 625         ; pwd
        Potassium bromide (5% moist)                   ; 1826        ; pwd
        Potassium carbonate (potash)                   ; 1185        ; pwd
        Potassium chloride                             ; 961         ; pwd
        Potassium iodate                               ; 2067        ; pwd
        Potassium muriate                              ; 1057        ; pwd
        Potassium sulfate                              ; 1442        ; pwd
        Potatoes (flakes)                              ; 208         ; pwd
        Potatoes (powdered)                            ; 769         ; pwd
        Potting soil                                   ; 256         ; pwd
        Poultry meal                                   ; 577         ; pwd
        Powdered sugar                                 ; 561         ; pwd
        Pumice powder                                  ; 625         ; pwd
        PVC chips                                      ; 865         ; pwd
        PVC resin                                      ; 513         ; pwd
        Raisins (moist)                                ; 609         ; pwd
        Rapeseed                                       ; 774         ; pwd
        Red lead                                       ; 2643        ; pwd
        Red oxide pigment                              ; 1153        ; pwd
        Rice                                           ; 721         ; pwd
        Rice (puffed)                                  ; 96          ; pwd
        Rice bran                                      ; 417         ; pwd
        Rock salt                                      ; 1089        ; pwd
        Rubber (granules)                              ; 449         ; pwd
        Rubber composition powder                      ; 545         ; pwd
        Rubber compound                                ; 609         ; pwd
        Rubber crumb                                   ; 352         ; pwd
        Rubber foam (chopped)                          ; 48          ; pwd
        Rubber powder                                  ; 529         ; pwd
        Rye bran                                       ; 288         ; pwd
        Rye feed                                       ; 529         ; pwd
        Rye, malted                                    ; 513         ; pwd
        Rye, middlings                                 ; 673         ; pwd
        Rye, shorts                                    ; 529         ; pwd
        Rye, whole                                     ; 705         ; pwd
        Salt, fine table                               ; 1378        ; pwd
        Salt, granulated                               ; 1282        ; pwd
        Sand                                           ; 1586        ; pwd
        Sand (dry)                                     ; 1762        ; pwd
        Sand (fine)                                    ; 2002        ; pwd
        Sand (foundry)                                 ; 1602        ; pwd
        Sand (moist)                                   ; 2083        ; pwd
        Sand (molding)                                 ; 1250        ; pwd
        Sand foundry, coarse                           ; 1538        ; pwd
        Sand foundry, fine                             ; 1666        ; pwd
        Sawdust (coarse)                               ; 400         ; pwd
        Sawdust (fine)                                 ; 288         ; pwd
        Sawdust (moist)                                ; 449         ; pwd
        Seed (grass)                                   ; 641         ; pwd
        Shellac resin                                  ; 1298        ; pwd
        Silica flour                                   ; 1282        ; pwd
        Silica gel                                     ; 673         ; pwd
        Silica sand                                    ; 1298        ; pwd
        Silicon carbide                                ; 721         ; pwd
        Silicon dioxide                                ; 48          ; pwd
        Silver (powder)                                ; 1105        ; pwd
        Slate (crushed)                                ; 1602        ; pwd
        Soap flakes                                    ; 465         ; pwd
        Soap powder                                    ; 577         ; pwd
        Soapstone                                      ; 753         ; pwd
        Soda ash                                       ; 865         ; pwd
        Soda ash-iron chromite                         ; 1234        ; pwd
        Sodium aluminate                               ; 977         ; pwd
        Sodium benzoate                                ; 753         ; pwd
        Sodium bicarbonate                             ; 801         ; pwd
        Sodium bisulfate                               ; 1442        ; pwd
        Sodium borate                                  ; 1234        ; pwd
        Sodium caseinate                               ; 336         ; pwd
        Sodium chloride                                ; 1282        ; pwd
        Sodium chloride                                ; 1330        ; pwd
        Sodium hydrosulfate                            ; 1121        ; pwd
        Sodium hydrosulfite                            ; 1169        ; pwd
        Sodium hydroxide                               ; 961         ; pwd
        Sodium metasilicate                            ; 1121        ; pwd
        Sodium naptholine sulfate                      ; 433         ; pwd
        Sodium nitrate                                 ; 1346        ; pwd
        Sodium perborate                               ; 849         ; pwd
        Sodium pyrophosphate                           ; 1009        ; pwd
        Sodium silicate                                ; 513         ; pwd
        Sodium sulfate                                 ; 1362        ; pwd
        Sodium sulfite                                 ; 1634        ; pwd
        Sodium thiosulfate                             ; 881         ; pwd
        Sodium tripolyphosphate                        ; 961         ; pwd
        Soybean flakes                                 ; 577         ; pwd
        Soybean hulls                                  ; 400         ; pwd
        Soybean meal                                   ; 641         ; pwd
        Starch (corn)                                  ; 689         ; pwd
        Stearic acid (flakes)                          ; 513         ; pwd
        Stearic acid (powder)                          ; 577         ; pwd
        Styrene beads                                  ; 721         ; pwd
        Sucrose                                        ; 849         ; pwd
        Sucrose octoacetate                            ; 529         ; pwd
        Sugar (beet)                                   ; 801         ; pwd
        Sugar (dextrose)                               ; 625         ; pwd
        Sugar (granulated)                             ; 705         ; pwd
        Sugar (powdered)                               ; 561         ; pwd
        Sulfur                                         ; 721         ; pwd
        Sulfur (granular)                              ; 1121        ; pwd
        Sunflower seed                                 ; 609         ; pwd
        Talcum powder                                  ; 881         ; pwd
        Tantalum powder                                ; 641         ; pwd
        Tea                                            ; 433         ; pwd
        Tea (flakes)                                   ; 384         ; pwd
        Tea (powdered)                                 ; 433         ; pwd
        Teflon (fiber)                                 ; 481         ; pwd
        Teflon (granules)                              ; 577         ; pwd
        Teflon (powdered)                              ; 465         ; pwd
        Teflon pellets                                 ; 961         ; pwd
        Terepthalic acid                               ; 481         ; pwd
        Thiamine                                       ; 753         ; pwd
        Thionex                                        ; 481         ; pwd
        Thorium oxide                                  ; 993         ; pwd
        Titanium dioxide                               ; 769         ; pwd
        Tobacco (cigarette)                            ; 192         ; pwd
        Tobacco (powdered)                             ; 449         ; pwd
        Tricalcium phosphate                           ; 561         ; pwd
        Trichicrocyanuric acid                         ; 801         ; pwd
        Tripolyphosphate                               ; 1282        ; pwd
        Trisodium phosphate                            ; 801         ; pwd
        Tumaric (acid fines)                           ; 817         ; pwd
        Tungsten carbide                               ; 4005        ; pwd
        Uranium (compound)                             ; 3060        ; pwd
        Uranium (granules)                             ; 2948        ; pwd
        Uranium oxide                                  ; 1730        ; pwd
        Urea                                           ; 673         ; pwd
        Urea formaldehyde                              ; 577         ; pwd
        Urea powder                                    ; 625         ; pwd
        Urea prills                                    ; 721         ; pwd
        Vermiculite                                    ; 993         ; pwd
        Vinyl acetate                                  ; 577         ; pwd
        Vinyl chips (irregular)                        ; 320         ; pwd
        Vinyl compound                                 ; 577         ; pwd
        Vinyl powder                                   ; 545         ; pwd
        Vinyl resin                                    ; 577         ; pwd
        Wax (flake)                                    ; 801         ; pwd
        Wax (powder)                                   ; 609         ; pwd
        Wheat (hulls)                                  ; 705         ; pwd
        Wheat (shaved)                                 ; 545         ; pwd
        Wheat flour                                    ; 481         ; pwd
        Wheat gluten                                   ; 689         ; pwd
        Wheat middling                                 ; 240         ; pwd
        Wheat, cracked                                 ; 561         ; pwd
        Wheat, whole                                   ; 785         ; pwd
        Whey                                           ; 561         ; pwd
        White lead                                     ; 1362        ; pwd
        Wood chips                                     ; 481         ; pwd
        Wood flour                                     ; 320         ; pwd
        Wood shavings                                  ; 160         ; pwd
        Yeast                                          ; 945         ; pwd
        Zinc ammonium chloride                         ; 1057        ; pwd
        Zinc carbonate                                 ; 561         ; pwd
        Zinc oxide                                     ; 881         ; pwd
        Zinc powder                                    ; 3364        ; pwd
    ''')
if 1:   # References
    refdoc = dedent('''
 
        This set of data was culled from numerous sources and took a number
        of years to compile.  Some things I learned from this exercise
        (done around 2013) are:
            - There's a lot of copying of data on the web, so finding all
              the sites you can and coalescing their data just leads to a
              bunch of incestuous data and is a waste of your time.
            - You need to be careful of errors, both published and in
              transcribing.
            - It's a lot of work.
            - My goal was to include data that I could attribute.  This has
              been handy, as a few times I wondered about the number I was
              using and referring back to the original source showed I had
              made a mistake transcribing it.
            - Do not make any assumptions about the uncertainty of a
              given number based on the number of significant figures it
              has.  Rigorous uncertainty information is not available in
              any of the references consulted.  

        I divide these references up into two categories:  primary and
        secondary.  Primary references are those published books that tend
        to be standard references and which are probably held to higher
        scholarship standards because of numerous editions and careful
        editing.  Secondary references are those that are either on the web
        or are books that probably don't have the scholarship/attribution
        levels of primary references.
 
        My primary references are: aes asm ceh tel hcp hep mar mhb.  The
        oters are secondary references.  

            mar and mhb are references that originated in the early 1900's
            and have been reviewed and used by many eyes.  mar dates to at
            least as early as 1916 and mhb was on its 5th edition in 1919.

            tel is a 1989 book that contains no attributions for its data,
            yet is a careful compilation by a chemist at King's College,
            London.  It represents his long collection of notes on the
            properties of the elements.  To me, it appears to be
            meticulously edited and stands up to modern notations and
            proper SI unit use.  While lacking attributions, my sense tells
            me this author would have carefully researched all the
            fundamental data and cross-checked it in the literature,
            primarily because his name was going to be on the work.  It
            probably represents a lifetime of work.  It reached a second
            edition, but appears to be out of print.  You can find used
            copies on Amazon for under $10 as of Apr 2022.
 
        I make no judgment regarding the veracity of all of these numbers,
        as my "built-in doubter" suspects all of them, even those from the
        primary references.  

        If you're making an important decision based on some density data,
        search out the primary sources of this information, which will
        probably be in some chemical or physical journal.  Supplement it
        with basic measurements of your own -- you should be able to work
        to at least 1% levels without a fancy lab.

        Example:  suppose we want the density of aluminum.  You'll get the
        following values in kg/m3 from the above data
            2640    glo 390
            2698    tel 12
            2700    pht
            2700    aes 117
            2700    mhb 2270
            2770    asm 52 (2024 alloy)
            2680    asm 52 (5052 alloy)
            2700    asm 52 (6061 alloy)
            2698.9  asm 52 (99.995%)

 
    ''')
    g.references = {
        # All references are indexed by 3-letter strings
        "aes" : dedent('''
                Bolz & Tuve, "Handbook of Tables for Applied Engineering
                Science", 2nd ed., CRC Press, 1973.'''),
        "asm" : dedent('''
                American Society of Metals, "Metals Handbook", Vol. 1,
                8th ed., 1961 (9th printing, Aug 1977).'''),
        "ceh" : dedent('''
                Perry (ed.), "Chemical Engineers' Handbook", 5th ed.,
                McGraw-Hill, 1973.'''),
        "tel"  : dedent('''Emsley, "The Elements", Oxford, 1989.'''),
        "glo" : dedent('''Glover, "Pocket Ref", Sequoia Publishing, 16th
                printing, 1993.'''),
        "hcp" : dedent('''
                Weast (ed.), "CRC Handbook of Chemistry and Physics",
                CRC, 59th ed., 1978.'''),
        "hep" : dedent('''
                Koshkin & Shirkevich, "Handbook of Elementary Physics",
                3rd ed., MIR Publishers, 1977.'''),
        "mar" : dedent('''
                Marks, "Standard Handbook for Mechanical Engineers",
                7th ed., McGraw-Hill, 1967.'''),
        "msa" : "Measured by script author",
        "mhb" : dedent('''
                Oberg, Jones, Horton, "Machinery's Handbook", 21st
                ed. (1979), 19th ed. (1972), Industrial Press, 1979.'''),
        "pht" : dedent('''
                "Physics Hypertextbook", http://physics.info/density
                (various pages accessed on various dates)'''),
        "pvc" : dedent('''
                http://www.pvc.org/en/p/specific-gravity-density
                (accessed 13 Nov 2018)'''),
        "pwd" : dedent('''https://www.powderhandling.com.au/bulk-density-chart,
                (accessed 2 Jul 2021)'''),
        "sim" : dedent('''
                http://www.simetric.co.uk/si_materials.htm
                (accessed 27 Jan 2013)'''),
        "web" : "From web, location and date not noted.",
        "wkp" : dedent('''
                Wikipedia http://en.wikipedia.org, accessed various
                pages on various dates.'''),
    }
    g.categories = bidict()
    g.categories.update(
        {
            'None':     0,
            'gas':      1,
            'liquid':   2,
            'metal':    3,
            'mineral':  4,
            'misc':     5,
            'plastic':  6,
            'wood':     7,
        }
    )
if 1:   # Generate output
    def GetNum(s):
        '''s is a density in g/cc or a range of such densities.  Change it
        to a float, convert it to kg/m3, and round it to the number of
        significant figures in the original string.  If it's a range with
        two numbers, use the smaller of the two significant figures.
        Return it as a string representing a density in kg/m3 or a range of
        densities in kg/m3.
        '''
        from roundoff import RoundOff, SigFig
        maxfig = 6  # Max from data is 5 figures
        if "-" in s:
            x = [float(i) for i in s.split("-")]
            nlow, nhigh = [SigFig(i) for i in x]
            n = min(nlow, nhigh)
            x = [flt(i) for i in x]
            # The components in x are flt instances, so we'll get their
            # strings to the requisite number of figures
            with x[0]:
                x[0].n = n
                x[0].rtz = x[0].rtdp = True
                a, b = [str(1000*flt(i)) for i in x]
                if a == b:
                    return a
                else:
                    return '-'.join((a, b))
        else:
            x = float(s)
            n = SigFig(x)
            y = flt(x)
            with y:
                y.n = n
                y.rtz = y.rtdp = True
                return str(1000*y)

if 1:
    class Ref:
        def __init__(self, s):
            f = s.split()
            self.key = f[0]
            self.pg = None
            if len(f) > 1:
                self.pg = f[1]
            # Make sure it's in g.references
            if self.key not in g.references:
                raise ValueError(f"'{self.key}' not in g.references")
        def __lt__(self, other):
            assert(ii(other, Ref))
            return self.key < other.key
        def __eq__(self, other):
            assert(ii(other, Ref))
            return self.key == other.key
        def __repr__(self):
            return str(self)
        def __str__(self):
            s = f"{self.key} {self.pg}" if self.pg else self.key
            return repr(s)
    class Den:
        maxlen = 50     # Maximum length of name string
        def __init__(self, line, category):
            self._line = line
            f = line.split(";")
            self.category = category
            self.name = f[0].strip()
            self.rho = GetNum(f[1])
            self.ref = Ref(f[2])
        def __str__(self):
            'Print in form suitable for a sequence'
            s = f"{self.name!r},"
            return f"({s:{Den.maxlen}s} {self.rho!s:12s}, {self.ref!r}),"
        def get_rho(self, s):
            if "-" in s:
                low, high = [1000*flt(i) for i in s.split("-")]
                self._rho = s
                return (low + high)/2
            else:
                return 1000*flt(s)
    def GenerateOutput():
        x = flt(0)
        x.n = 4
        x.rtz = x.rtdp = True
        if 0:
            lines = g.raw_data.split("\n")
            lines = lines[:5]
        else:
            lines = GetLines(g.raw_data, script=True, ignore_empty=True)
        for line in lines:
            line = line.strip()
            if line.startswith("category"):
                category = line.split("=")[1].strip()
                continue
            if not line or line.startswith("#"):
                continue
            d = Den(line, category)
            print(d)
if __name__ == "__main__": 
    GenerateOutput()

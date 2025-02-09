'''
Search for text in the components database
'''
if 1:   # Data
    data = '''

        The compartments are numbered from left to right and front to back.  These data are free
        form.  The actual data lines contain three integers separated by colons:
            Box
            Compartment
            Quantity
        The default quantity parameter is ? at the moment, but will eventually get set to the
        actual count or a symbol.

        This also allows for another field (maybe called shelf) that locates it on a bookcase,
        rolling cart, or shelves in another room.

        Each data line's description is free form and optional keywords follow a no-break space
        (use 'nbs' in vim).

        Box 1
            1:1:?    Component pins   pin
            1:1:?    Pin rings   pin
            1:1:?    Pin sockets   pin socket
            1:1:?    Test pins   pin
            1:2:?    CAT5 jack connector, female RJ-45, panel mount   jack connector
            1:2:?    Capacitor, 20 pF   capacitor
            1:3:?    3-5 V piezo device   sound
            1:4:?    Various Radio Shack (276-1657) CdS photocells   opto
            1:5:?    Small relays   relay switch
            1:7:?    #6 solder lugs   lug
            1:6:?    0.1 uF capacitor   capacitor
            1:7:?    Jumpers   jumper
            1:8:?    3 V piezo buzzer   sound
            1:9:?    2 kHz piezo buzzer   sound
            1:10:?    Piezo buzzers   sound
            1:11:?    Microphone   sound
            1:11:?    Piezo, buzzer   sound
            1:12:?    Piezo, buzzer   sound
            1:13:?    Speaker, small, 8 ohm   sound
            1:14:?    2 kHz piezo buzzer   sound
            1:15:?    Buzzer 1.2-3.5 V   sound
            1:16:?    Chime, 1.5-3 V, 30-60 mA, two tone, + RED, -BLK, connect WHT to + for sound   sound
            1:17:?    Piezo, buzzer   sound
            1:18:?    Piezo, buzzer   sound
        Box 2
            2:1:?    LEDs, misc (high brightness, UV)   opto LED
            2:2:?    120 VAC neon indicator in threaded housing   opto
            2:2:?    Small red panel mount LEDs in threaded housing   opto LED
            2:3:?    Threaded housing for 3 mm LED   opto
            2:3:?    Threaded housing for 5 mm LED   opto
            2:4:?    LED, red, 3 mm   opto LED
            2:5:?    Plastic bezels for 5 mm LEDs   opto
            2:6:?    Lamps with wires, small pea bulbs   opto
            2:6:?    LED, red, 3 mm, fairly bright with short leads   opto LED
            2:6:?    Neon bulbs   opto
            2:7:?    LED, amber, 3 mm   opto LED
            2:8:?    LED, red, 3 mm   opto LED
            2:9:?    LED, red, 5 mm   opto LED
            2:10:?    LED, green, 5 mm   opto LED
            2:11:?    LED, yellow, 5 mm   opto LED
            2:12:?    Misc. LEDs   opto LED
            2:12:?    Thermistor, 10 kohms @ 25 deg C, Radio Shack 271-110   thermistor
            2:13:?    7 segment LEDs   opto
            2:14:?    3 mm photodiode   opto diode
            2:14:?    Radio Shack 276-145A NPN Si IR phototransistor 5 mm 20 mA   opto
            2:15:?    Radio Shack 276-142 IR detector and emitter pair, 5 mm LED package   opto LED
            2:16:?    HP alphanumeric LED display   opto
            2:16:?    LED bars   opto LED
            2:17:?    2N3704 NPN 30 V 500 mA, hfe=100-300   NPN
            2:17:?    74HC74N dual D flip-flop   IC TTL
            2:17:?    Luxeon star, 1 W, white   LED LED
            2:17:?    MPQ2222A Motorola, quad NPN transistor (HP 1858-0112)   NPN
            2:18:?    7 segment LEDs   opto LED
        Box 3
            3:1:?    Cable clamps   misc
            3:1:?    Captured fastener, right angle   fastener
            3:1:?    Tinnerman fastener   fastener
            3:2:?    fastener, 4.2" long, 1/4" dia, plated steel   fastener
            3:2:?    fasteners   fastener
            3:3:?    fasteners   fastener
            3:4:?    Star fasteners   fastener
            3:5:?    fasteners   fastener
            3:6:?    fasteners   fastener
            3:7:?    fasteners   fastener
            3:8:?    Molex pins   pin
            3:8:?    Rubber fastener   fastener
            3:9:?    Thumb fasteners   fastener
            3:10:?    fasteners, nylon   fastener
            3:11:?    fasteners, nylon   fastener
            3:12:?    fasteners   fastener
        Box 4
            4:1:?    2N5114 transistor, P-channel JFET, < 75 ohm, 30 V, 500 mW   FET transistor
            4:1:?    4-pin transistor socket   socket
            4:2:?    1855-0078 N-channel JFET, depletion mode   FET transistor
            4:3:?    1854-0019 HP NPN transistor, silicon, TO-18   NPN transistor
            4:4:?    1853-0316 Dual PNP, ITS-1160, (?) 40 V 200 mA   PNP transistor
            4:5:?    TI932 (?), was labeled as 1855-0078   
            4:6:?    1854-0071 NPN   NPN transistor
            4:7:?    2N2160 unijunction transistor, GE   misc transistor
            4:7:?    2N2907 PNP 40 V 800 mA, hfe=100-300 at 150 mA   PNP transistor
            4:7:?    2N5416 PNP 300 V 1 A, hfe=5 at 5 mA   PNP transistor
            4:7:?    2N697 NPN 40 V 150 mA, hfe=3-12   NPN transistor
            4:8:?    1853-0036 PNP 2N3906 40 V 200 mA, hfe=80   PNP transistor
            4:9:?    1853-0462 PNP   PNP transistor
            4:9:?    2N3440 NPN 250 V 1 A, hfe=40-160   NPN transistor
            4:9:?    2N3635 PNP 140 V 1 A, hfe=100-300   PNP transistor
            4:10:?    1854-0045 NPN  hfe=150   NPN transistor
            4:11:?    1854-0045 NPN  hfe=150   NPN transistor
            4:12:?    1854-0404 NPN small signal transistor, National NS04008   NPN transistor
            4:13:?    LM725 op amp   opamp linear
            4:13:?    Small 600 uA meter (from old Omega TC box)   misc
            4:14:?    2N2369A NPN 40 V 200 mA, hfe=20-40   NPN transistor
            4:15:?    2N2907A PNP 60 V 600 mA, hfe=100-450   PNP transistor
            4:16:?    LF353AH Dual input JFET op amp, 8-pin metal can   opamp linear
            4:17:?    1826-0217 HP IC, op amp, TO-99 8 pin package   IC linear
            4:18:?    2N3251 PNP 40 V 200 mA, hfe>90   PNP transistor
        Box 5
            5:1:?    Switches, pushbutton   switch
            5:2:?    Switch, rotary, 7 position, single deck    switch
            5:2:?    Switch, slide    switch
            5:3:?    Ring terminals, various   terminal
            5:3:?    Switch, toggle, momentary   switch
            5:4:?    Switch, toggle, single throw   switch
            5:5:?    Switch, toggle, double throw   switch
            5:6:?    Switch fasteners   hardware
            5:7:?    Switch, DIP   switch
            5:8:?    Switch, various PC mount plastic toggle   switch
            5:9:?    Switch, toggle, DPDT, momentary, large   switch
            5:9:?    Thermal sensors (switches) (?)   thermostat
            5:10:?    Switch, rocker   switch
            5:11:?    Switch, rocker   switch
            5:12:?    Switch, rocker   switch
            5:12:?    Switch, small microswitches   switch
        Box 6
            6:1:?    4 mm banana jacks, mostly salvaged HP   banana
            6:2:?    CalTest 4 mm shrouded banana plug, fastener, red and black   banana
            6:3:?    CalTest 4 mm banana plug, red or black   banana
            6:4:?    CalTest 4 mm banana plug, no fastener needed, red or black   banana
            6:5:?    4 mm banana jacks, salvaged, red and black, single and double   banana
            6:6:?    4 mm banana jacks, tall, red and black   banana
            6:7:?    4 mm banana jacks, mostly salvaged HP   banana
            6:8:?    Red pin jacks   jack
            6:9:?    Misc. banana plugs   banana
            6:10:?    Ground banana jacks, nickel plated   banana
            6:11:?    CalTest low profile banana jacks, black   banana
            6:12:?    CalTest low profile banana jacks, red   banana
        Box 7
            7:1:?    1N3600 silicon diode 100 PIV, 200 mA   diode
            7:1:?    1N4004 diode 400 PIV, 1 A   diode
            7:1:?    Zener 12 V 30 mA   zener
            7:1:?    1N759 zener 12 V 30 mA   zener
            7:1:?    1N965 zener 15 V 400 mA   zener
            7:1:?    1N4728 zener 3.3 V @ 100 mA   zener
            7:1:?    9.5 V rated silicon diode   diode
            7:1:?    9.5 V rated silicon diode   diode
            7:1:?    Assorted small signal diodes, silicon   diode
            7:1:?    C battery holder (holds one battery)   battery
            7:1:?    Zener 1/2 W: 3.3 4.7 5.1 6.2 7.5 8.2 9.1 10 12 15 18 24 27 30 V   zener
            7:2:?    Various AGC fuses   fuse
            7:3:?    Small silicon diodes (probably 1N4148), adhesive on leads (from Steve King)   diode
            7:4:?    DC micromotor, 1 rev/s at 6 VDC, 10 mA no load current, 100 mA under load   misc
            7:5:?    1N4004 diode 400 PIV, 1 A   diode
            7:5:?    Round fluorescent starters, two pin   opto
            7:6:?    D battery holder (holds one battery)   battery
            7:6:?    Misc. resistors (can toss)   resistor
            7:7:?    OPB1941 photodiode/phototransistor (?)   opto
            7:8:?    9 volt battery adapter   battery
            7:9:?    Surface mount to PCB adapters, various sizes   adapter
            7:10:?    12 VDC LED assembly   opto
            7:10:?    USB connector to PC board   USB connector
            7:10:?    Lithium coin cell battery holder (20 mm, fits 2025 and 2032)   battery
            7:11:?    10 W resistor, 20 ohm   resistor
            7:11:?    10 W resistor, 24 mohm   resistor
            7:11:?    Precision resistor, 200.9 ohms   resistor
            7:12:?    MPJA level sensors   sensor
            7:12:?    Incandescent flashlight bulbs   opto
        Box 8
            8:1:?    Pot, 10 ohm, 10 turn PC mount   pot
            8:2:?    Pot, 20 ohm, 10 turn PC mount   pot
            8:3:?    Pot, 50 ohm, 10 turn PC mount   pot
            8:4:?    Pot, 100 ohm, 10 turn PC mount   pot
            8:4:?    Pot, 100 ohm, square & round, 1 turn PC mount   pot
            8:5:?    Pot, 200 ohm, round, 1 turn PC mount, facing normal to board, finger turn   pot
            8:6:?    Pot, 500 ohm, 10 turn PC mount   pot
            8:6:?    Pot, 500 ohm, round, 1 turn PC mount, facing normal to board   pot
            8:6:?    Pot, 500 ohm, round, 1 turn PC mount, facing normal to board, finger turn   pot
            8:7:?    Pot, 1 kohm, round, 1 turn PC mount, facing normal to board, finger turn   pot
            8:8:?    Pot, 2 kohm, 10 turn PC mount   pot
            8:9:?    Pot, 5 kohm, 1 turn PC mount, round, finger turn   pot
            8:9:?    Pot, 5 kohm, 10 turn PC mount   pot
            8:10:?    Pot, 10 kohm, 10 turn PC mount   pot
            8:11:?    Pot, 20 kohm, 1 turn PC mount, round   pot
            8:11:?    Pot, 20 kohm, 10 turn PC mount   pot
            8:12:?    Pot, 50 kohm, 1 turn PC mount, round, facing normal to board, miniature   pot
            8:12:?    Pot, 50 kohm, 1 turn PC mount, square, facing normal to board   pot
            8:13:?    Pot, 100 kohm, 10 turn PC mount   pot
            8:14:?    Pot, 200 kohm, 10 turn PC mount   pot
            8:15:?    Pot, 500 kohm, 10 turn PC mount   pot
            8:16:?    Pot, 1 Mohm, 10 turn PC mount   pot
            8:17:?    Pot, 2 Mohm, 10 turn PC mount   pot
            8:18:?    World War 2 1/4" pot shaft waterproof feedthrough   hardware
        Box 9
            9:1:?    Socket, transistor, TO-92   socket
            9:2:?    Relay, 12 V, DPDT, latching   relay switch
            9:3:?      
            9:4:?    Luxeon star LED, 350 mA max   opto
            9:5:?    555 timer   IC linear
            9:5:?    556 timer (dual 555)   IC linear
            9:6:?    8-pin DIP sockets   socket
            9:7:?    1826-0065 LM311 comparator   IC linear
            9:7:?    1826-0311 LM201A op amp   opamp linear
            9:7:?    74LS14 hex inverter with Schmitt trigger   IC TTL
            9:7:?    CD4051 8 channel analog mux CMOS   IC CMOS
            9:8:?    74LS151 8-channel digital mux   IC TTL
            9:9:?    CA3094E transconductance amplifier, Intersil   IC linear
            9:10:?    Orthodontic rubber bands   misc
        Box 10
            10:1:?    Pot, 2 kohm, PC mount, finger dial   pot
            10:2:?    Pot, 250 ohm, PC mount, finger dial   pot
            10:3:?    Pot, 2.4 kohm, PC mount, finger dial   pot
            10:4:?    Pot, 800 kohm, PC mount, fastener driver dial   pot
            10:5:?    Pot, 500 ohm, PC mount, finger dial   pot
            10:6:?    Pot, 2 kohm, PC mount, finger dial   pot
            10:7:?    Pot, 100 ohm, PC mount, finger dial   pot
            10:8:?    Pot, 250 kohm, PC mount, finger dial   pot
            10:9:?    Pot, 50 kohm, PC mount, finger dial   pot
            10:10:?    Pot, 480 ohm, PC mount, finger dial   pot
        Box 11
            11:1:?    Capacitor, adjustable, 3 to 9 pF   capacitor
            11:2:?    Power jack, takes 5.5/2.1 mm plug, also plugs   jack
            11:3:?    1 A, 120 VAC SSR solid state relay, Grayhill 70YY14350   relay switch
            11:4:?    2 A, 120 VAC SSR solid state relay, Kyotto KB20C02A, 3-32 VDC in   relay switch
            11:5:?    1 A, 120 VAC SSR solid state relay, Grayhill 70YY14350   relay switch
            11:6:?    TIP120 NPN Darlington 60 V 5 A, TO220, BCE from front, tab is B   NPN transistor
            11:7:?    12 VDC reed relay, 1 kohm coil, single pole NO   relay switch
            11:8:?    2N2222 NPN 30 V 600 mA, hfe=35-300   NPN transistor
            11:9:?    LF353 Dual JFET op amp, 8-pin DIP   opamp linear
            11:9:?    PT27311 current transformer, 30-200 kHz   transformer
            11:10:?    Photosensitive resistors from 1960's HP differential voltmeter   opto
        Box 12
            12:1:?    Chunk of broken UV glass   opto
            12:2:?    Frosted neon bulbs, short   opto
            12:3:?    741 op amp   opamp linear
            12:4:?    4066 quad bilateral switch CMOS   IC CMOS
            12:4:?    74LS04 hex inverter   IC TTL
            12:5:?    fasteners, red LED, 2N3904 transistor   misc
            12:6:?    10 kohm resistor   resistor
            12:7:?    470 ohm resistor   resistor
            12:8:?    Various disk capacitors   capacitor
            12:9:?    Diodes   diode
            12:10:?    Capacitor, 10 nF, bypass   capacitor
        Box 13
            13:1:?      
            13:2:?      
            13:3:?      
            13:4:?      
            13:5:?      
            13:6:?      
            13:7:?      
            13:8:?      
            13:9:?      
            13:10:?      
        Box 14
            14:1:?    Various inductors (coils) around 0.5 uH   inductor
            14:2:?    Various inductors (coils) around 0.2 uH   inductor
            14:3:?    Small matching transformer, 1:1, around 500 mH   transformer
            14:4:?    Various inductors (coils) around 0.2 uH   inductor
            14:5:?    Various inductors (coils) around 10 uH   inductor
            14:6:?    Ferrite toroid, square, 10 mm dia, 3 mm thick   ferrite
            14:7:?    Ferrite toroid, square, 13 mm dia, 5 mm thick, 7 mm ID   ferrite
            14:8:?    Ferrite toroid, square, 19 mm dia, 10 mm thick, 9 mm ID   ferrite
            14:9:?    Ferrite toroid, square, 13 mm dia, 6 mm thick, 7 mm ID   ferrite
            14:10:?    Ferrite toroid, square, 10 mm dia, 5 mm thick, 5 mm ID, with 2 wires, 2 turns   ferrite
        Box 15
            15:1:?    Capacitor, 68 uF, 15 V, electrolytic, 1970's Sprague salvaged from Ithaca lock-in   capacitor
            15:2:?    Capacitor, 15 uF, 20 V, electrolytic, 1970's Sprague salvaged from Ithaca lock-in   capacitor
            15:3:?    Capacitor, 100 pF, 1 kV, ceramic?   capacitor
            15:4:?    US Sensor PT502J2 bead thermistor, 5 kohm @ 25 °C, 0.2 °C accuracy   thermistor
            15:5:?    5 V 5 mW 650 nm lasers   opto
            15:6:?    D battery holder (holds one battery)   capacitor
            15:6:?    Capacitor, 100 nF, 100 V, 1970's GE salvaged from Ithaca lock-in   capacitor
            15:7:?    Capacitor, 205 uF, 10 V, 1970's Kemet salvaged from Ithaca lock-in   capacitor
            15:8:?    Capacitor, 2 uF, 200 V, 1970's Electrocube salvaged from Ithaca lock-in   capacitor
            15:9:?    Capacitor, 0.977 uF, 200 V, 1970's Electrocube salvaged from Ithaca lock-in   capacitor
            15:10:?      
        Box 16
            16:1:?    Ring terminal, blue, #10   terminal
            16:2:?    Ring terminal, blue, #8   terminal
            16:3:?    Spade terminal, blue, #10   terminal
            16:4:?    Spade terminal, blue, #10   terminal
            16:5:?    Spade terminal, blue, #8   terminal
            16:6:?    Spade terminal, blue, #8   terminal
            16:7:?    Spade terminal, red, #8   terminal
            16:8:?      
            16:9:?    Spade terminal, red, #6   terminal
            16:10:?      
        Box 17
            17:1:?    Resistor, precision, 1 kohm, HP from June 1968, 0.1%   resistor
            17:2:?    Resistor, precision, 1.001 kohm, HP from June 1968, 0.0075%   resistor
            17:2:?    Resistor, Dale, 10 W, 0.025 ohm   resistor
            17:3:?    Resistor, precision, 1111 ohm, Daven   resistor
            17:4:?    Resistor, precision, 10.101 kohm, HP from May 1968, 0.02%   resistor
            17:5:?    Resistor, precision, 206.1, IRC   resistor
            17:6:?    Resistor, precision, 2 kohm, RCL, 0.05%   resistor
            17:7:?    Resistor, precision, 4 kohm, Daven   resistor
            17:8:?    Resistor, power, 55 kohm, Dale, 10 W   resistor
            17:8:?    Resistor, power, 20 ohm, Dale, 10 W   resistor
            17:8:?    Resistor, power, 25.49 mohm, Dale, 10 W   resistor
            17:9:?    Resistor, precision, 89.975 kohm, HP from Mar 1966, 0.02%   resistor
            17:10:?    Resistor, power, Dale, 0.1337 ohm, about 3 W, three resistors in parallel   resistor
        Box 18
            18:1:?    AGC fuse holder, end   fuse
            18:2:?    Pins, gold-plated, and matching sockets   pin
            18:3:?    AGC fuse holder, panel mount   fuse
            18:3:?    10 A and 0.25 A multimeter fuses (for Aneng DMMs)   fuse
            18:3:?    1N5817G Schottky diode, 20 PIV, 1 A   diode
            18:4:?    AGC fuse holder, panel mount   fuse
            18:4:?    2 A AGC slo-blo fuses   fuse
            18:5:?    IRF630 N channel MOSFET 200 V   transistor
            18:5:?    Socket, 8-pin DIP   socket
            18:6:?    16 pin ZIF socket   socket
            18:6:?    Jumper, 0.1 inch   jumper
            18:7:?    Fuse, AGC, various sizes   fuse
            18:8:?    Jumper, fits 8-pin DIP socket   jumper
            18:9:?    Fuse, AGC, various sizes   fuse
            18:10:?    1A 250 V lever snap action microswitch   switch
            18:11:?    2N7000 MOSFET transistor   MOS
            18:12:?    IC tube pin (closes IC antistatic tube off)   misc
            18:12:?    0.2 A AGC-size fuse for Aneng 870 DMM   fuse
        Box 19
            19:1:?    LF353 dual JFET op amp, 8-pin DIP   opamp linear
            19:2:?    LM224 quad op amp, 14-pin DIP   opamp linear
            19:2:?    LM324 quad op amp, 14-pin DIP   opamp linear
            19:3:?    CA3140  op amp, 8-pin DIP   opamp linear
            19:3:?    LM2904 dual op amp (like LM358), 8-pin DIP   opamp linear
            19:4:?    741 op amp, 8-pin DIP   opamp linear
            19:4:?    747 dual op amp, 14-pin DIP   opamp linear
            19:5:?    CA3130 op amp, 8-lead metal can   opamp linear
            19:6:?    LM386 low power audio amplifier, 8-pin DIP   IC linear
            19:6:?    MAX480 micropower op amp   opamp linear
            19:6:?    TS912IN dual CMOS op amp   opamp linear
            19:7:?    1826-0123 LM320-12K negative 12 V regulator TO-3   IC linear
            19:7:?    2N1487 NPN 40 V 6 A, hfe=15-45   NPN transistor
            19:8:?    LM339 quad comparator, 14-pin DIP (HP part no. 1826-0138)   IC linear
            19:9:?    ECG56020 triac, 25 A, 400 V, 2.5 V gate voltage, 50 mA gate current   misc
            19:9:?    NTE5638 triac, 400 V, 8 A, 80 A surge, 2 V gate voltage max, 10 mA gate current   misc
            19:10:?    LM350 adjustable regulator, 3 A, TO-3   IC linear
            19:11:?    LM338 regulator, 5 A, TO-3   IC linear
            19:12:?    LM338 regulator, 5 A, TO-3   IC linear
        Box 20
            20:1:?    LM285Z-1.2 voltage reference, TO-92   IC linear
            20:1:?    LM285Z-2.5 voltage reference, TO-92   IC linear
            20:1:?    MAX8069 1.2 volts voltage reference, TO-92   IC linear
            20:1:?    MAX872 2.5 volts voltage reference, 8-pin DIP   IC linear
            20:2:?    CD40106/74C14 hex inverter Schmitt trigger CMOS   IC CMOS
            20:2:?    CD40192/74C192 synchronous 4-bit up/down decade counter CMOS   IC CMOS
            20:2:?    CD4047 monostable/astable multivibrator CMOS   IC CMOS
            20:2:?    CD4082 dual 4-input AND gate CMOS   IC CMOS
            20:3:?    4001 quad 2-in NOR CMOS   IC CMOS
            20:3:?    4093 quad 2-in NAND Schmitt trigger CMOS   IC CMOS
            20:3:?    74AC14 hex inverter with Schmitt trigger   IC TTL
            20:3:?    7555 CMOS version of 555   IC CMOS
            20:4:?    1N5818 Schottky diode 30 V 1 A, 0.26 V @ 10 mA   diode
            20:4:?    4N25 opto isolator   opto
            20:4:?    4N26 opto isolator   opto
            20:4:?    6N139 opto isolator Darlington   opto
            20:4:?    Diac   misc
            20:5:?    IRF540 NMOS FET 33 A, 100 V, 44 mohm   FET transistor
            20:6:?    74F240 octal buffer with 3-state outputs   IC TTL
            20:7:?    IRF3205 NMOS FET 75 A, 33 V, 8 mohm   FET transistor
            20:8:?    74LS251M 3 state 1-of-8 line data selector/mux   IC TTL
            20:9:?    210A102 SIP resistors, 1 kohm, Allen-Bradley   resistor
            20:9:?    DIP resistors, 1 kohm   resistor
            20:10:?    LM317 adjustable voltage regulator   IC linear
            20:10:?    TL780-05C 5 V voltage regulator   IC linear
            20:11:?    7812 voltage regulator TO220   IC linear
            20:12:?    7818 voltage regulator TO220   IC linear
            20:12:?    7805 voltage regulator TO220   IC linear
        Box 21
            21:1:?    Alligator clips   misc
            21:2:?    BNC all-female tees and angles   adapter BNC
            21:3:?    BNC splices (male and female)   adapter BNC
            21:4:?    BNC tees   adapter BNC
            21:5:?    BNC female to double banana plug   adapter BNC
            21:6:?    BNC male to double banana jack   adapter BNC
            21:7:?    Sheathed banana (female) to unsheathed banana plug   adapter banana
            21:8:?    Photodiode with BNC mount   opto
            21:8:?    UHF male to BNC female adapter   adapter BNC
            21:8:?    BNC female to N male   adapter BNC
            21:9:?    Dual banana plugs   banana
            21:10:?    BNC 50 ohm terminators and feedthroughs   adapter BNC
            21:11:?    Banana jack to 120 VAC ground male   adapter banana
            21:12:?    Lug to banana jack adapter   adapter banana
        Box 22
            22:1:?    PICDEM lab parts -- short wires   misc
            22:2:?    PICDEM lab parts -- jumpers   jumper
            22:3:?    PICDEM lab parts -- 1 k resistors   resistor
            22:4:?    PICDEM lab parts -- LEDs   opto
            22:5:?    PICDEM lab parts -- 10 uF 35 V cap   capacitor
            22:6:?    PICDEM lab parts -- resistors, pot   resistor
            22:7:?    PICDEM lab parts -- resistor   resistor
            22:8:?    PICDEM lab parts -- resistor   resistor
            22:9:?    PICDEM lab parts -- resistor   resistor
            22:10:?    PICDEM lab parts -- 10 uF cap   capacitor
        Box 23 is he cardboard box of resistors
            23:1:?    inductor (coil), 2 uH, 0.77 ohm   inductor
            23:1:?    inductor (coil), 150 uH, 4.41 ohm   inductor
            23:1:?    inductor (coil), 10 uH, 0.72 ohm   inductor
            23:1:?    inductor (coil), 6.8 uH, 0.42 ohm   inductor
            23:1:?    inductor (coil), 2.2 uH, 0.86 ohm   inductor
            23:1:?    inductor (coil), 22 uH, 2.25 ohm   inductor
            23:1:?    inductor (coil), 0.55 uH, 0.19 ohm   inductor
            23:1:?    inductor (coil), 2.6 uH, 0.49 ohm   inductor
            23:1:?    inductor (coil), 33 uH, 2.44 ohm   inductor
            23:1:?    inductor (coil), 1.5 uH, 0.36 ohm   inductor
            23:1:?    inductor (coil), 1 mH, 15 ohm   inductor
            23:1:?    FET, 100 A (Rch < 1 mohm if Vgs > 5.39 V)   FET transistor
        Box 24
            24:1:?    Various small batteries   battery
            24:2:?    Precision current transformer 50 A = 10 mA, 20 Hz to 20 kHz banggood 991591   ferrite transformer
            24:3:?    16-pin DIP header (socket) for 8 resistor-type components   socket
            24:4:?    Super capacitors   capacitor
            24:5:?    Mercury switch, 2 A rating   switch
            24:6:?    5 A panel mount circuit breaker, 125 VAC   breaker
            24:7:?    15 A panel mount circuit breaker, 50 VDC, 120/240 VAC   breaker
            24:8:?    15 A panel mount circuit breaker, 50 VDC, 120/240 VAC   breaker
            24:9:?    10 A panel mount circuit breaker, 50 VDC, 120/240 VAC   breaker
            24:10:?    15 A panel mount circuit breaker, 50 VDC, 120/240 VAC   breaker
            24:11:?    15 A panel mount circuit breaker, 50 VDC, 120/240 VAC   breaker
            24:12:?    15 A panel mount circuit breaker, 50 VDC, 120/240 VAC   breaker
            24:13:?    Fahnestock clips   terminal
            24:14:?    FDP8030L MOSFET transistor, 80 A 30 V   transistor
            24:15:?    MPJA mini 3 W per channel stereo amplifier   amplifier
            24:15:?    LTC1968 RMS-to-DC converter 500 kHz   IC
            24:16:?    50 A 1 kV PIV full wave bridge rectifier   diode
            24:16:?    Rubber feet   diode
            24:17:?    DPDT toggle switch   switch
            24:18:?    DPDT toggle switch   switch
            24:19:?    1/8" phone plug adapters   adapter
            24:20:?    RCA jack adapters   adapter
            24:21:?    F adapters   adapter
            24:22:?    N, UHF adapters   adapter
            24:23:?    Mini toggle switch DPDT on-off-mom 6 A at 125 V AC   switch
            24:24:?    Grayhill 240 VAC SSR 3.5 A solid state relay   relay
        Box 25
            25:1:?    5 mm RGB LEDs (12 cents each from banggood)   opto
            25:1:?    High gain μV/mV amplifier module, gain 1.5 to 1000   IC
            25:1:?    2.5/5/7.5/10 V voltage reference   IC
            25:1:?    GR precision wirewound resistors (1, 10, 100, 1000 kΩ) from 1656 impedance bridge   resistor
            25:2:?    650 nm laser 5 mW, 5 V, two wires   opto
            25:2:?    LM34 temperature IC   IC
            25:3:?    Green 5 mm LED   opto LED
            25:4:?    Red 5 mm LED   opto LED
            25:5:?    Blue 5 mm LED   opto LED
            25:6:?    Yellow 5 mm LED   opto LED
            25:7:?    White 5 mm LED   opto LED
            25:8:?    Miniature DPDT center-off toggle switches 6 A 120 V   switch
        Box 26
            26:1:?    8 and 10 pin SIP, resistor, 1k   resistor
            26:2:?    10 pin SIP, resistor, 1.5k   resistor
            26:3:?    8 pin SIP, resistor, 10k   resistor
            26:4:?    8 pin SIP, resistor, 10k   resistor
            26:5:?    Resistor SIP & DIP, various   resistor
            26:6:?    10 pin SIP, resistor, 3.3k   resistor
            26:7:?    Roller microswitches, 5 A 120/240 VAC, 20x10x5 mm   switch
            26:8:?    2 channel push stereo/speaker connectors, red & black, panel mount   terminal
            26:9:?    5 pin mini connector, bulkhead, 10 mm, male & female   connector
            26:9:?    DPDT emergency switch, mushroom head, mechanical latching in activated position   switch
            26:10:?    High gain μV/mV amplifier module, gain 1.5 to 1000   amplifier
            26:11:?    Encoder from MPJA with pushbutton switch   misc
            26:12:?      
            26:13:?    0.6 Ω wirewound resistor 1% 3 W MPJA 27042   resistor
            26:14:?    TO-220 style heat sink kit   misc
            26:15:?    91 MΩ resistor   resistor
            26:15:?    10k, 50k, and 100k NTC thermistors 5%   thermistor
            26:15:?    200 mA fuses for Aneng 8009 meter   fuse
        Box 27
            27:1:?    3 mm LED, yellow, 2.04 V @ 10 mA   opto LED
            27:2:?    3 mm LED, green, 2.02 V @ 10 mA   opto LED
            27:3:?    3 mm LED, red, 1.91 V @ 10 mA   opto LED
            27:4:?    3 mm LED, blue, 2.99 V @ 10 mA   opto LED
            27:5:?    3 mm LED, white, 2.96 V @ 10 mA   opto LED
        Box 28
            28:1:?    Connector pair, locking 8-pin MPJA 32426   connector
            28:2:?    Connector pair, locking 8-pin MPJA 32426   connector
            28:3:?    1N4007 diode   diode
            28:4:?      
            28:5:?    Red boot 35 mm alligator clips MPJA 16452   misc
            28:6:?    Rubber feet   hardware
            28:7:?      
            28:8:?    Banana plugs, screw attach MPJA 30045   banana
            28:9:?    DPDT on-on mini toggle switch MPJA 31886   switch
            28:10:?    Black boot 35 mm alligator clips MPJA 16453   misc
            28:11:?      
            28:12:?      
            28:13:?      
            28:14:?    Dual banana jack MPJA 14492   banana
            28:15:?    Feed-throughs   connector
            28:16:?      
            28:17:?    Plastic tips for Soldapullt   misc
            28:18:?    Dual banana jack MPJA 14492   banana
        Box 29
            29:1:?      
            29:2:?    BNC jacks & hardware   connector
            29:3:?    2N7000 MOSFET transistor   MOS
            29:4:?    Normally closed thermostats, MPJA 38152   thermostat
            29:5:?    Rubber tips & plugs for banana test leads   probe
            29:6:?    Normally open thermostats, MPJA 35719   thermostat
            29:7:?    Standard toggle switch safety cover   switch
            29:8:?    Hamon 0.1 and 0.01 divider parts   misc
            29:9:?      
        Box 30
            30:1:?    Dupont jumper wires, assorted, 100 mm   connector
            30:1:?    AC volts multi-function meter (line voltage & current measurement)   meter
            30:2:?    ZK-TD2 timer module $4.6 ea banggood 19Nov2021 /elec/projects/TimerBox.odt   module
            30:3:?    IRFZ44N N-ch MOSFET 55 V, 17.5 mΩ, 62 °C/W   MOS
            30:4:?      
            30:5:?    5 V relay, 2.5 mA @ 5 V, 15 A 125 V (new 7 Aug 2017 banggood)   relay
            30:6:?    12 V 10 A relay, 60 mA closed (new 19 May 2022, Amazon, $2)   relay
        Box 31
            31:1:?    Header 1x10 pin   socket
            31:2:?    Header 2x3 pin   socket
            31:3:?    Header 1x10 pin   socket
            31:4:?    Header 1x6 pin   socket
            31:5:?    Header 1x8 pin   socket
        Box 32
            32:1:?    Capacitor, 100 nF, 25 V, part no. 104M5C806   capacitor
            32:2:?      
            32:3:?      
            32:4:?      
            32:5:?      
            32:6:?      
            32:7:?      
            32:8:?      
            32:9:?      
            32:10:?      
            32:11:?      
            32:12:?      
            32:13:?      

    '''
if 1:   # Header
    if 1:   # Imports
        import sys
        import os
        import getopt
        import csv
        import re
        from collections import defaultdict
        from pdb import set_trace as xx
        from functools import cmp_to_key
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from columnize import Columnize
        from color import TRM as t
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        beginning_lines_to_ignore = 3
if 1:   # Classes
    class Entry:
        def __init__(self, line_number, info, description, keywords):
            self.line_number = line_number  # 1-based number
            # info will be two integers and a string separated by colons
            self.box, self.compartment, self.quantity = info.split(":")
            self.box = int(self.box)
            self.compartment = int(self.compartment)
            self.description = description.strip()
            self.keywords = keywords.strip().split()
            # Attributes to indicate a regex match in the self.description string
            self.start = None
            self.end = None
        def __str__(self):
            k = '/'.join(self.keywords)
            i = " "*2
            s = (f"{t.box}{self.box:2d}:{t.compartment}{self.compartment:2d}:"
                 f"{t.quantity}{self.quantity:s}{t.n}{i}{self.description}")
            #s = f"{t.box}{self.box:2d}:{t.compartment}{self.compartment:2d}{t.n}{i}{self.description}"
            if k:
                s += f" {t.keyword}[{k}]{t.n}"
            return s
        def __repr__(self):
            return str(self)
        def __lt__(self, other):
            '''Comparison for sorting.  The primary key is the box number and the secondary key is
            the compartment number.
            '''
            if int(self.box) < int(other.box):
                return True
            elif int(self.box) > int(other.box):
                return False
            else:
                return int(self.compartment) < int(other.compartment)
if 1:   # Utility
    def SetColors(on=True):
        # Colors
        t.match = t("skyl") if on else ""
        t.box = t("yel") if on else ""
        t.compartment = t("grn") if on else ""
        t.quantity = t("pnkl") if on else ""
        t.keyword = t("gry") if on else ""
        t.warn = t("ornl") if on else ""     # Color for a missing category warning
    def Usage(status=0):
        print(dedent(f'''
            {sys.argv[0]} [options] [regex [regex2...]]
                Searches the components database for the indicated regular expressions AND'd
                together.  The search is case-insensitive.  Prefix a regex with '-' and anything
                that matches this with the '-' removed will not appear in the output.
            Example
                python '{sys.argv[0]}' diode -zener
                    shows diodes that don't contain 'zener'.
            Options
                -a        Dump all records
                -b N      Show contents of box number N
                -C        Do not use color highlighting
                -c        Show category
                -d        Inspect the data, looking for problems
                -e        Show empty compartments
                -i        Do not ignore case in searches
                -k kwd    Show items with keyword kwd (not case-sensitive)
                -l        List the keywords
                -o        OR the regexes instead of AND
                -v        Print out color code and numbering key 
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Dump all records
        d["-b"] = None      # Specifies box number to list
        d["-C"] = False     # Turn off color highlighting
        d["-c"] = False     # Show category
        d["-d"] = False     # Inspection
        d["-e"] = False     # Show empty compartments
        d["-i"] = True      # Ignore case
        d["-k"] = ""        # Show this keyword
        d["-l"] = False     # List the keywords
        d["-o"] = False     # OR the regexes on the command line
        d["-v"] = False     # Print color coding & numbering key
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "ab:Ccdehik:lov")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in optlist:
            if o[1] in "aCcdehilov":
                d[o] = not d[o]
            elif o in ("-b",):
                d["-b"] = int(a)
            elif o in ("-h",):
                Usage()
            elif o in ("-k",):
                d["-k"] = a
        SetColors(False) if d["-C"] else SetColors()
        return args
if 1:   # Core functionality
    def GetData():
        'Return a list of Entry items'
        items = []
        # This regex should find lines beginning with two integers, each with a colon after
        # them, then a string.
        r = re.compile(r"^(\s*\d+\s*:\s*\d+\s*:)")
        for i, line in enumerate(data.split("\n")):
            line = line.strip()
            mo = r.search(line)
            if mo:
                try:
                    location, remainder = line.split(" ", 1)
                except ValueError:
                    # Empty line after matched location stuff
                    e = Entry(i + 1, location, "", "")
                else:
                    # location is of the form 'n:m:s' where n and m are integers and s is a
                    # string.  remainder is the description followed by a non-breaking space,
                    # followed by optional keyword(s).
                    nbs = "\xa0"    # Non-breaking space character
                    if nbs in remainder:
                        description, keywords = remainder.split(nbs)
                    else:
                        description = remainder.strip()
                        keywords = ""
                    e = Entry(i + 1, location, description, keywords)
                items.append(e)
        items = list(sorted(items))
        if not items:
            print(f"{t.ornl}items is empty")
            exit()
        return items
    def TextSearch(args, items):
        '''found will hold the Entry items that matched; pos holds the start and
        end position of the first match and is keyed by the line.
        
        args        List of regexes to search for
        items       List of Entry instances; when printed, an Entry will result in a string like
                    "1:1 Component pins".
        '''
        if 1:  # regexps is a list of the regular expressions made from args
            regexps = []
            remove = []     # Hold those that begin with "-"
            for i in args:
                i = i.strip()
                if not i:
                    continue
                if i.startswith("-"):
                    remove.append(i[1:])
                else:
                    regexps.append(re.compile(i, re.I) if d["-i"] else re.compile(i))
        if 1:  # Search all the items (Entry instances) for regex matches in their descr attribute
            found = []  # List containing the Entry instances that had a regex match
            if d["-o"]:  # OR the regexes
                for i in items:
                    s = i.description
                    for r in regexps:
                        mo = r.search(s)
                        if mo:
                            i.start, i.end = mo.start(), mo.end()
                            found.append(i)
                            break
            else:  # AND the regexes
                for i in items:
                    s = i.description
                    matched_all = True          # Assume we'll match all
                    # Since this is reversed, the only regex that will be color-coded is the first
                    for r in reversed(regexps):
                        mo = r.search(s)
                        if mo:
                            i.start, i.end = mo.start(), mo.end()
                        else:
                            matched_all = False
                    if matched_all:
                        found.append(i)
        if 1 and remove:  # Remove any specified regexes
            keep = []
            # Compile the regexes
            remove = [re.compile(regex, re.I) if d["-i"] else re.compile(regex) for regex in remove]
            for item in found:
                not_found = True
                for r in remove:
                    if r.search(item.description):
                        # Had a match, so ignore this item
                        not_found = False
                        break
                if not_found:
                    keep.append(item)
            found = keep
        if 1:  # Print results
            # We can't just print the string of the Entry because we want to highlight the search
            # match in the description
            for item in sorted(found):
                # Box and compartment
                print(f"{t.box}{item.box:>2d}:"
                      f"{t.compartment}{item.compartment:>2d}:"
                      f"{t.quantity}{item.quantity:s}{t.n}", end="")
                # Description
                if 1:
                    print("", end=" "*2)    # Spacing between box:compartment and description
                    s = item.description
                    print(s[:item.start], end="")
                    # Colorized match
                    print(f"{t.match}{s[item.start:item.end]}{t.n}", end="")
                    # Remainder
                    print(s[item.end:], end="")
                # Keywords
                k = '/'.join(item.keywords)
                print(f" {t.keyword}[{k}]{t.n}") if k else print()
            if found:
                PrintColorCoding()
    def PrintColorCoding(qty=True):
        if not d["-v"]:
            return
        if not d["-C"]:
            t.print(f"Color coding:  {t.box}box "
                    f"{t.compartment}compartment "
                    f"{t.quantity}quantity "
                    f"{t.keyword}keyword")
        # Quantity coding
        if qty:
            print(dedent('''
                Letters for quantity:
                    ?   Not inventoried yet
                    f   A few
                    m   Too many to count
            '''))
    def Keywords(items):
        'Returns a set of the keywords'
        kw = []
        for item in items:
            kw.extend(item.keywords)
        return set(kw)
    def Inspection():
        '''Look for problems in the data:
            - No keyword
            - Misspelled
        '''
        #for item in items:
        #    if 

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if not d["-C"]:
        t.cat = t.hl = t.N = ""
    items = GetData()
    if d["-a"]:  # Show all items
        for item in items:
            if item.description:
                print(item)
        PrintColorCoding()
    elif d["-b"] is not None:  # Show items in box number -b
        n = int(d["-b"])
        for item in items:
            if item.box == n:
                print(item)
        PrintColorCoding()
    elif d["-d"]:
            Inspection()
    elif d["-e"]:  # Show empty compartments
        for item in items:
            if not item.description:
                print(item)
        PrintColorCoding(False)
    elif d["-l"]:  # Show allowed keywords
        print("Keywords:")
        # Put each keyword into a dict with its count
        KW = defaultdict(int)
        for item in items:
            for kw in item.keywords:
                KW[kw] += 1
        # Get maximum count
        max_count = max(KW.values())
        w = len(str(max_count))     # Needed printing width
        # Print sorted alphabetically
        o, o1, max_count = [], [], 0
        print("Keywords sorted alphabetically (number is count):")
        for name in sorted(KW, key=str.lower):
            count = KW[name]
            o.append(f"{count:{w}d} {name}")
            o1.append((count, name))
        for item in Columnize(o):
            print(item)
        # Print sorted numerically
        print("\nKeywords sorted by count:")
        o = []
        for count, name in sorted(o1):
            o.append(f"{count:{w}d} {name}")
        for item in Columnize(o):
            print(item)
    elif d["-k"]:  # Show all the items with the given keyword
        kw = d["-k"].lower()
        for item in items:
            ikw = [j.lower() for j in item.keywords]
            if kw in ikw:
                print(item)
        PrintColorCoding()
    elif not args:
        Usage()
    else:
        TextSearch(args, items)

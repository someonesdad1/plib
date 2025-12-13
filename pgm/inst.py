_pgminfo = '''
<oo desc
    Show electrical instrument data
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - Build list of instrument data

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Instrument data
    g.categories = set('''
        DCPS
        ACPS
        DMM
        Scope
        Generator
        DigitalMeter
        AnalogMeter
        Standard
        Resistance
        Attenuator
        PCB_assy
        Transformer
        LCR
        DCLoad
        ComponentTest
        Soldering 
    '''.split())
    data = '''
        # Model_num ; Manufacturer ; SN ; Received ; Price ; Category ; Description
        6115A ; HP ; ; Jul 2006 ; 72 ; DCPS ; 100 V 0.4 A power supply
        3466A ; HP ; 1716A-10634 ; 16 Jan 2021 ; 60 ; DMM ; 4.5 digit DMM with AC+DC
        4221 ; L&N ; 1587111 ; 12 Jan 2021 ; 145 ; Standard ; 0.1 Ω resistance standard (manufactured 1961)
        927F ; Eiden ; HK69227 ; 19 May 2010 ; 19 ; Attenuator ; 2 GHz 70 dB attenuator
        6181C ; HP ; 2423A-01997 ; 16 Feb 2021 ; 157 ; DCPS ; Current source
        NMN ; EDFM ; NSN ; 23 Sep 2021 ; 200 ; Resistance ; RC box
        427A ; HP ; 0947A22983 ; 27 Sep 2021 ; 158 ; AnalogMeter ; AC/DC Voltmeter/ohmmeter
        E3615A ; HP ; KR72705221 ; 27 Sep 2021 ; 95 ; DCPS ; 20 V 3 A power supply #2
        VP-7201A ; Panasonic ; ; 7 Oct 2021 ; 132 ; Generator ; RC oscillator
        NMN ; Stancor ; NSN ; 19 Oct 2021 ; 15 ; Transformer ; Stancor 1 kVA 115-230 V autotransformer
        TO92 ; M&G ; NSN ; 19 Oct 2021 ; 13 ; Transformer ; Transformer
        TO120 ; M&G ; NSN ; 19 Oct 2021 ; 13 ; Transformer ; Transformer (qty 2)
        62012G ; HP ; ; 22 Oct 2021 ; 36 ; DCPS ; 12 V 12 A power supply
        NMN ; Triad ; NSN ; 22 Oct 2021 ; 15 ; Transformer ; Triad 1 kVA 115-230 V autotransformer
        W5 ; GR ; NSN ; 29 Oct 2021 ; 53 ; Transformer ; 6 A Variac (qty 3)
        870 ; Aneng ; NSN ; 10 Aug 2023 ; 35 ; DMM ; 20000 count DMM
        E3614A ; HP ; KR31500964 ; 24 Sep 2024 ; 60 ; DCPS ; 8 V 6A power supply 
        AOS03 ; Aneng ; ; 29 Oct 2024 ; 80 ; DMM ; 20000 count DMM & scope
        400EL ; HP ; 1208A26958 ; 1 Nov 2024 ; 55 ; AnalogMeter ; 10 MHz AC voltmeter
        6236B ; HP ; ; 2 Dec 2025 ; 35 ; DCPS ; 5 V 2.5 A ±20 V 0.5 A triple power supply
        FY6900-60M ; FeelElec ; ; 11 Dec 2025 ; 135 ; Generator ; 60 MHz dual channel function generator
        3435A ; HP ; ; 1978 ; 350 ; DMM; 3.5 digit multimeter (died in 2022)
        3400A ; HP ; ; 1987 ; 65 ; AnalogMeter; 10 MHz RMS voltmeter
        4001 ; Continental Specialties ; ; 1985 ; 200 ; Generator ; Pulse generator
        886 ; B&K ; ; 2008 ; 350 ; LCR ; LCR meter
        9130 ; B&K ; ; 2008 ; 680 ; DCPS ; Triple power supply
        8500 ; B&K ; ; 2012 ; 0 ; DCLoad ; 300 W DC load
        6033A ; HP ; ; 2015 ; 0 ; DCPS ; 20 V 30 A power supply (gift from Todd)
        CT2593-2 ; Cal Test ; ; 2015 ; 250 ; Scope ; 700 V 25 MHz differential scope probe
        E3615A ; HP ; KR83506480 ; 2002 ; 100 ; DCPS ; 20 V 3 A power supply #1
        54601B ; HP ; ; 2006 ; 600 ; Scope ; 100 MHz 4 channel scope
        AS23723 ; GE ; ; 2007 ; 100 ; Transformer ; 1 kW medical isolation transformer
        6038A ; HP ; ; 2007 ; 150 ; DCPS ; 60 V 10 A power supply
        TC1 ; NIU ; ; 2018 ; 30 ; ComponentTest ; Multifunction component tester
        1432-N ; GR ; ; 2000 ; 75 ; Resistance; 5 decade resistance box 10 kΩ
        DHO804 ; Rigol ; ; Dec 2024 ; 373 ; Scope ; 70 MHz 4 channel scope
        STATION-75 ; Circuit Specialists ; ; 2024 ; 53 ; Soldering ; 75 W soldering iron
    '''
if 1:   # Classes
    class Instrument:
        numfields = 7
        def __init__(self, line):
            self.line = line
            f = [i.strip() for i in line.strip().split(";")]
            if len(f) != Instrument.numfields:
                raise ValueError(f"{line!r} doesn't have {Instrument.numfields} fields")
            self.model, self.mfg, self.sn, self.received, self.cost, self.category, self.description = f 
            self.cost = flt(self.cost)
            assert self.cost >= 0
            assert self.category in g.categories
        def __str__(self):
            s = (f"{t.ornl}{self.model}{t.n} {self.mfg} {t.yel}${self.cost}{t.n} " +
                 f"{t.grn}{self.received}{t.n} {t.sky}{self.description}{t.n}")
            return s
        def __lt__(self, other):
            return self.model < other.model
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [regex1 [regex2...]]
          Search my instruments for a regex; more than one are ANDed together.
        Options:
            -d      Dump the raw data
            -i      Don't ignore case
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Dump the raw data
        d["-i"] = True      # Ignore case
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dhi") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("di"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        if d["-d"]:
            DumpData()
            exit(0)
        GetColors()
        return args

if __name__ == "__main__":
    d = {}      # Options dictionary
    instruments = []
    for line in data.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        i = Instrument(line)
        instruments.append(i)
    if 0:   # Show the Instrument instances
        for i in instruments:
            print(i)
        exit()
    args = ParseCommandLine(d)
    # Get candidates from first regex
    found = []
    regex = args.pop(0)
    r = re.compile(regex, re.I if d["-i"] else 0)
    for i in instruments:
        if r.search(i.line):
            found.append(i)
    if not found:
        exit()
    # Don't keep unless remaining regexes match
    regexes = [re.compile(i, re.I if d["-i"] else 0) for i in args]
    keep = []
    for instrument in sorted(found):
        matched = True
        for r in regexes:
            if not r.search(instrument.line):
                matched = False
                break
        if matched:
            keep.append(instrument)
    for instrument in keep:
        print(instrument)
                
            

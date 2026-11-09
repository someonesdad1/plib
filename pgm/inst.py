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

    - Add an option that dumps detailed information for each instrument that I often
      look up.  This can be free-form text stored in each Instrument instance.  For
      example, when I use the L&N 0.1 Ω standard, I need to know the maximum DC and AC
      currents allowed through it (3 A RMS to maintain a 10 ppm calibration).

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
        import termtables as tt
        import trm
        t = trm.TrmDP()
        from lwtest import Assert
        from dputil import PP
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
        Prototyping
    '''.split())
    data = '''
        # inst_num ; model_num ; manufacturer ; SN ; Received ; Cost ; Category ; Description
        # The inst_num must be an integer > 0 and sequential.  If a particular
        # instrument is retired, disposed of, etc., then put a '*' after the inst_num.
        # Aneng stuff
            1 ; 870 ; Aneng ; None ; 10Aug2023 ; 35 ; DMM ; 20000 count DMM
            2 ; 8009 ; Aneng ; ; .....2019 ; 20 ; DMM ; 9999 count DMM 
            3 ; AOS03 ; Aneng ; ; 29Oct2024 ; 80 ; DMM ; 20000 count DMM & scope

        # HP stuff
            4 ; E3615A ; HP ; KR72705221 ; 27Sep2021 ; 95 ; DCPS ; 20 V @ 3 A power supply #2
            5 ; E3615A ; HP ; KR83506480 ; .....2002 ; 100 ; DCPS ; 20 V @ 3 A power supply #1
            6 ; E3614A ; HP ; KR31500964 ; 24Sep2024 ; 60 ; DCPS ; 8 V @ 6A power supply 
            7 ; 6115A ; HP ; ; ..Jul2006 ; 72 ; DCPS ; 100 V @ 0.4 A power supply
            8 ; 6236B ; HP ; ; .2Dec2025 ; 35 ; DCPS ; Triple power supply
            9 ; 62012G ; HP ; ; 22Oct2021 ; 36 ; DCPS ; 12 V @ 12 A power supply
            10 ; 6033A ; HP ; ; .....2015 ; 0 ; DCPS ; 20 V @ 30 A power supply
            11 ; 6038A ; HP ; ; .....2007 ; 150 ; DCPS ; 60 V @ 10 A power supply
            12* ; 6181C ; HP ; 2423A-01997 ; 16Feb2021 ; 157 ; DCPS ; Current source
            13 ; 3466A ; HP ; 1716A-10634 ; 16Jan2021 ; 60 ; DMM ; 4.5 digit DMM with AC+DC
            14 ; 427A ; HP ; 0947A22983 ; 27Sep2021 ; 158 ; AnalogMeter ; Voltmeter
            15 ; 3435A ; HP ; ; .....1978 ; 350 ; DMM; 3.5 digit multimeter
            16 ; 3400A ; HP ; ; .....1987 ; 65 ; AnalogMeter; 10 MHz RMS voltmeter
            17 ; 400EL ; HP ; 1208A26958 ; .1Nov2024 ; 55 ; AnalogMeter ; 10 MHz AC voltmeter
            18 ; 54601B ; HP ; ; .....2006 ; 600 ; Scope ; 100 MHz 4 channel scope

        # GR stuff
            19 ; W5 ; GR ; None ; 29Oct2021 ; 53 ; Transformer ; 6 A Variac (qty 3)
            20 ; W5 ; GR ; None ; 29Oct2021 ; 53 ; Transformer ; 6 A Variac (qty 3)
            21 ; W5 ; GR ; None ; 29Oct2021 ; 53 ; Transformer ; 6 A Variac (qty 3)
            22 ; 1432-N ; GR ; ; .....2000 ; 75 ; Resistance; 5 decade resistance box 10 kΩ
            23 ; W10 ; GR ; ; .....1969 ; 0 ; Transformer ; 10 A Variac

        # B&K stuff
            24 ; 886 ; B&K ; ; .....2008 ; 350 ; LCR ; LCR meter
            25 ; 8500 ; B&K ; ; .....2012 ; 0 ; DCLoad ; 300 W DC load
            26 ; 9130 ; B&K ; ; .....2008 ; 600 ; DCPS ; Triple DC power supply

        # Other
            27 ; DHO804 ; Rigol ; ; ..Dec2024 ; 373 ; Scope ; 70 MHz 4 channel scope
            28 ; FY6900-60M ; FeelElec ; ; 11Dec2025 ; 135 ; Generator ; 60 MHz 2-ch fn generator
            29 ; STATION-75 ; CSI ; ; .....2024 ; 53 ; Soldering ; 75 W soldering iron
            30 ; 4001 ; ContSpec ; ; .....1985 ; 200 ; Generator ; Pulse generator
            31 ; CT2593-2 ; Cal Test ; ; .....2015 ; 250 ; Scope ; 700 V 25 MHz diff. scope probe
            32 ; 4221 ; L&N ; 1587111 ; 12Jan2021 ; 145 ; Standard ; 0.1 Ω standard
            33 ; 927F ; Eiden ; HK69227 ; 19May2010 ; 19 ; Attenuator ; 2 GHz 70 dB attenuator
            34 ; None ; EDFM ; None ; 23Sep2021 ; 200 ; Resistance ; RC box
            35 ; VP-7201A ; Panasonic ; ; 7Oct2021 ; 132 ; Generator ; RC oscillator
            36 ; TC1 ; NIU ; ; .....2018 ; 30 ; ComponentTest ; Multifunction component tester
            37 ; 260-7 ; Simpson ; ; .....2024 ; 0 ; AnalogMeter; VOM

        # Transformers
            38 ; None ; Stancor ; None ; 19Oct2021 ; 15 ; Transformer ; 1 kVA 115-230 V autotransformer
            39 ; TO92 ; M&G ; None ; 19Oct2021 ; 13 ; Transformer ; Transformer
            40 ; TO120 ; M&G ; None ; 19Oct2021 ; 13 ; Transformer ; Transformer (qty 2)
            41 ; None ; Triad ; None ; 22Oct2021 ; 15 ; Transformer ; 1 kVA 115-230 V autotransformer
            42 ; AS23723 ; GE ; ; .....2007 ; 100 ; Transformer ; 1 kW medical isol. transformer

        # Other
            43 ; ProtoBoard ; ContSpec ; ; .....1986 ; 25 ; Prototyping ; Small prototyping board 

    '''
if 1:   # Classes
    class Instrument:
        numfields = 8
        widths = {
            "inst_num": 2,
            "model": 12,
            "mfg": 10,
            "cost": 4,
            "received": 10,
        }
        def __init__(self, line):
            self.line = line
            f = [i.strip() for i in line.strip().split(";")]
            if len(f) != Instrument.numfields:
                raise ValueError(f"{line!r} doesn't have {Instrument.numfields} fields")
            try:
                self.inst_num = int(f[0])
                self.missing = False
            except ValueError:
                assert f[0].endswith("*")
                self.inst_num = int(f[0][:-1])
                self.missing = True
            self.model = f[1]
            self.mfg = f[2]
            self.sn = f[3]
            self.received = f[4].replace(" ", "")
            self.cost = f[5]
            self.category = f[6]
            self.description = f[7]
            self.cost = flt(self.cost)
            assert self.cost >= 0
            assert self.category in g.categories, f"{self.category} missing"
        def __str__(self):
            u = self.received.replace(".", " ")
            s = (f"{t.red}{self.inst_num:{Instrument.widths['inst_num']}d}"
                 f" {t.orn}{self.model:{Instrument.widths['model']}s}{t.n}"
                 f" {self.mfg:{Instrument.widths['model']}s}"
                 f" {t.yel}${str(self.cost):{Instrument.widths['cost']}s}{t.n}"
                 f" {t.grn}{u:{Instrument.widths['received']}s}{t.n}"
                 f" {t.sky}{self.description}{t.n}")
            return s
        def __lt__(self, other):
            return self.model < other.model
        def items(self):
            return (
                self.model,
                self.mfg,
                self.sn,
                self.received,
                self.cost,
                self.category,
                self.description
            )
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
          Search my instruments for a regex; more than one are ANDed together.  If it's
          an integer, then search for that instrument number.
        Options:
            -d      Dump the raw data
            -i      Don't ignore case
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Dump the raw data
        d["-i"] = True      # Ignore case
        #if len(sys.argv) < 2:
        #    Usage()
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
        GetColors()
        if d["-d"] or not args:
            PrintInstrumentData()
            exit(0)
        return args
if 1:   # Core functionality
    def GetInstrumentData(instruments):
        for line in data.split("\n"):
            line = line.strip()
            if not line or line[0] == "#":
                continue
            i = Instrument(line)
            instruments.append(i)
        # Verify there are no missing instrument numbers
        numbers = []
        for i in instruments:
            numbers.append(i.inst_num)
        nums = set(numbers)
        missing = []
        for i in range(1, max(numbers)):
            if i not in nums:
                missing.append(i)
        missing = [str(i) for i in missing]
        if missing:
            print(f"Missing inst_num:  {' '.join(missing)}")
            exit(1)
        if len(nums) != len(numbers):
            dups = []
            for i in numbers:
                if numbers.count(i) > 1:
                    dups.append(i)
            dups = [str(i) for i in sorted(set(dups))]
            if dups:
                print(f"Error:  duplicate numbers: {' '.join(dups)}")
                exit(1)
    def HandleIntegers(args):
        found = False
        integers = []
        for arg in args:
            try:
                n = int(arg)
                integers.append(n)
            except ValueError:
                if found:
                    continue
                else:
                    return
        integers = list(sorted(set(integers)))
        if integers:
            for i in instruments:
                if i.inst_num in integers:
                    t.print(f"{t.grnl}{i.inst_num:4d}{t.n} {i.mfg} {i.model} {i.description}")
            exit(0)
    def PrintInstrumentData():
        o = [[
            "N",
            "Model",
            "Mfg",
            "SN",
            "Date",
            "Cost", 
            "Category",
            "Description"
        ]]
        for i in instruments:
            u = i.received.replace(".", " ")
            o.append([
                str(i.inst_num),
                i.model,
                i.mfg,
                i.sn,
                u,
                str(i.cost),
                i.category,
                i.description,
            ])
        tt.print(o, padding=(0, 0), style=" "*15, alignment="l"*8)
    def PerformSearch(args):
        # Get candidates from first regex
        found = []
        HandleIntegers(args)
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

if __name__ == "__main__":
    d = {}      # Options dictionary
    instruments = []
    GetInstrumentData(instruments)
    args = ParseCommandLine(d)
    PerformSearch(args)

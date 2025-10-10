'''

Description here

'''
_pgminfo = '''
<oo 
    desc
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import csv
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from columnize import Columnize
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
        __all__ = "attributes elements symbols Element".split()
if 1:   # Classes
    class Element:
        attributes = None   # Will hold the attributes' names and definitions dict
        def __init__(self, data):
            'data is a dictionary of the needed attribute names and their values'
            def Int(x):
                try:
                    return int(x)
                except Exception:
                    return x.strip()
            def Flt(x):
                try:
                    return flt(x)
                except Exception:
                    return x.strip()
            for name in data:
                exec(f"self.{name} = data[{name!r}]")
            # Convert to integer
            self.num = Int(self.num)
            self.row = Int(self.row)
            self.col = Int(self.col)
            # Convert to flt
            self.atwt = Flt(self.atwt)
            self.den = Flt(self.den)
            self.ldenmp = Flt(self.ldenmp)
            self.ldenbp = Flt(self.ldenbp)
            self.mp = Flt(self.mp)
            self.Tcrit = Flt(self.Tcrit)
            self.Pcrit = Flt(self.Pcrit)
            self.fus = Flt(self.fus)
            self.vap = Flt(self.vap)
            self.spheat = Flt(self.spheat)
            self.vp1Pa = Flt(self.vp1Pa)
            self.vp10Pa = Flt(self.vp10Pa)
            self.vp100Pa = Flt(self.vp100Pa)
            self.vp1kPa = Flt(self.vp1kPa)
            self.vp10kPa = Flt(self.vp10kPa)
            self.vp100kPa = Flt(self.vp100kPa)
            self.en = Flt(self.en)
            self.ion1 = Flt(self.ion1)
            self.ion2 = Flt(self.ion2)
            self.ion3 = Flt(self.ion3)
            self.atrad = Flt(self.atrad)
            self.covrad = Flt(self.covrad)
            self.vdwrad = Flt(self.vdwrad)
            self.res = Flt(self.res)
            self.thcond = Flt(self.thcond)
            self.thexp = Flt(self.thexp)
            self.spsnd = Flt(self.spsnd)
            self.neucap = Flt(self.neucap)
            self.young = Flt(self.young)
            self.shear = Flt(self.shear)
            self.bulk = Flt(self.bulk)
            self.poisson = Flt(self.poisson)
            self.mohs = Flt(self.mohs)
            self.brinell = Flt(self.brinell)
            self.abun = Flt(self.abun)
        def __str__(self):
            'Return all the data in columns'
            o, di = [], self.__dict__
            for i in di:
                n, u = Element.attributes[i]
                if i == "mp" or i == "fus":
                    c = t.denl
                elif i == "bp" or i == "vap":
                    c = t.lipl
                elif i == "num":
                    c = t.whtl
                elif i == "atwt":
                    c = t.cynl
                elif i == "den":
                    c = t.lip
                elif i == "spheat":
                    c = t.magl
                elif i == "ion1":
                    c = t.purl
                elif i == "res":
                    c = t.grn
                elif i == "thexp":
                    c = t.yel
                elif i == "thcond":
                    c = t.sky
                elif i == "abun":
                    c = t.brnl
                else:
                    c = ""
                if ii(di[i], str) and di[i] == "--":
                    o.append(f"{t.none}{i} = {t.n}")
                else:
                    o.append(f"{c}{i} = {di[i]} {u}{t.n}" if u else f"{c}{i} = {di[i]}{t.n}")
            return '\n'.join(Columnize(o, indent=" "*2))
        def __repr__(self):
            return f"Element({self.name})"
if 1:   # Utility
    def GetColors():
        t.name = t.ornl
        t.none = t.gry
        t.mp = t.denl
        t.bp = t.lipl
        t.atwt = t.grnl
        t.den = t.purl
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
        Usage:  {sys.argv[0]} [options] regex1 [regex2...]
          Print information on the elements found by the regexes.
        Examples:
          'Co' shows the properties of cobalt.
          'u' shows the elements with 'u' in the name
        Options:
            -a      Describe the attributes
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ah") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Data
    def GetAttributes():
        '''Return a dictionary of attribute names.  The keys are the short-hand
        attribute names like atwt for "atomic weight".  The values are (name, unit) with
        the unit being "" for a dimensionless number.
        '''
        data = '''abun   Abundance in Earth's crust (mass fraction); ppm
            atrad   Atomic radius; pm
            atwt    Atomic weight; g/mol
            bp      Boiling point; K
            brinell Brinell hardness; GPa
            bulk    Bulk modulus; GPa
            cas     CAS (Chemical Abstracts Service) registry number
            col     1-based column number on page (can be float) for periodic table
            covrad  Covalent radius; pm
            cryst   Crystal structure
            den     Density near 20 deg C (gases at 0 deg C, 101325 Pa); g/cm³
            diat    Diatomic: thermophysical properties are for the diatomic molecules
            econ    Electronic configuration
            elcat   Element category
            en      Electronegativity (Pauling scale)
            fus     Heat of fusion; kJ/mol
            grpebl  Group, period, block
            ion1    First ionization energy; kJ/mol
            ion2    Second ionization energy; kJ/mol
            ion3    Third ionization energy; kJ/mol
            ldenbp  Liquid density at boiling point; g/cm³
            ldenmp  Liquid density at melting point; g/cm³
            magord  Magnetic ordering
            mohs    Mohs hardness
            mp      Melting point; K
            name    Element's name
            neucap  Thermal neutron capture cross section; barn
            num     Atomic number
            Pcrit   Critical pressure for gas phase; MPa
            phase   Normal phase at room temperature: s, l, g, a = artificial
            poisson Poisson's ratio
            res     Electrical resistivity; nΩ·m
            row     1-based row number on page (can be float) for periodic table
            shear   Shear modulus; GPa
            spheat  Specific heat; J//mol·K
            spsnd   Speed of sound in thin rod; m/s
            sym     Element's symbol
            Tcrit   Critical temperature for gas phase; K
            thcond  Thermal conductivity; W//m·K
            thexp   Thermal expansion; 1/MK
            vap     Heat of vaporization; kJ/mol
            vdwrad  Van der Waals radius; pm
            vp100kPa Temperature at which vapor pressure is 100 KPa; K
            vp100Pa Temperature at which vapor pressure is 100 Pa; K
            vp10kPa Temperature at which vapor pressure is 10 KPa; K
            vp10Pa  Temperature at which vapor pressure is 10 Pa; K
            vp1kPa  Temperature at which vapor pressure is 1 KPa; K
            vp1Pa   Temperature at which vapor pressure is 1 Pa; K
            young   Young's modulus; GPa'''.split("\n")
        attributes = {}
        for line in data:
            line = line.strip()
            name, value = [i.strip() for i in line.split(" ", maxsplit=1)]
            unit = ""
            if ";" in value:
                descr, unit = [i.strip() for i in value.split(";")]
                value = descr
            attributes[name] = (value, unit)
        Element.attributes = attributes
        return attributes
    def GetElements():
        'Return a dict of the Element instances keyed by atomic number'
        data = dedent('''
            num,sym,name,diat,row,col,elcat,grpebl,atwt,econ,phase,den,ldenmp,ldenbp,mp,bp,Tcrit,Pcrit,fus,vap,spheat,vp1Pa,vp10Pa,vp100Pa,vp1kPa,vp10kPa,vp100kPa,en,ion1,ion2,ion3,atrad,covrad,vdwrad,cryst,magord,res,thcond,thexp,spsnd,neucap,young,shear,bulk,poisson,mohs,brinell,cas,abun
            1,H,Hydrogen,x,1,2,nonmetal,"1,1,s",1.0079,1s1,g,8.988e-5,0.07,0.07099,14.01,20.28,32.97,1.293,0.117,0.904,28.836,--,--,--,--,15,20,2.20 ,1312.0,--,--,--,31,120 ,hexagonal,diamagnetic,--,0.1805,--,1310,0.332,--,--,--,--,--,--,1333-74-0,1400
            2,He,Helium,0,1,18,noble gas,"18,1,s",4.00260,1s2,g,1.786e-4,0.145,--,0.95,4.22,5.19,0.227,0.0138,0.08,20.786,--,--,1.23,1.67,2.48,4.21,--,2372.3,5250.5,--,--,28,140 ,hcp,diamagnetic,--,0.1513,--,972,0.332,--,--,--,--,--,--,7440-59-7,0.0080
            3,Li,Lithium,0,2,1,alkali metal,"1,2,s",6.941,[He]2s1,s,0.534,0.512,--,453.69,1615,3223,67,3.00,147.1,24.860,797,885,995,1144,1337,1610,0.98 ,520.2,7298.1,11815.0,152,128,182 ,bcc,paramagnetic,92.8  ,84.8,46,6000,71,4.9,4.2,11,--,0.6,--,7439-93-2,20
            4,Be,Beryllium,0,2,2,alkaline earth metal,"2,2,s",9.01218,[He]2s2,s,1.85,1.690,--,1560,2742,--,--,7.895,297,16.443,1462,1608,1791,2023,2327,2742,1.57 ,899.5,1757.1,14848.7 ,112,96,153 ,hexagonal,diamagnetic,35.6  ,200,11.3,12870,0.0092,287,132,130,--,5.5,0.6,7440-41-7,2.8
            5,B,Boron,0,2,13,metalloid,"13,2,p",10.81,[He]2s2:2p1,s,2.34,2.08,--,2349,4200,--,--,50.2,480,11.087,2348,2562,2822,3141,3545,4072,2.04 ,800.6,2427.1,3659.7 ,90,84,192 ,--,diamagnetic,1e6,27.4,6,16200,3837,--,--,185,--,9.5,--,7440-42-8,10
            6,C,Carbon,0,2,14,nonmetal,"14,2,p",12.010,[He]2s2:2p2,s,2.267,--,--,3800,4300,--,--,117,715,8.517,--,2839,3048,3289,3572,3908,2.55 ,1086.5,2352.6,4620.5 ,91.4,73,170 ,--,diamagnetic,13750,142,0.8,18350,0.0034,1050,478,442,--,10,--,7440-44-0,200
            7,N,Nitrogen,x,2,15,nonmetal,"15,2,p",14.006,[He]2s2:2p3,g,1.251e-3,--,0.808,63.15,77.36,126.21,3.3978,0.72,5.57,29.124,37,41,46,53,62,77,3.04 ,1402.3,2856,4578.1 ,92,71,155 ,hexagonal,diamagnetic,--,2.583e-2,--,353,0.075,--,--,--,--,--,--,7727-37-9,19
            8,O,Oxygen,x,2,16,nonmetal,"16,2,p",15.999,[He]2s2:2p4,g,1.429e-3,--,1.141,54.36,90.20,154.59,5.043,0.444,6.82,29.378,--,--,--,61,73,90,3.44 ,1313.9,3388.3,5300.5 ,--,66,152 ,cubic,paramagnetic,--,2.658e-2,--,330,0.0002,--,--,--,--,--,--,7782-44-7,460e3
            9,F,Fluorine,x,2,17,halogen,"17,2,p",18.9984,[He]2s2:2p5,g,1.7e-3,--,1.505,53.53,85.03,144.13,5.220,0.51,6.62,31.3,38,44,50,58,69,85,3.98 ,1681.0,3374.2,6050.4 ,--,60,147 ,cubic,diamagnetic,--,2.77e-2,--,--,--,--,--,--,--,--,--,7782-41-4,590
            10,Ne,Neon,0,2,18,noble gas,"18,2,p",20.179,[He]2s2:2p6,g,9.002e-4,--,1.207,24.56,27.07,44.4,2.76,0.335,1.71,20.786,12,13,15,18,21,27,--,2080.7,3952.3,6122 ,--,58,154 ,fcc,diamagnetic,--,4.91e-2,--,435,0.038,--,--,654,--,--,--,7440-01-9,0.0050
            11,Na,Sodium,0,3,1,alkali metal,"1,3,s",22.9898,[Ne]3s1,s,0.968,0.927,--,370.87,1156,2573,35,2.60,97.42,28.230,554,617,697,802,946,1153,0.93 ,495.8,4562,6910.3 ,186,166,227 ,bcc,paramagnetic,47.7  ,142,71,3200,0.534,10,3.3,6.3,--,0.5,0,7440-23-5,24e3
            12,Mg,Magnesium,0,3,2,alkaline earth metal,"2,3,s",24.305,[Ne]3s2,s,1.738,1.584,--,923,1363,--,--,8.48,128,24.869,701,773,861,971,1132,1361,1.31 ,737.7,1450.7,7732.7 ,160,141,173 ,hexagonal,paramagnetic,43.9  ,156,24.8,4940,0.064,45,17,45,0.290,2.5,0.26,7439-95-4,23e3
            13,Al,Aluminum,0,3,13,other metal,"13,3,p",26.9815,[Ne]3s2:3p1,s,2.70,2.375,--,933.47,2792,--,--,10.71,294,24.200,1482,1632,1817,2054,2364,2790,1.61 ,577.5,1816.7,2744.8 ,143,121,184 ,fcc,paramagnetic,26.50  ,237,23.1,5000,0.232,70,28,76,0.35,2.75,0.25,7429-90-5,82e3
            14,Si,Silicon,0,3,14,metalloid,"14,3,p",28.085,[Ne]3s2:3p2,s,2.33,2.57,--,1687,3538,--,--,50.21,359,19.789,1908,2102,2339,2636,3021,3537,1.90 ,786.5,1577.1,3231.6 ,111,111,210 ,diamond cubic,diamagnetic,1e12,149,2.6,8433,0.160,185,52,100,0.28,7,--,7440-21-3,280e3
            15,P,Phosphorus,0,3,15,nonmetal,"15,3,p",30.9738,[Ne]3s2:3p3,s,1.823,--,--,317.30,550,994,--,0.66,12.4,23.824,279,307,342,388,453,549,2.19 ,1011.8,1907,2914.1 ,--,107,180 ,--,diamagnetic,1e18,0.236,--,--,0.19,--,--,5,--,--,--,7723-14-0,1100
            16,S,Sulfur,0,3,16,nonmetal,"16,3,p",32.06,[Ne]3s2:3p4,s,2.08,1.819,--,388.36,717.8,1314,20.7,1.727,45,22.75,375,408,449,508,591,717,2.58 ,999.6,2252,3357 ,--,105,180 ,orthorhombic,diamagnetic,2e24,0.205,--,--,0.51,--,--,7.7,--,2.0,--,7704-34-9,350
            17,Cl,Chlorine,x,3,17,halogen,"17,3,p",35.45,[Ne]3s2:3p5,g,3.2e-3,1.5649,1.5625,171.6,239.11,416.9,7.991,6.406,20.41,33.949,128,139,153,170,197,239,3.16 ,1251.2,2298,3822 ,--,102,175 ,orthorhombic,diamagnetic,>1e10,8.9e-3,--,206,44,--,--,--,--,--,--,7782-50-5,150
            18,Ar,Argon,0,3,18,noble gas,"18,3,p",39.945,[Ne]3s2:3p6,g,1.784e-3,--,1.40,83.80,87.30,150.87,4.898,1.18,6.43,20.786,--,47,53,61,71,87,--,1520.6,2665.8,3931 ,--,106,188 ,fcc,diamagnetic,--,1.772e-2,--,323,0.65,--,--,--,--,--,--,7440–37–1,3.5
            19,K,Potassium,0,4,1,alkali metal,"1,4,s",39.098,[Ar]4s1,s,0.89,0.828,--,336.53,1032,2223,16,2.33,76.9,29.6,473,530,601,697,832,1029,0.82 ,418.8,3052,4420 ,227,203,275 ,bcc,paramagnetic,72.0  ,102.5,83.3,2000,2.2,3.53,1.3,3.1,--,0.4,0,7440-09-7,21e3
            20,Ca,Calcium,0,4,2,alkaline earth metal,"2,4,s",40.08,[Ar]4s2,s,1.55,1.378,--,1115,1757,--,--,8.54,154.7,25.929,864,956,1071,1227,1443,1755,1.00 ,589.9,1145.4,4912.4 ,197,176,231 ,fcc,diamagnetic,33.6  ,201,22.3,3810,0.44,20,7.4,17,0.31,1.75,0.17,7440-70-2,42e3
            21,Sc,Scandium,0,4,3,transition metal,"3,4,d",44.9559,[Ar]4s2:3d1,s,2.985,2.80,--,1814,3109,--,--,14.1,332.7,25.52,1645,1804,(2006),(2266),(2613),(3101),1.36 ,633.1,1235,2388.6 ,162,170,211 ,hexagonal,paramagnetic,--,15.8,10.2,--,25,74.4,29.1,56.6,0.279,--,0.75,7440-20-2,22
            22,Ti,Titanium,0,4,4,transition metal,"4,4,d",47.87,[Ar]4s2:3d2,s,4.506,4.11,--,1941,3560,--,--,14.15,425,25.060,1982,2171,(2403),2692,3064,3558,1.54 ,658.8,1309.8,2652.5 ,147,160,-- ,hexagonal,paramagnetic,420,21.9,8.6,5090,6.1,116,44,110,0.32,6.0,0.72,7440-32-6,5700
            23,V,Vanadium,0,4,5,transition metal,"5,4,d",50.941,[Ar]4s2:3d3,s,6.0,5.5,--,2183,3680,--,--,21.5,459,24.89,2101,2289,2523,2814,3187,3679,1.63 ,650.9,1414,2830 ,134,153,-- ,bcc,paramagnetic,197  ,30.7,8.4,4560,5.06,128,47,160,0.37,6.7,0.63,7440-62-2,120
            24,Cr,Chromium,0,4,6,transition metal,"6,4,d",51.996,[Ar]4s1:3d5,s,7.15,6.3,--,2180,2944,--,--,21.0,339.5,23.35,1656,1807,1991,2223,2530,2942,1.66 ,652.9,1590.6,2987 ,128,139,-- ,bcc,antiferromagnetic,125  ,93.9,4.9,5940,3.1,279,115,160,0.21,8.5,1.12,7440-47-3,100
            25,Mn,Manganese,0,4,7,transition metal,"7,4,d",54.93804,[Ar]4s2:3d5,s,7.21,5.95,--,1519,2334,--,--,12.91,221,26.32,1228,1347,1493,1691,1955,2333,1.55 ,717.3,1509,3248 ,127,139,-- ,bcc,paramagnetic,1440,7.81,21.7,5150,13.3,198,--,120,--,6.0,0.2,7439-96-5,950
            26,Fe,Iron,0,4,8,transition metal,"8,4,d",55.84,[Ar]4s2:3d6,s,7.86,6.98,--,1811,3134,--,--,13.81,340,25.10,1728,1890,2091,2346,2679,3132,1.83 ,762.5,1561.9,2957 ,126,132,-- ,bcc,ferromagnetic,96.1  ,80.4,11.8,5120,2.56,211,82,170,0.29,4,0.49,7439-89-6,56e3
            27,Co,Cobalt,0,4,9,transition metal,"9,4,d",58.9332,[Ar]4s2:3d7,s,8.90,7.75,--,1768,3200,--,--,16.06,377,24.81,1790,1960,2165,2423,2755,3198,1.88 ,760.4,1648,3232 ,125,126,-- ,hexagonal,ferromagnetic,62.4  ,100,13,4720,37.5,209,75,180,0.31,5.0,0.7,7440-48-4,25
            28,Ni,Nickel,0,4,10,transition metal,"10,4,d",58.693,[Ar]4s2:3d8,s,8.908,7.81,--,1728,3186,--,--,17.48,377.5,26.07,1783,1950,2154,2410,2741,3184,1.91 ,737.1,1753,3395 ,124,124,163 ,fcc,ferromagnetic,69.3  ,90.9,13.4,4900,4.51,200,76,180,0.31,4.0,0.7,7440-02-0,84
            29,Cu,Copper,0,4,11,transition metal,"11,4,d",63.55,[Ar]4s1:3d10,s,8.96,8.02,--,1357.77,2835,--,--,13.26,300.4,24.440,1509,1661,1850,2089,2404,2836,1.90 ,745.5,1957.9,3555 ,128,132,140 ,fcc,diamagnetic,16.78  ,401,16.5,3810,3.8,119,48,140,0.34,3.0,0.87,7440-50-8,60
            30,Zn,Zinc,0,4,12,transition metal,"12,4,d",65.4,[Ar]4s2:3d10,s,7.14,6.57,--,692.68,1180,--,--,7.32,123.6,25.470,610,670,750,852,990,(1185),1.65 ,906.4,1733.3,3833 ,134,122,139 ,hexagonal,diamagnetic,59.0  ,116,30.2,3850,1.10,108,43,70,0.25,2.5,0.41,7440-66-6,70
            31,Ga,Gallium,0,4,13,post-transition metal,"13,4,p",69.72,[Ar]4s2:3d10:4p1,s,5.91,6.095,--,302.91,2477,--,--,5.59,254,25.86,1310,1448,1620,1838,2125,2518,1.81 ,578.8,1979.3,2963 ,135,122,187 ,orthorhombic,diamagnetic,--,40.6,--,2740,3.1,9.8,--,--,0.47,1.5,0.06,7440-55-3,19
            32,Ge,Germanium,0,4,14,metalloid,"14,4,p",72.6,[Ar]4s2:3d10:4p2,s,5.323,5.60,--,1211.40,3106,--,--,36.94,334,23.222,1644,1814,2023,2287,2633,3104,2.01 ,762,1537.5,3302.1 ,122,122,211 ,diamond cubic,diamagnetic,1e9,60.2,6,5400,2.3,103,41,75,0.26,6.0,--,7440-56-4,1.5
            33,As,Arsenic,0,4,15,metalloid,"15,4,p",74.9216,[Ar]4s2:3d10:4p3,s,5.727,5.22,--,1090,887,1673,--,24.44,32.4,24.64,553,596,646,706,781,874,2.18 ,947.0,1798,2735 ,119,119,185 ,trigonal,diamagnetic,333  ,50.2,--,--,4.30,8,--,22,--,3.5,--,7440-38-2,1.8
            34,Se,Selenium,0,4,16,nonmetal,"16,4,p",78.9,[Ar]4s2:3d10:4p4,s,4.81,3.99,--,494,958,1766,27.2,6.69,95.48,25.363,500,552,617,704,813,958,2.55 ,941.0,2045,2973.7 ,120,120,190 ,hexagonal,diamagnetic,1e7,0.519,37,3350,12.2,10,3.7,8.3,0.33,2.0,0.74,7782-49-2,0.050
            35,Br,Bromine,x,4,17,halogen,"17,4,p",79.90,[Ar]4s2:3d10:4p5,l,3.1028,3.1028,--,265.8,332.0,588,10.34,10.571,29.96,75.69,185,201,220,244,276,332,2.96 ,1139.9,2103,3470 ,120,120,185 ,orthorhombic,diamagnetic,7.8e19,0.122,--,206,6.8,--,--,--,--,--,--,7726-95-6,2.4
            36,Kr,Krypton,0,4,18,noble gas,"18,4,p",83.79,[Ar]4s2:3d10:4p6,g,3.749e-3,--,2.413,115.79,119.93,209.41,5.50,1.64,9.08,20.786,59,65,74,84,99,120,3.00 ,1350.8,2350.4,3565 ,--,116,202 ,fcc,diamagnetic,--,9.43e-3,--,220,24.1,--,--,--,--,--,--,7439-90-9,0.00010
            37,Rb,Rubidium,0,5,1,alkali metal,"1,5,s",85.468,[Kr]5s1,s,1.532,1.46,--,312.46,961,2093,16,2.19,75.77,31.060,434,486,552,641,769,958,0.82 ,403.0,2633,3859.4,248,220,303 ,bcc,paramagnetic,128  ,58.2,--,1300,0.5,2.4,--,2.5,--,0.3,0,7440-17-7,90
            38,Sr,Strontium,0,5,2,alkaline earth metal,"2,5,s",87.6,[Kr]5s2,s,2.64,2.375,--,1050,1655,--,--,7.43,136.9,26.4,796,882,990,1139,1345,1646,0.95 ,549.5,1064.2,4138 ,215,195,249 ,fcc,paramagnetic,132  ,35.4,22.5,--,1.21,--,6.1,--,0.28,1.5,--,7440-24-6,370
            39,Y,Yttrium,0,5,3,transition metal,"3,5,d",88.9058,[Kr]4d1:5s2,s,4.472,4.24,--,1799,3609,--,--,11.42,365,26.53,1883,2075,(2320),(2627),(3036),(3607),1.22 ,600,1180,1980 ,180,190,-- ,hexagonal,paramagnetic,596,17.2,10.6,3300,1.3,63.5,25.6,41.2,0.243,--,0.59,7440-65-5,33
            40,Zr,Zirconium,0,5,4,transition metal,"4,5,d",91.22,[Kr]4d2:5s2,s,6.52,5.8,--,2128,4682,--,--,14,573,25.36,2639,2891,3197,3575,4053,4678,1.33 ,640.1,1270,2218 ,160,175,-- ,hcp,paramagnetic,421 ,22.6,5.7,3800,0.182,88,33,91.1,0.34,5.0,0.65,7440-67-7,170
            41,Nb,Niobium,0,5,5,transition metal,"5,5,d",92.9064,[Kr]4d4:5s1,s,8.57,--,--,2750,5017,--,--,30,689.9,24.60,2942,3207,3524,3910,4393,5013,1.6 ,652.1,1380,2416 ,146,164,-- ,bcc,paramagnetic,152,53.7,7.3,3480,1.15,105,38,170,0.40,6.0,0.74,7440-03-1,20
            42,Mo,Molybdenum,0,5,6,transition metal,"6,5,d",96.0,[Kr]4d5:5s1,s,10.28,9.33,--,2896,4912,--,--,37.48,617,24.06,2742,2994,3312,3707,4212,4879,2.16 ,684.3,1560,2618 ,139,154,-- ,bcc,paramagnetic,53.4  ,138,4.8,--,2.65,329,126,230,0.31,5.5,1.5,7439-98-7,1.2
            43,Tc,Technetium,0,5,7,transition metal,"7,5,d",(98),[Kr]4d5:5s2,sa,11,--,--,2430,4538,--,--,33.29,585.2,24.27,(2727),(2998),(3324),(3726),(4234),(4894),1.9 ,702,1470,2850,136,147,-- ,hexagonal,paramagnetic,--,50.6,--,16200,22,--,--,--,--,--,--,7440-26-8,trace
            44,Ru,Ruthenium,0,5,8,transition metal,"8,5,d",101.1,[Kr]4d7:5s1,s,12.45,10.65,--,2607,4423,--,--,38.59,591.6,24.06,2588,2811,3087,3424,3845,4388,2.2 ,710.2,1620,2747,134,146,-- ,hexagonal,paramagnetic,71,117,6.4,5970,3.0,447,173,220,0.30,6.5,2.16,7440-18-8,0.0010
            45,Rh,Rhodium,0,5,9,transition metal,"9,5,d",102.906,[Kr]4d8:5s1,s,12.41,10.7,--,2237,3968,--,--,26.59,494,24.98,2288,2496,2749,3063,3405,3997,2.28 ,719.7,1740,2997,134,142,-- ,fcc,paramagnetic,43.3,150,8.2,4700,150,380,150,275,0.26,6.0,1.1,7440-16-6,0.0010
            46,Pd,Palladium,0,5,10,transition metal,"10,5,d",106.4,[Kr]4d10,s,12.023,10.38,--,1828.05,3236,--,--,16.74,362,25.98,1721,1897,2117,2395,2753,3234,2.20 ,804.4,1870,3177,137,139,163 ,fcc,paramagnetic,105.4  ,71.8,11.8,3070,6.0,121,44,180,0.39,4.75,0.04,7440-05-3,0.015
            47,Ag,Silver,0,5,11,transition metal,"11,5,d",107.868,[Kr]4d10:5s1,s,10.49,9.320,--,1234.93,2435,--,--,11.28,258,25.350,1283,1413,1575,1782,2055,2433,1.93 ,731.0,2070,3361,144,145,172 ,fcc,diamagnetic,15.87  ,429,18.9,--,63.8,83,30,100,0.37,2.5,0.02,7440-22-4,0.075
            48,Cd,Cadmium,0,5,12,transition metal,"12,5,p",112.41,[Kr]4d10:5s2,s,8.65,7.996,--,594.22,1040,--,--,6.21,99.87,26.020,530,583,654,745,867,1040,1.69 ,867.8,1631.4,3616,151,144,158 ,hexagonal,diamagnetic,72.7,96.6,30.8,2310,2450,50,19,42,0.30,2.0,0.2,7440-43-9,0.15
            49,In,Indium,0,5,13,post-transition metal,"13,5,p",114.82,[Kr]4d10:5s2:5p1,s,7.31,7.02,--,429.75,2345,--,--,3.281,231.8,26.74,1196,1325,1485,1690,1962,2340,1.78 ,558.3,1820.7,2704 ,167,142,193 ,tetragonal,diamagnetic,83.7  ,81.8,32.1,1215,194,11,--,--,--,1.2,0.01,7440-74-6,0.25
            50,Sn,Tin,0,5,14,post-transition metal,"14,5,p",118.71,[Kr]4d10:5s2:5p2,s,7.265,6.99,--,505.08,2875,--,--,7.03,296.1,27.112,1497,1657,1855,2107,2438,2893,1.96 ,708.6,1411.8,2943.0 ,140,139,217 ,tetragonal,paramagnetic,115,66.8,22,--,0.63,50,18,58,0.36,1.5,0.01,7440-31-5,2.3
            51,Sb,Antimony,0,5,15,metalloid,"15,5,p",121.76,[Kr]4d10:5s2:5p3,s,6.697,6.53,--,903.78,1860,--,--,19.79,193.43,25.23,807,876,1011,1219,1491,1858,2.05 ,834,1594.9,2440 ,140,139,206 ,trigonal,diamagnetic,417  ,24.4,11,3420,5,55,20,42,--,3.0,0.29,7440-36-0,0.20
            52,Te,Tellurium,0,5,16,metalloid,"16,5,p",127.6,[Kr]4d10:5s2:5p4,s,6.24,5.70,--,722.66,1261,--,--,17.49,114.1,25.73,--,--,(775),(888),1042,1266,2.1 ,869.3,1790,2698 ,140,138,206 ,hexagonal,diamagnetic,4.36e6,1.97-3.38,--,2610,4.7,43,16,65,--,2.25,0.02,13494-80-9,0.0010
            53,I,Iodine,x,5,17,halogen,"17,5,p",126.904,[Kr]4d10:5s2:5p5,s,4.933,--,--,386.85,457.4,819,11.7,15.52,41.57,54.44,260,282,309,342,381,457,2.66 ,1008.4,1845.9,3180,140,139,198 ,orthorhombic,diamagnetic,1.3e16,0.449,--,--,6.2,--,--,7.7,--,--,--,7553-56-2,0.45
            54,Xe,Xenon,0,5,18,noble gas,"18,5,p",131.29,[Kr]4d10:5s2:5p6,g,5.894e-3,--,3.057,161.4,165.03,289.77,5.841,2.27,12.64,20.786,83,92,103,117,137,165,2.6 ,1170.4,2046.4,3099.4,--,140,216 ,fcc,diamagnetic,--,5.65e-3,--,169,24.5,--,--,--,--,--,--,7440-63-3,3.0e-005
            55,Cs,Cesium,0,6,1,alkali metal,"1,6,s",132.905,[Xe]6s1,s,1.93,1.843,--,301.59,944,1938,9.4,2.09,63.9,32.210,418,469,534,623,750,940,0.79 ,375.7,2234.3,3400,265,244,343 ,bcc,paramagnetic,205  ,35.9,97,--,30.0,1.7,--,1.6,--,0.2,0,7440-46-2,3.0
            56,Ba,Barium,0,6,2,alkaline earth metal,"2,6,s",137.33,[Xe]6s2,s,3.51,3.338,--,1000,2170,--,--,7.12,140.3,28.07,911,1038,1185,1388,1686,2170,0.89 ,502.9,965.2,3600,222,215,268 ,bcc,paramagnetic,332  ,18.4,20.6,--,1.2,13,4.9,9.6,--,1.25,--,7440-39-3,430
            57,La,Lanthanum,0,7.1,4.1,lanthanide,"--,6,f",138.905,[Xe]5d1:6s2,s,6.162,5.94,--,1193,3737,--,--,6.20,402.1,27.11,(2005),(2208),(2458),(2772),(3178),(3726),1.10 ,538.1,1067,1850.3 ,187,207,-- ,hexagonal,paramagnetic,615,13.4,12.1,2475,8.9,36.6,14.3,27.9,0.280,2.5,0.36,7439-91-0,39
            58,Ce,Cerium,0,7.1,5.1,lanthanide,"--,6,f",140.12,[Xe]4f:5d:6s2,s,6.770,6.55,--,1068,3716,--,--,5.46,398,26.94,1992,2194,2442,2754,3159,3705,1.12 ,534.4,1050,1949 ,181.8,204,-- ,fcc,paramagnetic,828,11.3,6.3,2100,0.73,33.6,13.5,21.5,0.24,2.5,0.41,7440-45-1,67
            59,Pr,Praseodymium,0,7.1,6.1,lanthanide,"--,6,f",140.908,[Xe]4f3:6s2,s,6.77,6.50,--,1208,3793,--,--,6.89,331,27.20,1771,1973,(2227),(2571),(3054),(3779),1.13 ,527,1020,2086 ,182,203,-- ,hexagonal,paramagnetic,700,12.5,6.7,2280,11.5,37.3,14.8,28.8,0.281,--,0.48,7440-10-0,9.2
            60,Nd,Neodymium,0,7.1,7.1,lanthanide,"--,6,f",144.24,[Xe]4f4:6s2,s,7.01,6.89,--,1297,3347,--,--,7.14,289,27.45,1595,1774,1998,(2296),(2715),(3336),1.14 ,533.1,1040,2130 ,181,201,-- ,hexagonal,paramagnetic,643,16.5,9.6,2330,49,41.4,16.3,31.8,0.281,--,0.27,7440-00-8,42
            61,Pm,Promethium,0,7.1,8.1,lanthanide,"--,6,f",(145),[Xe]4f5:6s2,sa,7.26,--,--,1315,3273,--,--,7.13,289,--,--,--,--,--,--,--,1.13?,540,1050,2150 ,183,199,-- ,hexagonal,paramagnetic,750[e],17.9,11[e],--,8400,46[e],18[e],33[e],0.28[e],--,--,7440-12-2,trace
            62,Sm,Samarium,0,7.1,9.1,lanthanide,"--,6,f",150.4,[Xe]4f6:6s2,s,7.52,7.16,--,1345,2067,--,--,8.62,165,29.54,1001,1106,1240,(1421),(1675),(2061),1.17 ,544.5,1070,2260 ,180,198,-- ,rhombohedral,paramagnetic,940,13.3,12.7,2130,5820,49.7,19.5,37.8,0.274,--,0.44,7440-19-9,7.0
            63,Eu,Europium,0,7.1,10.1,lanthanide,"--,6,f",151.96,[Xe]4f7:6s2,s,5.244,5.13,--,1099,1802,--,--,9.21,176,27.66,863,957,1072,1234,1452,1796,1.2?,547.1,1085,2404 ,180,198,-- ,bcc,paramagnetic,900,13.9[e],35.0,--,4100,18.2,7.9,8.3,0.152,--,--,7440-53-1,2.0
            64,Gd,Gadolinium,0,7.1,11.1,lanthanide,"--,6,f",157.2,[Xe]4f7:5d1:6s2,s,7.90,7.4,--,1585,3546,--,--,10.05,301.3,37.03,(1836),(2028),(2267),(2573),(2976),(3535),1.20 ,593.4,1170,1990 ,180,196,-- ,hexagonal,paramagnetic,1310,10.6,9.4,2680,49000,54.8,21.8,37.9,0.259,--,--,7440-54-2,6.2
            65,Tb,Terbium,0,7.1,12.1,lanthanide,"--,6,f",158.925,[Xe]4f9:6s2,s,8.23,7.65,--,1629,3503,--,--,10.15,293,28.91,1789,1979,(2201),(2505),(2913),(3491),1.2?,565.8,1110,2114 ,177,194,-- ,hexagonal,paramagnetic,1150,11.1,10.3,2620,30,55.7,22.1,38.7,0.261,--,0.68,7440-27-9,1.2
            66,Dy,Dysprosium,0,7.1,13.1,lanthanide,"--,6,f",162.50,[Xe]4f10:6s2,s,8.540,8.37,--,1680,2840,--,--,11.06,280,27.7,1378,1523,(1704),(1954),(2304),(2831),1.22 ,573.0,1130,2200 ,178,192,-- ,hexagonal,paramagnetic,926,10.7,9.9,2710,90,61.4,24.7,40.5,0.247,--,0.5,7429-91-6,5.2
            67,Ho,Holmium,0,7.1,14.1,lanthanide,"--,6,f",164.930,[Xe]4f11:6s2,s,8.79,8.34,--,1734,2993,--,--,17.0,265,27.15,1432,1584,(1775),(2040),(2410),(2964),1.23 ,581.0,1140,2204 ,176,192,-- ,hexagonal,paramagnetic,814,16.2,11.2,2760,65,64.8,26.3,40.2,0.231,--,0.75,7440-60-0,1.3
            68,Er,Erbium,0,7.1,15.1,lanthanide,"--,6,f",167.26,[Xe]4f12:6s2,s,9.066,8.86,--,1802,3141,--,--,19.90,280,28.12,1504,1663,(1885),(2163),(2552),(3132),1.24 ,589.3,1150,2194 ,176,189,-- ,hexagonal,paramagnetic,860,14.5,12.2,2830,0.16,69.9,28.3,44.4,0.237,--,0.81,7440-52-0,3.5
            69,Tm,Thulium,0,7.1,16.1,lanthanide,"--,6,f",168.934,[Xe]4f13:6s2,s,9.32,8.56,--,1818,2223,--,--,16.84,247,27.03,1117,1235,1381,1570,(1821),(2217),1.25 ,596.7,1160,2285 ,176,190,-- ,hexagonal,paramagnetic,676,16.9,13.3,--,115,74.0,30.5,44.5,0.213,--,0.47,7440-30-4,0.52
            70,Yb,Ytterbium,0,7.1,17.1,lanthanide,"--,6,f",173.05,[Xe]4f14:6s2,s,6.90,6.21,--,1097,1469,--,--,7.66,159,26.74,736,813,910,1047,(1266),(1465),1.1?,603.4,1174.8,2417 ,176,187,-- ,fcc,paramagnetic,250,38.5,26.3,1590,37,23.9,9.9,30.5,0.207,--,0.34,7440-64-4,3.2
            71,Lu,Lutetium,0,7.1,18.1,lanthanide,"--,6,f",174.967,[Xe]4f14:6s2:5d1,s,9.841,9.3,--,1925,3675,--,--,22,414,26.86,1906,2103,2346,(2653),(3072),(3663),1.27 ,523.5,1340,2022.3 ,174,160,-- ,hexagonal,paramagnetic,582,16.4,9.9,--,75,68.6,27.2,47.6,0.261,--,0.89,7439-94-3,0.80
            72,Hf,Hafnium,0,6,4,transition metal,"4,6,d",178.5,[Xe]4f14:6s2:5d2,s,13.31,12,--,2506,4876,--,--,27.2,571,25.73,2689,2954,3277,3679,4194,4876,1.3 ,658.5,1440,2250 ,159,175,-- ,hexagonal,paramagnetic,331  ,23.0,5.9,3010,103,78,30,110,0.37,5.5,1.7, 7440-58-6,3.0
            73,Ta,Tantalum,0,6,5,transition metal,"5,6,d",180.948,[Xe]4f14:6s2:5d3,s,16.69,15,--,3290,5731,--,--,36.57,732.8,25.36,3297,3597,3957,4395,4939,5634,1.5 ,761,1500,--,146,170,-- ,bcc,paramagnetic,131  ,57.5,6.3,3400,22,186,69,200,0.34,6.5,0.8, 7440-25-7,2.0
            74,W,Tungsten,0,6,6,transition metal,"6,6,d",183.8,[Xe]4f14:6s2:5d4,s,19.25,17.6,--,3695,5828,--,--,35.3,806.7,24.27,3477,3773,4137,4579,5127,5823,2.36 ,770,1700,--,139,162,-- ,bcc,paramagnetic,52.8  ,173,4.5,--,18.5,411,161,310,0.28,7.5,2.57,7440-33-7,1.3
            75,Re,Rhenium,0,6,7,transition metal,"7,6,d",186.21,[Xe]4f14:6s2:5d5,s,21.02,18.9,--,3459,5869,--,--,60.43,704,25.48,3303,3614,4009,4500,5127,5954,1.9 ,760,1260,2510 ,137,151,-- ,hexagonal,paramagnetic,193  ,48.0,6.2,4700,85,463,178,370,0.30,7.0,1.32, 7440-15-5,0.00070
            76,Os,Osmium,0,6,8,transition metal,"8,6,d",190.2,[Xe]4f14:6s2:5d6,s,22.61,20,--,3306,5285,--,--,57.85,738,24.7,3160,3423,3751,4148,4638,5256,2.2 ,840,1600,--,135,144,-- ,hexagonal,paramagnetic,81.2,87.6,5.1,4940,15.3,--,222,462,0.25,7.0,3.92,7440-04-2,0.0015
            77,Ir,Iridium,0,6,9,transition metal,"9,6,d",192.22,[Xe]4f14:6s2:5d7,s,22.65,19,--,2719,4701,--,--,41.12,563,25.10,2713,2957,3252,3614,4069,4659,2.20 ,880,1600,--,136,141,-- ,fcc,paramagnetic,47.1  ,147,6.4,4825,425,528,210,320,0.26,6.5,1.67,7439-88-5,0.0010
            78,Pt,Platinum,0,6,10,transition metal,"10,6,d",195.08,[Xe]4f14:6s1:5d9,s,21.45,19.77,--,2041.4,4098,--,--,22.17,469,25.86,2330,(2550),2815,3143,3556,4094,2.28 ,870,1791,--,139,136,175 ,fcc,paramagnetic,105  ,71.6,8.8,--,9,168,61,230,0.38,4-4.5,0.39, 7440-06-4,0.0050
            79,Au,Gold,0,6,11,transition metal,"11,6,d",196.966,[Xe]4f14:6s1:5d10,s,19.3,17.31,--,1337.33,3129,--,--,12.55,324,25.418,1646,1814,2021,2281,2620,3078,2.54 ,890.1,1980,--,144,136,166 ,fcc,diamagnetic,22.14  ,318,14.2,2030,98.8,79,27,180,0.44,2.5,0.25,7440-57-5,0.0040
            80,Hg,Mercury,0,6,12,transition metal,"12,6,d",200.6,[Xe]4f14:6s2:5d10,l,--,13.534,--,234.32,629.88,1750,172.00,2.29,59.11,27.983,315,350,393,449,523,629,2.00 ,1007.1,1810,3300,151,132,155 ,rhombohedral,diamagnetic,961,8.30,60.4,1451.4,375,--,--,--,--,--,--,7439-97-6,0.085
            81,Tl,Thallium,0,6,13,post-transition metal,"13,6,d",204.383,[Xe]4f14:6s2:5d10:6p1,s,11.85,11.22,--,577,1746,--,--,4.14,165,26.32,882,977,1097,1252,1461,1758,1.62 ,589.4,1971,2878,170,170,196 ,hexagonal,diamagnetic,180,46.1,29.9,818,3.4,8,2.8,43,0.45,1.2,0.03,7440-28-0,0.85
            82,Pb,Lead,0,6,14,post-transition metal,"14,6,d",207,[Xe]4f14:6s2:5d10:6p2,s,11.34,10.66,--,600.61,2022,--,--,4.77,179.5,26.650,978,1088,1229,1412,1660,2027,2.33 ,715.6,1450.5,3081.5 ,175,146,202 ,fcc,diamagnetic,208  ,35.3,28.9,--,0.18,16,5.6,46,0.44,1.5,0.04,7439-92-1,14
            83,Bi,Bismuth,0,6,15,post-transition metal,"15,6,d",208.980,[Xe]4f14:6s2:5d10:6p3,s,9.78,10.05,--,544.7,1837,--,--,11.30,151,25.52,941,1041,1165,1325,1538,1835,2.02 ,703,1610,2466 ,156,148,207 ,trigonal,diamagnetic,1290,7.97,13.4,1790,0.034,32,12,31,0.33,2.25,0.09,7440-69-9,0.0085
            84,Po,Polonium,0,6,16,metalloid,"16,6,d",(209),[Xe]4f14:6s2:5d10:6p4,s,9.398,--,--,527,1235,--,--,13,102.91,26.4,--,--,--,(846),1003,1236,2.0 ,812.1,--,--,168,140,197 ,cubic,nonmagnetic,400,20?,23.5,--,<0.5,--,--,--,--,--,--,7440-08-6,2.0e-10
            85,At,Astatine,0,6,17,halogen,"17,6,p",(210),[Xe]4f14:6s2:5d10:6p5,s,--,--,--,575,610?,--,--,--,40,--,361,392,429,475,531,607,2.2 ,890,--,--,--,150,202 ,--,--,--,1.7,--,--,--,--,--,--,--,--,--,7440-68-8,trace
            86,Rn,Radon,0,6,18,noble gas,"18,6,p",(222),[Xe]4f14:6s2:5d10:6p6,g,9.73e-3,4.4,--,202,211.3,377,6.28,3.247,18.1,20.786,110,121,134,152,176,211,2.2,1037,--,--,--,150,220 ,fcc,non-magnetic,--,3.61e-3,--,--,--,--,--,--,--,--,--,10043-92-2,4.0e-13
            87,Fr,Francium,0,7,1,alkali metal,"1,7,s",(223),[Rn]7s1,s,1.87,--,--,300?,950?,--,--,2,65,31.8,(404),(454),(519),(608),(738),(946),0.7 ,380,--,--,--,260,348 ,bcc,paramagnetic,3000,15,--,--,--,--,--,--,--,--,--,7440-73-5,trace
            88,Ra,Radium,0,7,2,alkaline earth metal,"2,7,s",(226),[Rn]7s2,s,5.5,--,--,973,2010,--,--,8.5,113,--,819,906,1037,1209,1446,1799,0.9 ,509.3,"979,0",--,--,221,283 ,bcc,non-magnetic,1000,18.6,--,--,--,--,--,--,--,--,--, 7440-14-4,9.0e-7
            89,Ac,Actinium,0,8.15,4.1,actinide,"na,7,f",(227),[Rn]6d1:7s2,s,10,--,--,1323,3471,--,--,14,400,27.2,--,--,--,--,--,--,1.1 ,499,1170,--,--,215,-- ,fcc,--,--,12,--,--,--,--,--,--,--,--,--,7440-34-8,5.5e-10
            90,Th,Thorium,0,8.15,5.1,actinide,"na,7,f",232.038,[Rn]6d2:7s2,s,11.7,--,--,2115,5061,--,--,13.81,514,26.230,2633,2907,3248,3683,4259,5055,1.3 ,587,1110,1930 ,179,206,-- ,fcc,paramagnetic,147,54.0,11,2490,7.4,79,31,54,0.27,3.0,0.4,7440-29-1,9.6
            91,Pa,Protactinium,0,8.15,6.1,actinide,"na,7,f",231.036,[Rn]6d1:7s2:5f2,s,15.37,--,--,1841,4300?,--,--,12.34,481,--,--,--,--,--,--,--,1.5 ,568,--,--,163,200,-- ,tetragonal,paramagnetic,177,47,--,--,--,--,--,--,--,--,--,7440-13-3,1.4e-6
            92,U,Uranium,0,8.15,7.1,actinide,"na,7,f",238.029,[Rn]6d1:7s2:5f3,s,19.1,17.3,--,1405.3,4404,--,--,9.14,417.1,27.665,2325,2564,2859,3234,3727,4402,1.38 ,597.6,1420,--,156,196,186 ,orthorhombic,paramagnetic,280,27.5,13.9,3155,7.6,208,111,100,0.23,--,2.4,7440-61-1,2.7
            93,Np,Neptunium,0,8.15,8.1,actinide,"na,7,f",(237),[Rn]6d1:7s2:5f4,sa,20.45,--,--,917,4273,--,--,3.20,336,29.46,2194,2437,--,--,--,--,1.36 ,604.5,--,--,155,190,-- ,,paramagnetic,1220,6.3,--,--,--,--,--,--,--,--,--,7439-99-8,trace
            94,Pu,Plutonium,0,8.15,9.1,actinide,"na,7,f",(244),[Rn]7s2:5f6,sa,19.816,16.63,--,912.5,3501,--,--,2.82,333.5,35.5,1756,1953,2198,2511,2926,3499,1.28 ,584.7,--,--,159,187,-- ,monoclinic,paramagnetic,1460,6.74,46.7,2260,1.8,96,43,--,0.21,--,--, 7440-07-5,trace
            95,Am,Americium,0,8.15,10.1,actinide,"na,7,f",(243),[Rn]7s2:5f7,sa,12,--,--,1449,2880,--,--,14.39,--,62.7,1239,1356,--,--,--,--,1.3 ,578,--,--,173,180,-- ,hexagonal,paramagnetic,690,10,--,--,--,--,--,--,--,--,--,7440-35-9,--
            96,Cm,Curium,0,8.15,11.1,actinide,"na,7,f",(251),[Rn]7s2:5f7:6d1,sa,13.51,-- ,--,1613,3383,-- ,-- ,15?,--,--,1788,1982,--,--,--,-- ,1.3,581,--,--,174,169,-- ,hcp,paramagnetic,1250,--,--,--,--,--,--,--,--,--,0,7440-51-9,--
            97,Bk,Berkelium,0,8.15,12.1,actinide,"na,7,f",(247),[Rn]7s2:5f9,sa,14.78,--,--,1259,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,601,--,--,170,--,-- ,hcp,paramagnetic,--,10,--,--,--,--,--,--,--,--,--,7440-40-6,--
            98,Cf,Californium,0,8.15,13.1,actinide,"na,7,f",(251),[Rn]7s2:5f10,sa,13.51,--,--,1613,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,608,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,3-4,--, 7440-71-3,--
            99,Es,Einsteinium,0,8.15,14.1,actinide,"na,7,f",(252),[Rn]7s2:5f11,sa,8.84,--,--,1133,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,619,--,--,--,--,--,--,paramagnetic,--,--,--,--,--,--,--,--,--,--,--,7429-92-7,--
            100,Fm,Fermium,0,8.15,15.1,actinide,"na,7,f",(257),[Rn]7s2:5f12,sa,--,--,--,1800,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,627,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,7440-72-4,--
            101,Md,Mendelevium,0,8.15,16.1,actinide,"na,7,f",(258),[Rn]7s2:5f13,sa,--,--,--,1100,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,635,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--, 7440-11-1,--
            102,No,Nobelium,0,8.15,17.1,actinide,"na,7,f",(259),[Rn]7s2:5f14,sa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,641.6,1254.3,2605.1,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--, 10028-14-5,--
            103,Lw,Lawrencium,0,8.15,18.1,actinide,"na,7,f",(262),[Rn]7s2:6d1:5f14,sa,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,1.3 ,443.8,1428.0,2219.1,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,22537-19-5,--
        ''').split("\n")
        elements = {}
        for i, items in enumerate(csv.reader(data)):
            if not i:
                numfields = len(items)
                names = items
                continue
            else:
                if len(items) != numfields:
                    raise ValueError(f"Data line doesn't have {numfields} fields: {items}")
            e = dict(zip(names, items))
            atomic_number = int(e["num"])
            assert atomic_number == i
            elements[i] = Element(e)
        return elements
    def GetElementNames(elements):
        names = {}
        for z in elements:
            sym = elements[z].sym
            names[sym] = z
        return names
if 1:   # Core functionality
    def PrintElement(z):
        element = elements[z]
        t.print(f"{t.name}{element.name}")
        print(elements[z])

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if 1:   # Get our data
        # attributes = {attr: description}
        attributes = GetAttributes()
        # elements = {atomicnum: Element instance}
        elements = GetElements()
        # symbols = {symbol: atomicnum}
        symbols = GetElementNames(elements)
    for arg in args:
        if arg in symbols:
            z = symbols[arg]
            PrintElement(z)
        else:
            r = re.compile(arg, re.I)
            for z in elements:
                mo = r.search(elements[z].name)
                if mo:
                    PrintElement(z)
    if d["-a"]:
        w = max(len(i) for i in attributes)
        for attr in attributes:
            descr, unit = attributes[attr]
            if unit:
                print(f"{attr:{w}s} {descr} [{unit}]")
            else:
                print(f"{attr:{w}s} {descr}")

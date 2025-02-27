"""
Call GetElementNamedTuples() to get a list of named tuples with the properties of the elements.
The index is 1 minus the atomic number.

    Can also be run as a script to look at the properties of individual elements and launch
    wikipedia's web page on an element.

    Data from e.g.
        https://en.wikipedia.org/wiki/Hydrogen
        https://en.wikipedia.org/wiki/Isotopes_of_hydrogen
        https://en.wikipedia.org/wiki/List_of_chemical_elements
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Program description string
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        import re
        import string
        import sys
        import webbrowser
        from pprint import pprint as pp
        from collections import deque, namedtuple
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from lwtest import Assert
        from columnize import Columnize
        from f import flt

        if 1:
            import debug

            debug.SetDebugger()
        t.dbg = t("brnl")
        t.err = t("ornl")
    if 1:  # Global variables
        ii = isinstance
        elements = """
            Hydrogen       H    1
            Helium         He   2
            Lithium        Li   3
            Beryllium      Be   4
            Boron          B    5
            Carbon         C    6
            Nitrogen       N    7
            Oxygen         O    8
            Fluorine       F    9
            Neon           Ne   10
            Sodium         Na   11
            Magnesium      Mg   12
            Aluminum       Al   13
            Silicon        Si   14
            Phosphorus     P    15
            Sulfur         S    16
            Chlorine       Cl   17
            Argon          Ar   18
            Potassium      K    19
            Calcium        Ca   20
            Scandium       Sc   21
            Titanium       Ti   22
            Vanadium       V    23
            Chromium       Cr   24
            Manganese      Mn   25
            Iron           Fe   26
            Cobalt         Co   27
            Nickel         Ni   28
            Copper         Cu   29
            Zinc           Zn   30
            Gallium        Ga   31
            Germanium      Ge   32
            Arsenic        As   33
            Selenium       Se   34
            Bromine        Br   35
            Krypton        Kr   36
            Rubidium       Rb   37
            Strontium      Sr   38
            Yttrium        Y    39
            Zirconium      Zr   40
            Niobium        Nb   41
            Molybdenum     Mo   42
            Technetium     Tc   43
            Ruthenium      Ru   44
            Rhodium        Rh   45
            Palladium      Pd   46
            Silver         Ag   47
            Cadmium        Cd   48
            Indium         In   49
            Tin            Sn   50
            Antimony       Sb   51
            Tellurium      Te   52
            Iodine         I    53
            Xenon          Xe   54
            Cesium         Cs   55
            Barium         Ba   56
            Lanthanum      La   57
            Cerium         Ce   58
            Praseodymium   Pr   59
            Neodymium      Nd   60
            Promethium     Pm   61
            Samarium       Sm   62
            Europium       Eu   63
            Gadolinium     Gd   64
            Terbium        Tb   65
            Dysprosium     Dy   66
            Holmium        Ho   67
            Erbium         Er   68
            Thulium        Tm   69
            Ytterbium      Yb   70
            Lutetium       Lu   71
            Hafnium        Hf   72
            Tantalum       Ta   73
            Tungsten       W    74
            Rhenium        Re   75
            Osmium         Os   76
            Iridium        Ir   77
            Platinum       Pt   78
            Gold           Au   79
            Mercury        Hg   80
            Thallium       Tl   81
            Lead           Pb   82
            Bismuth        Bi   83
            Polonium       Po   84
            Astatine       At   85
            Radon          Rn   86
            Francium       Fr   87
            Radium         Ra   88
            Actinium       Ac   89
            Thorium        Th   90
            Protactinium   Pa   91
            Uranium        U    92
            Neptunium      Np   93
            Plutonium      Pu   94
            Americium      Am   95
            Curium         Cm   96
            Berkelium      Bk   97
            Californium    Cf   98
            Einsteinium    Es   99
            Fermium        Fm   100
            Mendelevium    Md   101
            Nobelium       No   102
            Lawrencium     Lr   103
            Rutherfordium  Rf   104
            Dubnium        Db   105
            Seaborgium     Sg   106
            Bohrium        Bh   107
            Hassium        Hs   108
            Meitnerium     Mt   109
            Darmstadtium   Ds   110
            Roentgenium    Rg   111
            Copernicium    Cn   112
            Nihonium       Nh   113
            Flerovium      Fl   114
            Moscovium      Mc   115
            Livermorium    Lv   116
            Tennessine     Ts   117
            Oganesson      Og   118
            """

        # Mappings for element names, symbols, atomic numbers
        class g:
            pass

        g.sym2num = {}  # {('h', 1), ('he', 2), ...
        #  ('H', 1), ('He', 2)}
        g.num2sym = {}  # {(1, 'h'), (2, 'he')}
        g.num2Sym = {}  # {(1, 'H'), (2, 'He')}
        g.num2name = {}  # {(1, 'hydrogen'), (2, 'helium')}
        g.num2Name = {}  # {(1, 'Hydrogen'), (2, 'Helium')}
        g.name2num = {}  # [('hydrogen', 1), ('helium', 2)]
        g.Name2num = {}  # [('Hydrogen', 1), ('Helium', 2)]
        g.names = []  # ['hydrogen', 'helium', ...
        #  'Hydrogen', 'Helium']
        g.symbols = []  # ['h', 'he', 'li', 'be', ...
        #  'H', 'He', 'Li', 'Be']
if 1:  # Element data
    # Screen-scraped from https://en.wikipedia.org/wiki/List_of_chemical_elements
    # Edits made
    # - Removed notes like '[a]' and '[7]'
    # - Changed Fm's mp to a single estimate
    # - Changed numbers like 1×10-4 to 1×10⁻⁴

    data = """
    1	H	Hydrogen	Greek elements hydro- and -gen, 'water-forming'	1	1	s-block	1.0080	0.00008988	14.01	20.28	14.304	2.20	1400	primordial	gas
    2	He	Helium	Greek hḗlios, 'sun'	18	1	s-block	4.0026	0.0001785	-[k]	4.22	5.193	-	0.008	primordial	gas
    3	Li	Lithium	Greek líthos, 'stone'	1	2	s-block	6.94	0.534	453.69	1560	3.582	0.98	20	primordial	solid
    4	Be	Beryllium	Beryl, a mineral (ultimately from the name of Belur in southern India)[4]	2	2	s-block	9.0122	1.85	1560	2742	1.825	1.57	2.8	primordial	solid
    5	B	Boron	Borax, a mineral (from Arabic bawraq, Middle Persian *bōrag)	13	2	p-block	10.81	2.34	2349	4200	1.026	2.04	10	primordial	solid
    6	C	Carbon	Latin carbo, 'coal'	14	2	p-block	12.011	2.267	>4000	4300	0.709	2.55	200	primordial	solid
    7	N	Nitrogen	Greek nítron and -gen, 'niter-forming'	15	2	p-block	14.007	0.0012506	63.15	77.36	1.04	3.04	19	primordial	gas
    8	O	Oxygen	Greek oxy- and -gen, 'acid-forming'	16	2	p-block	15.999	0.001429	54.36	90.20	0.918	3.44	461000	primordial	gas
    9	F	Fluorine	Latin fluere, 'to flow'	17	2	p-block	18.998	0.001696	53.53	85.03	0.824	3.98	585	primordial	gas
    10	Ne	Neon	Greek néon, 'new'	18	2	p-block	20.180	0.0009002	24.56	27.07	1.03	-	0.005	primordial	gas
    11	Na	Sodium	English (from medieval Latin) soda ·  Symbol Na is derived from New Latin natrium, coined from German Natron, 'natron'	1	3	s-block	22.990	0.968	370.87	1156	1.228	0.93	23600	primordial	solid
    12	Mg	Magnesium	Magnesia, a district of Eastern Thessaly in Greece	2	3	s-block	24.305	1.738	923	1363	1.023	1.31	23300	primordial	solid
    13	Al	Aluminium	Alumina, from Latin alumen (gen. aluminis), 'bitter salt, alum'	13	3	p-block	26.982	2.70	933.47	2792	0.897	1.61	82300	primordial	solid
    14	Si	Silicon	Latin silex, 'flint' (originally silicium)	14	3	p-block	28.085	2.3290	1687	3538	0.705	1.9	282000	primordial	solid
    15	P	Phosphorus	Greek phōsphóros, 'light-bearing'	15	3	p-block	30.974	1.823	317.30	550	0.769	2.19	1050	primordial	solid
    16	S	Sulfur	Latin sulphur, 'brimstone'	16	3	p-block	32.06	2.07	388.36	717.87	0.71	2.58	350	primordial	solid
    17	Cl	Chlorine	Greek chlōrós, 'greenish yellow'	17	3	p-block	35.45	0.0032	171.6	239.11	0.479	3.16	145	primordial	gas
    18	Ar	Argon	Greek argós, 'idle' (because of its inertness)	18	3	p-block	39.95	0.001784	83.80	87.30	0.52	-	3.5	primordial	gas
    19	K	Potassium	New Latin potassa, 'potash', itself from pot and ash ·  Symbol K is derived from Latin kalium	1	4	s-block	39.098	0.89	336.53	1032	0.757	0.82	20900	primordial	solid
    20	Ca	Calcium	Latin calx, 'lime'	2	4	s-block	40.078	1.55	1115	1757	0.647	1.00	41500	primordial	solid
    21	Sc	Scandium	Latin Scandia, 'Scandinavia'	3	4	d-block	44.956	2.985	1814	3109	0.568	1.36	22	primordial	solid
    22	Ti	Titanium	Titans, the sons of the Earth goddess of Greek mythology	4	4	d-block	47.867	4.506	1941	3560	0.523	1.54	5650	primordial	solid
    23	V	Vanadium	Vanadis, an Old Norse name for the Scandinavian goddess Freyja	5	4	d-block	50.942	6.11	2183	3680	0.489	1.63	120	primordial	solid
    24	Cr	Chromium	Greek chróma, 'colour'	6	4	d-block	51.996	7.15	2180	2944	0.449	1.66	102	primordial	solid
    25	Mn	Manganese	Corrupted from magnesia negra; see § magnesium	7	4	d-block	54.938	7.21	1519	2334	0.479	1.55	950	primordial	solid
    26	Fe	Iron	English word, from Proto-Celtic *īsarnom ('iron'), from a root meaning 'blood' ·  Symbol Fe is derived from Latin ferrum	8	4	d-block	55.845	7.874	1811	3134	0.449	1.83	56300	primordial	solid
    27	Co	Cobalt	German Kobold, 'goblin'	9	4	d-block	58.933	8.90	1768	3200	0.421	1.88	25	primordial	solid
    28	Ni	Nickel	Nickel, a mischievous sprite of German miner mythology	10	4	d-block	58.693	8.908	1728	3186	0.444	1.91	84	primordial	solid
    29	Cu	Copper	English word, from Latin cuprum, from Ancient Greek Kýpros 'Cyprus'	11	4	d-block	63.546	8.96	1357.77	2835	0.385	1.90	60	primordial	solid
    30	Zn	Zinc	Most likely from German Zinke, 'prong' or 'tooth', though some suggest Persian sang, 'stone'	12	4	d-block	65.38	7.14	692.88	1180	0.388	1.65	70	primordial	solid
    31	Ga	Gallium	Latin Gallia, 'France'	13	4	p-block	69.723	5.91	302.9146	2673	0.371	1.81	19	primordial	solid
    32	Ge	Germanium	Latin Germania, 'Germany'	14	4	p-block	72.630	5.323	1211.40	3106	0.32	2.01	1.5	primordial	solid
    33	As	Arsenic	French arsenic, from Greek arsenikón 'yellow arsenic' (influenced by arsenikós, 'masculine' or 'virile'), from a West Asian wanderword ultimately from Old Iranian *zarniya-ka, 'golden'	15	4	p-block	74.922	5.727	1090[l]	887	0.329	2.18	1.8	primordial	solid
    34	Se	Selenium	Greek selḗnē, 'moon'	16	4	p-block	78.971	4.81	453	958	0.321	2.55	0.05	primordial	solid
    35	Br	Bromine	Greek brômos, 'stench'	17	4	p-block	79.904	3.1028	265.8	332.0	0.474	2.96	2.4	primordial	liquid
    36	Kr	Krypton	Greek kryptós, 'hidden'	18	4	p-block	83.798	0.003749	115.79	119.93	0.248	3.00	1×10⁻⁴	primordial	gas
    37	Rb	Rubidium	Latin rubidus, 'deep red'	1	5	s-block	85.468	1.532	312.46	961	0.363	0.82	90	primordial	solid
    38	Sr	Strontium	Strontian, a village in Scotland, where it was found	2	5	s-block	87.62	2.64	1050	1655	0.301	0.95	370	primordial	solid
    39	Y	Yttrium	Ytterby, Sweden, where it was found; see also terbium, erbium, ytterbium	3	5	d-block	88.906	4.472	1799	3609	0.298	1.22	33	primordial	solid
    40	Zr	Zirconium	Zircon, a mineral, from Persian zargun, 'gold-hued'	4	5	d-block	91.224	6.52	2128	4682	0.278	1.33	165	primordial	solid
    41	Nb	Niobium	Niobe, daughter of king Tantalus from Greek mythology; see also tantalum	5	5	d-block	92.906	8.57	2750	5017	0.265	1.6	20	primordial	solid
    42	Mo	Molybdenum	Greek molýbdaina, 'piece of lead', from mólybdos, 'lead', due to confusion with lead ore galena (PbS)	6	5	d-block	95.95	10.28	2896	4912	0.251	2.16	1.2	primordial	solid
    43	Tc	Technetium	Greek tekhnētós, 'artificial'	7	5	d-block	[97][a]	11	2430	4538	-	1.9	~3×10⁻⁹	from decay	solid
    44	Ru	Ruthenium	New Latin Ruthenia, 'Russia'	8	5	d-block	101.07	12.45	2607	4423	0.238	2.2	0.001	primordial	solid
    45	Rh	Rhodium	Greek rhodóeis, 'rose-coloured', from rhódon, 'rose'	9	5	d-block	102.91	12.41	2237	3968	0.243	2.28	0.001	primordial	solid
    46	Pd	Palladium	Pallas, an asteroid, considered a planet at the time	10	5	d-block	106.42	12.023	1828.05	3236	0.244	2.20	0.015	primordial	solid
    47	Ag	Silver	English word ·  Symbol Ag is derived from Latin argentum	11	5	d-block	107.87	10.49	1234.93	2435	0.235	1.93	0.075	primordial	solid
    48	Cd	Cadmium	New Latin cadmia, from King Kadmos	12	5	d-block	112.41	8.65	594.22	1040	0.232	1.69	0.159	primordial	solid
    49	In	Indium	Latin indicum, 'indigo', the blue colour found in its spectrum	13	5	p-block	114.82	7.31	429.75	2345	0.233	1.78	0.25	primordial	solid
    50	Sn	Tin	English word ·  Symbol Sn is derived from Latin stannum	14	5	p-block	118.71	7.265	505.08	2875	0.228	1.96	2.3	primordial	solid
    51	Sb	Antimony	Latin antimonium, the origin of which is uncertain: folk etymologies suggest it is derived from Greek antí ('against') + mónos ('alone'), or Old French anti-moine, 'Monk's bane', but it could plausibly be from or related to Arabic ʾiṯmid, 'antimony', reformatted as a Latin word ·  Symbol Sb is derived from Latin stibium 'stibnite'	15	5	p-block	121.76	6.697	903.78	1860	0.207	2.05	0.2	primordial	solid
    52	Te	Tellurium	Latin tellus, 'the ground, earth'	16	5	p-block	127.60	6.24	722.66	1261	0.202	2.1	0.001	primordial	solid
    53	I	Iodine	French iode, from Greek ioeidḗs, 'violet'	17	5	p-block	126.90	4.933	386.85	457.4	0.214	2.66	0.45	primordial	solid
    54	Xe	Xenon	Greek xénon, neuter form of xénos 'strange'	18	5	p-block	131.29	0.005894	161.4	165.03	0.158	2.60	3×10⁻⁵	primordial	gas
    55	Cs	Caesium	Latin caesius, 'sky-blue'	1	6	s-block	132.91	1.93	301.59	944	0.242	0.79	3	primordial	solid
    56	Ba	Barium	Greek barýs, 'heavy'	2	6	s-block	137.33	3.51	1000	2170	0.204	0.89	425	primordial	solid
    57	La	Lanthanum	Greek lanthánein, 'to lie hidden'	f-block groups	6	f-block	138.91	6.162	1193	3737	0.195	1.1	39	primordial	solid
    58	Ce	Cerium	Ceres, a dwarf planet, considered a planet at the time	f-block groups	6	f-block	140.12	6.770	1068	3716	0.192	1.12	66.5	primordial	solid
    59	Pr	Praseodymium	Greek prásios dídymos, 'green twin'	f-block groups	6	f-block	140.91	6.77	1208	3793	0.193	1.13	9.2	primordial	solid
    60	Nd	Neodymium	Greek néos dídymos, 'new twin'	f-block groups	6	f-block	144.24	7.01	1297	3347	0.19	1.14	41.5	primordial	solid
    61	Pm	Promethium	Prometheus, a figure in Greek mythology	f-block groups	6	f-block	[145]	7.26	1315	3273	-	1.13	2×10⁻¹⁹	from decay	solid
    62	Sm	Samarium	Samarskite, a mineral named after V. Samarsky-Bykhovets, Russian mine official	f-block groups	6	f-block	150.36	7.52	1345	2067	0.197	1.17	7.05	primordial	solid
    63	Eu	Europium	Europe	f-block groups	6	f-block	151.96	5.244	1099	1802	0.182	1.2	2	primordial	solid
    64	Gd	Gadolinium	Gadolinite, a mineral named after Johan Gadolin, Finnish chemist, physicist and mineralogist	f-block groups	6	f-block	157.25	7.90	1585	3546	0.236	1.2	6.2	primordial	solid
    65	Tb	Terbium	Ytterby, Sweden, where it was found; see also yttrium, erbium, ytterbium	f-block groups	6	f-block	158.93	8.23	1629	3503	0.182	1.2	1.2	primordial	solid
    66	Dy	Dysprosium	Greek dysprósitos, 'hard to get'	f-block groups	6	f-block	162.50	8.540	1680	2840	0.17	1.22	5.2	primordial	solid
    67	Ho	Holmium	New Latin Holmia, 'Stockholm'	f-block groups	6	f-block	164.93	8.79	1734	2993	0.165	1.23	1.3	primordial	solid
    68	Er	Erbium	Ytterby, Sweden, where it was found; see also yttrium, terbium, ytterbium	f-block groups	6	f-block	167.26	9.066	1802	3141	0.168	1.24	3.5	primordial	solid
    69	Tm	Thulium	Thule, the ancient name for an unclear northern location	f-block groups	6	f-block	168.93	9.32	1818	2223	0.16	1.25	0.52	primordial	solid
    70	Yb	Ytterbium	Ytterby, Sweden, where it was found; see also yttrium, terbium, erbium	f-block groups	6	f-block	173.05	6.90	1097	1469	0.155	1.1	3.2	primordial	solid
    71	Lu	Lutetium	Latin Lutetia, 'Paris'	3	6	d-block	174.97	9.841	1925	3675	0.154	1.27	0.8	primordial	solid
    72	Hf	Hafnium	New Latin Hafnia, 'Copenhagen' (from Danish havn, harbour)	4	6	d-block	178.49	13.31	2506	4876	0.144	1.3	3	primordial	solid
    73	Ta	Tantalum	King Tantalus, father of Niobe from Greek mythology; see also niobium	5	6	d-block	180.95	16.69	3290	5731	0.14	1.5	2	primordial	solid
    74	W	Tungsten	Swedish tung sten, 'heavy stone' ·  Symbol W is from Wolfram, originally from Middle High German wolf-rahm 'wolf's foam' describing the mineral wolframite[5]	6	6	d-block	183.84	19.25	3695	5828	0.132	2.36	1.3	primordial	solid
    75	Re	Rhenium	Latin Rhenus, 'the Rhine'	7	6	d-block	186.21	21.02	3459	5869	0.137	1.9	7×10⁻⁴	primordial	solid
    76	Os	Osmium	Greek osmḗ, 'smell'	8	6	d-block	190.23	22.59	3306	5285	0.13	2.2	0.002	primordial	solid
    77	Ir	Iridium	Iris, the Greek goddess of the rainbow	9	6	d-block	192.22	22.56	2719	4701	0.131	2.20	0.001	primordial	solid
    78	Pt	Platinum	Spanish platina, 'little silver', from plata 'silver'	10	6	d-block	195.08	21.45	2041.4	4098	0.133	2.28	0.005	primordial	solid
    79	Au	Gold	English word, from the same root as 'yellow' ·  Symbol Au is derived from Latin aurum	11	6	d-block	196.97	19.3	1337.33	3129	0.129	2.54	0.004	primordial	solid
    80	Hg	Mercury	Mercury, Roman god of commerce, communication, and luck, known for his speed and mobility ·  Symbol Hg is derived from its Latin name hydrargyrum, from Greek hydrárgyros, 'water-silver'	12	6	d-block	200.59	13.534	234.43	629.88	0.14	2.00	0.085	primordial	liquid
    81	Tl	Thallium	Greek thallós, 'green shoot or twig'	13	6	p-block	204.38	11.85	577	1746	0.129	1.62	0.85	primordial	solid
    82	Pb	Lead	English word, from Proto-Celtic *ɸloudom, from a root meaning 'flow' ·  Symbol Pb is derived from Latin plumbum	14	6	p-block	207.2	11.34	600.61	2022	0.129	1.87 (2+) 2.33 (4+)	14	primordial	solid
    83	Bi	Bismuth	German Wismut, from weiß Masse 'white mass', unless from Arabic	15	6	p-block	208.98	9.78	544.7	1837	0.122	2.02	0.009	primordial	solid
    84	Po	Polonium	Latin Polonia, 'Poland', home country of Marie Curie	16	6	p-block	[209][a]	9.196	527	1235	-	2.0	2×10⁻¹⁰	from decay	solid
    85	At	Astatine	Greek ástatos, 'unstable'	17	6	p-block	[210]	(8.91-8.95)	575	610	-	2.2	3×10⁻²⁰	from decay	unknown phase
    86	Rn	Radon	Radium emanation, originally the name of the isotope Radon-222	18	6	p-block	[222]	0.00973	202	211.3	0.094	2.2	4×10⁻¹³	from decay	gas
    87	Fr	Francium	France, home country of discoverer Marguerite Perey	1	7	s-block	[223]	(2.48)	281	890	-	>0.79[6]	~1×10⁻¹⁸	from decay	unknown phase
    88	Ra	Radium	French radium, from Latin radius, 'ray'	2	7	s-block	[226]	5.5	973	2010	0.094	0.9	9×10⁻⁷	from decay	solid
    89	Ac	Actinium	Greek aktís, 'ray'	f-block groups	7	f-block	[227]	10	1323	3471	0.12	1.1	5.5×10⁻¹⁰	from decay	solid
    90	Th	Thorium	Thor, the Scandinavian god of thunder	f-block groups	7	f-block	232.04	11.7	2115	5061	0.113	1.3	9.6	primordial	solid
    91	Pa	Protactinium	Proto- (from Greek prôtos, 'first, before') + actinium, since actinium is produced through the radioactive decay of protactinium	f-block groups	7	f-block	231.04	15.37	1841	4300	-	1.5	1.4×10⁻⁶	from decay	solid
    92	U	Uranium	Uranus, the seventh planet in the Solar System	f-block groups	7	f-block	238.03	19.1	1405.3	4404	0.116	1.38	2.7	primordial	solid
    93	Np	Neptunium	Neptune, the eighth planet in the Solar System	f-block groups	7	f-block	[237]	20.45	917	4273	-	1.36	≤ 3×10⁻¹²	from decay	solid
    94	Pu	Plutonium	Pluto, a dwarf planet, considered a planet in the Solar System at the time	f-block groups	7	f-block	[244]	19.85	912.5	3501	-	1.28	≤ 3×10⁻¹¹	from decay	solid
    95	Am	Americium	The Americas, where the element was first synthesized, by analogy with its homologue § europium	f-block groups	7	f-block	[243]	12	1449	2880	-	1.13	-	synthetic	solid
    96	Cm	Curium	Pierre Curie and Marie Curie, French physicists and chemists	f-block groups	7	f-block	[247]	13.51	1613	3383	-	1.28	-	synthetic	solid
    97	Bk	Berkelium	Berkeley, California, where the element was first synthesized	f-block groups	7	f-block	[247]	14.78	1259	2900	-	1.3	-	synthetic	solid
    98	Cf	Californium	California, where the element was first synthesized in the LBNL laboratory	f-block groups	7	f-block	[251]	15.1	1173	(1743)[b]	-	1.3	-	synthetic	solid
    99	Es	Einsteinium	Albert Einstein, German physicist	f-block groups	7	f-block	[252]	8.84	1133	(1269)	-	1.3	-	synthetic	solid
    100	Fm	Fermium	Enrico Fermi, Italian physicist	f-block groups	7	f-block	[257]	(9.7)[b]	(1125)[7]	-	-	1.3	-	synthetic	unknown phase
    101	Md	Mendelevium	Dmitri Mendeleev, Russian chemist who proposed the periodic table	f-block groups	7	f-block	[258]	(10.3)	(1100)	-	-	1.3	-	synthetic	unknown phase
    102	No	Nobelium	Alfred Nobel, Swedish chemist and engineer	f-block groups	7	f-block	[259]	(9.9)	(1100)	-	-	1.3	-	synthetic	unknown phase
    103	Lr	Lawrencium	Ernest Lawrence, American physicist	3	7	d-block	[266]	(14.4)	(1900)	-	-	1.3	-	synthetic	unknown phase
    104	Rf	Rutherfordium	Ernest Rutherford, chemist and physicist from New Zealand	4	7	d-block	[267]	(17)	(2400)	(5800)	-	-	-	synthetic	unknown phase
    105	Db	Dubnium	Dubna, Russia, where the element was discovered in the JINR laboratory	5	7	d-block	[268]	(21.6)	-	-	-	-	-	synthetic	unknown phase
    106	Sg	Seaborgium	Glenn T. Seaborg, American chemist	6	7	d-block	[269]	(23-24)	-	-	-	-	-	synthetic	unknown phase
    107	Bh	Bohrium	Niels Bohr, Danish physicist	7	7	d-block	[270]	(26-27)	-	-	-	-	-	synthetic	unknown phase
    108	Hs	Hassium	New Latin Hassia, 'Hesse', a state in Germany	8	7	d-block	[269]	(27-29)	-	-	-	-	-	synthetic	unknown phase
    109	Mt	Meitnerium	Lise Meitner, Austrian physicist	9	7	d-block	[278]	(27-28)	-	-	-	-	-	synthetic	unknown phase
    110	Ds	Darmstadtium	Darmstadt, Germany, where the element was first synthesized in the GSI laboratories	10	7	d-block	[281]	(26-27)	-	-	-	-	-	synthetic	unknown phase
    111	Rg	Roentgenium	Wilhelm Conrad Röntgen, German physicist	11	7	d-block	[282]	(22-24)	-	-	-	-	-	synthetic	unknown phase
    112	Cn	Copernicium	Nicolaus Copernicus, Polish astronomer	12	7	d-block	[285]	(14.0)	(283±11)	(340±10)[b]	-	-	-	synthetic	unknown phase
    113	Nh	Nihonium	Japanese Nihon, 'Japan', where the element was first synthesized in the Riken laboratories	13	7	p-block	[286]	(16)	(700)	(1400)	-	-	-	synthetic	unknown phase
    114	Fl	Flerovium	Flerov Laboratory of Nuclear Reactions, part of JINR, where the element was synthesized; itself named after Georgy Flyorov, Russian physicist	14	7	p-block	[289]	(11.4±0.3)	(284±50)[b]	-	-	-	-	synthetic	unknown phase
    115	Mc	Moscovium	Moscow, Russia, where the element was first synthesized in the JINR laboratories	15	7	p-block	[290]	(13.5)	(700)	(1400)	-	-	-	synthetic	unknown phase
    116	Lv	Livermorium	Lawrence Livermore National Laboratory in Livermore, California	16	7	p-block	[293]	(12.9)	(700)	(1100)	-	-	-	synthetic	unknown phase
    117	Ts	Tennessine	Tennessee, United States, where Oak Ridge National Laboratory is located	17	7	p-block	[294]	(7.1-7.3)	(700)	(883)	-	-	-	synthetic	unknown phase
    118	Og	Oganesson	Yuri Oganessian, Russian physicist	18	7	p-block	[294]	(7)	(325±15)	(450±10)	-	-	-	synthetic	unknown phase
    """
    # Fields for Element named tuple
    # 0   Atomic number Z
    # 1   Symbol
    # 2   Name
    # 3   Origin of name
    # 4   Group
    # 5   Period
    # 6   Block
    # 7   Standard atomic weight, Da
    # 8   Density, g/cm3
    # 9   Melting point, K
    # 10  Boiling point, K
    # 11  Specific heat capacity, J/(g*K)
    # 12  Electronegativity (Pauling)
    # 13  Abundance in Earth's crust, ppm
    # 14  Origin
    # 15  Phase at 25 °C, 100 kPa
    Element = namedtuple(
        "Element",
        """
        Z
        sym
        name
        name_origin
        group
        period
        block
        aw_Da
        rho
        mp
        bp
        sp_ht
        en
        ppm
        origin
        phase
    """,
    )
    if 0:

        def Analyze(d):
            "Use to look at set of each element's contents"
            o = []
            for i in d:
                o.append(i.rho)
            k = list(set(o))
            print("   ".join(sorted(k)))
            """
            group:  integer except for 'f-block groups'
            period: int 1-7
            block:  d-block   f-block   p-block   s-block
            aw_Da:  floats except for [n] for synthetics
            rho:    floats, (x) = predicted, ± is uncertainty, a-b
            mp:     float, int, -, ± is uncertainty, -[k] (does not solidify at 1 atm), >4000
            bp:     float, () predicted, ±, -, ()[x] note
            sp_ht:  float, -
            en:     float, -, (2+), >0.79[6]
            ppm:    float, -, 1×10-4, ~ 1×10-18, ~, ≤ 3×10-11
            origin: from decay, primordial, synthetic
            phase:  gas, liquid, solid, unknown phase
            """

    def FixLine(line):
        """Fix lines that contain things like '[a]' by deleting such
        things in square brackets.
        """
        s = re.sub(r"\[[a-z]\]", "", line)
        s = re.sub(r"\[[0-9]\]", "", s)
        return s

    def GetElementNamedTuples():
        "Return a list of Element namedtuple objects"
        o = []
        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue
            line = FixLine(line)
            f = line.split("\t")
            assert len(f) == 16
            # Convert to integers
            for i in (0, 5):  # Z and period (row)
                f[i] = int(f[i])
            o.append(Element(*f))
        return o


if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(
                f"""
        This script is intended to let you see physical properties of the elements through the
        following features:
            
            - A list of properties printed to stdout with no arguments, one element per line.  This
              gives the symbol, name, number of protons, atomic weight, melting and boiling points,
              density, and abundance in the Earth's crust.  I use this mode the most frequently.
            - You can print the data for selected elements on the command line, identified by
              atomic number, symbol (case needs to be correct), or a regular expression.  The
              printed data are a little more extensive than the previous item.
            - The -o and -i options allow you to open the wikipedia web pages on the element and
              the element's isotopes, respectively, for the arguments on the command line.
 
        Short list
        ----------
 
        The default behavior is to print out data for the elements from 1 to 92, one line per
        element.  Things are color-coded to help with interpretation.
 
        The items that print out in the color for unknown phase exist in such tiny quantities that
        this property (and others) are impossible to measure with present technology, either
        because they are only found as decay products of other materials or they are artificially
        generated and not enough atoms are available to measure.
 
        Example [3]:  a sample of pure astatine has never been created because any macroscopic
        specimen would be vaporized by the heat of its own radioactivity.  Even so, small amounts
        of astatine are used in nuclear medicine research (see Uses section of [3]).
 
        The atomic weight is of course more properly called an atomic mass, but the use of "weight"
        is entrenched.  The unit is in daltons, a non-Si unit of mass equal to
        1.66053906660(50)×10−27 kg and is defined to be 1/12 of the mass of an unbound neutral atom
        of carbon 12.  A more sensible unit would be yg to be compatible with SI (and one wouldn't
        need to look up conversion factors), but like with things like the American Wire Gauge,
        we're stuck with these conventions.   
 
        Data
        ----
 
        This script uses data scraped from the web page [1] around the middle of February 2023.
        The table includes information on 118 elements.  Note that you won't see all 118 elements
        unless you use the -a option.
 
        A useful feature of [1]'s table is that the controls in the fourth row can be used to sort
        the table on the column's information.  For example, if you sort descending on abundance,
        you'll see that the most common elements in the Earth's crust are oxygen, silicon,
        aluminum, and iron.
 
        References
        ----------
 
          [1] https://en.wikipedia.org/wiki/List_of_chemical_elements
          [2] https://www.rsc.org/periodic-table
          [3] https://en.wikipedia.org/wiki/Astatine
 
        """.rstrip()
            )
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [el1 [el2 ...]]
          Print the properties of the matched elements.  The el strings can be the element's
          symbol, a regular expression for the name, or the atomic number.  There are {d["n"]}
          elements in the script.  If no arguments on the command line are given, the short list of
          elements is printed.  The data were screen scraped from the web page
          https://en.wikipedia.org/wiki/List_of_chemical_elements
        Notation:
          [223] means an atomic weight of a radioactive element
          (223) means a predicted number, not yet observed
          ~223  means an approximate number (difficult to measure)
          x±u   I assume means a value x with standard uncertainty u, but the web page used doesn't
          explicitly state this
        Options:
            -a      Show all elements (default is to show up to Z = 92)
            -c      Include colorizing even if stdout isn't a terminal
            -D      Dump data structures
            -d n    Set number of significant digits
            -i      Launch page on isotopes
            -H      Show manpage
            -h      Usage statement
            -l      Launch page on list of elements
            -n m    Allow up to m pages to be opened [{d["-n"]}]
            -o      Open wikipedia page on matched elements
            -t      Run self-tests
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show all elements
        d["-c"] = False  # Use color if stdout isn't terminal
        d["-D"] = False  # Dump data structures
        d["-d"] = 4  # Significant digits
        d["-H"] = False  # Manpage
        d["-h"] = False  # Usage
        d["-i"] = False  # Open isotopes page
        d["-l"] = False  # Launch page on list of elements
        d["-n"] = 5  # Number of allowed pages
        d["-o"] = False  # Open web page instead of printing to stdout
        d["-t"] = False  # Run self-tests
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acDd:Hhiln:ot")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acDHhilost"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-n":
                try:
                    n = int(a)
                    if n < 1:
                        raise ValueError
                except ValueError:
                    Error("-n argument must be an integer > 0")
        GetData()
        d["el"] = GetElementNamedTuples()
        d["n"] = len(g.num2sym)  # Number of elements in the script
        x = flt(0)
        x.N = d["-d"]
        # Set formatting for flts to use Unicode for scientific notation
        x.u = True
        if d["-c"]:
            t.always = True
        if d["-t"]:
            TestGetElements()
        if d["-l"]:
            LaunchWebPage("")
        if d["-h"]:
            Usage(status=0)
        if d["-H"]:
            Manpage()
        if not args:
            ShortList()
        return args


if 1:  # Core functionality

    def Uppercase(word):
        assert word
        return word[0].upper() + word[1:]

    def GetData():
        "Construct global dicts"
        for line in elements.strip().split("\n"):
            Name, Sym, num = [i.strip() for i in line.split()]
            num = int(num)
            sym = Sym.lower()
            name = Name.lower()
            # Dicts
            g.sym2num[sym] = num
            g.sym2num[Sym] = num
            g.num2sym[num] = sym
            g.num2Sym[num] = Sym
            g.num2Name[num] = Name
            g.num2name[num] = name
            g.Name2num[Name] = num
            g.name2num[name] = num
            #  Lists
            g.symbols.append(Sym)
            g.symbols.append(sym)
            g.names.append(Name)
            g.names.append(name)
        #  Set of capitalized element names
        g.all = set(i for i in g.names if i[0] in string.ascii_uppercase)
        if d["-D"]:  # Dump data structures

            def L(di):
                return list(di.items())[:2]

            print(f"{t.dbg}g.names    [list]: {g.names[:4]}")
            print(f"g.symbols  [list]: {g.symbols[:4]}")
            print()
            #
            print(f"g.sym2num  [dict]: {L(g.sym2num)}")
            #
            print(f"g.num2sym  [dict]: {L(g.num2sym)}")
            print(f"g.num2Sym  [dict]: {L(g.num2Sym)}")
            print(f"g.num2name [dict]: {L(g.num2name)}")
            print(f"g.num2Name [dict]: {L(g.num2Name)}")
            #
            print("All formal element names, capitalized:")
            t.print(f"  g.all       [set]: {list(g.all)[:2]}")
            print()
            exit(0)

    def LaunchWebPage(name):
        base = "https://en.wikipedia.org/wiki/"
        if d["-i"]:
            # Open the isotope page
            url = base + "Isotopes_of_" + name.lower()
        elif d["-l"]:
            # Open the list of elements page
            url = "https://en.wikipedia.org/wiki/List_of_chemical_elements"
        else:
            # Open the element page
            url = base + name
        webbrowser.open(url)

    def GetElements(el, test=False):
        """Return the name(s) of the indicated element as a list.
        Search strategy:
            - See if it's an integer, meaning an atomic number
            - See if it's an element symbol (1st character must be upper case)
            - See if it's a full element name
            - Search with it as a regex
        If test is True, always return a list, even if empty.
        """
        if not el.strip():
            return []
        try:  # Atomic number?
            atomic_number = int(el)
            name = g.num2Name[atomic_number]
            assert name in g.all
            return [name]
        except (ValueError, KeyError):
            if test:
                return []
        # Element symbol?
        if el[0] in string.ascii_uppercase:
            try:
                if el in g.symbols:
                    atomic_number = g.sym2num[el]
                    name = g.num2Name[atomic_number]
                    assert name in g.all
                    return [name]
            except KeyError:
                if test:
                    return []
        # Matches a full element name?
        if el in g.names:
            index = g.names.index(el)
            name = Uppercase(g.names[index])
            assert name in g.all
            return [name]
        # Use regular expression
        r = re.compile(el)
        names = []
        for name in g.names:
            mo = r.search(name)
            if mo and Uppercase(name) not in names:
                names.append(Uppercase(name))
        for name in names:
            assert name in g.all
        return names

    def TestGetElements():
        "Check that GetElements returns reasonable values"
        # Valid atomic number
        Assert(GetElements("1") == ["Hydrogen"])
        # Invalid atomic number
        Assert(GetElements("0", test=True) == [])
        # Valid symbol
        Assert(GetElements("H") == ["Hydrogen"])
        # Invalid symbol
        Assert(GetElements("Zz", test=True) == [])
        # Valid full element name
        Assert(GetElements("Hydrogen") == ["Hydrogen"])
        Assert(GetElements("hydrogen") == ["Hydrogen"])
        # Invalid full element name
        Assert(GetElements("Zydrogen") == [])
        # Valid regex
        Assert(GetElements("[YZ]") == ["Zinc", "Yttrium", "Zirconium", "Ytterbium"])
        # Invalid regex
        Assert(GetElements("Zydrogen") == [])
        Assert(GetElements("") == [])
        #
        print("Tests passed")
        exit(0)

    def DumpElements():
        for i in Columnize(sorted(g.found_names)):
            print(i)

    def ToFlt(s):
        try:
            return flt(s)
        except ValueError:
            return s

    def F(K):
        "Convert temperature in K to °F"
        assert ii(K, flt)
        return (K - 273.15) * 9 / 5 + 32

    def C(K):
        "Convert temperature in K to °C"
        assert ii(K, flt)
        return K - 273.15

    def PrintElement(Name):
        # Must subtract 1 because the array is 0-based
        num = g.Name2num[Name] - 1
        e = d["el"][num]
        i, w = " " * 4, 20
        Da2yg = 1.66053906660
        Da2kg = Da2yg * 1e-27
        print(f"{Name} ({e.sym})    Z = {e.Z}")
        # Atomic weight
        aw = ToFlt(e.aw_Da)
        if ii(aw, flt):
            # print(f"{i}{'Atomic weight':{w}s}{aw} Da = {aw*Da2kg} kg")
            # Print in yg
            print(f"{i}{'Atomic weight':{w}s}{aw} Da = {aw * Da2yg} yg")
        else:
            print(f"{i}{'Atomic weight':{w}s}{e.aw_Da} Da")
        # Density
        rho = ToFlt(e.rho)
        print(f"{i}{'Density':{w}s}{rho} g/cm³")
        # Melting point
        mp = ToFlt(e.mp)
        print(f"{i}{'Melting point':{w}s}{mp} K", end=" ")
        if ii(mp, flt):
            print(f"= {C(mp)} °C = {F(mp)} °F")
        else:
            print()
        # Boiling point
        bp = ToFlt(e.bp)
        print(f"{i}{'Boiling point':{w}s}{bp} K", end=" ")
        if ii(bp, flt):
            print(f"= {C(bp)} °C = {F(bp)} °F")
        else:
            print()
        # Specific heat
        sh = ToFlt(e.sp_ht)
        print(f"{i}{'Specific heat':{w}s}{sh} J/(g*K)")
        # Pauling electronegativity
        en = ToFlt(e.en)
        print(f"{i}{'Electronegativity':{w}s}{en}")
        # Abundance
        ppm = ToFlt(e.ppm)
        print(f"{i}{'Abundance (crust)':{w}s}{ppm} ppm")
        # Origin
        print(f"{i}{'Origin':{w}s}{e.origin}")
        # Phase
        print(f"{i}{'Phase':{w}s}{e.phase}")
        # Name origin
        s = e.name_origin.replace(" ·  ", " ")
        print(f"{i}{'Name origin':{w}s}{s}")
        # Group, period, block
        print(f"{i}{'Group':{w}s}{e.group}")
        print(f"{i}{'Period':{w}s}{e.period}")
        print(f"{i}{'Block':{w}s}{e.block}")

    def ShortList():
        "This is printed if there are no arguments.  One element per line."
        # Print header
        hdr = dedent("""
        Sym  Z      Name     AtWt, Da       mp/bp K         g/cm³      ppm
        --- -- ------------- --------- ----------------- ---------- ----------
        """)
        t.hdr = t("brnl")
        t.print(f"{t.hdr}{hdr}")
        # Get colors for phases
        dc = {
            "solid": t("wht"),
            "liquid": t("grnl"),
            "gas": t("denl"),
            "unknown phase": t("lipl"),
        }
        t.rad = t("redl")
        for i in d["el"]:
            num = i.Z
            if not d["-a"] and num > 92:
                continue
            c = dc[f"{i.phase}"]  # Phase color
            if i.aw_Da[0] == "[":
                s = f"{t.rad}{i.aw_Da:^9s}{t.n}"  # Radioactive atomic weight
            else:
                s = f"{i.aw_Da:^9s}"  # Regular atomic weight
            # symbol, Z, name, at. wt.
            print(f"{c}{i.sym:2s} {i.Z:3d} {i.name:13s} {s:^9s} {c}", end=" ")
            s = f"{i.mp}/{i.bp}"
            # Melting point/boiling point, density, ppm in crust
            print(f"{s:^17s} {i.rho:^11s} {i.ppm:^10s}{t.n}")
        # Print "reverse header"
        f = hdr.split("\n")
        t.print(f"{t.hdr}{f[1]}\n{f[0]}")
        # Color codes
        sol = dc["solid"]
        liq = dc["liquid"]
        gas = dc["gas"]
        unk = dc["unknown phase"]
        print(
            f"\nPhase colors:  {sol}solid{t.n} "
            f"{liq}liquid{t.n} {gas}gas{t.n} {unk}unknown{t.n} "
            "at 25 °C and 100 kPa"
        )
        print(f"{t.rad}[209]{t.n} means the atomic weight of the most stable isotope")
        print(f"(1125) means a predicted property")
        print(f"1 Da is 1.66054×10⁻²⁴ g (i.e., yg)")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    # Find all the element names referenced by the command line
    g.found_names = []
    for el in args:
        for name in GetElements(el):
            if name not in g.found_names:
                g.found_names.append(name)
    if d["-D"]:  # Dump for debugging
        print("Found the following elements:")
        DumpElements()
        exit(0)
    # Open the web pages
    if len(g.found_names) > d["-n"] and (d["-i"] or d["-o"]):
        n = len(g.found_names)
        t.print(f"{t.err}{n} is too many pages, refine your regex")
        exit(1)
    for name in g.found_names:
        if d["-o"] or d["-i"]:
            LaunchWebPage(name)
        else:
            PrintElement(name)

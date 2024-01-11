'''
Data on area of countries.  Two global tuples are wp_area_data
and cia_area_data from GetWPData() and GetCIAData().
'''
from f import flt
from f import flt
from io import StringIO
from pathlib import Path as P
import csv

def GetWPData():
    '''Return a tuple of tuples of the area in m² of earth and the countries
    of the world.  Each entry is (name, total_area, land_area, water_area).
 
    Screen-scraped from
    https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area
    Thu 11 Jan 2024 09:11:45 AM.  Corrections made with help of CIA().
 
    As always with wikipedia's data, you should check the values as there
    are often errors.  The only check I could make here was to see that the
    land and water values summed to the total value.  If there was a
    difference, the CIA World Factbook's value was used to correct things
    if it made sense.
 
    Corrections made ([CIA] = CIA World Factbook):
        - Brazil gave 8510346 as total, but land + water summed to 8515767,
          which nearly matches the 8515770 in [CIA].  I changed Brazil's
          total to 8515767.
        - Kazakhstan gave 2724910 as total, but land + water summed to
          2724900.  Total was changed to 2724900and matches [CIA].
        - DR Congo gave 2345410 as total, but land + water summed to
          2344858.  [CIA] gives 2344858, so that's what we'll use for total
          and 2344858 - 77810 = 2267048 for land.

    '''
    data='''
        –	 Earth	510,072,000 (196,940,000)	148,940,000 (57,506,000)	361,132,000 (139,434,000)	70.8	
        1	 Russia	17,098,246 (6,601,667)	16,378,410 (6,323,737)	719,836 (277,930)	4.2	[b]
        –	 Antarctica	14,200,000 (5,480,000)	14,200,000 (5,480,000)	0	0	[c]
        2	 Canada	9,984,670 (3,855,100)	9,093,507 (3,511,021)	891,163 (344,080)	8.9	[d]
        3	 China	9,596,960 (3,705,410)	9,326,410 (3,600,950)	270,550 (104,460)	2.8	[f]
        4	 United States	9,833,517 (3,796,741)	9,147,593 (3,531,904)	685,924 (264,837)	7.0	[g]
        5	 Brazil	8,515,767 (3,285,862)	8,460,415 (3,266,583)	55,352 (21,372)	0.6	[h]
        6	 Australia	7,741,220 (2,988,900)	7,682,300 (2,966,200)	58,920 (22,750)	0.8	[i]
        7	 India	3,287,263 (1,269,219)	2,973,190 (1,147,960)	314,073 (121,264)	9.6	[j]
        8	 Argentina	2,780,400 (1,073,500)	2,736,690 (1,056,640)	43,710 (16,880)	1.6	[k]
        9	 Kazakhstan	2,724,900 (1,052,090)	2,699,700 (1,042,400)	25,200 (9,730)	0.9	[l]
        10	 Algeria	2,381,741 (919,595)	2,381,741 (919,595)	0	0	[m]
        11	 DR Congo	2,344,858 (905,567)	2,267,048 (875,312)	77,810 (30,040)	3.3	[n]
        –	 Kingdom of Denmark	2,210,426 (853,450)	2,220,072 (857,174)	21 (8)	0	[o]
        12	 Saudi Arabia	2,206,714 (852,017)	2,149,690 (830,000)	0	0	[p]
        –	 Greenland (Denmark)	2,166,086 (836,330)	2,166,086 (836,330)	0	0	[q]
        13	 Mexico	1,964,375 (758,449)	1,943,945 (750,561)	20,430 (7,888)	1.0	[r]
        14	 Indonesia	1,910,931 (737,814)	1,811,569 (699,450)	93,000 (36,000)	4.9	[s]
        15	 Sudan	1,861,484 (718,723)	1,731,671 (668,602)	129,813 (50,121)	7.0	[t]
        16	 Libya	1,676,198 (647,183)	1,759,540 (679,362)	0	0	
        17	 Iran	1,648,195 (636,371)	1,531,595 (591,352)	116,600 (45,020)	7.1	[u]
        18	 Mongolia	1,564,116 (603,908)	1,553,556 (599,831)	10,560 (4,077)	0.7	[v]
        19	 Peru	1,285,216 (496,224)	1,279,996 (494,209)	5,220 (2,020)	0.4	[w]
        20	 Chad	1,284,000 (495,800)	1,259,200 (486,180)	24,800 (9,580)	1.9	[x]
        21	 Niger	1,267,000 (489,200)	1,266,700 (489,080)	300 (100)	0	[y]
        22	 Angola	1,246,700 (481,350)	1,246,700 (481,350)	0	0	
        23	 Mali	1,240,192 (478,841)	1,220,190 (471,118)	20,002 (7,723)	1.6	
        24	 South Africa	1,221,037 (471,445)	1,214,470 (468,909)	4,620 (1,780)	0.4	[z]
        25	 Colombia	1,138,910 (439,735)	1,038,700 (401,040)	100,210 (38,691)	8.8	[aa]
        26	 Ethiopia	1,104,300 (426,370)	1,096,630 (423,411)	7,670 (2,960)	0.7	[ab]
        27	 Bolivia	1,098,581 (424,164)	1,083,300 (418,260)	15,280 (5,900)	1.4	
        28	 Mauritania	1,030,700 (397,960)	1,025,520 (395,955)	4,480 (1,730)	0.4	
        29	 Egypt	1,002,000 (386,900)	995,450 (384,350)	6,000 (2,000)	0.6	[ac]
        30	 Tanzania	947,303 (365,756)	885,800 (342,000)	61,500 (23,700)	6.5	
        31	 Nigeria	923,768 (356,669)	910,768 (351,649)	13,000 (5,000)	1.4	
        32	 Venezuela	912,050 (352,140)	882,050 (340,560)	30,000 (10,000)	3.3	[ad]
        33	 Pakistan	881,913 (340,508)	856,690 (330,770)	25,223 (9,739)	2.9	[ae]
        34	 Namibia	825,615 (318,772)	823,290 (317,870)	2,425 (936)	0.3	
        35	 Mozambique	801,590 (309,500)	786,380 (303,620)	13,000 (5,000)	1.6	
        36	 Turkey	783,562 (302,535)	769,632 (297,156)	13,930 (5,378)	1.8	[af]
        37	 Chile	756,102 (291,932)	743,812 (287,187)	12,290 (4,745)	1.6	[ag]
        38	 Zambia	752,612 (290,585)	743,398 (287,027)	9,220 (3,560)	1.2	
        39	 Myanmar	676,577 (261,228)	653,508 (252,321)	23,070 (8,907)	3.4	[ah]
        40	 Afghanistan	652,864 (252,072)	652,230 (251,830)	630 (240)	0.1	
        41	 South Sudan	644,329 (248,777)	644,329 (248,777)	0	0	[aa]
        42	 France	643,801 (248,573)	640,427 (247,270)	3,374 (1,303)	0.5	[ai]
        43	 Somalia	637,657 (246,201)	627,337 (242,216)	10,320 (3,985)	1.6	[aj]
        44	 Central African Republic	622,984 (240,535)	622,984 (240,535)	0	0	
        45	 Ukraine	603,500 (233,000)	579,300 (223,700)	24,250 (9,363)	4.0	[ak]
        46	 Kenya	591,958 (228,556)	569,140 (219,750)	11,227 (4,335)	1.9	
        47	 Madagascar	587,041 (226,658)	581,540 (224,530)	5,501 (2,124)	0.9	[al]
        48	 Botswana	582,000 (225,000)	566,730 (218,820)	15,000 (5,800)	2.6	[aa]
        –	 France (metropolitan)	543,940 (210,020)				[am]
        49	 Yemen	527,968 (203,850)	527,968 (203,850)	0	0	[an]
        50	 Thailand	513,140 (198,120)	510,890 (197,260)	2,230 (861)	0.4	[ao]
        51	 Spain	506,009 (195,371)	498,980 (192,660)	6,390 (2,470)	1.3	[ap]
        52	 Turkmenistan	488,100 (188,500)	469,930 (181,440)	18,170 (7,015)	3.7	
        53	 Cameroon	475,650 (183,650)	472,710 (182,510)	2,730 (1,050)	0.6	[aa]
        54	 Papua New Guinea	462,840 (178,700)	452,860 (174,850)	9,980 (3,850)	2.2	[aq]
        55	 Uzbekistan	448,969 (173,348)	425,400 (164,200)	22,000 (8,500)	4.9	
        56	 Sweden	447,425 (172,752)	407,284 (157,253)	40,142 (15,499)	9.0	[ar]
        57	 Morocco	446,550 (172,410)	446,300 (172,300)	250 (97)	0.1	[as]
        58	 Iraq	438,317 (169,235)	437,367 (168,868)	950 (370)	0.2	[at]
        59	 Paraguay	406,752 (157,048)	397,302 (153,399)	9,450 (3,650)	2.3	
        60	 Zimbabwe	390,757 (150,872)	386,847 (149,362)	3,910 (1,510)	1.0	
        61	 Norway	385,207 (148,729)	365,957 (141,297)	19,520 (7,537)	5.1	[au]
        62	 Japan	377,976 (145,937)	364,546 (140,752)	13,430 (5,185)	3.6	[av]
        63	 Germany	357,581 (138,063)	348,672 (134,623)	8,350 (3,220)	2.3	[aw]
        64	 Congo	342,000 (132,000)	341,500 (131,900)	500 (200)	0.1	
        65	 Finland	338,145 (130,558)	303,816 (117,304)	34,330 (13,260)	10.1	[ax]
        66	 Vietnam	331,345 (127,933)	310,070 (119,720)	21,140 (8,162)	6.4	
        67	 Malaysia	330,621 (127,653)	329,613 (127,264)	1,190 (459)	0.4	
        –	 Norway (mainland)	323,802 (125,021)	304,282 (117,484)	19,520 (7,537)	6.0	[ay]
        68	 Ivory Coast	322,462 (124,503)	318,003 (122,782)	4,460 (1,720)	1.4	
        69	 Poland	312,679 (120,726)	311,888 (120,421)	791 (305)	0.3	
        70	 Oman	309,980 (119,680)	309,500 (119,500)	0	0	
        71	 Italy	302,068 (116,629)	294,140 (113,570)	7,200 (2,800)	2.4	
        72	 Philippines	300,000 (100,000)	298,170 (115,120)	1,830 (707)	0.61	[aa]
        73	 Ecuador	283,561 (109,483)	276,841 (106,889)	6,720 (2,600)	2.4	[az]
        74	 Burkina Faso	274,200 (105,900)	273,800 (105,700)	400 (200)	0.2	[aa]
        75	 New Zealand	268,107 (103,517)	262,443 (101,330)	4,395 (1,697)	1.6	[ba]
        76	 Gabon	267,668 (103,347)	257,667 (99,486)	10,001 (3,861)	3.7	
        –	 Western Sahara	266,000 (103,000)	266,000 (103,000)	0	0	[bb]
        77	 Guinea	245,836 (94,918)	245,717 (94,872)	140 (54)	0.1	
        78	 United Kingdom	242,495 (93,628)	241,930 (93,410)	1,680 (649)	0.7	[bc]
        79	 Uganda	241,550 (93,263)	197,100 (76,100)	43,938 (16,965)	18.2	
        80	 Ghana	238,537 (92,100)	228,567 (88,250)	11,000 (4,200)	4.6	
        81	 Romania	238,398 (92,046)	231,291 (89,302)	7,100 (2,700)	3.0	
        82	 Laos	236,800 (91,430)	230,800 (89,110)	6,000 (2,000)	2.5	[bd]
        83	 Guyana	214,969 (83,000)	196,849 (76,004)	18,120 (6,996)	8.4	
        84	 Belarus	207,600 (80,160)	202,900 (78,340)	4,700 (1,800)	2.3	[be]
        85	 Kyrgyzstan	199,949 (77,201)	191,801 (74,055)	8,150 (3,150)	4.1	
        86	 Senegal	196,712 (75,951)	192,530 (74,336)	4,192 (1,619)	2.1	
        87	 Syria	185,180 (71,498)	183,630 (70,900)	1,550 (598)	0.8	[bf]
        88	 Cambodia	181,035 (69,898)	176,520 (68,155)	4,520 (1,750)	2.5	
        –	 Somaliland	177,000 (68,300)				[bg]
        89	 Uruguay	173,626 (67,037)	175,015 (67,574)	1,200 (460)	0.7	
        90	 Suriname	163,820 (63,251)	156,000 (60,200)	7,820 (3,020)	4.8	[bh]
        91	 Tunisia	163,610 (63,170)	155,360 (59,985)	8,250 (3,190)	5.0	
        92	 Bangladesh	148,460 (57,321)	130,170 (50,259)	18,290 (7,062)	12.3	[bi]
        93	   Nepal	147,181 (56,827)	143,686 (55,477)	3,830 (1,480)	2.6	[bj]
        94	 Tajikistan	141,400 (54,600)	141,510 (54,637)	2,590 (1,000)	1.8	
        95	 Greece	131,957 (50,949)	130,647 (50,443)	1,310 (506)	1.0	[bk]
        96	 Nicaragua	130,373 (50,337)	119,990 (46,328)	10,380 (4,008)	8.0	[bl]
        97	 Eritrea	121,144 (46,774)	124,330 (48,004)	0	0	
        98	 North Korea	120,538 (46,540)	120,538 (46,540)	2 (1)	0	[bm]
        99	 Benin	114,763 (44,310)	112,760 (43,537)	2,000 (800)	1.7	
        100	 Honduras	112,492 (43,433)	111,890 (43,201)	200 (80)	0.2	
        101	 Liberia	111,369 (43,000)	96,320 (37,190)	15,049 (5,810)	13.5	
        102	 Bulgaria	110,879 (42,811)	108,489 (41,888)	2,390 (923)	2.2	[bn]
        103	 Cuba	109,884 (42,426)	103,800 (40,080)	6,080 (2,350)	5.5	[bo]
        104	 Guatemala	108,889 (42,042)	107,159 (41,374)	1,730 (668)	1.6	
        105	 Iceland	103,000 (39,800)	100,250 (38,707)	2,750 (1,060)	2.7	
        106	 South Korea	100,432 (38,777)	99,909 (38,575)	301 (116)	0.3	[bp]
        107	 Malawi	94,552 (36,507)	94,080 (36,320)	24,404 (9,422)	20.6	[bq]
        108	 Hungary	93,025 (35,917)	89,608 (34,598)	3,420 (1,320)	3.7	
        109	 Portugal	92,225 (35,608)	91,119 (35,181)	1,107 (427)	1.2	
        110	 Jordan	89,318 (34,486)	88,802 (34,287)	540 (210)	0.6	
        111	 Serbia	88,444 (34,148)	88,384 (34,125)	115 (44)	0.1	[br]
        112	 Azerbaijan	86,600 (33,400)	82,650 (31,910)	3,950 (1,530)	4.6	[bs]
        113	 Austria	83,878 (32,385)	82,520 (31,860)	1,359 (525)	1.6	
        114	 Czech Republic	78,871 (30,452)	77,187 (29,802)	1,684 (650)	2.1	
        115	 Panama	75,320 (29,080)	74,340 (28,700)	1,080 (417)	1.4	[bt]
        116	 Sierra Leone	72,300 (27,900)	71,620 (27,650)	120 (46)	0.2	
        117	 United Arab Emirates	71,024 (27,423)	83,600 (32,300)	0	0	
        118	 Ireland	69,825 (26,960)	68,883 (26,596)	1,390 (537)	2.0	[bu]
        119	 Georgia	69,700 (26,900)	69,700 (26,900)	0	0	[bv]
        120	 Sri Lanka	65,610 (25,330)	62,732 (24,221)	2,878 (1,111)	4.4	
        121	 Lithuania	65,286 (25,207)	62,680 (24,200)	2,620 (1,010)	4.0	
        122	 Latvia	64,594 (24,940)	62,249 (24,034)	2,340 (903)	3.6	
        –	 Svalbard (Norway)	62,045 (23,956)	62,045 (23,956)	0	0	[bw]
        123	 Togo	56,785 (21,925)	54,385 (20,998)	2,400 (930)	4.2	
        124	 Croatia	56,594 (21,851)	55,974 (21,612)	620 (240)	1.1	[aa]
        125	 Bosnia and Herzegovina	51,209 (19,772)	51,200 (19,800)	10 (4)	0.0	
        126	 Costa Rica	51,100 (19,700)	51,060 (19,710)	40 (20)	0.1	
        127	 Slovakia	49,035 (18,933)	48,105 (18,573)	930 (360)	1.9	
        128	 Dominican Republic	48,671 (18,792)	48,320 (18,660)	350 (140)	0.7	
        129	 Estonia	45,339 (17,505)	42,388 (16,366)	2,840 (1,100)	6.3	
        130	 Denmark	42,947 (16,582)	42,434 (16,384)	660 (260)	1.5	[bx]
        131	 Netherlands	41,865 (16,164)	33,893 (13,086)	7,957 (3,072)	19.0	[by]
        132	  Switzerland	41,277 (15,937)	39,997 (15,443)	1,280 (494)	3.1	[aa]
        133	 Bhutan	38,394 (14,824)	38,140 (14,730)	250 (97)	0.7	
        –	 Taiwan	36,193 (13,974)	32,260 (12,460)	3,720 (1,440)	10.3	[bz]
        134	 Guinea-Bissau	36,125 (13,948)	28,120 (10,860)	8,005 (3,091)	22.2	
        135	 Moldova	33,847 (13,068)	32,891 (12,699)	960 (370)	2.8	[ca]
        136	 Belgium	30,528 (11,787)	30,280 (11,690)	250 (97)	0.8	
        137	 Lesotho	30,355 (11,720)	30,355 (11,720)	0	0	
        138	 Armenia	29,743 (11,484)	28,470 (10,990)	1,270 (490)	4.3	
        139	 Solomon Islands	28,896 (11,157)	27,986 (10,805)	910 (350)	3.1	
        140	 Albania	28,748 (11,100)	27,400 (10,600)	330 (130)	1.1	
        141	 Equatorial Guinea	28,051 (10,831)	28,051 (10,831)	0	0	
        142	 Burundi	27,834 (10,747)	25,680 (9,915)	2,150 (830)	7.7	
        143	 Haiti	27,750 (10,710)	27,560 (10,640)	190 (73)	0.7	
        144	 Rwanda	26,338 (10,169)	24,668 (9,524)	1,670 (645)	6.3	
        145	 North Macedonia	25,713 (9,928)	25,433 (9,820)	280 (110)	1.1	
        146	 Djibouti	23,200 (8,960)	23,180 (8,950)	20 (8)	0.1	
        147	 Belize	22,965 (8,867)	22,810 (8,807)	160 (62)	0.7	
        148	 Israel	21,937 (8,470)	21,497 (8,300)	440 (170)	2.1	[cb]
        149	 El Salvador	21,041 (8,124)	20,721 (8,000)	320 (120)	1.5	[cc]
        150	 Slovenia	20,273 (7,827)	20,151 (7,780)	120 (46)	0.6	
        –	 New Caledonia (France)	19,100 (7,380)	18,275 (7,056)	300 (100)	1.6	
        151	 Fiji	18,272 (7,055)	18,274 (7,056)	0	0	
        152	 Kuwait	17,818 (6,880)	17,818 (6,880)	0	0	
        153	 Eswatini	17,363 (6,704)	17,204 (6,642)	160 (62)	0.9	
        154	 East Timor	14,954 (5,774)	14,874 (5,743)	0	0	
        155	 Bahamas	13,880 (5,359)	10,010 (3,865)	3,870 (1,490)	27.8	
        156	 Montenegro	13,888 (5,362)	13,452 (5,194)	360 (140)	2.6	
        157	 Vanuatu	12,189 (4,706)	12,189 (4,706)	0	0	
        –	 Falkland Islands (UK)	12,173 (4,700)	12,173 (4,700)	0	0	
        158	 Qatar	11,637 (4,493)	11,586 (4,473)	0	0	
        159	 Gambia	11,295 (4,361)	10,000 (4,000)	1,295 (500)	11.5	[cd]
        160	 Jamaica	10,991 (4,244)	10,831 (4,182)	160 (62)	1.5	
        –	 Kosovo	10,887 (4,203)				[26]
        161	 Lebanon	10,452 (4,036)	10,230 (3,950)	170 (66)	1.6	[ce]
        162	 Cyprus	9,251 (3,572)	9,241 (3,568)	10 (4)	0.1	[cf]
        –	 Puerto Rico (US)	8,868 (3,424)	8,959 (3,459)	145 (56)	1.6	[cg]
        –	 Abkhazia	8,665 (3,346)				[ch]
        –	 French Southern Territories (France)	7,747 (2,991)	7,668 (2,961)	80 (30)	1.0	[ci]
        163	 Palestine	6,220 (2,400)	6,000 (2,000)	220 (85)	3.5	[cj]
        164	 Brunei	5,765 (2,226)	5,270 (2,040)	500 (200)	8.7	
        165	 Trinidad and Tobago	5,127 (1,980)	5,128 (1,980)	0	0	
        –	 Transnistria	4,163 (1,607)				[ck]
        166	 Cape Verde	4,033 (1,557)	4,033 (1,557)	0	0	
        –	 South Georgia and the South Sandwich Islands (UK)	3,903 (1,507)	3,903 (1,507)	0	0	[aa]
        –	 South Ossetia	3,900 (1,500)				[cl]
        –	 French Polynesia (France)	3,687 (1,424)	3,827 (1,478)	340 (130)	8.2	
        –	 Northern Cyprus	3,355 (1,295)				[cm]
        167	 Samoa	2,842 (1,097)	2,821 (1,089)	10 (4)	0.4	
        –	 Hong Kong (China)	2,755 (1,064)	1,106 (427)	1,649 (637)	59.9	[28]
        168	 Luxembourg	2,586 (998)	2,586 (998)	0	0	[cn]
        –	 Bir Tawil (terra nullius)	2,060 (795)	2,060 (795)	0	0	
        169	 Mauritius	2,040 (788)	2,030 (784)	10 (4)	0.5	[co]
        170	 Comoros	1,861 (719)	1,861 (719)	0	0	[cp]
        –	 Åland (Finland)	1,581 (610)	1,553 (600)	28 (11)	1.8	[cq]
        –	 Faroe Islands (Denmark)	1,393 (538)	1,393 (538)	0	0	[aa]
        171	 São Tomé and Príncipe	964 (372)	964 (372)	0	0	
        –	 Turks and Caicos Islands (UK)	948 (366)	430 (170)	0	0	[cr]
        172	 Kiribati	811 (313)	811 (313)	0	0	[cs]
        173	 Bahrain	778 (300)	778 (300)	0	0	[ct]
        174	 Dominica	750 (290)	751 (290)	0	0	
        175	 Tonga	747 (288)	717 (277)	30 (10)	4.0	
        176	 Singapore	733 (283)	716 (276)	10 (4)	1.4	
        177	 Micronesia	702 (271)	702 (271)	0	0	
        178	 Saint Lucia	616 (238)	606 (234)	10 (4)	1.6	
        –	 Isle of Man (UK)	572 (221)	572 (221)	0	0	
        –	 Guam (US)	541 (209)	544 (210)	0	0	
        179	 Andorra	468 (181)	468 (181)	0	0	[cu]
        180	 Palau	459 (177)	459 (177)	0	0	
        –	 Northern Mariana Islands (US)	457 (176)	464 (179)	0	0	
        181	 Seychelles	457 (176)	455 (176)	0	0	[cv]
        –	 Curaçao (Netherlands)	444 (171)	444 (171)	0	0	[by]
        182	 Antigua and Barbuda	442 (171)	442 (171)	0	0	
        183	 Barbados	431 (166)	431 (166)	0	0	
        –	 Heard Island and McDonald Islands (Australia)	412 (159)	412 (159)	0	0	[aa]
        184	 Saint Vincent and the Grenadines	389 (150)	389 (150)	0	0	
        –	 Jan Mayen (Norway)	377 (146)	377 (146)	0	0	
        –	 U.S. Virgin Islands (US)	347 (134)	346 (134)	0	0	[aa]
        185	 Grenada	345 (133)	344 (133)	0	0	
        186	 Malta	315 (122)	316 (122)	0	0	[cw]
        –	 Saint Helena, Ascension and Tristan da Cunha (UK)	309 (119)	308 (119)	0	0	[cx]
        187	 Maldives	300 (100)	298 (115)	0	0	[cy]
        –	 Bonaire (Netherlands)	288 (111)	288 (111)	0	0	[by]
        –	 Cayman Islands (UK)	264 (102)	240 (93)	24 (9)	0	
        188	 Saint Kitts and Nevis	261 (101)	261 (101)	0	0	[cz]
        –	 Niue	260 (100)	260 (100)	0	0	[da]
        –	 Akrotiri and Dhekelia (UK)	254 (98)				[db]
        –	 Saint Pierre and Miquelon (France)	242 (93)	242 (93)	0	0	
        –	 Cook Islands	236 (91)	236 (91)	0	0	[dc]
        –	 American Samoa (US)	199 (77)	199 (77)	0	0	
        189	 Marshall Islands	181 (70)	181 (70)	0	0	
        –	 Aruba (Netherlands)	180 (69)	180 (69)	0	0	[by]
        –	 Easter Island (Chile)	163 (63)	163 (63)	0	0	
        190	 Liechtenstein	160 (62)	160 (62)	0	0	[dd]
        –	 British Virgin Islands (UK)	151 (58)	151 (58)	0	0	
        –	 Wallis and Futuna (France)	142 (55)	142 (55)	0	0	
        –	 Christmas Island (Australia)	135 (52)	135 (52)	0	0	[aa]
        –	 Jersey (UK)	116 (45)	116 (45)	0	0	[aa]
        –	 Montserrat (UK)	103 (40)	102 (39)	0	0	
        –	 Anguilla (UK)	91 (35)	91 (35)	0	0	
        –	 Guernsey (UK)	78 (30)	78 (30)	0	0	[aa]
        191	 San Marino	61 (24)	61 (24)	0	0	[de]
        –	 British Indian Ocean Territory (UK)	60 (20)	60 (20)	0	0	[aa]
        –	 Bermuda (UK)	54 (21)	54 (21)	0	0	
        –	 Saint Martin (France)	53 (20)	53 (20)	0	0	
        –	 Bouvet Island (Norway)	49 (19)	49 (19)	0	0	[aa]
        –	 Pitcairn Islands (UK)	47 (18)	47 (18)	0	0	[df]
        –	 Norfolk Island (Australia)	36 (14)	36 (14)	0	0	
        –	 Sint Maarten (Netherlands)	34 (13)	34 (13)	0	0	[by]
        –	 Macao (China)	31 (12)	28 (11)	0	0	[dg]
        192	 Tuvalu	26 (10)	26 (10)	0	0	[dh]
        –	 Saint Barthélemy (France)	22 (8)	22 (8)	0	0	
        193	 Nauru	21 (8)	21 (8)	0	0	[di]
        –	 Sint Eustatius (Netherlands)	21 (8)				[by]
        –	 U.S. Minor Outlying Islands (US)	19 (7)	19 (7)	0	0	[dj]
        –	 Cocos (Keeling) Islands (Australia)	14 (5)	14 (5)	0	0	[aa]
        –	 Saba (Netherlands)	13 (5)				[by]
        –	 Tokelau (New Zealand)	12 (5)	12 (5)	0	0	
        –	 Gibraltar (UK)	6.8 (2.6)	6.8 (2.6)	0	0	[dk]
        –	 Clipperton Island (France)	6.0 (2.3)	2.0 (0.77)	4.0 (1.5)	66.7	[dl]
        –	 Ashmore and Cartier Islands (Australia)	5.0 (1.9)	5.0 (1.9)	0	0	[aa]
        –	 Coral Sea Islands (Australia)	3.0 (1.2)	3.0 (1.2)	0	0	[dm]
        –	 Spratly Islands (disputed)	2.0 (0.77)	2.0 (0.77)	0	0	
        194	 Monaco	2.0 (0.77)	2.0 (0.77)	0	0	[dn]
        195	 Vatican City	0.49 (0.19)	0.49 (0.19)	0	0	[do]
    '''
    def Num(s):
        '''Will be something like '3.0 (1.2)'.  Remove the number in
        parentheses and return a flt that is area in km².
        '''
        if not s:
            return flt(0)
        return flt(s.replace(",", "").split()[0])
    o = []
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue
        f = line.split("\t")
        f.pop(0)    # Remove rank number
        if "[" in f[-1]:
            f.pop(-1)   # Remove last item if it's a reference
        f.pop(-1)   # Remove percentage
        # Fix the fields
        f[0] = f[0].strip()     # No spaces around name
        for i in (1, 2, 3):
            f[i] = Num(f[i])    # Convert to flt numbers
        # Check that land and water areas add to total
        if f[1] != f[2] + f[3]:
            # Note these units are km²
            name = f[0]
            total, land, water = [int(i) for i in f[1:]]
            print(f"Bad data for {name}:")
            print(f"  Total           = {total:15d}")
            print(f"    Land + water  = {land + water:15d}")
            print(f"    Diff          = {total - (land + water):15d}")
            print(f"  Land            = {land:15d}")
            print(f"  Water           = {water:15d}")
            print(f"  Total - water   = {total - water:15d}")
            print(f"  Total - land    = {total - land:15d}")
            exit(1)
        o.append(f)
    # Convert areas to m²
    for item in o:
        for i in (1, 2, 3):
            item[i] *= 1e6
    breakpoint() #xx

def GetCIAData(show=False):
    '''Return a tuple of tuples of CIA World Factbook information on the
    areas of countries.  If show is True, print the data to stdout.
    Each tuple is (name, region, area) where area is a flt in square
    meters.
 
    World Factbook https://www.cia.gov/the-world-factbook/ dated 11 Jan
    2024.  The page used was
    https://www.cia.gov/the-world-factbook/field/area/country-comparison/
    (this page has a download button for a CSV file).
    '''
    data = '''
    name,slug,sq km,date_of_information,ranking,region
    "Russia","russia","17,098,242","",1,"Central Asia"
    "Antarctica","antarctica","14,200,000","",2,"Antarctica"
    "Canada","canada","9,984,670","",3,"North America"
    "United States","united-states","9,833,517","",4,"North America"
    "China","china","9,596,960","",5,"East and Southeast Asia"
    "Brazil","brazil","8,515,770","",6,"South America"
    "Australia","australia","7,741,220","",7,"Australia and Oceania"
    "India","india","3,287,263","",8,"South Asia"
    "Argentina","argentina","2,780,400","",9,"South America"
    "Kazakhstan","kazakhstan","2,724,900","",10,"Central Asia"
    "Algeria","algeria","2,381,740","",11,"Africa"
    "Congo, Democratic Republic of the","congo-democratic-republic-of-the","2,344,858","",12,"Africa"
    "Greenland","greenland","2,166,086","",13,"North America"
    "Saudi Arabia","saudi-arabia","2,149,690","",14,"Middle East"
    "Mexico","mexico","1,964,375","",15,"North America"
    "Indonesia","indonesia","1,904,569","",16,"East and Southeast Asia"
    "Sudan","sudan","1,861,484","",17,"Africa"
    "Libya","libya","1,759,540","",18,"Africa"
    "Iran","iran","1,648,195","",19,"Middle East"
    "Mongolia","mongolia","1,564,116","",20,"East and Southeast Asia"
    "Peru","peru","1,285,216","",21,"South America"
    "Chad","chad","1,284,000","",22,"Africa"
    "Niger","niger","1,267,000","",23,"Africa"
    "Angola","angola","1,246,700","",24,"Africa"
    "Mali","mali","1,240,192","",25,"Africa"
    "South Africa","south-africa","1,219,090","",26,"Africa"
    "Colombia","colombia","1,138,910","",27,"South America"
    "Ethiopia","ethiopia","1,104,300","",28,"Africa"
    "Bolivia","bolivia","1,098,581","",29,"South America"
    "Mauritania","mauritania","1,030,700","",30,"Africa"
    "Egypt","egypt","1,001,450","",31,"Africa"
    "Tanzania","tanzania","947,300","",32,"Africa"
    "Nigeria","nigeria","923,768","",33,"Africa"
    "Venezuela","venezuela","912,050","",34,"South America"
    "Namibia","namibia","824,292","",35,"Africa"
    "Mozambique","mozambique","799,380","",36,"Africa"
    "Pakistan","pakistan","796,095","",37,"South Asia"
    "Turkey (Turkiye)","turkey-turkiye","783,562","",38,"Middle East"
    "Chile","chile","756,102","",39,"South America"
    "Zambia","zambia","752,618","",40,"Africa"
    "Morocco","morocco","716,550","",41,"Africa"
    "Burma","burma","676,578","",42,"East and Southeast Asia"
    "Afghanistan","afghanistan","652,230","",43,"South Asia"
    "South Sudan","south-sudan","644,329","",44,"Africa"
    "France","france","643,801","",45,"Europe"
    "Somalia","somalia","637,657","",46,"Africa"
    "Central African Republic","central-african-republic","622,984","",47,"Africa"
    "Ukraine","ukraine","603,550","",48,"Europe"
    "Madagascar","madagascar","587,041","",49,"Africa"
    "Botswana","botswana","581,730","",50,"Africa"
    "Kenya","kenya","580,367","",51,"Africa"
    "Yemen","yemen","527,968","",52,"Middle East"
    "Thailand","thailand","513,120","",53,"East and Southeast Asia"
    "Spain","spain","505,370","",54,"Europe"
    "Turkmenistan","turkmenistan","488,100","",55,"Central Asia"
    "Cameroon","cameroon","475,440","",56,"Africa"
    "Papua New Guinea","papua-new-guinea","462,840","",57,"East and Southeast Asia"
    "Sweden","sweden","450,295","",58,"Europe"
    "Uzbekistan","uzbekistan","447,400","",59,"Central Asia"
    "Iraq","iraq","438,317","",60,"Middle East"
    "Paraguay","paraguay","406,752","",61,"South America"
    "Zimbabwe","zimbabwe","390,757","",62,"Africa"
    "Japan","japan","377,915","",63,"East and Southeast Asia"
    "Germany","germany","357,022","",64,"Europe"
    "Congo, Republic of the","congo-republic-of-the","342,000","",65,"Africa"
    "Finland","finland","338,145","",66,"Europe"
    "Vietnam","vietnam","331,210","",67,"East and Southeast Asia"
    "Malaysia","malaysia","329,847","",68,"East and Southeast Asia"
    "Norway","norway","323,802","",69,"Europe"
    "Cote d'Ivoire","cote-divoire","322,463","",70,"Africa"
    "Poland","poland","312,685","",71,"Europe"
    "Oman","oman","309,500","",72,"Middle East"
    "Italy","italy","301,340","",73,"Europe"
    "Philippines","philippines","300,000","",74,"East and Southeast Asia"
    "Ecuador","ecuador","283,561","",75,"South America"
    "Burkina Faso","burkina-faso","274,200","",76,"Africa"
    "New Zealand","new-zealand","268,838","",77,"Australia and Oceania"
    "Gabon","gabon","267,667","",78,"Africa"
    "Guinea","guinea","245,857","",79,"Africa"
    "United Kingdom","united-kingdom","243,610","",80,"Europe"
    "Uganda","uganda","241,038","",81,"Africa"
    "Ghana","ghana","238,533","",82,"Africa"
    "Romania","romania","238,391","",83,"Europe"
    "Laos","laos","236,800","",84,"East and Southeast Asia"
    "Guyana","guyana","214,969","",85,"South America"
    "Belarus","belarus","207,600","",86,"Europe"
    "Kyrgyzstan","kyrgyzstan","199,951","",87,"Central Asia"
    "Senegal","senegal","196,722","",88,"Africa"
    "Syria","syria","187,437","",89,"Middle East"
    "Cambodia","cambodia","181,035","",90,"East and Southeast Asia"
    "Uruguay","uruguay","176,215","",91,"South America"
    "Suriname","suriname","163,820","",92,"South America"
    "Tunisia","tunisia","163,610","",93,"Africa"
    "Bangladesh","bangladesh","148,460","",94,"South Asia"
    "Nepal","nepal","147,181","",95,"South Asia"
    "Tajikistan","tajikistan","144,100","",96,"Central Asia"
    "Greece","greece","131,957","",97,"Europe"
    "Nicaragua","nicaragua","130,370","",98,"Central America and the Caribbean"
    "Korea, North","korea-north","120,538","",99,"East and Southeast Asia"
    "Malawi","malawi","118,484","",100,"Africa"
    "Eritrea","eritrea","117,600","",101,"Africa"
    "Benin","benin","112,622","",102,"Africa"
    "Honduras","honduras","112,090","",103,"Central America and the Caribbean"
    "Liberia","liberia","111,369","",104,"Africa"
    "Bulgaria","bulgaria","110,879","",105,"Europe"
    "Cuba","cuba","110,860","",106,"Central America and the Caribbean"
    "Guatemala","guatemala","108,889","",107,"Central America and the Caribbean"
    "Iceland","iceland","103,000","",108,"Europe"
    "Korea, South","korea-south","99,720","",109,"East and Southeast Asia"
    "Hungary","hungary","93,028","",110,"Europe"
    "Portugal","portugal","92,090","",111,"Europe"
    "Jordan","jordan","89,342","",112,"Middle East"
    "Azerbaijan","azerbaijan","86,600","",113,"Middle East"
    "Austria","austria","83,871","",114,"Europe"
    "United Arab Emirates","united-arab-emirates","83,600","",115,"Middle East"
    "Czechia","czechia","78,867","",116,"Europe"
    "Serbia","serbia","77,474","",117,"Europe"
    "Panama","panama","75,420","",118,"Central America and the Caribbean"
    "Sierra Leone","sierra-leone","71,740","",119,"Africa"
    "Ireland","ireland","70,273","",120,"Europe"
    "Georgia","georgia","69,700","",121,"Middle East"
    "Sri Lanka","sri-lanka","65,610","",122,"South Asia"
    "Lithuania","lithuania","65,300","",123,"Europe"
    "Latvia","latvia","64,589","",124,"Europe"
    "Svalbard","svalbard","62,045","",125,"Europe"
    "Togo","togo","56,785","",126,"Africa"
    "Croatia","croatia","56,594","",127,"Europe"
    "Bosnia and Herzegovina","bosnia-and-herzegovina","51,197","",128,"Europe"
    "Costa Rica","costa-rica","51,100","",129,"Central America and the Caribbean"
    "Slovakia","slovakia","49,035","",130,"Europe"
    "Dominican Republic","dominican-republic","48,670","",131,"Central America and the Caribbean"
    "Estonia","estonia","45,228","",132,"Europe"
    "Denmark","denmark","43,094","",133,"Europe"
    "Netherlands","netherlands","41,543","",134,"Europe"
    "Switzerland","switzerland","41,277","",135,"Europe"
    "Bhutan","bhutan","38,394","",136,"South Asia"
    "Guinea-Bissau","guinea-bissau","36,125","",137,"Africa"
    "Taiwan","taiwan","35,980","",138,"East and Southeast Asia"
    "Moldova","moldova","33,851","",139,"Europe"
    "Belgium","belgium","30,528","",140,"Europe"
    "Lesotho","lesotho","30,355","",141,"Africa"
    "Armenia","armenia","29,743","",142,"Middle East"
    "Solomon Islands","solomon-islands","28,896","",143,"Australia and Oceania"
    "Albania","albania","28,748","",144,"Europe"
    "Equatorial Guinea","equatorial-guinea","28,051","",145,"Africa"
    "Burundi","burundi","27,830","",146,"Africa"
    "Haiti","haiti","27,750","",147,"Central America and the Caribbean"
    "Rwanda","rwanda","26,338","",148,"Africa"
    "North Macedonia","north-macedonia","25,713","",149,"Europe"
    "Djibouti","djibouti","23,200","",150,"Africa"
    "Belize","belize","22,966","",151,"Central America and the Caribbean"
    "Israel","israel","21,937","",152,"Middle East"
    "El Salvador","el-salvador","21,041","",153,"Central America and the Caribbean"
    "Slovenia","slovenia","20,273","",154,"Europe"
    "New Caledonia","new-caledonia","18,575","",155,"Australia and Oceania"
    "Fiji","fiji","18,274","",156,"Australia and Oceania"
    "Kuwait","kuwait","17,818","",157,"Middle East"
    "Eswatini","eswatini","17,364","",158,"Africa"
    "Timor-Leste","timor-leste","14,874","",159,"East and Southeast Asia"
    "Bahamas, The","bahamas-the","13,880","",160,"Central America and the Caribbean"
    "Montenegro","montenegro","13,812","",161,"Europe"
    "Vanuatu","vanuatu","12,189","",162,"Australia and Oceania"
    "Falkland Islands (Islas Malvinas)","falkland-islands-islas-malvinas","12,173","",163,"South America"
    "Qatar","qatar","11,586","",164,"Middle East"
    "Gambia, The","gambia-the","11,300","",165,"Africa"
    "Jamaica","jamaica","10,991","",166,"Central America and the Caribbean"
    "Kosovo","kosovo","10,887","",167,"Europe"
    "Lebanon","lebanon","10,400","",168,"Middle East"
    "Cyprus","cyprus","9,251","",169,"Europe"
    "Puerto Rico","puerto-rico","9,104","",170,"Central America and the Caribbean"
    "West Bank","west-bank","5,860","",171,"Middle East"
    "Brunei","brunei","5,765","",172,"East and Southeast Asia"
    "Trinidad and Tobago","trinidad-and-tobago","5,128","",173,"Central America and the Caribbean"
    "French Polynesia","french-polynesia","4,167","",174,"Australia and Oceania"
    "Cabo Verde","cabo-verde","4,033","",175,"Africa"
    "South Georgia and South Sandwich Islands","south-georgia-and-south-sandwich-islands","3,903","",176,"South America"
    "Samoa","samoa","2,831","",177,"Australia and Oceania"
    "Luxembourg","luxembourg","2,586","",178,"Europe"
    "Comoros","comoros","2,235","",179,"Africa"
    "Mauritius","mauritius","2,040","",180,"Africa"
    "Virgin Islands","virgin-islands","1,910","",181,"Central America and the Caribbean"
    "Faroe Islands","faroe-islands","1,393","",182,"Europe"
    "Hong Kong","hong-kong","1,108","",183,"East and Southeast Asia"
    "Sao Tome and Principe","sao-tome-and-principe","964","",184,"Africa"
    "Turks and Caicos Islands","turks-and-caicos-islands","948","",185,"Central America and the Caribbean"
    "Kiribati","kiribati","811","",186,"Australia and Oceania"
    "Bahrain","bahrain","760","",187,"Middle East"
    "Dominica","dominica","751","",188,"Central America and the Caribbean"
    "Tonga","tonga","747","",189,"Australia and Oceania"
    "Singapore","singapore","719","",190,"East and Southeast Asia"
    "Micronesia, Federated States of","micronesia-federated-states-of","702","",191,"Australia and Oceania"
    "Saint Lucia","saint-lucia","616","",192,"Central America and the Caribbean"
    "Isle of Man","isle-of-man","572","",193,"Europe"
    "Guam","guam","544","",194,"Australia and Oceania"
    "Andorra","andorra","468","",195,"Europe"
    "Northern Mariana Islands","northern-mariana-islands","464","",196,"Australia and Oceania"
    "Palau","palau","459","",197,"Australia and Oceania"
    "Seychelles","seychelles","455","",198,"Africa"
    "Curacao","curacao","444","",199,"Central America and the Caribbean"
    "Antigua and Barbuda","antigua-and-barbuda","443","",200,"Central America and the Caribbean"
    "Barbados","barbados","430","",201,"Central America and the Caribbean"
    "Heard Island and McDonald Islands","heard-island-and-mcdonald-islands","412","",202,"Antarctica"
    "Saint Helena, Ascension, and Tristan da Cunha","saint-helena-ascension-and-tristan-da-cunha","394","",203,"Africa"
    "Saint Vincent and the Grenadines","saint-vincent-and-the-grenadines","389","",204,"Central America and the Caribbean"
    "Jan Mayen","jan-mayen","377","",205,"Europe"
    "Gaza Strip","gaza-strip","360","",206,"Middle East"
    "Grenada","grenada","344","",207,"Central America and the Caribbean"
    "Malta","malta","316","",208,"Europe"
    "Maldives","maldives","298","",209,"South Asia"
    "Cayman Islands","cayman-islands","264","",210,"Central America and the Caribbean"
    "Saint Kitts and Nevis","saint-kitts-and-nevis","261","",211,"Central America and the Caribbean"
    "Niue","niue","260","",212,"Australia and Oceania"
    "Saint Pierre and Miquelon","saint-pierre-and-miquelon","242","",213,"North America"
    "Cook Islands","cook-islands","236","",214,"Australia and Oceania"
    "American Samoa","american-samoa","224","",215,"Australia and Oceania"
    "Marshall Islands","marshall-islands","181","",216,"Australia and Oceania"
    "Aruba","aruba","180","",217,"Central America and the Caribbean"
    "Liechtenstein","liechtenstein","160","",218,"Europe"
    "British Virgin Islands","british-virgin-islands","151","",219,"Central America and the Caribbean"
    "Wallis and Futuna","wallis-and-futuna","142","",220,"Australia and Oceania"
    "Christmas Island","christmas-island","135","",221,"Australia and Oceania"
    "Dhekelia","dhekelia","131","",222,"Europe"
    "Akrotiri","akrotiri","123","",223,"Europe"
    "Jersey","jersey","116","",224,"Europe"
    "Montserrat","montserrat","102","",225,"Central America and the Caribbean"
    "Anguilla","anguilla","91","",226,"Central America and the Caribbean"
    "Guernsey","guernsey","78","",227,"Europe"
    "San Marino","san-marino","61","",228,"Europe"
    "British Indian Ocean Territory","british-indian-ocean-territory","60","",229,"South Asia"
    "Bermuda","bermuda","54","",230,"North America"
    "Saint Martin","saint-martin","50","",231,"Central America and the Caribbean"
    "Bouvet Island","bouvet-island","49","",232,"Antarctica"
    "Pitcairn Islands","pitcairn-islands","47","",233,"Australia and Oceania"
    "Norfolk Island","norfolk-island","36","",234,"Australia and Oceania"
    "Sint Maarten","sint-maarten","34","",235,"Central America and the Caribbean"
    "Macau","macau","28","",236,"East and Southeast Asia"
    "Tuvalu","tuvalu","26","",237,"Australia and Oceania"
    "Saint Barthelemy","saint-barthelemy","25","",238,"Central America and the Caribbean"
    "Nauru","nauru","21","",239,"Australia and Oceania"
    "Cocos (Keeling) Islands","cocos-keeling-islands","14","",240,"Australia and Oceania"
    "Tokelau","tokelau","12","",241,"Australia and Oceania"
    "Palmyra Atoll","palmyra-atoll","12","",242,"Australia and Oceania"
    "Paracel Islands","paracel-islands","8","",243,"East and Southeast Asia"
    "Wake Island","wake-island","7","",244,"Australia and Oceania"
    "Gibraltar","gibraltar","7","",245,"Europe"
    "Clipperton Island","clipperton-island","6","",246,"North America"
    "Midway Islands","midway-islands","6","",247,"Australia and Oceania"
    "Ashmore and Cartier Islands","ashmore-and-cartier-islands","5","",248,"Australia and Oceania"
    "Navassa Island","navassa-island","5","",249,"Central America and the Caribbean"
    "Spratly Islands","spratly-islands","5","",250,"East and Southeast Asia"
    "Jarvis Island","jarvis-island","5","",251,"Australia and Oceania"
    "Johnston Atoll","johnston-atoll","3","",252,"Australia and Oceania"
    "Coral Sea Islands","coral-sea-islands","3","",253,"Australia and Oceania"
    "Monaco","monaco","2","",254,"Europe"
    "Howland Island","howland-island","2","",255,"Australia and Oceania"
    "Kingman Reef","kingman-reef","1","",256,"Australia and Oceania"
    "Holy See (Vatican City)","holy-see-vatican-city","0","",257,"Europe"
    '''
    # Put data into a temporary file (using a string buffer doesn't work
    # and this does)
    file = P("/tmp/tmpcountrydata.tmp")
    with open(file, "w") as f:
        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue
            f.write(line + "\n")
    w = 60
    cia = []
    for i in csv.reader(file.open()):
        if not i:
            continue
        name, slug, area_sqkm, date, rank, region = [j.strip() for j in i]
        if name == "name":
            continue
        if name.startswith("Holy See"):
            area_sqkm = "0.49"
        area = flt(area_sqkm.replace(",", ""))*1e6
        s = f"{name} ({region})"
        if show:
            # Print the data in km²
            print(f"{s:{w}s} {int(area/1e6)} km²")
        cia.append((name, region, area))
    file.unlink()
    return tuple(cia)

if 0:
    GetCIAData(1)
    exit()

wp_area_data = GetWPData()
cia_area_data = GetCIAData()

if __name__ == "__main__": 
    import sys
    if len(sys.argv) > 1:
        import debug
        debug.SetDebugger()
    # Print out the data
    v, w = 8, max(len(i[0]) for i in areas)
    a = "Area of countries of the world in m² (T = 10¹², G = 10⁹, M = 10⁶, k = 10³)"
    # Wikipedia stuff
    print("\nWikipedia data")
    print(f"{a:{w}s} {'Total':^{v}s} {'Land':^{v}s} {'Water':^{v}s}")
    for i in wp_area_data:
        name, total_area, land_area, water_area = i
        a, b, c, d = i
        e = "m²"
        b, c, d = b.engsi + e, c.engsi + e, d.engsi + e
        print(f"{a:{w}s} {b:^{v}s} {c:^{v}s} {d:^{v}s}")
    # CIA stuff
    print("\nCIA data")
    v, w = 40, 20
    for name, region, area in CIA_area_data:
        name, region, area = i
        e = "m²"
        b, c, d = b.engsi + e, c.engsi + e, d.engsi + e
        print(f"{name:{v}s} {region:{w}s} {area.engsi:s}m²")

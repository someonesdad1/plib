"""
List of shortwave frequencies from catalog #14 of the C. Crane
Company.  The list was updated May 2003.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2003 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # List of shortwave frequencies
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import re
    import sys
    from collections import defaultdict, deque
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
    from columnize import Columnize
if 1:  # Frequency class

    class Freq:
        """Encapsulate a frequency in kHz, allowing suffixes like "v",
        "-lsb", and "-usb".  The primary functionality is to sort the
        frequency numerically regardless of the suffix.
        """

        def __init__(self, s):
            me, freq = deque(s), deque()
            digits = "0123456789."
            while me and me[0] in digits:
                freq.append(me.popleft())
            f = "".join(freq)
            s = "".join(me)
            self.suffix = ""
            if s == "-usb":
                self.suffix = "U"
            elif s == "-lsb":
                self.suffix = "L"
            elif s == "v":
                self.suffix = "v"
            self.kHz = round(float(f), 1) if "." in f else int(f)

        def __lt__(self, other):
            assert isinstance(other, Freq)
            return self.kHz < other.kHz

        def __str__(self):
            return str(self.kHz) + str(self.suffix)


if 1:  # Data

    def CCrane():
        """Returns a dictionary indexed by frequency; the values are the
        countries.  Downloaded 15 Aug 2021 from
        https://ccrane.com/shortwave-frequency-list/.  Notations:  usb =
        upper sideband, lsb = lower sideband, v = frequency varies or is
        not exact.
        """
        data = """
            Alaska: 6150 6950 7355 9920
            Albania: 6115 7425 7450 7465
            Argentina: 9690 11710 15345
            Australia: 2310 2325 2485 4835 4910 5025 5995 6020 6080 7240 9475 9560 9580 9590 9660 9710 11650 11880 12080 13630 13670 15160 15230 15240 15515 17715 17750 17775 17785 17795 21725
            Austria: 5945 6155 7325 9870 13675 13730
            Bahrain: 6010
            Bangladesh: 7185
            Belarus: 7360 7390 7420
            Bulgaria: 7400 9400 9500 9700 11700 11900 15700
            Canada RCI: 9610 9755 9770 13650 15365 17740
            Canada CBC: 6160 9625
            China: 5960 5990 6005 6020 6040 6080 6115 6190 7285 9570 9580 9690 9730 9785 9790 9870 11885 11900 11970 13675 13740 15230 15240
            Croatia: 7285 9470 11690
            Cuba: 6000 6060 6180 6300 9505 9550 11760
            Czech rep: 5930 6200 7345 7385 9400 9430 9435 9890 9955 11600 13580 15710
            Ecuador: 6050 7385 9745 11700
            Egypt: 4680 7270 9990 11885 15375 17835
            Ethiopia: 7165 9560v
            France: 5920 7315 9720 9765 9805 9865 11615 11725 13680 11995 15160 15275 15605 21620
            Germany: 5905 6140 6180 7225 7240 7280 7285 9565 9735 9755 11690 12045 15275
            Ghana: 4915
            Greece: 7475 9420 9935 12105 15630 17525
            Guyana: 3291 5950
            Hungary: 5980 6025 6035 9525
            India: 7410 9425 9445 9690 9705 9910 9950 11620 11645 11715 11935 13605 13710 15020 15075 15155 15235 17510 17670 17800 17895
            Indonesia: 9525v 11785 15150v
            Iran: 6010 6120 6250 7160 7320 7330 9855 11695 15460 17660
            Israel: 6280 6985 7545 9345 15640 15760 17535 17600
            Italy: 5965 6010 6035 6090 6120 7170 9760 11800
            Japan: 5975 6110 6120 6145 7230 9505 9535 9875 11690 11695 11715 11730 11740 11935 11970 13650 15195 15355 17685 17810 17825 17845 17870 21610 21670
            Jordan: 11690
            North Korea: 3560 4405 6185 6285 7570 9325 9335 9345 9730 9850 9975 9990 11535 11545 11710 11735 12015 13650 13760 15100 15180
            South Korea: 7275 9560 9570 9640 9650 9770 15575
            Laos: 7145
            Liberia: 4760 5470 9525
            Libya: 7320 17725 21695
            Lithuania: 7325 9710 9875
            Malaysia: 7295 9750 15295
            Mexico: 6185
            Moldova: 6235
            Mongolia: 12085
            Myanmar: 5986
            Nepal: 5005
            Netherlands: 6020 6040 6165 7120 9345 9795 9895 11655 11675 12065 12080 15315 15525 15595 17725 17810
            New Zealand: 3935 5950 9765 9870 11725 13840 15720 17675
            Nigeria: 7255 7275 7380 15120
            Oman: 15140
            Pakistan: 6215 7530 11570 15100 17835
            Papua New Guinea: 3385 4960 7120
            Philippines: 11720 11885 15190 15270 17665 17720
            Poland: 7130 9525
            Romania: 6055 6115 6150 7105 7145 7180 9515 9610 9640 9690 9755 11895 15105 15135 17745
            Russia: 6240 7150 7250 7350 9840 12010 12030 13665 15425
            Senegal: 12000
            Serbia: 6100
            Singapore: 6080 6150
            Slovakia: 7230 9440
            Solomon Islands: 5020v 9545
            South Africa: 3345 7240 7390 9685 15235 15255 17770
            Spain: 6055 6125 9680 11625 11680
            Sri Lanka: 6005 9770 11905 15745v
            Sudan: 4750 7280 9525 9660 9840 13720
            Suriname: 4990
            Sweden: 6010 7420 11550 15240
            Syria: 9330 12085 13610
            Taiwan: 5950 7130 7445 9355 9680 9785 11550 11850 1995 15215 15465
            Tajikistan: 7245
            Thailand: 5890 9535 9680 9725 9805 9810 13770
            Tibet: 4820 4905 5935 6050 7170 7240 9490
            Turkey: 5960 6020 6055 7240 9525 11735 12035
            Turkmenistan: 4930 5015
            Uganda: 4976 5026
            Ukraine: 5820 5830 9925
            UK: 5875 5975 6005 6040 6130 6195 7130 7160 7320 9410 9480 9660 9740 9750 11675 11750 11765 11920 12095 15105 15285 15360 15400 15575 17640 17830 17885 21470
            United Nations: 9565 17810
            USA AFRTS: 4319-usb 5446.5-usb 5765-usb 6350-usb 7811.5-usb 10320-usb 12133.5-usb 12759-usb 13362-usb
            USA VOA: 4930 4960 5960 6080 6105 6110 7125 7175 7205 7405 9645 9760 9785 9885 11655 11885 11890 11975 12015 12150 13600 13640 13710 13735 13755 15150 15185 15205 15290 15445 15580 17640 17715 17730 17895
            USA KAIJ: 5755 9480
            USA WBCQ: 5110-lsb 7415 9330-lsb 18910-lsb
            USA WEWN: 5810 5850 7560 7570 9450 9955 9975 15785 17595
            USA WRMI: 7385 9955
            USA WWCR: 3215 5070 7465 9985 12160 15825
            Vanuatu: 3945v 7260v
            Vatican: 4005 5885 6185 7250 7305 7360 7365 9310 9610 9635 9645 9660 9755 11625 11740 11850 13765 15595
            Vietnam: 6175 7285 9840 12020
            Yemen: 9780v
            Zambia: 4910 5915 6165
            Zanzibar: 11735
        """
        byfreq = defaultdict(list)
        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue
            country, frequencies = line.split(":")
            for s in frequencies.split():
                f = Freq(s)
                byfreq[f].append(country)
        return byfreq

    def PrimeTime():
        """From http://www.primetimeshortwave.com/country.txt downloaded
        15 Aug 2021.
        """
        data = """
            PRIME TIME SHORTWAVE - http://www.primetimeshortwave.com
            English shortwave broadcasts sorted by country

            Relay site codes: ae-United Arab Emirates, al-Albania, ar-Armenia,
            as-Ascension, au-Austria, bt-Botswana, bu-Bulgaria, ch-China, cu-Cuba,
            cy-Cyprus, fr-France, ge-Germany, gr-Greenville USA, ka-Kazakhstan,
            ko-South Korea, ku-Kuwait, ma-Madagascar, ml-Mali, mo-Moldova,
            nm-North Mariana Islands, my R. Myanmar(MRTV), om-Oman, pa-Palau, 
            ph-Philippines, ro-Romania, ru-Russia, rw-Rwanda, sa-Sao Tome e Principe, 
            se-Seychelles, si-Singapore, sl-Sri Lanka, sp-Spain, ta-Taiwan,th-Thailand, 
            tj-Tajikistan, uk-United Kingdom, uz-Uzbekistan, va-Santa Maria Vatican, 
            wb-WWRB USA, wc-WWCR USA, wh-WHRI USA, wi-WINB USA, wq-WBCQ USA, wr-WRMI USA, 
            wt-WTWW USA. za-South Africa

            Notes -- Days of week: Su-Sunday, M-Monday, Tu-Tuesday, W-Wednesday,
            Th-Thursday, F-Friday, Sa-Saturday, exW-except Wednesday
            Target areas: Af-Africa, Am-America, As-Asia, Eu-Europe, LA-Latin America,
            ME-Middle East, NA-North America, Oc-Oceania/Australia; e-East, w-West, 
            Other: alt-alternate frequency, drm-Digital Radio Mondiale, occ-occasional use,
            le-Learning English

            This page was last updated by Ernest Riley on December 28, 2017. Version B17v03

            Country         Station           UTC Time  Notes      Frequencies
            Alaska          KNLS              0800-0900 As         7370
            Alaska          KNLS              1000-1100 As         7370
            Alaska          KNLS              1200-1300 As         7355, 7370
            Alaska          KNLS              1400-1500 As         7355
            Albania         R. Tirana         2300-2330 NA,M-Sa    5850wr
            Anguilla        Wld Univ Network  0000-1000 Am         6090
            Anguilla        Wld Univ Network  1000-2200 Am         11775
            Anguilla        Wld Univ Network  2200-2400 Am         6090
            Argentina       RAE               0100-0200 NA,Tu-Sa   9395wr
            Argentina       RAE               0700-0800 wNA,Tu-Sa  5850wr, 7730wr
            Australia       Reach Beyond Aust 0000-0015 eAs, W,F   15400
            Australia       Reach Beyond Aust 1115-1130 As,M-W,F   15575
            Australia       Reach Beyond Aust 1145-1200 sAs,Sa-Su  11915
            Australia       Reach Beyond Aust 1200-1215 seAs, F    11865
            Australia       Reach Beyond Aust 1215-1230 seAs, F    11865
            Australia       Reach Beyond Aust 1230-1245 seAs, F    11865
            Australia       Reach Beyond Aust 1245-1300 sAs        11865
            Australia       Reach Beyond Aust 1300-1330 sAs, Su    9610
            Australia       Reach Beyond Aust 1315-1330 sAs, M,W,F 11865
            Australia       Reach Beyond Aust 2230-2245 eAs, M-F   15400
            Bahrain         R. Bahrain        1500-1530 ME         9745
            Bangladesh      Bangladesh Betar  1200-1300 As         15105
            Bangladesh      Bangladesh Betar  1730-2000 Eu         13580
            Biafra          R. Biafra         0500-0558 wAf        7240fr
            Biafra          R. Biafra         0500-0600 wAf        11530wr
            Biafra          R. Biafra         1900-2000 wAf        11530wr
            Canada          CFRX              0000-2400 NA         6070
            Canada          CFVP              0000-2400 NA         6030
            Canada          CKZU              0000-2400 NA         6160
            China           China R. Int'l    0000-0100 Eu         7350
            China           China R. Int'l    0000-0100 As         6075, 6180, 7425, 9425, 11790, 11885, 15125
            China           China R. Int'l    0000-0200 NA         6020al, 9570al
            China           China R. Int'l    0100-0200 NA         9580cu
            China           China R. Int'l    0100-0200 As         6075, 6180, 7370, 11885, 15125
            China           China R. Int'l    0100-0200 Eu         7350, 9675
            China           China R. Int'l    0200-0300 As         9610, 11770
            China           China R. Int'l    0300-0400 NA         9790cu
            China           China R. Int'l    0300-0400 As         11770, 13570, 13590, 13800, 15120
            China           China R. Int'l    0400-0500 As         13570, 13590, 15120
            China           China R. Int'l    0400-0500 eEu        17730, 17855
            China           China R. Int'l    0500-0600 As         11895, 15350, 15430, 15465, 17540
            China           China R. Int'l    0500-0600 ME         7220al
            China           China R. Int'l    0500-0600 Af, ME     17510
            China           China R. Int'l    0500-0600 eEu        17730, 17855
            China           China R. Int'l    0600-0700 As         11895, 13645, 15350, 15430, 15465, 17710
            China           China R. Int'l    0600-0700 ME         11750al, 11870, 15145
            China           China R. Int'l    0600-0700 Af, ME     17510
            China           China R. Int'l    0700-0800 As         11895, 13660, 15185, 15350, 15465, 17710
            China           China R. Int'l    0700-0900 Af, ME     17670
            China           China R. Int'l    0700-0900 Eu         11785al, 17490
            China           China R. Int'l    0800-0900 As         9415, 11710, 11895, 15185, 15350, 15465
            China           China R. Int'l    0900-1000 Oc         15210, 17690
            China           China R. Int'l    0900-1000 Eu         17490, 17570, 17650
            China           China R. Int'l    0900-1000 As         9415, 15185, 15350
            China           China R. Int'l    1000-1100 As         5955, 13590, 13720, 15190, 15350
            China           China R. Int'l    1000-1100 Eu         17490
            China           China R. Int'l    1000-1100 Oc         15210, 17690
            China           China R. Int'l    1000-1100 eEu        7215, 11635
            China           China R. Int'l    1100-1200 As         5955, 7250, 11650, 11795, 12015, 13590, 13720
            China           China R. Int'l    1100-1300 Eu         13665al, 17490
            China           China R. Int'l    1200-1300 As         5955, 7250, 9460, 9600, 9645, 9730, 11650, 11980, 12015
            China           China R. Int'l    1200-1300 Oc         9760, 11760
            China           China R. Int'l    1200-1300 eEu        11690
            China           China R. Int'l    1200-1300 Eu         17490
            China           China R. Int'l    1300-1400 NA         9570cu
            China           China R. Int'l    1300-1400 Eu         13670, 13790
            China           China R. Int'l    1300-1400 As         5955, 7300, 9655, 9730, 9870, 11910, 11980
            China           China R. Int'l    1300-1400 Oc         11760, 11900
            China           China R. Int'l    1300-1400 eEu        9765
            China           China R. Int'l    1400-1500 Eu         9795, 11880
            China           China R. Int'l    1400-1500 Af         13685ml, 17630ml
            China           China R. Int'l    1400-1500 As         5955, 7300, 9460, 9870
            China           China R. Int'l    1400-1500 NA         15700cu
            China           China R. Int'l    1400-1500 eEu        9765
            China           China R. Int'l    1400-1500 ME         6100
            China           China R. Int'l    1500-1600 Eu         9435, 9525
            China           China R. Int'l    1500-1600 As         5955, 7325, 7395, 9785, 9870, 9880
            China           China R. Int'l    1500-1600 Af, ME     6095, 9720
            China           China R. Int'l    1500-1600 NA         15700cu
            China           China R. Int'l    1500-1600 Af         13685ml, 17630ml
            China           China R. Int'l    1600-1700 As         6060, 6175, 7235, 9880
            China           China R. Int'l    1600-1700 Eu         7255, 9875
            China           China R. Int'l    1600-1700 Af         7435, 9570
            China           China R. Int'l    1600-1700 Af, ME     7420
            China           China R. Int'l    1700-1800 As         6090, 6140, 6175, 7235, 7410, 7420, 9880
            China           China R. Int'l    1700-1800 ME         6165
            China           China R. Int'l    1700-1800 Af         7435, 9570
            China           China R. Int'l    1700-1800 Eu         6100, 7255
            China           China R. Int'l    1800-1900 Eu         6100, 7405
            China           China R. Int'l    1900-2000 Af, ME     7295, 9440
            China           China R. Int'l    2000-2100 Af         5985, 11640ml, 13630ml
            China           China R. Int'l    2000-2100 Eu         5960al, 7285al, 7415, 9600
            China           China R. Int'l    2000-2100 Af, ME     7295, 9440
            China           China R. Int'l    2100-2130 Af         11640ml, 13630ml
            China           China R. Int'l    2100-2200 Af         7205, 7325
            China           China R. Int'l    2100-2200 Eu         5960al, 7285al, 7415, 9600
            China           China R. Int'l    2200-2300 As         5915
            China           China R. Int'l    2300-2400 Am         5990cu
            China           China R. Int'l    2300-2400 As         5915, 6145, 7410, 9535, 11790
            China           China R. Int'l    2300-2400 Eu         7350
            China           PBS Zizang Lhaza  0700-0800 As         4905, 4920, 6025, 6110, 6130, 6200, 9490, 9580
            China           PBS Zizang Lhaza  1600-1700 As         4905, 4920, 6025, 6110, 6130, 6200, 7255, 7385
            Cuba            R. Havana Cuba    0000-0100 LA         5040
            Cuba            R. Havana Cuba    0000-0100 Af         9720
            Cuba            R. Havana Cuba    0200-0600 NA         6000
            Cuba            R. Havana Cuba    0200-0800 wNA        6165
            Cuba            R. Havana Cuba    0600-0800 eNA        6000, 6060
            Cuba            R. Havana Cuba    0600-0800 wNA        6100
            Cuba            R. Havana Cuba    2000-2100 wNA        15140
            Cyprus          FG Radio          0115-0130 Af, Su     21675wr
            Cyprus          FG Radio          0245-0300 LA, Th     9955wr
            Cyprus          FG Radio          0515-0530 LA, W,F    9955wr
            Cyprus          FG Radio          1230-1245 LA, Su     9955wr
            Cyprus          FG Radio          1400-1415 LA, W      9955wr
            Cyprus          FG Radio          1445-1500 LA, Tu     9955wr
            Cyprus          FG Radio          2100-2115 Eu, W      15770wr
            Cyprus          FG Radio          2100-2115 NA, W      7570wr
            Cyprus          FG Radio          2145-2200 Eu, W      15770wr
            Cyprus          FG Radio          2300-2315 Eu, Tu     5850wr, 5985wr, 11580wr
            Cyprus          FG Radio          2300-2315 Eu, Th     5850wr, 11580wr, 11920wr
            Czech Republic  R. Prague         0230-0300 eNA,Eu     11580wr
            Czech Republic  R. Prague         0400-0430 LA, Su-M   9955wr
            Czech Republic  R. Prague         1300-1330 LA, M-Sa   9955wr
            Czech Republic  R. Prague         2330-2400 wNA        5850wr
            Diego Garcia    AFRTS             0000-2400 As         12759 USB
            Egypt           R. Cairo          0000-0030 NA         9965
            Egypt           R. Cairo          0200-0330 NA         9315
            Egypt           R. Cairo          1600-1800 Af         11800
            Egypt           R. Cairo          1900-2030 Af         15290
            Egypt           R. Cairo          2115-2245 Eu         9900
            Egypt           R. Cairo          2300-2400 NA         9965
            Equ Guinea      R. Africa         1300-2100 Af         21525wr
            France          Oromo Voice R.    1615-1630 Af, M      17850
            France          R. France Int'l   0100-0200 LA, F-Sa   11580wr
            France          R. France Int'l   0200-0300 LA, W-Su   11580wr
            France          R. France Int'l   0600-0700 Af         9735
            France          R. France Int'l   2100-2200 LA, M-Tu   15770wr
            France          R. France Int'l   2115-2200 LA, W      15770wr
            France          R. France Int'l   2130-2200 LA, Th     15770wr
            France          Radio Biafra      1800-2100 Af         11700bu
            Germany         Eur Shortwave R   1000-1200 wEu, M-Sa  6160
            Germany         Eur Shortwave R   1200-1400 wEu, M-Sa  3975
            Germany         Eur Shortwave R   1400-1600 wEu, M-Sa  6160
            Germany         Eur Shortwave R   1600-1800 wEu, M-Sa  3975
            Germany         Eur Shortwave R   1800-2000 wEu, M-Sa  6160
            Germany         Eur Shortwave R   2000-2200 wEu, M-Sa  3975
            Germany         R. der Dokumenta  0600-0800 cEu        15560
            Germany         R. der Dokumenta  1500-1800 cEu        15560
            Guam            KSDA              1600-1630 As         15490, 15715
            Guam            KSDA              2200-2230 As,Su,Tu,Th15435
            Guam            KTWR              1000-1030 As,Oc, M-F 11995
            Guam            KTWR              1000-1030 As,Oc, Su  11965
            Guam            KTWR              1000-1045 As,Oc, Sa  11995
            Guam            KTWR              1100-1130 As,Oc, M   11965
            Guam            KTWR              1100-1145 As,Oc, W-Sa11965
            Guam            KTWR              1100-1200 As,Oc, Su  11965
            Guam            KTWR              1230-1300 As,Oc, Sa  11695
            Guam            KTWR              1315-1345 As,Oc, Sa  7510
            India           All India R.      0000-0045 As         6045, 7550, 9445, 9705, 11645
            India           All India R.      1000-1100 As         7270, 13605, 15410, 17510
            India           All India R.      1000-1100 Oc         13695, 15770, 17895
            India           All India R.      1330-1500 As         9690, 13695
            India           All India R.      1530-1545 As         6155, 11560
            India           All India R.      1745-1945 Af         9445, 11935, 13695, 17670
            India           All India R.      1745-1945 Eu         7550, 9950
            India           All India R.      2045-2230 Eu         7550, 9445, 9950
            India           All India R.      2045-2230 Oc         9910, 11620, 11740
            India           All India R.      2245-2400 As         6045, 7550, 9445, 9705, 11645
            Indonesia       V. of Indonesia   1000-1100 Oc         9525
            Indonesia       V. of Indonesia   1300-1400 eAs        9525
            Indonesia       V. of Indonesia   1900-2000 wEu        9525
            Iran            VOIRI             1020-1120 As         17820, 21510
            Iran            VOIRI             1520-1620 As         11640, 11830
            Iran            VOIRI             1920-2020 Af         9420, 9800
            Iran            VOIRI             1920-2020 Eu         7315, 9810
            Iran            VOIRI (VO Justice)0320-0420 NA         9420
            Italy           IRRS              0800-0900 Eu, Sa     9510bu
            Italy           IRRS              0930-1200 Eu, Su     9510bu
            Italy           IRRS              1500-1600 eEu, Su    9400bu
            Italy           IRRS              1800-1900 Eu, F-Su   7290bu
            Japan           R. Japan          0500-0530 Eu         6155au
            Japan           R. Japan          0500-0530 sAf        9770fr
            Japan           R. Japan          0710-0725 seAs, Sa-Su9730
            Japan           R. Japan          1100-1130 As         11825si
            Japan           R. Japan          1100-1130 Eu, F      9760uk drm
            Japan           R. Japan          1400-1430 As         9560uz, 11925pa
            Japan           R. Japan          1540-1600 seAs, Th,F 5985my
            Japan           R. Japan          1800-1830 Af         11800za
            Japan           R. Japan          1930-2000 wAf        9485va
            Japan           R. Japan          1930-2000 Oc         9625
            Japan           Shiokaze          1300-1400 As, Th     6085
            Japan           Shiokaze          1600-1700 As, Th     7285
            Kuwait          R. Kuwait         0500-0800 As         11970
            Kuwait          R. Kuwait         1800-2100 Eu         15540
            Laos            Lao National Radio1430-1500 As         6130
            Malaysia        RTM Malaysia      0000-2400 Domestic   7295
            Mongolia        V. of Mongolia    0900-0930 As         12085
            Mongolia        V. of Mongolia    1530-1600 eAs        12015
            Myanmar         Myanmar R.        0700-0730 As         9731
            Myanmar         Thazin R.         0130-0200 As         6030
            Myanmar         Thazin R.         0630-0700 As         9460
            Myanmar         Thazin R.         1430-1500 As         6165
            Netherlands     Mighty KBC Radio  0000-0200 NA, Su     6150ge
            Netherlands     Mighty KBC Radio  1500-1600 wEu, Sa    9400bu
            New Zealand     RNZI              0000-0458 Oc         15720
            New Zealand     RNZI              0459-0758 Oc         13730
            New Zealand     RNZI              0759-1058 Oc         9765
            New Zealand     RNZI              1059-1258 Oc         11610
            New Zealand     RNZI              1259-1650 Oc         7390
            New Zealand     RNZI              1651-1750 Oc, Su-F   7285 drm
            New Zealand     RNZI              1651-1758 Oc, Sa     7390
            New Zealand     RNZI              1751-1850 Su-F       9780 drm
            New Zealand     RNZI              1759-1958 Oc, Sa     11725
            New Zealand     RNZI              1851-1950 Oc, Su-F   11690 drm
            New Zealand     RNZI              1951-2050 Oc, Su-F   13840 drm
            New Zealand     RNZI              1959-2058 Oc, Sa     13840
            New Zealand     RNZI              2051-2400 Oc         15720
            Nigeria         V. of Nigeria     0800-0900 Af         7255
            Nigeria         V. of Nigeria     0900-1200 Af         9690
            Nigeria         V. of Nigeria     1200-1530 Af         15120
            Nigeria         V. of Nigeria     1800-1930 Af         7255
            North Korea     V. of Korea       0430-0527 LA         11735, 13760, 15180
            North Korea     V. of Korea       0430-0527 neAs       7220, 9445, 9730
            North Korea     V. of Korea       0530-0627 seAs       13650, 15105
            North Korea     V. of Korea       0630-0727 neAs       7220, 9445, 9730
            North Korea     V. of Korea       1030-1127 LA         6170, 9435
            North Korea     V. of Korea       1030-1127 seAs       6185, 9850
            North Korea     V. of Korea       1330-1427 NA         9435, 11710
            North Korea     V. of Korea       1330-1427 wEu        7570, 12015
            North Korea     V. of Korea       1530-1627 NA         9435, 11710
            North Korea     V. of Korea       1530-1627 wEu        7570, 12015
            North Korea     V. of Korea       1630-1727 ME         9890, 11645
            North Korea     V. of Korea       1830-1927 wEu        7570, 12015
            North Korea     V. of Korea       1930-2027 ME         9875, 11635
            North Korea     V. of Korea       1930-2027 sAf        7210, 11910
            North Korea     V. of Korea       2130-2227 wEu        7570, 12015
            Oman            R. Sultanate Oman 0300-0400 Af         15355
            Oman            R. Sultanate Oman 1400-1500 Eu         15140
            Pakistan        R. Pakistan       1100-1104 Eu         15730, 17730
            Palau           T8WH              0100-0130 As, Su     17720
            Palau           T8WH              0130-0200 As, Su     17720
            Palau           T8WH              0200-0300 As, Su     17720
            Palau           T8WH              0400-0430 As, Su     17720
            Palau           T8WH              0800-0930 As, M-F    9930
            Palau           T8WH              0900-1000 As, Su     9930
            Palau           T8WH              0915-0930 As, Sa     9930
            Palau           T8WH              0930-0945 As, F      9930
            Palau           T8WH              0930-1000 As, M,W,Th 9930
            Palau           T8WH              0930-1000 As, Sa     9930
            Palau           T8WH              0945-1000 As, F      9930
            Palau           T8WH              1000-1030 As, Sa-Su  9930
            Palau           T8WH              1030-1100 As, Sa-Su  9930
            Palau           T8WH              1100-1130 As,Su      9930
            Palau           T8WH              1100-1200 As, Sa     9930
            Palau           T8WH              1130-1400 As, Su     9930
            Palau           T8WH              1200-1230 As, Su     9930
            Palau           T8WH              1200-1230 As, Sa     9930
            Palau           T8WH              1245-1300 As,Sa      9930
            Palau           T8WH              1300-1330 As, Sa     9930
            Palau           T8WH              1300-1330 As, Su     9965
            Palau           T8WH              1300-1400 As, Su     17720
            Palau           T8WH              1300-1400 As, Sa     9965
            Palau           T8WH              1330-1345 As, Sa     9930
            Palau           T8WH              1330-1400 As, Su     9965
            Palau           T8WH              1345-1400 As, Sa     9930
            Palau           T8WH              1400-1430 As, Su     9965
            Palau           T8WH              1430-1600 As, Sa-Su  11675
            Philippines     R. Pilipinas      1730-1930 ME         9925, 12120, 15190
            Romania         R. Romania Int'l  0100-0200 eNA        6130, 7325
            Romania         R. Romania Int'l  0400-0500 wNA        6020, 7410
            Romania         R. Romania Int'l  0400-0500 As         9800 drm, 11790
            Romania         R. Romania Int'l  0630-0700 Eu         7345, 9770 drm
            Romania         R. Romania Int'l  0630-0700 Oc, As     15450, 17780
            Romania         R. Romania Int'l  1200-1300 Eu         15460, 17650
            Romania         R. Romania Int'l  1200-1300 seAf       17765, 21490
            Romania         R. Romania Int'l  1800-1900 Eu         5935, 7350 drm
            Romania         R. Romania Int'l  2130-2200 Eu         6030 drm, 7375
            Romania         R. Romania Int'l  2130-2200 eNA        6170, 7310
            Romania         R. Romania Int'l  2300-2400 Eu         5980, 7220
            Romania         R. Romania Int'l  2300-2400 As         7325, 9620
            Russia          Voice of Russia   1800-2100 As         11760 drm
            Saudi Arabia    BSKSA             1000-1225 Af         15250
            Slovakia        R. Slovakia       0030-0100 wNA        5850wr
            Slovakia        R. Slovakia       0030-0100 wEu, eNA   11580wr
            Slovakia        R. Slovakia       0630-0700 Eu         3985ge
            Slovakia        R. Slovakia       1600-1630 Eu         7310ge
            Slovakia        R. Slovakia       2000-2030 Eu         3985ge
            Slovakia        R. Slovakia       2100-2130 wEu,eNA    11580wr(Sa-Su)
            South Africa    Channel Africa    0300-0400 Af, M-F    3345, 6155
            South Africa    Channel Africa    0400-0500 Af, M-F    3345
            South Africa    Channel Africa    0500-0900 Af, M-F    7230
            South Africa    Channel Africa    0600-0700 Af, M-F    15255
            South Africa    Channel Africa    0900-1600 Af, M-F    9625
            South Africa    Channel Africa    1500-1600 Af, M-F    9625
            South Africa    Channel Africa    1700-1755 Af, M-F    15235
            South Africa    S.Afr. Radio Leag.0800-0900 Af, Su     7205, 17660
            South Africa    S.Afr. Radio Leag.1630-1730 Af, M      4895
            South Korea     KBS World R.      0200-0300 LA         9580
            South Korea     KBS World R.      0800-1030 seAs       9770
            South Korea     KBS World R.      1100-1130 Eu, Sa     9760uk drm
            South Korea     KBS World R.      1300-1400 seAs       9570
            South Korea     KBS World R.      1300-1400 NA         15575
            South Korea     KBS World R.      1400-1500 sAs        9630
            South Korea     KBS World R.      1500-1700 Eu         9515
            South Korea     KBS World R.      1500-1700 As         9630
            South Korea     KBS World R.      1600-1700 seAs       9640
            South Korea     KBS World R.      2200-2300 wEu        11810
            South Korea     KBS World R.      2200-2300 As         13705
            Sudan           Miraya FM R       0300-0600 Af         11560mo
            Sudan           V. of Africa      0800-0900 Af         9505
            Sudan           Voice of Africa R.0800-0900 Af         9505
            Sudan           Voice of Africa R.1700-1800 Af         9505
            Swaziland       TWR Africa        0255-0325 Af, Su     3200
            Swaziland       TWR Africa        0430-0600 Af, M-F    3200
            Swaziland       TWR Africa        0430-0700 Af         4775
            Swaziland       TWR Africa        0500-0700 Af         6120
            Swaziland       TWR Africa        1420-1455 Af         6025
            Swaziland       TWR Africa        1802-1832 Af, M-F    9500
            Swaziland       TWR Africa        1802-1902 Af, Sa     9500
            Taiwan          PCJ Radio Int'l   0900-1000 As, Sa     17825sl
            Taiwan          PCJ Radio Int'l   2200-2300 LA, F      9955wr
            Taiwan          R. Taiwan Int'l   0300-0400 As         15320
            Taiwan          R. Taiwan Int'l   1100-1200 As         7445, 11600
            Taiwan          R. Taiwan Int'l   1500-1600 As         9405, 11685
            Taiwan          R. Taiwan Int'l   1600-1700 sAs        6185
            Tajikistan      V. of Tajik       1300-1400 As,ME,Eu   7245
            Tanzania        Zanzibar B/C      1800-1810 Af         11735
            Thailand        R. Thailand       0000-0100 NA         13745
            Thailand        R. Thailand       0200-0230 NA         13745
            Thailand        R. Thailand       0530-0600 Eu         17640
            Thailand        R. Thailand       1230-1300 As, Oc     9390
            Thailand        R. Thailand       1400-1430 As, Oc     9390
            Thailand        R. Thailand       1900-2000 Eu         9390
            Thailand        R. Thailand       2030-2045 Eu         9390
            Turkey          V. of Turkey      0400-0455 eNA,wEu    6125
            Turkey          V. of Turkey      0400-0455 ME         7240
            Turkey          V. of Turkey      0500-0555 seAs       17530
            Turkey          V. of Turkey      1330-1425 wEu        12035
            Turkey          V. of Turkey      1730-1825 As         11730
            Turkey          V. of Turkey      1930-2025 wEu        6050
            Turkey          V. of Turkey      2130-2225 seAs       9610
            Turkey          V. of Turkey      2300-2355 eNA        5960
            U. S. A.        AWR               1530-1600 As, Sa-W   11985sl
            U. S. A.        AWR               1600-1630 As         11955sl, 17730ma
            U. S. A.        AWR               1830-1900 Af         15155ma
            U. S. A.        AWR               2100-2130 Af         11980au
            U. S. A.        AWR               2200-2230 As,M,W,Sa  9720sl
            U. S. A.        AWR               2230-2300 LA         5950wr
            U. S. A.        Eternal Good News 0200-0215 NA, M      7385wh
            U. S. A.        Eternal Good News 0445-0500 Eu,Sa      11635wh
            U. S. A.        Eternal Good News 1230-1245 As, Su     21480ma
            U. S. A.        Eternal Good News 1230-1245 As,Su      9930pa
            U. S. A.        Eternal Good News 1400-1415 As, Sa     17650fr
            U. S. A.        Eternal Good News 1730-1745 Af, Sa     21600wh
            U. S. A.        Eternal Good News 1815-1830 As, Su     7365ge
            U. S. A.        Eternal Good News 1930-1945 Eu, Sa     6030ge
            U. S. A.        Eternal Good News 2100-2115 Eu, Su     11705wh
            U. S. A.        Eternal Good News 2345-2400 LA,Su      7315wh
            U. S. A.        Follow the Bible M1900-1930 Af         12005as, 12030ae
            U. S. A.        From Isle of Music0000-0100 NA,Eu, Tu  7490wq
            U. S. A.        From Isle of Music1200-1300 Eu, Sa     6070ge
            U. S. A.        From Isle of Music1500-1600 eEu,Su     9400bu
            U. S. A.        From Isle of Music1900-2000 Eu, Tu     6070ge
            U. S. A.        KVOH              1900-2000 LA, F      17775
            U. S. A.        Overcomer Ministry0000-0100 NA,Eu, M   5920wh
            U. S. A.        Overcomer Ministry0000-0100 NA         9370wb, 7570wr, 7780wr
            U. S. A.        Overcomer Ministry0100-0200 LA         7780wr
            U. S. A.        Overcomer Ministry0100-0200 eNA        9370wb
            U. S. A.        Overcomer Ministry0100-0200 wNA        5850wr
            U. S. A.        Overcomer Ministry0100-0200 eNA, M     7490wq
            U. S. A.        Overcomer Ministry0100-0200 wNA        7570wr, 7730wr
            U. S. A.        Overcomer Ministry0200-0300 eNA, F-Su  7490wq
            U. S. A.        Overcomer Ministry0200-0300 eNA        3185wb, 5130wq
            U. S. A.        Overcomer Ministry0200-0300 LA         7780wr
            U. S. A.        Overcomer Ministry0200-0300 wNA        5850wr, 7570wr, 7730wr
            U. S. A.        Overcomer Ministry0200-0300 eNA, Tu,W  7490wq
            U. S. A.        Overcomer Ministry0300-0400 wNA        5850wr, 7570wr, 7730wr
            U. S. A.        Overcomer Ministry0300-0400 LA         7780wr
            U. S. A.        Overcomer Ministry0300-0400 wEu        11580wr
            U. S. A.        Overcomer Ministry0300-0400 eNA        3185wb, 5130wq, 7490wq
            U. S. A.        Overcomer Ministry0400-0500 wNA        5850wr,7570wr, 7730wr
            U. S. A.        Overcomer Ministry0400-0500 wEu        11580wr
            U. S. A.        Overcomer Ministry0400-0500 eNA        3185wb
            U. S. A.        Overcomer Ministry0400-0500 LA         5890wc, 7780wr
            U. S. A.        Overcomer Ministry0500-0600 wEu        11580wr
            U. S. A.        Overcomer Ministry0500-0600 wNA        5850wr, 7570wr, 7730wr
            U. S. A.        Overcomer Ministry0500-0600 eNA        3185wb
            U. S. A.        Overcomer Ministry0500-0600 LA         5890wc, 7780wr
            U. S. A.        Overcomer Ministry0500-0600 eNA, M-F   3215wc
            U. S. A.        Overcomer Ministry0600-0700 eNA, M-Sa  3215wc
            U. S. A.        Overcomer Ministry0600-0700 eNA, Su    4840wc
            U. S. A.        Overcomer Ministry0600-0700 wNA        5850wr, 7570wr
            U. S. A.        Overcomer Ministry0600-0700 eNA        3185wb
            U. S. A.        Overcomer Ministry0600-0700 wEu        7315wh, 11580wr
            U. S. A.        Overcomer Ministry0600-0700 NA, Su     4840wc
            U. S. A.        Overcomer Ministry0600-0700 LA         5890wc, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry0700-0800 wNA        7570wr
            U. S. A.        Overcomer Ministry0700-0800 eNA, M-Sa  3215wc
            U. S. A.        Overcomer Ministry0700-0800 eNA, Sa    4840wc
            U. S. A.        Overcomer Ministry0700-0800 wEu        7355wh, 11580wr
            U. S. A.        Overcomer Ministry0700-0800 eNA        3185wb
            U. S. A.        Overcomer Ministry0700-0800 LA         5890wc, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry0800-0900 LA         5890wc, 7730wr, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry0800-0900 wNA        7570wr
            U. S. A.        Overcomer Ministry0800-0900 wEu        11850wr
            U. S. A.        Overcomer Ministry0800-0900 eNA, M-Sa  3215wc
            U. S. A.        Overcomer Ministry0800-0900 eNA        3185wb
            U. S. A.        Overcomer Ministry0900-0930 LA         5890wc, 7730wr, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry0900-0930 eNA, M-Sa  3215wc
            U. S. A.        Overcomer Ministry0900-0930 wEu        11580wr
            U. S. A.        Overcomer Ministry0900-0930 eNA        3185wb
            U. S. A.        Overcomer Ministry0900-0930 wNA        7570wr
            U. S. A.        Overcomer Ministry0930-1000 eNA, M-Sa  3215wc
            U. S. A.        Overcomer Ministry0930-1000 wEu        11580wr
            U. S. A.        Overcomer Ministry0930-1000 LA         5890wc, 7730wr, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry0930-1000 eNA        3185wb
            U. S. A.        Overcomer Ministry0930-1000 eNA, Sa    4840wc
            U. S. A.        Overcomer Ministry0930-1000 wNA        7570wr
            U. S. A.        Overcomer Ministry1000-1030 wNA        7570wr
            U. S. A.        Overcomer Ministry1000-1030 Eu         11580wr
            U. S. A.        Overcomer Ministry1000-1030 eNA        3185wb
            U. S. A.        Overcomer Ministry1000-1030 LA         5890wc, 7730wr, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry1000-1030 eNA, Sa    4840wc
            U. S. A.        Overcomer Ministry1030-1100 wNA        7570wr
            U. S. A.        Overcomer Ministry1030-1100 eNA        3185wb
            U. S. A.        Overcomer Ministry1030-1100 LA         5890wc, 7730wr, 7780wr, 9955wr
            U. S. A.        Overcomer Ministry1030-1100 wEu        11580wr
            U. S. A.        Overcomer Ministry1100-1200 eNA, Su    4840wc
            U. S. A.        Overcomer Ministry1100-1200 LA         5890wc, 7730wr, 7780wr
            U. S. A.        Overcomer Ministry1100-1200 wEu        11580wr
            U. S. A.        Overcomer Ministry1100-1200 wNA        5850wr, 7570wr
            U. S. A.        Overcomer Ministry1100-1200 eNA        3185wb
            U. S. A.        Overcomer Ministry1100-1200 wEu, M-F   15795wc
            U. S. A.        Overcomer Ministry1200-1300 wNA        5850wr, 7570wr
            U. S. A.        Overcomer Ministry1200-1300 LA,-M-F    5890wc
            U. S. A.        Overcomer Ministry1200-1300 eNA, Su    9840wh
            U. S. A.        Overcomer Ministry1200-1300 wEu        11580wr
            U. S. A.        Overcomer Ministry1200-1300 LA         7730wr
            U. S. A.        Overcomer Ministry1200-1300 eNA        9370wb
            U. S. A.        Overcomer Ministry1300-1400 LA         7730wr
            U. S. A.        Overcomer Ministry1300-1400 eNA        9370wb
            U. S. A.        Overcomer Ministry1300-1400 LA, M-F    9980wc
            U. S. A.        Overcomer Ministry1300-1400 LA, Sa-Su  21610wh
            U. S. A.        Overcomer Ministry1300-1400 wNA        5850wr, 7570wr, 11825wr
            U. S. A.        Overcomer Ministry1400-1500 cAf, Sa    21600wh
            U. S. A.        Overcomer Ministry1400-1500 eNA, Sa    9840wh
            U. S. A.        Overcomer Ministry1400-1500 wNA        11825wr
            U. S. A.        Overcomer Ministry1400-1500 LA, M-F    9980wc
            U. S. A.        Overcomer Ministry1400-1500 eNA        9370wb
            U. S. A.        Overcomer Ministry1500-1600 wNA        11825wr
            U. S. A.        Overcomer Ministry1500-1600 eNA        9370wb
            U. S. A.        Overcomer Ministry1500-1600 wEu        11580wr
            U. S. A.        Overcomer Ministry1500-1600 eNA, Sa    9840wh
            U. S. A.        Overcomer Ministry1500-1600 LA         9955wr, 9980wc
            U. S. A.        Overcomer Ministry1600-1700 wNA        11825wr
            U. S. A.        Overcomer Ministry1600-1700 eNA        9370wb, 9840wh
            U. S. A.        Overcomer Ministry1600-1700 LA         9955wr, 9980wc
            U. S. A.        Overcomer Ministry1600-1700 wEu        11580wr
            U. S. A.        Overcomer Ministry1700-1800 eNA        9370wb, 9840wh
            U. S. A.        Overcomer Ministry1700-1800 LA         9955wr, 9980wc
            U. S. A.        Overcomer Ministry1700-1800 wEu        11580wr
            U. S. A.        Overcomer Ministry1700-1800 wNA        11825wr
            U. S. A.        Overcomer Ministry1800-1900 eNA        5900bu
            U. S. A.        Overcomer Ministry1800-1900 eNA        9370wb
            U. S. A.        Overcomer Ministry1800-1900 eAF        9400bu
            U. S. A.        Overcomer Ministry1800-1900 LA         9955wr, 9980wc
            U. S. A.        Overcomer Ministry1800-1900 wEu        11580wr
            U. S. A.        Overcomer Ministry1800-1900 wNA        11825wr, 15710wh
            U. S. A.        Overcomer Ministry1800-1900 LA, Su     12160wc
            U. S. A.        Overcomer Ministry1800-1900 cAf, M-F   21610wh
            U. S. A.        Overcomer Ministry1830-1900 ME, M-F    6000bu
            U. S. A.        Overcomer Ministry1900-2000 ME, M-F    6000bu
            U. S. A.        Overcomer Ministry1900-2000 eNA        9370wb
            U. S. A.        Overcomer Ministry1900-2000 eAF        9400bu
            U. S. A.        Overcomer Ministry1900-2000 eNA, Su    9840wh
            U. S. A.        Overcomer Ministry1900-2000 LA         9955wr, 9980wc
            U. S. A.        Overcomer Ministry1900-2000 wEU        11580wr
            U. S. A.        Overcomer Ministry1900-2000 wNA        11825wr, 15710wh
            U. S. A.        Overcomer Ministry1900-2000 cAF, Sa-Su 12160wc
            U. S. A.        Overcomer Ministry1900-2000 cAF, M-F   21610wh
            U. S. A.        Overcomer Ministry2000-2100 eNA        9370wb
            U. S. A.        Overcomer Ministry2000-2100 LA         9955wr, 9980wc
            U. S. A.        Overcomer Ministry2000-2100 wNA        11825wr, 15710wh
            U. S. A.        Overcomer Ministry2000-2100 cA, Sa     12160wc
            U. S. A.        Overcomer Ministry2100-2200 eNA        9370wb, 15710wh
            U. S. A.        Overcomer Ministry2100-2200 LA, M-F    9955wr
            U. S. A.        Overcomer Ministry2100-2200 LA         9980wc
            U. S. A.        Overcomer Ministry2100-2200 wNA        11825wr
            U. S. A.        Overcomer Ministry2200-2300 eNA        9370wb, 11825wr
            U. S. A.        Overcomer Ministry2200-2300 wEU, M-F   5910wh
            U. S. A.        Overcomer Ministry2200-2300 LA         9980wc
            U. S. A.        Overcomer Ministry2300-2400 eNA, M-F   7490wq
            U. S. A.        Overcomer Ministry2300-2400 wNA        7570wr
            U. S. A.        Overcomer Ministry2300-2400 LA         7730wr
            U. S. A.        Overcomer Ministry2300-2400 eNA        9370wb, 11825wr
            U. S. A.        Overcomer Ministry2300-2400 wEU, M-F   5910wh
            U. S. A.        Overcomer Ministry2300-2400 LA, M-F    9980wc
            U. S. A.        Pan American B/C  1400-1430 As, Su     15205ge
            U. S. A.        Pan American B/C  1430-1445 As, Su     15205bu
            U. S. A.        Pan American B/C  1930-2000 Af, Su     5930ge
            U. S. A.        V. of America     0300-0400 Af         4930bt, 6080sa, 15580ku
            U. S. A.        V. of America     0400-0500 Af         4930bt, 4960sa, 6080sa, 15580ku
            U. S. A.        V. of America     0500-0600 Af         4930bt, 6080sa, 15580bt
            U. S. A.        V. of America     0600-0700 Af         6080sa, 9550sa, 15580bt
            U. S. A.        V. of America     1400-1500 Af         4930bt, 15580bt, 17885bt
            U. S. A.        V. of America     1500-1600 Af         4930bt, 7455bt, 15580bt, 17895sa
            U. S. A.        V. of America     1600-1630 Af         4930bt, 6080sa,15580bt, 17895va
            U. S. A.        V. of America     1630-1700 Af         4930bt, 6080bt Sa-Su, 15580bt Sa-Su
            U. S. A.        V. of America     1630-1700 Af, M-F    11850za, 13865uk, 15180va
            U. S. A.        V. of America     1700-1730 Af         6080sa, 13590ku, 17895va
            U. S. A.        V. of America     1730-1800 Af         6080sa, 13590ku/sa, 15580bt, 17895va
            U. S. A.        V. of America     1800-1900 Af         4930bt (Sa-Su), 13590th, 15580bt
            U. S. A.        V. of America     1900-2000 Af         4930bt, 13590sa, 15580bt
            U. S. A.        V. of America     2000-2100 Af         4930bt, 6195bt, 15580bt
            U. S. A.        V. of America     2030-2100 Af, Sa-Su  4960sa
            U. S. A.        V. of America     2100-2200 Af         6195bt, 15580gr
            U. S. A.        WBCQ              0000-0100 Am, Sa     5130
            U. S. A.        WBCQ              0100-0200 Am, Tu-Sa  7490
            U. S. A.        WBCQ              0100-0200 Am         9330
            U. S. A.        WBCQ              0100-0500 Am, Su-M   5130
            U. S. A.        WBCQ              0300-0500 Am, M      7490
            U. S. A.        WBCQ              0400-0500 Am, M-Sa   7490
            U. S. A.        WBCQ              2000-2100 Am, Tu     7490
            U. S. A.        WBCQ              2100-2200 Am, M-F    7490
            U. S. A.        WBCQ              2200-2300 Am, Su     7490
            U. S. A.        WBCQ              2200-2400 Am, Sa-Su  7490
            U. S. A.        WEWN              0000-0900 Af         11520
            U. S. A.        WEWN              1200-1500 As         12065
            U. S. A.        WEWN              1500-1900 ME         15610
            U. S. A.        WEWN              1900-2400 Af         15610
            U. S. A.        WHRI              0000-0100 NA, Tu-Su  5920
            U. S. A.        WHRI              0000-0100 NA         7385
            U. S. A.        WHRI              0100-0200 NA, Su-M   7385
            U. S. A.        WHRI              0100-0200 NA, Tu-Sa  5920
            U. S. A.        WHRI              0200-0300 NA         7385
            U. S. A.        WHRI              0200-0300 LA         7315
            U. S. A.        WHRI              0200-0300 NA         5920
            U. S. A.        WHRI              0300-0400 NA         5920
            U. S. A.        WHRI              0300-0400 NA         7385
            U. S. A.        WHRI              0300-0400 Eu, Su     7520
            U. S. A.        WHRI              0300-0400 LA, M-Sa   7315
            U. S. A.        WHRI              0400-0430 NA         7385
            U. S. A.        WHRI              0400-0430 As,Oc,Sa   12015
            U. S. A.        WHRI              0430-0500 nAf, Sa-Su 9825
            U. S. A.        WHRI              0500-0600 nAf        9825
            U. S. A.        WHRI              1300-2100 Af         11750
            U. S. A.        WHRI              1700-1800 wNA,Su     15760
            U. S. A.        WHRI              1800-1900 NA         9840
            U. S. A.        WHRI              1900-2000 NA, Su     9840
            U. S. A.        WHRI              2000-2100 eNA,wEu,Su 11750
            U. S. A.        WHRI              2000-2100 Af         21610
            U. S. A.        WHRI              2100-2200 LA         17540
            U. S. A.        WHRI              2200-2300 NA, Sa-Su  9505
            U. S. A.        WHRI              2200-2300 wNA, Su    15760
            U. S. A.        WHRI              2300-2400 LA         7315
            U. S. A.        WHRI              2300-2400 NA, Sa-Su  9505
            U. S. A.        WINB              0000-0230 LA, Tu-Sa  9265
            U. S. A.        WINB              0000-0300 LA, M      9265
            U. S. A.        WINB              1100-1300 LA, Su     9265
            U. S. A.        WINB              1300-1930 LA, Sa-Su  9265
            U. S. A.        WINB              1930-2400 LA         9265
            U. S. A.        WJHR              1400-2200 NA         15555 USB
            U. S. A.        Wld Univ Network  0000-0100 NA         13845wc
            U. S. A.        Wld Univ Network  0000-1200 Af         5935wc
            U. S. A.        Wld Univ Network  1200-2400 NA, Sa-Su  13845wc
            U. S. A.        Wld Univ Network  1500-2400 NA, M-F    13845wc
            U. S. A.        WMLK              1700-2200 Eu         9275
            U. S. A.        World Voice       0200-0300 As         9600ma
            U. S. A.        World Voice       0300-0400 As         15560ma
            U. S. A.        World Voice       0400-0500 Af         11825ma
            U. S. A.        World Voice       1800-1900 Af         17640ma
            U. S. A.        World Voice       2000-2100 Af         17640ma
            U. S. A.        WRMI              0000-0100 LA         9955
            U. S. A.        WRMI              0100-0300 Eu         11580
            U. S. A.        WRMI              0100-0600 LA         9955
            U. S. A.        WRMI              0700-1000 LA         5850
            U. S. A.        WRMI              1000-1030 NA         5850
            U. S. A.        WRMI              1100-1500 LA         9955
            U. S. A.        WRMI              2100-2200 Eu         15770
            U. S. A.        WRMI              2100-2400 LA         9955
            U. S. A.        WRMI              2100-2400 LA, W-Su   9955
            U. S. A.        WRMI              2300-2400 Eu         5850, 11580
            U. S. A.        WRMI              2300-2400 LA         9955
            U. S. A.        WRNO              0200-0500 Am         7506.4
            U. S. A.        WTWW              0000-0100 NA         12105
            U. S. A.        WTWW              0000-0100 LA         9930
            U. S. A.        WTWW              0000-0200 NA,Eu      9475
            U. S. A.        WTWW              0000-1400 LA         5085
            U. S. A.        WTWW              0200-1400 NA,Eu,Af   5830
            U. S. A.        WTWW              1400-2400 NA,Eu      9475
            U. S. A.        WTWW              1400-2400 LA         9930
            U. S. A.        WTWW              1700-2400 NA         12105
            U. S. A.        WWCR1             0000-0100 eNA, Eu    6115
            U. S. A.        WWCR1             0100-0900 eNA, Eu    3215
            U. S. A.        WWCR1             0900-1200 eNA, Eu    15795
            U. S. A.        WWCR1             1200-2100 eNA, Eu    15825
            U. S. A.        WWCR1             2100-2400 eNA, Eu    6115
            U. S. A.        WWCR2             0000-1200 Af         5935
            U. S. A.        WWCR2             1200-1500 Af         7490
            U. S. A.        WWCR2             1500-2000 Af         12160
            U. S. A.        WWCR2             2000-2200 Af         9350
            U. S. A.        WWCR2             2200-2400 Af         5890
            U. S. A.        WWCR3             0000-1200 eNA, wEu   4840
            U. S. A.        WWCR3             1200-1500 NA, M-F    13845
            U. S. A.        WWCR3             1500-1700 NA, Sa     13845
            U. S. A.        WWCR4             0000-0200 Af, Tu-Sa  7520
            U. S. A.        WWCR4             0200-0300 Af, Tu-Sa  5890
            U. S. A.        WWCR4             1900-2200 Af, Sa-Su  9980
            U. S. A.        WWCR4             2300-2400 Af, M-F    7520
            U. S. A.        WWRB              0000-0200 NA         3215
            U. S. A.        WWRB              0200-0500 NA         3195
            U. S. A.        WWRB              2200-2400 NA         3215
            Uganda          R. Lead Africa    0300-0400 Af, M,Tu,F 5915za
            Uganda          R. Lead Africa    0500-0600 Af, W,Th   12060za
            Uganda          R. Lead Africa    0500-0700 Af, Sa     12060za
            Uganda          R. Lead Africa    1900-2200 Af, Sa-Su  7425za
            Ukraine         R. Ukraine Int'l  0200-0230 eNA, Eu    11580wr(Tu-Sa)
            Ukraine         R. Ukraine Int'l  2330-2400 eNA,Eu M-F 11580wr
            United Kingdom  BBC               0000-0200 As         5970om
            United Kingdom  BBC               0200-0300 As         6155om
            United Kingdom  BBC               0300-0400 ME         6195om, 9410om
            United Kingdom  BBC               0400-0500 Af         9915as, 12095ae
            United Kingdom  BBC               0400-0500 ME         9410om, 12035om
            United Kingdom  BBC               0500-0600 Af         3255za, 5875as, 5925as, 6005as, 6190za, 12095za, 15420ma
            United Kingdom  BBC               0600-0700 Af         6005as, 6190za, 7325, 7345as, 7445za
            United Kingdom  BBC               0600-0700 Eu         3955 drm
            United Kingdom  BBC               0600-0700 Af         12095za, 15420ma, 17640ae
            United Kingdom  BBC               0700-0800 Af         6190za, 7445za, 9915as, 11770as, 12095as, 15400za, 15420ma, 17830za
            United Kingdom  BBC               0800-0900 As         17790si drm
            United Kingdom  BBC               1000-1100 As         6195si, 9740si, 11895si, 15285si
            United Kingdom  BBC               1100-1200 As         6195si, 9740si, 15285si
            United Kingdom  BBC               1200-1300 As         6195si, 9740si, 11895si
            United Kingdom  BBC               1300-1400 As         9410om
            United Kingdom  BBC               1400-1500 As         9410om
            United Kingdom  BBC               1500-1600 Af         12095ma, 15420za
            United Kingdom  BBC               1500-1600 ME         7405om
            United Kingdom  BBC               1500-1630 As         9540si, 9940ch
            United Kingdom  BBC               1600-1700 Af         3255za, 6190za, 7445ma, 12095za, 17640as, 17830as
            United Kingdom  BBC               1600-1700 ME         7405om
            United Kingdom  BBC               1700-1800 Af         3255za, 6190za, 7445ma, 9410za, 15400as, 17780as, 17830as
            United Kingdom  BBC               1700-1900 ME         6195om
            United Kingdom  BBC               1800-1900 Af         3255za, 6190za, 7445ma, 9410ae, 9915
            United Kingdom  BBC               1800-1900 Af         11810as, 15400as
            United Kingdom  BBC               1900-2000 Af         3255za, 6190za, 7445ma, 9410ae
            United Kingdom  BBC               1900-2000 Af         11810as, 15400as
            United Kingdom  BBC               2000-2100 Af         11810as, 12095as
            United Kingdom  BBC               2100-2200 Af, M-F    9915as, 11810as, 12095as
            United Kingdom  BBC               2200-2300 As         3915si, 5905om, 5960om, 6195si, 7205om, 7300om, 9890om
            United Kingdom  BBC               2300-2400 As         3915si, 6195si
            United Kingdom  Bible Voice       0445-0515 ME, Su     7325ge
            United Kingdom  Bible Voice       0800-0830 wEu, Su    7220ge
            United Kingdom  Bible Voice       1200-1230 As, Sa     21480ma
            United Kingdom  Bible Voice       1230-1245 As, Sa     21480ma
            United Kingdom  Bible Voice       1400-1415 sAs, Sa    6260uz
            United Kingdom  Bible Voice       1400-1430 sAs, Sa    17510fr
            United Kingdom  Bible Voice       1430-1500 sAs, Sa    17510fr
            United Kingdom  Bible Voice       1730-1800 eAf, M     11790ge
            United Kingdom  Bible Voice       1800-1815 ME, F      9715au
            United Kingdom  Bible Voice       1800-1830 ME, Sa     9715au
            United Kingdom  Bible Voice       1800-2000 ME, Su     9715au
            United Kingdom  Bible Voice       1815-2000 ME, Sa     9715au
            United Kingdom  Bible Voice       1830-1930 eEu, Su    6030ge
            United Kingdom  Bible Voice       1930-2015 ME, Su     7425ge
            United Kingdom  Bible Voice       1930-2015 ME Su      7425ge
            United Kingdom  End Times Coming  1900-1930 wEu        11590bu
            United Kingdom  FEBA              1415-1430 As, M      9775sl
            Vanuatu         R. Vanuatu        0000-0700 Oc         7260
            Vanuatu         R. Vanuatu        0700-1900 Oc         7260
            Vanuatu         R. Vanuatu        0700-2000 Oc         3945
            Vanuatu         R. Vanuatu        2000-2400 Oc         7260
            Vatican City    Vatican R.        0730-0745 ME         11935
            Vatican City    Vatican R.        1130-1200 ME, F      15595, 17590
            Vatican City    Vatican R.        1530-1600 As, Sa     9510ph, 11700ph
            Vatican City    Vatican R.        1630-1700 Af         11625ma
            Vatican City    Vatican R.        1715-1730 ME         9700
            Vatican City    Vatican R.        2000-2027 Af         7365, 9660
            Vietnam         V. of Vietnam     0000-0030 LA         7315wh
            Vietnam         V. of Vietnam     0100-0130 LA         7315wh
            Vietnam         V. of Vietnam     1000-1030 As         9840, 12020
            Vietnam         V. of Vietnam     1130-1200 As         9840, 12020
            Vietnam         V. of Vietnam     1230-1300 As         9840, 12020
            Vietnam         V. of Vietnam     1330-1400 As         9840, 12020
            Vietnam         V. of Vietnam     1500-1530 As         9840, 12020
            Vietnam         V. of Vietnam     1600-1630 ME         7220
            Vietnam         V. of Vietnam     1600-1630 wEu        7280
            Vietnam         V. of Vietnam     1600-1630 wEu        9730
            Vietnam         V. of Vietnam     1600-1630 nAf        9550
            Vietnam         V. of Vietnam     1900-1930 wEu        7280, 9730
            Vietnam         V. of Vietnam     2030-2100 ME         7220
            Vietnam         V. of Vietnam     2030-2100 nAf        9550
            Vietnam         V. of Vietnam     2130-2200 wEu        7280, 9730
            Vietnam         V. of Vietnam     2330-2400 As         9840, 12020
            Yemen           R. Sanna          1800-1900 ME         6135
            Zambia          V. of Hope Africa 0500-0800 sAf, M-F   9680, 11680
            Zambia          V. of Hope Africa 1200-1700 sAf        9680
            Zambia          V. of Hope Africa 1200-1700 wAf        13680
            Zambia          V. of Hope Africa 1600-1900 sAf, M-F   4965, 6065
            Zambia          V. of Hope Africa 1700-2200 sAf        4965
            Zambia          V. of Hope Africa 1700-2200 wAf        6065
            Zambia          V.of Hope Africa  0500-0800 sAf, M-F   9680
            Zambia          V.of Hope Africa  0500-0800 wAf, M-F   11680
            Zambia          V.of Hope Africa  1200-1700 sAf, Sa-Su 9680
            Zambia          V.of Hope Africa  1200-1700 wAf, Sa-Su 13680
            Zambia          V.of Hope Africa  1600-1900 sAf, M-F   4965
            Zambia          V.of Hope Africa  1600-1900 wAf, M-F   6065
            Zambia          V.of Hope Africa  1700-1730 sAf, Su    9680
        """


if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [freq1] [freq2 ...]
          Search for shortwave frequencies in kHz.
        Options:
          -c  Print table by country
          -f  Print table by frequency
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-c"] = False  # Print table by country
        d["-f"] = False  # Print table by frequency
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cf")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "cf":
                d[o] = not d[o]
        if not args and not d["-c"] and not d["-f"]:
            Usage()
        return args


if 1:  # Core functionality

    def ConstructDictionary():
        dict = {}
        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue
            country, frequencies = line.split(":")
            country = country.strip()
            dict[country] = frequencies.split()
        return dict

    def PrintByCountry(dict):
        print("Frequencies in kHz by country:")
        out = defaultdict(list)
        for f in dict:
            for c in dict[f]:
                out[c].append(f)
        for c in sorted(out):
            print(f"{c}")
            for line in Columnize(out[c], indent=" " * 4):
                print(line)

    def PrintByFrequency(dict):
        print("By frequency in kHz:")
        out = deque()
        for f in dict:
            for c in dict[f]:
                out.append((f, c))
        for f, c in sorted(out):
            print(f"{f!s:8s} {c}")

    def Search(args, dict):
        found = deque()
        for arg in args:
            r = re.compile(arg, re.I)
            for f in dict:
                mo = r.search(str(f))
                if mo:
                    print(f, ", ".join(dict[f]))


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    dict = CCrane()
    if d["-f"]:
        PrintByFrequency(dict)
    elif d["-c"]:
        PrintByCountry(dict)
    else:
        Search(args, dict)

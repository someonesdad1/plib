from columnize import Columnize
from sig import sig

def Print_tpi():
    tpi_data = '''
        4 8 16 32 64 128
        4.5 9 18 36 72 144
        5 10 20 40 80 160
        5.5 11 22 44 88 176
        5.75 11.5 23 46 92 184
        7 14 28 56 112 224
        6.75 13.5 27 54 108 216
        6.5 13 26 52 104 208
        6 12 24 48 96 192
    '''
    tpi = []
    for i in tpi_data.strip().split("\n"):
        for j in i.split():
            tpi.append(float(j))
    def f(x):
        return int(x) if int(x) == x else x
    tpi = list(sorted(f(i) for i in tpi))
    print("Threading tpi:")
    for line in Columnize([str(i) for i in tpi], col_width=8, indent=" "*4):
        print(line)
    print("Pitches in mils:")
    p = list(1/i for i in tpi)
    for line in Columnize([f"{sig(i*1000, 4)}" for i in p], col_width=8, indent=" "*4):
        print(line)

def Print_feeds():
    def Print(data, in_or_out):
        feed = []
        for i in data.strip().split("\n"):
            for j in i.split():
                feed.append(float(j))
        feed = list(sorted(feed))
        print(f"\nFeeds with slide gear {in_or_out} (mils/rev):")
        for line in Columnize([f"{sig(i*1000, 4)}" for i in feed], col_width=8, indent=" "*4):
            print(line)
        print(f"Feeds with slide gear {in_or_out} (μm/rev):")
        for line in Columnize([f"{sig(i*25.4*1000, 4)}" for i in feed], col_width=8, indent=" "*4):
            print(line)
    data_slide_gear_in = '''
        0.03670 0.01830 0.00920
        0.03260 0.01630 0.00810
        0.02930 0.01470 0.00730
        0.02670 0.01340 0.00660
        0.02550 0.01270 0.00630
        0.02090 0.01050 0.00520
        0.02180 0.01090 0.00540
        0.02260 0.01130 0.00560
        0.02440 0.01220 0.00610
    '''.strip()
    data_slide_gear_out = '''
        0.00460 0.00220 0.00110
        0.00410 0.00200 0.00094
        0.00360 0.00180 0.00092
        0.00330 0.00170 0.00083
        0.00310 0.00160 0.00079
        0.00260 0.00130 0.00065
        0.00270 0.00136 0.00068
        0.00280 0.00140 0.00070
        0.00300 0.00150 0.00076
    '''.strip()
    Print(data_slide_gear_in, "in")
    Print(data_slide_gear_out, "out")

if __name__ == "__main__": 
    print('''
Clausing 12x36 lathe

Swing over bed = 6.08 inches = 154 mm
Swing over cross slide = 3.72 inches = 94 mm
'''[1:])
    Print_tpi()
    Print_feeds()

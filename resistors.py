'''
On-hand resistors
'''

from f import flt

resistors = None

def OnHand():
    'Return a list of on-hand resistors'
    l = '''
        0.025 0.18 0.2 0.27 0.33           1 2.2 4.6 8.3
        10.1 12 14.7 15 17.8 22 27 28.4 30 31.6 33 35 38.4 46.3 50 55.5 61.8 67
        75 78 81
        100 110 115 121 150 162 170 178 196 215 220 237 268 270 287 316 330 349
        388 465 500 513 546 563 617 680 750 808 822 980
        1k 1.1k 1.18k 1.21k 1.33k 1.47k 1.5k 1.62k 1.78k 1.96k 2.16k 2.2k 2.37k
        2.61k 2.72k 3k 3.16k 3.3k 3.47k 3.82k 4.64k 5k 5.53k 6.8k 6.84k 8k 8.3k
        9.09k
        10k 11.8k 12.1k 13.3k 15k 16.2k 17.8k 18k 19.5k 20k 22k 26.2k 33k 39k
        42.4k 46k 51k 55k 67k 75k 82k
        100k 120k 147k 162k 170k 180k 220k 263k 330k 390k 422k 460k 464k 560k
        674k 820k
        1M 1.2M 1.5M 1.7M 1.9M 2.2M 2.4M 2.6M 2.8M 3.2M 4M 4.8M 5.6M 6M 8.7M
        10M 16M 23.5M
    '''
    o = []
    for i in l.split():
        i = i.replace("k", "*1000")
        i = i.replace("M", "*1e6")
        o.append(flt(eval(i)))
    global resistors
    resistors = tuple(o)
OnHand()

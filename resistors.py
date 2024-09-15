'''
On-hand resistors
'''
#∞test∞# ignore #∞test∞#
import bisect
# This tuple is a sorted sequence of on-hand resistors
resistors = (
    0.025, 0.18, 0.2, 0.27, 0.33,

    1, 2.2, 4.6, 8.3,

    10.1, 12, 14.7, 15, 17.8, 22, 27, 28.4, 30, 31.6, 33, 35, 38.4, 46.3, 50, 55.5, 61.8, 67, 75,
    78, 81,

    100, 110, 115, 121, 150, 162, 170, 178, 196, 215, 220, 237, 268, 270, 287, 316, 330, 349, 388,
    465, 500, 513, 546, 563, 617, 680, 750, 808, 822, 980,

    1000, 1100, 1180, 1210, 1330, 1470, 1500, 1620, 1780, 1960, 2160, 2200, 2370, 2610, 2720,
    3000, 3160, 3300, 3470, 3820, 4640, 5000, 5530, 6800, 6840, 8000, 8300, 9090,

    10000, 11800, 12100, 13300, 15000, 16200, 17800, 18000, 19500, 20000, 22000, 26200, 33000,
    39000, 42400, 46000, 51000, 55000, 67000, 75000, 82000,

    100000, 120000, 147000, 162000, 170000, 180000, 220000, 263000, 330000, 390000, 422000,
    460000, 464000, 560000, 674000, 820000,

    1000000, 1200000, 1500000, 1700000, 1900000, 2200000, 2400000, 2600000, 2800000, 3200000,
    4000000, 4800000, 5600000, 6000000, 8700000,

    10000000, 16000000, 23500000)
def FindClosest(R, favor_highest=True):
    '''Return the closest on-hand resistor.  If less than the smallest or
    greater than the largest, None is returned.
    '''
    def find_le(a, x):
        'Find rightmost value less than or equal to x'
        i = bisect.bisect_right(a, x)
        if i:
            return a[i-1]
        return None
    def find_ge(a, x):
        'Find leftmost item greater than or equal to x'
        i = bisect.bisect_left(a, x)
        if i != len(a):
            return a[i]
        return None
    if R < min(resistors) or R > max(resistors):
        return None
    less = find_le(resistors, R)
    more = find_ge(resistors, R)
    if less is None and more is not None:
        return more
    elif less is not None and more is None:
        return less
    elif less is None and more is None:
        return None
    else:
        # Return whichever is closer to desired R
        L, m = abs((less - R)), abs((more - R))
        if L == m:
            return more if favor_highest else less
        else:
            return less if L <= m else more
def OnHand():
    'Return a list of on-hand resistors'
    # Use this to remake the above resistors tuple
    L = '''
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
    for R in L.split():
        x = float(eval(R.replace("k", "*1000").replace("M", "*1e6")))
        o.append(int(x) if x == int(x) else x)
    return tuple(sorted(list(set(o))))
if __name__ == "__main__":  
    print(OnHand())

'''
BB gun target
'''
from g import *
line_width  = 0.0075
def DrawTarget(X, Y, size):
    push()
    translate(X, Y)
    move(0, 0)
    N = 5
    dr = size/(2*N)
    for i in range(1, N+1):
        r = i*dr
        circle(2*r)
        push()
        move(0, r - dr/1.4)
        ctext("%d" % (N-i+1))
        pop()
    fillOn()
    circle(size/40)
    pop()
def Target(file):
    s = SetUp(file, portrait, inches)
    width = 8.5
    height = 11
    nx = 2
    ny = 3
    dx = width/(2*nx)
    dy = height/ny
    D = 3
    translate(width/2, height/2)
    lineWidth(0.05)
    DrawTarget(-dx, -dy, D)
    DrawTarget(-dx,  0 , D)
    DrawTarget(-dx,  dy, D)
    DrawTarget( dx, -dy, D)
    DrawTarget( dx,  0 , D)
    DrawTarget( dx,  dy, D)
    s.close()
Target("out/target_bb.ps")

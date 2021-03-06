'''Get the next character typed at the keyboard
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   No specific license; as it was mostly copied from the URL below,
    #   see that site for any license coverage.
    #∞license∞#
    #∞what∞#
    # <programming> Get the next character typed at the keyboard.  Works
    # on Posix systems.
    #∞what∞#
    #∞test∞# ignore #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import termios
    import fcntl
def kbhit(block=True):
    '''Get the next character typed at the keyboard.  If block is True,
    then wait for the key to be pressed, otherwise return immediately.
    This is for Linux; under Windows, use
        from msvcrt import kbhit
    for similar functionality.
 
    *****************************************************************
    WARNING:  this only returns the first byte in the keyboard buffer
    and, thus, will probably not give you what you want if you want to
    detect function keys, arrow keys, etc.
    *****************************************************************
    '''
    # From
    # http://stackoverflow.com/questions/9882985/capture-keystrokes-for-a-game-python
    fd = sys.stdin.fileno()
    oldattr = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    if block:
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    else:
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    try:
        while True:
            try:
                c = sys.stdin.read(1)
                return c
            except IOError:
                return None
    finally:
        # This code is executed before returning:  Reset to old terminal
        # characteristics.
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldattr)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
if __name__ == "__main__":
    # Run as a script for a demonstration
    print("Type 'q' to exit")
    while True:
        c = kbhit()
        if c == "q":
            break
        o = ord(c)
        s = c if o >= ord(" ") else ''
        print(f"char = '{s}'  ord(char) = {o:3d} (0x{o:02x})")

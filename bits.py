_pgminfo = '''
<oo 
    Utilities to help dealing with binary bits
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test run oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        pass
if 1:   # Functions
    def ByteReverseDict():
        '''Return a dictionary that reverses the bits in a byte.  Example:
            di = ByteReverseDict()
            di[0b11001010] returns
               0b01010011
        '''
        # Method from
        # https://stackoverflow.com/questions/2602823/in-c-c-whats-the-simplest-way-to-reverse-the-order-of-bits-in-a-bytbytee
        def f(num):
            num = (num & 0xf0) >> 4 | (num & 0x0f) << 4
            num = (num & 0xcc) >> 2 | (num & 0x33) << 2
            num = (num & 0xaa) >> 1 | (num & 0x55) << 1
            return num
        if not hasattr(ByteReverseDict, "dict"):
            di = {}
            for i in range(256):
                di[i] = f(i)
            ByteReverseDict.dict = di
        return ByteReverseDict.dict
                

if __name__ == "__main__":
    from lwtest import run, Assert
    def Test_ReverseBitsInByte():
        di = ByteReverseDict()
        for i in range(256):
            Assert(f"{i:08b}" == ''.join(reversed(f"{di[i]:08b}")))
    exit(run(globals(), halt=True)[0])

'''
Implementation of a homogeneous list.  It's used as an example in the
/doc/Python.odt document.
'''

class HomogenousList(list):
    '''A homogenous list which allows items only of a single type.  The
    first element of the sequence provided to the constructor determines
    the type of objects allowed to be stored in the container.
    '''
    def __init__(self, seq=None):
        self.super = super(HomogenousList, self)
        self.type = None
        if seq is not None and seq:
            self.type = type(seq[0])
            for item in seq:
                self._check_type(item)
                self.append(item)
    def _check_type(self, item):
        if not isinstance(item, self.type):
            raise ValueError("item must be of type {}".format(self.type))
    def append(self, item):
        if self.type is None:
            self.type = type(item)
        self._check_type(item)
        self.super.append(item)
    def extend(self, seq):
        for item in seq:
            self.append(item)
    def insert(self, i, item):
        self._check_type(item)
        self.super.insert(i, item)
    def __add__(self, seq):
        try:
            for item in seq:
                self.append(item)
        except TypeError:
            raise TypeError("Item being added must be a sequence")

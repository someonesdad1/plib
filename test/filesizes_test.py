from filesizes import FileInfo
import pathlib
from lwtest import run, assert_equal, raises

from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

def Test_FileInfo():
    # Single file
    file = "atm.f90"
    fi = FileInfo("atm.f90")
    pth, fs = list(fi.items())[0]
    assert(isinstance(pth, pathlib.Path))
    assert(fs.size == 4617)
    assert(fs.hash == 'ba5d4ba43e37103eee7bdd83ace307b4a190ed0b')
    # Globbing pattern in sequence.  Note these test some files that
    # shouldn't change over time.
    fi = FileInfo(["loo_image?.png"])
    for i, f in enumerate(fi):
        file = str(f)
        info = fi[f]
        assert(file == f"loo_image{i + 1}.png")
        if i == 0:
            assert(info.size == 3676)
        elif i == 1:
            assert(info.size == 4009)
        elif i == 2:
            assert(info.size == 4097)
        else:
            raise Exception("Unexpected number of files")

if __name__ == "__main__":
    exit(run(globals(), halt=True, dryrun=False)[0])

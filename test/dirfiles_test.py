import os
import pathlib
from lwtest import run, assert_equal, raises
from dirfiles import Dirfiles
from threading import Thread, Lock
from pdb import set_trace as xx 
from pprint import pprint as pp

P = pathlib.PosixPath
image_list = "img1.png img2.png".split()
filea = "file.a"
images = set([P(i) for i in image_list])
dir = "dirfiles"

def init():
    'Return an instance with no files'
    os.chdir(Setup.cwd)     # Go back to starting directory
    # Change to the test directory
    os.chdir(dir)
    return Dirfiles(".", clear=True)

def Test_globbing():
    a = init()
    a.add("*.png")
    for i in images:
        assert(i in a.files)
    a.update()
    for i in images:
        assert(i not in a.files)
        assert(i in Dirfiles.files)

def Test_size():
    a = init()
    a.add("*.png")
    assert(a.size >= len(images))

def Test_dir():
    '''This assumes the parent directory has more files than the current
    directory.
    '''
    a = init()
    a.add("*")
    n = a.size
    a.update()
    assert(not a.size)
    a.dir = ".."
    a.add("*")
    m = a.size
    assert(m and m > n)

def Test_get():
    a = init()
    a.add("*.png")
    f = a.get
    assert(f == images)
    a.update()
    f = a.get
    assert(not f and f != images)

def Test_get_all():
    a = init()
    a.add("*.png")
    a.update()
    f = a.get_all
    assert(f == images)

def Test_clear():
    a = init()
    a.add("*.png")
    assert(a.size)
    assert(not len(Dirfiles.files))
    a.update()
    a.add("*.png")
    assert(a.size)
    assert(len(Dirfiles.files))
    a.files.clear()
    assert(not a.size)
    assert(len(Dirfiles.files))
    a.clear()
    assert(not a.size)
    assert(not len(Dirfiles.files))

def Test_update():
    a = init()
    a.add("*.png")
    assert(not Dirfiles.files)
    a.update()
    assert(Dirfiles.files == images)
    assert(not a.files)

def Test_keepext():
    a = init()
    a.add("*")
    assert(a.size == 3)
    a.keepext("png")
    assert(P(filea) not in a.files)

def Test_keep():
    a = init()
    a.add("*")
    a.keep("file")
    assert(P(filea) in a.files)

def Test_rmr():
    a = init()
    a.add("*")
    n = a.size
    a.rmr(r"^img.?\.png$")
    assert(a.size == n - 2)

def Test_rm():
    a = init()
    a.add("*")
    n = a.size
    a.rm("dkjfdkjfdkjfd")   # No exception, no change
    assert(a.size == n)
    a.rm(filea)
    assert(a.size == n - 1)
    a.add(filea)
    assert(a.size == n)
    a.add(filea)
    assert(a.size == n)
    # Verify multiple items are removed when a string is given
    assert(P("img1.png") in a.files)
    assert(P("img2.png") in a.files)
    assert(P(filea) in a.files)
    assert(a.rm("img") == 2)
    assert(P("img1.png") not in a.files)
    assert(P("img2.png") not in a.files)
    assert(P(filea) in a.files)
    # Check that exact works
    a = init()
    a.add("*")
    n = a.size
    a.rm("img", exact=True)
    assert(a.size == n)
    a.rm("img1.png", exact=True)
    assert(a.size == n - 1)

def Test_add():
    a = init()
    nonexistent = ";;nonexistent;;"
    # Get exception for nonexistent file or directory
    raises(ValueError, a.add, nonexistent, ignore=False)
    a.add("*.png")
    assert(a.size == 2)
    # Ignore exception if ignore set
    raises(ValueError, a.add, nonexistent, ignore=True)

def Test_threading():
    '''Show that two threads with different instances have access to the
    same Dirfiles.files data.
    '''
    a = init()
    a.add("*.png")
    a.update()
    assert(Dirfiles.files == images)
    lock = Lock()
    def Process(s):
        lock.acquire()
        assert(Dirfiles.files == images)
        # Add the 'files.a' file
        b = Dirfiles(".")
        b.add(filea)
        b.update()
        lock.release()
    t = Thread(name="Thd", target=Process, args=(a.get,))
    t.start()
    # Block until the started thread returns
    lock.acquire()
    # Show that Dirfiles.files now has filea.
    s = images.copy()
    s.add(P(filea))
    assert(s == Dirfiles.files)

def Setup():
    '''Create a dirfiles directory that will contain the three empty files
    '''
    Setup.cwd = os.getcwd()
    if not P(dir).exists():
        os.mkdir(dir)
    os.chdir(dir)
    # Create three empty files
    for file in image_list:
        if not P(file).exists():
            open(file, "w")
    if not P(filea).exists():
        open(filea, "w")

def Teardown():
    os.chdir(Setup.cwd)     # Go back to starting directory
    os.chdir(dir)
    for file in image_list:
        if P(file).exists():
            os.remove(file)
    if P(filea).exists():
        os.remove(filea)
    os.chdir(Setup.cwd)     # Go back to starting directory
    os.rmdir(dir)

def Test_get_directories():
    os.chdir(Setup.cwd)     # Go back to starting directory
    a = Dirfiles(".", clear=True, getdirs=True)
    a.add("*")
    if a.size == 1:
        assert(a.files == set([P(dir)]))
    else:
        assert(P(dir) in a.files)
    # Check we have recursion and that repos are seen
    os.chdir("../pgm")  # Will be /pylib/pgm
    a = Dirfiles(".", clear=True, getdirs=True, ignore_repo=False)
    a.add("**/*")
    assert(P("ts") in a.files)
    assert(P("ts/.hg") in a.files)
    # Check we have recursion and that repos are not seen
    a = Dirfiles(".", clear=True, getdirs=True, ignore_repo=True)
    a.add("**/*")
    assert(P("ts") in a.files)
    assert(P("ts/.hg") not in a.files)
    # Go back to starting directory
    os.chdir(Setup.cwd)
    
if __name__ == "__main__":
    Setup()
    status = run(globals(), halt=True)[0]
    Teardown()
    exit(status)

import sys
from lwtest import run, assert_equal, raises
from gettokens import GetTokens, GetWords, Tokenize
import io
from pdb import set_trace as xx

sio = io.StringIO


def TestGetTokens():
    m = "Cat et rat"
    s = sio(m)
    g = GetTokens(s)
    t = g.__next__()
    assert t == "Cat"
    t = g.__next__()
    assert t == "et"
    t = g.__next__()
    assert t == "rat"
    with raises(StopIteration):
        t = g.__next__()
    # convert function to make each token uppercase
    s = sio(m)
    c = lambda x: x.upper()
    g = GetTokens(s, convert=c)
    t = g.__next__()
    assert t == "CAT"
    # fltr
    s = sio(m)
    f = lambda x: "".join(list(reversed(x)))
    g = GetTokens(s, fltr=f)
    t = g.__next__()
    assert t == "tar"
    # Other separator
    m = "Cat|et|rat"
    s = sio(m)
    g = GetTokens(s, sep="|")
    t = g.__next__()
    assert t == "Cat"
    t = g.__next__()
    assert t == "et"
    t = g.__next__()
    assert t == "rat"
    with raises(StopIteration):
        t = g.__next__()


def TestGetWords():
    m = "This is\n a test"
    s = sio(m)
    words = GetWords(s)
    assert words == set(m.split())
    m1 = "  # A comment\n" + m
    s = sio(m1)
    more = GetWords(s)
    assert more == words
    # Change case
    s = sio(m)
    w = GetWords(s, case="upper")
    assert w == set(m.upper().split())
    s = sio(m)
    w = GetWords(s, case="lower")
    assert w == set(m.lower().split())
    # Comment string
    m1 = "  ;;; A comment\n" + m
    s = sio(m1)
    more = GetWords(s, comment_char=";;;")
    assert more == words
    # String argument
    more = GetWords(m1, comment_char=";;;", isstring=True)
    assert more == words
    # Using an existing set
    s = set(("cheetah",))
    more = GetWords(m, comment_char=";;;", isstring=True, existing_set=s)
    cheetah = words.add("cheetah")
    assert more == cheetah


def TestTokenize():
    s = '"Hello", said the rabbit\'s sister.'
    if 0:
        # Default behavior
        l = Tokenize(s, remove_punct=False, asciify=False)
        e = ['"', "Hello", '"', ",", "said", "the", "rabbit's", "sister", "."]
        assert l == e
        # Remove punctuation
        l = Tokenize(s, remove_punct=True, asciify=False)
        e = ["Hello", "said", "the", "rabbit's", "sister"]
        assert l == e
    # Remove possessive single quotes
    l = Tokenize(s, remove_punct=True, asciify=False, no_possessives=True)
    e = ["Hello", "said", "the", "rabbits", "sister"]
    assert l == e
    # ASCIIfy Unicode quotes
    s = '"Hello", said the rabbit\u2019s sister.'
    l = Tokenize(s, asciify=True)
    e = ['"', "Hello", '"', ",", "said", "the", "rabbit's", "sister", "."]
    assert l == e


if __name__ == "__main__":
    exit(run(globals())[0])

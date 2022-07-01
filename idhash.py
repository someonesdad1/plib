'''

Hashes a set of string answers to a set of questions.  This is intended to
to provide a secure hash that no one else can guess, even if given this
script and questions.  This is because you select questions that no one
else would know all the answers to.  They should have reasonably long
answers that also preclude a brute force attack.

Update 1 Jul 2022:  Changed to sha3_512 hash, as SHA-1 is considered weak.
Also added a prompt for the number of passes, which is another secret you
should keep.  Here's a use case for multiple passes:

    Suppose you publish a document that you want to write anonymously, but
    include a hash that only you know how to generate in case you ever want
    to verify your authorship.  You'd include this function's code and the
    questions in the document.  You'd keep the number of hashes secret.
    Generate the hashes and only keep the last two.   Give the
    second-to-last hash to the person you're verifying your authorship with
    and have them hash it to see that it gives the displayed last hash,
    which is what you include in the document.  This proves you know how
    the document's hash was generated or you were able to find a hash
    collision.

'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Hashes answers to a set of questions to provide a
        # secure hash value.
        #∞what∞#
        #∞test∞# ignore #∞test∞#
    # Imports
        import hashlib
        import sys
        from getpass import getpass
        from string import whitespace
        from wrap import dedent
def AnswerQuestions(questions, remws=True, lc=True, visible=False, test=None):
    '''Return the answer string by prompting the user for each question in
    the sequence questions.  
 
    remws       If True, remove all whitespace in the answers.
    lc          If True, change returned answers to lowercase.
    visible     If True, echo answers to the screen.
    test        If not None, return the test string as the result.
    '''
    print(dedent('''
    Enter the answers to the following questions.  Whitespace
    and case are ignored; backspace erases characters.
    '''))
    answers = []
    if test:
        answers = [test]
    else:
        for question in questions:
            print(question)
            answer = input() if visible else getpass("")
            answers.append(answer)
    answer = ''.join(answers)
    if remws:
        for i in whitespace:
            answer = answer.replace(i, "")
    if lc:
        answer = answer.lower()
    return answer
def HashAnswer(answer, hash, truncate=None, passes=2):
    '''passes defaults to 2 to handle the following case.  Suppose you
    publish a document that you want to write anonymously, but include a
    hash that only you know how to generate in case you ever want to verify
    your authorship.  You'd include 1) this function's code and 2) the
    questions in the document and the resulting 2-pass hash.  If you later
    needed to verify the hash in front of someone, you'd give them the
    first hash that would hash into the second.  This means you wouldn't
    have to expose the answers to the questions.  The person(s) viewing
    this would then either believe you were the author or that you had
    found a suitable collision for that hash.
    '''
    hash_string = answer
    for i in range(passes):
        h = eval(f"hashlib.{hash}()")
        h.update(hash_string.encode("utf8"))
        hash_string = h.hexdigest()
        print(f"pass {i}: {hash_string[:truncate]}")
    if truncate is not None:
        hash_string = hash_string[:truncate]
    return hash_string
def NumberOfPasses():
    while True:
        s = input("How many passes (q to quit, defaults to 2)? ")
        if s == "q":
            exit(0)
        elif not s.strip():
            return 2
        try:
            n = int(s)
            if n > 1:
                return n
            print("Must be > 1")
        except Exception:
            pass
if 0:
    # The old version of this file used SHA-1, but it is no longer considered
    # secure.
    #
    # Answer 'a' to every question and you should get the SHA-1 hash
    # 3aa25c07b73e196ecda364043a270ee9bb8143e2 
    # (on system with python 3.7.10)
    # 
    # With the correct answers the hash was
    # 7512c8ea046f930c6cb8c805ecf5c988f44ea9ad
    hashfunc = "sha1"
    vis = False
    answer, hash = ID_Hash(questions, visible=vis, show=vis, hash=hashfunc)
    print("Using", hashfunc, "hash")
    print("Hash =", hash)
    print("Orig = 7512c8ea046f930c6cb8c805ecf5c988f44ea9ad")

if __name__ == "__main__":
    dbg = False
    passes = NumberOfPasses()
    questions = [
        "Vernon's phone number?",
        "DLN of Zazu's youngest daughter?",
        "Phone extension?",
        "Phone password?",
        "Gary E.'s password?",
        "Dave R.'s old computer's password?",
    ]
    if dbg:
        answer = AnswerQuestions([], test="aaaaaa")
    else:
        answer = AnswerQuestions(questions, visible=0)
    use_hash = "sha3_512"
    print(f"{use_hash:10s} {HashAnswer(answer, use_hash, truncate=64, passes=passes)}")
    print(dedent('''
    --------------------------------------------------------------------------------
    Expected hash for answering 'a' to each question:
      sha3_512 = 793aa316ab694fc3f1eca4005fbaab6450d2b7e62beefc3d0cd9aa5d93b49ceb
    Expected hash for correct answers:
      sha3_512 = 0fe4057ee111e854039dc24dee820528b1b9fd442af17ab90352fdc3db6efa47
    '''))

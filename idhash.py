'''
Hashes the string answers to a set of questions.  This is intended to allow
me to have a secure hash that is nearly certain that no one else would be
able to guess, even if given this script.  This is because no one would
know all the answers to the questions below.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Hashes answers to a set of questions
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import hashlib
    from getpass import getpass
def ID_Hash(questions, remws=True, lc=True, visible=False,
            hash="sha1", truncate=None, show=False, passes=2):
    '''Returns a tuple (a, hash) where a is the answer string that was
    hashed (is None if show is False) and hash is the indicated hash of
    the answer string.  The answers are gotten to the questions (you can
    see the answers on the screen if visible is True); then whitespace
    is removed if remws is True and the string is converted to lower
    case if lc is True.  The answer is converted to bytes using UTF-8
    encoding and the hash is then taken of the resulting string;
    see the number of passes below for exactly what happens.
 
    Keyword parameters:
 
    remws [bool]
        Remove any whitespace before hashing (whitespace is defined to
        be newlines, carriage returns, tabs, or space characters).
 
    lc [bool]
        Change the string to lower case before hashing
 
    visible [bool]
        Show the text of the answers on the screen.
 
    hash [string]
        Defines which hash function to use.
 
    truncate [int]
        If not None, must be an integer > 0.  Truncate the returned hex
        string to this many characters.
 
    show [bool]
        Print the resulting string that is hashed.
 
    passes [int]
        Specify the number of passes through the hash algorithm.  2
        means the composite answer string is hashed, then the hex digest
        of that string is hashed again with the same algorithm.
 
    passes defaults to 2 to handle the following case.  Suppose you
    publish a document that you want to write anonymously, but include a
    hash that only you know how to generate in case you ever want to
    verify your authorship.  You'd include this function's code and the
    questions in the document and the resulting 2-pass hash.  If you
    later needed to verify the hash in front of someone, you'd give them
    the first hash that would hash into the second.  This means you
    wouldn't have to expose the answers to the questions.  The person(s)
    viewing this would then either believe you were the author or that
    you had found a suitable collision for that hash.
    '''
    answers = []
    for question in questions:
        print(question)
        answer = input() if visible else getpass("")
        answers.append(answer)
    answer = ''.join(answers)
    if remws:
        for i in " \t\n\r":
            answer = answer.replace(i, "")
    if lc:
        answer = answer.lower()
    hash_string = answer
    for i in range(passes):
        m = eval("hashlib.{}()".format(hash))
        m.update(hash_string.encode("utf8"))
        hash_string = m.hexdigest()
    if truncate is not None:
        hash_string = hash_string[:truncate]
    if not show:
        answer = None
    return (answer, hash_string)

if __name__ == "__main__":
    # Answer 'a' to every question and you should get the hash
    # 3aa25c07b73e196ecda364043a270ee9bb8143e2 
    # (on system with python 3.7.10)
    print('''Enter the answers to the following questions.  Whitespace
and case are ignored; backspace erases characters.
''')
    q = [
        "Vernon's phone number",
        "DLN of Zazu's youngest daughter?",
        "Phone extension?",
        "Phone password?",
        "Gary E.'s password?",
        "Dave R.'s old computer's password?",
    ]
    hashfunc = "sha1"
    vis = True
    vis = False
    answer, hash = ID_Hash(q, visible=vis, show=vis, hash=hashfunc)
    if answer is not None:
        print("Answer =", repr(answer))
    print("Using", hashfunc, "hash")
    print("Hash =", hash)
    print("Orig = 7512c8ea046f930c6cb8c805ecf5c988f44ea9ad")

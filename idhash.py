'''
Hashes a set of string answers to a set of questions.  
    Returns a hash string that would be hard to guess, even if given this script
    and questions.

    Example of use:  Suppose you write an anonymous document, but want to leave
    information in the document to help prove you were the author.  To do this, 
        - Include this script's code in the document (or a pointer to it)
        - Choose a set of questions that you know the answers to
        - Use this script to generate a hash string from the answers to the questions
            - Include the resulting hash string in the document
        - Other secret information you must remember:
            - Keywords to the AnswerQuestions() function:
                - remws     Whether to remove whitespace
                - lc        Whether to convert answers to lower case
            - Keywords to the HashAnswer() function:
                - hashfunc  Which hashlib function is used for hashing
                - truncate  How many hex digits in the resulting hex digest
                - passes    How many passes were made
    
    Suppose you use a set of n symbols for answers.  The string that makes up the answer
    to all your set of questions can be from 1 to p symbols long.  To do a brute force
    calculation of all the possible hashes, there will be 

        N = (number of 1 character strings) + (number of 2 character strings) + ... +
            (number of p character strings)
        N = n + n**2 + n**3 + ... + n**p 

    possible strings made up of the n symbols.  This is well-approximated by n**p.

    As an example, suppose you use two ten-digit phone numbers that use the digits 0, 1,
    ..., 9.  There are 10**(2*10) or 1e20 of these possible strings.  A brute force
    checking tool that did 1e11 comparisons per second would take 1e20/1e11 = 1e9 s to
    look at all the possibilities -- this is 32 years, still probably out of the range
    most individuals.  1e11 checks per second is the approximate speed of modern hash
    checking hardware.

'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Hashes a set of string answers to a set of questions oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import hashlib
        import getpass
        import string
    if 1:  # Custom imports
        import wrap
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def AnswerQuestions(questions, remws=True, lc=True, visible=False, test=None):
        '''Return the answer string by prompting the user for each question in
        the sequence questions.
            remws       If True, remove all whitespace in the answers.
            lc          If True, change returned answers to lowercase.
            visible     If True, echo answers to the screen.
            test        If not None, return the test string as the result.
        '''
        print("Enter the answers to the following questions:")
        answers = []
        if test:
            answers = [test]
        else:
            for question in questions:
                print(question)
                response = input() if visible else getpass.getpass("")
                #t.print(f"{t.purl}answer = {response!r}")
                answers.append(response)
        answer = ''.join(answers)
        if remws:
            for i in string.whitespace:
                answer = answer.replace(i, "")
        if lc:
            answer = answer.lower()
        return answer
    def HashAnswer(answer, hashfunc=hashlib.sha3_512, truncate=None, passes=2, show=False):
        '''Hash the string the number of times in passes using the hashlib function
        hashfunc and return the hash's hexdigest string.
            truncate    Limit the hexdigest to this number of hex digits
            passes      Number of times to hash the string
            show        Print the resulting hex digits for each pass
        '''
        assert isinstance(answer, str)
        hash_string = answer
        for i in range(passes):
            h = eval(f"hashlib.{hashfunc}()")
            h.update(hash_string.encode("utf8"))
            hash_string = h.hexdigest()
            if show:
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

if __name__ == "__main__":
    import trm
    t = trm.Trm()
    questions = (
        "Vernon's phone number before 1970?",
        "DLN of Zazu's youngest daughter?",
        "HP phone?",
        "HP password?",
        "Gary E.'s password?",
        "First HP-UX password?",
    )
    dbg = False
    #dbg = True
    passes = NumberOfPasses()
    if dbg:
        t.print(f"{t.redl}Debugging on:  all questions answered with ''")
        answer = AnswerQuestions([], test="")
    else:
        answer = AnswerQuestions(questions, visible=0)
    use_hash = "sha3_512"
    t.ans = t.sky
    t.exp = t.ornl
    t.print(f"{use_hash:10s} {t.ans}{HashAnswer(answer, use_hash, truncate=64, passes=passes)}")
    print(wrap.dedent(f'''
    --------------------------------------------------------------------------------
    Expected hash for answering '' to each question:
        sha3_512 {t.ans}203b36aac62037ac7c4502aa023887f7fcae843c456fde083e6a1dc70a29f3d6{t.n}
    Expected hash for correct answers:
        sha3_512 {t.exp}0fe4057ee111e854039dc24dee820528b1b9fd442af17ab90352fdc3db6efa47{t.n}
    '''))
    

'''

Script to generate hard-to-crack passwords

    Method 1:  uses secrets module and a list of words to randomly select words from the list.  You
    specify the number of words, the list of words, and the number of lines to generate.


Method 2
    - Script to ask a bunch of questions, concatenate your responses, and deliver a desired hash of
      the response data.
    - The script will number and output the questions along with the hashed answer.
    - With a good set of questions, it is unlikely anyone could crack things, especially if the
      answers have numerous characters in them.

Example of method 2:
    - Here are a set of questions with answers in double quotes:
        - Name Donald Duck's nephews
            - "Huey Dewey Louie"
        - Name of the duck that the cat loved to wipe its tail under
            - "Daddles"
        - So-and-so's phone number
            - "916-456-7890"
    - The answer strings are concatenated to get the string to be hashed:
        - "Huey Dewey LouieDaddles916-456-7890"
    - The command line options to the program are used to transform the input string to make it
      easier to tolerate input differences later
        - -i is used to ignore case
        - -p is used to remove punctuation
        - -w is used to remove whitespace
    - If all these options were used, the string to be hashed is 
        - "hueydeweylouiedaddles9164567890"
        - Even if you knew the string had 21 letters and 10 digits, you'd still be faced with
          26**21*10**10 = 5e39 combinations that must be tried in a brute-force attack.
    - A bitcoin mining website in Nov 2023 gave a $3.2k Bitmain AntMiner S19 Pro's hash speed at
      110 Th/s or 1e14 Hz.  Suppose you could afford a million of these machines ($3e9), giving you
      a brute force checking rate of 1e20 Hz.  You'd need 1e39/1e20 = 1e19 s to check all the
      possibilities, which larger than 4e17 s, the age of the universe.

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Questions to help generate a password
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import random
        import secrets
        import sys
    if 1:   # Custom imports
        from wrap import dedent
    if 1:   # Global variables
        class G:
            pass
        g = G()     # Global variables as attributes to this instance
        g.words = (
            P("/words/words.ef.3000"),
            P("/words/words.beale.2of12inf"),
            P("/words/words.ngsl.experimental"),
            P("/words/words.univ"),
        )
        g.wordlist = None
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''

        The cartoon https://xkcd.com/936/ pokes fun at humans' attempt to make secure passwords.
        As computers keep getting faster, they can more easily be used to crack passwords on
        systems by brute force searching.  Just as problematic, humans are often lax at password
        security, even if they have good passwords.  A good example is the secretary who can't
        remember the password he/she needs, so writes it on a Post-It note and puts it on the
        computer monitor.

        The trouble is caused by our inability to remember secure passwords like
        'fw2Sn,ZBzxYNdAH2KASPRkKl0jKelO0m', a random password of 32 characters generated by the
        password manager I use, which labeled this password as having 180 bits.  This problem is
        compounded by the large number of passwords we need today.

        One technique is to generate a set of words that you can remember.  This script does this
        for you, selecting from various lists of words.  

        Estimating Security
        -------------------

        A simple assessment of the security of a password involves 1) n = the size of the set of
        characters used and 2) m = the number of characters used in the password.  Then to "crack"
        the password by brute force, you'd have to try all mⁿ passwords that can be generated
        from these assumptions.  This is an elementary combinatoric argument.  Assume you use a
        password of length 2.  The first character can be chosen n different ways and the second
        character can be chose n different ways, giving n² possibilities.

        A measure of this number of possibilities is its base 2 logarithm, which is rounded to an
        integer and called 'bits'.  We have log2(mⁿ) = n*log2(m).  We can make a table of the
        number of bits as a function of m, the number of characters in your password.  If we assume
        the size of the set of characters used, let's assume it's only the lowercase letters and digits,
        meaning n = 36.

        Most people probably only use the 7-bit ASCII characters from 0x20 to 0x7e for their
        passwords, which is 95 characters.  The number of bits in a password with m characters is
        then about 6.5*m bits.  A basic problem with many websites is that they limit your
        character choices and length of the password you can choose.

        How many bits must you have in your password to feel secure?  The answer depends on the
        resources of the person or organization trying to get your password.  A good benchmark
        might be a single hacker with a modern desktop computer and graphics card.  A well-heeled
        attacker (e.g. corporation or government) could have orders of magnitude larger resources
        than this.  https://www.hivesystems.com/blog/are-your-passwords-in-the-green gives some
        hashing speeds of modern hardware.  I'll give these numbers in Hz, as this makes it easy to
        compare to frequencies.  The current hardware seems to be around 50 to 150 GHz.  150 GHz
        means computing hashes at 150e9 per second.  This, in turn, is useful if an attacker has
        gotten hold of e.g. a hashed password file from a computer and knows what hashing algorithm
        was used.


        The security of a password can be estimated by the number of bits that represent the number
        of passwords you'd have to try in a brute force search to guess the password.  The easiest
        password for brute force search is a symbol that's either 0 or 1.  Then you have to check
        two possible symbols.

        A more complicated password would be the 5-digit phone password I used in the 1980's at
        work.  How many 5 digit passwords using the digits 0 to 9 are there?  10**5 or one hundred
        thousand.  This was nicely secure, as an incoming caller would have to try all the possible
        numbers and typing these in on a phone would take too much time.

        The base 2 logarithm of the number of possible passwords is often used to estimate password
        strength.  It is usually rounded to an integer.

        The most straightforward measure of the effectiveness of a password is to calculate the 
        number of passwords that are "similar" to it, with similar meaning roughly the number
        of possible strings that can be generated by the set of characters you used and the number
        of characters in the password.  Here's an example.  Suppose we allow only lower case
        letters in our password, or 26 characters.  Add in the space character, the comma, and the
        semicolon.  This is a set of 29 characters.  If you then choose an n character password
        from this character set, you'd calculate that there are 29**n possible passwords.  Since
        the logarithm of 2 is 4.8 to two places, this is (2**4.8)**n or 2**(4.8*n).  Password
        strength is often estimated with the number of bits, which is the base 2 logarithm of the
        number of possible passwords.  Thus, our estimate here is 4.8*n bits.  Call it 5 bits per
        character. 

        Here's a table from around 2022
        (https://www.hivesystems.com/blog/are-your-passwords-in-the-green) that gives cracking time
        when the attacker knows the hash values.  I've rounded the values to 2 figures and these
        estimates change quickly with time.

        Columns:
            N   number of characters
            A   Number digits only used
            B   Lower case letters
            C   Upper and lower case letters
            D   Numbers and letters
            E   Numbers, letters, symbols

        The crack times are given the units:
            s = seconds, m = minutes, h = hours, d = days, m = months, y = years, c = century
            If a cell is empty, it means more than 1000 yearss.

            N       A       B       C       D       E
            8       0s      0s      1s      2s      4s
            10      0s      1m      21h     5d      14d
            12      1s      14h     6y      53y     230y
            14      52s     1y     
            16      1h      710y    
            18      6d      

        Such numbers are strongly dependent on the assumptions and hardware; the basic assumption
        likely is what a hacker could build with current hardware and graphics card.

        The major takeaway from the table is that crack times go up with 1) size of the set of the
        number of symbols used in the password and 2) the number of symbols in the password.

        Column E is probably limited to the ASCII 7-bit characters that include the letters, number
        digits, and punctuation.  These are the bytes from 0x20 to 0x7e or 95 characters.



        '''))
        exit()
    def Usage():
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] n [k [M [m]]]

          If only n is given, print a line of n randomly-selected words.  If k is given, print k
          lines of n words.  If M is given, limit the words to a maximum of M characters.  If m is
          given, the words must be at least m letters long.  The output is random and not
          repeatable unless you use the -s option.

        Options:
            -0      Simple wordlist (3000 words) [default]
            -1      Moderately-sized wordlist (16378 words)
                    excellent list of words from Alan Beale.
            -3      Complex wordlist (302618 words)
            -h      Print a manpage
            -s sd   Define seed to use repeatable pseudorandom generator
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-s"] = None      # Random number seed; implies pseudorandom number generator
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0123hs:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o[1] in list("0123"):
                g.wordlist = int(o[1])
            elif o == "-h":
                Manpage()
            elif o in ("-s",):
                d["-s"] = a
        if g.wordlist is None:
            g.wordlist = 0
        return args
if 1:   # Core functionality
    def Method1(*args):
        N, m = [int(i) for i in args]
        if N < 1:
            Error("N must be an integer > 0")
        if m < 1:
            Error("m must be an integer > 0")
        file = g.words[g.wordlist]
        assert file.exists()
        with open(file) as f:
            words = [word.strip() for word in f]
        if d["-l"]:
            # Keep words with d["-l"] letters or less
            words = [i for i in words if len(i) <= d["-l"]]
        if d["-m"]:
            # Keep words with d["-m"] letters or more
            words = [i for i in words if len(i) >= d["-m"]]
        if d["-s"] is None:
            # Random selection, cannot be repeated
            for i in range(m):
                password = ' '.join(secrets.choice(words) for i in range(N))
                print(password)
        else:
            # Pseudorandom number generator, same output for same seed
            random.seed(d["-s"])
            n = len(words)
            for linenum in range(m):
                o = []
                for i in range(N):
                    k = random.randint(0, n - 1)
                    o.append(words[k])
                print(' '.join(o))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if len(args) == 1:
        Method2(*args)
    elif len(args) == 2:
        Method1(*args)
    else:
        Usage()

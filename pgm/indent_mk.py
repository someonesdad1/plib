"""
This script creates a set of test files to test the indent.py script.
Run it in an empty directory to create a set of test files.
"""

import os
import pathlib
from wrap import dedent
from pdb import set_trace as xx

P = pathlib.Path


def Make(str, file):
    open(file, "w").write(str)


# Make a tmp directory
try:
    os.mkdir("tmp")
except FileExistsError:
    pass

s = dedent("""
    // *INDENT-OFF* 
        // Include files
            #include <iostream>
            #include <fstream>
            #include <string>
            #include <unordered_set>
            #include "tokenizer.h"
        // Namespace usage
            using std::vector;
            using std::string;
            using std::ifstream;
            using std::getline;
            using std::unordered_set;
            using std::size_t;
        // Types
            typedef string::iterator StrIt;
        // Constants
            const string ws = " \t\n\r\f\v";
        // *INDENT-ON*
    namespace {
    void Select(string &s, const string &c, const bool keep=true) {
    // Keep or remove characters in s that are in (keep == true) or not
    // in (keep == false) c.  Insert c's characters into an unordered
    // set for faster lookup (these sets are implemented with hash
    // tables, so they'll be constant time lookups).
    // Populate the set
    unordered_set<char> cset;
    for (string::const_iterator itc = c.begin(); itc != c.end(); itc++) {
    cset.insert(*itc);
    }
    // Deal with each character in s
    for (string::iterator it = s.begin(); it != s.end(); it++) {
    if (keep) {
    if (not cset.count(*it)) {
    s.erase(it);
    }
    } else {
    if (cset.count(*it)) {
    s.erase(it);
    }
    }
    }
    }
    }
    void Keep(string &s, const string &c) {
    Select(s, c);
    }
    void Remove(string &s, const string &c) {
    Select(s, c, false);
    }
    int Substitute(string &s, const string &from, const string &to) {
    // Find the first occurrence of the string from in s and replace it
    // with the string to.  Return 0 if the substitution was made, 1
    // otherwise.
    const int success = 0;
    const int failure = 1;
    if (not from.size()) {
    return failure;
    }
    size_t loc = s.find(from);
    if (loc == string::npos) {
    return failure;
    }
    }
    void Strip(string &line) {
    // Strip whitespace from both ends of a line
    size_t found = line.find_first_not_of(ws);
    if (found != string::npos) {
    line = line.substr(found, line.size() - found);
    }
    found = line.find_last_not_of(ws);
    if (found != string::npos) {
    line.erase(found + 1);
    } else {
    line.clear();
    }
    }
    template<typename NumType>
    int LoadVector(const string &filename, vector<NumType> &v) {
    // Fill the indicated vector with the numbers from file separated by
    // whitespace.  Returns 0 if worked OK, 1 means couldn't read file.
    ifstream infile(filename);
    if (not infile) {
    string msg = "Couldn't read " + filename;
    return 1;
    }
    string s;
    while (infile >> s) {
    const double x = std::stod(s);
    v.push_back(x);
    }
    return 0;
    }
    // Test code
        // *INDENT-OFF* 
        #ifdef DPSTRMAIN
            // Unit tests
            #include <cassert>
            using std::cout;
            using std::endl;
            void TestStrip(void) {
                const string S = "\t\r\f\v\n";
                const string empty = "";
                const string plain = "plain";
                string s;
                // Plain string
                s = plain;
                Strip(s);
                assert(s == plain);
                s = " " + plain + " ";
                Strip(s);
                assert(s == plain);
            }
            template<typename T>
            void TestLoadVector(const string &file) {
                vector<T> v;
                (void) LoadVector<T>(file, v);
                typename vector<T>::const_iterator it = v.begin();
                while (it != v.end()) {
                    cout << *it << " ";
                    it++;
                }
                cout << endl;
            }
            int main(int argc, char **argv) {
                TestStrip();
                cout << "Should get 1.1 2 3.7 twice:" << endl;
                TestLoadVector<double>("data");
                TestLoadVector<double>("data_ending_newline");
            }
        #endif
    """)
Make(s, "dpstr.cpp")
Make(s, "tmp/dpstr.cpp")
s = dedent("""
    // String utilities
    #ifndef DPSTR_H
    #define DPSTR_H

    #include <vector>
    #include <string>
    using std::vector;
    using std::string;

    // Doubles
    typedef vector<double> VecD;
    typedef vector<double> * VecDptr;
    typedef vector<VecDptr> VecDCont;
    // Floats
    typedef vector<float> VecF;
    typedef vector<float> * VecFptr;
    typedef vector<VecFptr> VecFCont;

    int Tokenize(const string &file, VecD &v);
    template<typename NumType>
        int LoadVector(const string &filename, vector<NumType> &v);
    void Keep(string &s, const string &c);
    void Remove(string &s, const string &c);
    int Substitute(string &s, const string &from, const string &to);
    #endif // DPSTR_H
    """)
Make(s, "dpstr.h")
Make(s, "tmp/dpstr.h")
s = dedent("""
    style = python
    dpstr.cpp
    dpstr.h
    """)
Make(s, "dpstr.proj")
# Remove any backup files
os.system("rm -f *.astyle.bak tmp/*.astyle.bak")

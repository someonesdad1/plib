"""
Prints out a minimum C/C++ program.
"""

print("""#if 0
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{

    return 0;
}
#else
#include <stdio.h>

int main(int argc, char **argv)
{

    return 0;
}
#endif""")

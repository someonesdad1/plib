# Constructed 19 Jul 2022

# This makefile builds cephes.dll used to provide the functionality of the
# /plib/prob.py module.  The functions used are from Moshier's double
# precision cephes library from https://netlib.org/cephes/.  The prob.py
# module calls into this DLL using ctypes.

# Assumes GNU make and gcc on cygwin.  Note the DLL construction is specific
# to cygwin and doesn't use e.g. dlltool like on other UNIX-like systems.

CC = gcc
CFLAGS = -g -O2 -fno-builtin
DLL = cephes.dll

.PHONY: $(DLL)	# Always build the DLL

# The distributions supported are (*.c file names follow):
# 	Binomial   			bdtr
# 	Beta 				btdtr
# 	chisq 				chdtr
# 	F 					fdtr
# 	Gamma				gdtr
# 	Negative binomial	nbdtr
# 	Normal 				ndtr, ndtri
# 	Poisson 			pdtr
# 	Student's t 		stdtr


SRC = bdtr.c btdtr.c chdtr.c fdtr.c nbdtr.c ndtr.c ndtri.c \
	  pdtr.c stdtr.c mtherr.c const.c isnan.c polevl.c \
	  incbet.c igami.c igam.c incbi.c expx2.c gamma.c

all: $(DLL) tags
	gcc -shared -o $(DLL) $(SRC:c=o)
	cp $(DLL) /plib		# Deploy to /plib

$(DLL): $(SRC:c=o)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $^

tags:	$(SRC)
	ctags $(SRC)

clean:
	rm -f *.o tags
realclean:  clean
	rm -f $(DLL)

# vim: noet

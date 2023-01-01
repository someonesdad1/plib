'''

Convert this old C program to a python script.  I no longer have the
graphics.lib file and I can't read the design.doc file anymore.

'''
r'''
This is the original code, written to compile IIRC under both the Borland
and QuickC compilers.

/*

10 Mar 2022:  This C program was written to be compiled with the QuickC
compiler and it ran on my HP-200LX palmtop computer.  It was pretty
convenient and did what I needed.  I used it with my film cameras.

Unfortunately, the design.doc Word document is no longer readable, showing
that it would have been smarter to e.g. use RTF for files in those days.

This should be straightforward to convert to a python script.  Note that it was 
able to handle reciprocity failure too.


make.bat:
    @echo off
    rm ev.exe
    bcc ev.c \qc\graphics.lib
    ev


Here's a data structure found in another file:
    typedef UINT unsigned integer

    typedef EXPOSURE struct {  /* Used to contain f, T, EV */
        double f;
        double T;
        double EV;
        double Trecip;
    }

    typdef FILM struct {
        char *name;
        float *T;
        float *Trecip;
    }

    typedef RECIP struct { /* Define the reciprocity curve */
        float *T;
        float *Trecip;
        RECIP *next;
    }

    struct SETUP { /* Defines the setup state of the program */
        UINT body;   /* Which camera body is current.  0 means none. */
        UINT lens;   /* Which lens is current.  0 means none. */
        UINT film;   /* Which film is current.  0 means none. */
        UINT filter; /* Which lens is current.  0 means none. */
        char *time;  /* Points to string of allowed shutter times; null if body=0 */
        char *aper;  /* Points to string of allowed apertures; null if lens=0 */
        FILM *filmlist /* Linked list of films */
        double tmult;  /* Multiplier for time */
        double fmult;  /* Multiplier for aperture */
        int display; /* Display mode; 0 = default */
        int lock;    /* Which variable is locked; 0=f, 1=T, 2=EV */
        int timedir; /* Time increment direction; 0=normal, 1 = reversed */
    }
*/


/*************************************************************************
ev.c   DP 7/3/94 Presents camera exposure information and allows you to 
adjust the values displayed.  Also will present reciprocity failure 
exposure corrected times for selected films.
*************************************************************************/

#define BORLAND

/************************ INCLUDE FILES *********************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <conio.h>
#ifndef BORLAND
    #include <graph.h>
#endif

/************************ DEFINES ***************************************/

#define F1 315   /* Key values of function keys */
#define F2 316
#define F3 317
#define F4 318
#define F5 319
#define F6 320
#define F7 321
#define F8 322

#define XTEXTIN       1
#define YTEXTIN       5
#define XRESULTNAME   3
#define XRESULTVALUE  8
#define XLOCKED       1
#define YFNUM         1
#define YSHUTTER      2
#define YEXPOSURE     3
#define XRECIP        20
#define YFILMTYPE     5
#define YSOFTKEYS     7

#define APERTURE      1
#define SHUTTER       2
#define EXPOSURE      3

#ifdef BORLAND
    #define GOTO(x,y) gotoxy(x,y)
    #define CLS() clrscr()
#else
    #define GOTO(x,y) _settextposition(y, x)
    #define CLS() _clearscreen(_GCLEARSCREEN);
#endif
/************************ GLOBAL VARIABLES ******************************/

/* Main exposure variables */
double f=1.0;      /* f/# */
double E=0.0;      /* EV (exposure value) */
double T=1.0;      /* Shutter speed in seconds */
int film_type=0;   /* If != 0, flags a specific film type */

/* These multipliers determine how incrementing the variables works */
double fmult = 1.41421356237L;
double tmult = 2.0L;

/* locked keeps track of which variable is locked.  1=f/#, 2=T, 3=E.  It
is also used to position the locked asterisk. */
int locked=3;

/************************ PROTOTYPES ************************************/

int  main(int argc, char **argv);
void Initialize(int argc, char **argv);
void PrintScreen(void);
void ClearScreen(void);
int  GetKey(void);
void ProcessKey(int key_pressed, int *Again);
double GetDouble(char *prompt);
void GetNearestShutter(double ShutterSpeed, char *str);
void CanonProgram(int locked);
double EV(double f, double T);
double Reciprocity(double T, int film);
void Eng(double T, char *str);

/************************ FUNCTIONS *************************************/

int main(int argc, char **argv)
{
    int Again=1;
    int key_pressed=0;

    Initialize(argc, argv);
    CLS();
    PrintScreen();

    do {
        key_pressed = GetKey();
        ProcessKey(key_pressed, &Again);
    } while ( Again );

    return 0;
}

/*************************************************************************
Initialize
*************************************************************************/

void Initialize(int argc, char **argv)
{
}

/*************************************************************************
PrintScreen  Print the information out and check that the values are 
close to being correct.
*************************************************************************/

void PrintScreen(void)
{
    double E_trial;
    char *fmt = "                             ";
    char *str = "                             ";

    CLS();

    /* First, check that the values are close to being correct */
    E_trial = 3.3*log10(f*f/T);
    if ( fabs(E_trial - E) > 0.01 ) {
        printf("Error in program:  values not consistent\n");
        printf("  f = %g\n  T = %g\n  E = %g\n", f, T, E);
        exit(1);
    }

    /* Print the locked asterisk */
    GOTO(XLOCKED, locked);
    printf("*");

    /* Print the three variables' names */
    GOTO(XRESULTNAME, YFNUM);
    printf("f/#");
    GOTO(XRESULTNAME, YSHUTTER);
    printf("T");
    GOTO(XRESULTNAME, YEXPOSURE);
    printf("EV");

    /* Print the values of the three variables.  Note we will pick the
    format based on the value of the variable. */

    /* Print the aperture */
    GOTO(XRESULTVALUE, YFNUM);
    strcpy(fmt, "%.1f");
    if ( f >= 10.0 ) strcpy(fmt, "%.0f");
    printf(fmt, f);

    /* Print the shutter speed */
    Eng(T, str);
    GOTO(XRESULTVALUE, YSHUTTER);
    printf("%s", str);
    GetNearestShutter(T, str);
    printf("  [%s]  ", str);

    /* Print the exposure */
    GOTO(XRESULTVALUE, YEXPOSURE);
    printf("%.1f", E);

    /* Print the softkey labels */
    GOTO(1, YSOFTKEYS);
    printf("1   2   3   4    5    6    7   \n");
    printf("f+  f-  T+  T-  EV+  EV-  LOCK");
}

/*************************************************************************
GetKey  Returns an integer representing the key pressed.  The low 7 bits
returned are the standard ascii value of the key.  For normal keys, the
higher bits are zero.  Special keys pressed are indicated by the high
byte being nonzero.  Note that getch() can't trap ^C.

This function makes the function keys F1 through F8 return 315 through 
322, respectively.
*************************************************************************/

int GetKey(void)
{
    int lo=0, hi=0;

    do {
        lo = getch();
        if ( lo == 0 || lo == 0xE0 ) {
            /* A function key or cursor movement key was pressed. */
            hi = lo;
            lo = getch();
            if ( hi == 0 )
                hi = 1;
            else
                hi = 2;
        }
    } while ( lo == 0 && hi == 0 );

    return (hi << 8) + lo;
}

/*************************************************************************
ProcessKey  Using the indicated key pressed, take the proper action.  If 
the key pressed was the escape key, set Again to 0 and return.
*************************************************************************/

void ProcessKey(int key_pressed, int *Again)
{
    int entered=0;         /* Tells which variable was changed */
    int changed_locked=0;  /* Flags when a locked variable is changed */

    if ( key_pressed == 27 ) {
        *Again = 0;
        return;
    }

    switch ( key_pressed ) {
        case F1: /* f+ */
            if ( locked != APERTURE ) {
                f *= fmult;
                entered = APERTURE;
            }
            break;
        case F2: /* f- */
            if ( locked != APERTURE ) {
                f /= fmult;
                if ( f < 1.0 ) f = 1.0;
                entered = APERTURE;
            }
            break;
        case F3: /* T+ */
            if ( locked != SHUTTER ) {
                T *= tmult;
                entered = SHUTTER;
            }
            break;
        case F4: /* T- */
            if ( locked != SHUTTER ) {
                T /= tmult;
                entered = SHUTTER;
            }
            break;
        case F5: /* E+ */
            if ( locked != EXPOSURE ) {
                E++;
                entered = EXPOSURE;
            }
            break;
        case F6: /* E- */
            if ( locked != EXPOSURE ) {
                E--;
                entered = EXPOSURE;
            }
            break;
        case F7: /* Bump locked item */
            locked++;
            if ( locked > 3 ) locked = 1;
            break;
        case 'e':  /* Enter an exposure value directly */
        case 'E':
            E = GetDouble("Exposure = ");
            while ( E <= -16.5 || E > 13.2 )
                E = GetDouble("Try again (EV) = ");
            entered = EXPOSURE;
      break;
        case 'f':  /* Enter an f/# directly */
        case 'F':
            f = GetDouble("f/# = ");
            while ( f <= 0.0 )
                f = GetDouble("Try again (f/#) = ");
            entered = APERTURE;
            break;
        case 't':  /* Enter a shutter speed value directly */
        case 'T':
            T = GetDouble("Shutter speed in s = ");
            while ( T <= 0.0 )
                T = GetDouble("Try again (shutter speed) = ");
            entered = SHUTTER;
            break;
    }

    /* Now calculate the new exposure if entered was nonzero */
    if ( entered == locked )
        CanonProgram(locked);  /* Get the other 2 vars by AE-1 pgm */
    else if ( entered ) {

        if ( (entered == APERTURE && locked == SHUTTER  ) ||
                 (entered == SHUTTER  && locked == APERTURE ) )
                E = 3.3*log10(f*f/T);

        if ( (entered == APERTURE && locked == EXPOSURE ) ||
                 (entered == EXPOSURE && locked == APERTURE ) )
                T = f*f/(pow(10, E/3.3));

        if ( (entered == SHUTTER  && locked == EXPOSURE ) ||
                 (entered == EXPOSURE && locked == SHUTTER  ) )
                f = sqrt(T*pow(10, E/3.3));
    }

    PrintScreen();
}

/*************************************************************************
GetDouble  Input a value from the user on the specified line, then erase
the things typed on the line and return the value.
*************************************************************************/

double GetDouble(char *prompt)
{
    char response[200]="";
    double num=0.0;
    int i;

    GOTO(XTEXTIN, YTEXTIN);
    printf("%s ", prompt);
    if ( fgets(response, 128, stdin) == NULL ) {
        printf("Error in function.  Program stopped.\n");
        exit(1);
    }

    num = strtod(response, NULL);
    GOTO(XTEXTIN, YTEXTIN);
    for(i=0; i<50; i++) printf(" ");
    GOTO(XTEXTIN, YTEXTIN);
    return num;
}

/*************************************************************************
GetNearestShutter  Returns a string that contains the nearest standard
shutter speed.  If it is outside the "normal" limits, then null is
returned.  Normal limits here are defined by the Canon AE-1 camera body.
*************************************************************************/

#define PUTSTR(A) { strcpy(str, A); return; }
void GetNearestShutter(double T, char *str)
{
    *str = 0;
    if ( 1/T > 1400 || T > 2 ) return;
    if ( T >= 1.5 ) PUTSTR("2 s")
    if ( T >= .714 && T < 1.5 ) PUTSTR("1 s")
    T = 1/T;
    if ( T > 1.4 && T <= 2.8 ) PUTSTR("2")
    if ( T > 2.8 && T <= 5.6 ) PUTSTR("4")
    if ( T > 5.6 && T <= 11  ) PUTSTR("8")
    if ( T > 11  && T <= 21  ) PUTSTR("15")
    if ( T > 21  && T <= 42  ) PUTSTR("30")
    if ( T > 42  && T <= 87  ) PUTSTR("60")
    if ( T > 87  && T <= 177 ) PUTSTR("125")
    if ( T > 177 && T <= 350 ) PUTSTR("250")
    if ( T > 350 && T <= 700 ) PUTSTR("500")
    if ( T > 700 && T <= 1400) PUTSTR("1000")

}

/*************************************************************************
CanonProgram  Calculate the two other variables per the Canon A-1 AE
mode program, given the locked variable.

A fit to the graph on page 35 of "How to select & use Canon SLR cameras"
by Carl Shipman, HP Books, gives the relationship f=a/sqrt(T) where
a = .507, a mean gotten from averaging the values from the curve.
This curve was given for the A-1 camera and was limited to f/1.4, but
I've used it here for all values of f and T.

Thus, to solve this problem, we have the two equations E = 3.3*log10(f^2/T)
and f = a/sqrt(T).  They are used in various forms to solve for the two
unlocked variables.
*************************************************************************/

void CanonProgram(int locked)
{
    double a=0.507;

    switch (locked ) {
        case APERTURE:
            T = (a/f)*(a/f);
            E = EV(f,T);
            break;
        case SHUTTER:
            f = a/sqrt(T);
            E = EV(f,T);
            break;
        case EXPOSURE:
            T = a/pow(10, E/6.6);
            f = a/sqrt(T);
            break;
        default:
            printf("Internal error:  locked had illegal value.  Program stopped.\n");
            exit(1);
            break;
    }
}

/*************************************************************************
EV  Calculates the equation EV = 3.3*log(f*f/T).
*************************************************************************/

double EV(double f, double T)
{
    if ( T == 0.0 || f < 0.0 || T < 0.0 ) {
        printf("Internal error:  bad values in function EV\n");
        exit(1);
    }

    return 3.3*log(f*f/T);
}

/*************************************************************************
Reciprocity  Calculates the corrected exposure time in seconds for an
indicated time T in seconds and a particular film type film.
*************************************************************************/

double Reciprocity(double T, int film)
{
}

/*************************************************************************
Eng  Returns a number formatted in engineering notation with 3 significant
figures.  The number is assumed to be a time, so the proper prefix to s
is added.  We'll assume that the number of seconds will be less than 
1E6 and more than 1E-6.
*************************************************************************/

void Eng(double T, char *str)
{
    char prefix[2], *tmpstr="                                         ";
    int ip;
    double tmp;

    if ( T < 1e-6 || T >= 1e6 ) {
        printf("Internal error:  T not between 1e-6 and 1e6.\n");
        exit(1);
    }

    /* Get the exponent.  We'll take the integer part of the base 10 
    log.  If this is less than zero, we'll decrement it. */
    ip = log10(T);
    if ( ip < 0 ) ip--;
    T /= pow(10, ip);  /* Get the mantissa */

    if ( ip >= 0 ) {
        strcpy(prefix, " s");
        if ( T >= 3 ) strcpy(prefix, "ks");
    }
    else {
        strcpy(prefix, "ms");
        if ( T < -3 ) strcpy(prefix, "us");
    }

    /* Convert T to X.XX, XX.X, or XXX form */
    T *= pow(10, ip % 3);
    
    /* Now print to a string and extract the first three digits. */
    sprintf(tmpstr, "%-+e", T);  /* +X.XXXXXXEXX format */
    tmpstr[5] = 0;  /* Truncate the string after second decimal place */
    strcat(tmpstr, " ");
    strcat(tmpstr, prefix); 
    tmpstr++;  /* Remove the sign character */
    strcpy(str, tmpstr);
}
'''

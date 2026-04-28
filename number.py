'''

Abstract number class with units and linear uncertainty propagation
    - Persistence in REPL
        - Mike has a 50 line vision of an SQLite db persistence connection for the REPL
        using the memento pattern.
            - A memento is a class that the Originator (Num class instance) saves its state
            to.  The memento is passed to a Caretaker that e.g. persists it with block
            chaining to establish provenance.  When restoring old state is needed, the
            Originator is given back the memento and uses memento.GetState() to restore
            the Num's state.  https://refactoring.guru/design-patterns/memento
            - He also feels we can get this implemented in a single day, so it's worth the
            effort.  This gives me persistence without losing my development context that
            remembers the twisted paths of development and where the problems are; this
            lets me continue to try the whole thing out as a real prototype with
            persistence.

    - .flip:  property used to flip the output of str() and repr().  Use case:  in the REPL
    and the debugger, you usually see the repr() form; this allows you to see the str()
    form
    - .frac:  property used to show fractional form.  
        - None:  always show number as mpf
            - The formatter shows it as a float, but italicizes it to tell you it's actually
            a fraction
        - "i":  show number as improper fraction, denominator limited to 100000
        - "p":  show as proper fraction, but denominator limited to 100000
        - "I":  show number as improper fraction to full resolution
        - "P":  show as proper fraction to full resolution

    - Loss of linear uncertainty

        - An important idea was in the UnitArbiter.inject_math(self) function which was an
        early form of the currently-use NoetherWrap() function.  This is in the revisions
        before about 84073ed2678a5f8bc for a week or two.  This was the core code:

            with workdps(mp.dps + 4):
                h_base = mp.power(10, -(mp.dps // 2))
                d1 = diff(mp_func, x.as_mpc, h=h_base)
                d2 = diff(mp_func, x.as_mpc, h=h_base / 2)
                sens = abs(d1)
                sens2 = abs(d2)
                if abs(sens - sens2) / (sens + 1e-30) > 0.01:
                    print(f"Warning: Possible singularity suspected in {func_name} at {x.raw_value}."
                        f"\nUncertainty propagation may be non-physical.", file=sys.stderr)
                new_re_unc = sens * x.re_unc
                new_im_unc = sens * x.im_unc

        - This looked at the relative change of the sensitivity (absolute value of the
        slope) and if it was above a threshold, a warning about uncertainty propagation
        was made.  Note the default mp.dps is 15, so this uses an h of around 1e-7, then
        h/2.  This is a practical strategy to detect steep derivatives that invalidate
        linear uncertainty propagation.  I think it should be added back into the existing
        closure factory.

'''
if 1:  # Header
    if 1:   # Standard imports
        from pdb import set_trace as yy
        import contextlib
        import dataclasses
        import decimal
        import enum
        import fcntl
        import fractions
        import inspect
        import io
        import operator
        import os
        import pathlib
        import random
        import re
        import select
        import shutil
        import subprocess
        import sys
        import tempfile
        import threading
        import typing as ty
    if 1:   # Custom imports
        import dpmath
        import dptypes
        import fmt
        import lwtest
        import mpmath
        import trm
        import uncertainties
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Class to contain a general number"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "math"
        __todo__      = ''' '''
    if 1:   # Global variables
        Path = pathlib.Path
        Assert = lwtest.Assert
        t = trm.TrmDP()
        t.dbg = "#bdf6fe"
        #g = dptypes.Constant()
        class G:
            pass
        g = G()
        g.dbg = False
    if 1:   # Types and enums
        class NumType(enum.IntEnum):
            Int = 1
            Rat = 2
            Flt = 3
            Cpx = 4
            Unc = 5
            UncCpx = 6
        NumericalTypes = ty.Union[
            int , float , complex , decimal.Decimal ,
            fractions.Fraction , mpmath.mpf , mpmath.mpc ,
            uncertainties.UFloat , "Num" , str , None]
    if 1:   # Utility stuff
        def Dbg(*p, **kw):
            # Simple debugging command
            if not g.dbg:
                return
            print("DEBUG ", end="")
            print(*p, **kw)
        def _Dbg(*p, **kw):
            if not hasattr(Dbg, "file"):
                Dbg.file = sys.stdout
            if g.dbg:
                if "color" in kw:
                    print(f"{t(kw['color'])}", end="", file=Dbg.file)
                    del kw["color"]
                else:
                    print(f"{t.dbg}", end="", file=Dbg.file)
                k = kw.copy()
                k["file"] = Dbg.file
                print(*p, **k)
                print(f"{t.n}", end="", file=Dbg.file)
        def get_caller_info() -> tuple[str, int]:
            'Returns (file_name, line_number) for the frame above the caller'
            # frame 0 is get_caller_info
            # frame 1 is Warn
            # frame 2 is the code that called Warn
            frame = inspect.stack()[2]
            return os.path.basename(frame.filename), frame.lineno
        def Warn(*p, **kw):
            '''Write a message to stderr in red color with location from where called.
            To minimize the number of messages, you can set single=True and the message
            will be printed only once.
            '''
            if not hasattr(Warn, "single"):
                Warn.single = False
                Warn.already_printed = set()
            fname, line = get_caller_info()
            k = kw.copy()   # Only modify a copy of kw
            k["file"] = sys.stderr
            Warn.single = bool(k.get("single", False))  # See if only print once
            if "single" in k:
                del k["single"]
            if Warn.single and p in Warn.already_printed:
                return
            Warn.already_printed.add(p)
            # Print the warning
            print(f"{t.red}[{fname}:{line}]:  ", end="", file=sys.stderr)
            print(*p, **k)
            print(f"{t.n}", end="", file=sys.stderr)
if 0:   # Documentation
    '''Represent a general number useful for routine calculations

        Dependencies
            - mpmath:  https://mpmath.org/
            - GNU units:  https://www.gnu.org/software/units/
            
        The Num class is an abstract container of numbers intended to model the routine
        calculations we do in the real world.  The primary features of the class are
            - Integers, fractions, real, and complex numbers are supported.  Just type
              them in with simple notation:
                - Num(1), Num("1") -> integer
                - Num(3/8), Num("3/8") -> fraction
                - Num(1.0), Num("1.0") -> real
                - Num(1-4.2j), Num("1-4.2j") -> complex
                - Num("1.00(5)") -> real number with uncertainty
                - Num("1.00(5)+2.0(1)j") -> complex number with uncertainty
                - Num("1.00(5)+2.0(1)j<R=0.77>") -> complex number with uncertainty and
                  correlation between the real and imaginary parts (linear uncertainty
                  propagation)
            - Physical units can be attached to the numbers:  x = Num("1.2 m/s")
                - You can define new units:  x.base("dogs"); x.base("cats")
            - Num objects with units document your intent and prevent
            - Many special functions are supported
            - Infection model:  a binary operation with a Num results in another Num

        Architecture:  The num class is a wrapper for mpmath numbers and the special
        functions of the mpmath library.  The GNU units program is run as a coprocess to
        provide the dimensional algebra support.

        Example:  suppose gasoline costs $5/gallon and your vehicle averages 50
        miles/gallon.  Using the Num class in the python REPL, the equivalent
        calculation is

            >>> from number import Num
            >>> cost_per_mile = Num("5 $/gal")/Num("50 mi/gal")
            >>> cost_per_mile
            0.100 ($/gal)/(mi/gal)
            >>> cost_per_mile.to("$/km")
            0.0621 $/km
            >>> cost_per_mile.to("$/mi")
            0.100 $/mi

        You can't see it here, but the terminal printout shows the 0.100 in a color that
        represents a fraction, as the actual computed number is the ratio of two
        integers, which is the fraction 1/10.  Most of the time we want to see the
        decimal form, but the .frac property can be used to see the fractional results.

        An important feature is that the cost_per_mile display shows the units as a
        division of two other units, indicating that an operation was performed (here,
        division).

        The Num class reduces the number to its simplest representation (here, a
        rational number).  This units representation shows the computational history;
        the current example shows that a cost per unit volume was divided by a mileage
        per unit volume, giving a result with units of cost per unit length.  The last
        step shows you can see it in the reduced units if you wish.

        The units of the first argument in a binary expression are retained in the
        expression's result.

        --------------------------------------------------------------------------- 

        Parser mandates
            - Unit string separated from numeric string by one or more spaces
            - No spaces allowed in unit string
            - All space characters in the numerical portion are stripped before parsing
            - Underscores can be used per the python float/int convention
            - Parser uses x.rsplit(" ", 1) to check for a unit.  If the right-hand part
              is a valid unit (verified via UnitArbiter), it is treated as a unit.
              Otherwise, the entire string is treated as a numeric expression.
            - Complex numbers must follow standard python syntax: <re>j, <im>j, or
              <re><sign><im>j.  No spaces are allowed within the complex expression.
            - Uncertainty:  only the short-form string form is allowed:  "1.234(5)" or
              "1.234(5)e-12".  No "/" allowed in the expression.  The uncertainty
              parenthetical expression can only contain digits (it's an arbitrary
              positive integer or zero).
            - Rational numbers are indicated by a '/' in the string.  Only improper
              fractional forms are allowed.

        '''

if 0: # NumericMixin
    '''Manifest [17]: __add__ __sub__ __mul__ __truediv__ __pow__ _do_uncertainty_math _check_ordering __lt__ __le__ __gt__ __ge__ __eq__ __abs__ __neg__ __radd__ __rsub__ __rmul__ __rtruediv__ _ensure_conformable'''
    class NumericMixin:
        '''Operator overloading for the Num class, leveraging Fraction arithmetic where appropriate.'''
        def _ensure_conformable(self, other: "Num", op: str) -> None:
            if self._unit == other._unit:
                return
            is_ok, msg = self.arb.check_conformable(other._unit, self._unit)
            if not is_ok:
                raise ValueError(f"Operation '{op}' failed: {self._unit} and {other._unit} are incompatible. ({msg})")
        def __add__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            self._ensure_conformable(other, "+")
            other_norm = self._normalize(other, "add")
            if self.mytype <= NumType.Rat and other_norm.mytype <= NumType.Rat:
                res_val = self.as_int_or_rat + other_norm.as_int_or_rat
                return self._make_result(res_val, unit=self._unit)
            return self._binary_op(other_norm, lambda a, b: a+b)
        def __sub__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            self._ensure_conformable(other, "-")
            other_norm = self._normalize(other, "sub")
            if self.mytype <= NumType.Rat and other_norm.mytype <= NumType.Rat:
                return self._make_result(self.as_int_or_rat - other_norm.as_int_or_rat, unit=self._unit)
            return self._binary_op(other_norm, lambda a, b: a-b)
        def __mul__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self._unit and other._unit:
                res_unit = f"({self._unit})*({other._unit})"
            elif self._unit or other._unit:
                res_unit = self._unit or other._unit
            if self.mytype <= NumType.Rat and other.mytype <= NumType.Rat:
                res = self._make_result(self.as_int_or_rat * other.as_int_or_rat, unit=res_unit)
                return res
            res = self._binary_op(other, lambda a, b: a*b)
            res._unit = res_unit
            return res
        def __truediv__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self._unit and other._unit:
                res_unit = f"({self._unit})/({other._unit})"
            elif self._unit:
                res_unit = self._unit
            elif other._unit:
                res_unit = f"1/({other._unit})"
            if self.mytype <= NumType.Rat and other.mytype <= NumType.Rat:
                res = self._make_result(self.as_int_or_rat / other.as_int_or_rat, unit=res_unit)
                return res
            res = self._binary_op(other, lambda a, b: a/b)
            res._unit = res_unit
            return res
        def __pow__(self, other: ty.Any) -> "Num":
            '''Exponentiation with safe unit propagation.'''
            if not isinstance(other, Num):
                other = Num(str(other))
            if self._unit and other.mytype == NumType.Cpx:
                raise TypeError(f"Cannot raise unit-bearing quantity ({self._unit}) to a complex power")
            res = self._binary_op(other, lambda a, b: a**b)
            if self._unit:
                if other.mytype == NumType.Rat:
                    exp_str = f"({other.as_int_or_rat.numerator}/{other.as_int_or_rat.denominator})"
                else:
                    try:
                        exp_f = float(other.as_mpf)
                        exp_str = str(int(exp_f)) if exp_f.is_integer() else str(exp_f)
                    except:
                        exp_str = str(other.raw_value)
                raw_unit = f"({self._unit})^{exp_str}"
                new_val, simplified_unit = self.arb.simplify(res.raw_value, raw_unit)
                return Num(new_val, unit=simplified_unit)
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            from mpmath import workdps, diff, sqrt as mp_sqrt
            if self.mytype == NumType.UncCpx or other.mytype == NumType.UncCpx:
                z_val = op_func(self.as_mpc, other.as_mpc)
                new_re_unc = mp_sqrt((self.re_unc**2) + (other.re_unc**2))
                new_im_unc = mp_sqrt((self.im_unc**2) + (other.im_unc**2))
                res = self._make_result(z_val, unit=self._unit)
                res.re_unc = new_re_unc
                res.im_unc = new_im_unc
                res.mytype = NumType.UncCpx
                return res
            z_val = op_func(self.as_mpc, other.as_mpc)
            with workdps(mpmath.mp.dps+4):
                df_dself = diff(lambda x: op_func(x, other.as_mpc), self.as_mpc)
                df_dother = diff(lambda y: op_func(self.as_mpc, y), other.as_mpc)
                s_sens = abs(df_dself)
                o_sens = abs(df_dother)
                new_re_unc = mp_sqrt((s_sens*self.re_unc)**2 + (o_sens*other.re_unc)**2)
                new_im_unc = mp_sqrt((s_sens*self.im_unc)**2 + (o_sens*other.im_unc)**2)
            res = self._make_result(z_val, unit=self._unit)
            res.re_unc = new_re_unc
            res.im_unc = new_im_unc
            res.mytype = NumType.Unc
            return res
        def _check_ordering(self, other: ty.Any, op: str):
            other_num = other if isinstance(other, Num) else Num(other)
            if self.mytype in (NumType.Cpx, NumType.UncCpx) or other_num.mytype in (NumType.Cpx, NumType.UncCpx):
                raise TypeError(f"'{op}' not supported between complex numbers.")
            if self.mytype in (NumType.Unc, NumType.UncCpx) or other_num.mytype in (NumType.Unc, NumType.UncCpx):
                raise TypeError(f"'{op}' not supported for numbers with uncertainty.")
        def __lt__(self, other):
            self._check_ordering(other, "<")
            return self.raw_value < (other.raw_value if isinstance(other, Num) else other)
        def __le__(self, other):
            self._check_ordering(other, "<=")
            return self.raw_value <= (other.raw_value if isinstance(other, Num) else other)
        def __gt__(self, other):
            self._check_ordering(other, ">")
            return self.raw_value > (other.raw_value if isinstance(other, Num) else other)
        def __ge__(self, other):
            self._check_ordering(other, ">=")
            return self.raw_value >= (other.raw_value if isinstance(other, Num) else other)
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                try:
                    other = Num(other)
                except:
                    return False
            if self._unit != other._unit:
                try:
                    other = self._normalize(other, "cmp")
                except (ValueError, TypeError):
                    return False
            v1, v2 = self.raw_value, other.raw_value
            try:
                if hasattr(v1, "real") or hasattr(v2, "real"):
                    res = mpmath.mpc(v1) == mpmath.mpc(v2)
                else:
                    res = mpmath.mpf(v1) == mpmath.mpf(v2)
                if res:
                    return True
                return str(v1) == str(v2)
            except:
                return v1 == v2
        def __abs__(self) -> "Num":
            return self._make_result(abs(self.raw_value), unit=self._unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self._unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other)+self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other)-self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other)*self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other)/self
        def __float__(self) -> float:
            return float(self.as_mpf)
        def __complex__(self) -> complex:
            s = self.as_mpc
            return complex(float(s.real), float(s.imag))
    # Goodbye from the Mike & Don comedy show
# CHUNK: NumericMixin
if 1: # NumericMixin
    '''Manifest [17]: __add__ __sub__ __mul__ __truediv__ __pow__ _do_uncertainty_math _check_ordering __lt__ __le__ __gt__ __ge__ __eq__ __abs__ __neg__ __radd__ __rsub__ __rmul__ __rtruediv__ _ensure_conformable'''
    class NumericMixin:
        '''Operator overloading for the Num class, leveraging Fraction arithmetic where appropriate.'''
        def _do_unary_uncertainty(self, op_func: ty.Callable, res_unit: str = "") -> "Num":
            from mpmath import workdps, diff, mpc, sqrt as mp_sqrt
            with workdps(mpmath.mp.dps + 4):
                # Ensure we are working with mpmath complex numbers throughout
                real_mpc = mpc(self._real)
                imag_mpc = mpc(self._imag)
                # Partial derivatives using mpmath mpc context
                df_dx = diff(lambda x: op_func(mpc(x) + 1j*imag_mpc), real_mpc)
                df_dy = diff(lambda y: op_func(real_mpc + 1j*mpc(y)), imag_mpc)
                # Covariance term
                cov_xy = self.correl * self.re_unc * self.im_unc
                # Variance propagation formula (Taylor expansion)
                var_real = ((abs(df_dx)**2 * self.re_unc**2)
                            + (abs(df_dy)**2 * self.im_unc**2)
                            + (2 * df_dx * df_dy * cov_xy))
                new_unc = mp_sqrt(abs(var_real))
            res = self._make_result(op_func(self.as_mpc), unit=res_unit)
            res.re_unc = new_unc
            res.correl = 0  # Resetting correlation after unary transformation
            res.mytype = self.mytype
            return res
        def _ensure_conformable(self, other: "Num", op: str) -> None:
            # If both have the same unit, we are good.
            if self._unit == other._unit:
                return
            # If one has a unit and the other doesn't, that is a dimensional mismatch.
            if not self._unit or not other._unit:
                raise ValueError(f"Operation '{op}' failed: Incompatible dimensions ({self._unit!r} vs {other._unit!r})")
            # If both have units, check with the arbiter.
            is_ok, msg = self.arb.check_conformable(other._unit, self._unit)
            if not is_ok:
                raise ValueError(f"Operation '{op}' failed: {self._unit} and {other._unit} are incompatible. ({msg})")
        def __add__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            self._ensure_conformable(other, "+")
            other_norm = self._normalize(other, "add")
            if self.mytype <= NumType.Rat and other_norm.mytype <= NumType.Rat:
                res_val = self.as_int_or_rat + other_norm.as_int_or_rat
                return self._make_result(res_val, unit=self._unit)
            return self._binary_op(other_norm, lambda a, b: a+b)
        def __sub__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            self._ensure_conformable(other, "-")
            other_norm = self._normalize(other, "sub")
            if self.mytype <= NumType.Rat and other_norm.mytype <= NumType.Rat:
                return self._make_result(self.as_int_or_rat - other_norm.as_int_or_rat, unit=self._unit)
            return self._binary_op(other_norm, lambda a, b: a-b)
        def __mul__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self._unit and other._unit:
                res_unit = f"({self._unit})*({other._unit})"
            elif self._unit or other._unit:
                res_unit = self._unit or other._unit
            if self.mytype <= NumType.Rat and other.mytype <= NumType.Rat:
                res = self._make_result(self.as_int_or_rat * other.as_int_or_rat, unit=res_unit)
                return res
            res = self._binary_op(other, lambda a, b: a*b)
            res._unit = res_unit
            return res
        def __truediv__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self._unit and other._unit:
                res_unit = f"({self._unit})/({other._unit})"
            elif self._unit:
                res_unit = self._unit
            elif other._unit:
                res_unit = f"1/({other._unit})"
            if self.mytype <= NumType.Rat and other.mytype <= NumType.Rat:
                res = self._make_result(self.as_int_or_rat / other.as_int_or_rat, unit=res_unit)
                return res
            res = self._binary_op(other, lambda a, b: a/b)
            res._unit = res_unit
            return res
        def __pow__(self, other: ty.Any) -> "Num":
            '''Exponentiation with safe unit propagation.'''
            if not isinstance(other, Num):
                other = Num(str(other))
            if self._unit and other.mytype == NumType.Cpx:
                raise TypeError(f"Cannot raise unit-bearing quantity ({self._unit}) to a complex power")
            res = self._binary_op(other, lambda a, b: a**b)
            if self._unit:
                if other.mytype == NumType.Rat:
                    exp_str = f"({other.as_int_or_rat.numerator}/{other.as_int_or_rat.denominator})"
                else:
                    try:
                        exp_f = float(other.as_mpf)
                        exp_str = str(int(exp_f)) if exp_f.is_integer() else str(exp_f)
                    except:
                        exp_str = str(other.raw_value)
                raw_unit = f"({self._unit})^{exp_str}"
                new_val, simplified_unit = self.arb.simplify(res.raw_value, raw_unit)
                return Num(new_val, unit=simplified_unit)
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            from mpmath import workdps, diff, sqrt as mp_sqrt
            if self.mytype == NumType.UncCpx or other.mytype == NumType.UncCpx:
                z_val = op_func(self.as_mpc, other.as_mpc)
                new_re_unc = mp_sqrt((self.re_unc**2) + (other.re_unc**2))
                new_im_unc = mp_sqrt((self.im_unc**2) + (other.im_unc**2))
                res = self._make_result(z_val, unit=self._unit)
                res.re_unc = new_re_unc
                res.im_unc = new_im_unc
                res.mytype = NumType.UncCpx
                return res
            z_val = op_func(self.as_mpc, other.as_mpc)
            with workdps(mpmath.mp.dps+4):
                df_dself = diff(lambda x: op_func(x, other.as_mpc), self.as_mpc)
                df_dother = diff(lambda y: op_func(self.as_mpc, y), other.as_mpc)
                s_sens = abs(df_dself)
                o_sens = abs(df_dother)
                new_re_unc = mp_sqrt((s_sens*self.re_unc)**2 + (o_sens*other.re_unc)**2)
                new_im_unc = mp_sqrt((s_sens*self.im_unc)**2 + (o_sens*other.im_unc)**2)
            res = self._make_result(z_val, unit=self._unit)
            res.re_unc = new_re_unc
            res.im_unc = new_im_unc
            res.mytype = NumType.Unc
            return res
        def _check_ordering(self, other: ty.Any, op: str):
            other_num = other if isinstance(other, Num) else Num(other)
            if self._unit or other_num._unit:
                self._ensure_conformable(other_num, op)
            if self.mytype in (NumType.Cpx, NumType.UncCpx) or other_num.mytype in (NumType.Cpx, NumType.UncCpx):
                raise TypeError(f"'{op}' not supported between complex numbers.")
            if self.mytype in (NumType.Unc, NumType.UncCpx) or other_num.mytype in (NumType.Unc, NumType.UncCpx):
                raise TypeError(f"'{op}' not supported for numbers with uncertainty.")
        def __lt__(self, other):
            self._check_ordering(other, "<")
            other_num = other if isinstance(other, Num) else Num(other)
            other_norm = self._normalize(other_num, "cmp")
            return self.raw_value < other_norm.raw_value
        def __le__(self, other):
            self._check_ordering(other, "<=")
            other_num = other if isinstance(other, Num) else Num(other)
            other_norm = self._normalize(other_num, "cmp")
            return self.raw_value <= other_norm.raw_value
        def __gt__(self, other):
            self._check_ordering(other, ">")
            other_num = other if isinstance(other, Num) else Num(other)
            other_norm = self._normalize(other_num, "cmp")
            return self.raw_value > other_norm.raw_value
        def __ge__(self, other):
            self._check_ordering(other, ">=")
            other_num = other if isinstance(other, Num) else Num(other)
            other_norm = self._normalize(other_num, "cmp")
            return self.raw_value >= other_norm.raw_value
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                try:
                    other = Num(other)
                except:
                    return False
            if self._unit != other._unit:
                try:
                    other = self._normalize(other, "cmp")
                except (ValueError, TypeError):
                    return False
            v1, v2 = self.raw_value, other.raw_value
            try:
                m1, m2 = self._to_mpmath(v1), self._to_mpmath(v2)
                # Parity check for real vs complex
                if hasattr(m1, "imag") != hasattr(m2, "imag"):
                    return False
                # Use default almosteq to allow for standard rounding noise
                # scaled to your current mp.dps
                return mpmath.almosteq(m1, m2)
            except:
                return v1 == v2
        def __abs__(self) -> "Num":
            return self._make_result(abs(self.raw_value), unit=self._unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self._unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other)+self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other)-self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other)*self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other)/self
        def __float__(self) -> float:
            return float(self.as_mpf)
        def __complex__(self) -> complex:
            s = self.as_mpc
            return complex(float(s.real), float(s.imag))
        @classmethod
        def _to_mpmath(cls, val):
            'Return a numerical value as an mpf/mpc'
            if isinstance(val, (mpmath.mpf, mpmath.mpc)):
                return val
            if hasattr(val, "imag") and not isinstance(val, (int, float, complex, fractions.Fraction)):
                return mpmath.mpc(val)
            try:
                s = str(val)
                if 'j' in s or 'i' in s:
                    return mpmath.mpc(s)
                return mpmath.mpf(s)
            except:
                return val
    # Goodbye from the Mike & Don comedy show
# END_CHUNK: NumericMixin

if 0: # Num
    '''Manifest [20]: __init__ _promote _binary_op _make_result _normalize base help _s _r __str__ __repr__ to approx dump unit raw_value as_mpc as_mpf as_int_or_rat num pi e'''
    class Num(NumericMixin):
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
            NumType.UncCpx: t("red", "gry1"),
        }
        flip = False
        show_color = True
        active_system = "default"
        Fmt = fmt.Fmt()
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            self._doc = ""
            self.arb = UnitArbiter()
            self.fmt = Num.Fmt
            self._val: fractions.Fraction = fractions.Fraction(0)
            self._real: mpmath.mpf = mpmath.mpf("0")
            self._imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self._mytype: NumType = NumType.Int
            if value is None:
                if unit:
                    self._unit = unit
                return
            if isinstance(value, str):
                payload = StringParser.parse(value, unit)
                if payload.type in (NumType.Int, NumType.Rat):
                    self._val = fractions.Fraction(payload.numer, payload.denom)
                else:
                    self._real, self._imag = payload.real, payload.imag
                    self.re_unc, self.im_unc = payload.re_unc, payload.im_unc
                    self.correl = payload.correl
                self._unit = payload.unit
                self.mytype = payload.type
            elif isinstance(value, Num):
                self._val = value._val
                self._real, self._imag = value._real, value._imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                self.correl = value.correl
                self._unit = unit if unit else value._unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self._val = fractions.Fraction(value)
                self.mytype = NumType.Int
            elif isinstance(value, fractions.Fraction):
                self._val = value
                self.mytype = NumType.Rat
            elif isinstance(value, (float, decimal.Decimal)):
                self._real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self._real, self._imag = mpmath.mpf(str(value.real)), mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif hasattr(value, "_mpf_") or isinstance(value, mpmath.mpf):
                self._real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self._real, self._imag = value.real, value.imag
                self.mytype = NumType.Cpx
            else:
                raise TypeError(f"Type {type(value)} not supported")
            if unit: 
                self._unit = unit
            if not (-1 <= self.correl <= 1):
                raise ValueError("Correlation coefficient must be on [-1, 1]")
        def _promote(self) -> "Num":
            '''Aggressively collapse Flt back to Rat or Int if precision allows.'''
            # 1. If Flt, try to convert to Rat (Fraction)
            if self.mytype == NumType.Flt:
                try:
                    # Using string conversion for mpmath accuracy
                    f = fractions.Fraction(str(self._real)).limit_denominator()
                    # Check for "perfect" representation
                    if mpmath.mpf(f.numerator) / mpmath.mpf(f.denominator) == self._real:
                        self._val = f
                        self.mytype = NumType.Rat
                except:
                    pass
            # 2. If Rat, try to convert to Int
            if self.mytype == NumType.Rat:
                if self._val.denominator == 1:
                    self._val = self._val.numerator
                    self.mytype = NumType.Int
            # 3. Handle Complex downcasting
            elif self.mytype == NumType.Cpx:
                if self._imag == 0:
                    self.mytype = NumType.Flt
                    self._promote() # Recursive call to collapse Flt
            return self
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            target_type = max(self.mytype.value, other.mytype.value)
            res_unit = self._unit
            if target_type <= NumType.Rat.value:
                raw_val = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return self._make_result(raw_val, unit=res_unit)
            if target_type >= NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            if self.mytype in (NumType.Cpx, NumType.UncCpx) or other.mytype in (NumType.Cpx, NumType.UncCpx):
                raw_val = op_func(self.as_mpc, other.as_mpc)
                return self._make_result(raw_val, unit=res_unit)
            a_val = self._real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other._real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return self._make_result(raw_val, unit=res_unit)
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit=unit)._promote()
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            if self._unit == other._unit or operation in ("mul", "div"):
                return other
            is_ok, factor_str = self.arb.check_conformable(other._unit, self._unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            adjusted._real = adjusted.as_mpf * factor
            adjusted.mytype = NumType.Flt
            adjusted._unit = self._unit
            return adjusted
        def base(self, unit: str = "") -> None:
            target = unit if unit else self._unit
            if target: print(self.arb._register_unit(target))
        def help(self, topic: str = "") -> None:
            h = Help()
            h(topic) if topic else h()
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self._val.numerator)
            elif self.mytype == NumType.Rat:
                s = self.fmt(self.as_mpf)
            elif self.mytype == NumType.Cpx:
                s = self.fmt(self.as_mpc)
            elif self.mytype == NumType.Unc:
                s = f"{self._real} +/- {self.re_unc}"
            elif self.mytype == NumType.UncCpx:
                s = f"{self.as_mpc} +/- {self.re_unc} + {self.im_unc}i <R={self.correl}>"
            else:
                s = self.fmt(self._real)
            unit_string = f" {t.whtl}{self._unit}{t.n}" if self._unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def _r(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self._val.numerator)
            elif self.mytype == NumType.Rat:
                s = f"{self._val.numerator}/{self._val.denominator}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.as_mpc!r}"
            else:
                s = str(self._real)
            if self._unit:
                s += f" {self._unit}"
            return f"Num('{s}')"
        def __str__(self) -> str:
            return self._r() if Num.flip else self._s()
        def __repr__(self) -> str:
            return self._s() if Num.flip else self._r()
        def __hash__(self) -> int:
            '''Noether-invariant hash of an immutable physical quantity.'''
            # Canonical string of value at fixed 25-digit precision ensures stability
            # independent of the global mpmath.mp.dps setting.
            val_str = mpmath.nstr(self.raw_value, 25)
            return hash((val_str, self._unit))
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not unit or unit == self._unit:
                return Num(self)
            is_ok, factor_str = self.arb.check_conformable(self._unit, unit)
            if not is_ok:
                self.arb._register_unit(unit)
                is_ok, factor_str = self.arb.check_conformable(self._unit, unit)
                if not is_ok: raise ValueError(f"Incompatible: {self._unit} -> {unit}")
            res = Num(self)
            res._real = res.as_mpf*mpmath.mpf(factor_str)
            res.mytype = NumType.Flt
            res._unit = unit
            return res._promote() if auto_promote else res
        def approx(self, y: ty.Any, ndigits: int) -> bool:
            if not isinstance(y, Num):
                y = Num(y)
            vx, vy = self.as_mpf, y.as_mpf
            if vy == 0:
                return abs(vx) < 10**(-ndigits)
            val = abs((vx-vy)/vy)
            return True if val == 0 else int(abs(mpmath.log10(val))) >= ndigits
        @property
        def dump(self) -> None:
            indent = " "*0
            d = {1: "Int", 2: "Rat", 3: "Flt", 4: "Cpx", 5: "Unc", 6: "UncCpx"}
            print(f"{indent}Num(id({hex(id(self))})) core attributes:")
            print(f"{indent}    self._val.numerator   {self._val.numerator}")
            print(f"{indent}    self._val.denominator {self._val.denominator}")
            print(f"{indent}    self._real            {self._real}")
            print(f"{indent}    self._imag            {self._imag}")
            print(f"{indent}    self.re_unc           {self.re_unc}")
            print(f"{indent}    self.im_unc           {self.im_unc}")
            print(f"{indent}    self.correl           {self.correl}")
            print(f"{indent}    self._unit             {self._unit!r}")
            print(f"{indent}    self.mytype           {self.mytype} {d[self.mytype]}")
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @property
        def raw_value(self) -> ty.Any:
            if self.mytype in (NumType.Int, NumType.Rat): return self._val
            return self.as_mpc if self.mytype in (NumType.Cpx, NumType.Unc, NumType.UncCpx) else self._real
        @property
        def as_mpc(self) -> mpmath.mpc:
            return (mpmath.mpc(self._real, self._imag) 
                    if self.mytype in (NumType.Cpx, NumType.Unc, NumType.UncCpx) else
                    mpmath.mpc(self.as_mpf, 0))
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype in (NumType.Int, NumType.Rat):
                return mpmath.mpf(self._val.numerator)/mpmath.mpf(self._val.denominator)
            return self._real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            return self._val
        @property
        def num(self) -> "Num":
            res = Num(self)
            res._unit = ""
            return res
        @property
        def pi(self) -> "Num": return Num(+mpmath.pi)
        @property
        def e(self) -> "Num": return Num(+mpmath.e)
        @property
        def mytype(self) -> NumType: return self._mytype
        @mytype.setter
        def mytype(self, new_type: NumType) -> None:
            if hasattr(self, "_mytype") and self._mytype == new_type: return
            old_type = getattr(self, "_mytype", None)
            if old_type in (NumType.Int, NumType.Rat) and new_type.value >= NumType.Flt.value:
                if self._real == 0: self._real = self.as_mpf
            if old_type is not None and new_type.value < old_type.value:
                if new_type == NumType.Flt:
                    self._real, self._imag = abs(self.as_mpc), mpmath.mpf("0")
                elif new_type == NumType.Rat:
                    f = fractions.Fraction(float(self.as_mpf)).limit_denominator()
                    self._val = f
                elif new_type == NumType.Int and old_type != NumType.Rat:
                    self._val = fractions.Fraction(int(abs(self.as_mpf)), 1)
                if new_type.value < NumType.Unc.value:
                    self.re_unc = self.im_unc = self.correl = mpmath.mpf("0")
            self._mytype = new_type
    # Goodbye from the Mike & Don comedy show
# CHUNK: Num
if 1: # Num
    '''Manifest [20]: __init__ _promote _binary_op _make_result _normalize base help _s _r __str__ __repr__ to approx dump unit raw_value as_mpc as_mpf as_int_or_rat num pi e'''
    class Num(NumericMixin):
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
            NumType.UncCpx: t("red", "gry1"),
        }
        flip = False
        show_color = True
        active_system = "default"
        Fmt = fmt.Fmt()
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            self.arb = UnitArbiter()
            self.fmt = Num.Fmt
            if 1:   # Set default state
                self._doc = ""
                self._val: fractions.Fraction = fractions.Fraction(0)
                self._real: mpmath.mpf = mpmath.mpf("0")
                self._imag: mpmath.mpf = mpmath.mpf("0")
                self.re_unc: mpmath.mpf = mpmath.mpf("0")
                self.im_unc: mpmath.mpf = mpmath.mpf("0")
                self.correl: mpmath.mpf = mpmath.mpf("0")
                self._unit = ""
                self._mytype: NumType = NumType.Int
            if value is None:
                if unit:
                    self._unit = unit
                return
            if isinstance(value, str):
                payload = StringParser.parse(value, unit)
                if payload.type in (NumType.Int, NumType.Rat):
                    self._val = fractions.Fraction(payload.numer, payload.denom)
                else:
                    self._real, self._imag = payload.real, payload.imag
                    self.re_unc, self.im_unc = payload.re_unc, payload.im_unc
                    self.correl = payload.correl
                self._unit = payload.unit
                self.mytype = payload.type
            elif isinstance(value, Num):
                self._val = value._val
                self._real, self._imag = value._real, value._imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                self.correl = value.correl
                self._unit = unit if unit else value._unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self._val = fractions.Fraction(value)
                self.mytype = NumType.Int
            elif isinstance(value, fractions.Fraction):
                self._val = value
                self.mytype = NumType.Rat
            elif isinstance(value, (float, decimal.Decimal)):
                self._real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self._real, self._imag = mpmath.mpf(str(value.real)), mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif hasattr(value, "_mpf_") or isinstance(value, mpmath.mpf):
                self._real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self._real, self._imag = value.real, value.imag
                self.mytype = NumType.Cpx
            else:
                raise TypeError(f"Type {type(value)} not supported")
            if unit: 
                self._unit = unit
            if not (-1 <= self.correl <= 1):
                raise ValueError("Correlation coefficient must be on [-1, 1]")
        def _promote(self) -> "Num":
            'Collapse Flt back to Rat or Int if precision allows'
            if self.mytype == NumType.Flt:
                try:
                    # This limits the denominator to 1e5; I think this is a good
                    # default, as it's too easy to get large integers when converting
                    # from floats to rationals
                    f = fractions.Fraction(str(self._real)).limit_denominator()
                    # Only convert if the fraction is equal to the mpf at working
                    # precision
                    if mpmath.mpf(f.numerator) / mpmath.mpf(f.denominator) == self._real:
                        self._val = f
                        # Note:  DO NOT set ._real to 0 here, as it will break other
                        # calculations (example:  Num("3/8") + Num("1.0"))
                        self.mytype = NumType.Rat
                except:
                    pass
            if self.mytype == NumType.Rat:
                if self._val.denominator == 1:
                    self._val = self._val.numerator
                    self.mytype = NumType.Int
            elif self.mytype == NumType.Cpx:
                if self._imag == 0:
                    self.mytype = NumType.Flt
                    self._promote()
            return self
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            target_type = max(self.mytype.value, other.mytype.value)
            res_unit = self._unit
            if target_type <= NumType.Rat.value:
                raw_val = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return self._make_result(raw_val, unit=res_unit)
            if target_type >= NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            if self.mytype in (NumType.Cpx, NumType.UncCpx) or other.mytype in (NumType.Cpx, NumType.UncCpx):
                raw_val = op_func(self.as_mpc, other.as_mpc)
                return self._make_result(raw_val, unit=res_unit)
            a_val = self._real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other._real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return self._make_result(raw_val, unit=res_unit)
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit=unit)._promote()
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            # If units match or it's a multiplicative operation, return as is.
            if self._unit == other._unit or operation in ("mul", "div"):
                return other
            # If one is unitless and the other is not, we cannot normalize add/sub/cmp.
            if not self._unit or not other._unit:
                raise ValueError(f"Normalization failed: Incompatible units {self._unit!r} and {other._unit!r}")
            is_ok, factor_str = self.arb.check_conformable(other._unit, self._unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: '{other._unit}' -> '{self._unit}' ({factor_str})")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            # Determine base numeric type
            if other.mytype in (NumType.Cpx, NumType.UncCpx):
                adjusted._real = other.as_mpc.real * factor
                adjusted._imag = other.as_mpc.imag * factor
                adjusted.mytype = NumType.Cpx
            else:
                adjusted._real = other.as_mpf * factor
                adjusted.mytype = NumType.Flt
            # Preserve uncertainty and metadata
            if other.mytype in (NumType.Unc, NumType.UncCpx):
                adjusted.re_unc = other.re_unc * factor
                adjusted.im_unc = other.im_unc * factor
                adjusted.mytype = other.mytype
            adjusted._unit = self._unit
            return adjusted
        def base(self, unit: str = "") -> None:
            target = unit if unit else self._unit
            if target: print(self.arb._register_unit(target))
        def help(self, topic: str = "") -> None:
            h = Help()
            h(topic) if topic else h()
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self._val.numerator)
            elif self.mytype in (NumType.Rat, NumType.Flt):
                s = self.fmt(self.as_mpf)
            elif self.mytype == NumType.Cpx:
                s = self.fmt(self.as_mpc)
            elif self.mytype == NumType.Unc:
                s = f"{self._real} +/- {self.re_unc}"
            elif self.mytype == NumType.UncCpx:
                s = f"{self.as_mpc} +/- {self.re_unc} + {self.im_unc}i <R={self.correl}>"
            else:
                raise TypeError("Bug in type(self)")
            unit_string = f" {t.whtl}{self._unit}{t.n}" if self._unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def _r(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self._val.numerator)
            elif self.mytype == NumType.Rat:
                s = f"{self._val.numerator}/{self._val.denominator}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.as_mpc!r}"
            else:
                s = str(self._real)
            if self._unit:
                s += f" {self._unit}"
            return f"Num('{s}')"
        def __str__(self) -> str:
            return self._r() if Num.flip else self._s()
        def __repr__(self) -> str:
            return self._s() if Num.flip else self._r()
        def __hash__(self) -> int:
            '''Noether-invariant hash of an immutable physical quantity.'''
            val_str = mpmath.nstr(self.raw_value, 25)
            return hash((val_str, self._unit))
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not unit or unit == self._unit:
                return Num(self)
            is_ok, factor_str = self.arb.check_conformable(self._unit, unit)
            if not is_ok:
                self.arb._register_unit(unit)
                is_ok, factor_str = self.arb.check_conformable(self._unit, unit)
                if not is_ok: raise ValueError(f"Incompatible: {self._unit} -> {unit}")
            res = Num(self)
            res._real = res.as_mpf*mpmath.mpf(factor_str)
            res.mytype = NumType.Flt
            res._unit = unit
            return res._promote() if auto_promote else res
        def approx(self, y: ty.Any, ndigits: int) -> bool:
            if not isinstance(y, Num):
                y = Num(y)
            vx, vy = self.as_mpf, y.as_mpf
            if vy == 0:
                return abs(vx) < 10**(-ndigits)
            val = abs((vx-vy)/vy)
            return True if val == 0 else int(abs(mpmath.log10(val))) >= ndigits
        def is_equal(self, other: "Num", digits: int = None) -> bool:
            'Compare two Nums to a specified number of digits'
            # 1. Normalize units using existing logic
            if not isinstance(other, Num):
                try:
                    other = Num(other)
                except:
                    return False
            if self._unit != other._unit:
                try:
                    other = self._normalize(other, "cmp")
                except (ValueError, TypeError):
                    return False
            if self.mytype > NumType.Cpx or other.mytype > NumType.Cpx:
                print("Warning:  comparing distribution(s)", file=sys.stderr)
                return False
            # 2. Convert to mpmath
            v1, v2 = self.raw_value, other.raw_value
            m1 = self._to_mpmath(v1) 
            m2 = self._to_mpmath(v2)
            # 3. Determine precision
            # If digits is provided, epsilon = 10^-digits.
            # Otherwise use default almosteq (which is 10^(1-dps))
            if digits is not None:
                rel_eps = mpmath.mpf(10) ** -digits
                return mpmath.almosteq(m1, m2, rel_eps=rel_eps)
            else:
                return mpmath.almosteq(m1, m2)
        @property
        def dump(self) -> None:
            indent = " "*0
            d = {1: "Int", 2: "Rat", 3: "Flt", 4: "Cpx", 5: "Unc", 6: "UncCpx"}
            print(f"{indent}Num(id({hex(id(self))})) core attributes:")
            print(f"{indent}    self._val.numerator   {self._val.numerator}")
            print(f"{indent}    self._val.denominator {self._val.denominator}")
            print(f"{indent}    self._real            {self._real}")
            print(f"{indent}    self._imag            {self._imag}")
            print(f"{indent}    self.re_unc           {self.re_unc}")
            print(f"{indent}    self.im_unc           {self.im_unc}")
            print(f"{indent}    self.correl           {self.correl}")
            print(f"{indent}    self._unit             {self._unit!r}")
            print(f"{indent}    self.mytype           {self.mytype} {d[self.mytype]}")
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @property
        def raw_value(self) -> ty.Any:
            if self.mytype in (NumType.Int, NumType.Rat):
                return self._val
            return self.as_mpc if self.mytype in (NumType.Cpx, NumType.Unc, NumType.UncCpx) else self._real
        @property
        def as_mpc(self) -> mpmath.mpc:
            return (mpmath.mpc(self._real, self._imag) 
                    if self.mytype in (NumType.Cpx, NumType.Unc, NumType.UncCpx) else
                    mpmath.mpc(self.as_mpf, 0))
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype in (NumType.Int, NumType.Rat):
                return mpmath.mpf(self._val.numerator)/mpmath.mpf(self._val.denominator)
            return self._real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            return self._val
        @property
        def num(self) -> "Num":
            res = Num(self)
            res._unit = ""
            return res
        @property
        def pi(self) -> "Num": return Num(+mpmath.pi)
        @property
        def e(self) -> "Num": return Num(+mpmath.e)
        @property
        def mytype(self) -> NumType: return self._mytype
        @mytype.setter
        def mytype(self, new_type: NumType) -> None:
            if hasattr(self, "_mytype") and self._mytype == new_type: return
            old_type = getattr(self, "_mytype", None)
            if old_type in (NumType.Int, NumType.Rat) and new_type.value >= NumType.Flt.value:
                if self._real == 0: self._real = self.as_mpf
            if old_type is not None and new_type.value < old_type.value:
                if new_type == NumType.Flt:
                    self._real, self._imag = abs(self.as_mpc), mpmath.mpf("0")
                elif new_type == NumType.Rat:
                    f = fractions.Fraction(float(self.as_mpf)).limit_denominator()
                    self._val = f
                elif new_type == NumType.Int and old_type != NumType.Rat:
                    self._val = fractions.Fraction(int(abs(self.as_mpf)), 1)
                if new_type.value < NumType.Unc.value:
                    self.re_unc = self.im_unc = self.correl = mpmath.mpf("0")
            self._mytype = new_type
        @property
        def r(self) -> "Num":
            'Reduce to base units'
            # 1. Get reduction factor from the arbiter
            # Note: Arbiter method needs to handle the double newline: f"{self._unit}\n\n"
            factor, base_unit = self.arb.reduce_to_base(self._unit)
            # 2. Use the existing Num arithmetic to scale the value.
            # By multiplying a Num object by a scalar (mpf), your __mul__ 
            # should already be handling the uncertainty propagation.
            new_num = self * factor
            # 3. Update the unit string
            # We manually overwrite the unit string of the result. 
            # This keeps the uncertainty (propagated by self * factor) 
            # while correcting the dimensionality.
            new_num._unit = base_unit
            return new_num
    # Goodbye from the Mike & Don comedy show
# END_CHUNK: Num

# CHUNK: ParsedPayload
if 1: # ParsedPayload
    @dataclasses.dataclass
    class ParsedPayload:
        '''Container for decomposition results from StringParser.'''
        type: NumType
        real: mpmath.mpf
        imag: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
        numer: int = 0
        denom: int = 1
        re_unc: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
        im_unc: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
        correl: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
        unit: str = ""
# END_CHUNK: ParsedPayload

if 0:  # UnitArbiter old implementation
    '''Manifest [12]: __new__ __init__ _start_process _translate_unicode check_conformable simplify is_known_unit add_base _check_definition _register_unit inject_math'''
    class UnitArbiter:
        '''Singleton co-process manager for GNU Units.'''
        _instance = None
        units_bin = "/home/don/.0rc/bin/units"
        main_config = "/home/don/.0rc/bin/definitions.units"
        dynamic_config = "/home/don/.units_dynamic"
        read_timeout = 0.5  # Timeout in seconds for I/O operations
        def __new__(cls) -> "UnitArbiter":
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
            return cls._instance
        def __init__(self) -> None:
            if not hasattr(self, "proc"):
                self.proc = None
                self._start_process()
        def _start_process(self) -> None:
            if self.proc:
                try:
                    self.proc.terminate()
                    self.proc.wait(timeout=0.2)
                except:
                    pass
            cmd = [self.units_bin, "-t", "-d", "15"]
            if os.path.exists(self.main_config): cmd.extend(["-f", self.main_config])
            if not os.path.exists(self.dynamic_config):
                with open(self.dynamic_config, "w") as f: f.write("")
            cmd.extend(["-f", self.dynamic_config])
            Dbg(f"Units _start_process command:\n  {' '.join(cmd)}")
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def _translate_unicode(self, s: str) -> str:
            trans = str.maketrans("0123456789+-", "0123456789+-")
            return s.translate(trans).replace(" ", "*")
        def _drain_units(self):
            # Non-blocking drain of all leftover data in the stdout buffer
            while True:
                # Poll for readiness with a tiny timeout
                ready, _, _ = select.select([self.proc.stdout], [], [], 0.001)
                if not ready:
                    break
                # Read line, but do it in a way that handles partial packets
                line = self.proc.stdout.readline()
                Dbg(f"Units _drain_units flushed: {line!r}")
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            have = self._translate_unicode(have)
            want = self._translate_unicode(want)
            query = f"{have}\n{want}\n"
            if g.dbg:
                print(f"DEBUG UnitArbiter.check_conformable sent: {query!r}")
            try:
                self.proc.stdin.write(query)
                self.proc.stdin.flush()
                result_line = ""
                for _ in range(3):
                    ready, _, _ = select.select([self.proc.stdout], [], [], self.read_timeout)
                    if not ready: break
                    line = self.proc.stdout.readline().strip()
                    if g.dbg:
                        print(f"DEBUG UnitArbiter.check_conformable scanned: {line!r}")
                    # Heuristic:
                    # 1. If we see an error/unknown, we are done (False).
                    # 2. If the line is a number, the units are conformable (True).
                    if "error" in line.lower() or "unknown" in line.lower():
                        result_line = line
                        break
                    # Check if line is a valid number (conversion factor)
                    try:
                        float(line)
                        result_line = line
                        break # Found a valid conversion factor, success!
                    except ValueError:
                        continue # Keep scanning for the real result
                # If result_line is empty, check_conformable failed to get a clear answer
                is_ok = (result_line != "" and "error" not in result_line.lower() and "unknown" not in result_line.lower())
                return is_ok, result_line
            except Exception as e:
                return False, f"Error: Pipe communication failed: {str(e)}"
            finally:
                self._drain_units()
        def simplify(self, value: ty.Any, unit_str: str) -> ty.Tuple[ty.Any, str]:
            query = f"{unit_str}\n\n"
            self.proc.stdin.write(query)
            self.proc.stdin.flush()
            ready, _, _ = select.select([self.proc.stdout], [], [], self.read_timeout)
            if not ready:
                raise TimeoutError(f"Simplify timed out after {self.read_timeout}s")
            res = self.proc.stdout.readline().strip()
            Dbg("Units UnitArbiter.simplify got:  {res!r}")
            parts = res.split(" ", 1)
            conv_factor = mpmath.mpf(parts[0])
            new_unit = parts[1]
            return mpmath.mpf(value) * conv_factor, new_unit
        def reduce_to_base(self, unit_str: str) -> ty.Tuple[float, str]:
            'Reduce to base SI units'
            # Send the unit to units, using -t for terse/base output
            query = f"{unit_str}\n\n"
            self.proc.stdin.write(query)
            self.proc.stdin.flush()
            # Read the base unit reduction (e.g., "3e-06 m^2")
            ready, _, _ = select.select([self.proc.stdout], [], [], self.read_timeout)
            line = self.proc.stdout.readline().strip()
            # Parse '3e-06 m^2' into (3e-06, 'm^2')
            # Handle potential edge cases where there might not be a scalar
            parts = line.split(" ", 1)
            scalar = float(parts[0])
            base_unit = parts[1] if len(parts) > 1 else ""
            return scalar, base_unit
        def is_known_unit(self, unit_str: str) -> bool:
            if not unit_str: return True
            query = f"{unit_str}\n\n"
            Dbg(f"Units UnitArbiter.is_known_unit sent:  {query!r}")
            self.proc.stdin.write(query)
            self.proc.stdin.flush()
            ready, _, _ = select.select([self.proc.stdout], [], [], self.read_timeout)
            if not ready:
                return False
            line = self.proc.stdout.readline()
            return "unknown unit" not in line.lower()
        def add_base(self, unit_name: str) -> None:
            definition = f"{unit_name}\t\t!base!"
            with open(self.dynamic_config, "a") as f:
                f.write(f"\n{definition}\n")
            self._start_process()
            Dbg(f"Units UnitArbiter new def:  {definition!r}, restarted units process ")
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                tmp.write(definition+"\n")
                tmp_path = tmp.name
            cmd = [self.units_bin, "-c", "-q", "-f", self.dynamic_config, "-f", tmp_path]
            if os.path.exists(self.main_config):
                cmd.extend(["-f", self.main_config])
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                is_ok = (result.returncode == 0)
                error_msg = result.stderr or result.stdout
            except subprocess.TimeoutExpired:
                is_ok, error_msg = False, "Timeout validating definition."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            Dbg(f"Units UnitArbiter._check_definition:  {definition!r}")
            Dbg(f"     got:  {is_ok}, {error_msg!r}")
            return is_ok, error_msg
        def _register_unit(self, unit_name: str) -> str:
            unit_name = unit_name.strip()
            if not unit_name:
                return "Error: Unit name empty."
            if not unit_name[0].isalpha():
                return f"Error: '{unit_name}' must start with a letter."
            if self.is_known_unit(unit_name):
                return "ok"
            try:
                self.add_base(unit_name)
                return "ok"
            except Exception as e:
                return f"Error: {str(e)}"
        def inject_math(self) -> None:
            '''Inject uncertainty-aware math wrappers into __main__ namespace.'''
            import sys
            import mpmath
            from mpmath import workdps, diff, mp
            target = sys.modules["__main__"]
            def create_wrapper(func_name: str, is_dimensionless: bool = True):
                mp_func = getattr(mpmath, func_name)
                def wrapped(x: ty.Any) -> "Num":
                    if isinstance(x, Num):
                        if is_dimensionless and x._unit:
                            raise ValueError(f"{func_name} requires a dimensionless Num (got {x._unit})")
                        z_val = mp_func(x.as_mpc)
                        res_unit = "" if is_dimensionless else x._unit
                        if func_name == "sqrt":
                            res_unit = f"sqrt({x._unit})" if x._unit else ""
                        if func_name == "degrees":
                            res_unit = "deg"
                        if func_name == "radians":
                            res_unit = "rad"
                        if x.mytype not in (NumType.Unc, NumType.UncCpx):
                            return Num(z_val, unit=res_unit)
                        with workdps(mp.dps + 4):
                            h_base = mp.power(10, -(mp.dps // 2))
                            d1 = diff(mp_func, x.as_mpc, h=h_base)
                            d2 = diff(mp_func, x.as_mpc, h=h_base / 2)
                            sens = abs(d1)
                            sens2 = abs(d2)
                            if abs(sens - sens2) / (sens + 1e-30) > 0.01:
                                print(f"Warning: Possible singularity suspected in {func_name} at {x.raw_value}.\nUncertainty propagation may be non-physical.", file=sys.stderr)
                            new_re_unc = sens * x.re_unc
                            new_im_unc = sens * x.im_unc
                        res = Num(z_val, unit=res_unit)
                        res.re_unc = new_re_unc
                        res.im_unc = new_im_unc
                        res.mytype = NumType.Unc if x.mytype == NumType.Unc else NumType.UncCpx
                        return res
                    return mp_func(x)
                return wrapped
            trig_funcs = ["cos", "sin", "tan", "acos", "asin", "atan", "exp", "log"]
            misc_funcs = ["sqrt", "degrees", "radians"]
            for name in trig_funcs:
                setattr(target, name, create_wrapper(name, is_dimensionless=True))
            for name in misc_funcs:
                setattr(target, name, create_wrapper(name, is_dimensionless=False))
    # Goodbye from the Mike & Don comedy show
# CHUNK: UnitArbiter
if 1:  # UnitArbiter: Core Implementation
    class UnitArbiter:
        def __init__(self, db_path: str = "units.db"):
            self.db_path = db_path
            self._registry = {}             # Maps name -> definition string
            self._registry_scales = {}      # Cache: name -> float scale to base
            self._registry_signatures = {}  # Cache: name -> dict {base: exponent}
            self._provenance_hash = "initial_state"
            self._max_depth = 10            # Prevent infinite recursion
        def _update_provenance(self):
            self._provenance_hash = hash(frozenset(self._registry.items()))
        def GetRegistryVersion(self) -> str:
            return str(self._provenance_hash)
        def RegisterDynamicUnit(self, name: str, definition: str) -> None:
            self._registry[name] = definition
            self._registry_scales.clear()
            self._registry_signatures.clear()
            self._update_provenance()
        def Parse(self, unit_str: str) -> str:
            if " " in unit_str:
                raise ValueError(f"Internal Error: Unit token '{unit_str}' contains spaces.")
            if unit_str not in self._registry:
                raise ValueError(f"Semantic Error: Unknown unit '{unit_str}'")
            return self.SimplifyUnit(unit_str)
        def SimplifyUnit(self, unit_str: str) -> str:
            # Placeholder for reduction logic (e.g., (mm)*(mm) -> m^2)
            return unit_str
        def GetScalingFactorToBaseUnits(self, unit_str: str, _depth: int = 0) -> float:
            if _depth > self._max_depth:
                raise RecursionError(f"Circular definition or max depth exceeded at '{unit_str}'")
            if unit_str not in self._registry_scales:
                self._registry_scales[unit_str] = self._calculate_scale(unit_str, _depth)
            return self._registry_scales[unit_str]
        def _calculate_scale(self, unit_str: str, depth: int) -> float:
            definition = self._registry.get(unit_str, "")
            if not definition: # Base unit
                return 1.0
            return self._resolve_definition_value(definition, depth + 1)
        def _resolve_definition_value(self, definition: str, depth: int) -> float:
            parts = definition.split(" ", 1)
            if len(parts) == 1:
                return self.GetScalingFactorToBaseUnits(parts[0], depth)
            magnitude = float(parts[0])
            unit = parts[1]
            return magnitude * self.GetScalingFactorToBaseUnits(unit, depth)
        def GetDimensionalitySignature(self, unit_str: str) -> dict:
            if unit_str not in self._registry_signatures:
                # Placeholder for signature resolution logic
                self._registry_signatures[unit_str] = {unit_str: 1}
            return self._registry_signatures[unit_str]
# END_CHUNK: UnitArbiter

# CHUNK: StringParser
if 1:  # StringParser
    '''Manifest [4]: parse _split_input _parse_number _calc_unc'''
    class StringParser:
        '''Engine to dichotomize numeric strings and units.'''
        unit_arbiter = UnitArbiter()
        @staticmethod
        def parse(s: str, passed_unit: str = "") -> ParsedPayload:
            s = s.strip()
            num_str, unit_str = StringParser._split_input(s)
            final_unit = unit_str if unit_str else passed_unit
            if final_unit:
                StringParser.unit_arbiter._register_unit(final_unit)
            if not s:
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=0, denom=1, unit=final_unit)
            return StringParser._parse_number(num_str if num_str else s, final_unit)
        @staticmethod
        def _split_input(s: str) -> ty.Tuple[str, str]:
            if " " not in s: return s, ""
            return s.rsplit(" ", 1)
        @staticmethod
        def _parse_number(s: str, unit: str) -> ParsedPayload:
            # 1. Handle special non-numeric cases safely
            s_clean = s.strip().lower()
            if s_clean in ("inf", "nan", "-inf", "-nan", "+inf", "+nan"):
                val = mpmath.mpf(s)
                return ParsedPayload(NumType.Flt, val, unit=unit)

            # 2. Setup for general processing
            clean_s = s.replace(" ", "").replace("_", "").lower()

            # 3. Handle complex numbers explicitly
            if "j" in clean_s or ("i" in clean_s and not ("inf" in clean_s or "nan" in clean_s)):
                clean_s = clean_s.replace("i", "j")

                # Handle correlation coefficient extraction
                correl = mpmath.mpf("0")
                match_correl = re.search(r"<r=(-?[\d\.]+)>", clean_s)
                if match_correl:
                    correl = mpmath.mpf(match_correl.group(1))
                    clean_s = re.sub(r"<r=(-?[\d\.]+)>", "", clean_s)

                s_stripped = clean_s.replace("j", "")

                # Helper: returns (value, uncertainty)
                def _parse_part(part: str) -> tuple[mpmath.mpf, mpmath.mpf]:
                    if "(" in part:
                        if "/" in part: raise ValueError("Uncertainty expression cannot contain '/'")
                        # Capture optional exponent group(3)
                        match = re.fullmatch(r"([+-]?\d*\.?\d+)\(([\d\.]+)\)(.*)", part)
                        if not match: raise ValueError("Invalid uncertainty format")
                        base_val = match.group(1)
                        unc = StringParser._calc_unc(base_val, match.group(2))
                        exponent = match.group(3)
                        if exponent: 
                            unc *= mpmath.mpf("1" + exponent)
                        val = mpmath.mpf(base_val + exponent)
                        return val, unc
                    return mpmath.mpf(part), mpmath.mpf("0")

                split_idx = -1
                for i in range(len(s_stripped) - 1, 0, -1):
                    # Check if character is a sign and not part of scientific notation (e.g., e-12)
                    if s_stripped[i] in "+-" and s_stripped[i-1] != "e":
                        split_idx = i
                        break

                if split_idx != -1:
                    real_part = s_stripped[:split_idx]
                    imag_part = s_stripped[split_idx:]
                    real_val, re_unc = _parse_part(real_part)
                    if imag_part == "+": imag_val, im_unc = mpmath.mpf("1"), mpmath.mpf("0")
                    elif imag_part == "-": imag_val, im_unc = mpmath.mpf("-1"), mpmath.mpf("0")
                    else:
                        imag_val, im_unc = _parse_part(imag_part.replace("+", ""))
                else:
                    real_val, re_unc = mpmath.mpf("0"), mpmath.mpf("0")
                    if s_stripped in ("", "+"): imag_val, im_unc = mpmath.mpf("1"), mpmath.mpf("0")
                    elif s_stripped == "-": imag_val, im_unc = mpmath.mpf("-1"), mpmath.mpf("0")
                    else: imag_val, im_unc = _parse_part(s_stripped)

                has_unc = (re_unc != 0 or im_unc != 0)
                ntype = NumType.UncCpx if (correl != 0 or has_unc) else NumType.Cpx
                return ParsedPayload(ntype, real_val, imag=imag_val, re_unc=re_unc, im_unc=im_unc, correl=correl, unit=unit)

            # 4. Handle real uncertainty
            if "(" in clean_s:
                if "/" in clean_s: raise ValueError("Uncertainty expression cannot contain '/'")
                match = re.fullmatch(r"([+-]?\d*\.?\d+)\(([\d\.]+)\)(.*)", clean_s)
                if not match: raise ValueError("Invalid uncertainty format")
                base_val = match.group(1)
                unc_str = match.group(2)
                exponent = match.group(3)
                if any(c in unc_str for c in "infnan"): raise ValueError("Uncertainty cannot be inf or nan")
                re_unc = StringParser._calc_unc(base_val, unc_str)
                if exponent: re_unc *= mpmath.mpf("1" + exponent)
                return ParsedPayload(NumType.Unc, mpmath.mpf(base_val + exponent), re_unc=re_unc, unit=unit)

            # 5. Handle fractions and standard floats/ints
            if "/" in clean_s:
                f = fractions.Fraction(clean_s)
                return ParsedPayload(NumType.Rat, mpmath.mpf("0"), numer=f.numerator, denom=f.denominator, unit=unit)
            try:
                if clean_s.startswith("."): clean_s = "0" + clean_s
                elif clean_s.startswith("-."): clean_s = clean_s.replace("-.", "-0.")
                elif clean_s.startswith("+."): clean_s = clean_s.replace("+.", "+0.")
                if "." not in clean_s and "e" not in clean_s:
                    val = int(clean_s)
                    return ParsedPayload(NumType.Int, mpmath.mpf(val), numer=val, denom=1, unit=unit)
                val = mpmath.mpf(clean_s)
                return ParsedPayload(NumType.Flt, val, unit=unit)
            except:
                raise ValueError("Could not parse numeric string: " + s)
        @staticmethod
        def _calc_unc(val_str: str, unc_str: str) -> mpmath.mpf:
            decimal_places = 0
            if "." in val_str: decimal_places = len(val_str.split(".")[1])
            return mpmath.mpf(unc_str) / (10**decimal_places)
    # Goodbye from the Mike & Don comedy show
# END_CHUNK: StringParser

# CHUNK: NumFunctionPopulation
if 1:   # Global namespace function population
    unit_arbiter = UnitArbiter() # Singleton initialization
    def NoetherWrap(func_name: str, logic: str = "dimensionless"):
        '''
        Closure factory to bridge mpmath functions to Num containers,
        with support for scalars and conformable iterables.
        '''
        mp_func = getattr(mpmath, func_name)
        def wrapped(*args, **kwargs) -> "Num":
            # 1. Standardize inputs: Handle both flat args and iterable inputs
            if len(args) == 1 and isinstance(args[0], (list, tuple)):
                # Case: fsum((arg1, arg2))
                n_args = [arg if isinstance(arg, Num) else Num(arg) for arg in args[0]]
                is_iterable = True
            else:
                # Case: sin(arg1) or atan2(arg1, arg2)
                n_args = [arg if isinstance(arg, Num) else Num(arg) for arg in args]
                is_iterable = False
            # 2. Uncertainty/Correlation Alert
            for i, a in enumerate(n_args):
                if a.mytype in (NumType.Unc, NumType.UncCpx):
                    Dbg(f"{func_name} received uncertainty for arg {i}. "
                        f"Propagation not yet implemented. Uncertainty will be lost.",
                        file=sys.stderr)
            # 3. Apply Unit Logic Gates
            res_unit = ""
            if logic == "dimensionless":
                for i, a in enumerate(n_args):
                    if a._unit:
                        raise ValueError(f"{func_name} argument {i} must be dimensionless, got {a._unit}")
            elif logic == "conformable":
                if is_iterable and len(n_args) > 1:
                    # Normalize all elements in the iterable to the first element's unit
                    base = n_args[0]
                    # Apply the normalized scale so all values are conformable
                    n_args = [base._normalize(a, "add") for a in n_args]
                    res_unit = base._unit
                elif len(n_args) >= 2:
                    have, want = n_args[0]._unit, n_args[1]._unit
                    is_ok, msg = unit_arbiter.check_conformable(have, want)
                    if not is_ok:
                        raise ValueError(f"{func_name} arguments must be conformable: {have!r} vs {want!r}. ({msg})")
                    res_unit = n_args[0]._unit
            elif logic == "sqrt":
                if n_args[0]._unit:
                    res_unit = f"sqrt({n_args[0]._unit})"
            # 4. Execute using raw values
            if is_iterable:
                # Note: We don't propagate uncertainty for iterables yet
                result_val = mp_func([a.raw_value for a in n_args], **kwargs)
                return Num(result_val, unit=res_unit)._promote()
            else:
                # Check for unary uncertainty propagation
                arg = n_args[0]
                if (arg.mytype in (NumType.Unc, NumType.UncCpx)) and len(n_args) == 1:
                    # Redirect to the new helper method we just added
                    return arg._do_unary_uncertainty(mp_func, res_unit)
                # Standard path: no uncertainty or not unary
                result_val = mp_func(*[a.raw_value for a in n_args], **kwargs)
                return Num(result_val, unit=res_unit)._promote()
            # 5. Return and Promote
            return Num(result_val, unit=res_unit)._promote()
        return wrapped
    # Trigonometric, Exponential, and Scaling
    for name in ["sin", "cos", "tan", "exp", "log", "log10", "asin", "acos", "atan",
                "asinh", "acosh", "atanh", "erf", "erfc", "gamma", "degrees", "radians"]:
        if hasattr(mpmath, name):
            globals()[name] = NoetherWrap(name, logic="dimensionless")
    # Conformable Pairs
    # Note: mpmath uses 'fmod' for remainder operations.
    for name in ["atan2", "fmod", "fsum"]:
        if hasattr(mpmath, name):
            globals()[name] = NoetherWrap(name, logic="conformable")
    # Manually alias remainder to fmod if you want the same behavior,
    # or just use fmod directly.
    remainder = globals().get("fmod")
    # Special Cases
    sqrt = NoetherWrap("sqrt", logic="sqrt")
    ceil = NoetherWrap("ceil", logic="dimensionless")
    floor = NoetherWrap("floor", logic="dimensionless")
# END_CHUNK: NumFunctionPopulation

# CHUNK: NumFunctions
if 1:  # Functions
    def RegisterUnit(unit_name: str) -> None:
        '''Global helper for the Num class to ensure units are registered.'''
        UnitArbiter()._register_unit(unit_name)
    def e(n: "Num"):
        '''The "Editor" command. Spawns your $EDITOR with the Num's state.'''
        import tempfile, os, subprocess
        initial_text = f"Unit: {n._unit}\nValue: {n._real}\nDoc: {n.d}"
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+', delete=False) as tf:
            tf.write(initial_text)
            temp_path = tf.name
        # Fire up vi/vim/nano
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, temp_path])
        # ... logic to read the file back and update n.d ...
        print(f"Updated {n._unit} metadata.")
# END_CHUNK: NumFunctions

if 1:  # Help 
    class Help:
        'Adds the help() function (singleton class)'
        _instance = None
        def __new__(cls) -> "Help":
            if cls._instance is None:
                cls._instance = super(Help, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self) -> None:
            if self._initialized:
                return
            self._initialized = True
        def __call__(self, *p, **kw) -> None:
            if not p:
                print(wrap.dedent(f'''
                Num class topics:  use numinstance.help("topic"):
                    overview    Basic example of use
                    init        Getting it to work
                '''))
                return
            if p[0] == "overview":
                wall_length = Num("50 m")
                wall_length.base("nails")
                nails_per_m = Num("20 nails/m")
                print(wrap.dedent(f'''
                Num class help
                    The Num class is a number used for routine calculations in the
                    python REPL.  You can use integers, fractions, floats, and complex
                    numbers.  The numbers can also include units.  Here's a sample
                    calculation for how many nails will be needed for a long wall:
                    
                        wall_length = Num("50 m")
                        wall_length.base("nails")
                        nails_per_m = Num("20 nails/m")
                        print(f"Need {{wall_length*nails_per_m}} for the wall")
                    
                    This will print the answer
                    
                        Need {wall_length*nails_per_m} for the wall
                    
                    You can define these "semantic units" dynamically as your problem's
                    solution develops.  These units can help keep the calculation's
                    logic correct.
                '''))
if 1:   # Set up config files   ∞∞2 This needs to move out of the main code area
    UnitArbiter.main_config = "/home/don/.0rc/bin/definitions.units"
    UnitArbiter.dynamic_config = "/home/don/.units_dynamic"
    UnitArbiter.units_bin = "/home/don/.0rc/bin/units"

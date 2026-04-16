from __future__ import annotations
'''
ToDo

- Tests
    - Get some key unit tests for __add__, __radd__, and __iadd__ and friends
    - Verify infection model
    - Test formatting in detail
- Start playing with it in the REPL; it's nearly a real calculator
    - The dirt work in the back could be an excellent real-world example
    - Need some way of letting user give preferred units
        - x.preferred("ft lb"), then x.preferred() means reset to original
        - x.to("unit") should return a Num in the new unit (non-working code
          at the moment because arbiter.discover_best_unit(self.unit) isn't
          working
    - If you use an unknown unit, the server hangs
    - Changed UnitArbiter's add_primitive() to add_base() (easier to type &
      remember)
    - Any way to have a non-blocking num.check(unit) function that returns
      True if unit is known, False if not?  This would be a way to avoid the
      hang.
- Add nbs to string between number and unit in fmt.py
- Num("3/4") in the local variables causes a deep fmt exception when trying to view the
  locals in dpdb.py.  But is likely that fmt doesn't handle fractions yet.
    
'''
if 1:  # Header
    if 1:   # Standard imports
        from pdb import set_trace as yy
        import decimal
        import enum
        import fcntl
        import fractions
        import inspect
        import operator
        import os
        import pathlib
        import random
        import re
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
        __todo__      = '''These are ToDo items not to forget
            
            - Num.strict:  if on, uncertainties never compare equal.  If off, then if
              the mean and stdev match, they're equal with a warning to stderr:
              "Warning:  comparing distributions".
            - If Num.hashable is True, you might want the hash to be a tuple of the core
              values: hash((self.mytype, self.real, self.imag, self.unit)).  
            - Num.on?  Turns colorizing on/off
        
        '''
    if 1:   # Global variables
        Path = pathlib.Path
        Assert = lwtest.Assert
        t = trm.TrmDP()
        t.dbg = "#bdf6fe"
        g = dptypes.Constant()
        g.dbg = True if 0 else False
    if 1:   # Types and enums
        class NumType(enum.IntEnum):
            Int = 1
            Rat = 2
            Flt = 3
            Cpx = 4
            Unc = 5
        NumericalTypes = ty.Union[
            int , float , complex , decimal.Decimal ,
            fractions.Fraction , mpmath.mpf , mpmath.mpc ,
            uncertainties.UFloat , "Num" , str , None]
    if 1:   # Utility stuff
        def Dbg(*p, **kw):
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
            
                Caution:  The internal representation uses the mpmath library, so it's
                your responsibility as the user to ensure the mpmath context has
                sufficient resolution for your problems.  Example:  'mpmath.mp.dps = 30'
                to set 30 digits of resolution; the default is 15, about the same as a
                python float.
                
                The Num class tries to be a container for the common numbers used
                for the problems we do in the real world.  It can deal with 
                    
                    - integers
                    - fractions
                    - floating point numbers
                    - complex numbers
                    - real and complex numbers with uncertainty
                        - Uses linear uncertainty propagation
                    - physical and logical units for these numbers
                        - GNU units program used for unit conversion fractors and
                          dimensional algebra.  Because of this, you may want to
                          familiarize yourself with its syntax and capabilities.
                
                The internal representation of the Num class uses 
                    
                    - Two python integers for integers and fractions
                    - Two mpmath.mpf instances for the real and imaginary components
                    - Two mpmath.mpf instances for the uncertainties in the real and
                      imaginary components
                    - One mpmath.mpf instance for the correlation coefficient between
                      the real and imaginary components
                
                In calculations, there's an internal type hierarchy that causes type
                promotion when needed (in the enum NumType):
                
                    Int < Rat < Flt < Cpx < Unc
                
                In binary operations, the type of the result is determined by the Num
                instance's largest NumType.
                
                Units are handled by letting you write them as strings.  Behind the scenes,
                the GNU units tool handles the conversion mechanics, unit definitions, and
                dimensional algebra.  
                
                Uncertainty is handled by using linear uncertainty propagation.  
                
                "Logical" units
                
                    We usually think of units as e.g. the familiar SI units.  However,
                    almost all practical calculations involve some types of units.  For
                    example, if you're measuring ut pet food mass to feed some dogs and
                    cats, you'd probably want the calculation to use the "units"
                    kg_cat_food and kg_dog_food, assuming the dogs and cats get fed
                    different foods.  This "unit orthogonality" helps keeps the animals
                    fed properly, avoiding a mistake of mixing the foods, which might
                    show up in a calculation as having units of kg_cat_food*kg_dog_food
                    or a sum of 'kg_cat_food + kg_dog_food'.  
                
                    It's a shame the programming tools we have don't natively support
                    both physical and logical units.  One of my goals in this Num class
                    was to provide a tool to do just this, because when the units in
                    some arithmetical calculation aren't consistent, a logical error has
                    been made.  Every scientist or engineer has learned to use such
                    dimensional errors as red flags.
                
                    The interesting feature of the Num class is that you can add logical
                    units dynamically, i.e., while you're doing your calculation.  This
                    is a powerful aid to doing a correct calculation, as the GNU units
                    program will tell you if the units haven't been used correctly.
                    Imagine how many bugs could be reduced in the world's programs if we
                    had this feature in our programming environments natively.
            
        '''

if 0:  # NumericMixin
    '''Manifest [17]: __add__ __sub__ __mul__ __truediv__ __pow__ _do_uncertainty_math __lt__ __le__ __gt__ __ge__ __eq__ __abs__ __neg__ __radd__ __rsub__ __rmul__ __rtruediv__'''
    class NumericMixin:
        '''
        Operator overloading for the Num class.
        Ensures unit propagation, type promotion, and uncertainty handling.
        '''
        def __add__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "add")
            return self._binary_op(other, lambda a, b: a+b)
        def __sub__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "sub")
            return self._binary_op(other, lambda a, b: a-b)
        def __mul__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self.unit and other.unit:
                res_unit = f"({self.unit})*({other.unit})"
            elif self.unit or other.unit:
                res_unit = self.unit or other.unit
            res = self._binary_op(other, lambda a, b: a*b)
            res.unit = res_unit
            return res
        def __truediv__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self.unit and other.unit:
                res_unit = f"({self.unit})/({other.unit})"
            elif self.unit:
                res_unit = self.unit
            elif other.unit:
                res_unit = f"1/({other.unit})"
            res = self._binary_op(other, lambda a, b: a/b)
            res.unit = res_unit
            return res
        def __pow__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res = self._binary_op(other, lambda a, b: a**b)
            if self.unit:
                try:
                    exp = int(other.as_mpf)
                    res.unit = f"({self.unit})^{exp}"
                except:
                    res.unit = f"({self.unit})^({other.raw_value})"
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''Internal helper for error propagation using the uncertainties library.'''
            u1 = uncertainties.ufloat(float(self.real), float(self.re_unc))
            u2 = uncertainties.ufloat(float(other.real), float(other.re_unc))
            res_u = op_func(u1, u2)
            return Num(res_u, unit=self.unit)
        def __lt__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value < other.raw_value
        def __le__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value <= other.raw_value
        def __gt__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value > other.raw_value
        def __ge__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value >= other.raw_value
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                try:
                    other = Num(other)
                except:
                    return False
            if self.unit == other.unit:
                return self.raw_value == other.raw_value
            try:
                # If units differ, try to normalize 'other' to 'self' units via GNU Units
                # This catches (V)*(A) == kg*m^2/s^3
                other_adj = self._normalize(other, "cmp")
                return self.raw_value == other_adj.raw_value
            except (ValueError, TypeError):
                return False
        def __abs__(self) -> "Num":
            return self._make_result(abs(self.raw_value), unit=self.unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self.unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other) + self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other) - self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other) * self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other) / self
if 0:  # NumericMixin
    '''Manifest [17]: __add__ __sub__ __mul__ __truediv__ __pow__ _do_uncertainty_math __lt__ __le__ __gt__ __ge__ __eq__ __abs__ __neg__ __radd__ __rsub__ __rmul__ __rtruediv__'''
    class NumericMixin:
        '''
        Operator overloading for the Num class.
        Ensures unit propagation, type promotion, and uncertainty handling.
        '''
        def __add__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "add")
            return self._binary_op(other, lambda a, b: a+b)
        def __sub__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "sub")
            return self._binary_op(other, lambda a, b: a-b)
        def __mul__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self.unit and other.unit:
                res_unit = f"({self.unit})*({other.unit})"
            elif self.unit or other.unit:
                res_unit = self.unit or other.unit
            res = self._binary_op(other, lambda a, b: a*b)
            res.unit = res_unit
            return res
        def __truediv__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self.unit and other.unit:
                res_unit = f"({self.unit})/({other.unit})"
            elif self.unit:
                res_unit = self.unit
            elif other.unit:
                res_unit = f"1/({other.unit})"
            res = self._binary_op(other, lambda a, b: a/b)
            res.unit = res_unit
            return res
        def __pow__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res = self._binary_op(other, lambda a, b: a**b)
            if self.unit:
                try:
                    exp = int(other.as_mpf)
                    res.unit = f"({self.unit})^{exp}"
                except:
                    res.unit = f"({self.unit})^({other.raw_value})"
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''
            Vision 1: The Jacobian Propagation Engine (Optimized).
            Propagates circular uncertainty disks through complex space.
            '''
            from mpmath import workdps, diff, sqrt
            z_val = op_func(self.as_mpc, other.as_mpc)
            with workdps(mpmath.mp.dps + 4):
                df_dself = diff(lambda x: op_func(x, other.as_mpc), self.as_mpc)
                df_dother = diff(lambda y: op_func(self.as_mpc, y), other.as_mpc)
            s_sens = abs(df_dself)
            o_sens = abs(df_dother)
            var_re = (s_sens*self.re_unc)**2 + (o_sens*other.re_unc)**2
            new_re_unc = sqrt(var_re)
            var_im = (s_sens*self.im_unc)**2 + (o_sens*other.im_unc)**2
            new_im_unc = sqrt(var_im)
            res = self._make_result(z_val, unit=self.unit)
            res.re_unc = new_re_unc
            res.im_unc = new_im_unc
            res.mytype = NumType.Unc
            return res
        def __lt__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value < other.raw_value
        def __le__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value <= other.raw_value
        def __gt__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value > other.raw_value
        def __ge__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value >= other.raw_value
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                try:
                    other = Num(other)
                except:
                    return False
            if self.unit == other.unit:
                return self.raw_value == other.raw_value
            try:
                other_adj = self._normalize(other, "cmp")
                return self.raw_value == other_adj.raw_value
            except (ValueError, TypeError):
                return False
        def __abs__(self) -> "Num":
            return self._make_result(abs(self.raw_value), unit=self.unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self.unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other) + self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other) - self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other) * self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other) / self
if 1:  # NumericMixin
    '''Manifest [17]: __add__ __sub__ __mul__ __truediv__ __pow__ _do_uncertainty_math __lt__ __le__ __gt__ __ge__ __eq__ __abs__ __neg__ __radd__ __rsub__ __rmul__ __rtruediv__'''
    class NumericMixin:
        '''
        Operator overloading for the Num class.
        Ensures unit propagation, type promotion, and uncertainty handling.
        '''
        def __add__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "add")
            return self._binary_op(other, lambda a, b: a+b)
        def __sub__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "sub")
            return self._binary_op(other, lambda a, b: a-b)
        def __mul__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self.unit and other.unit:
                res_unit = f"({self.unit})*({other.unit})"
            elif self.unit or other.unit:
                res_unit = self.unit or other.unit
            res = self._binary_op(other, lambda a, b: a*b)
            res.unit = res_unit
            return res
        def __truediv__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res_unit = ""
            if self.unit and other.unit:
                res_unit = f"({self.unit})/({other.unit})"
            elif self.unit:
                res_unit = self.unit
            elif other.unit:
                res_unit = f"1/({other.unit})"
            res = self._binary_op(other, lambda a, b: a/b)
            res.unit = res_unit
            return res
        def __pow__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            res = self._binary_op(other, lambda a, b: a**b)
            if self.unit:
                try:
                    exp = int(other.as_mpf)
                    res.unit = f"({self.unit})^{exp}"
                except:
                    res.unit = f"({self.unit})^({other.raw_value})"
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''
            Vision 1: The Jacobian Propagation Engine.
            Hygiene Fix: Uses mp_sqrt to avoid global namespace collision.
            '''
            from mpmath import workdps, diff, sqrt as mp_sqrt
            z_val = op_func(self.as_mpc, other.as_mpc)
            with workdps(mpmath.mp.dps + 4):
                df_dself = diff(lambda x: op_func(x, other.as_mpc), self.as_mpc)
                df_dother = diff(lambda y: op_func(self.as_mpc, y), other.as_mpc)
                s_sens = abs(df_dself)
                o_sens = abs(df_dother)
                var_re = (s_sens*self.re_unc)**2 + (o_sens*other.re_unc)**2
                # CRITICAL: Use mp_sqrt here, NOT the global sqrt
                new_re_unc = mp_sqrt(var_re)
                var_im = (s_sens*self.im_unc)**2 + (o_sens*other.im_unc)**2
                new_im_unc = mp_sqrt(var_im)
            res = Num(z_val, unit=self.unit)
            res.re_unc = new_re_unc
            res.im_unc = new_im_unc
            res.mytype = NumType.Unc
            return res
        def __lt__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value < other.raw_value
        def __le__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value <= other.raw_value
        def __gt__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value > other.raw_value
        def __ge__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                other = Num(other)
            other = self._normalize(other, "cmp")
            return self.raw_value >= other.raw_value
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, Num):
                try:
                    other = Num(other)
                except:
                    return False
            if self.unit == other.unit:
                return self.raw_value == other.raw_value
            try:
                other_adj = self._normalize(other, "cmp")
                return self.raw_value == other_adj.raw_value
            except (ValueError, TypeError):
                return False
        def __abs__(self) -> "Num":
            return self._make_result(abs(self.raw_value), unit=self.unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self.unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other) + self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other) - self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other) * self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other) / self

if 0:  # Num
    '''Manifest [24]: __init__ almost as_int_or_rat as_mpc as_mpf base help num _promote raw_value to unit _binary_op _extract_unit _make_result _normalize _parse_proper_fraction _parse_string _r _s __repr__ __str__ __pow__'''
    class Num(NumericMixin):
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
        }
        flip = False
        show_color = True
        active_system = "default"
        Fmt = fmt.Fmt()
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            '''Constructor for the Num instance, an immutable number container'''
            self._doc = ""
            self.arb = UnitArbiter()
            self.fmt = Num.Fmt
            if isinstance(value, str):
                val_str, found_unit = self._extract_unit(value)
                if found_unit:
                    unit = found_unit if not unit else f"({found_unit})*({unit})"
                value = val_str
            self.numer: int = 0
            self.denom: int = 1
            self.real: mpmath.mpf = mpmath.mpf("0")
            self.imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self.mytype: NumType = NumType.Int
            if unit:
                self.unit = unit
            if value is None:
                return
            if isinstance(value, Num):
                self.numer, self.denom = value.numer, value.denom
                self.real, self.imag = value.real, value.imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                self._unit = unit if unit else value.unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self.numer = value
                self.mytype = NumType.Int
            elif isinstance(value, fractions.Fraction):
                self.numer, self.denom = value.numerator, value.denominator
                self.mytype = NumType.Rat
            elif isinstance(value, (float, decimal.Decimal)):
                self.real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self.real = mpmath.mpf(str(value.real))
                self.imag = mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif hasattr(value, "_mpf_") or isinstance(value, mpmath.mpf):
                self.real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self.real, self.imag = value.real, value.imag
                self.mytype = NumType.Cpx
            elif isinstance(value, uncertainties.UFloat):
                self.real = mpmath.mpf(str(value.nominal_value))
                self.re_unc = mpmath.mpf(str(value.std_dev))
                self.mytype = NumType.Unc
            elif isinstance(value, str):
                self._parse_string(value.strip())
            else:
                raise TypeError(f"Type of {value!r} is not supported")
        def _promote(self) -> "Num":
            '''Central hygiene method to find LCD for rationals and collapse imaginary zeros.'''
            if self.mytype == NumType.Rat:
                f = fractions.Fraction(self.numer, self.denom)
                self.numer, self.denom = f.numerator, f.denominator
                if self.denom == 1:
                    self.mytype = NumType.Int
            elif self.mytype == NumType.Cpx:
                if self.imag == 0:
                    self.mytype = NumType.Flt
            return self
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''Dispatches math operations and preserves unit context.'''
            target_type = max(self.mytype.value, other.mytype.value)
            res_unit = self.unit
            if target_type <= NumType.Rat.value:
                raw_val = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return self._make_result(raw_val, unit=res_unit)
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                raw_val = op_func(self.as_mpc, other.as_mpc)
                return self._make_result(raw_val, unit=res_unit)
            a_val = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other.real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return self._make_result(raw_val, unit=res_unit)
        def __pow__(self, other: ty.Any) -> "Num":
            '''Handle exponentiation and unit dimensionality changes.'''
            if not isinstance(other, Num):
                other = Num(other)
            if self.unit:
                if other.mytype == NumType.Cpx or other.unit:
                    raise TypeError("Complex or dimensioned exponents not supported on units")
                exp_val = str(other.raw_value)
                new_unit_expr = f"({self.unit})^{exp_val}"
                res = self._binary_op(other, lambda a, b: a**b)
                new_mag, clean_unit = self.arb.simplify(res.raw_value, new_unit_expr)
                res.real = mpmath.mpf(str(new_mag))
                res._unit = clean_unit
                res.mytype = NumType.Flt
                return res._promote()
            return self._binary_op(other, lambda a, b: a**b)
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            '''Internal factory to ensure all math results are immediately promoted.'''
            return Num(value, unit=unit)._promote()
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            if self.unit == other.unit:
                return other
            if operation in ("mul", "div"):
                return other
            if operation in ("add", "sub", "cmp"):
                if bool(self.unit) != bool(other.unit):
                    raise ValueError(f"Unit Mismatch: {self.unit} vs {other.unit}")
            is_ok, factor_str = self.arb.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            if adjusted.mytype <= NumType.Rat:
                adjusted.real = adjusted.as_mpf*factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real *= factor
                adjusted.imag *= factor
                adjusted.re_unc *= factor
                adjusted.im_unc *= factor
            adjusted._unit = self.unit
            return adjusted
        def _parse_proper_fraction(self, s: str) -> mpmath.mpf:
            regex = r"^([+-])?(\d+)?(?:[- ](\d+)/(\d+))?$"
            match = re.match(regex, s.strip())
            if not match:
                raise ValueError(f"Invalid fraction format: {s}")
            sign = -1 if match.group(1) == "-" else 1
            whole = int(match.group(2)) if match.group(2) else 0
            num = int(match.group(3)) if match.group(3) else 0
            den = int(match.group(4)) if match.group(4) else 1
            return sign*(mpmath.mpf(whole)+(mpmath.mpf(num)/mpmath.mpf(den)))
        def _parse_string(self, value: str) -> None:
            raw = value.strip().replace(" ", "").lower()
            if not raw:
                raise ValueError("Empty string provided to Num")
            if raw in ("inf", "-inf", "nan"):
                self.real = mpmath.mpf(raw)
                self.mytype = NumType.Flt
                return
            if re.fullmatch(r"[+-]?\d+", raw):
                self.numer = int(raw)
                self.mytype = NumType.Int
                return
            if ("/" in raw and "-" in raw and raw[0] != "-"):
                self.real = self._parse_proper_fraction(value)
                self.mytype = NumType.Flt
                return
            if "/" in raw and "j" not in raw and "i" not in raw:
                parts = raw.split("/")
                if len(parts) == 2:
                    try:
                        self.numer, self.denom = int(parts[0]), int(parts[1])
                        if self.denom == 0:
                            raise ZeroDivisionError
                        self.mytype = NumType.Rat
                        return
                    except (ValueError, ZeroDivisionError): 
                        pass
            norm = raw.replace("i", "j")
            pattern = r"(?<!e)(?=[+-])"
            parts = [p for p in re.split(pattern, norm) if p]
            try:
                if len(parts) == 1:
                    p = parts[0]
                    if p.endswith("j"):
                        val = p[:-1].replace("+", "")
                        if val in ("", "-"):
                            val += "1"
                        self.imag = mpmath.mpf(val)
                        self.mytype = NumType.Cpx
                    else:
                        self.real = mpmath.mpf(p.replace("+", ""))
                        self.mytype = NumType.Flt
                elif len(parts) == 2:
                    re_p, im_p = parts
                    if not im_p.endswith("j"):
                        self.real = mpmath.mpf(norm.replace("+", ""))
                        self.mytype = NumType.Flt
                    else:
                        self.real = mpmath.mpf(re_p.replace("+", ""))
                        val = im_p[:-1].replace("+", "")
                        if val in ("", "-"):
                            val += "1"
                        self.imag = mpmath.mpf(val)
                        self.mytype = NumType.Cpx
                else:
                    self.real = mpmath.mpf(norm.replace("+", ""))
                    self.mytype = NumType.Flt
            except:
                raise ValueError(f"Could not parse numeric part: {value}")
        def _extract_unit(self, s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s:
                return s, ""
            parts = s.rsplit(None, 1)
            val_part, unit_part = parts
            if unit_part[0].isalpha() or unit_part[0] in "(%":
                if not val_part.lower().endswith("e"):
                    return val_part.strip(), unit_part.strip()
            return s, ""
        def base(self, unit: str = "") -> None:
            if not isinstance(unit, str):
                raise TypeError(f"Unit must be a string, not {type(unit).__name__}")
            target = unit if unit else self.unit
            if not target:
                print("No unit provided to register.")
                return
            status = self.arb._register_unit(target)
            if status != "ok":
                print(status)
        def help(self, topic: str = "") -> None:
            if not isinstance(topic, str):
                raise TypeError(f"Topic must be a string, not {type(topic).__name__}")
            h = Help()
            if not topic:
                h()
            else:
                h(topic)
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = self.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                s = self.fmt(self.as_mpc)
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = self.fmt(self.real)
            unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def _r(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self.numer)
            elif self.mytype == NumType.Rat:
                s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.as_mpc!r}"
            else:
                s = str(self.real)
            if self.unit:
                s += f" {self.unit}"
            return f"Num('{s}')"
        def __str__(self) -> str:
            return self._r() if Num.flip else self._s()
        def __repr__(self) -> str:
            return self._s() if Num.flip else self._r()
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not isinstance(unit, str):
                raise TypeError(f"Target unit must be a string, not {type(unit).__name__}")
            if not unit or unit == self.unit:
                return Num(self)
            is_ok, factor_str = self.arb.check_conformable(self.unit, unit)
            if not is_ok:
                self.arb._register_unit(unit)
                is_ok, factor_str = self.arb.check_conformable(self.unit, unit)
                if not is_ok:
                    raise ValueError(f"Incompatible: {self.unit} -> {unit}")
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            res.real = res.as_mpf*factor
            res.mytype = NumType.Flt
            res._unit = unit
            return res._promote() if auto_promote else res
        def almost(self, y: ty.Union["Num", float, int, mpmath.mpf, mpmath.mpc], ndigits: int) -> bool:
            if not isinstance(ndigits, int):
                raise TypeError(f"ndigits must be an int, not {type(ndigits).__name__}")
            assert ndigits > 0
            if not isinstance(y, Num):
                y = Num(y)
            if self == y:
                return True
            vx, vy = self.as_mpf, y.as_mpf
            if vy == 0:
                return abs(vx) < 10**(-ndigits)
            val = abs((vx-vy)/vy)
            if val == 0:
                return True
            return int(abs(mpmath.log10(val))) >= ndigits
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @unit.setter
        def unit(self, value: str) -> None:
            if not isinstance(value, str):
                raise TypeError("Unit must be a string")
            if value:
                self.arb._register_unit(value)
                self._unit = value.strip()
            else:
                self._unit = ""
        @property
        def raw_value(self) -> ty.Union[int, mpmath.mpf, mpmath.mpc]:
            if self.mytype == NumType.Int:
                return self.numer
            if self.mytype == NumType.Rat:
                return self.numer/self.denom
            if self.mytype == NumType.Cpx:
                return self.as_mpc
            return self.real
        @property
        def as_mpc(self) -> mpmath.mpc:
            if self.mytype == NumType.Cpx:
                return mpmath.mpc(self.real, self.imag)
            return mpmath.mpc(self.as_mpf, 0)
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype == NumType.Int:
                return mpmath.mpf(str(self.numer))
            if self.mytype == NumType.Rat:
                return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self.real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            if self.mytype == NumType.Int:
                return self.numer
            return fractions.Fraction(self.numer, self.denom)
        @property
        def num(self) -> "Num":
            '''Returns the dimensionless magnitude component as a Num object.'''
            res = Num(self)
            res.unit = ""
            return res
if 1:  # Num
    '''Manifest [24]: __init__ almost as_int_or_rat as_mpc as_mpf base help num _promote raw_value to unit _binary_op _extract_unit _make_result _normalize _parse_proper_fraction _parse_string _r _s __repr__ __str__ __pow__'''
    class Num(NumericMixin):
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
        }
        flip = False
        show_color = True
        active_system = "default"
        Fmt = fmt.Fmt()
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            self._doc = ""
            self.arb = UnitArbiter()
            self.fmt = Num.Fmt
            if isinstance(value, str):
                val_str, found_unit = self._extract_unit(value)
                if found_unit:
                    unit = found_unit if not unit else f"({found_unit})*({unit})"
                value = val_str
            self.numer: int = 0
            self.denom: int = 1
            self.real: mpmath.mpf = mpmath.mpf("0")
            self.imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self.mytype: NumType = NumType.Int
            if unit:
                self.unit = unit
            if value is None:
                return
            if isinstance(value, Num):
                self.numer, self.denom = value.numer, value.denom
                self.real, self.imag = value.real, value.imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                self._unit = unit if unit else value.unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self.numer = value
                self.mytype = NumType.Int
            elif isinstance(value, fractions.Fraction):
                self.numer, self.denom = value.numerator, value.denominator
                self.mytype = NumType.Rat
            elif isinstance(value, (float, decimal.Decimal)):
                self.real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self.real = mpmath.mpf(str(value.real))
                self.imag = mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif hasattr(value, "_mpf_") or isinstance(value, mpmath.mpf):
                self.real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self.real, self.imag = value.real, value.imag
                self.mytype = NumType.Cpx
            elif isinstance(value, uncertainties.UFloat):
                self.real = mpmath.mpf(str(value.nominal_value))
                self.re_unc = mpmath.mpf(str(value.std_dev))
                self.mytype = NumType.Unc
            elif isinstance(value, str):
                self._parse_string(value.strip())
            else:
                raise TypeError(f"Type of {value!r} is not supported")
        def _promote(self) -> "Num":
            if self.mytype == NumType.Rat:
                f = fractions.Fraction(self.numer, self.denom)
                self.numer, self.denom = f.numerator, f.denominator
                if self.denom == 1:
                    self.mytype = NumType.Int
            elif self.mytype == NumType.Cpx:
                if self.imag == 0:
                    self.mytype = NumType.Flt
            return self
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            target_type = max(self.mytype.value, other.mytype.value)
            res_unit = self.unit
            if target_type <= NumType.Rat.value:
                raw_val = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return self._make_result(raw_val, unit=res_unit)
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                raw_val = op_func(self.as_mpc, other.as_mpc)
                return self._make_result(raw_val, unit=res_unit)
            a_val = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other.real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return self._make_result(raw_val, unit=res_unit)
        def __pow__(self, other: ty.Any) -> "Num":
            if not isinstance(other, Num):
                other = Num(other)
            if self.unit:
                if other.mytype == NumType.Cpx or other.unit:
                    raise TypeError("Complex or dimensioned exponents not supported on units")
                exp_val = str(other.raw_value)
                new_unit_expr = f"({self.unit})^{exp_val}"
                res = self._binary_op(other, lambda a, b: a**b)
                new_mag, clean_unit = self.arb.simplify(res.raw_value, new_unit_expr)
                res.real = mpmath.mpf(str(new_mag))
                res._unit = clean_unit
                res.mytype = NumType.Flt
                return res._promote()
            return self._binary_op(other, lambda a, b: a**b)
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit=unit)._promote()
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            if self.unit == other.unit:
                return other
            if operation in ("mul", "div"):
                return other
            if operation in ("add", "sub", "cmp"):
                if bool(self.unit) != bool(other.unit):
                    raise ValueError(f"Unit Mismatch: {self.unit} vs {other.unit}")
            is_ok, factor_str = self.arb.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            if adjusted.mytype <= NumType.Rat:
                adjusted.real = adjusted.as_mpf*factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real *= factor
                adjusted.imag *= factor
                adjusted.re_unc *= factor
                adjusted.im_unc *= factor
            adjusted._unit = self.unit
            return adjusted
        def _parse_proper_fraction(self, s: str) -> mpmath.mpf:
            regex = r"^([+-])?(\d+)?(?:[- ](\d+)/(\d+))?$"
            match = re.match(regex, s.strip())
            if not match:
                raise ValueError(f"Invalid fraction format: {s}")
            sign = -1 if match.group(1) == "-" else 1
            whole = int(match.group(2)) if match.group(2) else 0
            num = int(match.group(3)) if match.group(3) else 0
            den = int(match.group(4)) if match.group(4) else 1
            return sign*(mpmath.mpf(whole)+(mpmath.mpf(num)/mpmath.mpf(den)))
        def _parse_string(self, value: str) -> None:
            raw = value.strip().replace(" ", "").lower()
            if not raw:
                raise ValueError("Empty string provided to Num")
            if raw in ("inf", "-inf", "nan"):
                self.real = mpmath.mpf(raw)
                self.mytype = NumType.Flt
                return
            if re.fullmatch(r"[+-]?\d+", raw):
                self.numer = int(raw)
                self.mytype = NumType.Int
                return
            if ("/" in raw and "-" in raw and raw[0] != "-"):
                self.real = self._parse_proper_fraction(value)
                self.mytype = NumType.Flt
                return
            if "/" in raw and "j" not in raw and "i" not in raw:
                parts = raw.split("/")
                if len(parts) == 2:
                    try:
                        self.numer, self.denom = int(parts[0]), int(parts[1])
                        if self.denom == 0:
                            raise ZeroDivisionError
                        self.mytype = NumType.Rat
                        return
                    except (ValueError, ZeroDivisionError):
                        pass
            norm = raw.replace("i", "j")
            pattern = r"(?<!e)(?=[+-])"
            parts = [p for p in re.split(pattern, norm) if p]
            try:
                if len(parts) == 1:
                    p = parts[0]
                    if p.endswith("j"):
                        val = p[:-1].replace("+", "")
                        if val in ("", "-"):
                            val += "1"
                        self.imag = mpmath.mpf(val)
                        self.mytype = NumType.Cpx
                    else:
                        self.real = mpmath.mpf(p.replace("+", ""))
                        self.mytype = NumType.Flt
                elif len(parts) == 2:
                    re_p, im_p = parts
                    if not im_p.endswith("j"):
                        self.real = mpmath.mpf(norm.replace("+", ""))
                        self.mytype = NumType.Flt
                    else:
                        self.real = mpmath.mpf(re_p.replace("+", ""))
                        val = im_p[:-1].replace("+", "")
                        if val in ("", "-"):
                            val += "1"
                        self.imag = mpmath.mpf(val)
                        self.mytype = NumType.Cpx
                else:
                    self.real = mpmath.mpf(norm.replace("+", ""))
                    self.mytype = NumType.Flt
            except:
                raise ValueError(f"Could not parse numeric part: {value}")
        def _extract_unit(self, s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s:
                return s, ""
            parts = s.rsplit(None, 1)
            val_part, unit_part = parts
            if unit_part[0].isalpha() or unit_part[0] in "(%":
                if not val_part.lower().endswith("e"):
                    return val_part.strip(), unit_part.strip()
            return s, ""
        def base(self, unit: str = "") -> None:
            if not isinstance(unit, str):
                raise TypeError(f"Unit must be a string, not {type(unit).__name__}")
            target = unit if unit else self.unit
            if not target:
                print("No unit provided to register.")
                return
            status = self.arb._register_unit(target)
            if status != "ok":
                print(status)
        def help(self, topic: str = "") -> None:
            if not isinstance(topic, str):
                raise TypeError(f"Topic must be a string, not {type(topic).__name__}")
            h = Help()
            if not topic:
                h()
            else:
                h(topic)
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = self.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                s = self.fmt(self.as_mpc)
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = self.fmt(self.real)
            unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def _r(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self.numer)
            elif self.mytype == NumType.Rat:
                s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.as_mpc!r}"
            else:
                s = str(self.real)
            if self.unit:
                s += f" {self.unit}"
            return f"Num('{s}')"
        def __str__(self) -> str:
            return self._r() if Num.flip else self._s()
        def __repr__(self) -> str:
            return self._s() if Num.flip else self._r()
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not isinstance(unit, str):
                raise TypeError(f"Target unit must be a string, not {type(unit).__name__}")
            if not unit or unit == self.unit:
                return Num(self)
            is_ok, factor_str = self.arb.check_conformable(self.unit, unit)
            if not is_ok:
                self.arb._register_unit(unit)
                is_ok, factor_str = self.arb.check_conformable(self.unit, unit)
                if not is_ok:
                    raise ValueError(f"Incompatible: {self.unit} -> {unit}")
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            res.real = res.as_mpf*factor
            res.mytype = NumType.Flt
            res._unit = unit
            return res._promote() if auto_promote else res
        def approx(self, y: ty.Union["Num", float, int, mpmath.mpf, mpmath.mpc], ndigits: int) -> bool:
            '''Returns True if self and y are approximately == to about 1 part in 10**ndigits
            
            Example:  if self = Num(1) and y = Num(1.01), then
                self.approx(y, 2) returns True
                self.approx(y, 3) returns False
            The approximate conclusion is that self and y are approximately equal to two
            decimal digits, but not three; i.e., equal to about 1 part in 100, but not
            equal to 1 part in 1000.
            '''
            if not isinstance(ndigits, int):
                raise TypeError(f"ndigits must be an int, not {type(ndigits).__name__}")
            assert ndigits > 0
            if not isinstance(y, Num):
                y = Num(y)
            if self == y:
                return True
            vx, vy = self.as_mpf, y.as_mpf
            if vy == 0:
                return abs(vx) < 10**(-ndigits)
            val = abs((vx-vy)/vy)
            if val == 0:
                return True
            return int(abs(mpmath.log10(val))) >= ndigits
        def dump(self, indent: str = "") -> str:
            'Dump our current state to stdout'
            print(f"{indent}Num(<id(self)>) core attributes:")
            print(f"{indent}    self.numer   {self.numer}")
            print(f"{indent}    self.denom   {self.denom}")
            print(f"{indent}    self.real    {self.real}")
            print(f"{indent}    self.imag    {self.imag}")
            print(f"{indent}    self.re_unc  {self.re_unc}")
            print(f"{indent}    self.im_unc  {self.im_unc}")
            print(f"{indent}    self.correl  {self.correl}")
            print(f"{indent}    self.unit    {self.unit!r}")
            print(f"{indent}    self.mytype  {self.mytype}")
            print(f"{indent}    1=Int, 2=Rat, 3=Flt, 4=Cpx, 5=Unc")
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @unit.setter
        def unit(self, value: str) -> None:
            if not isinstance(value, str):
                raise TypeError("Unit must be a string")
            if value:
                self.arb._register_unit(value)
                self._unit = value.strip()
            else:
                self._unit = ""
        @property
        def raw_value(self) -> ty.Union[int, mpmath.mpf, mpmath.mpc]:
            if self.mytype == NumType.Int:
                return self.numer
            if self.mytype == NumType.Rat:
                return self.numer/self.denom
            if self.mytype == NumType.Cpx:
                return self.as_mpc
            return self.real
        @property
        def as_mpc(self) -> mpmath.mpc:
            if self.mytype == NumType.Cpx:
                return mpmath.mpc(self.real, self.imag)
            return mpmath.mpc(self.as_mpf, 0)
        @property
        def as_mpf(self) -> mpmath.mpf:
            # If we have an integer or ratio magnitude, use it regardless of mytype
            if self.numer != 0:
                return mpmath.mpf(self.numer) / mpmath.mpf(self.denom)
            # Otherwise fall back to the float storage
            return self.real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            if self.mytype == NumType.Int:
                return self.numer
            return fractions.Fraction(self.numer, self.denom)
        @property
        def num(self) -> "Num":
            res = Num(self)
            res.unit = ""
            return res

if 0:  # UnitArbiter
    '''Manifest [10]: __new__ __init__ _start_process _translate_unicode check_conformable simplify is_known_unit add_base _check_definition _register_unit'''
    class UnitArbiter:
        '''
        Singleton co-process manager for GNU Units integration.
        Handles unit conversion, conformability checks, and dynamic unit registration.
        '''
        _instance = None
        units_bin: str = "units"
        main_config: str = ""
        dynamic_config: str = "~/.units_dynamic"
        def __new__(cls) -> "UnitArbiter":
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self) -> None:
            if self._initialized:
                return
            self.bin_path = str(Path(UnitArbiter.units_bin).expanduser())
            self.dynamic_path = Path(UnitArbiter.dynamic_config).expanduser()
            if not self.dynamic_path.exists():
                self.dynamic_path.parent.mkdir(parents=True, exist_ok=True)
                self.dynamic_path.touch()
            self.proc = None
            self._start_process()
            self._initialized = True
        def _start_process(self) -> None:
            '''Launches GNU Units in compact mode to ensure symbols over words.'''
            if self.proc:
                try:
                    self.proc.terminate()
                    self.proc.wait(timeout=0.2)
                except:
                    pass
            cmd = [self.bin_path, "-q", "--compact", "-t"]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            cmd.extend(["-f", str(self.dynamic_path)])
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def _translate_unicode(self, s: str) -> str:
            '''Converts superscript unicode exponents to ASCII carats for GNU Units.'''
            # Only translate actual superscript characters, not regular digits
            superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            exp_map = str.maketrans(superscripts, "0123456789")
            out = ""
            for char in s:
                if char in superscripts:
                    out += "^" + char.translate(exp_map)
                else:
                    out += char
            return out
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            if not have or not want:
                return (True, "1.0") if have == want else (False, "Mismatch")
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            try:
                self.proc.stdin.write(f"{self._translate_unicode(have)}\n{self._translate_unicode(want)}\n")
                self.proc.stdin.flush()
                line = self.proc.stdout.readline().strip()
                if not line:
                    return False, f"Empty response from GNU units: {have} to {want}"
                if "conformability error" in line.lower() or "unknown" in line.lower():
                    return False, line
                try:
                    mpmath.mpf(line)
                    return True, line
                except:
                    return False, f"Unexpected GNU units output: {line}"
            except Exception as e:
                self._start_process()
                return False, str(e)
        def simplify(self, value: ty.Any, unit_str: str) -> tuple[ty.Any, str]:
            if not unit_str or unit_str == "1":
                return value, ""
            cmd = [self.bin_path, "-q", "--compact", "-t", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            proc = subprocess.run(cmd + [self._translate_unicode(unit_str)], capture_output=True, text=True)
            output = proc.stdout.strip()
            match = re.match(r'^([\d.e+-]+)?\s*(.*)$', output)
            factor = mpmath.mpf(match.group(1) or "1.0") if match else mpmath.mpf("1.0")
            remainder = match.group(2).strip() if match else unit_str
            if "=" in remainder:
                remainder = remainder.split("=")[0].strip()
            return value * factor, remainder
        def is_known_unit(self, unit_str: str) -> bool:
            if not unit_str:
                return True
            cmd = [self.bin_path, "-q", "-t", "--compact", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            res = subprocess.run(cmd + [self._translate_unicode(unit_str)], capture_output=True, text=True)
            return res.returncode == 0 and "error" not in res.stderr.lower()
        def add_base(self, unit_name: str) -> None:
            definition = f"{unit_name}\t!"
            is_ok, err = self._check_definition(definition)
            if not is_ok:
                raise ValueError(f"Invalid unit definition for '{unit_name}': {err}")
            with open(self.dynamic_path, "a") as f:
                f.write(f"\n{definition}\n")
            self._start_process()
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                tmp.write(definition + "\n")
                tmp_path = tmp.name
            cmd = [self.bin_path, "-c", "-q"]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            cmd.extend(["-f", str(self.dynamic_path), "-f", tmp_path])
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                is_ok = (result.returncode == 0)
                error_msg = result.stderr or result.stdout
            except subprocess.TimeoutExpired:
                is_ok, error_msg = False, "Timeout validating definition."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
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
if 1:  # UnitArbiter
    '''Manifest [11]: __new__ __init__ _start_process _translate_unicode check_conformable simplify is_known_unit add_base _check_definition _register_unit inject_math'''
    class UnitArbiter:
        '''
        Singleton co-process manager for GNU Units and Math Orchestration.
        Handles unit conversion and injects uncertainty-aware math wrappers.
        '''
        _instance = None
        units_bin: str = "units"
        main_config: str = ""
        dynamic_config: str = "~/.units_dynamic"
        def __new__(cls) -> "UnitArbiter":
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self) -> None:
            if self._initialized:
                return
            self.bin_path = str(Path(UnitArbiter.units_bin).expanduser())
            self.dynamic_path = Path(UnitArbiter.dynamic_config).expanduser()
            if not self.dynamic_path.exists():
                self.dynamic_path.parent.mkdir(parents=True, exist_ok=True)
                self.dynamic_path.touch()
            self.proc = None
            self._start_process()
            self._initialized = True
            # Lift math functions into the global namespace
            self.inject_math()
        def _start_process(self) -> None:
            '''Launches GNU Units in compact mode to ensure symbols over words.'''
            if self.proc:
                try:
                    self.proc.terminate()
                    self.proc.wait(timeout=0.2)
                except:
                    pass
            cmd = [self.bin_path, "-q", "--compact", "-t"]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            cmd.extend(["-f", str(self.dynamic_path)])
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def _translate_unicode(self, s: str) -> str:
            '''Converts superscript unicode exponents to ASCII carats for GNU Units.'''
            superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            exp_map = str.maketrans(superscripts, "0123456789")
            out = ""
            for char in s:
                if char in superscripts:
                    out += "^" + char.translate(exp_map)
                else:
                    out += char
            return out
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            if not have or not want:
                return (True, "1.0") if have == want else (False, "Mismatch")
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            try:
                self.proc.stdin.write(f"{self._translate_unicode(have)}\n{self._translate_unicode(want)}\n")
                self.proc.stdin.flush()
                line = self.proc.stdout.readline().strip()
                if not line:
                    return False, f"Empty response from GNU units: {have} to {want}"
                if "conformability error" in line.lower() or "unknown" in line.lower():
                    return False, line
                try:
                    mpmath.mpf(line)
                    return True, line
                except:
                    return False, f"Unexpected GNU units output: {line}"
            except Exception as e:
                self._start_process()
                return False, str(e)
        def simplify(self, value: ty.Any, unit_str: str) -> tuple[ty.Any, str]:
            if not unit_str or unit_str == "1":
                return value, ""
            cmd = [self.bin_path, "-q", "--compact", "-t", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            proc = subprocess.run(cmd + [self._translate_unicode(unit_str)], capture_output=True, text=True)
            output = proc.stdout.strip()
            match = re.match(r'^([\d.e+-]+)?\s*(.*)$', output)
            factor = mpmath.mpf(match.group(1) or "1.0") if match else mpmath.mpf("1.0")
            remainder = match.group(2).strip() if match else unit_str
            if "=" in remainder:
                remainder = remainder.split("=")[0].strip()
            return value * factor, remainder
        def is_known_unit(self, unit_str: str) -> bool:
            if not unit_str:
                return True
            cmd = [self.bin_path, "-q", "-t", "--compact", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            res = subprocess.run(cmd + [self._translate_unicode(unit_str)], capture_output=True, text=True)
            return res.returncode == 0 and "error" not in res.stderr.lower()
        def add_base(self, unit_name: str) -> None:
            definition = f"{unit_name}\t!"
            is_ok, err = self._check_definition(definition)
            if not is_ok:
                raise ValueError(f"Invalid unit definition for '{unit_name}': {err}")
            with open(self.dynamic_path, "a") as f:
                f.write(f"\n{definition}\n")
            self._start_process()
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                tmp.write(definition + "\n")
                tmp_path = tmp.name
            cmd = [self.bin_path, "-c", "-q"]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            cmd.extend(["-f", str(self.dynamic_path), "-f", tmp_path])
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                is_ok = (result.returncode == 0)
                error_msg = result.stderr or result.stdout
            except subprocess.TimeoutExpired:
                is_ok, error_msg = False, "Timeout validating definition."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
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
            '''
            Automated Math Orchestrator. 
            Injects uncertainty-aware wrappers into the global namespace.
            '''
            import sys
            import mpmath
            from mpmath import workdps, diff, sqrt as mp_sqrt
            target = sys.modules['__main__']
            def create_wrapper(func_name: str, is_dimensionless: bool = True):
                mp_func = getattr(mpmath, func_name)
                def wrapped(x: ty.Any) -> "Num":
                    # If it's already a Num, proceed with Noether logic
                    if isinstance(x, Num):
                        if is_dimensionless and x.unit:
                            raise ValueError(f"{func_name} requires a dimensionless Num (got {x.unit})")
                        z_val = mp_func(x.as_mpc)
                        res_unit = "" if is_dimensionless else x.unit
                        if func_name == "sqrt":
                            res_unit = f"sqrt({x.unit})" if x.unit else ""
                        if x.mytype != NumType.Unc:
                            return Num(z_val, unit=res_unit)
                        with workdps(mpmath.mp.dps + 4):
                            deriv = diff(mp_func, x.as_mpc)
                            sens = abs(deriv)
                            new_re_unc = sens * x.re_unc
                            new_im_unc = sens * x.im_unc
                        res = Num(z_val, unit=res_unit)
                        res.re_unc = new_re_unc
                        res.im_unc = new_im_unc
                        res.mytype = NumType.Unc
                        return res
                    # If it's not a Num, just use the raw mpmath function
                    return mp_func(x)
                return wrapped
            trig_funcs = ["cos", "sin", "tan", "acos", "asin", "atan", "exp", "log"]
            # 'abs' removed from here - let the built-in handle it
            misc_funcs = ["sqrt"] 
            for name in trig_funcs:
                setattr(target, name, create_wrapper(name, is_dimensionless=True))
            for name in misc_funcs:
                setattr(target, name, create_wrapper(name, is_dimensionless=False))
                
if 1:  # Functions
    def RegisterUnit(unit_name: str) -> None:
        '''Global helper for the Num class to ensure units are registered.'''
        UnitArbiter()._register_unit(unit_name)
    def e(n: "Num"):
        '''The "Editor" command. Spawns your $EDITOR with the Num's state.'''
        import tempfile, os, subprocess
        initial_text = f"Unit: {n.unit}\nValue: {n.real}\nDoc: {n.d}"
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+', delete=False) as tf:
            tf.write(initial_text)
            temp_path = tf.name
        # Fire up vi/vim/nano
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, temp_path])
        # ... logic to read the file back and update n.d ...
        print(f"Updated {n.unit} metadata.")

if 1:   # Global namespace function population
    # Trigonometric, Exponential, and Scaling
    for name in ["sin", "cos", "tan", "exp", "log", "log10", "asin", "acos", "atan",
                "asinh", "acosh", "atanh", "erf", "erfc", "gamma", "degrees", "radians"]:
        if hasattr(mpmath, name):
            globals()[name] = NoetherWrap(name, logic="dimensionless")
    # Conformable Pairs
    # Note: mpmath uses 'fmod' for remainder operations.
    for name in ["atan2", "fmod"]:
        if hasattr(mpmath, name):
            globals()[name] = NoetherWrap(name, logic="conformable")
    # Manually alias remainder to fmod if you want the same behavior,
    # or just use fmod directly.
    remainder = globals().get("fmod")
    # Special Cases
    sqrt = NoetherWrap("sqrt", logic="sqrt")
    ceil = NoetherWrap("ceil", logic="dimensionless")
    floor = NoetherWrap("floor", logic="dimensionless")
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

if 0:  # Temp experiment
    exit()

if 1:   # Self-tests
        def Test_Constructor_With_Numbers():
            zero = 0
            if 1:   # No input
                num = Num()
                Assert(num.real == 0 and num.imag == 0)
                Assert(num.mytype == NumType.Int)
            if 1:   # int
                if 1:   # Positive
                    x, T = 30957357, NumType.Int
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                if 1:   # Negative
                    x, T = -30957357, NumType.Int
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
            if 1:   # Rational
                x, T = "-3/8", NumType.Rat
                num = Num(x)
                Assert(num.numer == -3 and num.denom == 8)
                Assert(num.mytype == T)
                Assert(num == Num("-0.375"))
            if 1:   # float
                x, T = 3095.7357, NumType.Flt
                num = Num(x)
                Assert(num.real == x and num.imag == 0)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == 0)
                Assert(num.mytype == T)
            if 1:   # Decimal
                s = "3095.7357"
                x, T = decimal.Decimal(s), NumType.Flt
                num = Num(x)
                Assert(num.real == mpmath.mpf(s) and num.imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == zero)
                Assert(num.mytype == T)
            if 1:   # mpmath.mpf
                s, T = "3095.7357", NumType.Flt
                x = mpmath.mpf(s)
                num = Num(x)
                Assert(num.real == x and num.imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == zero)
                Assert(num.mytype == T)
            if 1:   # Complex
                x, T = -1+3j, NumType.Cpx
                num = Num(x)
                Assert(num.real == mpmath.mpf(-1) and num.imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == mpmath.mpf(1) and num.imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # mpmath.mpc
                x, T = mpmath.mpc(-1, 3), NumType.Cpx
                num = Num(x)
                Assert(num.real == mpmath.mpf(-1) and num.imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == mpmath.mpf(1) and num.imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # Rational
                pass
            if 1:   # Unc
                pass
        def Test_Constructor_Strings():
            zero = 0
            ndigits = min(max(1, 7*mpmath.mp.dps//8), mpmath.mp.dps)
            test_cases = [("1", NumType.Int),
                          ("1/2", NumType.Rat),
                          ("1.2", NumType.Flt),
                          ("1.2e3", NumType.Flt),
                          ("1+2j", NumType.Cpx)]
            for s, typ in test_cases:
                x = Num(s)
                Assert(x.mytype == typ, got=typ, expected=x.mytype)
                # Check numerical value
                if s == "1":
                    Assert(x.numer == 1 and x.denom == 1)
                elif s == "1/2":
                    Assert(x.numer == 1 and x.denom == 2)
                elif s == "1.2":
                    Assert(x.approx(Num("1-1/5"), ndigits))
                    Assert(x.imag == zero)
                elif s == "1.2e3":
                    Assert(x.approx(Num("1200/1"), ndigits))
                    Assert(x.imag == zero)
                elif s == "1+2j":
                    Assert(x.real == mpmath.mpf("1") and x.imag == mpmath.mpf("2"))
            # Test using a long string to show we aren't dropping back to standard 64
            # bit float precision
            with mpmath.extradps(20):
                sx = "1.123456789012345678901234567890"
                sy = "11.23456789012345678901234567890"
                x = mpmath.mpf(sx)
                y = mpmath.mpf(sy)
                result = x*y
                expected = mpmath.mpf("12.621551567779301945529644873425361979")
                Assert(result == expected)
                x = Num(sx + " m")
                y = Num(sy + " kg")
                result = x*y
                expected = Num("12.621551567779301945529644873425361979 (m)*(kg)")
                Assert(result == expected)
        def Test_Arithmetic():
            if 1:   # Test addition
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x + y
                    expected = "4.28083989501312"   # 15 digit GNU units answer
                    expected = "4.2808399000000001"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "ft") or
                           result == Num(expected, "foot"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x + y
                    if 0:   # This is old test when the result was a rational
                        # Mike and I agreed it doesn't really make sense to spend effort
                        # fixing this now.  Maybe later it will feel more important if a
                        # special use case needs it.
                        expected = Num("15/8", "in")
                    else:
                        expected = Num("1.875", "inch")
                    Assert(result == expected)
                    # See if an integer and fraction remain a fraction
                    x = Num("3/8")
                    y = Num("1")
                    result = x + y
                    expected = Num("11/8")
                    Assert(result == expected)
                    # Fraction and float should give a float
                    x = Num("3/8")
                    y = Num("1.0")
                    result = x + y
                    expected = Num("1.375") # Fractions that are powers of 2 are exact floats
                    Assert(result == expected)
            if 1:   # Test subtraction
                if 1:   # Integer & real
                    x = Num("1", "ft")
                    y = Num("1", "m")
                    result = x - y
                    expected = "-2.2808399000000001"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "foot"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x - y
                    #expected = Num("-9/8", "in")   # 3/8 - 12/8 = -9/8
                    expected = Num("-1.125 inch")
                    Assert(result == expected)
            if 1:   # Test multiplication
                if 1:   # Integer & real
                    x = Num("1.5", "V")
                    y = Num("2.0", "A")
                    result = x*y
                    expected = "3.0"
                    Assert(result.real == mpmath.mpf(expected))
                    #Assert(result == Num("3.0 kg*m^2/s^3"))  Old parse; new keeps V*A
                    Assert(result == Num("3.0 (V)*(A)"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x*y
                    expected = Num("9/16", "(in)*(in)")   # 3/8*12/8 = 36/64 = 9/16
                    #expected = Num("0.00036290249999999997 m^2")
                    Assert(result == expected)
            if 1:   # Test division
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x/y
                    #expected = Num("0.30480000000000002") Older conversion to float
                    expected = Num("1.0 (ft)/(m)")
                    Assert(result == expected)
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x/y
                    #expected = Num("0.25") Older conversion to float
                    expected = Num("1/4 (in)/(in)")
                    Assert(result == expected)
        def Test_Noether_Invariant():
            '''The .num component is used to normalize to a "unit vector" in the
            particular "unit" vector's direction.  This means that x/x.num returns a Num
            with unit numerical magnitude and the same units of x.  This is analogous to
            how you normalize in linear vector spaces:  a unit vector in the direction
            of v is v/|v|.
            
            I think it would be fitting to call this x/x.num the "Noether invariant";
            it's really the "unit vector" in the dimensional space described by the
            units.
            '''
            x = Num("1.23 A")
            Assert(x.real == mpmath.mpf("1.23"))
            Assert(x.unit == "A")
            y = x/x.num
            # Now y is in some sense a unit vector in the units space
            Assert(y == Num("1 A"))
            Assert(y.unit == x.unit)    # Make sure units didn't change
            Assert(x.num*y == x)        # Prove the Noether invariance
            # It has to work for complex too
            z = Num("1+2i m")
            y = z/z.num
            Assert(y.unit == z.unit)    # Make sure units didn't change
            Assert(z.num*y == z)        # Prove the Noether invariance
        def Test_Corners():
            N = Num
            if 1:   # 0 and 1
                # Addition
                Assert(N(0) + N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1) + N(1) == N("2+0i") == N("4/2"))
                Assert(N(-1) + N(-1) == N("-2+0i") == N("-4/2"))
                # Subtraction
                Assert(N(0) - N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1) - N(1) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(-1) - N(-1) == N("0+0i") == N("0/1") == N("0.-0.i"))
                # Multiplication
                Assert(N(0)*N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1)*N(1) == N("1+0i") == N("2/2"))
                # Division
                Assert(N(0)/N(1) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1)/N(1) == N("1+0i") == N("2/2"))
            if 1:   # With units
                # Real
                Assert(N("0 m") + N("0 m") == N("0 m"))
                Assert(N("0 m")*N("1 m") == N("0 m2"))
                #Assert(N("0 m")/N("1 m") == N("0"))
                Assert(N("0 m")/N("1 m") == N("0.0 (m)/(m)"))
                # Complex
                Assert(N("0+0j m") + N("0+0j m") == N("0+0j m"))
                Assert(N("0+0j m")*N("1+0j m") == N("0+0j m2"))
                Assert(N("0+0j m")/N("1+0j m") == N("0.0 (m)/(m)"))
                # Complex units corner case
                Assert(N("1+0i m") + N("1 m") == N("2+0j m"))
                Assert(N("1+0i m")*N("1 m") == N("1+0j m2"))
            if 1:   # Test core properties: as_mpf, etc.
                x = Num("10")
                Assert(isinstance(x.as_int_or_rat, int))
                Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("10"))
                Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("10", 0))
                x = Num("10/20")
                Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("1/2"))
                Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("1/2", 0))
                x = Num("10+20j")
                Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("10"))
                Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("10", "20"))
            if 1:   # "1+2i m" * "3/4 A":  hope we don't get mA
                a = N("1+2i m")
                b = N("3/4 A")
                Assert(a*b == N("0.75+1.5i m*A"))
            if 1:   # Division by zero
                with raises(ZeroDivisionError):
                    N("0")/N("0")
                with raises(ValueError):
                    N("0/0")
                with raises(ZeroDivisionError):
                    N("0.")/N("0.")
                with raises(ZeroDivisionError):
                    N("0+0i")/N("0+0i")
            if 1:   # Complex powers
                # First try no units; should maintain complex type
                x = N("1+1i")
                y = x**x
                Assert(y == N(mpmath.mpc(1, 1)**mpmath.mpc(1, 1)))
                # See that complex exponent gets exception on base with units
                a = N("1.2 m")
                with raises(TypeError):
                    y = a**x
            if 1:   # Unit with rational power (base unit must be a root)
                x = N("2 gallons")
                a = N("2/3")
                result = x**a
                Assert(result == Num("0.038556306368604 m^2"))
            if 1:   # In-place scaling    
                a = Num("1 m")
                a += Num("50 cm")
                Assert(a == Num("1.5 m"))
            if 1:   # Type closure
                x = Num(5)*Num(2)
                Assert(x == Num(10))
                x = Num("3/8")*Num("1/2")
                Assert(x == Num("3/16"))
                x = Num("0.375")*Num("0.5")
                Assert(x == Num("3/16") == Num("0.1875"))
            if 1:   # Downcasting
                x = Num("1+i")*Num("1-i")
                Assert(x == Num("2") and x.mytype == NumType.Flt)
                x = Num("3/2")*Num("2/3")
                Assert(x == Num("1") and x.mytype == NumType.Int)
            if 1:   # inf and nan
                x = Num("inf m")
                Assert(x.real == mpmath.mpf("inf") and x.unit == "m")
                x = Num("-inf m")
                Assert(x.real == mpmath.mpf("-inf") and x.unit == "m")
                x = Num("nan m")
                Assert(mpmath.isnan(x.real) and x.unit == "m")
                x = Num("0+nanj m")
                Assert(x.real == 0 and mpmath.isnan(x.imag) and x.unit == "m")
                x = Num("nan+nanj m")
                Assert(mpmath.isnan(x.real) and mpmath.isnan(x.imag) and x.unit == "m")
        def Test_New_Unit():
            return
            # I've shut this off, as it has been tested and works
            if 0:
                basename = "delete_me_"
                for i in range(8):
                    c = random.randint(97, 122)
                    basename += chr(c)
                x = Num("1 m")
                print(f"basename = {basename!r}")
                x.base(basename) # The Arbiter will turn this into "name\t!"
        def Test_Functions():
            if 1:   # Prove radians() and sin() are in the global namespace
                x = Num(radians(30))
                Assert(sin(x).approx(0.5, 10))
            #yy
        def Test_Uncertainty():
            '''This output came from the _unc.py script, which uses the python
            uncertainties library to calculate the results.  I consider it a gold
            standard whose results we must reproduce.
            
            Introduction
              This simulates a measurement made in the yard with a Starrett fiberglass
              200 foot tape measure.  The tape measure is graduated in units of 0.01 ft.
              I have no standard or calibration to know the uncertainty, so I'm forced
              to estimate a type B uncertainty.  Much of the measurement uncertainty
              won't come from the uncertainty in the tape measure itself, it will come
              from going over the bumpy lawn and having to be pulled on to get things
              straighter (tape stretch and small cumulative cosine errors).  I'll
              estimate the uncertainty at 0.1 ft, which means the standard deviation is
              about 1.2 inches.  If you regard a measurement as "nearly certain" if it's
              within 3 standard deviations, then that means we regard each measurement
              as "known" within about ±3.5 inches as a near certainty.  For a 50 to 100
              ft typical measurement in the yard, that doesn't sound too optimistic or
              pessimistic.
            
            Basic arithmetic:
              x1 = 100.00(10)
              x2 = 150.00(10)
              x1 + x2 = 250.00(14)
              x1 - x2 = -50.00(14)
              x1*x2 = 15000(18)
              x1/x2 = 0.66667(80)
            Problematic:
              sqrt(ufloat(0, 1)) = 0.0+/-nan
              ufloat(0, 1)/ufloat(0.0001, 1) = (0.0+/-1.0)e+04
            Trig:
              Using the cosine law and lengths x1 = 100.00+/-0.10 and x2 = 150.00+/-0.10,
              calculate the third edge of a triangle if the angle between the two lengths is 
              60(2) degrees, measured with a small compass.  The formula is
                  y² = x1² + x2² - 2*x1*x2*cos(angle)
              where angle = 60.0+/-2.0°.  The task is to convert the angle to radians, then
              peform the calculation.  The terms are
                  x1² = 10000+/-20
                  x2² = 22500+/-30
                  2*x1*x2 = (3.000+/-0.004)e+04
                  cos(radians(angle)) = 0.500+/-0.030
              Putting the pieces together, the result is
                  y = 132.3+/-3.4
              Note:  a calculator gives 132.388.

            Num constructor guts:
                self.numer: int = 0
                self.denom: int = 1
                self.real: mpmath.mpf = mpmath.mpf("0")
                self.imag: mpmath.mpf = mpmath.mpf("0")
                self.re_unc: mpmath.mpf = mpmath.mpf("0")
                self.im_unc: mpmath.mpf = mpmath.mpf("0")
                self.correl: mpmath.mpf = mpmath.mpf("0")
                self._unit = ""
                self.mytype: NumType = NumType.Int
            '''
            mpf, mpc = mpmath.mpf, mpmath.mpc
            indent = " "*4
            x1 = Num("100 ft")
            x2 = Num("150 ft")
            # Manually convert to Unc instances
            x1.re_unc = mpf("0.1")
            x2.re_unc = x1.re_unc
            x1.mytype = NumType.Unc
            x2.mytype = NumType.Unc
            if 1:   # Addition
                result = x1 + x2
                if 0:   # Dump values for debugging
                    print("x1 dump")
                    x1.dump(indent)
                    print("\nx2 dump")
                    x2.dump(indent)
                    print("\nresult dump")
                    result.dump(indent)
                Assert(result == Num("250 ft"))
                myresult = Num(str(result.re_unc))
                expected = mpf("0.1")*mpmath.sqrt(2)
                Assert(myresult.approx(expected, 14))
            if 1:   # Multiplication
                result = x1 * x2
                if 0:   # Dump values for debugging
                    print("x1 dump")
                    x1.dump(indent)
                    print("\nx2 dump")
                    x2.dump(indent)
                    print("\nresult dump")
                    result.dump(indent)
                Assert(result == Num("15000 ft2") == Num("15000 (ft)*(ft)"))
                myresult = Num(str(result.re_unc))
                expected = mpf("18")
                Assert(myresult.approx(expected, 2))
            if 1:   # Division
                result = x1 / x2
                if 0:   # Dump values for debugging
                    print("x1 dump")
                    x1.dump(indent)
                    print("\nx2 dump")
                    x2.dump(indent)
                    print("\nresult dump")
                    result.dump(indent)
                Assert(result.approx(2/3, 14))
                myresult = Num(str(result.re_unc))
                expected = mpf("0.00080")
                Assert(myresult.approx(expected, 2))
            if 1:   # Cosine law example
                theta = Num(radians(60))    # 60°±2° 
                theta.re_unc = radians(mpf(2))
                theta.mytype = NumType.Unc
                result = sqrt(x1*x1 + x2*x2 - 2*x1*x2*cos(theta))
                if 1:   # Dump
                    print("theta dump")
                    theta.dump(indent)  # 1.0472 radians
                    print("result dump")
                    result.dump(indent)


'''
Other tests needed:
    - '0 m' + '0 J' -> error
    - '1 m' + '1 J' -> error
    - '3 m' % '14 j' (error, units must be conformable)
    - General:  x ⚬ y OK if units are conformable, result gets units of 1st arg
    - inf and nan
        - '3 + nan i'?, should stay in ℂ?
    - Nails:  ϵ + i, 1 + ϵi
    - '1.23453094830853048309739047394739473947394739473947e4 m3' Does GNU units barf
      on this?  No, handles it fine; appears to handle unlimited digits.

1. The "Ghost of Precision Past"

    In Test_Constructor_Strings, you use:

    Assert(x.real == mpmath.mpf("1.2") and x.imag == zero)

        Critique: Since we are using mpmath for arbitrary precision, the test is
        currently at the mercy of whatever mp_context precision is set to at that
        moment.

        The dark corner: If the library ever changes mp.dps globally during a
        calculation, a direct == might fail due to trailing epsilon differences.

        Recommendation: Consider an AssertClose() or checking x.mytype first. You
        already do this, but adding a test case for a very long string—e.g.,
        Num("1.123456789012345678901234567890")—would verify that we aren't accidentally
        dropping back to standard 64-bit float precision during the parse.

2. The "Surgeon's Edge" (Complex Signs)

    Your regex pattern = r"(?<!e)(?=[+-])" is clever, but there are two "human" ways of
    writing complex numbers that might trip it up:

        Case A: Num("1-j") or Num("-j+1").

        Case B: Num("1+-2j") (ugly, but it happens in generated strings).

        Recommendation: Add a test case for Num("j") and Num("-j"). My current logic
        handles val in ("", "+", "-") by appending "1", but seeing those in the test
        suite ensures no future refactor breaks the "implicit one" rule.

3. The "Uncertainty Propagation" Gap

    I noticed NumType.Unc in the mapping, but I didn't see a string-based test for it.

        The dark corner: If a user passes Num("1.2+/-0.01"), the current _parse_string
        will likely throw a ValueError because it doesn't recognize the +/- symbol
        before hitting the mpmath block.

        Recommendation: If you intend for Num to be initialized from "uncertainty
        strings," that’s a gap. If not, a test case confirming that Num("1.2+/-0.01")
        fails predictably is just as valuable.

'''
if __name__ == "__main__":  
    if 1:   # Standard imports
        import getopt
    if 1:   # Custom imports
        pass
    if 1:   # Import symbols
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
    if 1:   # Utility stuff for a script
        def GetScreen():
            'Return (LINES, COLUMNS)'
            return (
                int(os.environ.get("LINES", "50")),
                int(os.environ.get("COLUMNS", "80")) - 1,
            )
        def GetColors():
            t.err = "redl"
        #def Warn(*msg, **kw):
        #    print(*msg, file=sys.stderr)
        #def Error(*msg, status=1):
        #    Warn(f"{t.err}", end="")
        #    Warn(*msg)
        #    Warn(f"{t.n}")
        #    exit(status)
        def Usage(status=1):
            print(wrap.dedent(f'''
            Usage:  {sys.argv[0]} [options] [arg1 [arg2...]]
            Describe behavior
            Options:
                -d      Turn on debug printing
                -n n    Set number of digits [15]
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-d"] = False     # Debug printing
            d["-n"] = 15        # Number of mpmath digits
            try:
                opts, args = getopt.getopt(sys.argv[1:], "dh")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("d"):
                    d[o] = not d[o]
                elif o == "-n":
                    try:
                        d[o] = int(a)
                        if d[o] < 1:
                            raise ValueError()
                    except Exception:
                        Error(f"{o!r} option must be an int >= 1")
                elif o == "-h":
                    Usage(status=0)
            GetColors()
            g.W, g.L = GetScreen()
            if d["-d"]:
                with g:
                    g.dbg = True
            return args
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    #if args:
    #    for arg in args:
    #        pass    # Do stuff
    exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])

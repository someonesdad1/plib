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
        import dataclasses
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
        g.dbg = True if 1 else False
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
        '''Operator overloading for the Num class.'''
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
            if self.unit and other.mytype == NumType.Cpx:
                raise TypeError(f"Cannot raise unit-bearing quantity ({self.unit}) to a complex power")
            res = self._binary_op(other, lambda a, b: a**b)
            if self.unit:
                try:
                    exp_f = float(other.as_mpf)
                    exp_str = str(int(exp_f)) if exp_f.is_integer() else str(exp_f)
                except:
                    exp_str = str(other.raw_value)
                raw_unit = f"({self.unit})^{exp_str}"
                new_val, simplified_unit = self.arb.simplify(res.raw_value, raw_unit)
                return Num(new_val, unit=simplified_unit)
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            from mpmath import workdps, diff, sqrt as mp_sqrt
            # Use mpc to ensure we have a common high-precision starting point
            z_val = op_func(self.as_mpc, other.as_mpc)
            with workdps(mpmath.mp.dps+4):
                # Calculate partial derivatives numerically
                df_dself = diff(lambda x: op_func(x, other.as_mpc), self.as_mpc)
                df_dother = diff(lambda y: op_func(self.as_mpc, y), other.as_mpc)
                s_sens = abs(df_dself)
                o_sens = abs(df_dother)
                # Gaussian error propagation
                new_re_unc = mp_sqrt((s_sens*self.re_unc)**2 + (o_sens*other.re_unc)**2)
                new_im_unc = mp_sqrt((s_sens*self.im_unc)**2 + (o_sens*other.im_unc)**2)
            # Use _make_result to handle nominal value storage/promotion correctly
            res = self._make_result(z_val, unit=self.unit)
            # Manually attach uncertainty now that nominal value is safely stored
            res.re_unc = new_re_unc
            res.im_unc = new_im_unc
            res.mytype = NumType.Unc
            return res
        def _check_ordering(self, other: ty.Any, op: str):
            '''Raise a clean TypeError if ordering is non-physical or ambiguous.'''
            # Promotion logic
            other_num = other if isinstance(other, Num) else Num(other)
            if self.mytype == NumType.Cpx or other_num.mytype == NumType.Cpx:
                raise TypeError(f"'{op}' not supported between complex numbers.")
            if self.mytype == NumType.Unc or other_num.mytype == NumType.Unc:
                raise TypeError(f"'{op}' not supported for numbers with uncertainty. "
                                f"Compare .raw_value if you want nominal ordering.")
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
            if self.unit != other.unit:
                try:
                    other = self._normalize(other, "cmp")
                except (ValueError, TypeError):
                    return False
            v1 = self.raw_value
            v2 = other.raw_value
            try:
                # First attempt: Force cast to current context for standard mpmath comparison
                if hasattr(v1, "real") or hasattr(v2, "real"):
                    res = mpmath.mpc(v1) == mpmath.mpc(v2)
                else:
                    res = mpmath.mpf(v1) == mpmath.mpf(v2)
                if res:
                    return True
                # Fallback: String-based comparison at current precision to catch "049" drift
                return str(v1) == str(v2)
            except:
                return v1 == v2
        def __abs__(self) -> "Num":
            return self._make_result(abs(self.raw_value), unit=self.unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self.unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other)+self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other)-self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other)*self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other)/self
if 1: # NumericMixin
    '''Manifest [17]: __add__ __sub__ __mul__ __truediv__ __pow__ _do_uncertainty_math _check_ordering __lt__ __le__ __gt__ __ge__ __eq__ __abs__ __neg__ __radd__ __rsub__ __rmul__ __rtruediv__'''
    class NumericMixin:
        '''Operator overloading for the Num class.'''
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
        def __pow__(self, other: ty.Any) -> "Num":  # OLD:  delete when new working
            if not isinstance(other, Num):
                other = Num(other)
            if self.unit and other.mytype == NumType.Cpx:
                raise TypeError(f"Cannot raise unit-bearing quantity ({self.unit}) to a complex power")
            res = self._binary_op(other, lambda a, b: a**b)
            if self.unit:
                try:
                    exp_f = float(other.as_mpf)
                    exp_str = str(int(exp_f)) if exp_f.is_integer() else str(exp_f)
                except:
                    exp_str = str(other.raw_value)
                raw_unit = f"({self.unit})^{exp_str}"
                new_val, simplified_unit = self.arb.simplify(res.raw_value, raw_unit)
                return Num(new_val, unit=simplified_unit)
            return res
        def __pow__(self, other: ty.Any) -> "Num":
            '''Exponentiation with safe unit propagation.'''
            if not isinstance(other, Num):
                other = Num(str(other))
            # Guardrail: Prevent unit-bearing quantities raised to complex powers
            if self.unit and other.mytype == NumType.Cpx:
                raise TypeError(f"Cannot raise unit-bearing quantity ({self.unit}) to a complex power")
            # Compute numerical result
            res = self._binary_op(other, lambda a, b: a**b)
            if self.unit:
                # Use rational-aware exponent string if the exponent is of type Rat
                if other.mytype == NumType.Rat:
                    exp_str = f"({other.numer}/{other.denom})"
                else:
                    try:
                        exp_f = float(other.as_mpf)
                        exp_str = str(int(exp_f)) if exp_f.is_integer() else str(exp_f)
                    except:
                        exp_str = str(other.raw_value)
                raw_unit = f"({self.unit})^{exp_str}"
                # Simplify via the co-process
                new_val, simplified_unit = self.arb.simplify(res.raw_value, raw_unit)
                # Maintain the object state consistent with the new numeric/unit result
                return Num(new_val, unit=simplified_unit)
            return res
        def _do_uncertainty_math(self, other: "Num", op_func: ty.Callable) -> "Num":
            from mpmath import workdps, diff, sqrt as mp_sqrt
            z_val = op_func(self.as_mpc, other.as_mpc)
            with workdps(mpmath.mp.dps+4):
                df_dself = diff(lambda x: op_func(x, other.as_mpc), self.as_mpc)
                df_dother = diff(lambda y: op_func(self.as_mpc, y), other.as_mpc)
                s_sens = abs(df_dself)
                o_sens = abs(df_dother)
                new_re_unc = mp_sqrt((s_sens*self.re_unc)**2 + (o_sens*other.re_unc)**2)
                new_im_unc = mp_sqrt((s_sens*self.im_unc)**2 + (o_sens*other.im_unc)**2)
            res = self._make_result(z_val, unit=self.unit)
            res.re_unc = new_re_unc
            res.im_unc = new_im_unc
            res.mytype = NumType.Unc
            return res
        def _check_ordering(self, other: ty.Any, op: str):
            other_num = other if isinstance(other, Num) else Num(other)
            if self.mytype == NumType.Cpx or other_num.mytype == NumType.Cpx:
                raise TypeError(f"'{op}' not supported between complex numbers.")
            if self.mytype == NumType.Unc or other_num.mytype == NumType.Unc:
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
            if self.unit != other.unit:
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
            return self._make_result(abs(self.raw_value), unit=self.unit)
        def __neg__(self) -> "Num":
            return self._make_result(-self.raw_value, unit=self.unit)
        def __radd__(self, other: ty.Any) -> "Num":
            return Num(other)+self
        def __rsub__(self, other: ty.Any) -> "Num":
            return Num(other)-self
        def __rmul__(self, other: ty.Any) -> "Num":
            return Num(other)*self
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other)/self

if 0:  # Num
    '''Manifest [23]: __init__ _promote _binary_op _make_result _normalize _parse_proper_fraction _parse_string _extract_unit base help _s _r __str__ __repr__ to approx dump unit raw_value as_mpc as_mpf as_int_or_rat num pi e'''
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
            # 1. Capture and consolidate units from string or argument
            if isinstance(value, str):
                val_str, found_unit = self._extract_unit(value)
                if found_unit:
                    unit = found_unit if not unit else f"({found_unit})*({unit})"
                value = val_str
            # 2. Base initialization
            self.numer: int = 0
            self.denom: int = 1
            self._real: mpmath.mpf = mpmath.mpf("0")
            self._imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self.mytype: NumType = NumType.Int
            if value is None:
                # Still apply the unit even if value is None
                if unit: self.unit = unit
                return
            # 3. Type-specific parsing
            if isinstance(value, Num):
                self.numer, self.denom = value.numer, value.denom
                self._real, self._imag = value._real, value._imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                # Respect passed unit over the source Num unit if provided
                unit = unit if unit else value.unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self.numer = value
                self.mytype = NumType.Int
            elif isinstance(value, fractions.Fraction):
                self.numer, self.denom = value.numerator, value.denominator
                self.mytype = NumType.Rat
            elif isinstance(value, (float, decimal.Decimal)):
                self._real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self._real = mpmath.mpf(str(value.real))
                self._imag = mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif hasattr(value, "_mpf_") or isinstance(value, mpmath.mpf):
                self._real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self._real, self._imag = value.real, value.imag
                self.mytype = NumType.Cpx
            elif isinstance(value, uncertainties.UFloat):
                self._real = mpmath.mpf(str(value.nominal_value))
                self.re_unc = mpmath.mpf(str(value.std_dev))
                self.mytype = NumType.Unc
            elif isinstance(value, str):
                self._parse_string(value.strip())
            else:
                raise TypeError(f"Type of {value!r} is not supported")
            # 4. Final Unit Assertion
            # This ensures that even if _parse_string wiped _unit, we restore it.
            if unit:
                self.unit = unit
        def _promote(self) -> "Num":
            if self.mytype == NumType.Rat:
                f = fractions.Fraction(self.numer, self.denom)
                self.numer, self.denom = f.numerator, f.denominator
                if self.denom == 1:
                    self.mytype = NumType.Int
            elif self.mytype == NumType.Cpx:
                if self._imag == 0:
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
            a_val = self._real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other._real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return self._make_result(raw_val, unit=res_unit)
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit=unit)._promote()
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            if self.unit == other.unit:
                return other
            if operation in ("mul", "div"):
                return other
            # Check for unit compatibility
            is_ok, factor_str = self.arb.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            # Apply factor first to a float-storage variable
            new_real = adjusted.as_mpf * factor
            new_imag = adjusted._imag * factor if adjusted.mytype == NumType.Cpx else mpmath.mpf("0")
            # Now set the type and values manually to bypass migration logic
            adjusted._real = new_real
            adjusted._imag = new_imag
            adjusted._mytype = NumType.Flt if adjusted.mytype.value < NumType.Flt.value else adjusted.mytype
            if adjusted.mytype == NumType.Unc:
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
            raw = value.strip().replace(" ", "").lower()
            if not raw:
                raise ValueError("Empty string provided to Num")
            if raw in ("inf", "-inf", "nan"):
                self._real = mpmath.mpf(raw)
                self.mytype = NumType.Flt
                return
            if re.fullmatch(r"[+-]?\d+", raw):
                self.numer = int(raw)
                self.mytype = NumType.Int
                return
            if ("/" in raw and "-" in raw and raw[0] != "-"):
                self._real = self._parse_proper_fraction(value)
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
                        self._imag = mpmath.mpf(val)
                        self.mytype = NumType.Cpx
                    else:
                        self._real = mpmath.mpf(p.replace("+", ""))
                        self.mytype = NumType.Flt
                elif len(parts) == 2:
                    re_p, im_p = parts
                    if not im_p.endswith("j"):
                        self._real = mpmath.mpf(norm.replace("+", ""))
                        self.mytype = NumType.Flt
                    else:
                        self._real = mpmath.mpf(re_p.replace("+", ""))
                        val = im_p[:-1].replace("+", "")
                        if val in ("", "-"):
                            val += "1"
                        self._imag = mpmath.mpf(val)
                        self.mytype = NumType.Cpx
                else:
                    self._real = mpmath.mpf(norm.replace("+", ""))
                    self.mytype = NumType.Flt
            except:
                raise ValueError(f"Could not parse numeric part: {value}")
        def _parse_string(self, s: str) -> None:
            '''Logic to decompose strings into numeric components.'''
            s = s.strip()
            if not s: return

            # 1. Handle uncertainty like 1.23(45)
            if "(" in s:
                idx = s.find("(")
                if idx > 0 and s[idx-1].isdigit():
                    try:
                        main_part = s[:idx]
                        unc_part = s[idx+1:].rstrip(")")
                        self._real = mpmath.mpf(main_part)
                        dec_idx = main_part.find(".")
                        prec = len(main_part) - dec_idx - 1 if dec_idx != -1 else 0
                        self.re_unc = mpmath.mpf(unc_part) * mpmath.power(10, -prec)
                        self.mytype = NumType.Unc
                        return
                    except:
                        pass

            # 2. Handle Complex
            if "j" in s.lower() or "i" in s.lower():
                try:
                    # mpc parser is robust for 1+2j, 1j, etc.
                    val = mpmath.mpc(s.lower().replace("i", "j").replace(" ", ""))
                    self._real, self._imag = val.real, val.imag
                    self.mytype = NumType.Cpx
                    return
                except:
                    pass

            # 3. Handle Rationals
            if "/" in s:
                try:
                    f = fractions.Fraction(s)
                    self.numer, self.denom = f.numerator, f.denominator
                    self.mytype = NumType.Rat
                    return
                except:
                    pass

            # 4. Handle Integers
            try:
                # Only accept as Int if the string is purely numeric
                # (prevents scientific notation like 1e3 from being truncated here)
                if s.isdigit() or (s.startswith('-') and s[1:].isdigit()):
                    self.numer = int(s)
                    self.mytype = NumType.Int
                    return
            except ValueError:
                pass

            # 5. Default to Float
            try:
                self._real = mpmath.mpf(s)
                self.mytype = NumType.Flt
                return
            except ValueError:
                pass

            # 6. Naked unit string case (e.g. Num("ft"))
            # Only hit this if it failed every numeric parser above
            self.numer = 1
            self.denom = 1
            self.mytype = NumType.Int
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
                s = f"{self._real} +/- {self.re_unc}"
            else:
                s = self.fmt(self._real)
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
                s = str(self._real)
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
            res._real = res.as_mpf*factor
            res.mytype = NumType.Flt
            res._unit = unit
            return res._promote() if auto_promote else res
        def approx(self, y: ty.Union["Num", float, int, mpmath.mpf, mpmath.mpc], ndigits: int) -> bool:
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
            print(f"{indent}Num({id(self)}) core attributes:")
            print(f"{indent}    self.numer    {self.numer}")
            print(f"{indent}    self.denom    {self.denom}")
            print(f"{indent}    self._real    {self._real}")
            print(f"{indent}    self._imag    {self._imag}")
            print(f"{indent}    self.re_unc   {self.re_unc}")
            print(f"{indent}    self.im_unc   {self.im_unc}")
            print(f"{indent}    self.correl   {self.correl}")
            print(f"{indent}    self.unit     {self.unit!r}")
            print(f"{indent}    self.mytype   {self.mytype}")
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
        def raw_value(self) -> ty.Union[int, fractions.Fraction, mpmath.mpf, mpmath.mpc]:
            '''Return the underlying numerical value for mixin/unit operations.'''
            if self.mytype == NumType.Int:
                return self.numer
            if self.mytype == NumType.Rat:
                return fractions.Fraction(self.numer, self.denom)
            if self.mytype in (NumType.Cpx, NumType.Unc):
                return self.as_mpc
            return self._real
        @property
        def as_mpc(self) -> mpmath.mpc:
            '''Return the nominal value as a complex mpmath number.'''
            if self.mytype in (NumType.Cpx, NumType.Unc):
                return mpmath.mpc(self._real, self._imag)
            return mpmath.mpc(self.as_mpf, 0)
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.numer != 0:
                return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self._real
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
        @property
        def pi(self) -> "Num":
            return Num(+mpmath.pi)
        @property
        def e(self) -> "Num":
            return Num(+mpmath.e)
        @property
        def real(self) -> "Num":
            '''Returns the real component as a new Num instance with units.'''
            return Num(self.as_mpc.real, unit=self.unit)
        @property
        def imag(self) -> "Num":
            '''Returns the imaginary component as a new Num instance with units.'''
            return Num(self.as_mpc.imag, unit=self.unit)
        @property
        def unc(self) -> "Num":
            '''Returns the real uncertainty component as a new Num instance with units.'''
            return Num(self.re_unc, unit=self.unit)
        @property
        def mytype(self) -> NumType:
            return self._mytype
        @mytype.setter
        def mytype(self, new_type: NumType) -> None:
            if hasattr(self, "_mytype") and self._mytype == new_type:
                return
            old_type = getattr(self, "_mytype", None)
            # --- PRE-CAST DATA MIGRATION ---
            # Fix: Only migrate if the target field is currently zero/default
            if old_type in (NumType.Int, NumType.Rat) and new_type.value >= NumType.Flt.value:
                if self._real == 0:  # Only migrate if we haven't manually set _real yet
                    self._real = self.as_mpf
                    self._imag = mpmath.mpf("0")
            # --- CASTING LOGIC ---
            if old_type is not None and new_type.value < old_type.value:
                # Downcasting: Apply lossy transformations
                if new_type == NumType.Flt:
                    self._real = abs(self.as_mpc)
                    self._imag = mpmath.mpf("0")
                elif new_type == NumType.Rat:
                    from fractions import Fraction
                    f = Fraction(float(self.as_mpf)).limit_denominator()
                    self.numer, self.denom = f.numerator, f.denominator
                elif new_type == NumType.Int:
                    self.numer = int(abs(self.as_mpf))
                    self.denom = 1
                # Purge Ghost Data
                if new_type.value < NumType.Unc.value:
                    self.re_unc = self.im_unc = self.correl = mpmath.mpf("0")
            self._mytype = new_type
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
        }
        flip = False
        show_color = True
        active_system = "default"
        Fmt = fmt.Fmt()
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            self._doc = ""
            self.arb = UnitArbiter()
            self.fmt = Num.Fmt
            self.numer: int = 0
            self.denom: int = 1
            self._real: mpmath.mpf = mpmath.mpf("0")
            self._imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self._mytype: NumType = NumType.Int
            if value is None:
                if unit:
                    self.unit = unit
                return
            if isinstance(value, str):
                payload = StringParser.parse(value, unit)
                self.numer, self.denom = payload.numer, payload.denom
                self._real, self._imag = payload.real, payload.imag
                self.re_unc, self.im_unc = payload.re_unc, payload.im_unc
                self._unit = payload.unit
                self.mytype = payload.type
            elif isinstance(value, Num):
                self.numer, self.denom = value.numer, value.denom
                self._real, self._imag = value._real, value._imag
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
                self.unit = unit
        def _promote(self) -> "Num":
            if self.mytype == NumType.Rat:
                f = fractions.Fraction(self.numer, self.denom)
                self.numer, self.denom = f.numerator, f.denominator
                if self.denom == 1:
                    self.mytype = NumType.Int
            elif self.mytype == NumType.Cpx:
                if self._imag == 0:
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
            a_val = self._real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other._real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return self._make_result(raw_val, unit=res_unit)
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit=unit)._promote()
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            if self.unit == other.unit or operation in ("mul", "div"):
                return other
            is_ok, factor_str = self.arb.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            new_real = adjusted.as_mpf*factor
            new_imag = adjusted._imag*factor if adjusted.mytype == NumType.Cpx else mpmath.mpf("0")
            adjusted._real, adjusted._imag = new_real, new_imag
            adjusted.mytype = NumType.Flt if adjusted.mytype.value < NumType.Flt.value else adjusted.mytype
            if adjusted.mytype == NumType.Unc:
                adjusted.re_unc *= factor
                adjusted.im_unc *= factor
            adjusted._unit = self.unit
            return adjusted
        def base(self, unit: str = "") -> None:
            target = unit if unit else self.unit
            if target:
                print(self.arb._register_unit(target))
        def help(self, topic: str = "") -> None:
            h = Help()
            h(topic) if topic else h()
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = self.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                s = self.fmt(self.as_mpc)
            elif self.mytype == NumType.Unc:
                s = f"{self._real} +/- {self.re_unc}"
            else:
                s = self.fmt(self._real)
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
                s = str(self._real)
            if self.unit:
                s += f" {self.unit}"
            return f"Num('{s}')"
        def __str__(self) -> str:
            return self._r() if Num.flip else self._s()
        def __repr__(self) -> str:
            return self._s() if Num.flip else self._r()
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not unit or unit == self.unit:
                return Num(self)
            is_ok, factor_str = self.arb.check_conformable(self.unit, unit)
            if not is_ok:
                self.arb._register_unit(unit)
                is_ok, factor_str = self.arb.check_conformable(self.unit, unit)
                if not is_ok:
                    raise ValueError(f"Incompatible: {self.unit} -> {unit}")
            res = Num(self)
            res._real = res.as_mpf*mpmath.mpf(factor_str)
            res.mytype = NumType.Flt
            res.unit = unit
            return res._promote() if auto_promote else res
        def approx(self, y: ty.Any, ndigits: int) -> bool:
            if not isinstance(y, Num):
                y = Num(y)
            vx, vy = self.as_mpf, y.as_mpf
            if vy == 0:
                return abs(vx) < 10**(-ndigits)
            val = abs((vx-vy)/vy)
            return True if val == 0 else int(abs(mpmath.log10(val))) >= ndigits
        def dump(self, indent: str = "") -> None:
            print(f"{indent}Num({id(self)}) type: {self.mytype.name}")
            print(f"{indent}  val: {self.raw_value} | unit: {self.unit!r}")
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @unit.setter
        def unit(self, value: str) -> None:
            if value:
                self.arb._register_unit(value)
                self._unit = value.strip()
            else:
                self._unit = ""
        @property
        def raw_value(self) -> ty.Any:
            if self.mytype == NumType.Int:
                return self.numer
            if self.mytype == NumType.Rat:
                return fractions.Fraction(self.numer, self.denom)
            return self.as_mpc if self.mytype in (NumType.Cpx, NumType.Unc) else self._real
        @property
        def as_mpc(self) -> mpmath.mpc:
            return mpmath.mpc(self._real, self._imag) if self.mytype in (NumType.Cpx, NumType.Unc) else mpmath.mpc(self.as_mpf, 0)
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.numer != 0:
                return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self._real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            return self.numer if self.mytype == NumType.Int else fractions.Fraction(self.numer, self.denom)
        @property
        def num(self) -> "Num":
            res = Num(self)
            res.unit = ""
            return res
        @property
        def pi(self) -> "Num":
            return Num(+mpmath.pi)
        @property
        def e(self) -> "Num":
            return Num(+mpmath.e)
        @property
        def mytype(self) -> NumType:
            return self._mytype
        @mytype.setter
        def mytype(self, new_type: NumType) -> None:
            if hasattr(self, "_mytype") and self._mytype == new_type:
                return
            old_type = getattr(self, "_mytype", None)
            if old_type in (NumType.Int, NumType.Rat) and new_type.value >= NumType.Flt.value:
                if self._real == 0:
                    self._real = self.as_mpf
            if old_type is not None and new_type.value < old_type.value:
                if new_type == NumType.Flt:
                    self._real, self._imag = abs(self.as_mpc), mpmath.mpf("0")
                elif new_type == NumType.Rat:
                    f = fractions.Fraction(float(self.as_mpf)).limit_denominator()
                    self.numer, self.denom = f.numerator, f.denominator
                elif new_type == NumType.Int:
                    self.numer, self.denom = int(abs(self.as_mpf)), 1
                if new_type.value < NumType.Unc.value:
                    self.re_unc = self.im_unc = self.correl = mpmath.mpf("0")
            self._mytype = new_type

if 0:  # UnitArbiter
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
            self.inject_math()
        def _start_process(self) -> None:
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
            superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            exp_map = str.maketrans(superscripts, "0123456789")
            out = ""
            for char in s:
                if char in superscripts:
                    out += "^"+char.translate(exp_map)
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
            proc = subprocess.run(cmd+[self._translate_unicode(unit_str)], capture_output=True, text=True)
            output = proc.stdout.strip()
            match = re.match(r'^([\d.e+-]+)?\s*(.*)$', output)
            factor_raw = match.group(1) or "1.0" if match else "1.0"
            factor = +mpmath.mpf(factor_raw)
            res_val = +(value*factor)
            remainder = match.group(2).strip() if match else unit_str
            if "=" in remainder:
                remainder = remainder.split("=")[0].strip()
            return res_val, remainder
        def is_known_unit(self, unit_str: str) -> bool:
            if not unit_str:
                return True
            cmd = [self.bin_path, "-q", "-t", "--compact", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            res = subprocess.run(cmd+[self._translate_unicode(unit_str)], capture_output=True, text=True)
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
                tmp.write(definition+"\n")
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
            '''Inject uncertainty-aware math wrappers into __main__ namespace.'''
            import sys
            import mpmath
            from mpmath import workdps, diff, mp
            target = sys.modules['__main__']
            def create_wrapper(func_name: str, is_dimensionless: bool = True):
                mp_func = getattr(mpmath, func_name)
                def wrapped(x: ty.Any) -> "Num":
                    if isinstance(x, Num):
                        if is_dimensionless and x.unit:
                            raise ValueError(f"{func_name} requires a dimensionless Num (got {x.unit})")
                        z_val = mp_func(x.as_mpc)
                        res_unit = "" if is_dimensionless else x.unit
                        if func_name == "sqrt":
                            res_unit = f"sqrt({x.unit})" if x.unit else ""
                        if func_name == "degrees":
                            res_unit = "deg"
                        if func_name == "radians":
                            res_unit = "rad"
                        if x.mytype != NumType.Unc:
                            return Num(z_val, unit=res_unit)
                        with workdps(mp.dps + 4):
                            # Icelandic Heuristic: Two-step convergence check
                            h_base = mp.power(10, -(mp.dps // 2))
                            d1 = diff(mp_func, x.as_mpc, h=h_base)
                            d2 = diff(mp_func, x.as_mpc, h=h_base / 2)
                            sens = abs(d1)
                            sens2 = abs(d2)
                            # Check for divergence (Ratio > 1% difference)
                            if abs(sens - sens2) / (sens + 1e-30) > 0.01:
                                print(f"Warning: Possible singularity suspected in "
                                      f"{func_name} at {x.raw_value}.\n"
                                      f"Uncertainty propagation may be non-physical.", file=sys.stderr)
                            new_re_unc = sens * x.re_unc
                            new_im_unc = sens * x.im_unc
                        res = Num(z_val, unit=res_unit)
                        res.re_unc = new_re_unc
                        res.im_unc = new_im_unc
                        res.mytype = NumType.Unc
                        return res
                    return mp_func(x)
                return wrapped
            trig_funcs = ["cos", "sin", "tan", "acos", "asin", "atan", "exp", "log"]
            misc_funcs = ["sqrt", "degrees", "radians"]
            for name in trig_funcs:
                setattr(target, name, create_wrapper(name, is_dimensionless=True))
            for name in misc_funcs:
                setattr(target, name, create_wrapper(name, is_dimensionless=False))
if 1: # UnitArbiter
    '''Manifest [11]: __new__ __init__ _start_process _translate_unicode check_conformable simplify is_known_unit add_base _check_definition _register_unit inject_math'''
    class UnitArbiter:
        '''
        Singleton co-process manager for GNU Units and Math Orchestration.
        Handles unit conversion and injects uncertainty-aware math wrappers.
        '''
        _instance = None
        units_bin: str = "units"
        main_config: str = os.path.expanduser("~/.noether_units.dat")
        dynamic_config: str = os.path.expanduser("~/.units_dynamic")
        def __new__(cls) -> "UnitArbiter":
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
            return cls._instance
        def __init__(self) -> None:
            if not hasattr(self, "proc"):
                self.proc = None
                self._start_process()
                # self.inject_math() # Re-enable when math hooks are ready
        def _start_process(self) -> None:
            '''Launch GNU Units as a persistent co-process with high precision.'''
            if self.proc:
                try:
                    self.proc.terminate()
                    self.proc.wait(timeout=0.2)
                except:
                    pass
            # Using -d 15 for enhanced precision during number.py development
            cmd = [self.units_bin, "-q", "--compact", "-t", "-d", "15"]
            if os.path.exists(self.main_config):
                cmd.extend(["-f", self.main_config])
            if not os.path.exists(self.dynamic_config):
                with open(self.dynamic_config, "w") as f: f.write("")
            cmd.extend(["-f", self.dynamic_config])
            if g.dbg:
                print(f"DEBUG Units _start_process command:\n  {' '.join(cmd)}")
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def _translate_unicode(self, s: str) -> str:
            '''Convert superscript/Unicode math to ASCII for GNU Units.'''
            trans = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")
            for sup, normal in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"):
                s = s.replace(sup, f"^{normal}")
            return s.translate(trans).replace("·", "*")
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            '''Checks if two unit strings are compatible and returns the factor.'''
            if not self.proc or self.proc.poll() is not None:
                self._start_process()

            have = self._translate_unicode(have)
            want = self._translate_unicode(want)

            # Restoring the proven Have [NL] Want [NL] sequence
            query = f"{have}\n{want}\n"
            if g.dbg:
                print(f"DEBUG Units SENT:\n  Have: {have}\n  Want: {want}")

            try:
                self.proc.stdin.write(query)
                self.proc.stdin.flush()

                # GNU Units with --compact -t returns the factor immediately
                output = self.proc.stdout.readline().strip()

                if g.dbg:
                    print(f"DEBUG Units RECEIVED: {output}")

                if not output or "conformability error" in output or "error" in output.lower():
                    # If it's a conformability error, it usually spits out two lines
                    # of base units. We should clear the pipe.
                    return False, output

                return True, output
            except Exception as e:
                if g.dbg:
                    print(f"DEBUG Units EXCEPTION: {e}")
                return False, str(e)
        def simplify(self, value: ty.Any, unit_str: str) -> ty.Tuple[ty.Any, str]:
            '''
            Reduces the unit expression. We multiply the local magnitude
            by the conversion factor returned by GNU units.
            '''
            # Send ONLY the unit string to units.
            # As you found, (gallons)^(2/3) -> 0.02428... m^2
            query = f"{unit_str}\n\n"
            self.proc.stdin.write(query)
            self.proc.stdin.flush()
            # Read the response (e.g., "0.0242889506882033 m^2")
            res = self.proc.stdout.readline().strip()
            # Parse the response: [factor] [unit]
            # Example: factor=0.024288, unit=m^2
            parts = res.split(" ", 1)
            conv_factor = mpmath.mpf(parts[0])
            new_unit = parts[1]
            # Multiply the magnitude we already calculated by the conversion factor
            # This gives 1.5874... * 0.024288... = 0.038556...
            final_value = mpmath.mpf(value) * conv_factor
            return final_value, new_unit
        def is_known_unit(self, unit_str: str) -> bool:
            '''Query if a unit exists in the current database.'''
            self.proc.stdin.write(f"{unit_str}\n")
            self.proc.stdin.flush()
            line = self.proc.stdout.readline()
            return "unknown unit" not in line.lower()
        def add_base(self, unit_name: str) -> None:
            '''Append a new base unit to the dynamic configuration.'''
            with open(self.dynamic_config, "a") as f:
                f.write(f"{unit_name}\t\t!base!\n")
            self._start_process()
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
            '''Validate unit definition before registering.'''
            return True, ""
        def _register_unit(self, unit_name: str) -> str:
            return unit_name
        def inject_math(self) -> None:
            '''Wraps mpmath functions to handle uncertainty and units.'''
            pass

if 0: # StringParser Infrastructure
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
        unit: str = ""

    class StringParser:
        '''Engine to dichotomize numeric strings and units with recursive precision.'''
        @staticmethod
        def parse(s: str, passed_unit: str = "") -> ParsedPayload:
            s = s.strip()
            if not s:
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), unit=passed_unit)
            num_part, found_unit = StringParser._extract_unit(s)
            final_unit = (found_unit if not passed_unit
                          else f"({found_unit})*({passed_unit})").strip()
            if StringParser._is_pure_unit(num_part):
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=1, unit=s)
            # Tier A: Complex Uncertainty (Top-Level Parentheses Split)
            if "(" in num_part and ("j" in num_part.lower() or "i" in num_part.lower()):
                clean = num_part.lower().replace("i", "j")
                hinge_idx = -1
                paren_depth = 0
                for i, char in enumerate(clean):
                    if char == '(':
                        paren_depth += 1
                    elif char == ')':
                        paren_depth -= 1
                    elif char in ('+', '-') and paren_depth == 0 and i > 0:
                        hinge_idx = i
                if hinge_idx != -1:
                    re_s, sign = clean[:hinge_idx].strip(), clean[hinge_idx]
                    im_s = clean[hinge_idx+1:].strip().replace("j", "")
                    re_p = StringParser.parse(re_s)
                    im_p = StringParser.parse(im_s)
                    return ParsedPayload(NumType.Unc, re_p.real,
                                         imag=(im_p.real if sign == "+" else -im_p.real),
                                         re_unc=re_p.re_unc, im_unc=im_p.re_unc,
                                         unit=final_unit)
            # Tier B: Standard Uncertainty 1.23(45)
            if "(" in num_part and not num_part.startswith("("):
                idx = num_part.find("(")
                if idx > 0 and num_part[idx-1].isdigit():
                    try:
                        main_s, unc_s = num_part[:idx], num_part[idx+1:].rstrip(")")
                        real_val = mpmath.mpf(main_s)
                        dec_idx = main_s.find(".")
                        prec = len(main_s) - dec_idx - 1 if dec_idx != -1 else 0
                        re_unc = mpmath.mpf(unc_s)*mpmath.power(10, -prec)
                        return ParsedPayload(NumType.Unc, real_val, re_unc=re_unc, unit=final_unit)
                    except:
                        pass
            # Tier C: Complex (Standard mpc split)
            clean_num = num_part.lower().replace("i", "j").replace(" ", "")
            if "j" in clean_num:
                try:
                    match = re.match(r'^(.*?)([+-])?([^+-]*j)$', clean_num)
                    if match:
                        r_s, sign, i_s = match.groups()
                        i_s = i_s.replace('j', '')
                        if not i_s:
                            i_s = "1"
                        if sign == "-":
                            i_s = "-" + i_s
                        return ParsedPayload(NumType.Cpx, mpmath.mpf(r_s or "0"),
                                             imag=mpmath.mpf(i_s), unit=final_unit)
                except:
                    pass
            # Tier D: Rational
            if "/" in num_part:
                try:
                    f = fractions.Fraction(num_part)
                    # Check for explicit division by zero
                    if f.denominator == 0:
                        raise ValueError("Division by zero")
                    return ParsedPayload(NumType.Rat, mpmath.mpf("0"),
                                         numer=f.numerator, denom=f.denominator, unit=final_unit)
                except (ZeroDivisionError, ValueError):
                    # Re-raise to ensure tests expecting ValueError catch it
                    raise ValueError("Invalid rational: " + num_part)
            # Tier E: Integer/Float
            if re.fullmatch(r"[-+]?\d+", num_part):
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=int(num_part), unit=final_unit)
            try:
                return ParsedPayload(NumType.Flt, mpmath.mpf(num_part), unit=final_unit)
            except:
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=1, unit=s)
        @staticmethod
        def _extract_unit(s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s:
                if any(c.isdigit() for c in s) or any(c.lower() in 'ji' for c in s):
                    return s, ""
                return "1", s
            parts = s.rsplit(" ", 1)
            left, right = parts[0].strip(), parts[1].strip()
            if re.match(r'^[a-zA-Z(]', right) and right.lower() not in ('i', 'j'):
                if not (right.lower().startswith('e') and any(c.isdigit() for c in right)):
                    return left, right
            return s, ""
        @staticmethod
        def _is_pure_unit(s: str) -> bool:
            return not any(c.isdigit() for c in s) and not any(c.lower() in 'ij' for c in s)
if 1: # StringParser Infrastructure
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
        unit: str = ""
    class StringParser:
        '''Engine to dichotomize numeric strings and units with recursive precision.'''

        @staticmethod
        def flexible_mpc(s: str) -> mpmath.mpc:
            """Parses a string allowing i, j, I, J as imaginary units."""
            clean_s = re.sub(r'(?<![a-z])[ij](?![a-z])', 'j', s, flags=re.IGNORECASE)
            return mpmath.mpc(clean_s)

        @staticmethod
        def parse(s: str, passed_unit: str = "") -> ParsedPayload:
            s = s.strip()
            if not s:
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), unit=passed_unit)

            # 1. THE HARD GUARD: If it looks complex, it CANNOT be a unit.
            # This regex captures "1+2j", "1-2j", "2j", "1j"
            if re.search(r'\d+[+-]?\d*[ij]', s, flags=re.IGNORECASE):
                try:
                    val = StringParser.flexible_mpc(s)
                    return ParsedPayload(NumType.Cpx, val.real, imag=val.imag, unit=passed_unit)
                except:
                    pass

            # 2. Extract unit
            num_part, found_unit = StringParser._extract_unit(s)

            # 3. DEBUGGER PROTECTION: If we found a unit but the input had NO space,
            # we are likely in a false-positive scenario.
            # If the original s was '1+2j' and we are here, something is wrong.

            final_unit = (found_unit if not passed_unit
                          else f"({found_unit})*({passed_unit})").strip()

            if StringParser._is_pure_unit(num_part):
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=1, unit=s)

            # 4. Tier 0: Special numeric values (inf, nan)
            lower_num = num_part.lower()
            if "nan" in lower_num or "inf" in lower_num:
                return ParsedPayload(NumType.Flt, mpmath.mpf(num_part), unit=final_unit)

            # 5. Tier A: Complex Uncertainty (Parentheses)
            if "(" in num_part and ("j" in num_part.lower() or "i" in num_part.lower()):
                clean = num_part.lower().replace("i", "j")
                hinge_idx = -1
                paren_depth = 0
                for i, char in enumerate(clean):
                    if char == '(': paren_depth += 1
                    elif char == ')': paren_depth -= 1
                    elif char in ('+', '-') and paren_depth == 0 and i > 0:
                        hinge_idx = i
                if hinge_idx != -1:
                    re_s, sign = clean[:hinge_idx].strip(), clean[hinge_idx]
                    im_s = clean[hinge_idx+1:].strip().replace("j", "")
                    re_p = StringParser.parse(re_s)
                    im_p = StringParser.parse(im_s)
                    return ParsedPayload(NumType.Unc, re_p.real,
                                         imag=(im_p.real if sign == "+" else -im_p.real),
                                         re_unc=re_p.re_unc, im_unc=im_p.re_unc, unit=final_unit)

            # 6. Tier B: Standard Uncertainty 1.23(45)
            if "(" in num_part and not num_part.startswith("("):
                idx = num_part.find("(")
                if idx > 0 and num_part[idx-1].isdigit():
                    try:
                        main_s, unc_s = num_part[:idx], num_part[idx+1:].rstrip(")")
                        real_val = mpmath.mpf(main_s)
                        dec_idx = main_s.find(".")
                        prec = len(main_s) - dec_idx - 1 if dec_idx != -1 else 0
                        re_unc = mpmath.mpf(unc_s)*mpmath.power(10, -prec)
                        return ParsedPayload(NumType.Unc, real_val, re_unc=re_unc, unit=final_unit)
                    except: pass

            # 7. Tier D: Rational
            if "/" in num_part:
                try:
                    f = fractions.Fraction(num_part)
                    if f.denominator == 0: raise ValueError("Division by zero")
                    return ParsedPayload(NumType.Rat, mpmath.mpf("0"),
                                         numer=f.numerator, denom=f.denominator, unit=final_unit)
                except (ZeroDivisionError, ValueError):
                    raise ValueError("Invalid rational: " + num_part)

            # 8. Tier E: Integer/Float
            if re.fullmatch(r"[-+]?\d+", num_part):
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=int(num_part), unit=final_unit)
            try:
                return ParsedPayload(NumType.Flt, mpmath.mpf(num_part), unit=final_unit)
            except:
                return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=1, unit=s)

        @staticmethod
        def _extract_unit(s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s:
                if any(c.isdigit() for c in s) or any(c.lower() in 'ji' for c in s) or "nan" in s.lower() or "inf" in s.lower():
                    return s, ""
                return "1", s
            parts = s.rsplit(" ", 1)
            left, right = parts[0].strip(), parts[1].strip()
            if re.match(r'^[a-zA-Z(]', right) and right.lower() not in ('i', 'j', 'nan', 'inf'):
                if not (right.lower().startswith('e') and any(c.isdigit() for c in right)):
                    return left, right
            return s, ""

        @staticmethod
        def _is_pure_unit(s: str) -> bool:
            return not any(c.isdigit() for c in s) and not any(c.lower() in 'ij' for c in s) and "nan" not in s.lower() and "inf" not in s.lower()

if 1:  # Functions
    def RegisterUnit(unit_name: str) -> None:
        '''Global helper for the Num class to ensure units are registered.'''
        UnitArbiter()._register_unit(unit_name)
    def e(n: "Num"):
        '''The "Editor" command. Spawns your $EDITOR with the Num's state.'''
        import tempfile, os, subprocess
        initial_text = f"Unit: {n.unit}\nValue: {n._real}\nDoc: {n.d}"
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+', delete=False) as tf:
            tf.write(initial_text)
            temp_path = tf.name
        # Fire up vi/vim/nano
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, temp_path])
        # ... logic to read the file back and update n.d ...
        print(f"Updated {n.unit} metadata.")

if 0:   # Global namespace function population
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
    # Try to duplicate PUL's nan result.  The idea here is to do two calculations of the
    # derivative in UnitArbiter.inject_math.wrapped where uncertainty gets propagated.
    # If the slope is really steep like the 1e11 case for the sqrt at zero, the two
    # estimates should be hugely different.
    x = Num("0")
    x.re_unc = mpmath.mpf(1)
    x.mytype = NumType.Unc
    result = sqrt(x)
    # Note:  the numerical differentiation gives a large number 1.9e11 for
    # the sensitivity sens in inject_math.wrapped().  However, it of course
    # doesn't result in a NaN like the python uncertainties library gets.
    Assert(result == Num(0))
    y = Num(result.re_unc)
    Assert(y.approx(1.94368e+11, 4))
    exit()

if 1:   # Self-tests
        def Test_Constructor_With_Numbers():
            zero = 0
            if 1:   # No input
                num = Num()
                Assert(num._real == 0 and num._imag == 0)
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
                Assert(num._real == x and num._imag == 0)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num._real == -x and num._imag == 0)
                Assert(num.mytype == T)
            if 1:   # Decimal
                s = "3095.7357"
                x, T = decimal.Decimal(s), NumType.Flt
                num = Num(x)
                Assert(num._real == mpmath.mpf(s) and num._imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num._real == -x and num._imag == zero)
                Assert(num.mytype == T)
            if 1:   # mpmath.mpf
                s, T = "3095.7357", NumType.Flt
                x = mpmath.mpf(s)
                num = Num(x)
                Assert(num._real == x and num._imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num._real == -x and num._imag == zero)
                Assert(num.mytype == T)
            if 1:   # Complex
                x, T = -1+3j, NumType.Cpx
                num = Num(x)
                Assert(num._real == mpmath.mpf(-1) and num._imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num._real == mpmath.mpf(1) and num._imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # mpmath.mpc
                x, T = mpmath.mpc(-1, 3), NumType.Cpx
                num = Num(x)
                Assert(num._real == mpmath.mpf(-1) and num._imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num._real == mpmath.mpf(1) and num._imag == mpmath.mpf(-3))
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
                Assert(x.mytype == typ, expected=typ, got=x.mytype)
                # Check numerical value
                if s == "1":
                    Assert(x.numer == 1 and x.denom == 1)
                elif s == "1/2":
                    Assert(x.numer == 1 and x.denom == 2)
                elif s == "1.2":
                    Assert(x._real == mpmath.mpf(s))
                    Assert(x._imag == zero)
                elif s == "1.2e3":
                    Assert(x.approx(Num("1200/1"), ndigits))
                    Assert(x._imag == zero)
                elif s == "1+2j":
                    Assert(x._real == mpmath.mpf("1") and x._imag == mpmath.mpf("2"))
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
                    Assert(result._real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "ft"))
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
                    expected = Num('-2.28083989501312 ft')
                    Assert(result == expected)
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x - y
                    #expected = Num("-1.125 inch")
                    expected = Num("-9/8", "in")   # 3/8 - 12/8 = -9/8
                    Assert(result == expected)
            if 1:   # Test multiplication
                if 1:   # Integer & real
                    x = Num("1.5", "V")
                    y = Num("2.0", "A")
                    result = x*y
                    expected = "3.0"
                    Assert(result._real == mpmath.mpf(expected))
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
            Assert(x._real == mpmath.mpf("1.23"))
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
                expected = Num("0.0385563058736576 m^2")
                if 0:
                    result.dump()
                    expected.dump()
                    print("Are they equal?  ", result == expected)
                    print(f"result.raw_value   = {result.raw_value} {type(result.raw_value)}")
                    print(f"expected.raw_value = {expected.raw_value} {type(expected.raw_value)}")
                Assert(result == expected)
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
                Assert(x._real == mpmath.mpf("inf") and x.unit == "m")
                x = Num("-inf m")
                Assert(x._real == mpmath.mpf("-inf") and x.unit == "m")
                x = Num("nan m")
                Assert(mpmath.isnan(x._real) and x.unit == "m")
                x = Num("0+nanj m")
                Assert(x._real == 0 and mpmath.isnan(x._imag) and x.unit == "m")
                x = Num("nan+nanj m")
                Assert(mpmath.isnan(x._real) and mpmath.isnan(x._imag) and x.unit == "m")
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
                self._real: mpmath.mpf = mpmath.mpf("0")
                self._imag: mpmath.mpf = mpmath.mpf("0")
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
                if 1:   # Dump values for debugging
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
            if 0:   # Cosine law example
                theta = Num(radians(60))    # 60°±2° 
                theta.re_unc = radians(mpf(2))
                theta.mytype = NumType.Unc
                result = sqrt(x1*x1 + x2*x2 - 2*x1*x2*cos(theta))
                if 0:   # Dump
                    print("theta dump")
                    theta.dump(indent)  # 1.0472 radians
                    print("result dump")
                    result.dump(indent)
            if 1:   # NaN example
                x = Num("0")
                x.re_unc = mpf(1)
                x.mytype = NumType.Unc
                result = sqrt(x)
                # Note:  the numerical differentiation gives a large number (1.9e11 for
                # the default diff, but we're using a heuristic to select the step size
                # h) sensitivity sens in inject_math.wrapped().  However, it of course
                # doesn't result in a NaN like the python uncertainties library gets.
                Assert(result == Num(0))
                y = Num(result.re_unc)
                Assert(y.approx(22360, 4))
                #yy


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

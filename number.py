from __future__ import annotations
'''
Wed 8 Apr 2026 Tasks

- Verify infection model for REPL
- Should handle lbm/in³:  translate Unicode exponents to regular digits
- Start playing with it in the REPL; it's almost a real calculator
- What other __add__/__radd__ methods need to be done?  Can Mike automate this task with
  what we know now?
- Make sure Mike has latest code
- We're using 12 digits in RoundOff; this is probably a good heuristic for the usual
  float stuff, particularly with what's returned by gunits.
- Add nbs to string between number and unit

'''
if 1:  # Header
    if 1:   # Standard imports
        import decimal
        import enum
        import fcntl
        import fractions
        import operator
        import os
        import pathlib
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
        t = trm.TrmDP()
        t.dbg = "#bdf6fe"
        g = dptypes.Constant()
        g.dbg = True if 0 else False
        g.X = False
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

if 0:   # Num class 
    class Num:
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
        }
        flip = False    # If True, flip str() and repr() behavior
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            '''Constructor for the Num instance, an immutable number container

            value can be one of the numeric types int, fractions.Fraction, float,
            decimal.Decimal, mpmath.mpf, complex, mpmath.mpc, uncertainties.ufloat, or a
            string.  If a string, you can include the unit string with it, separated
            from the numerical string by one or more string.whitespace characters.  If
            the unit keyword is used, it will override any unit defined in the value
            string.

            '''
            self._doc = ""  # The mutable metadata
            self.main_config = "/home/don/.0rc/bin/definitions.units"
            self.dynamic_config_path = "/home/don/.units_dynamic"
            UnitArbiter(self.main_config, self.dynamic_config_path)
            if isinstance(value, str):
                # Check for a smart split, a rightmost whitespace character that is
                # between the number and the trailing unit.  _extract_unit() uses
                # str.rsplit(None, 1) for this case, an excellent tool.  Note the unit
                # keyword argument overrides the unit string in the value argument if
                # the keyword argument is not the empty string.
                val_str, found_unit = self._extract_unit(value)
                if found_unit:
                    unit = found_unit if not unit else f"({found_unit})*({unit})"
                value = val_str # Continue to _parse_string with just the number part
            if 1:  # Default internal state representation
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
                    RegisterUnit(unit)
                self.unit = unit
                if value is None:
                    return
            if 1:  # High-Precision Conversion Logic
                if isinstance(value, Num):
                    self.numer = value.numer
                    self.denom = value.denom
                    self.real = value.real
                    self.imag = value.imag
                    self.re_unc = value.re_unc
                    self.im_unc = value.im_unc
                    self.unit = unit if unit else value.unit
                    self.mytype = value.mytype
                elif isinstance(value, int):
                    self.numer = int(value)
                    self.mytype = NumType.Int
                elif isinstance(value, float):
                    self.real = mpmath.mpf(repr(value))
                    self.mytype = NumType.Flt
                elif isinstance(value, complex):
                    self.real = mpmath.mpf(repr(value.real))
                    self.imag = mpmath.mpf(repr(value.imag))
                    self.mytype = NumType.Cpx
                elif isinstance(value, decimal.Decimal):
                    self.real = mpmath.mpf(str(value))
                    self.mytype = NumType.Flt
                elif isinstance(value, fractions.Fraction):
                    self.numer = value.numerator
                    self.denom = value.denominator
                    self.mytype = NumType.Rat
                elif isinstance(value, mpmath.mpf):
                    self.real = value
                    self.mytype = NumType.Flt
                elif isinstance(value, mpmath.mpc):
                    self.real = value.real
                    self.imag = value.imag
                    self.mytype = NumType.Cpx
                elif isinstance(value, uncertainties.UFloat):
                    self.real = mpmath.mpf(str(value.nominal_value))
                    self.re_unc = mpmath.mpf(str(value.std_dev))
                    self.mytype = NumType.Unc
                elif isinstance(value, str):
                    self.unit = unit    # This overrides any unit in value
                    self._parse_string(value)
                else:
                    raise TypeError(f"Type of {value!r} is not supported")
        def _parse_string(self, value: str) -> None:
            msg = f"{value!r} not recognized as a number"
            normalized = set(value.lower().replace("i", "j").strip())
            if "/" in normalized:
                try:
                    parts = [int(i) for i in value.split("/")]
                    self.numer = parts[0]
                    self.denom = parts[1]
                    self.mytype = NumType.Rat
                except Exception as e:
                    raise ValueError(msg) from e
            elif "j" in normalized:
                re_part, im_part = dpmath.ParseComplex(value)
                self.real = mpmath.mpf(re_part)
                self.imag = mpmath.mpf(im_part)
                self.mytype = NumType.Cpx
            elif "." in normalized or "e" in normalized:
                try:
                    self.real = mpmath.mpf(value)
                    self.mytype = NumType.Flt
                except Exception as e:
                    raise ValueError(msg) from e
            else:
                try:
                    self.numer = int(value)
                    self.mytype = NumType.Int
                except Exception as e:
                    raise ValueError(msg) from e
        def _extract_unit(self, s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            # If there's no space, there's definitely no unit-shorthand
            if " " not in s:
                return s, ""
            parts = s.rsplit(None, 1)
            val_part, unit_part = parts
            # HEURISTIC: A unit usually starts with a letter, a parenthesis (e.g.
            # "(m)/(s)"), or a percent sign.  We also check that the val_part doesn't
            # end with an 'e' (protecting scientific notation like "1.23 e-4")
            if unit_part[0].isalpha() or unit_part[0] in "(%":
                if not val_part.lower().endswith("e"):
                    return val_part.strip(), unit_part.strip()
            return s, ""
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            target_type = max(self.mytype.value, other.mytype.value)
            if target_type <= NumType.Rat.value:
                result = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return Num(result)
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            a_val = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other.real if other.mytype >= NumType.Flt else other.as_mpf
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                a_complex = mpmath.mpc(self.real, self.imag)
                b_complex = mpmath.mpc(other.real, other.imag)
                return Num(op_func(a_complex, b_complex))
            return Num(op_func(a_val, b_val))
        def _normalize(self, other: "Num") -> "Num":
            '''Returns a copy of other scaled to self.unit.'''
            if (not self.unit and not other.unit) or (self.unit == other.unit):
                return Num(other)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {self.unit} vs {other.unit}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            if adjusted.mytype <= NumType.Rat:
                adjusted.real = adjusted.as_mpf*factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real = adjusted.real*factor
                adjusted.imag = adjusted.imag*factor
            adjusted.unit = self.unit
            return adjusted
        def __add__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adjusted = self._normalize(other_num)
            result = self._binary_op(adjusted, operator.add)
            result.unit = self.unit
            return result
        def __sub__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adjusted = self._normalize(other_num)
            result = self._binary_op(adjusted, operator.sub)
            result.unit = self.unit
            return result
        def __mul__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            result = self._binary_op(other_num, operator.mul)
            if not self.unit and not other_num.unit:
                result.unit = ""
            elif self.unit and not other_num.unit:
                result.unit = self.unit
            elif not self.unit and other_num.unit:
                result.unit = other_num.unit
            else:
                result.unit = f"({self.unit})*({other_num.unit})"
            return result
        def __rmul__(self, other: ty.Any) -> "Num":
            return self.__mul__(other)
        def __truediv__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            if other_num.as_mpf == 0:
                raise ZeroDivisionError("Tractor at 0 divisor.")
            result = self._binary_op(other_num, operator.truediv)
            if not self.unit and not other_num.unit:
                result.unit = ""
            elif self.unit and not other_num.unit:
                result.unit = self.unit
            elif not self.unit and other_num.unit:
                result.unit = f"1/({other_num.unit})"
            else:
                result.unit = f"({self.unit})/({other_num.unit})"
            return result
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other)/self
        def _compare(self, other: ty.Any, op_func: ty.Callable) -> bool:
            other_num = Num(other)
            adjusted = self._normalize(other_num)
            target_type = max(self.mytype.value, adjusted.mytype.value)
            if target_type <= NumType.Rat.value:
                return op_func(self.as_int_or_rat, adjusted.as_int_or_rat)
            return bool(op_func(self.as_mpf, adjusted.as_mpf))
        def __lt__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.lt)
        def __le__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.le)
        def __gt__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.gt)
        def __ge__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.ge)
        def __eq__(self, other: ty.Any) -> bool:
            other_num = Num(other)
            if self.unit != other_num.unit:
                return False
            target_type = max(self.mytype.value, other_num.mytype.value)
            if target_type <= NumType.Rat.value:
                return self.as_int_or_rat == other_num.as_int_or_rat
            return bool(self.as_mpf == other_num.as_mpf)
        def _s(self, flip: bool) -> str:
            '''Return str() or repr(), depending on Num.flip This is handy when you're
            in the debugger, because the default output for 'p x' where x is a Num
            instance is the repr() string.  Set 'x.f = True' and then you'll get the
            str() string, which is formatted for the chosen number of significant
            figures and uses colorizing to indicate type.
            '''
            if Num.flip:
                # Normal repr() string
                if self.mytype == NumType.Int:
                    s = str(self.numer)
                elif self.mytype == NumType.Rat:
                    s = f"{self.numer}/{self.denom}"
                elif self.mytype == NumType.Cpx:
                    s = f"{self.real!r}+{self.imag!r}j"
                elif self.mytype == NumType.Unc:
                    s = f"{self.real} +/- {self.re_unc}"
                else:
                    s = f"{self.real!r}"
                return f'Num("{s}", "{self.unit}")'
            else:
                # Normal str() string
                if self.mytype == NumType.Int:
                    s = fmt.fmt(self.numer)
                elif self.mytype == NumType.Rat:
                    s = fmt.fmt(fractions.Fraction(self.numer, self.denom))
                elif self.mytype == NumType.Cpx:
                    s = fmt.fmt(mpmath.mpc(self.real, self.imag))
                elif self.mytype == NumType.Unc:
                    s = f"{self.real} +/- {self.re_unc}"
                else:
                    s = fmt.fmt(self.real)
                unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
                color = Num.type_color.get(self.mytype, t.wht)
                return f"{color}{s}{t.n}{unit_string}"
        def __str__(self) -> str:
            if not self.f:
                return self._s(False)   # str() behavior
            return self._s(True)        # repr() behavior
        def __repr__(self) -> str:
            if not self.f:
                return self._s(True)    # repr() behavior
            return self._s(False)       # str() behavior
        def u(self, conversion_str: str) -> "Num":
            '''
            Conversion utility bridge to GNU units.
            Input format: "<from_expr> , <to_expr>"
            Example: x.u("17 yards + 2 feet + 5 inches, m")
            '''
            if "," not in conversion_str:
                raise ValueError("Format must be '<from> , <to>'")
            # Split into 'have' and 'want'
            have, want = [part.strip() for part in conversion_str.split(",", 1)]
            arbiter = UnitArbiter()
            # We use check_conformable under the hood because it handles 
            # the multi-line pipe logic and error catching for us.
            is_ok, result_str = arbiter.check_conformable(have, want)
            if is_ok:
                # GNU units returns the multiplier. 
                # We create a new Num with that magnitude and the 'want' unit.
                # Note: We use Num(result_str, want) which will handle 
                # the high-precision string -> mpf/Rat conversion.
                try:
                    return Num(result_str, want)
                except Exception as e:
                    raise ValueError(f"Could not parse units result '{result_str}': {e}")
            else:
                # Pass the GNU units error (e.g., 'Unknown unit', 'conformability error')
                # straight back to the user.
                raise ValueError(f"GNU Units Error: {result_str}")
        @property
        def f(self) -> bool:
            return Num.flip
        @f.setter
        def f(self, value) -> None:
            Num.flip = bool(value)
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @unit.setter
        def unit(self, value: str) -> None:
            self._unit = value.strip() if value else ""
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
        def d(self):
            return self._doc
        @d.setter
        def d(self, text):
            self._doc = text
            # Here we could trigger a "Silent Save" to SQLite
            # so the note is immediately persistent.
            self._sync_to_db()
        def _sync_to_db(self) -> None:
            'Placeholder for a synchronization'
            lwtest.ToDo("Num._sync_to_db needs implementation")
        def promote(self) -> "Num":
            '''Attempt to simplify the unit string using high-precision rounding.'''
            if not self.unit:
                return self
            arbiter = UnitArbiter()
            candidate = arbiter.discover_best_unit(self.unit)
            if candidate == self.unit:
                return self
            is_ok, factor_str = arbiter.check_conformable(self.unit, candidate)
            if is_ok:
                factor = mpmath.mpf(factor_str)
                # Check if factor is 1.0 within 12 digits
                if self.round_off(factor, digits=12) == 1:
                    return self.to(candidate)
            return self
        def round_off(self, val: ty.Any, digits: int = 12) -> ty.Any:
            '''Round the significand to clean up floating point noise.'''
            if isinstance(val, (int, fractions.Fraction)):
                return val
            if isinstance(val, mpmath.mpf):
                d = decimal.Decimal(mpmath.nstr(val, 17))
                with decimal.localcontext() as ctx:
                    ctx.prec = digits
                    d = +d
                return mpmath.mpf(str(d))
            return val
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            '''
            Convert current Num to the specified unit.
            If auto_promote is True, it will attempt to simplify the 
            resulting unit string to a standard symbol.
            '''
            if not unit:
                return Num(self)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
            if not is_ok:
                # Check if 'unit' is actually a known primitive first
                # If not, try to register it on the fly
                RegisterUnit(unit)
                is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
                if not is_ok:
                    raise ValueError(f"Incompatible units: {self.unit} and {unit}")
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            # Perform the scaling
            if res.mytype <= NumType.Rat:
                res.real = res.as_mpf * factor
                res.mytype = NumType.Flt
            else:
                res.real = res.real * factor
                res.imag = res.imag * factor
            res.unit = unit
            # The "REPL Intelligence" step
            if auto_promote:
                return res.promote()
            return res
        def add_unit(self, definition: str):
                '''
                Noether REPL: Teaches the system a new unit.
                Example: x.add_unit("bag 90 lb")
                '''
                arb = UnitArbiter()
                # The Arbiter handles the gatekeeping and the file append
                arb.add_unit(definition)
                # We don't necessarily need a local _restart_arbiter if the
                # Arbiter class handles its own restart, but it's good for
                # internal Num state consistency if we had any cached values.

if 0:  # Unit arbiter and registration
    class UnitArbiter:
        _instance = None
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self, main_config="", dynamic_config=""):
            UnitArbiter(self.main_config, self.dynamic_config_path)
            if self._initialized:
                return
            self.main_config = main_config
            # Path for the dynamic units file (Noether's "Memory")
            if dynamic_config:
                self.dynamic_path = dynamic_config
            else:
                self.dynamic_path = Path("~/.units_dynamic").expanduser()
            if not self.dynamic_path.exists():
                self.dynamic_path.touch()
            self.proc = None
            self._start_process()
            self._initialized = True
        def _start_process(self):
            '''Starts or Restarts the GNU Units pipe with -q (quiet) and -v (verbose).'''
            if self.proc:
                self.proc.terminate()
                self.proc.wait()
            # Load standard units then our dynamic ones
            # Use -v to get the 'verbose' output which check_conformable relies on
            cmd = ["units", "-q", "-v", "-f", "", "-f", str(self.dynamic_path)]
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def _check_definition(self, definition: str) -> tuple[bool, str]:
            '''The Gatekeeper: Uses 'units -c' to verify syntax and check for loops.'''
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                tmp.write(definition + "\n")
                tmp_path = tmp.name
            # -c checks for irreducible or circular definitions
            cmd = ["units", "-c", "-q", "-f", "", "-f", str(self.dynamic_path), "-f", tmp_path]
            try:
                # Added a short timeout to prevent "Infinite Loop" hangs
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                is_ok = (result.returncode == 0)
                error_msg = result.stderr or result.stdout
            except subprocess.TimeoutExpired:
                is_ok = False
                error_msg = "Checking hung (possible infinite circular definition)."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return is_ok, error_msg
        def add_primitive(self, unit_name: str):
            '''Defines a new fundamental dimension (e.g., 'step !').'''
            definition = f"{unit_name.strip()} !"
            self._commit_unit(definition)
        def add_unit(self, definition: str):
            '''Adds a scaling definition (e.g., 'steps 2 step').'''
            # Clean common user errors (like '=') but rely on -c for the final word
            sanitized = definition.replace("=", "").strip()
            self._commit_unit(sanitized)
        def _commit_unit(self, entry: str):
            '''Vets and appends the entry to the dynamic config file.'''
            is_ok, error = self._check_definition(entry)
            if is_ok:
                with open(self.dynamic_path, "a") as f:
                    f.write(f"{entry}\n")
                self._start_process()
                print(f"Noether REPL learned: {entry}")
            else:
                print(f"✔  Unit Definition Error: {error.strip()}")
                print("Action: Entry rejected. Fix syntax and try again.")
        def check_conformable(self, have: str, want: str) -> tuple[bool, str]:
            '''
            Asks the Units pipe if 'have' can convert to 'want'.
            Returns (True, "multiplier") or (False, "error message").
            '''
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            try:
                # Send the request to the pipe
                self.proc.stdin.write(f"{have}\n{want}\n")
                self.proc.stdin.flush()
                # Read result lines
                line1 = self.proc.stdout.readline().strip()
                line2 = self.proc.stdout.readline().strip()
                if "*" in line1:
                    # Success: return the multiplier (usually the second line is the '/')
                    multiplier = line1.replace("*", "").strip()
                    return True, multiplier
                else:
                    # Failure: line1 might be 'conformability error'
                    return False, f"{line1} {line2}".strip()
            except Exception as e:
                return False, f"Pipe communication error: {str(e)}"
        def get_base_dimensions(self, unit_str: str) -> str:
            '''Reduces a unit to its primitive SI components for hashing/invariance.'''
            # Shortcut: asking for conversion to '' (empty) often triggers base reduction
            ok, res = self.check_conformable(unit_str, "")
            # This part requires parsing the 'v' (verbose) output for base units
            # For now, returning the raw result string
            return res if ok else "dimensionless"
else:
    class UnitArbiter:
        _instance = None
        # Class-level configuration defaults
        # Set these once at the start of your session if they differ from defaults
        main_config = "/home/don/.0rc/bin/definitions.units"
        dynamic_config = "/home/don/.units_dynamic"
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self):
            if self._initialized:
                return
            self.dynamic_path = Path(self.dynamic_config).expanduser()
            if not self.dynamic_path.exists():
                self.dynamic_path.touch()
            self.proc = None
            self._start_process()
            self._initialized = True
        def _start_process(self):
            '''Starts/Restarts the GNU Units pipe with custom config paths.'''
            if self.proc:
                self.proc.terminate()
                self.proc.wait()
            # -f "" loads the standard units library
            # -f self.main_config loads your static custom definitions
            # -f self.dynamic_path loads Noether's "learned" units
            cmd = ["units", "-q", "-v", "-f", "", "-f", self.main_config, "-f", str(self.dynamic_path)]
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def is_known_unit(self, unit_str: str) -> bool:
            '''Check if a unit is already defined without attempting a conversion.'''
            if not unit_str: return True
            # Converting a unit to itself is the fastest way to check existence
            ok, _ = self.check_conformable(unit_str, unit_str)
            return ok
        def _check_definition(self, definition: str) -> tuple[bool, str]:
            '''Gatekeeper: Verifies syntax/loops using 'units -c'.'''
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                tmp.write(definition + "\n")
                tmp_path = tmp.name
            cmd = ["units", "-c", "-q", "-f", "", "-f", self.main_config, "-f", str(self.dynamic_path), "-f", tmp_path]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                is_ok = (result.returncode == 0)
                error_msg = result.stderr or result.stdout
            except subprocess.TimeoutExpired:
                is_ok, error_msg = False, "Circular definition detected (Check timed out)."
            finally:
                if os.path.exists(tmp_path): os.remove(tmp_path)
            return is_ok, error_msg
        def add_primitive(self, unit_name: str):
            self._commit_unit(f"{unit_name.strip()} !")
        def add_unit(self, definition: str):
            sanitized = definition.replace("=", "").strip()
            self._commit_unit(sanitized)
        def _commit_unit(self, entry: str):
            is_ok, error = self._check_definition(entry)
            if is_ok:
                with open(self.dynamic_path, "a") as f:
                    f.write(f"{entry}\n")
                self._start_process()
                print(f"Γ¥ô Noether REPL learned: {entry}")
            else:
                print(f"!! Unit Error: {error.strip()}")
        def check_conformable(self, have: str, want: str) -> tuple[bool, str]:
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            try:
                self.proc.stdin.write(f"{have}\n{want}\n")
                self.proc.stdin.flush()
                line1 = self.proc.stdout.readline().strip()
                line2 = self.proc.stdout.readline().strip()
                if "*" in line1:
                    return True, line1.replace("*", "").strip()
                return False, f"{line1} {line2}"
            except Exception as e:
                return False, str(e)

if 1:  # Utility functions
    def RegisterUnit(unit_name: ty.Optional[str]) -> None:
        '''Register a new primitive unit if it is unknown to the arbiter.'''
        if not unit_name:
            return
        arbiter = UnitArbiter()
        # Existence check: compare unit to itself.
        # This avoids dimension mismatches with '1'.
        breakpoint() # ∞∞ 
        is_known, message = arbiter.check_conformable(unit_name, unit_name)
        if not is_known and "unknown" in message.lower():
            arbiter.add_primitive(unit_name)
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

if 1:  # Temp experiment
    x = Num("1 step")
    x.add_unit("steps = step")
    exit()
if 0:  # Section: Discovery Pipe Test
    def Test_Discovery_Pipe():
        '''Test if '?' dump works over a non-interactive pipe without a pager.'''
        arbiter = UnitArbiter()
        unit_to_test = "kg m^2 / s^2"
        try:
            Dbg(f"Testing discovery pipe for: {unit_to_test}", color="sky")
            # We send the unit, then the '?', then 'quit' just to be safe
            query = f"{unit_to_test}\n?\nquit\n"
            arbiter.proc.stdin.write(query)
            arbiter.proc.stdin.flush()
            Dbg("Reading response from pipe...", color="mag")
            lines_captured = 0
            # We'll read until the pipe is empty or we hit a timeout
            while lines_captured < 100:
                line = arbiter.proc.stdout.readline().strip()
                if not line:
                    break
                # We expect to see units like 'joule', 'newton meter', etc.
                Dbg(f"  [{lines_captured:02d}] {line}")
                lines_captured += 1
                # If we see the next prompt, we're done with the list
                if "You want:" in line:
                    break
            if lines_captured > 5:
                print(f"{t.grn}Success:{t.n} Captured {lines_captured} conformable units.")
            else:
                print(f"{t.red}Failure:{t.n} Captured only {lines_captured} lines. Pager might be blocking.")
        except Exception as e:
            print(f"{t.red}Error during pipe test:{t.n} {e!r}")
if 1:   # Self-tests
        def Test_Constructor_With_Numbers():
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
                    Assert(x.real == mpmath.mpf("1.2") and x.imag == zero)
                elif s == "1.2e3":
                    Assert(x.real == mpmath.mpf("1.2e3") and x.imag == zero)
                elif s == "1+2j":
                    Assert(x.real == mpmath.mpf("1") and x.imag == mpmath.mpf("2"))
        def Test_Arithmetic():
            if 1:   # Test addition
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x + y
                    expected = "4.2808398950131199"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "ft"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x + y
                    expected = Num("15/8", "in")
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
                    expected = "-2.2808398950131199"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "ft"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x - y
                    expected = Num("-9/8", "in")   # 3/8 - 12/8 = 9/8
                    Assert(result == expected)
            if 1:   # Test multiplication
                if 1:   # Integer & real
                    x = Num("1.5", "V")
                    y = Num("2.0", "A")
                    result = x*y
                    expected = "3.0"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "(V)*(A)"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x*y
                    expected = Num("9/16", "(in)*(in)")   # 3/8*12/8 = 36/64 = 9/16
                    Assert(result == expected)
            if 1:   # Test division
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x/y
                    expected = "1.0"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "(ft)/(m)"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x/y
                    expected = Num("1/4", "(in)/(in)")   # (3/8)/(12/8) = 1/4
                    Assert(result == expected)
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
                with g:
                    g.X = 1
                Assert(N("0 m") + N("0 m") == N("0 m"))
            if 1:   # "1+2i m" * "3/4 A":  hope we don't get mA
                a = N("1+2i m")
                b = N("3/4 A")
                lwtest.ToDo("Bug in '1+2i m'*'3/4 A' -> 0.00+0.00j (m)*(A)")
                breakpoint() # ∞∞ 
                Assert(a*b == N("0.75+1.5i m*A"))
'''
Other tests
    - '0 m' + '0 J' -> error
    - '1 m' + '1 J' -> error
    - '3 m' % '14 j' (error, units must be conformable)
    - General:  x ⚬ y OK if units are conformable, result gets units of 1st arg
    - inf and nan
        - '3 + nan i'?, should stay in ℂ?
    - Nails:  ϵ + i, 1 + ϵi
    - '1.23453094830853048309739047394739473947394739473947e4 m3' Does GNU units barf
      on this?  No, handles it fine; appears to handle unlimited digits.

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
        def Warn(*msg, **kw):
            print(*msg, file=sys.stderr)
        def Error(*msg, status=1):
            Warn(f"{t.err}", end="")
            Warn(*msg)
            Warn(f"{t.n}")
            exit(status)
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
    if 1:
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        #if args:
        #    for arg in args:
        #        pass    # Do stuff
    if 1:   # Demo & tests for module
        zero = mpmath.mpf(0)
        def Demo():
            pass
        if 0:   # Special one-off test area
            Test_Discovery_Pipe()
            exit()
            
        exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])

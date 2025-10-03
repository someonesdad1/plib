'''
Date/time strings for now() I use a lot
'''
##∞test∞# ignore #∞test∞#
from time import strftime
def Date():
    'Date = 12Feb2022'
    s = strftime("%d%b%Y")
    if s[0] == "0":
        s = s[1:]
    return s
def date():
    'date = 12 Feb 2022'
    s = strftime("%d %b %Y")
    if s[0] == "0":
        s = s[1:]
    return s
def Time():
    'Time = 8:50:00am'
    s = strftime("%p").lower()
    t = strftime(f"%I:%M:%S{s}")
    if t[0] == "0":
        t = t[1:]
    return t
def time():
    'time = 8:50:00 am'
    s = strftime("%p").lower()
    t = strftime(f"%I:%M:%S {s}")
    if t[0] == "0":
        t = t[1:]
    return t
def Dttm():
    'Date/time = 12Feb2022-8:50:00am'
    return f"{Date()}-{Time()}"
def dttm():
    'Date/time = 12 Feb 2022 8:50:00 am'
    return f"{date()} {time()}"
def tm24():
    'Time in 24 hour mode'
    return strftime(f"%H:%M:%S")
def Dttm24():
    'Date/time in 24 hr mode = 12Feb2022-08:50:00'
    return f"{Date()}-{tm24()}"
def dttm24():
    'Date/time in 24 hr mode = 12Feb2022 08:50:00'
    return f"{date()} {tm24()}"
if __name__ == "__main__":
    print(f"Date() = {Date()}, date() = {date()}")
    print(f"Time() = {Time()}, time() = {time()}")
    print(f"Date/time (Dttm()) = {Dttm()}")
    print(f"Date/time (dttm()) = {dttm()}")
    print(f"Time in 24 hr mode (tm24()) = {tm24()}")
    print(f"Date/time in 24 hr mode (Dttm24()) = {Dttm24()}")
    print(f"Date/time in 24 hr mode (dttm24()) = {dttm24()}")

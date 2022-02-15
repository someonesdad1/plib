'''
Date/time strings for now() I use a lot
'''

from time import strftime as ft

def dt():
    'Date = 12Feb2022'
    return ft("%d%b%Y")
def tm():   # Time in am/pm form
    'Time = 8:50:00am'
    s = ft("%p").lower()
    t = ft(f"%I:%M:%S{s}")
    if t[0] == "0":
        t = t[1:]
    return t
def dttm():   # Date/time in am/pm form
    'Date/time = 12Feb2022-8:50:00am'
    return f"{dt()}-{tm()}"
def tm24():   # Time in 24 hour form
    'Time in 24 hr mode = 08:50:00'
    return ft(f"%H:%M:%S")
def dttm24():   # Date/time in 24 hour form
    'Date/time in 24 hr mode = 12Feb2022-08:50:00'
    return f"{dt()}-{tm24()}"

if __name__ == "__main__": 
    print(f"Date = {dt()}")
    print(f"Time = {tm()}")
    print(f"Date/time = {dttm()}")
    print(f"Time in 24 hr mode = {tm24()}")
    print(f"Date/time in 24 hr mode = {dttm24()}")

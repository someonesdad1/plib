'''
Date/time strings I use a lot
'''

from time import strftime as ft

def dt():
    return ft("%d%b%Y")
def tm():   # Time in am/pm form
    s = ft("%p").lower()
    t = ft(f"%I:%M:%S{s}")
    if t[0] == "0":
        t = t[1:]
    return t
def dttm():   # Date/time in am/pm form
    return f"{dt()}-{tm()}"
def tm24():   # Time in 24 hour form
    return ft(f"%H:%M:%S")
def dttm24():   # Date/time in 24 hour form
    return f"{dt()}-{tm24()}"

if __name__ == "__main__": 
    print(f"Date = {dt()}")
    print(f"Time = {tm()}")
    print(f"Date/time = {dttm()}")
    print(f"Time in 24 hr mode = {tm24()}")
    print(f"Date/time in 24 hr mode = {dttm24()}")

from fairbanks_scale import init, current
from threading import Timer

init()

def print_scale_value():
    print(current())

t = Timer(10.0, print_scale_value)
t.start()
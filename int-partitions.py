#!/usr/bin/python

import sys
import re

PERX = 100

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

s = sum(ints)
t = 0

def perx(x):
    return PERX * x / s

for n in ints:
    t += n
    slot = perx(t) - perx(t - n)
    actual = perx(float(n))
    diff = slot - actual

    print "%d: %d (%.3f) (%.3f)" % (n, slot, actual, diff)


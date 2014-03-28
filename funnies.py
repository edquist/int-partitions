#!/usr/bin/python

import sys
import re
import math

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

P = 100
s = float(sum(ints))
qq = [x*P/s for x in ints]

for n,q in zip(ints,qq):
    if math.modf(q)[0] in (0,.5):
        print "%7d: %.3f%%" % (n, q)


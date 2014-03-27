#!/usr/bin/python

import sys
import re

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

P = 100
t = 0
s = sum(ints)
w = max(len(str(i)) for i in ints)

for n in ints:
    t += n
    slot = P*t/s - P*(t-n)/s

    print "%*d: %d%%" % (w, n, slot)


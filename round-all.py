#!/usr/bin/python

import sys
import re

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

P = 100
s = float(sum(ints))
w = max(len(str(i)) for i in ints)
r = [int(round(x*P/s)) for x in ints]

for n,slot in zip(ints,r):
    print "%*d: %d%%" % (w, n, slot)


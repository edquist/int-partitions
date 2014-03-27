#!/usr/bin/python

import sys
import re
import math
#from math import ceil
#from math import floor
import math

def iceil(x):  return int(math.ceil(x))
def ifloor(x): return int(math.floor(x))

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

P = 100
S = sum(ints)
w = max(len(str(i)) for i in ints)

P_S = float(P)/S
qq = [n * P_S for n in ints]
rr = map(int,map(round,qq))
R = sum(rr)
U = sum(map(int,map(ceil,qq)))
V = sum(map(int,map(floor,qq)))

ee = [rr[i] - qq[i] for i in range(len(qq))]

qq2,ii2=zip(*sorted(zip(qq,range(len(qq)))))
mm = list(enumerate(ii2))

for n in ints:
    t += n
    slot = P*t/s - P*(t-n)/s

    print "%*d: %d%%" % (w, n, slot)


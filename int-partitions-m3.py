#!/usr/bin/python

import sys
import re
import math
import itertools

# convenience functions
def     sgn(x): return -1 if x < 0 else 1
def   iceil(x): return int(math.ceil(x))
def  ifloor(x): return int(math.floor(x))
def  iround(x): return int(round(x))

# and magic functions, also for convenience  :)
def    iic(xx): return list(xx) + [itertools.count()]
def  zsort(*x): return zip(*sorted(zip(*x)))
def  msort(*x): return zsort(*iic(x))[-1]
def mmsort(*x): return msort(msort(*x))

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

P = 100
S = float(sum(ints))
N = len(ints)
w = max(len(str(d)) for d in ints)     # for print formatting

qq = [d * P / S for d in ints]         # raw percentages
rr = map(iround,qq)                    # rounded percentages
uu = map( iceil,qq)                    # integer ceilings of percentages
vv = map(ifloor,qq)                    # integer floors of percentages
ii = range(N)                          # convenience range array
ee = [rr[i] - qq[i]      for i in ii]  # primary sort by raw error
zz = [qq[i] * sgn(ee[i]) for i in ii]  # secondary sort to minimize rel. error
mm = mmsort(ee,zz)  # magic!           # reverse index of sort by arrays
R = sum(rr)

# percent partitions (also somewhat magic)
pp = [ uu[i] if mm[i] <  P-R      else
       vv[i] if mm[i] >= P-R + N  else
       rr[i] for i in ii ]

for d,p in zip(ints,pp):
    print "%*d: %d%%" % (w,d,p)


#!/usr/bin/python

import sys
import re
import math

# convenience functions
def  iceil(x): return int(math.ceil(x))
def ifloor(x): return int(math.floor(x))
def iround(x): return int(round(x))
def zsort(*x): return zip(*sorted(zip(*x)))

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

P = 100
S = sum(ints)
w = max(len(str(i)) for i in ints)

P_S = float(P)/S
qq = [n * P_S for n in ints]
rr = map(iround,qq)
ii = range(len(qq))
ee = [rr[i] - qq[i] for i in ii]
R = sum(rr)
U = sum(map(iceil,qq))
V = sum(map(ifloor,qq))

_,_,ii2 = zsort(ee,qq,ii)
_,mm = zsort(ii2,ii)

pp = [ iceil(qq[i]) if mm[i] <  P-R      else
      ifloor(qq[i]) if mm[i] >= P-R + n  else rr[i] for i in ii ]

#import __main__
#print "---"
#for v in "R P U V".split():
#    print "%s: %d" % (v,__main__.__dict__[v])
#print "---"

for n,slot in zip(ints,pp):
    print "%*d: %d%%" % (w, n, slot)


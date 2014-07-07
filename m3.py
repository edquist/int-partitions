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

def ints2pp(ints, P=100):
    S = sum(ints)
    N = len(ints)

    P_S = float(P)/S                         # just compute this once
    qq = [d * P_S for d in ints]             # raw percentages
    rr = map(iround,qq)                      # rounded percentages
    uu = map( iceil,qq)                      # integer ceilings of percentages
    vv = map(ifloor,qq)                      # integer floors of percentages
    ii = range(N)                            # convenience range array
    ee = [ rr[i] - qq[i]      for i in ii ]  # primary sort by raw error
    zz = [ qq[i] * sgn(ee[i]) for i in ii ]  # secondary sort, minimize rel err
    mm = mmsort(ee,zz)  # magic!             # reverse index of sort-by arrays
    R = sum(rr)                              # sum of rounded percents
    U = sum(uu)                              # sum of percent ceilings
    V = sum(vv)                              # sum of percent floors
    # Note: V <= (P,R) <= U <= V + N

    # percent partitions (also somewhat magic)
    pp = [ uu[i] if mm[i] <  P-R      else
           vv[i] if mm[i] >= P-R + N  else
           rr[i] for i in ii ]

    return pp

def print_ints_pp(ints):
    pp = ints2pp(ints)
    w  = max( len(str(d)) for d in ints )
    for d,p in zip(ints,pp):
        print "%*d: %d%%" % (w,d,p)

def hms2s(x):
    return sum( int(n) * 60**i for i,n in enumerate(reversed(x.split(':'))) )

def get_ints(seq, rx):
    for line in seq:
        m = re.search(rx,line)
        if m:
            yield line, hms2s(m.groups()[0])

def process_lines(seq):
    rx = r'(\d+(?:\d+)*)'
    lines,ints = zip(*get_ints(seq, rx))
    pp = ints2pp(ints)
    return [ re.sub(rx, '%d%%' % p, line, 1) for line,p in zip(lines,pp) ]

for line in process_lines(sys.stdin):
    print line.rstrip()



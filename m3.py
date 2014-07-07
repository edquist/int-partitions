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

def ints2pp(ints, flags=None, P=100):
    S = sum(ints)
    N = len(ints)

    if not flags:
        flags = [None] * N

    int_flags = zip(ints,flags)

    S0 = sum( d for d,f in int_flags if f is None    )
    S2 = sum( d for d,f in int_flags if f is not "@" )

    qq = [ 0               if f is "!" else
           d * float(P)/S  if f is "@" else
           d * float(P)*S2/S/S0 for d,f in int_flags ]

#   qq = [ d * float(P)/S for d in ints ]    # raw percentages
    rr = map(iround,qq)                      # rounded percentages
    uu = map( iceil,qq)                      # integer ceilings of percentages
    vv = map(ifloor,qq)                      # integer floors of percentages
    ii = range(N)                            # convenience range array
    ee = [ rr[i] - qq[i]      for i in ii ]  # primary sort by raw error
    zz = [ qq[i] * sgn(ee[i]) for i in ii ]  # secondary sort, minimize rel err
    mm = mmsort(ee,zz)  # magic!             # reverse index of sort-by arrays
    R = sum(rr)
    U = sum(uu)
    V = sum(vv)
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
            flag,hms = m.groups()
            yield line, hms2s(hms), flag

def process_lines(seq):
    rx = r'([@!])?(\d+(?:\d+)*)'
    lines,ints,flags = zip(*get_ints(seq, rx))
    pp = ints2pp(ints, flags)
    return [ re.sub(rx, '%d%%' % p, line, 1) for line,p in zip(lines,pp) ]

for line in process_lines(sys.stdin):
    print line.rstrip()



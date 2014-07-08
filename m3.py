#!/usr/bin/python

import sys
import re
import os
import math
import itertools
import getopt

class Cfg:
    show_orig     = False
    keep_nonzeros = True
    P             = 100

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

def fail(msg):
    print >>sys.stderr, msg
    sys.exit(1)

#  flag adjusted raw percentage:
#  !    -> 0% (to be amortized over non-flag items). only relevant with "@"
#  @    -> % based on total, including "!" values (use for leave)
#  %    -> fixed percentage, but doesn't contribute a number for "@"
#  +    -> locked 1%, but value still goes toward total for the sake of "@"
#  None -> amortized % for regular items

def ints2qq(ints, flags, P):
    int_flags = zip(ints,flags)

    S   = sum( d for d,f in int_flags if f is not "%"       )
    P  -= sum( d for d,f in int_flags if f is "%"           )
    P  -= sum( 1 for d,f in int_flags if f is "+"           )
    S0  = sum( d for d,f in int_flags if f is None          )
    S2  = sum( d for d,f in int_flags if f not in ("@","%") )
    SP  = float(P)/S if S  else 0
    SP2 = SP*S2/S0   if S0 else 0

    if P < 0:
        fail("this doesn't add up...")

    qq = [ 0       if flag is "!" else
           1       if flag is "+" else
           d       if flag is "%" else
           d * SP  if flag is "@" else
           d * SP2 for d,flag in int_flags ]

    #print "sum(qq) = %.3f" % sum(qq)

    return qq

def ints2pp(ints, flags=None, ops=Cfg()):
    N = len(ints)
    P = ops.P

    if flags:
        qq = ints2qq(ints,flags,P)           # flag-adjusted raw percentages
    else:
        S  = sum(ints)
        qq = [ float(d*P)/S for d in ints ]  # raw percentages
        flags = [None] * N

    rr = map(iround,qq)                      # rounded percentages
    uu = map( iceil,qq)                      # integer ceilings of percentages
    vv = map(ifloor,qq)                      # integer floors of percentages
    ii = range(N)                            # convenience range array
    ee = [ rr[i] - qq[i]      for i in ii ]  # primary sort by raw error
    zz = [ qq[i] * sgn(ee[i]) for i in ii ]  # secondary sort, minimize rel err
    mm = mmsort(ee,zz)  # magic!             # reverse index of sort-by arrays
    R = sum(rr)                              # rounded total
    U = sum(uu)                              # ceiling total
    V = sum(vv)                              # floor total
    # Note: V <= (P,R) <= U <= V + N

    # percent partitions (also somewhat magic)
    pp = [ uu[i] if mm[i] <  P-R      else
           vv[i] if mm[i] >= P-R + N  else
           rr[i] for i in ii ]

    # guarantee non-zero items produce non-zero percents
    if ops.keep_nonzeros:
        f2 = tuple( '+' if qq[i] > 0 and pp[i] == 0 else flags[i] for i in ii )
        if f2 != flags:
            pp = ints2pp(ints, f2, ops)

    return pp

def hms2s(x):
    return sum( int(n) * 60**i for i,n in enumerate(reversed(x.split(':'))) )

def get_ints(seq, rx):
    for line in seq:
        if line.startswith("#"):
            continue
        m = re.search(rx,line)
        if m:
            flag1,hms,flag2 = m.groups()
            yield line, hms2s(hms), flag1 or flag2

def process_lines(seq, ops=Cfg()):
    rx = r'([@!%])?(\d+(?::\d+)*)([@!%])?'
    repl = r'\2: %d%%' if ops.show_orig else r'%d%%'
    lines,ints,flags = zip(*get_ints(seq, rx))
    pp = ints2pp(ints, flags, ops)
    return [ re.sub(rx, repl % p, line, 1)
             for line,p,flag in zip(lines,pp,flags) if flag is not "!" ]

def main(argv):
    cfg = Cfg()
    ops,args = getopt.getopt(argv, 'znp:')
    for op,val in ops:
        if   op == '-z': cfg.keep_nonzeros = False
        elif op == '-n': cfg.show_orig     = True
        elif op == '-p': cfg.P             = int(val)

    inf = open(args[0]) if args else sys.stdin
    for line in process_lines(inf, cfg):
        print line.rstrip()

def usage():
    print "usage: %s [options] [file]" % os.path.basename(sys.argv[0])
    print
    print "options:"
    print "  -z     allow non-zero values to go to zero percent"
    print "  -n     show original numbers along with percents"
    print "  -p N   partition values into a total of N percent (default=100)"
    print

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except getopt.GetoptError:
        usage()


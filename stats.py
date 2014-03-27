#!/usr/bin/python

import sys
import re

def getints(f):
    for line in f:
        m = re.search(r'^\D*(\d+)\D+(\d+)\D*$', line)
        if m is not None:
            yield map(int,m.groups())

ints = list(getints(sys.stdin))

#def getints(line):
#    m = re.search(r'^\D*(\d+)\D+(\d+)\D*$', line)
#    return m and map(int,m.groups())
#
#ints = filter(None,(getints(line) for line in sys.stdin))

nn,pp = zip(*ints)

S = sum(nn)
P = sum(pp)
P_S = float(P)/S

qq = [n * P_S for n in nn]
dd = [abs(p-q) for p,q in zip(pp,qq)]

def avg(a):
    return float(sum(a))/len(a)

maxdiff = max(dd)
avgdiff = avg(dd)

print "%.3f %.3f" % (maxdiff,avgdiff)


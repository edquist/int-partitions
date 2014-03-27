#!/usr/bin/python

import sys
import re
import math
import itertools

PERX = 100

ints = [int(line) for line in sys.stdin if re.search(r'^\s*\d+\s*$', line)]

def go(arr):
    s = sum(arr)
    t = 0

    def perx(x):
        return PERX * x / s

    for n in arr:
        t += n
        slot = perx(t) - perx(t - n)
        actual = perx(float(n))
        diff = slot - actual

        yield (n, slot, actual, diff)
        #print "%d: %d (%.3f) (%.3f)" % (n, slot, actual, diff)

def go2(arr):
    s = sum(arr)
    t = 0

#   def perx(x):
#       return int(round(float(PERX * x) / s))
#
#   r = map(perx,arr[:-1])
#   r.append(PERX - sum(r))
#   return r

    def perx(x):
        return PERX * x / s

    for n in arr[:-1]:
        actual = perx(float(n))
        slot = int(round(actual))
        diff = slot - actual
        t += slot

        yield (n, slot, actual, diff)

    for n in arr[-1:]:
        actual = perx(float(n))
        slot = PERX - t
        diff = slot - actual

        yield (n, slot, actual, diff)

def go_max(arr):
    s = sum(arr)

    def perx(x):
        return PERX * x / s

    for n in arr:
        actual = perx(float(n))
        slot = int(round(actual))
        diff = slot - actual

        yield (n, slot, actual, diff)

def avg(a):
    return float(sum(a))/len(a)

def getdiff(x):
    return abs(x[3])

def getreldiff(x):
    return abs(x[3] / x[2]) if x[2] else x[3] > 0

def fpart(x):
    if x < 0:
        return -fpart(-x)
    else:
        return x - math.floor(x)

def afpart(x):
    return fpart(abs(x))

def stats(a):
    maxdiff = max(map(getdiff,a))
    avgdiff = avg(map(getdiff,a))
    maxreldiff = max(map(getreldiff,a))
    avgreldiff = avg(map(getreldiff,a))
    return "%.3f " * 4 % (maxdiff, avgdiff, maxreldiff, avgreldiff)

a1  = list(go(ints))
a2  = list(go(sorted(ints)))
a2r = list(go(sorted(ints,reverse=True)))
a3  = list(go(sorted(ints,key=fpart)))
a3r = list(go(sorted(ints,key=fpart,reverse=True)))
a4  = list(go(sorted(ints,key=afpart)))
a4r = list(go(sorted(ints,key=afpart,reverse=True)))

b1  = list(go2(ints))
b2  = list(go2(sorted(ints)))

tbest  = list(go_max(ints))

#print a1
#print a2
#print b1
#print b2
#sys.exit()

print "xxxxxxxx maxdiff avgdiff maxreldiff avgreldiff"
print "unsorted", stats(a1)
print "sorted", stats(a2)
print "reverse", stats(a2r)
print "fpart", stats(a3)
print "fpart_r", stats(a3r)
print "afpart", stats(a4)
print "afpart_r", stats(a4r)
print "m2", stats(b1)
print "m2s", stats(b2)
print "tbest", stats(tbest)

if len(ints) < 10:
    for p in itertools.permutations(ints):
        print "xxx", stats(list(go(p)))


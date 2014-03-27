#!/bin/bash

mkdir {2..10}

for n in {2..10}; do for x in {1..100}; do perl -le "print int exp rand 9 for 1..$n" > $n/list_$x; done; done

for x in {2..10}; do for n in $(ls -v $x); do ../int-partitions-basic.py < $x/$n | ../stats.py ; done >$x.intp.log & done; wait
for x in {2..10}; do for n in $(ls -v $x); do ../rounder.py < $x/$n | ../stats.py ; done >$x.rounder.log & done; wait

for x in {2..10}; do
  echo -n "$x: ";
  paste $x.rounder.log $x.intp.log | awk '
    $1 > $3 {mr++};
    $1 < $3 {mi++};
    $1 == $3 {me++};
    $2 > $4 {ar++};
    $2 < $4 {ai++};
    $2 == $4 {ae++};
    END {print mr,me,mi " " ar,ae,ai}' OFS=:;
done 

for x in {2..10}; do
  echo -n "$x: ";
  paste $x.rounder.log $x.intp.log | awk '
    {mr+=$1;ar+=$2;mi+=$3;ai+=$4};
    END {print mr/NR,ar/NR,mi/NR,ai/NR}';
done | column -t


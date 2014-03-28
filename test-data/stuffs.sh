#!/bin/bash
set -e

cd "$(dirname "$0")"

if mkdir {2..10} 2>/dev/null; then
  for n in {2..10}; do for x in {1..100}; do perl -le "print int exp rand 9 for 1..$n" > $n/list_$x; done; done
fi

loggen () {
  if ! ls | grep -q "\.$2\.log$"; then
    for x in {2..10}; do for n in $(ls -v $x); do ../$1 < $x/$n | ../stats.py ; done >$x.$2.log & done; wait
  fi
}

loggen int-partitions-basic.py intp
loggen rounder.py rounder
loggen int-partitions-m3.py m3

# for x in {2..10}; do for n in $(ls -v $x); do ../int-partitions-basic.py < $x/$n | ../stats.py ; done >$x.intp.log & done; wait
# for x in {2..10}; do for n in $(ls -v $x); do ../rounder.py < $x/$n | ../stats.py ; done >$x.rounder.log & done; wait
# for x in {2..10}; do for n in $(ls -v $x); do ../int-partitions-m3.py < $x/$n | ../stats.py ; done >$x.m3.log & done; wait


vs () {
  echo "$1 vs $2:"
  echo
  { echo "n: m1 me m2 / a1 ae a2"
    for x in {2..10}; do
      echo -n "$x: ";
      paste $x.$1.log $x.$2.log | awk '
        BEGIN { m1=me=m2=a1=ae=a2=0 }
        $1 >  $3 {m1++};
        $1 == $3 {me++};
        $1 <  $3 {m2++};
        $2 >  $4 {a1++};
        $2 == $4 {ae++};
        $2 <  $4 {a2++};
        END {print m1,me,m2, "/", a1,ae,a2}'
    done 
  } | column -t

  echo

  { echo "n: m1a a1a m2a a2a m1m a1m m2m a2m"
    for x in {2..10}; do
      echo -n "$x: ";
      paste $x.$1.log $x.$2.log | awk '
        {m1+=$1;a1+=$2;m2+=$3;a2+=$4};
        $1 > m1m { m1m = $1 }
        $2 > a1m { a1m = $2 }
        $3 > m2m { m2m = $3 }
        $4 > a2m { a2m = $4 }
        END {
          print m1/NR,a1/NR,m2/NR,a2/NR, m1m,a1m,m2m,a2m
        }';
    done
  } | column -t
  echo
}

vs rounder intp
vs intp m3
vs rounder m3

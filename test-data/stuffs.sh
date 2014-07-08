#!/bin/bash
set -e

cd "$(dirname "$0")"

if mkdir {2..10} 2>/dev/null; then
  for n in {2..10}; do
  for x in {1..100}; do
    perl -le "print int exp rand 12 for 1..$n" > $n/list_$x;
  done;
  done
fi

loggen () {
  if ! ls | grep -q "\.$2\.log$"; then
    for x in {2..10}; do
      for n in $(ls -v $x); do
        ../$1 < $x/$n | ../stats.py
      done >$x.$2.log &
    done; wait
  fi
}

loggen int-partitions-basic.py intp
loggen rounder.py rounder
loggen rounder2.py rounder2
loggen int-partitions-m3.py m3
loggen tims.py tims

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
}

ma () {
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

ma2 () {
  echo "max-max, max-avg, avg-max, avg-avg:"
  for ((i=1;i<=$#;i++)); do
    echo "  $i = ${!i}"
  done
  echo
  { # n: lbl-mm lbl-ma lbl-am lbl-aa
    awk '
      BEGIN {
        printf "n:"
        for (i=1;i<ARGC;i++) { printf " %d-mm", i }
        for (i=1;i<ARGC;i++) { printf " %d-ma", i }
        for (i=1;i<ARGC;i++) { printf " %d-am", i }
        for (i=1;i<ARGC;i++) { printf " %d-aa", i }
        printf "\n"
      }' "$@"
    for x in {2..10}; do
      ll=( "${@/#/$x.}" )
      ll=( "${ll[@]/%/.log}" )
      echo -n "$x: ";
      awk '
        { m[ARGIND] += $1 }
        { a[ARGIND] += $2 }
        $1 > mm[ARGIND] { mm[ARGIND] = $1 }
        $2 > am[ARGIND] { am[ARGIND] = $2 }
        END {
          for (i=1;i<ARGC;i++) { printf " %s", mm[i]   }
          for (i=1;i<ARGC;i++) { printf " %f", m[i]/NR }
          for (i=1;i<ARGC;i++) { printf " %s", am[i]   }
          for (i=1;i<ARGC;i++) { printf " %f", a[i]/NR }
          printf "\n"
        }
        ' "${ll[@]}"
    done
  } | column -t
}

vs rounder intp
vs intp m3
vs rounder m3
vs rounder rounder2
vs rounder tims
vs tims m3

ma2 rounder intp m3 tims


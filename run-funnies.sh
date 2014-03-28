#!/bin/bash

cd "$(dirname "$0")"

for x in $(ls -v test-data/*/list_*); do
  ./funnies.py < $x | awk '{print x ": " $0}' x="$x";
done

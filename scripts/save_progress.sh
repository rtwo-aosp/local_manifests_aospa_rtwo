#!/bin/bash
MSG="${1:-WIP: port progress}"
DIRS="device/motorola/rtwo device/motorola/sm8550-common hardware/motorola kernel/motorola/sm8550 kernel/motorola/sm8550-devicetrees kernel/motorola/sm8550-modules vendor/aospa"
for d in $DIRS; do
  echo "== $d"
  git -C ~/aospa/$d checkout aospa
  git -C ~/aospa/$d add -A
  git -C ~/aospa/$d commit -m "$MSG"
  git -C ~/aospa/$d push -u isma aospa
done
echo "Listo"

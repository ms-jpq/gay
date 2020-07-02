#!/usr/bin/env bash

set -eu
set -o pipefail


cd "$(dirname "$0")" || exit 1


./gay -f -l
printf '\n\n'
./gay -f -g
printf '\n\n'
./gay -f -b
printf '\n\n'
./gay -f -t
printf '\n\n'
./gay -f -a
printf '\n\n'
./gay -f -p
printf '\n\n'
./gay -f -n
printf '\n\n'
./gay -f --gq


TEXT="$(< /dev/stdin)"
./gay -l -i 1d <<< "$TEXT"
./gay -l -i 2d <<< "$TEXT"
printf '\n\n'
./gay -g -i 1d <<< "$TEXT"
./gay -g -i 2d <<< "$TEXT"
printf '\n\n'
./gay -b -i 1d <<< "$TEXT"
./gay -b -i 2d <<< "$TEXT"
printf '\n\n'
./gay -t -i 1d <<< "$TEXT"
./gay -t -i 2d <<< "$TEXT"
printf '\n\n'
./gay -a -i 1d <<< "$TEXT"
./gay -a -i 2d <<< "$TEXT"
printf '\n\n'
./gay -p -i 1d <<< "$TEXT"
./gay -p -i 2d <<< "$TEXT"
printf '\n\n'
./gay -n -i 1d <<< "$TEXT"
./gay -n -i 2d <<< "$TEXT"
printf '\n\n'
./gay --gq -i 1d <<< "$TEXT"
./gay --gq -i 2d <<< "$TEXT"

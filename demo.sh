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
./gay -l <<< "$TEXT"
printf '\n\n'
./gay -g <<< "$TEXT"
printf '\n\n'
./gay -b <<< "$TEXT"
printf '\n\n'
./gay -t <<< "$TEXT"
printf '\n\n'
./gay -a <<< "$TEXT"
printf '\n\n'
./gay -p <<< "$TEXT"
printf '\n\n'
./gay -n <<< "$TEXT"
printf '\n\n'
./gay --gq <<< "$TEXT"

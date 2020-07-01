#!/usr/bin/env bash

set -eu
set -o pipefail


cd "$(dirname "$0")" || exit 1


if [[ $# -gt 0 ]]
then
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
else
  ./gay < ./gay
fi

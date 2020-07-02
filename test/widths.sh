#!/usr/bin/env bash

set -eu
set -o pipefail


COLS="$(tput cols)"

pr() {
  local txt="$1"
  printf '%s' "$txt"
}

ret() {
  printf '\n'
}

rep() {
  local num="$1"
  local ch="$2"
  local acc=''
  for ((i=0; i<COLS; i++))
  do
    acc="$acc$ch"
  done
  pr "$acc"
}


rep $((COLS - 1)) '-'
pr '王'
ret


rep $((COLS - 1)) '-'
pr '🏳️‍🌈'
ret
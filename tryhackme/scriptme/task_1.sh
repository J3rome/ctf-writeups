#!/bin/bash

TO_DECODE="$(cat tsk1_base64_50times.txt)"

for i in {1..50};do
	TO_DECODE="$(echo ${TO_DECODE} | base64 -d)"
done

echo ${TO_DECODE}
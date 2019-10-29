#!/bin/bash

dataset=(ml1m)
for i in 0
do
    python3 prepro.py ${dataset[$index]}
done

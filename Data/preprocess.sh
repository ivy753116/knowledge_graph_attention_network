#!/bin/bash

dataset=(ml1m_0.75)
for i in 0
do
    python3 prepro.py ${dataset[$index]}
done

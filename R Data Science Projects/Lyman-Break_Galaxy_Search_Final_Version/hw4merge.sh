#!/bin/bash

echo '"distance","spectrumID","i"' > hw4best100.csv

tail -n +2 -q *.csv | grep -v '^Inf,' | sort -n -t, -k1 | head -n 100 >> hw4best100.csv


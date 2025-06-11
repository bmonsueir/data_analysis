#!/bin/sh
export MPLBACKEND=Agg 
export QT_QPA_PLATFORM=offscreen
python unit_tests.py ${@}
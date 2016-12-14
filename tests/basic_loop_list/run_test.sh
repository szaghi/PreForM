#!/usr/bin/env bash

rm -f *.f90 *.o
PreForM.py basic_loop_list.pfm -o basic_loop_list.f90
gfortran -c basic_loop_list.f90

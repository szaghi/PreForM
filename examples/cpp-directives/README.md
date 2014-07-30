# PreForM.py example of the supported `cpp` preprocessing directives

A KISS usage example of PreForM.py

## Description

This example consists of a very simple Fortran program, _cpp-directives.F90_  (which includes _foo.inc_). This program shows a complete list of the `cpp` preprocessing directives currently supported, just open the source file and read the code. 

For testing the example type the followings statement

```bash
PreForM.py cpp-directives.F90
```
This will print to stdout the preprocessed source file, line by line. If all goes right, you should read a sequence of prints similar to _Ok, ... this works!_, otherwise something similar to _No, something is wrong!_. If you want to test a real compilation of the preprocessed source you can type something similar to the following statement (that redirect the output to a temporary file)
```bash
PreForM.py cpp-directives.F90 -o cpp-directives.pfm.f90 ; YOUR-COMPILER cpp-directives.pfm.f90 ; rm -f cpp-directives.pfm.f90
```
where `YOUR-COMPILER` is your preferred Fortran compiler (e.g `gfortran` or `ifort`).

# PreForM.py example of the Template System Usage

A KISS usage example of PreForM.py

## Description

This directory contains examples of PreForM.py usage as Template System.

### Simple pairs loop control

The file `simple-for-loop.f90` contains an example of `#PFM for EXPRESSION`-`#PFM endfor` pairs loop control. This `#PFM` directive is particularly useful for automate the generation of blocks of differing for only small part such as a variable type (kind or shape), etc. In the example reported the `#PFM for EXPRESSION` is used for build a generic `interface` for handling 3 different derived types. As an example the snippet
```fortran
...
interface less_than
  #PFM for i in range(3):
  module procedure less_than_type_$i
  #PFM endfor
endinterface
...
```
is used for generate (after the pre-processing)
```fortran
...
interface less_than
  module procedure less_than_type_1
  module procedure less_than_type_2
  module procedure less_than_type_3
endinterface
...
```
It is worth noting that the counter `i` is expanded if it is prefixed with a `$`. The expression of the `for` loop is any valid Python iteration-expression. Presently the only constrain is that the expression as only one counter (named as you want, not necessarly `i`, but rember that it is case sensitive). 

Note also that the `#PFM for EXPRESSION`-`#PFM endfor` pairs can be combined (and nested) with `cpp` macros.

### Complex pairs loop control
To be written.

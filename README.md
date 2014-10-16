[![Build Status](https://travis-ci.org/szaghi/PreForM.png)](https://travis-ci.org/szaghi/PreForM)
[![Latest Version](https://pypip.in/version/PreForM.py/badge.svg)](https://pypi.python.org/pypi/PreForM.py/)
[![Downloads](https://pypip.in/download/PreForM.py/badge.svg)](https://pypi.python.org/pypi/PreForM.py/)
[![Supported Python versions](https://pypip.in/py_versions/PreForM.py/badge.svg)](https://pypi.python.org/pypi/PreForM.py/)
[![Development Status](https://pypip.in/status/PreForM.py/badge.svg)](https://pypi.python.org/pypi/PreForM.py/)
[![License](https://pypip.in/license/PreForM.py/badge.svg)](https://pypi.python.org/pypi/PreForM.py/)

# PreForM.py
### <a name="top">PreForM.py,  Preprocessor for Fortran poor Men
A very simple and stupid preprocessor for modern Fortran projects. 

PreForM.py supports the most used `cpp` pre-processing directives and provides advanced features typical of templating systems. Even if PreForM.py is currently Fortran-agnostic (it being usable within any programming languages) it is focused on Fortran programming language.

## <a name="toc">Table of Contents
* [Team Members](#team-members)
    + [Contributors](#contributors)
* [Why?](#why)
    + [Why not use cpp?](#cpp)
* [Main features](#main-features)
* [Todos](#todos)
* [Requirements](#requirements)
* [Install](#install)
    + [Manual Installation](#manual-install)
    + [PyPI Installation, the Python Package Index](#pip-install)
* [Getting Help](#help)
* [Copyrights](#copyrights)
* [Usage](#usage)
    + [Pre-process a file on-the-fly to stdout](#preprocess-fly)
    + [Pre-process a file and save result to a file](#preprocess-tofile)
    + [Defines MACROS from CLI](#cli-macro)
* [Examples](#examples)
* [Tips for non pythonic users](#tips)
* [Version History](#versions)

## <a name="team-members"></a>Team Members
* Stefano Zaghi, aka _szaghi_ <https://github.com/szaghi>

### <a name="contributors"></a>Contributors
* Tomas Bylund, aka _Tobychev_ <https://github.com/Tobychev>

Go to [Top](#top) or [Toc](#toc)
## <a name="why"></a>Why?
The Fortran programming language has not its own pre-processor neither it has a standard pre-processing syntax. Consequently, Fortran developers must rely on external pre-processor tools. However, the pre-processors focused on Fortran language are very fews: PreForM.py is just anther Pythonic pre-processor designed with only main target, the _Fortran poor-men_. 

It is designed to be very simple, but flexible enough to constitute a _template system_ for Fortran developers. Moreover, to facilitate the migration from other pre-processors, PreForM.py supports the most used _cpp_ pre-processing directives. 

It is worth noting that PreForM.py even if it is designed for _Fortran poor-men_ is presently Fortran-agnostic, as a consequence it can be used within any programming language. 

### <a name="cpp"></a>Why not use cpp?
As a matter of fact, many Fortran developers use _cpp_, the C pre-processor, being one of the most diffused and standardised pre-processor. _cpp_ is a great pre-processor, but it is basically a _macro processor_, meaning that it is quite focused on _macro expansion/substitution/evaluation_. _cpp_ has some limitations that makes complex using it as a template system. Let us suppose we want to write a generic interface as the following:

```fortran
...
interface foo
  module procedure foo1
  module procedure foo2
  module procedure foo3
endinterface
contains
  function foo1(in) result(out)
  type(first), intent(IN):: in
  logical:: out
  out = in%logical_test()
  endfunction foo1

  function foo2(in) result(out)
  type(second), intent(IN):: in
  logical:: out
  out = in%logical_test()
  endfunction foo2

  function foo3(in) result(out)
  type(third), intent(IN):: in
  logical:: out
  out = in%logical_test()
  endfunction foo3
...
```
Writing a _macro_ in _cpp_ syntax to _generalize_ such a generic interface implementation is quite impossible. On the contrary, using PreForM.py as a template system the implementation becomes very simple and elegant:
```fortran
...
interface foo
  #PFM for i in [1,2,3]:
  module procedure foo$i
  #PFM endfor
endinterface
contains
  #PFM for i in [1,2,3] and t in [first,second,third]:
  function foo$i(in) result(out)
  type($t), intent(IN):: in
  logical:: out
  out = in%logical_test()
  endfunction foo$i
  #PFM endfor
```

PreForM.py is just a pre-processor for Fortran poor-men supporting the most used _cpp_ directives, but overtaking some of the _cpp_ limitations in order to make PreForM.py similar to a template system. 

Go to [Top](#top) or [Toc](#toc)
## <a name="main-features"></a>Main features
+ Easy-extensible: PreForM.py is just a less-than 500 lines of Python statements... no bad for a poor-cpp-preprocessor improvement;
+ well integrated with a powerful yet simple automatic Building System for Fortran poor-men, namely [FoBiS.py](https://github.com/szaghi/FoBiS);
+ simple command line interface;
+ support the most used `cpp` pre-processing directives:
  + conditionals:
      + operators (also nested):
        * [x] `defined MACRO` or `defined(MACRO)`;
        * [x] `EXPRESSION || EXPRESSION` (logic or);
        * [x] `EXPRESSION && EXPRESSION` (logic and);
    * [x] `#if EXPRESSION`;
    * [x] `#elif EXPRESSION`;
    * [x] `#ifdef MACRO`;
    * [x] `#ifndef MACRO`;
    * [x] `#else`;
    * [x] `#endif`;
  + macros:
    + standard predefined macros:
      * [x] `__FILE__`;
      * [x] `__LINE__`;
      * [x] `__DATE__`;
      * [x] `__TIME__`;
    * [x] expansion;
    * [x] stringification;
    * [x] concatenation;
    * [x] variadic macros;
    + object-like macros:
      * [x] `#define MACRO [VALUE]`, VALUE is optional;
    + function-like macros:
      * [x] `#define FUNCTION FUNCTION_DEFINITION`;
    * [x] `#undef`;
  + [x] `#include`;
+ pythonic Template System:
  * [x] `#PFM for EXPRESSION`-`#PFM endfor` pairs loop control (only for one iteration counter at time;
+ ...

Note that in general the `cpp` pre-processing directives should start at the first column, the symbol `#` being the first one. PreForM.py relaxes this rule allowing any number of leading white spaces before `#`.

Go to [Top](#top) or [Toc](#toc)
## <a name="todos"></a>Todos
+ Pythonic Template System;
  * [ ] `#PFM for EXPRESSION`-`#PFM endfor` pairs loop control for complex EXPRESSION;
+ any feature request is welcome.

Go to [Top](#top) or [Toc](#toc)
## <a name="requirements"></a>Requirements
+ Python 2.7+ or Python 3.x;
    + required modules:
        + sys;
        + os;
        + argparse;
        + configparser;
        + re;
    + optional modules:
        + datetime;
        + multiprocessing;
+ a lot of patience with the author.

PreForM.py is developed on a GNU/Linux architecture. For Windows architecture there is no support, however it should work out-of-the-box.

Go to [Top](#top) or [Toc](#toc)
## <a name="install"></a>Install

### <a name="manual-install"></a>Manual Installation
PreForM.py is a one-file-script, consequently it does not need a real installation: simply download the script and placed into your PATH. See the [requirements](#requirements) section.

However, note that the script placed into the root of PreForM.py project is just a wrapper to the real script. As a matter of fact, the tree structure of the PreForM.py project is the following:
```bash
├── CONTRIBUTING.md
├── examples
│   ├── cpp-directives
│   │   ├── cpp-directives.F90
│   │   ├── foo.inc
│   │   └── README.md
│   └── template-system
│       ├── README.md
│       └── simple-for-loop.f90
├── LICENSE.gpl3.md
├── PreForM
│   ├── __init__.py
│   ├── __main__.py
│   └── PreForM.py
├── PreForM.py
├── README.md
└── setup.py
```
Therefore, the actual script that you need to download is `PreForM/PreForM.py `. This cumbersome files tree is necessary to create a valid `PyPI egg`, see PyPI [install](#pip-install) procedure.

It can be convenient to _clone_ the project:
```bash
git clone https://github.com/szaghi/PreForM
```
and then make a link to the script where your environment can find it.

### <a name="pip-install"></a>Using, PyPI the Python Package Index
PreForM.py can be installed by means of `pip`, the python installer that search into the PyPI (Python Package Index) for packages and automatically install them. Just type:
```bash
pip install PreForM.py
```
Note that you need root permissions if you are not using your virtualenv or you are trying to install PreForM.py into your system space.

It is worth noting that the `pip` installation will create a command line tool named `PreForM` and not `PreForM.py`: take this into account when using PreForM.py.

It is also worth noting that the `pip` installation will allow you to directly import PreForM.py code into your Python application by means of module import, e.g.
```python
from PreForM.PreForM import preprocess_file 
```
will import the `preprocess_file` function into your python application.

Go to [Top](#top) or [Toc](#toc)
## <a name="help"></a>Getting Help]
You are reading the main documentation of PreForM.py that should be comprehensive. For more help contact directly the [author](stefano.zaghi@gmail.com). 

Go to [Top](#top) or [Toc](#toc)
## <a name="Copyrights"></a>Copyrights
PreForM.py is an open source project, it is distributed under the [GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) license. A copy of the license should be distributed within PreForM.py. Anyone interested to use, develop or to contribute to PreForM.py is welcome. Take a look at the [contributing guidelines](CONTRIBUTING.md) for starting to contribute to the project.

Go to [Top](#top) or [Toc](#toc)
## <a name="usage"></a>Usage
Printing the main help message:
```bash
PreForM.py -h
```
This will echo:
```bash
usage: PreForM.py [-h] [-v] [-o OUTPUT] [-D D [D ...]] [-lm] input

PreForM.py, Preprocessor for Fortran poor Men

positional arguments:
  input                 Input file name of source to be preprocessed

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show version
  -o OUTPUT, --output OUTPUT
                        Output file name of preprocessed source
  -D D [D ...]          Define a list of macros in the form NAME1=VALUE1
                        NAME2=VALUE2...
  -lm, --list-macros    Print the list of macros state as the last parsed line
                        left it
```
### <a name="preprocess-fly"></a>Pre-process a file on-the-fly to stdout
```bash
PreForM.py my_file_to_be_preprocessed.my_extension
```
This will print to stdout the pre-processed file.
### <a name="preprocess-tofile"></a>Pre-process a file and save result to a file
```bash
PreForM.py my_file_to_be_preprocessed.my_extension -o my_result_file
```
This will save into `my_result_file` the pre-processed file.

### <a name="cli-macro"></a>Defines MACROS from CLI
It is possible to define macros on-the-fly using the CLI switch `-D`. As an example
```bash
PreForM.py my_source.f90 -D first=1 second=sec third=.true.
```
pre-process the source file `my_source.f90` defining on-the-fly 3 macros, `first,second,third`, having the values `1,'sec',.true.`, respectively. The syntax is `macro_name=macro_value`. In case you want just define a macro name (without take into account for its value) you must always insert the symbol `=`, e.g.
```bash
PreForM.py my_source.f90 -D first= second=2
```
This defines 2 macros, `first,second`, but `second` only has a true value (`2`), whereas `first` is only _defined_, but it has not a value.

Go to [Top](#top) or [Toc](#toc)
## <a name="examples"></a>Examples
Into the directory _examples_ there are some KISS examples, just read their provided _REAMDE.md_.

Go to [Top](#top) or [Toc](#toc)
## <a name="tips"></a>Tips for non pythonic users
In the examples above PreForM.py is supposed to have the executable permissions, thus it is used without an explicit invocation of the Python interpreter. In general, if PreForM.py is not set to have executable permissions, it must be executed as:

```bash
python PreForM.py ...
```
Go to [Top](#top) or [Toc](#toc)
## <a name="versions"></a>Version History
In the following the changelog of most important releases is reported.
### v1.1.0 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/v1.1.0.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/v1.1.0.tar.gz) one
Add PyPI installation procedure. Strongly modify the project tree. Fully backward compatible.
### v1.0.0 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/v1.0.0.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/v1.0.0.tar.gz) one
First STABLE release. Implement `#PFM for EXPRESSION`-`#PFM endfor` pairs loop control for only simple expressions (i.e. expression having only one iteration counter). Fully backward compatible.
### v0.0.4 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/v0.0.4.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/v0.0.4.tar.gz) one
`CPP` Support almost complete. The most used `cpp` pre-processing directives are now supported. Fully backward compatible.
### v0.0.3 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/v0.0.3.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/v0.0.3.tar.gz) one
Implement function-like macros substitution. Fully backward compatible.
### v0.0.2 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/v0.0.2.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/v0.0.2.tar.gz) one
_Quasi_ stable API, with many _cpp_ directives supported. Fully backward compatible.
### v0.0.1 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/v0.0.1.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/v0.0.1.tar.gz) one
Very first, totally UNSTABLE release. Implement only few cpp directives.

Go to [Top](#top) or [Toc](#toc)

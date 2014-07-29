# PreForM.py
### <a name="top">PreForM.py,  Preprocessor for Fortran poor Men
A very simple and stupid preprocessor for modern Fortran projects.

## <a name="toc">Table of Contents
* [Team Members](#team-members)
    + [Contributors](#contributors)
* [Why?](#why)
    + [Why not use cpp?](#cpp)
* [Main features](#main-features)
* [Todos](#todos)
* [Requirements](#requirements)
* [Install](#install)
* [Getting Help](#help)
* [Copyrights](#copyrights)
* [Usage](#usage)
    + [Preprocess a file on-the-fly to stdout](#preprocess-fly)
    + [Preprocess a file and save result to a file](#preprocess-tofile)
* [Examples](#examples)
* [Tips for non pythonic users](#tips)
* [Version History](#versions)

## <a name="team-members"></a>Team Members
* Stefano Zaghi, aka _szaghi_ <https://github.com/szaghi>

### <a name="contributors"></a>Contributors
* Tomas Bylund, aka _Tobychev_ <https://github.com/Tobychev>

Go to [Top](#top) or [Toc](#toc)
## <a name="why"></a>Why?
The Fortran programming language has not its own pre-processor neither it has a standard pre-processing syntax. Consequently, Fortran developers must rely on external pre-processor tool. However, the pre-processors focused on Fortran language are very fews: PreForM.py is just anther Pythonic pre-processor designed with only main target, the _Fortran poor-men_. It is designed to be very simple, but flexible enough to constitute a _template system_ for Fortran developers. Moreover, to facilitate the migration from other pre-processors, PreForM.py support many _cpp_ pre-processing directives.

### <a name="cpp"></a>Why not use cpp?
As a matter of fact, many Fortran developers use _cpp_, the C pre-processor, being one of the most diffused and standardised pre-processor. _cpp_ is a great pre-processor, but is basically a _macro processor_, meaning that it is quite focused on _macroexpansion/substitution/evaluation_. _cpp_ has some limitations that makes complex using it as a template system. Let us suppose we want to write a generic interface as the following:

```fortran
...
interface foo
  module procedure foo1,foo2,foo3
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
  module procedure foo1,foo2,foo3
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

PreForM.py is just a pre-processor for Fortran poor-men supporting a sub-set of _cpp_ directives, but overtaking some of _cpp_ limitations making PreForM.py similar to a template system. 

Go to [Top](#top) or [Toc](#toc)
## <a name="main-features"></a>Main features
+ Support for `cpp` preprocessing directives:
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
    * [ ] stringification;
    * [ ] concatenation;
    * [ ] variadic macros;
    + object-like macros:
      * [x] `#define MACRO [VALUE]`, VALUE is optional;
    + function-like macros:
      * [x] `#define FUNCTION FUNCTION_DEFINITION`;
    * [x] `#undef`;
  + [x] `#include`;
+ Pythonic Templating System:
  * [ ] `#PFM for EXPRESSION` loop control;
+ ...

Go to [Top](#top) or [Toc](#toc)
## <a name="todos"></a>Todos
+ Almost all!
+ ...

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
        + multiprocessing;
+ a lot of patience with the author.

PreForM.py is developed on a GNU/Linux architecture. For Windows architecture there is no support, however it should work out-of-the-box.

Go to [Top](#top) or [Toc](#toc)
## <a name="install"></a>Install
The installation is very simple: put PreForM.py in your path or execute it using full path. See the [requirements](#requirements) section.

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
### <a name="preprocess-fly"></a>Preprocess a file on-the-fly to stdout
```bash
PreForM.py my_file_to_be_preprocessed.my_extension
```
This will echoed to stdout the result of pre-processing the input file.
### <a name="preprocess-tofile"></a>Preprocess a file and save result to a file
```bash
PreForM.py my_file_to_be_preprocessed.my_extension -o my_result_file
```
This will save into `my_result_file` the result of pre-processing the input file.

Go to [Top](#top) or [Toc](#toc)
## <a name="examples"></a>Examples
To be written.

Go to [Top](#top) or [Toc](#toc)
## <a name="tips"></a>Tips for non pythonic users
In the examples above PreForM.py is supposed to have the executable permissions, thus it is used without an explicit invocation of the Python interpreter. In general, if PreForM.py is not set to have executable permissions, it must be executed as:

```bash
python PreForM.py ...
```
Go to [Top](#top) or [Toc](#toc)
## <a name="versions"></a>Version History
In the following the changelog of most important releases is reported.
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

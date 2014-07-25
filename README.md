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
* [Examples](#examples)
* [Tips for non pythonic users](#tips)
* [Version History](#versions)

## <a name="team-members"></a>Team Members
* Stefano Zaghi, aka _szaghi_ <https://github.com/szaghi>

### <a name="contributors"></a>Contributors
* Tomas Bylund, aka _Tobychev_ <https://github.com/Tobychev>

Go to [Top](#top) or [Toc](#toc)
## <a name="why"></a>Why?
To be written.
### <a name="cpp"></a>Why not use cpp?
To be written.

Go to [Top](#top) or [Toc](#toc)
## <a name="main-features"></a>Main features
+ Support for cpp preprocessing directives:
  [+] `#ifdef-#else-#endif`;
  [ ] `#ifndef-#else-#endif`;
  [ ] `#if-#elif-#else-#endif`;
  [+] `#define`;
  [+] `#undef`;
  [ ] `#include`;
+ Pythonic Templating System;
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
usage: PreForM.py [-h] [-v] [-o OUTPUT] [-D D [D ...]] input

PreForM.py, Preprocessor for Fortran poor Men

positional arguments:
  input                 Input file name of source to be preprocessed

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show version
  -o OUTPUT, --output OUTPUT
                        Output file name of preprocessed source
  -D D [D ...]          List of defined macros in the form NAME1=VALUE1
                        NAME2=VALUE2...
```

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
### 0.0.1 
##### Download [ZIP](https://github.com/szaghi/PreForM/archive/0.0.1.zip) ball or [TAR](https://github.com/szaghi/PreForM/archive/0.0.1.tar.gz) one
Very first, totally UNSTABLE release. Implement only few cpp directives.

Go to [Top](#top) or [Toc](#toc)

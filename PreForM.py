#!/usr/bin/env python
"""
PreForM.py, Preprocessor for Fortran poor Men
"""
__appname__ = 'PreForM.py'
__version__ ="0.0.1"
__author__  = 'Stefano Zaghi'
# modules loading
import sys
try:
  import os
except:
  print("Module 'os' not found")
  sys.exit(1)
try:
  import argparse
except:
  print("Module 'argparse' not found")
  sys.exit(1)
try:
  import re
except:
  print("The regular expression module 're' not found")
  sys.exit(1)
try:
  from multiprocessing import Pool
  parallel=True
except:
  print("Module 'multiprocessing' not found: parallel compilation disabled")
  parallel=False
# setting CLI
cliparser = argparse.ArgumentParser(prog=__appname__,description='PreForM.py, Preprocessor for Fortran poor Men')
cliparser.add_argument('-v','--version',               action='version',                       help='Show version',version='%(prog)s '+__version__)
cliparser.add_argument('input',                        action='store',            default=None,help='Input file name of source to be preprocessed')
cliparser.add_argument('-o','--output', required=False,action='store',            default=None,help='Output file name of preprocessed source')
cliparser.add_argument('-D',            required=False,action='store',  nargs='+',default=[],  help='List of defined macros in the form NAME1=VALUE1 NAME2=VALUE2...')
#regular expressions
# cpp directives
cpp_macro = r"(?P<cpp_macro>.*)"
regex_cpp_cond_if      = re.compile(r"(?P<cpp_if>^#[Ii][Ff])\s+"+cpp_macro)
regex_cpp_cond_ifdef   = re.compile(r"(?P<cpp_ifdef>^#[Ii][Ff][Dd][Ee][Ff])\s+"+cpp_macro)
regex_cpp_cond_ifndef  = re.compile(r"(?P<cpp_ifndef>^#[Ii][Ff][Nn][Dd][Ee][Ff])\s+"+cpp_macro)
regex_cpp_cond_elif    = re.compile(r"(?P<cpp_elif>^#[Ee][Ll][Ii][Ff])\s+"+cpp_macro)
regex_cpp_cond_else    = re.compile(r"(?P<cpp_else>^#[Ee][Ll][Ss][Ee])\s+"+cpp_macro)
regex_cpp_cond_endif   = re.compile(r"(?P<cpp_endif>^#[Ee][Nn][Dd][Ii][Ff]).*")
regex_cpp_cond_defined = re.compile(r"(?P<cpp_defined>^#[Dd][Ee][Ff][Ii][Nn][Ee][Dd])\s+.*")
regexs_cpp_cond = {}
for k, v in locals().items():
  if re.match(r"^regex_cpp_cond_.*",k):
    regexs_cpp_cond[k] = v
regex_cpp_define = re.compile(r"(?P<cpp_define>^#[Dd][Ee][Ff][Ii][Nn][Ee])\s+"+cpp_macro)
regex_cpp_undef  = re.compile(r"(?P<cpp_undef>^#[Uu][Nn][Dd][Ee][Ff])\s+"+cpp_macro)
regexs_cpp = {}
for k, v in locals().items():
  if not re.match(r"^regex_cpp_cond_.*",k) and re.match(r"^regex_cpp_.*",k):
    regexs_cpp[k] = v
# functions definitions
# classes definitions
class Macros(object):
  """
  Macros is an object that handles defined and non defined macros, their attributes and methods.
  """
  def __init__(self,dic={}):
    self.dic = dic
  def is_def(self,macro):
    """
    Method for checking if a macro is presently defined.
    """
    result = False
    for k, v in self.dic.items():
      if macro == k:
        if v is not None:
          result = True
          return result
    return result
  def list(self):
    """
    Method for printing the list of macros.
    """
    print('Defined macros')
    for k, v in self.dic.items():
      if v is not None:
        print(k+': '+str(v))
    print('Undefined macros')
    for k, v in self.dic.items():
      if v is None:
        print(k)
  def get_from_CLI(self,macros=[]):
    """
    Method for getting macros defined from CLI.
    """
    if len(macros)>0:
      for m in macros:
        self.dic[m.split('=')[0]]=m.split('=')[1]
  def get_from_cpp(self,macro=''):
    """
    Method for getting macro defined from cpp 'define'.
    """
    macro_split = macro.split(' ')
    if len(macro_split)>1:
      self.dic[macro_split[0]]=macro_split[1]
    else:
      self.dic[macro_split[0]]=''
  def undef(self,macro_name=''):
    """
    Method for undefine a macro.
    """
    if macro_name != '':
      self.dic[macro_name]=None
class Conditional(object):
  """
  Conditional is an object that handles conditional directive, its attributes and methods.
  """
  def __init__(self,inside=False,condition=[]):
    self.inside = inside
    self.condition = condition
class Parsed_Line(object):
  """
  Parsed_Line is an object that handles a parsed line, its attributes and methods.
  """
  def __init__(self,line='',cpp=False,conditional=False,define_macro=False,undef_macro=False,output=True):
    self.line         = line
    self.cpp          = cpp
    self.conditional  = conditional
    self.define_macro = define_macro
    self.undef_macro  = undef_macro
    self.output       = output
  def cpp_check(self,macros,conditional):
    """
    Method for checking if line contains cpp directives.
    """
    for k, v in regexs_cpp.items():
      matching = re.search(v,self.line)
      if matching:
        self.cpp    = True
        self.output = False
        if k == 'regex_cpp_define':
          self.define_macro = True
          matching = re.match(v,self.line)
          macro    = matching.group('cpp_macro')
          macros.get_from_cpp(macro=macro)
        elif k == 'regex_cpp_undef':
          self.undef_macro = True
          matching = re.match(v,self.line)
          macro    = matching.group('cpp_macro')
          macros.undef(macro_name=macro)
        return
    for k, v in regexs_cpp_cond.items():
      matching = re.search(v,self.line)
      if matching:
        self.cpp         = True
        self.output      = False
        self.conditional = True
        if k == 'regex_cpp_cond_if' or k == 'regex_cpp_cond_ifdef' or k == 'regex_cpp_cond_ifndef':
          matching = re.match(v,self.line)
          macro    = matching.group('cpp_macro')
          conditional.inside    = True
          conditional.condition = []
          conditional.condition.append(k.split('regex_cpp_cond_')[1])
          conditional.condition.append(macro)
          conditional.condition.append('check')
        if k == 'regex_cpp_cond_else':
          conditional.inside    = True
          if len(conditional.condition)==3:
            if conditional.condition[2]=='ifdef':
              conditional.condition = []
              conditional.condition.append(k.split('regex_cpp_cond_')[1])
              conditional.condition.append('')
              conditional.condition.append('ifdef')
        elif k == 'regex_cpp_cond_endif':
          conditional.inside    = False
          conditional.condition = []
        return
    return
  def output_check(self,macros,conditional):
    """
    Method for checking if line is output line or not.
    """
    if conditional.inside:
      if conditional.condition[2]== 'check':
        if conditional.condition[0]== 'ifdef':
          if macros.is_def(macro=conditional.condition[1]):
            self.output = True
            conditional.condition[2] = 'ifdef'
          else:
            self.output = False
            conditional.condition[2] = 'else'
      elif conditional.condition[0]== 'else':
        if conditional.condition[2] == 'ifdef':
          self.output = False
        else:
          self.output = True
  def parse(self,macros,conditional):
    """
    Method for parsing a line.
    """
    self.cpp_check(macros=macros,conditional=conditional)
    if conditional.inside and not self.cpp:
      self.output_check(macros=macros,conditional=conditional)
    if self.output:
      return self.line
    else:
      return None
# main loop
if __name__ == '__main__':
  cliargs = cliparser.parse_args()
  macros = Macros()
  macros.get_from_CLI(macros=cliargs.D)
  if cliargs.input:
    if cliargs.output:
      parsed_file = open(cliargs.output,'w')
    source_file = open(cliargs.input,'r')
    conditional = Conditional()
    for line in source_file:
      pline = Parsed_Line(line=line)
      output = pline.parse(macros=macros,conditional=conditional)
      if output:
        if cliargs.output:
          parsed_file.writelines(output)
        else:
          print(output),
    if cliargs.output:
      parsed_file.close()
    source_file.close()

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
cliparser.add_argument('-v','--version',                    action='version',                           help='Show version',version='%(prog)s '+__version__)
cliparser.add_argument('input',                             action='store',               default=None, help='Input file name of source to be preprocessed')
cliparser.add_argument('-o','--output',      required=False,action='store',               default=None, help='Output file name of preprocessed source')
cliparser.add_argument('-D',                 required=False,action='store',     nargs='+',default=[],   help='Define a list of macros in the form NAME1=VALUE1 NAME2=VALUE2...')
cliparser.add_argument('-lm','--list-macros',required=False,action='store_true',          default=False,help='Print the list of macros state as the last parsed line left it')
#regular expressions
name = r"(?P<name>[a-zA-Z][a-zA-Z0-9_]*)"
macro = r"(?P<macro>[a-zA-Z][a-zA-Z0-9_]*(|\(.*\)))"
expr = r"(?P<expr>.*)"
regex_function = re.compile(name+r"\("+expr+r"\).*")
# cpp directives
regex_cpp_define  = re.compile(r"(?P<cpp_define>#[Dd][Ee][Ff][Ii][Nn][Ee])\s+"+macro+r"\s+"+expr)
regex_cpp_undef   = re.compile(r"(?P<cpp_undef>#[Uu][Nn][Dd][Ee][Ff])\s+"+macro)
regex_cpp_include = re.compile(r"(?P<cpp_include>#[Ii][Nn][Cc][Ll][Uu][Dd][Ee])\s+"+r"(?P<fname>.*)")
regexs_cpp = {}
for k, v in locals().items():
  if not re.match(r"^regex_cpp_cond_.*",k) and re.match(r"^regex_cpp_.*",k):
    regexs_cpp[k] = v
# cpp conditional directives
regex_cpp_cond_if          = re.compile(r"(?P<cpp_if>#[Ii][Ff])\s+"+expr)
regex_cpp_cond_ifdef       = re.compile(r"(?P<cpp_ifdef>#[Ii][Ff][Dd][Ee][Ff])\s+"+macro)
regex_cpp_cond_ifndef      = re.compile(r"(?P<cpp_ifndef>#[Ii][Ff][Nn][Dd][Ee][Ff])\s+"+macro)
regex_cpp_cond_elif        = re.compile(r"(?P<cpp_elif>#[Ee][Ll][Ii][Ff])\s+"+expr)
regex_cpp_cond_else        = re.compile(r"(?P<cpp_else>#[Ee][Ll][Ss][Ee])\s*")
regex_cpp_cond_endif       = re.compile(r"(?P<cpp_endif>#[Ee][Nn][Dd][Ii][Ff]).*")
regex_cpp_cond_defined     = re.compile(r"(?P<cpp_defined>[Dd][Ee][Ff][Ii][Nn][Ee][Dd])"+"(\s+|\()"+macro+r"(|\))")
regex_cpp_cond_defined_kwd = re.compile(r"(?P<cpp_defined>[Dd][Ee][Ff][Ii][Nn][Ee][Dd])")
regexs_cpp_cond = {}
for k, v in locals().items():
  if re.match(r"^regex_cpp_cond_.*",k):
    regexs_cpp_cond[k] = v
# pre-defined macros
try:
  from datetime import datetime
  now = datetime.now()
  __date__ = now.strftime('%b %d %Y')
  __time__ = now.strftime('%X')
except:
  __date__ = ''
  __time__ = ''
predef_macro = {'__FILE__':'','__LINE__':'','__DATE__':__date__,'__TIME__':__time__}
# classes definitions
class Macros(object):
  """
  Macros is an object that handles defined and non defined macros, their attributes and methods.
  """
  def __init__(self,dic=predef_macro):
    self.dic = dic
  def set(self,macro,value):
    self.dic[macro] = value
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
  def is_undef(self,macro):
    """
    Method for checking if a macro is not presently defined.
    """
    result = True
    for k, v in self.dic.items():
      if macro == k:
        if v is not None:
          result = False
          return result
    return result
  def expand(self,expression):
    """
    Method for expandind defined macros present into the expression.
    """
    for k, v in self.dic.items():
      if v is not None:
        if '(' in k or ')' in k:
          # function-like macro
          matching = re.match(regex_function,k)
          if matching:
            fname  = matching.group('name')             # function name
            vnames = matching.group('expr').split(',')  # variables names
            if fname in expression:
              for matching in re.finditer(regex_function,expression):
                if matching:
                  avnames = matching.group('expr').split(',')  # actual variables names
                  # substituting first variables names
                  expr = v
                  for var,vname in enumerate(vnames):
                    expr = expr.replace(vname,avnames[var])
                  # substituting leftmost match
                  expression = re.sub(regex_function,expr,expression)
        else:
          # object-like macro
          expression = expression.replace(k,v)
    return expression
  def evaluate(self,expression):
    """
    Method for evaluating a conditional expression accordingly to the current macros state.
    """
    expression_processed = expression
    # check for "defined" operators
    defined = re.findall(regex_cpp_cond_defined,expression)
    for d in defined:
      expression_processed = expression_processed.replace(d[2],str(self.is_def(d[2])))
      expression_processed = re.sub(regex_cpp_cond_defined_kwd,'',expression_processed)
    # check for "or" and "and" operators
    expression_processed = expression_processed.replace('||',' or ')
    expression_processed = expression_processed.replace('&&',' and ')
    # expand macros
    expression_processed = self.expand(expression=expression_processed)
    try:
      result = eval(expression_processed)
    except:
      print('Error: conditional expression not correctly evaluated!')
      print('Original expression: '+expression)
      print('Processed expression: '+expression_processed)
      self.list()
      sys.exit(1)
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
  def get_from_cpp(self,macro,expr):
    """
    Method for getting macro defined from cpp 'define'.
    """
    self.dic[macro]=expr
  def undef(self,macro_name=''):
    """
    Method for undefine a macro.
    """
    if macro_name != '':
      self.dic[macro_name]=None
class State(object):
  """
  State is an object that handles the state of the current parsed line, their attributes and methods.
  """
  def __init__(self,
               action='print', # action = 'include','print','omit'
               scope='normal', # scope  = 'normal', 'print','omit'
               include=''):    # include file
    self.action  = action
    self.scope   = scope
    self.include = include
class Parsed_Line(object):
  """
  Parsed_Line is an object that handles a parsed line, its attributes and methods.
  """
  def __init__(self,line=''):
    self.line = line
  def preproc_check(self,macros,state):
    """
    Method for checking if line contains preprocessing directives.
    """
    # cpp directives
    for k, v in regexs_cpp.items():
      matching = re.search(v,self.line)
      if matching:
        state.action = 'omit'
        #state.scope = 'normal'
        if k == 'regex_cpp_define':
          matching = re.match(v,self.line)
          macro    = matching.group('macro')
          if matching.group('expr'):
            expr = matching.group('expr')
          else:
            expr = ''
          macros.get_from_cpp(macro=macro,expr=expr)
        elif k == 'regex_cpp_undef':
          matching = re.match(v,self.line)
          macro    = matching.group('macro')
          macros.undef(macro_name=macro)
        elif k == 'regex_cpp_include':
          matching = re.match(v,self.line)
          inc = matching.group('fname')
          inc = inc.replace('"','')
          state.action = 'include'
          state.include = inc
        return
    # cpp conditional directives
    for k, v in regexs_cpp_cond.items():
      matching = re.search(v,self.line)
      if matching:
        if k == 'regex_cpp_cond_if' or k == 'regex_cpp_cond_elif':
          matching = re.match(v,self.line)
          expression = matching.group('expr')
          state.action = 'omit'
          if macros.evaluate(expression):
            state.scope = 'print'
          else:
            state.scope = 'omit'
        elif k == 'regex_cpp_cond_ifdef':
          matching = re.match(v,self.line)
          macro    = matching.group('macro')
          state.action = 'omit'
          if macros.is_def(macro=macro):
            state.scope = 'print'
          else:
            state.scope = 'omit'
        elif k == 'regex_cpp_cond_ifndef':
          matching = re.match(v,self.line)
          macro    = matching.group('macro')
          state.action = 'omit'
          if macros.is_undef(macro=macro):
            state.scope = 'print'
          else:
            state.scope = 'omit'
        elif k == 'regex_cpp_cond_else':
          state.action = 'omit'
          if state.scope == 'print':
            state.scope = 'omit'
          else:
            state.scope = 'print'
        elif k == 'regex_cpp_cond_endif':
          state.action = 'omit'
          state.scope = 'normal'
        return
    # directives not found
    state.action = 'print'
    if state.scope == 'print':
      state.action = 'print'
    elif state.scope == 'omit':
      state.action = 'omit'
    return
  def parse(self,macros,state):
    """
    Method for parsing a line.
    """
    self.preproc_check(macros=macros,state=state)
    if state.action == 'include' or state.action == 'omit':
      return None
    elif state.action == 'print':
      return macros.expand(self.line)
    else:
      return None
# functions definitions
def preprocess_file(sfile,parsed_file,macros,state):
  if not os.path.exists(sfile):
    print('Error: input file "'+sfile+'" not found!')
    sys.exit(1)
  else:
    macros.set(macro='__FILE__',value=sfile)
    source_file = open(sfile,'r')
    for l,line in enumerate(source_file):
      macros.set(macro='__LINE__',value=str(l+1))
      pline = Parsed_Line(line=line)
      output = pline.parse(macros=macros,state=state)
      if output:
        if parsed_file:
          parsed_file.writelines(output)
        else:
          print(output),
      elif state.action == 'include':
        state.action = 'print'
        preprocess_file(sfile=state.include,parsed_file=parsed_file,macros=macros,state=state)
    source_file.close()
  return
# main loop
if __name__ == '__main__':
  cliargs = cliparser.parse_args()
  macros = Macros()
  macros.get_from_CLI(macros=cliargs.D)
  if cliargs.input:
    if cliargs.output:
      parsed_file = open(cliargs.output,'w')
    else:
      parsed_file = None
    state = State()
    preprocess_file(sfile=cliargs.input,parsed_file=parsed_file,macros=macros,state=state)
    if cliargs.output:
      parsed_file.close()
    if cliargs.list_macros:
      macros.list()

#!/usr/bin/env python
"""
PreForM.py, Preprocessor for Fortran poor Men
"""
from __future__ import print_function
import ast
try:
  from datetime import datetime
  __now__ = datetime.now()
  __date__ = __now__.strftime('%b %d %Y')
  __time__ = __now__.strftime('%X')
except ImportError:
  __date__ = ''
  __time__ = ''
import os
import re
import sys
import argparse
__appname__ = "PreForM.py"
__description__ = "PreForM.py, Preprocessor for Fortran poor Men"
__long_description__ = "A very simple and stupid preprocessor for modern Fortran projects. PreForM.py supports the most used cpp pre-processing directives and provides advanced features typical of templating systems. Even if PreForM.py is currently Fortran-agnostic (it being usable within any programming languages) it is focused on Fortran programming language."
__version__ = "v1.1.2"
__author__ = "Stefano Zaghi"
__author_email__ = "stefano.zaghi@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/szaghi/PreForM"
# setting CLI
__cliparser__ = argparse.ArgumentParser(prog=__appname__, description='PreForM.py, Preprocessor for Fortran poor Men')
__cliparser__.add_argument('-v', '--version', action='version', help='Show version', version='%(prog)s '+__version__)
__cliparser__.add_argument('input', action='store', default=None, help='Input file name of source to be preprocessed')
__cliparser__.add_argument('-o', '--output', required=False, action='store', default=None, help='Output file name of preprocessed source')
__cliparser__.add_argument('-D', required=False, action='store', nargs='+', default=[], help='Define a list of macros in the form NAME1=VALUE1 NAME2=VALUE2...')
__cliparser__.add_argument('-lm', '--list-macros', required=False, action='store_true', default=False, help='Print the list of macros state as the last parsed line left it')
#regular expressions
__vname__ = r"(?P<name>[a-zA-Z][a-zA-Z0-9_]*)"
__macro__ = r"(?P<macro>[a-zA-Z][a-zA-Z0-9_]*(|\(.*?\)))"
__expr__ = r"(?P<expr>.*)"
__regex_function__ = re.compile(__vname__+r"\("+__expr__+r"\).*")
# cpp directives
__regex_cpp_define__ = re.compile(r"(?P<cpp_define>^(|\s*)#[Dd][Ee][Ff][Ii][Nn][Ee])\s+"+__macro__+r"\s+"+__expr__)
__regex_cpp_undef__ = re.compile(r"(?P<cpp_undef>^(|\s*)#[Uu][Nn][Dd][Ee][Ff])\s+"+__macro__)
__regex_cpp_include__ = re.compile(r"(?P<cpp_include>^(|\s*)#[Ii][Nn][Cc][Ll][Uu][Dd][Ee])\s+"+r"(?P<fname>.*)")
__regexs_cpp__ = {}
for k, v in locals().items():
  if not re.match(r"^__regex_cpp_cond_.*__", k) and re.match(r"^__regex_cpp_.*__", k):
    __regexs_cpp__[k] = v
# cpp conditional directives
__regex_cpp_cond_if__ = re.compile(r"(?P<cpp_if>^(|\s*)#[Ii][Ff])\s+"+__expr__)
__regex_cpp_cond_ifdef__ = re.compile(r"(?P<cpp_ifdef>^(|\s*)#[Ii][Ff][Dd][Ee][Ff])\s+"+__macro__)
__regex_cpp_cond_ifndef__ = re.compile(r"(?P<cpp_ifndef>^(|\s*)#[Ii][Ff][Nn][Dd][Ee][Ff])\s+"+__macro__)
__regex_cpp_cond_elif__ = re.compile(r"(?P<cpp_elif>^(|\s*)#[Ee][Ll][Ii][Ff])\s+"+__expr__)
__regex_cpp_cond_else__ = re.compile(r"(?P<cpp_else>^(|\s*)#[Ee][Ll][Ss][Ee])\s*")
__regex_cpp_cond_endif__ = re.compile(r"(?P<cpp_endif>^(|\s*)#[Ee][Nn][Dd][Ii][Ff]).*")
__regex_cpp_cond_defined__ = re.compile(r"(?P<cpp_defined>[Dd][Ee][Ff][Ii][Nn][Ee][Dd])"+r"(\s+|\()"+__macro__+r"(|\))")
__regex_cpp_cond_defined_kwd__ = re.compile(r"(?P<cpp_defined>[Dd][Ee][Ff][Ii][Nn][Ee][Dd])")
__regexs_cpp_cond__ = {}
for k, v in locals().items():
  if re.match(r"^__regex_cpp_cond_.*__", k):
    __regexs_cpp_cond__[k] = v
# pre-defined macros
__predef_macro__ = {'__FILE__':'', '__LINE__':'', '__DATE__':__date__, '__TIME__':__time__}
# PreForM.py macros: template system
__regex_pfm_kwd__ = "#PFM"
__regex_pfm__ = re.compile(r"^(|\s*)#PFM\s+")
# classes definitions
class PFMdirective(object):
  """
  PFMdirectives is an object that handles PreForM.py specific pre-processing directives, their attributes and methods.
  """
  def __init__(self, for_block=False, for_expression='', block_contents=None):
    self.for_block = for_block
    self.for_expression = for_expression
    self.block_contents = block_contents
  def add_to_block(self, line):
    """
    Method for adding line to block_contents.
    """
    if not self.block_contents:
      self.block_contents = []
    self.block_contents.append(line.replace('\n', ''))
  def execute(self):
    """
    Method for executing PFM directive.
    """
    if self.for_block:
      counter = self.for_expression.split('for')[1].split(' ')
      counter = next(item for item in counter if item is not '')
      block = ''
      cmd = ''
      cmd = cmd + self.for_expression.lstrip()
      for ctn in self.block_contents:
        cmd = cmd + "  block = block + '"+ctn.replace('$'+counter, "'+str("+counter+")+'")+"'"
        cmd = cmd +r'+"\n"'+'\n'
      #if sys.version_info[0]<3 :
      exec(cmd)
      #else:
        #exec(expr=cmd)
      return block
class Macros(object):
  """
  Macros is an object that handles defined and non defined macros, their attributes and methods.
  """
  def __init__(self, dic=None):
    if dic:
      self.dic = dic
    else:
      self.dic = __predef_macro__
    return

  def set(self, macro, value):
    """
    Method for setting macro's value or defining it.
    """
    self.dic[macro] = value
    return

  def is_def(self, macro):
    """
    Method for checking if a macro is presently defined.
    """
    result = False
    for key, val in self.dic.items():
      if macro == key:
        if val is not None:
          result = True
          return result
    return result

  def is_undef(self, macro):
    """
    Method for checking if a macro is not presently defined.
    """
    result = True
    for key, val in self.dic.items():
      if macro == key:
        if val is not None:
          result = False
          return result
    return result

  def expand(self, expression):
    """
    Method for expandind defined macros present into the expression.
    """
    for mkey, mval in self.dic.items():
      if mval is not None:
        if '(' in mkey or ')' in mkey:
          # function-like macro
          matching = re.match(__regex_function__, mkey)
          if matching:
            fname = matching.group('name')             # function name
            vnames = matching.group('expr').split(',')  # variables names
            if fname in expression:
              for matching in re.finditer(__regex_function__, expression):
                if matching:
                  expr = mval
                  if vnames[0] == '...':
                    # variadic macro
                    avnames = matching.group('expr')  # actual variables names
                    if '__VA_ARGS__' in mval:
                      # stringification
                      if '#__VA_ARGS__' in mval:
                        for match in re.finditer(',', avnames):
                          avnames = re.sub(',', '","', avnames)
                        avnames = '"'+avnames+'"'
                      expr = re.sub('(|#)__VA_ARGS__', avnames, expr)
                  else:
                    avnames = matching.group('expr').split(',')  # actual variables names
                    # substituting first variables names
                    for var, vname in enumerate(vnames):
                      # stringification
                      if '#' in expr:
                        for match in re.finditer('#'+vname, expr):
                          expr = re.sub('#'+vname, '"'+vname+'"', expr)
                      expr = expr.replace(vname, avnames[var])
                  # concatenation
                  if '##' in expr:
                    for match in re.finditer(r'(?P<lhs>.*[^ ])\s*##\s*(?P<rhs>[^ ].*)', expr):
                      lhs = match.group('lhs')
                      rhs = match.group('rhs')
                      expr = re.sub(r'(?P<lhs>.*[^ ])\s*##\s*(?P<rhs>[^ ].*)', lhs+rhs, expr)
                  # substituting leftmost match
                  expression = re.sub(__regex_function__, expr, expression)
        else:
          # object-like macro
          expression = expression.replace(mkey, mval)
    return expression

  def evaluate(self, expression):
    """
    Method for evaluating a conditional expression accordingly to the current macros state.
    """
    expression_processed = expression
    # check for "defined" operators
    defined = re.findall(__regex_cpp_cond_defined__, expression)
    for dfd in defined:
      expression_processed = expression_processed.replace(dfd[2], str(self.is_def(dfd[2])))
      expression_processed = re.sub(__regex_cpp_cond_defined_kwd__, '', expression_processed)
    # check for "or" and "and" operators
    expression_processed = expression_processed.replace('||', ' or ')
    expression_processed = expression_processed.replace('&&', ' and ')
    # expand macros
    expression_processed = self.expand(expression=expression_processed)
    try:
      result = ast.literal_eval(expression_processed)
    except SyntaxError:
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
    for key, val in self.dic.items():
      if val is not None:
        print(key+': '+str(val))
    print('Undefined macros')
    for key, val in self.dic.items():
      if val is None:
        print(key)
    return

  def get_from_cli(self, climacros):
    """
    Method for getting macros defined from CLI.
    """
    if len(climacros) > 0:
      for macro in climacros:
        self.dic[macro.split('=')[0]] = macro.split('=')[1]
    return

  def undef(self, macro_name=''):
    """
    Method for undefine a macro.
    """
    if macro_name != '':
      self.dic[macro_name] = None
    return

class State(object):
  """
  State is an object that handles the state of the current parsed line, their attributes and methods.
  """
  def __init__(self,
               action='print', # action = 'include','print','omit'
               scope='normal', # scope  = 'for_block', 'normal', 'print','omit'
               include=''):    # include file
    self.action = action
    self.scope = scope
    self.include = include
    return

class ParsedLine(object):
  """
  ParsedLine is an object that handles a parsed line, its attributes and methods.
  """
  def __init__(self, line=''):
    self.line = line
    return

  def preproc_check(self, macros, state, pfmdir):
    """
    Check if line contains preprocessing directives.
    """
    # cpp directives
    for key, val in __regexs_cpp__.items():
      matching = re.search(val, self.line)
      if matching:
        state.action = 'omit'
        #state.scope = 'normal'
        if key == '__regex_cpp_define__':
          matching = re.match(val, self.line)
          macro = matching.group('macro')
          if matching.group('expr'):
            expr = matching.group('expr')
          else:
            expr = ''
          macros.set(macro=macro, value=expr)
        elif key == '__regex_cpp_undef__':
          matching = re.match(val, self.line)
          macro = matching.group('macro')
          macros.undef(macro_name=macro)
        elif key == '__regex_cpp_include__':
          matching = re.match(val, self.line)
          inc = matching.group('fname')
          inc = inc.replace('"', '')
          state.action = 'include'
          state.include = inc
        return
    # cpp conditional directives
    for key, val in __regexs_cpp_cond__.items():
      matching = re.search(val, self.line)
      if matching:
        if key == '__regex_cpp_cond_if__' or key == '__regex_cpp_cond_elif__':
          matching = re.match(val, self.line)
          expression = matching.group('expr')
          state.action = 'omit'
          if macros.evaluate(expression):
            state.scope = 'print'
          else:
            state.scope = 'omit'
        elif key == '__regex_cpp_cond_ifdef__':
          matching = re.match(val, self.line)
          macro = matching.group('macro')
          state.action = 'omit'
          if macros.is_def(macro=macro):
            state.scope = 'print'
          else:
            state.scope = 'omit'
        elif key == '__regex_cpp_cond_ifndef__':
          matching = re.match(val, self.line)
          macro = matching.group('macro')
          state.action = 'omit'
          if macros.is_undef(macro=macro):
            state.scope = 'print'
          else:
            state.scope = 'omit'
        elif key == '__regex_cpp_cond_else__':
          state.action = 'omit'
          if state.scope == 'print':
            state.scope = 'omit'
          else:
            state.scope = 'print'
        elif key == '__regex_cpp_cond_endif__':
          state.action = 'omit'
          state.scope = 'normal'
        return
    # PreForM.py directives
    if state.scope != 'omit':
      matching = re.search(__regex_pfm__, self.line)
      if matching:
        state.action = 'omit'
        match = re.search(r"\s+for\s+", self.line.split(__regex_pfm_kwd__)[1])
        if match:
          # for block starts
          state.scope = 'for_block'
          pfmdir.for_block = True
          pfmdir.for_expression = self.line.split(__regex_pfm_kwd__)[1]
        else:
          match = re.search(r"\s+endfor\s+", self.line.split(__regex_pfm_kwd__)[1])
          if match:
            # for block ends
            self.line = pfmdir.execute()
            pfmdir.for_block = False
            pfmdir.for_expression = ''
            pfmdir.block_contents = []
            state.action = 'print'
            state.scope = 'print'
        return
      if state.scope == 'for_block':
        pfmdir.add_to_block(line=self.line)
        return
    # directives not found
    state.action = 'print'
    if state.scope == 'print':
      state.action = 'print'
    elif state.scope == 'omit':
      state.action = 'omit'
    return

  def parse(self, macros, state, pfmdir):
    """
    Method for parsing a line.
    """
    self.preproc_check(macros=macros, state=state, pfmdir=pfmdir)
    if state.action == 'include' or state.action == 'omit':
      return None
    elif state.action == 'print':
      return macros.expand(self.line)
    else:
      return None

# functions definitions
def preprocess_file(sfile, parsed_file, macros, state, pfmdir):
  """
  Function for pre-processing a single file.
  """
  if not os.path.exists(sfile):
    print('Error: input file "'+sfile+'" not found!')
    sys.exit(1)
  else:
    macros.set(macro='__FILE__', value=sfile)
    source_file = open(sfile, 'r')
    for lnn, line in enumerate(source_file):
      macros.set(macro='__LINE__', value=str(lnn+1))
      pline = ParsedLine(line=line)
      output = pline.parse(macros=macros, state=state, pfmdir=pfmdir)
      if output:
        if parsed_file:
          parsed_file.writelines(output)
        else:
          print(output, end='')
      elif state.action == 'include':
        state.action = 'print'
        preprocess_file(sfile=state.include, parsed_file=parsed_file, macros=macros, state=state, pfmdir=pfmdir)
    source_file.close()
  return

def main():
  """
  Main function.
  """
  cliargs = __cliparser__.parse_args()
  macros_ = Macros()
  macros_.get_from_cli(climacros=cliargs.D)
  pfmdir_ = PFMdirective()
  if cliargs.input:
    if cliargs.output:
      parsed_file_ = open(cliargs.output, 'w')
    else:
      parsed_file_ = None
    state_ = State()
    preprocess_file(sfile=cliargs.input, parsed_file=parsed_file_, macros=macros_, state=state_, pfmdir=pfmdir_)
    if cliargs.output:
      parsed_file_.close()
    if cliargs.list_macros:
      macros_.list()

# main loop
if __name__ == '__main__':
  main()

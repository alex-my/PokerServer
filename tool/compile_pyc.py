# coding:utf8
import compileall
import re
import os


path = os.path.dirname(os.getcwd())
compileall.compile_dir(path, rx=re.compile(r'^.svn'))




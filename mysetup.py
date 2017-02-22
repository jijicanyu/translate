from distutils.core import setup
import py2exe

setup(windows=["translate_test.py"],options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}})
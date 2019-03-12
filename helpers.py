import json
import time
import os
from sh import ibmcloud as ibmcloud0, ErrorReturnCode
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv
import threading
from threading import current_thread

# init for colorama
init()

threadLocal = threading.local()

def makeLocal():
  if getattr(threadLocal, 'indent', None) is None:
    threadLocal.indent = 0

def iprint(string):
  makeLocal()
  indent = threadLocal.indent
  if (indent == 0):
    print(Style.BRIGHT + string + Style.RESET_ALL)
  else:
    print(Style.DIM + (' ' * threadLocal.indent * 2) + string + Style.RESET_ALL)

# wraps ibmcloud and always use the JSON output
def ibmcloudj(*args, **kwargs):
  cmd = 'ibmcloud'
  for arg in args:
    cmd = cmd + ' ' + str(arg)
  for key, value in kwargs.items():
    cmd = cmd + ' --' + key.replace('_', '-') + '=' + str(value)
  iprint(Style.BRIGHT + cmd + Style.RESET_ALL)
  return json.loads(ibmcloud0(*args, json=True, **kwargs).stdout)

def ibmcloud(*args, **kwargs):
  cmd = 'ibmcloud'
  for arg in args:
    cmd = cmd + ' ' + str(arg)
  for key, value in kwargs.items():
    cmd = cmd + ' --' + key.replace('_', '-') + '=' + str(value)
  iprint(Style.BRIGHT + cmd + Style.RESET_ALL)
  return ibmcloud0(*args, **kwargs).stdout

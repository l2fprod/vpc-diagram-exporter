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

new_env = os.environ.copy()
new_env["IBMCLOUD_COLOR"] = "false"

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

def sanitize(output):
  sanitized = output.decode("utf-8").replace("OK", "")
  return sanitized

# wraps ibmcloud and always use the JSON output
def ibmcloudj(*args, **kwargs):
  cmd = 'ibmcloud'
  for arg in args:
    cmd = cmd + ' ' + str(arg)
  for key, value in kwargs.items():
    cmd = cmd + ' --' + key.replace('_', '-') + '=' + str(value)
  iprint(Style.BRIGHT + cmd + Style.RESET_ALL)
  return json.loads(sanitize(ibmcloud0(*args, json=True, _env=new_env, **kwargs).stdout))

def ibmcloudoj(*args, **kwargs):
  cmd = 'ibmcloud'
  for arg in args:
    cmd = cmd + ' ' + str(arg)
  for key, value in kwargs.items():
    cmd = cmd + ' --' + key.replace('_', '-') + '=' + str(value)
  iprint(Style.BRIGHT + cmd + Style.RESET_ALL)
  return json.loads(sanitize(ibmcloud0(*args, output='JSON', _env=new_env, **kwargs).stdout))

def ibmcloud(*args, **kwargs):
  cmd = 'ibmcloud'
  for arg in args:
    cmd = cmd + ' ' + str(arg)
  for key, value in kwargs.items():
    cmd = cmd + ' --' + key.replace('_', '-') + '=' + str(value)
  iprint(Style.BRIGHT + cmd + Style.RESET_ALL)
  return sanitize(ibmcloud0(*args, _env=new_env, **kwargs).stdout)

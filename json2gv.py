#!/usr/bin/python
#
# take a big JSON of VPC resources and renders a Graphviz file
#
import inspect
import os
import sys
import json
from jinja2 import Template

def get_script_dir(follow_symlinks=True):
  path = inspect.getabsfile(get_script_dir)
  if follow_symlinks:
    path = os.path.realpath(path)
  return os.path.dirname(path)

with open('output/all.json', 'r') as allFile:
  all = json.load(allFile)

with open(get_script_dir() + '/json2gv-styling.json', 'r') as styleFile:
  styles = json.load(styleFile)

with open(get_script_dir() + '/render-to-gv.j2', 'r') as templateFile:
  template = Template(templateFile.read().decode('utf8'))

# generate one graphviz per vpc
vpcs = all['vpcs']
for vpc in vpcs:
  all['vpcs'] = [ 1 ]
  all['vpcs'][0] = vpc
  print('>>> Generating {0}'.format('output/' + vpc['name'] + '.gv'))
  with open('output/' + vpc['name'] + '.gv', 'w') as allOutputFile:
    allOutputFile.write(template.render(data=all, styles=styles).encode('utf8'))

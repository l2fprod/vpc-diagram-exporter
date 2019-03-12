#!/usr/bin/python
#
# take a big JSON of VPC resources and renders a Graphviz file
#
import json
from jinja2 import Template

with open('output/all.json', 'r') as allFile:
  all = json.load(allFile)

with open('json2gv-styling.json', 'r') as styleFile:
  styles = json.load(styleFile)

with open('render-to-gv.j2', 'r') as templateFile:
  template = Template(templateFile.read().decode('utf8'))

# generate one graphviz per vpc
vpcs = all['vpcs']
for vpc in vpcs:
  all['vpcs'] = [ 1 ]
  all['vpcs'][0] = vpc
  print('>>> Generating {0}'.format('output/' + vpc['name'] + '.gv'))
  with open('output/' + vpc['name'] + '.gv', 'w') as allOutputFile:
    allOutputFile.write(template.render(data=all, styles=styles).encode('utf8'))

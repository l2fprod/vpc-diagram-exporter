#!/usr/bin/python3
#
# dump all VPC resources
#
import os
from helpers import *
from jinja2 import Template
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as e:
  floatingips = e.submit(ibmcloudj, 'is', 'floating-ips')
  images = e.submit(ibmcloudj, 'is', 'images')
  ikePolicies = e.submit(ibmcloudj, 'is', 'ike-policies')
  instances = e.submit(ibmcloudj, 'is', 'instances')
  instanceProfiles = e.submit(ibmcloudj, 'is', 'instance-profiles')
  ipsecPolicies = e.submit(ibmcloudj, 'is', 'ipsec-policies')
  keys = e.submit(ibmcloudj, 'is', 'keys')
  loadBalancers = e.submit(ibmcloudj, 'is', 'load-balancers')
  networkAcls = e.submit(ibmcloudj, 'is', 'network-acls')
  publicGateways = e.submit(ibmcloudj, 'is', 'public-gateways')
  securityGroups = e.submit(ibmcloudj,'is', 'security-groups')
  subnets = e.submit(ibmcloudj, 'is', 'subnets')
  vpcs = e.submit(ibmcloudj, 'is', 'vpcs')
  vpns = e.submit(ibmcloudj, 'is', 'vpn-gateways')
  volumes = e.submit(ibmcloudj, 'is', 'volumes')
  target = e.submit(ibmcloudoj, 'target')

def get_result(call):
  try:
    return call.result()
  except Exception as err:
    print(err)
    return []

all = {
  'floating-ips': get_result(floatingips),
  'images': get_result(images),
  'ike-policies': get_result(ikePolicies),
  'instances': get_result(instances),
  'instance-profiles': get_result(instanceProfiles),
  'ipsec-policies': get_result(ipsecPolicies),
  'keys': get_result(keys),
  'load-balancers': get_result(loadBalancers),
  'network-acls': get_result(networkAcls),
  'public-gateways': get_result(publicGateways),
  'security-groups': get_result(securityGroups),
  'subnets': get_result(subnets),
  'vpcs': get_result(vpcs),
  'vpn-gateways': get_result(vpns),
  'volumes': get_result(volumes),
  'region': get_result(target)['region'],
}

# add zones
region = all['region']
region['zones'] = ibmcloudj('is', 'zones', region['name'])

# add subnets under their vpcs
vpcIdToVPC = {}
for vpc in all['vpcs']:
  vpcIdToVPC[vpc['id']] = vpc
  vpc['subnets'] = []
for subnet in all['subnets']:
  if vpcIdToVPC[subnet['vpc']['id']]:
    vpcIdToVPC[subnet['vpc']['id']]['subnets'].append(subnet)

# set the VPC region to the region of the first subnet
for vpc in all['vpcs']:
  vpc['region'] = region['name']

# map subnet id to subnet
subnetIdToSubnet = {}
for subnet in all['subnets']:
  subnetIdToSubnet[subnet['id']] = subnet
  subnet['instances'] = []

# map floating ip id to floating ip
fipNameToFloatingIP = {}
for fip in all['floating-ips']:
  fipNameToFloatingIP[fip['name']] = fip

# group all nic
all['nics'] = []
for server in all['instances']:
  all['nics'].extend(ibmcloudj('is', 'instance-network-interfaces', server['id']))

# replace the floating ip references under nic with the actual fip
for nic in all['nics']:
  if 'floating_ips' in nic and nic['floating_ips']:
    for fipIndex, fip in enumerate(nic['floating_ips']):
      nic['floating_ips'][fipIndex] = fipNameToFloatingIP[fip['name']]

# add the nics under their servers
# and the servers under their subnets
for server in all['instances']:
  for serverNicIndex, serverNic in enumerate(server['network_interfaces']):
    for nic in all['nics']:
      if (serverNic['id'] == nic['id']):
        server['network_interfaces'][serverNicIndex] = nic
        subnetIdToSubnet[nic['subnet']['id']]['instances'].append(server)

# fill VPN Gateway connections
for vpn in all['vpn-gateways']:
  vpn['connections'] = ibmcloudj('is', 'vpn-gateway-connections', vpn['id'])

# retrieve VPC address prefixes
for vpc in all['vpcs']:
  vpc['address_prefixes'] = ibmcloudj('is', 'vpc-address-prefixes', vpc['id'])

# save the output
if not os.path.exists('output'):
  os.makedirs('output')
with open('output/all.json', 'w') as outfile:
  json.dump(all, outfile, sort_keys=True, indent=2)

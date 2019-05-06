#!/usr/bin/python
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
  regions = e.submit(ibmcloudj, 'is', 'regions')
  securityGroups = e.submit(ibmcloudj,'is', 'security-groups')
  subnets = e.submit(ibmcloudj, 'is', 'subnets')
  vpcs = e.submit(ibmcloudj, 'is', 'vpcs')
  vpns = e.submit(ibmcloudj, 'is', 'vpn-gateways')
  volumes = e.submit(ibmcloudj, 'is', 'volumes')

all = {
  'floating-ips': floatingips.result(),
  'images': images.result(),
  'ike-policies': ikePolicies.result(),
  'instances': instances.result(),
  'instance-profiles': instanceProfiles.result(),
  'ipsec-policies': ipsecPolicies.result(),
  'keys': keys.result(),
  'load-balancers': loadBalancers.result(),
  'network-acls': networkAcls.result(),
  'public-gateways': publicGateways.result(),
  'regions': regions.result(),
  'security-groups': securityGroups.result(),
  'subnets': subnets.result(),
  'vpcs': vpcs.result(),
  'vpn-gateways': vpns.result(),
  'volumes': volumes.result(),
}

# add the VPCs with classic access
all['vpcs'].extend(ibmcloudj('is', 'vpcs', '--classic-access'))

# add zones
for region in all['regions']:
  region['zones'] = ibmcloudj('is', 'zones', region['name'])

# add subnets under their vpcs
vpcIdToVPC = {}
for vpc in all['vpcs']:
  vpcIdToVPC[vpc['id']] = vpc
  vpc['subnets'] = []
for subnet in all['subnets']:
  vpcIdToVPC[subnet['vpc']['id']]['subnets'].append(subnet)

# set the VPC region to the region of the first subnet
for vpc in all['vpcs']:
  if len(vpc['subnets']) > 0:
    subnetZone = vpc['subnets'][0]['zone']['name']
    # find the region with this zone
    for region in all['regions']:
      for zone in region['zones']:
        if (zone['name'] == subnetZone):
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
  if nic.has_key('floating_ips'):
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

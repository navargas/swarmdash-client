#!/usr/bin/env python
import ibmiotf.device
import subprocess
import time
import uuid
import sys
import re

ID = str(uuid.uuid4()).replace('-','')
if (len(sys.argv) > 1):
  ID = sys.argv[1]

iotclient = None

try:
  options = {
    'org': 'quickstart',
    'type': 'quickstart',
    'id': ID,
    'auth-method':'quickstart',
    'auth-token':''
  }
  iotclient = ibmiotf.device.Client(options)
except ibmiotf.ConnectionException  as e:
  print('There was an issue')
  print(e)


print('Connecting...')
iotclient.connect()
print('done. Data available at http://navargas.github.io/swarmdash/#' + ID)


def getMachines():
  try:
    machines = {}
    raw = subprocess.check_output(
      ['docker', 'info']
    )
    for i in re.findall('[a-zA-Z: ]+[0-9]+\.[0-9]+\.[0-9]+\.[0-9]', raw):
      machineName = i.replace(' ','').split(':')[0]
      machines[machineName] = {}
    return machines
  except subprocess.CalledProcessError as e:
    print('Unable to read docker information')
    sys.exit(1)

def collectData():
  try:
    data = getMachines()
    raw = subprocess.check_output(
      ['docker', 'ps', '--format', '{{.ID}}\t{{.Names}}\t{{.Image}}']
    ).split('\n')
    for i in raw:
      if len(i) == 0: continue
      container, name, image = i.split('\t')
      machine, _ = name.split('/')
      if (machine not in data):
        data[machine] = {}
      data[machine][image + ' (' + container + ')'] = [];
    return data
  except subprocess.CalledProcessError as e:
    print('Unable to read docker information')
    sys.exit(1)

def main():
  try:
    while 1:
      iotclient.publishEvent('event', 'json', collectData())
      time.sleep(1)
  except KeyboardInterrupt:
    sys.exit(0)

main()

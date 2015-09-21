#!/usr/bin/env python
import ibmiotf.device
import uuid

ID = str(uuid.uuid4()).replace('-','')
ID=  'wdiaiodioasdojbobobo'
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


iotclient.connect()

iotclient.publishEvent('event', 'json', {'name1':{}})

#!/usr/bin/python
#import sys
#import psycopg2
import json
import requests
from datetime import datetime


lambdaUrl = 'https://icswse9im8.execute-api.us-west-2.amazonaws.com/ocf/base'
pk = 'Room-temp-' + datetime.now().strftime("%H:%M:%S")
temp_params = { 
  'command': 'addRooms',
  'staging_rooms': [{
    'pk': pk,
    'sk': 'TESTING',
    'data': 'bbbbbbb',
    'size': 35}],
  'event_rooms': []
}

print(json.dumps(temp_params))
print("SENDING!!!")
r = requests.post(lambdaUrl, json = temp_params)
print(r.text)


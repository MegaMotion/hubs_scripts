#!/usr/bin/python
#import sys
#import psycopg2
import json
import requests


lambdaUrl = 'https://icswse9im8.execute-api.us-west-2.amazonaws.com/ocf/base'
temp_params = { 
  'command': 'addRooms',
  'staging_rooms': [{'pk': 'Room-bbbbbbb',
    'sk': 'TESTING',
    'data': 'bbbbbbb',
    'size': 35}],
  'event_rooms': []
}

print(json.dumps(temp_params))
print("SENDING!!!")
r = requests.post(lambdaUrl, json = temp_params)
print(r.text)

#!/usr/bin/python
#import sys
#import psycopg2
import json
import requests


lambdaUrl = 'https://icswse9im8.execute-api.us-west-2.amazonaws.com/ocf/base'
#temp_params = { 
#  'command': 'setRoomSize',
#  'size': 25
#}

#print(json.dumps(temp_params))
#print("SENDING!!!")
#r = requests.post(lambdaUrl, json = temp_params)
#print(r.text)

rooms_file = "rooms.json"
with open(rooms_file, "r") as read_file:
    rooms_data = json.load(read_file)
    read_file.close()

rooms_out = { 'Rooms': [] }
params = {
  'command': 'addRooms',
  'staging_rooms': [],
  'event_rooms': []
}
b = 0
for room in rooms_data["rooms"]:
  b += 1
  sid = room["hub_sid"]
  pk = "Room-" + sid
  #print("Staging room: " + sid)
  stage_params = {
    'pk': pk,
    'sk': 'STAGING',
    'data': room["copy_name"],
    'size': 25,
    'sort_index': 0
  }
  params["staging_rooms"].append(stage_params)
  
  c = 0
  for copy_room in room["copy_rooms"]:
    c += 1
    counter = ""
    if (c < 10):
      counter = "0" + str(c)
    else:
      counter = str(c)
    #print("Event room: " + copy_room)
    new_params = {
      'pk': "Room-" + copy_room,
      'sk': "Room-" + sid,
      'data': room["copy_name"] + counter,
      'size': 25,
      'sort_index': c
    }
    params["event_rooms"].append(new_params)
  
  
#print(json.dumps(params))
#print("SENDING!!!")
r = requests.post(lambdaUrl, json = params)
print(r.text)


#r = requests.post(lambdaUrl, json = params)

#entities_file = "entities.json"
#r = requests.get('https://hubbub6-data.s3-us-west-2.amazonaws.com/entities.json') 

#entities_data = json.loads(r.text)
#print(r.text)

#!/usr/bin/python
import sys
import psycopg2
import json
import requests
import datetime

entities_file = "entities.json" # new way
r = requests.get('https://hubbub6-data.s3-us-west-2.amazonaws.com/entities.json') # newest way
entities_data = json.loads(r.text)


db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()

# Task: to add a row in hub_role_memberships for each entity member, for each room, both staging and event.

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for entity in entities_data["entities"]:
  rooms = []
  for room in entity["rooms"]:
    sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + room["staging"] + "';"
    c.execute(sql)
    rooms.append(c.fetchone()[0])    
    for event_room in room["event"]:
      #print("Event room: " + event_room)
      sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + event_room + "';"
      c.execute(sql)
      rooms.append(c.fetchone()[0])

  for room in rooms:
    #print("Room: " + str(room))
    for member in entity["members"]:
      sql = "INSERT INTO hub_role_memberships (hub_id,account_id,inserted_at,updated_at) VALUES (" + str(room) + "," + str(member) + ",'" + str(dt) + "','" + str(dt) + "');"
      print(sql)
      #c.execute(sql)
  #for member in entity["members"]:
    #print("Member: " + member)
    

db.commit()    
c.close()
db.close()

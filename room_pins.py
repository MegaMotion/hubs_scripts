#!/usr/bin/python
import sys
import psycopg2
import json
import requests

entities_file = "entities.json"
r = requests.get('https://hubbub6-data.s3-us-west-2.amazonaws.com/entities.json') # newest way
entities_data = json.loads(r.text)

do_not_copy = [] #  useful for signage or whatever you need in the staging rooms that you do not want in the event rooms.
do_not_delete = [] # pinned items in event rooms that should not be overwritten from the staging rooms (for future)

db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()

# New way, using entities.json: 
for entity in entities_data["entities"]:
  for room in entity["rooms"]:
    sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + room["staging"] + "';"
    c.execute(sql)
    hub_id = c.fetchone()[0]
    sql = "SELECT * FROM room_objects WHERE hub_id=" + str(hub_id) + ";"
    c.execute(sql)
    object_rows = c.fetchall()
    print("Found " + str(len(object_rows)) + " objects in " + room["name"])

    for event_room in room["event"]:
      print("Event room: " + event_room)
      sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + event_room + "';"
      c.execute(sql)
      event_hub_id = c.fetchone()[0]
      sql = "DELETE FROM room_objects WHERE hub_id=" + str(event_hub_id) + ";"
      c.execute(sql)
      for row in object_rows:
        room_object_id = row[0]
        object_id = row[1]
        gltf_node = row[3]
        inserted_at = row[4]
        updated_at = row[5]
        account_id = row[6]
        if object_id not in do_not_copy:
          c.execute("INSERT INTO room_objects(object_id,hub_id,gltf_node,inserted_at,updated_at,account_id) " + \
                    "VALUES (%s,%s,%s,%s,%s,%s);",\
                    (object_id,event_hub_id,psycopg2.Binary(gltf_node),inserted_at,updated_at,account_id))

db.commit()    
c.close()
db.close()

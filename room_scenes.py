#!/usr/bin/python
import sys
import psycopg2
import json

rooms_file = "rooms.json"
if (len(sys.argv)==2):
    rooms_file = sys.argv[1]
print("Copying pins for rooms file: " + rooms_file)

with open(rooms_file, "r") as read_file:
    rooms_data = json.load(read_file)
    read_file.close()
    
db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()
for room in rooms_data["rooms"]:
    sql = "SELECT scene_id,scene_listing_id FROM hubs WHERE hub_sid='" + room["hub_sid"] + "';"
    c.execute(sql)
    hub = c.fetchone()
    scene_id = hub[0]
    scene_listing_id = hub[1]
    if (scene_id):
        print("Room " + room["slug"] + " has a scene id: " + str(scene_id))
    elif (scene_listing_id):
        print("Room " + room["slug"] + " has a scene listing id: " + str(scene_listing_id))

c.close()
db.close()

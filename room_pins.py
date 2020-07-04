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
    print("slug: " + room["slug"] + " SID: " + room["hub_sid"])
    for copy_room in room["copy_rooms"]:
        print("Copy room: " + copy_room_
    sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + room["hub_sid"] + "';"
    c.execute(sql)
    hub_id = c.fetchone()[0]
    sql = "DELETE FROM room_objects WHERE hub_id=" + str(hub_id) + ";"
    c.execute(sql)
    sql = "SELECT * FROM room_objects WHERE hub_id=" + str(hub_id) + ";"
    c.execute(sql)
    object_rows = c.fetchall()
    for row in object_rows:
        room_object_id = row[0]
        object_id = row[1]
        gltf_node = row[3]
        inserted_at = row[4]
        updated_at = row[5]
        account_id = row[6]        
        for copy_room in room["copy_rooms"]:
            print("Adding objects to room: " + copy_room)
            sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + copy_room + "';"
            c.execute(sql)
            copy_hub_id = c.fetchone()[0]
            c.execute("INSERT INTO room_objects(object_id,hub_id,gltf_node,inserted_at,updated_at,account_id) " + \
                      "VALUES (%s,%s,%s,%s,%s,%s);",\
                      (object_id,copy_hub_id,psycopg2.Binary(gltf_node),inserted_at,updated_at,account_id))

db.commit()    
c.close()
db.close()

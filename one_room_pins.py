#!/usr/bin/python
import sys
import psycopg2
import json

rooms_file = "rooms.json"
if (len(sys.argv)!=3):
    print("This script requires two arguments: the hub_sid of the source room, and that of the destination room.")
    sys.exit()

source_sid = sys.argv[1]
dest_sid   = sys.argv[2]

print("Copying pins from room: " + source_sid  + "  to room: " + dest_sid)    

db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()
sql = "SELECT hub_id,name FROM hubs WHERE hub_sid='" + source_sid + "';"
c.execute(sql)
source = c.fetchone()
hub_id = source[0]
source_name = source[1]

sql = "SELECT * FROM room_objects WHERE hub_id=" + str(hub_id) + ";"
c.execute(sql)
object_rows = c.fetchall()
print("Found " + str(len(object_rows)) + " objects in " + source_name)

sql = "SELECT hub_id,name FROM hubs WHERE hub_sid='" + dest_sid + "';"
c.execute(sql)
dest = c.fetchone()
dest_hub_id = dest[0]
dest_name = dest[1]
print("source name: " + source_name  + "  dest name: " + dest_name)
sql = "DELETE FROM room_objects WHERE hub_id=" + str(dest_hub_id) + ";"
c.execute(sql)
for row in object_rows:
    room_object_id = row[0]
    object_id = row[1]
    gltf_node = row[3]
    inserted_at = row[4]
    updated_at = row[5]
    account_id = row[6]
    c.execute("INSERT INTO room_objects(object_id,hub_id,gltf_node,inserted_at,updated_at,account_id) " + \
              "VALUES (%s,%s,%s,%s,%s,%s);",\
              (object_id,dest_hub_id,psycopg2.Binary(gltf_node),inserted_at,updated_at,account_id))

db.commit()
c.close()
db.close()

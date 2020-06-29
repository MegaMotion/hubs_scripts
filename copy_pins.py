#!/usr/bin/python
import sys
import psycopg2

if (len(sys.argv)!=2):
    print("You must enter the base name of the room from which you want to copy pinned objects. Rooms must be named such that there is a room with e.g. 'yourroom' as its name, and then a collection of rooms named like 'yourroom_*'. The base room is the source of the pinned objects and the other rooms are recipients of copies.")
    sys.exit()

base_name = sys.argv[1]
db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is not None:
    c = db.cursor()

    sql = "SELECT hub_id FROM hubs WHERE name='" + base_name + "';"
    c.execute(sql)
    if c.rowcount==0:
        print ("Room " + base_name + " not found.")
        c.close()
        db.close()
        sys.exit()
    
    hub_row = c.fetchone()
    hub_id = str(hub_row[0])
    sql =  "SELECT * FROM room_objects WHERE hub_id=" + hub_id + ";"
    c.execute(sql)
    object_rows = c.fetchall()
    print ("there are " + str(len(object_rows)) + " pinned objects for room " + base_name)

    sql = "SELECT hub_id FROM hubs WHERE name LIKE '" + base_name + "_%';"
    c.execute(sql)
    hub_copy_rows = c.fetchall()
    print ("there are " + str(len(hub_copy_rows)) + " room copies of " + base_name)

    for room_id in hub_copy_rows:
        new_hub_id = str(room_id[0])
        for row in object_rows:
            room_object_id = row[0]
            object_id = row[1]
            gltf_node = row[3]
            inserted_at = row[4]
            updated_at = row[5]
            account_id = row[6]
            c.execute("INSERT INTO room_objects(object_id,hub_id,gltf_node,inserted_at,updated_at,account_id) VALUES (%s,%s,%s,%s,%s,%s);",\
                      (object_id,new_hub_id,psycopg2.Binary(gltf_node),inserted_at,updated_at,account_id))

    db.commit()    
    c.close()
    db.close()
    
else:
    print("Error: Database not found.")


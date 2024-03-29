#!/usr/bin/python
import sys
import psycopg2
import json
import requests
import datetime



member = 727627167411732616
dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()

# First, clear the table?
#sql = "DELETE FROM hub_role_memberships;"
#c.execute(sql)
room_count = 0
lambdaUrl = 'https://icswse9im8.execute-api.us-west-2.amazonaws.com/ocf/base'
params = { 
  'command': 'getAllRooms'
}
r = requests.post(lambdaUrl, json = params)
data = json.loads(r.text)

#First, convert the seven digit sid strings to Room IDs, which are big ints
rooms = []
for room in data["body"]["Items"]:
  sid = room["pk"][5:]
  print(" room: " + sid + " length: " + str(len(sid)))
  if (len(sid)==7):
    sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + sid + "';"
    c.execute(sql)
    print("Rowcount: " + str(c.rowcount))
    if (c.rowcount == 1):
      RoomID = c.fetchone()[0]
      print("Room ID: " + str(RoomID))
      rooms.append(RoomID)
      room_count += 1

for room in rooms: #Then add hub role memberships to all of them, for member.
  sql = "INSERT INTO hub_role_memberships (hub_id,account_id,inserted_at,updated_at) VALUES (" + str(room) + "," + str(member) + ",'" + dt + "','" + dt + "');"
  c.execute(sql)
  print(sql)

db.commit()    
c.close()
db.close()
#!/usr/bin/python
import sys
import psycopg2
import json
import requests
import datetime

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()

return_data = {}
return_data["users"] = []
room_count = 0
lambdaUrl = 'https://icswse9im8.execute-api.us-west-2.amazonaws.com/ocf/base'
params = { 
  'command': 'getRoomRequests'
}
r = requests.post(lambdaUrl, json = params)
#data = r.json #
data = json.loads(r.text)
print(r.text)
body = json.loads(data["body"])

room_index = body["member_room_index"]

print("Users: \n" )
rooms = {}
for user in body["users"]:
  print("    user   "  +  user["pk"] + "  " +   user["sk"] + "  " +   user["last_room"] + "\n")
  rooms[user["last_room"]] = ""

print("Rooms: " )
#for room in rooms:
for key in rooms:
  print(key)
  sql = "SELECT hub_id,scene_id,scene_listing_id FROM hubs WHERE hub_sid='" + key + "';"
  c.execute(sql)
  if (c.rowcount == 1):
      #rooms[key]["hub_id"] = c.fetchone()[0]
      room_ID = c.fetchone()[0]  
      scene_ID = c.fetchone()[1]
      scene_listing_ID = c.fetchone()[2]
      #if (scene_ID.length > 0):
      #  rooms[key]["scene_id"] = scene_ID
      #elif (scene_listing_ID.length > 0):
      #  rooms[key]["scene_id"] = scene_listing_ID
      print("Room ID: " + room_ID + " scene ID " + scene_ID + " listing ID " + scene_listing_ID)

for user in body["users"]:
  print(sql)
  new_sid = "ocf"
  if (room_index < 10):
    new_sid += "000" + str(room_index)
  elif (room_index < 100):
    new_sid += "00" + str(room_index)
  elif (room_index < 1000):
    new_sid += "0" + str(room_index)
  else:
    new_sid += str(room_index)

  sql = "INSERT INTO hubs (hub_sid,slug,name,inserted_at,updated_at,entry_mode,scene_id," + \
       "room_size,created_by_account_id,member_permissions,allow_promotion) VALUES " + \
        "('" + new_sid + "','" + new_sid + "','" + new_sid + "','" + dt + "','" + dt + \
        "','allow'," + rooms[user["last_room"]]["scene_id"] + ",40," + user["sk"] + ",48,'t');"
  print(sql)
  #c.execute(sql)
  this_user = { "pk": user["pk"], "sk": user["sk"], "room": new_sid }
  return_data["users"].append(this_user)

  room_index += 1

print(json.dumps(return_data))
  #NOW: look up scene ID from database, and grab room ID bigint while you're here
  #Then use that to create a new room, with this accountID as owner, and the scene ID
  #Then store that new sid (ocf0004 etc) with this user, and send it back with a returnRoomRequests command.



#First, convert the seven digit sid strings to Room IDs, which are big ints
#rooms = []
#for room in data["body"]["Items"]:
#  sid = room["pk"][5:]
#  print(" room: " + sid + " length: " + str(len(sid)))
#  if (len(sid)==7):
#    sql = "SELECT hub_id FROM hubs WHERE hub_sid='" + sid + "';"
#    c.execute(sql)
#    print("Rowcount: " + str(c.rowcount))
#    if (c.rowcount == 1):
#      RoomID = c.fetchone()[0]
#      print("Room ID: " + str(RoomID))
#      rooms.append(RoomID)
#      room_count += 1

#for room in rooms: #Then add hub role memberships to all of them, for member.
#  sql = "INSERT INTO hub_role_memberships (hub_id,account_id,inserted_at,updated_at) VALUES (" + str(room) + "," + str(member) + ",'" + dt + "','" + dt + "');"
#  c.execute(sql)
#  print(sql)

#db.commit()    
#c.close()
#db.close()
#!/usr/bin/python
import sys
import psycopg2
import json

rooms_file = "rooms.json"
with open(rooms_file, "r") as read_file:
    rooms_data = json.load(read_file)
    read_file.close()

db = psycopg2.connect(host="localhost",database="polycosm_production",user="postgres")
if db is None:
    print("Error: Database not found.")
    sys.exit() #temp
    
c = db.cursor()

start_date = '2020-07-01'
end_date =   '2020-07-14'

session_length_query = "SELECT session_id,started_at,ended_at,AGE(ended_at,started_at) AS length,entered_event_payload FROM session_stats WHERE started_at::date>='" + start_date + "' AND started_at<='" + end_date  + "';"
#  ORDER BY AGE(ended_at,started_at) DESC;"

c.execute(session_length_query)
session_rows = c.fetchall()
for session in session_rows:
    print("Start: " + str(started_at) + "  Session length: " + str(session[3]))


for room in rooms_data["rooms"]:
    print("slug: " + room["slug"] + " SID: " + room["hub_sid"])

    
c.close()
db.close()

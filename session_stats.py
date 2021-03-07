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

start_date = '2021-03-05'
end_date =   '2021-03-06'


#New strategy: use sql INTERVAL to increment
current_hour = 0
current_minute = 0

h = 17
#while n < 72: #for a three day event
while h < 18: # for a one hour event starting at five pm, ie check 17:00 to 19:00 to count stragglers.
    session_query = "SELECT session_id,entered_event_payload FROM session_stats WHERE started_at > timestamp '" + \
                    start_date + " 00:00:00' + INTERVAL '" + str(h) + " hours' AND started_at < timestamp '" + \
                    start_date + " 00:00:00' + INTERVAL '" + str(h+1) + " hours';"
    h += 1
    print("QUERY: " + session_query)
    c.execute(session_query)
    rows = c.fetchall()
    for row in rows:
        id = row[0]
        payload = row[1]
        print "ID: " + str(id) + "   " + payload

#session_length_query = "SELECT session_id,started_at,ended_at,AGE(ended_at,started_at),entered_event_payload FROM session_stats WHERE started_at::date>='" + start_date + "' AND started_at<='" + end_date  + "';"
#  ORDER BY AGE(ended_at,started_at) DESC;"
#c.execute(session_length_query)
#session_rows = c.fetchall()
#for session in session_rows:
#    session_id = session[0]
#    started_at = session[1]
#    ended_at = session[2]
#    length = session[3]
#    payload = session[4]
#    print("Session " + str(session[0])  + " Start: " + str(session[1]) + "  Session length: " + str(session[3]))


#for room in rooms_data["rooms"]:
#    print("slug: " + room["slug"] + " SID: " + room["hub_sid"])

    
c.close()
db.close()

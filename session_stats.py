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

start_date = '2020-07-10'
end_date =   '2020-07-14'


#New strategy: use sql INTERVAL to increment
current_hour = 0
current_minute = 0

h = 0
while h < 72:
    session_query = "SELECT COUNT(session_id) FROM session_stats WHERE started_at > timestamp '" + \
                    start_date + " 00:00:00' + INTERVAL '" + str(h) + " hours' AND started_at < timestamp '" + \
                    start_date + " 00:00:00' + INTERVAL '" + str(h+1) + " hours';"
    c.execute(session_query)
    count = c.fetchone()[0]
    time = h % 24
    if h < 24:
        date = start_date
    elif h >= 24 and h < 48:
        date = '2020-07-11'
    elif h >= 48:
        date = '2020-07-12'
    print (date + " " + str(time) + ":00 -  " + str(count))
    h += 1
    




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

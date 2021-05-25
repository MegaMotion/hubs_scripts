#!/usr/bin/python
import sys
#import psycopg2
import requests
import datetime

#r = requests.get('https://cgi.chriscalef.com/add_user/PyUser')
#r = requests.get('https://7eg0pdrtea.execute-api.us-west-2.amazonaws.com/default/HubsEventsLambdaPg')
r = requests.get('https://hubbub6-data.s3-us-west-2.amazonaws.com/entities.json')

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Now: " + str(dt) )

#if (r != None):
#  print ("status: " + str(r.status_code) + "\n",)
#  print (r.text + "\n\n")
  #print (r.raw)
#  with open('response_log.txt', 'wb') as fd:
#    for chunk in r.iter_content(chunk_size=128):
#        fd.write(chunk)




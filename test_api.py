#!/usr/bin/python
import sys
#import psycopg2
import requests

#r = requests.get('https://cgi.chriscalef.com/add_user/PyUser')
r = requests.get('https://7eg0pdrtea.execute-api.us-west-2.amazonaws.com/default/HubsEventsLambdaPg')

if (r != None):
  print ("status: " + str(r.status_code) + "\n",)
  print (r.text + "\n\n")
  #print (r.raw)
  with open('response_log.txt', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)




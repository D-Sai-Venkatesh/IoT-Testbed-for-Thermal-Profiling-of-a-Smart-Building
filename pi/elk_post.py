#!/usr/bin/python
import httplib2
import json
import time
import datetime
import sys
import time
import requests
from time import sleep           # Allows us to call the sleep function to slow down our loop
         # Allows us to call our GPIO pins and names it just GPIO



httplib2.debuglevel     = 0
http                    = httplib2.Http()
content_type_header     = "application/json"

#url = "http://127.0.0.1:5000/homecontrol/api/v1.0/temperature"
#url = "http://10.0.0.43:8070/homecontrol/api/v1.0/temperature"
url = "http://172.16.174.29:8070/homecontrol/api/v1.0/temperature"
#url = "http://192.168.1.22:8000"

def send_data(zone,temp):
	if(temp<-25.00):
		return
	data = {        'Room #':         "zone "+zone,
    	            'Temp in deg C':         temp,
    	            #'humidity in Percentage':     humidity,
    	            #'Pressure in Pascals':pressure,
    	            #'Sound detected': sound_detect_1,
    	            #'Smoke level in ppm': smokelevel["SMOKE"],
    	            #'LPG level in ppm': smokelevel["GAS_LPG"],
    	            #'Carbon Monoxide level in ppm': smokelevel["CO"],
    	            #'Light level in Lux':light_level,
    	            'Timestamp':    str(datetime.datetime.now())
    	    }
	headers = {'Content-Type': content_type_header}
	#print ("Posting %s" % data)
	try:
            response, content = http.request( url,'POST', json.dumps(data), headers=headers)
            #print (response)
	except:
            print("Server is offline")
if __name__=='__main__':
	while(True):
		temp=float(input())
		zone=input()
		send_data(zone,temp)
	

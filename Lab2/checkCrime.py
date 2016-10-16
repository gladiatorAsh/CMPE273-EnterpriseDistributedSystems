"""
This is a simple example to show the basics of writing a Http api
using Spyne. Here's a sample:

curl "http://localhost:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=1"

[
  {
    "total_crime": 50,
    "the_most_dangerous_streets": [
      "00 BLOCK OF VIRGINIA LN",
      "2700 BLOCK OF 25TH AV",
      "4400 BLOCK OF CAMDEN ST"
    ],
    "crime_type_count": {
      "assault": 4,
      "arrest": 2,
      "burglary": 6,
      "robbery": 8,
      "theft": 1,
      "other": 27
    },
    "event_time_count": {
      "12:01am-3am": 3,
      "3:01am-6am": 0,
      "6:01am-9am": 0,
      "9:01am-12noon": 0,
      "12:01pm-3pm": 0,
      "3:01pm-6pm": 0,
      "6:01pm-9pm": 0,
      "9:01pm-12midnight": 47
    }
  }
]

"""


import logging
import urllib2
import json
import requests
import time
import re
import pprint
from collections import OrderedDict
from bs4 import BeautifulSoup
from spyne import Application, srpc, ServiceBase, Iterable, UnsignedInteger, \
	String
from collections import namedtuple
from collections import Counter
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
from datetime import datetime
from objdict import ObjDict
from json import JSONDecoder
from collections import Counter

pp = pprint.PrettyPrinter(indent=4)
Crime= namedtuple('crimes','address,cdid,date,lat,link,lon,type')
temp = OrderedDict()


#def pp_json(json_thing, sort=True, indents=4):
 #   if type(json_thing) is str:
 #       print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
 #   else:
 #      print(json.dumps(json_thing, sort_keys=sort, indent=indents))
 #   return None

class CheckCrimeService(ServiceBase):
	@srpc(String,String,String,_returns=Iterable(String))
	def checkcrime(lat, lon,radius):
		url="http://api.spotcrime.com/crimes.json?lat=%s\&lon=%s\&radius=%s\&key=." %(lat,lon,radius)
	
		data = requests.get(url,timeout=20).json()
		crimes=[Crime(**k) for k in data["crimes"]]
		
		total_crime=len(crimes)
	
		temp['total_crime']=total_crime

		assault=[item for item in crimes if 'Assault' in item.type]   
		arrest=[item for item in crimes if 'Arrest' in item.type]
		burglary=[item for item in crimes if 'Burglary' in item.type]
		robbery=[item for item in crimes if 'Robbery' in item.type]
		theft=[item for item in crimes if 'Theft' in item.type]
		other=[item for item in crimes if 'Other' in item.type]

		crime_address= [item.address for item in crimes]
		
		split_address=[]
		for item in crime_address:
			if item.find('&')>=0:
				current_add=item.split('&')
				split_address.append(current_add[0].strip())	
				split_address.append(current_add[1].strip())
			
			else:
				split_address.append(item.strip())
	
		c=Counter(split_address)
		common=[x[0] for x in c.most_common(3)]

		logging.info(c.most_common(3))

		temp['the_most_dangerous_streets']=common

		temp['crime_type_count']=OrderedDict()
		temp['crime_type_count']['assault']=len(assault)
		temp['crime_type_count']['arrest']=len(arrest)
		temp['crime_type_count']['burglary']=len(burglary)
		temp['crime_type_count']['robbery']=len(robbery)
		temp['crime_type_count']['theft']=len(theft)
		temp['crime_type_count']['other']=len(other)

		slot=[]
		slot1=slot2=slot3=slot4=slot5=slot6=slot7=slot8=0

		for item in crimes:
			date_object = datetime.strptime(item.date,'%m/%d/%y %I:%M %p')
			slot.append(date_object)

		
		curr_date=datetime.now()

		for item in slot:
			if (item>=curr_date.replace(hour=0,minute=1) and item<curr_date.replace(hour=3,minute=0)):
				slot1+=1 
			elif (item>=curr_date.replace(hour=3,minute=1) and item<curr_date.replace(hour=6,minute=0)):
				slot2+=1
			elif (item>=curr_date.replace(hour=6,minute=1) and item<curr_date.replace(hour=9,minute=0)):
				slot3+=1
			elif (item>=curr_date.replace(hour=9,minute=1) and item<curr_date.replace(hour=12,minute=0)):
				slot4+=1
			elif (item>=curr_date.replace(hour=12,minute=1) and item<curr_date.replace(hour=15,minute=0)):
				slot5+=1
			elif (item>=curr_date.replace(hour=15,minute=1) and item<curr_date.replace(hour=18,minute=0)):
				slot6+=1
			elif (item>=curr_date.replace(hour=18,minute=1) and item<curr_date.replace(hour=21,minute=0)):
				slot7+=1
			else:
				slot8+=1
		
		temp['event_time_count']=OrderedDict()
		temp['event_time_count']['12:01am-3am']=slot1
		temp['event_time_count']['3:01am-6am']=slot2
		temp['event_time_count']['6:01am-9am']=slot3
		temp['event_time_count']['9:01am-12noon']=slot4
		temp['event_time_count']['12:01pm-3pm']=slot5
		temp['event_time_count']['3:01pm-6pm']=slot6
		temp['event_time_count']['6:01pm-9pm']=slot7
		temp['event_time_count']['9:01pm-12midnight']=slot8

		yield temp

if __name__ == '__main__':
	# Python daemon boilerplate
	from wsgiref.simple_server import make_server

	logging.basicConfig(level=logging.DEBUG)

	# Instantiate the application by giving it:
	#   * The list of services it should wrap,
	#   * A namespace string.
	#   * An input protocol.
	#   * An output protocol.
	application = Application([CheckCrimeService], 'spyne.examples.hello.http',
		# The input protocol is set as HttpRpc to make our service easy to
		# call. Input validation via the 'soft' engine is enabled. (which is
		# actually the the only validation method for HttpRpc.)
		in_protocol=HttpRpc(validator='soft'),

		# The ignore_wrappers parameter to JsonDocument simplifies the reponse
		# dict by skipping outer response structures that are redundant when
		# the client knows what object to expect.
		out_protocol=JsonDocument(ignore_wrappers=True),
	)

	# Now that we have our application, we must wrap it inside a transport.
	# In this case, we use Spyne's standard Wsgi wrapper. Spyne supports
	# popular Http wrappers like Twisted, Django, Pyramid, etc. as well as
	# a ZeroMQ (REQ/REP) wrapper.
	wsgi_application = WsgiApplication(application)

	# More daemon boilerplate
	server = make_server('127.0.0.1', 8000, wsgi_application)

	logging.info("listening to http://127.0.0.1:8000")
	logging.info("wsdl is at: http://localhost:8000/?wsdl")

	server.serve_forever()
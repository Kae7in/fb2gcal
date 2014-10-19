import facebook
import requests
from apiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
# from oauth2client import 
from secrets import *
from pprint import pprint
from datetime import datetime, timedelta

user = "josh.kelle"

graph = facebook.GraphAPI(facebook_access_token)
profile = graph.get_object(user)
events = graph.get_connections(profile['id'], 'events')

# Perform some action on each post in the collection we receive from
# Facebook.
print("Facebook Events:")
for event in events['data']:
	print(" - " + event['name'])

# Attempt to make a request to the next page of data, if it exists.
#events = requests.get(events['paging']['next']).json()
# When there are no more pages (['paging']['next']), break from the
# loop and end the script.

ghttp = httplib2.Http()
gcred = AccessTokenCredentials(google_access_token, 'fb2gcal hackathon project')
gcred.authorize(ghttp)

service = build("calendar", "v3", http=ghttp)

calendars = service.calendarList().list().execute()

print("\nGoogle Calendars:")
for calendar in calendars['items'] :
	print (" - " + calendar['summary'])
	if calendar['summary'] == "Facebook Events":
		fbEventCalendar = calendar

"""
1. for each fb event
	1. make sure it's not already in any calendar
	2. add it to the calendar
"""

def eventInCalendars(event, calendars):
	for calendar in calendars['items']:
		if eventInCalendar(event, calendar):
			return True
	return False

def eventInCalendar(f_event, calendar):
	calendar_id = calendar['id']
	timezone = f_event["start_time"][-5:]
	timezone = timezone[:-2] + ":" + timezone[-2:]

	def parseFacebookTime(s):
		return datetime.strptime(s[:-5], '%Y-%m-%dT%H:%M:%S')

	def formatGoogleTime(dt):
		s = datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.000')
		return s + timezone

	event_name = f_event['name']
	start_time = parseFacebookTime(f_event['start_time'])
	end_time   = parseFacebookTime(f_event['end_time']) if 'end_time' in f_event else start_time + timedelta(hours=1)
	print('calendarId: ' + calendar_id)
	print('start_time: %s' % start_time)
	print('end_time: %s' % end_time)

	#this is redundant and expensive to perform for every event
	#grab events in g_cal once
	g_events = service.events().list(
		calendarId=calendar_id,
		timeMin=formatGoogleTime(start_time),
		timeMax=formatGoogleTime(end_time)
	).execute()
	for e in g_events['items']:
		if (e['summary'] == f_event['name']):
			return True
	return False

def addEventToCalendar(event, calendar):
	# print "type(event) =", type(event)

	timezone = event["start_time"][-5:]
	timezone = timezone[:-2] + ":" + timezone[-2:]

	def parseFacebookTime(s):
		return datetime.strptime(s[:-5], '%Y-%m-%dT%H:%M:%S')

	def formatGoogleTime(dt):
		s = datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.000')
		return s + timezone

	event_name = event['name']
	start_time = parseFacebookTime(event['start_time'])
	end_time   = parseFacebookTime(event['end_time']) if 'end_time' in event else start_time + timedelta(hours=1)

	body = {
		'summary' : event_name,
		'start' : {
			'dateTime' : formatGoogleTime(start_time)
		},
		'end' : {
			'dateTime' : formatGoogleTime(end_time)
		}
	}

	print "making request: ", body

	created_event = service.events().insert(calendarId=targetCalendar, body=body).execute()

# print "events"
# pprint(events)

for event in events['data']:
	if not eventInCalendars(event, calendars):
		addEventToCalendar(event, fbEventCalendar)
	else:
		print "event already in calendar, skipping"


import facebook
import requests
from apiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
# from oauth2client import 
from secrets import *
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
events = requests.get(events['paging']['next']).json()
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




import facebook
import requests
# from oauth2client import 
from secrets import *

user = "josh.kelle"

graph = facebook.GraphAPI(facebook_access_token)
profile = graph.get_object(user)
events = graph.get_connections(profile['id'], 'events')

# Perform some action on each post in the collection we receive from
# Facebook.
for event in events['data']:
	print(event['name'])

# Attempt to make a request to the next page of data, if it exists.
events = requests.get(events['paging']['next']).json()
# When there are no more pages (['paging']['next']), break from the
# loop and end the script.


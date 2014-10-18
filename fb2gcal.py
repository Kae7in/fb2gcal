import facebook
import requests
import time

access_token = "CAACEdEose0cBAJPPtEdcz0HT3600NVmPP1soxN0wYygm5gBZAdd1ZCuGqmdxOz7QtpWwoZCKEw2Owy73unFDkzGvrBBu4actfiZBzHx7DwHtZCDCbmjMHhJpperCR0zXtPZCPI4jPu2yiRgPfIlfyFPBarmJC8pElsYpVit2QZBgrZAVyXcCXfC7KZCySvK2hMQ97Q259OKxmxXzbMEZCcxdJx"
user = "josh.kelle"

graph = facebook.GraphAPI(access_token)
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

time.sleep(5)
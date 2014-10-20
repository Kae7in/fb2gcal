#!/usr/bin/env python

import json
import google_calendar as gcal
import facebook_events as fb
import filtering

appSettings = {}
userSettings = {}
userState = {}

def loadSettings():
	global appSettings, userSettings, userState

	try:
		with open("app_settings.json", "r") as f:
			appSettings = json.load(f)
		with open("user_settings.json", "r") as f:
			userSettings = json.load(f)
		with open("user_state.json", "r") as f:
			userState = json.load(f)
	
	except:
		print "Error: must run config.py first!"
		return False

	return True

def saveSettings():
	with open("user_settings.json", "w") as f:
		json.dump(userSettings, f, indent=1)
	with open("user_state.json", "w") as f:
		json.dump(userState, f, indent=1)

def log(msg):
	userState["log"].append(msg)

def main():
	
	# load settings
	print "Loading settings..."
	settingsLoaded = loadSettings()
	if not settingsLoaded:
		return

	# refresh tokens if needed
	print "Refreshing access tokens..."
	authModules = {
		"facebook": fb,
		"google": gcal,
	}
	for service, module in authModules.items():
		appAuth = appSettings[service+"_auth"]
		userAuth = userSettings[service+"_auth"]
		token, expire = module.refreshTokens(
			appAuth["client_id"],
			appAuth["client_secret"],
			userAuth["access_token"],
			userAuth["expiration"]
		)
		userAuth["access_token"] = token
		userAuth["expiration"] = expire

	# choose start and end dates
	startDate = None
	endDate = None

	# fetch google events
	print "Fetching existing events from Google Calendar..."
	googleEvents = gcal.getEvents(userSettings["google_auth"]["access_token"], startDate, endDate)

	# fetch facebook events
	print "Fetching Facebook events..."
	fbEvents = fb.getEvents(userSettings["facebook_auth"]["access_token"], startDate, endDate)

	# filter facebook events, queueing create/update tasks
	print "Filtering events..."
	updateTasks, createTasks = filtering.filterEvents(fbEvents, googleEvents)

	# run update google query
	print "Updating existing events on Google Calendar..."
	for task in updateTasks:
		event = None
		gcal.updateEvent(userSettings["google_auth"]["access_token"], event)

	# run create google query
	print "Creating new events on Google Calendar..."
	for task in createTasks:
		event = None
		gcal.createEvent(userSettings["google_auth"]["access_token"], event)

	# update log/visited
	print "Updating log/settings files..."
	saveSettings()

if __name__ == '__main__':
	main()
	print "Done!"
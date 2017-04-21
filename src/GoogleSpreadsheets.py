#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os
import sys
sys.dont_write_bytecode = True

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = '..data/client_secret.json'
APPLICATION_NAME = 'Python script for personal usage'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'sheets.googleapis.com-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

class GSpreadsheet:

	def __init__(self, id):
		self.id = id
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
	
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
		self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	
	def GetSheetsTitles(self):
		result = self.service.spreadsheets().get(spreadsheetId=self.id).execute()
		sheets = result.get('sheets', '')
		titles = []
		for sheet in sheets:
			title = sheet.get("properties", {}).get("title")
			titles.append(title)
		
		return titles
		
	def GetSheetContent(self, sheet_title, arg=''):
		rangeName = sheet_title if arg == '' else sheet_title + '!' + arg

		result = self.service.spreadsheets().values().get(
			spreadsheetId=self.id, range=rangeName).execute()
		values = result.get('values', [])
		content = []
		for row in values:
			content.append(row)
			
		return content
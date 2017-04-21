#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

from GoogleSpreadsheets import GSpreadsheet

def DownloadData(spreadsheetId):
	print('\nLoading spreadsheet: [' + spreadsheetId + ']...\n')
	gSpread = GSpreadsheet(spreadsheetId)
	
	print('Getting spreadsheet sheets...\n')
	sheetsTitles = gSpread.GetSheetsTitles()
	print('found: {0}'.format(str(len(sheetsTitles))))
	
	for i, title in enumerate(sheetsTitles):
		print('List #{0}: [{1}]'.format(i, title))
		
	print('')
	
	data = {}
	for title in sheetsTitles:
		content = gSpread.GetSheetContent(title, 'A2:B')
		# if (content):
			# print('\nList [{0}] content:'.format(title))
			# for row in content:
				# print(''.join(row))
				
		data[str(title)] = content
		
	return data
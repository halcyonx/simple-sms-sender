#!/usr/bin/python
# -*- coding: utf-8 -*-

import DownloadParentGroups
import SenderImpl
import time
import sys
import unicodedata
sys.dont_write_bytecode = True

id = 'spreadsheet id here' # spread sheet id

# data contains data:
# phone_number	|	Name
# therefore indices phone_number is 0, for Name is 1

class Person:

	def __init__(self, phone_number, name):
		assert (len(str(phone_number)) == 11)
		assert (name)
		t = int(phone_number)
		
		self.phone_number = str(phone_number)
		self.name = name
		# dirty supression of unicode
		# self.name = self.__init_name(name)
		# assert(self.name)
		
	def __init_name(self, name):
		f = open('__temp__.txt', 'w')
		f.write(name.encode('ascii'))
		f.close()
		
		new_name = ''
		with open('__temp__.txt') as f:
			new_name = f.readline()
		return new_name
		
	def __str__(self):
		return 'Person(number={0}, name={1})'.format(self.phone_number, self.name)

def GetParentGroups():
	data = DownloadParentGroups.DownloadData(id)
	
	# parentGroups[group][number] = person
	parentGroups = {}
	for group in data:
		rows = data[group]
		
		parentGroups[group] = {}
		
		for row in rows:
			if str(row[0]) not in parentGroups[group]:
				person = Person(str(row[0]), row[1])
				parentGroups[group][person.phone_number] = person
			else:
				print('[INFO] :: {0} is duplicate'.format(str(row[0])))
				
	return parentGroups
		
def PrintGroups(groups):
	print('-' * 50)
	for group in groups:
		print('Group: [{0}]'.format(group))
		for number in groups[group]:
			print('   > ' + number + ' : ' + groups[group][number].name)
			
			
def SendGroupMessage(groupName, group, message):
	assert(message)
	assert(groupName)
	assert(group)
	pattern = '%name%'
	
	sender = SenderImpl.SenderImpl()
	
	# print('Message: [{0}]'.format(message))
	print('Try to send message to group: {0}, {1} persons...'.format(groupName, len(group)))
	
	for number in group:
		person = group[number]
		
		msg = message
		if '%s' in message:
			msg = msg % (person.name)
			
		print('Сообщение: ' + msg)
		
		response = sender.SendSms(person.phone_number, msg, total_price=0)
		print('response: ', response)
	'''
	f = open('__temp__.txt', 'w')
	for number in group:
		person = group[number]
		
		# test
		f.write(person.name.encode("UTF-8"))
		f.write('\n')
	f.close()
	
	with open('__temp__.txt') as f:
		for line in f:
			if len(line) > 1:
				line = line.strip()
				msg = message
				msg = msg % (line)
				print('here Сообщение: ' + msg) '''
		
		# response = sender.SendSms(person.phone_number, msg, total_price=0)
		# print('response: ', response)
		# test break
		# break
		

parentGroups = GetParentGroups()
SendGroupMessage('authors', parentGroups['authors'], 'Доброе утро!')
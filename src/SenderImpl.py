#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True

import urllib
import json
import time

class SenderImpl:

	def __init__(self):
		path = '../data/config'
		self.login = ''
		self.password = ''
		with open('../data/config') as config:
			self.login = config.readline().strip()
			self.password = config.readline().strip()
			
		assert (self.login)
		assert (self.password)
		
		self.errors = {
			1: '������ � ����������.',
			2: '�������� ����� ��� ������.',
			3: '������������ ������� �� ����� �������.',
			4: 'IP-����� �������� ������������ ��-�� ������ ������ � ��������. ���������',
			5: '�������� ������ ����.',
			6: '��������� ��������� (�� ������ ��� �� ����� �����������).',
			7: '�������� ������ ������ ��������.',
			8: '��������� �� ��������� ����� �� ����� ���� ����������.',
			9: '�������� ����� ������ ����������� ������� �� �������� SMS-��������� ���� ����� ���� ���������� �������� �� ��������� ��������� ��������� � ������� ������. '
		}
		print('Config loaded')
		
	def SendSms(self, phones, text, total_price=1):
		assert (len(phones) >= 11)
		assert (self.login)
		assert (self.password)
		assert (text)
		assert (total_price == 1 or total_price == 0)
		
		url = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&fmt=3" % (self.login, self.password, phones, text, total_price)
		# print(url)
		# assert False, 'Test assert'
		answer = json.loads(urllib.urlopen(url).read())
		if 'error_code' in answer:
			# �������� ������
			return errors[answer['error_code']]
		else:
			if total_price == 1:
				# �� ����������, ������ ������ ����
				print('����� ����������: %d SMS, ���� ��������: %s' % (answer['cnt'], answer['cost'].encode('utf-8')))
			else:
				# ��� ���������, ����� �������
				print ('SMS successfully sent')
				return answer
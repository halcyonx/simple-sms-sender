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
			1: 'Ошибка в параметрах.',
			2: 'Неверный логин или пароль.',
			3: 'Недостаточно средств на счете Клиента.',
			4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
			5: 'Неверный формат даты.',
			6: 'Сообщение запрещено (по тексту или по имени отправителя).',
			7: 'Неверный формат номера телефона.',
			8: 'Сообщение на указанный номер не может быть доставлено.',
			9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты. '
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
			# Возникла ошибка
			return errors[answer['error_code']]
		else:
			if total_price == 1:
				# Не отправлять, узнать только цену
				print('Будут отправлены: %d SMS, цена рассылки: %s' % (answer['cnt'], answer['cost'].encode('utf-8')))
			else:
				# СМС отправлен, ответ сервера
				print ('SMS successfully sent')
				return answer
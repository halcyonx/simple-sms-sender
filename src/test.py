#!/usr/bin/python
# -*- coding: utf-8 -*-
with open('test.txt') as test:
	for line in test:
		url = "Привет, %s" % (line)
		print(url)

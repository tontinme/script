#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import urllib
context = urllib.urlopen('http://ws.qunar.com/holidayService.jcp?lane=北京-西宁')
tree = etree.parse(context)
root = tree.getroot()
for node in root[0]:
	if node.attrib["date"] == "2012-07-30":
		for child in node:
			for child_detail in child.attrib.keys():
				if child.attrib["type"] == "go" and int(child.attrib["price"])<2000:
					print child_detail,child.attrib[child_detail]
					#urllib.urlopen('http://api.sms.xxx.com/sms.jcp?c="xxx"')

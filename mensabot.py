# coding: utf8

from errbot import BotPlugin, botcmd
from urllib2 import urlopen
from lxml import etree
from datetime import datetime

class MensaBot(BotPlugin):

	@botcmd
	def mensa(self, mess, args):
		""" Prints the menu @Mensa Uni Karlsruhe for this day (before 2pm) or the next day (2pm and after) in a compact form. """
		result = {}
		lines = ["1", "2", "3", "4/5", "SB", "6"]
		html = etree.HTML(urlopen("http://www.studentenwerk-karlsruhe.de/de/food/?view=ok&STYLE=popup_plain&c=adenauerring&p=1").read())
		
		# Show table for next day after 2pm
		tableindex = 1
		if datetime.now().hour >= 14:
			tableindex = 2
		
		# Each row represents a line.
		rows = [r for r in html.xpath("/html/body/table/tr/td/div/table[" + str(tableindex) + "]/tr") if len(r)]
		for idx, row in enumerate(rows):
			# Don't show special lines like Curry Queen, Cafeteria etc.
			if idx >= len(lines):
				break

			# Each row inside the subtable represents a food item
			for food in row[1].xpath("table/tr"):
			
				# Don't display food items which cost less than €1 or have no assigned price.
				price_nodes = food[1].xpath("span//text()[last()]")
				if len(price_nodes) == 0:
					continue

				price = price_nodes[0].strip().encode("utf-8")
				if price.strip().startswith("0,"):
					continue
				
				# Display only the bold-face part of the food name
				foodname = food[0].xpath("span/b")[0].text.strip().encode("utf-8")
				
				# Append food and price to results
				if lines[idx] not in result:
					result[lines[idx]] = []
					
				result[lines[idx]].append(foodname + " " + price)

		return " ".join(["[" + key + "] " + ", ".join(result[key]) for key in lines if key in result])
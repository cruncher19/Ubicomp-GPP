from lxml import html
import requests
import datetime
import time

#dictionary to store x-path mappings of the HTML elements on the solar power site
xpath_mappings = dict()

config = open('table_mapping.config')

#Currently the metric being collected is peak power today. THis can be changed by setting the below variable
metric = 'Peak Power Today'

metric_value = ""

#Fills the x-path mappings dictionary. This is more for flexibility in the future since we know what metrics we;re capturing
for line in config:
	mapping = line.split('->')
	xpath_mappings[mapping[0]] = mapping[1]

def getPower():
	#Requests and stores page
	page = requests.get('http://newquayweather.com/wxsolarpv.php')

	#Converts text to HTML
	tree = html.fromstring(page.text)
	
	#Get last update date from the solat site
	last_update = tree.xpath(xpath_mappings["Last Update"])[0].text_content()

	#Add seconds to allow conversion
	last_update = last_update + ":00"

	#convert to datetime object
	last_update_datetime = datetime.datetime.strptime(last_update, '%d-%m-%Y %H:%M:%S')

	#get current timestamp
	ts = time.time()

	#Convert to datetime object
	current_time = datetime.datetime.fromtimestamp(ts)

	print "Power data last updated on " + last_update + " GMT"

	#checks to see if last updated date is from a previous day
	if last_update_datetime.day < current_time.day:
		print "Power data is not from today, consider discarding..."


	#If the metric requested is valid, parse the HTML and find the value (text_content)
	if xpath_mappings.has_key(metric):
	    metric_value = tree.xpath(xpath_mappings[metric])[0].text_content()

	#Calls rest API
	requests.get("http://localhost:5000/storePowerProduction?powerLevel=" + metric_value.replace("W", ""))

	return metric_value.replace("W", "")

print "Current power level: " + getPower()
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import logging
import predictor
from utilities import getConfig
import requests

config       = getConfig('config.ini')
arduinoAddress  = config.get('config', 'arduino_address').encode('ascii')

logging.basicConfig()

def update():
	predictor.predict()

def pullPowerProduction():
	# powerProduction = Get the reading from the arduino when the API call is implemented
	# requests.get("http://localhost:5000/storePowerProduction?powerLevel=" + powerProduction)
	print "pulled power production data"


scheduler = BackgroundScheduler()

scheduler.start()

scheduler.add_job(update, 'interval', hours=1)
scheduler.add_job(pullPowerProduction, 'interval', minutes=30)

while True:
	sleep(1)

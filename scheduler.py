from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import logging
import predictor

logging.basicConfig()

def update():
	predictor.predict()

scheduler = BackgroundScheduler()

scheduler.start()

scheduler.add_job(update, 'interval', minutes=1)

while True:
	sleep(1)

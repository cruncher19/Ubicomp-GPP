from flask import Flask
from flask import request
from pyowm import OWM
from utilities import getConfig

config       = getConfig('config.ini')
OWM_API_key  = config.get('config', 'OWM_API_key').encode('ascii')
OWM_location = config.get('config', 'OWM_location').encode('ascii')

app = Flask(__name__)

@app.route('/storePowerProduction')
def storePowerProduction():
	# Pull a weather forcast from Open Weather Map
	powerLevel = request.args.get('powerLevel', '')
	owm = OWM(OWM_API_key)
	obs = owm.weather_at(OWM_location)
	w = obs.get_weather()

	# Get all the variables we want to store in the database
	cloudCover = w.get_clouds()
	windSpeed = w.get_wind()['speed']
	humidity = w.get_humidity()
	pressure = w.get_pressure()['press']
	temperature = w.get_temperature(unit='celsius')['temp']
	status = w.get_status()

	# Figure out if the sun is up(probably important)
	daytime = False
	currTime = w.get_reference_time()
	sunriseTime = w.get_sunrise_time()
	sunsetTime = w.get_sunset_time()
	if(currTime > sunriseTime and currTime < sunsetTime):
		daytime = True

	from db_definition import db, powerProduction

	dbEntry = powerProduction(powerLevel, cloudCover, windSpeed, humidity, pressure,
								temperature, status, daytime)
	db.session.add(dbEntry)
	db.session.commit()
	return "Success!"



if __name__ == '__main__':
	app.run(debug=True)

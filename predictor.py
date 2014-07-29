from numpy import *
from sklearn import linear_model
from pyowm import OWM
from utilities import getConfig

# Accepts an array of weather data and the corresponding power production array
# Creates a linear regression model from the data
# returns an array containing predicted power production for the next three days
def predict(weatherData, powerData):
	# perform multivariate linear regression on the data to find the correlation between weather and power production
	model = linear_model.LinearRegression()
	model.fit(weatherData,powerData)

	# fetch the current forecast
	config = getConfig('config.ini')
	OWM_API_key = config.get('config', 'OWM_API_key').encode('ascii')
	OWM_location = config.get('config', 'OWM_location').encode('ascii')
	owm = OWM(OWM_API_key)
	fc = owm.daily_forecast(OWM_location, limit=3)
	f = fc.get_forecast()

	predictions = []
	for w in f:
		# Get all the variables we want to store in the database
		cloudCover = w.get_clouds()
		windSpeed = w.get_wind()['speed']
		humidity = w.get_humidity()
		pressure = w.get_pressure()['press']
		temperature = w.get_temperature(unit='celsius')['temp']
		status = w.get_status()

		currentWeather = array([cloudCover, windSpeed, humidity, pressure, temperature])

		# use the regression model to generate production predictions based on the current forecast
		# print "Predicted power production: " + str(model.predict(currentWeather))
		predictions.append(model.predict(currentWeather))
	return predictions
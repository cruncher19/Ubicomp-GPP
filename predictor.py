	from numpy import *
	from sklearn import linear_model
	from pyowm import OWM
	from utilities import getConfig
	from db_definition import powerProduction

# Accepts an array of weather data and the corresponding power production array
# Creates a linear regression model from the data
# returns an array containing predicted power production for the next three days
def predict():
	# fetch the current forecast
	config = getConfig('config.ini')
	OWM_API_key = config.get('config', 'OWM_API_key').encode('ascii')
	OWM_location = config.get('config', 'OWM_location').encode('ascii')
	owm = OWM(OWM_API_key)
	fc = owm.daily_forecast(OWM_location, limit=3)
	f = fc.get_forecast()

	predictions = []
	for w in f:
		# Figure out if the sun is up(probably important)
		daytime = 'f'
		currTime = w.get_reference_time()
		sunriseTime = w.get_sunrise_time()
		sunsetTime = w.get_sunset_time()
		if(currTime > sunriseTime and currTime < sunsetTime):
			daytime = 't'
		result = powerProduction.query.filter_by(daytime=daytime, status=w.get_status())
		weatherData = []
		powerData = []
		for r in result:
			weatherData.append([r.cloudCover, r.windSpeed, r.humidity, r.pressure, r.temperature])
			powerData.append([r.powerLevel])
		
		# perform multivariate linear regression on the data to find the correlation between weather and power production
		model = linear_model.LinearRegression()
		model.fit(weatherData,powerData)

		cloudCover = w.get_clouds()
		windSpeed = 0
		humidity = w.get_humidity()
		pressure = w.get_pressure()['press']
		temperature = w.get_temperature(unit='celsius')['temp']
		status = w.get_status()

		currentWeather = array([cloudCover, windSpeed, humidity, pressure, temperature])

		# use the regression model to generate production predictions based on the current forecast
		# print "Predicted power production: " + str(model.predict(currentWeather))
		predictions.append(model.predict(currentWeather))

	return predictions
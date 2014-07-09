from numpy import *
from sklearn import linear_model
from pyowm import OWM
from utilities import getConfig


# add code to pull data out of database through REST API when documentation on this is available
powerData = None
# Some fake placheolder data
weatherData = array([[1,2,3,4,5],
                    [5,4,3,2,1],
                    [2,3,1,5,4],
                    [3,4,1,2,5]])

powerData = array([[10],
                    [9],
                    [8],
                    [7]])

# perform multivariate linear regression on the data to find the correlation between weather and power production
model = linear_model.LinearRegression()
model.fit(weatherData,powerData)

# fetch the current forecast
config = getConfig('config.ini')
OWM_API_key = config.get('config', 'OWM_API_key').encode('ascii')
OWM_location = config.get('config', 'OWM_location').encode('ascii')
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

currentWeather = array([cloudCover, windSpeed, humidity, pressure, temperature])

# use the regression model to generate production predictions based on the current forecast
model.predict(currentWeather)
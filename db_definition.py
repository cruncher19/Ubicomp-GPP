from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from utilities import getConfig

config = getConfig('config.ini')
db_uri = config.get('config', 'db_uri');

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
db = SQLAlchemy(app)

class powerProduction(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	timestamp   = db.Column(db.DateTime, default=db.func.now(), nullable=False)
	powerLevel  = db.Column(db.Float, nullable=False)
	cloudCover  = db.Column(db.Integer, nullable=False)
	windSpeed   = db.Column(db.Float, nullable=False)
	humidity    = db.Column(db.Integer, nullable=False)
	pressure    = db.Column(db.Integer, nullable=False)
	temperature = db.Column(db.Float, nullable=False)
	status      = db.Column(db.String(30), nullable=False)
	daytime     = db.Column(db.Boolean, nullable=False)

	def __init__(self, powerLevel, cloudCover, windSpeed,
					humidity, pressure, temperature, status, daytime):
		self.powerLevel  = powerLevel
		self.cloudCover  = cloudCover
		self.windSpeed   = windSpeed
		self.humidity    = humidity
		self.pressure    = pressure
		self.temperature = temperature
		self.status      = status
		self.daytime     = daytime

	def __repr__(self):
		return '<powerProduction PL: ' + self.powerLevel + ', timestamp: ' + self.timestamp + '>'

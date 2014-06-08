from configparser import ConfigParser

def getConfig(filename):
	config = ConfigParser()
	config.read(filename)
	return config
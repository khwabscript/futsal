import json

def writeJson(data, dataFile):
	jsonData = json.JSONEncoder().encode(data)
	f = open(dataFile, 'w')
	f.write(jsonData)
	f.close()
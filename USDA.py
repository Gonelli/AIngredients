import shlex
import subprocess
import json

# Tony's data.gov registered API key
API_key = "vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1"

def searchCurl(q):
	cmd = '''curl -H "Content-Type:application/json" -d '{"q":"''' + q + '''","ds":"Standard Reference","max":"5","offset":"0"}' ''' + API_key + '''@api.nal.usda.gov/ndb/search'''
	args = shlex.split(cmd)
	process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	return stdout

def getFoodID(q):
	myJson = json.loads(searchCurl(q))
	return myJson["list"]["item"][0]["ndbno"]

def reportCurl(nbdno, reportType):
	cmd = '''curl -H "Content-Type:application/json" -d '{"ndbno":["''' + "\",\"".join([str(x) for x in nbdno]) + '''"],"type":"''' + reportType + '''"}' ''' + API_key + '''@api.nal.usda.gov/ndb/V2/reports'''
	args = shlex.split(cmd)
	process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	return stdout


# def parseCurl(stdout):
# 	return stdout

###############################################################################

searchTerms = "salted butter"
reportType = "b"
reportJson = json.loads(reportCurl([getFoodID(searchTerms)], reportType))

# Name of ingredient
print(reportJson["foods"][0]["food"]["desc"]["name"])
# Name of nutrient 0 (water)
print(reportJson["foods"][0]["food"]["nutrients"][0]["name"])

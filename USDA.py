import shlex
import subprocess
import json

# Tony's data.gov registered API key
API_key = "vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1"

class Ingredient:
	reportJson = None
	name = ""
	nutrients = {} # Nutrient name: (Amount per 100g of ingredient, Unit)
	nutrientsDetailed = [] # Fully detailed nutient list with measurement options

	def __init__(self, searchTerms):
		# Defaults to [b]asic report stats
		self.reportJson = json.loads(self.getReport([self.getFoodID(searchTerms, "Standard Reference")], "b"))
		self.name = self.reportJson["foods"][0]["food"]["desc"]["name"]
		self.nutrient0 = self.reportJson["foods"][0]["food"]["nutrients"][0]["name"]

		# Add all nutrient lists to nutrients[]
		for nutrient in self.reportJson["foods"][0]["food"]["nutrients"]:
			self.nutrientsDetailed.append(nutrient)
			self.nutrients[nutrient["name"]] = (nutrient["value"], nutrient["unit"])

	"""
	Takes an input string (q) and searches USDA's database to get a list of possible matching non-branded food items. Also takes "Standard Reference" or "Branded Food Products" inputs. Returns the nbdno of the top result.
	"""
	def getFoodID(self, q, ds):
		cmd = '''curl -H "Content-Type:application/json" -d '{"q":"''' + q + '''","ds":"''' + ds + '''","max":"5","offset":"0"}' ''' + API_key + '''@api.nal.usda.gov/ndb/search'''
		args = shlex.split(cmd)
		process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		myJson = json.loads(stdout)

		try:
			# for item in myJson["list"]["item"]:
			# 	print(item["name"])
			return myJson["list"]["item"][0]["ndbno"]
		except:
			if ds is "Branded Food Products":
				return stderr
			else:
				return self.getFoodID(q, "Branded Food Products")	
	
	"""
	Takes an food ID (nbdno) and a report type character ([b]asic, [f]ull, or [s]tats), then returns a json file of the food's nutritional data. 
	"""
	def getReport(self, nbdno, reportType):
		cmd = '''curl -H "Content-Type:application/json" -d '{"ndbno":["''' + "\",\"".join([str(x) for x in nbdno]) + '''"],"type":"''' + reportType + '''"}' ''' + API_key + '''@api.nal.usda.gov/ndb/V2/reports'''
		args = shlex.split(cmd)
		process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		# parsed = json.loads(stdout)
		# print(json.dumps(parsed, indent=4, sort_keys=True))
		return stdout


###############################################################################
myIngredient = Ingredient("Ready-to-bake corn tortillas")
# print(myIngredient.reportJson)

# measures = myIngredient.reportJson["foods"][0]["food"]["nutrients"][0]["measures"]

# for measure in measures:
# 	print(measure["label"])

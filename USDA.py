import shlex
import subprocess
import json

# Tony's data.gov registered API key
API_key = "vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1"

class Ingredient:

	def __init__(self, searchTerms):
		# Defaults to [b]asic report stats
		self.reportJson = json.loads(self.getReport([self.getFoodID(searchTerms, "Standard Reference")], "b"))
		self.name = self.reportJson["foods"][0]["food"]["desc"]["name"]
		self.nutrients = {} # Nutrient name: (Amount per 100g of ingredient, Unit)
		self.nutrientsDetailed = [] # Fully detailed nutient list with measurement options


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

	"""
	Returns the amount of nutrientType for the ingredient in grams, given a quantity of the ingredient in grams
	"""
	def getNutrientValue(self, nurtientType, quantity):
		for nutrientSection in self.reportJson["foods"][0]["food"]["nutrients"]:
			print nutrientSection
			if nutrientSection["name"].lower() == nurtientType.lower():
				quantityString = str(float(nutrientSection["value"]) / 100 * quantity) + " " +nutrientSection["unit"]
				return self.convertQuantity(quantityString)
		return 0
		# print (self.reportJson["foods"][0]["food"]["nutrients"])

	"""
	Takes a string of ingredient amount and unit type, converts this ingredient's quantity to grams
	"""
	def convertQuantity(self, quantity):
		amount = float(quantity.split(" ", 1)[0])
		unit = quantity.split(" ", 1)[1]

		if unit == "oz":
			amount *= 28.34952	# 1 oz is ~28.34952 grams
		# Check is tsp is a measurement option first, then fall back to these
		elif unit == "teaspoons":
			amount *= 4.93	# 1 tsp of WATER is ~4.93, so possible density issues
		elif unit == "cups":
			amount *= 236.6 # 1 cup of WATER is ~236.6, so possible density issues
		elif unit == "g":
			amount *= 1.0
		elif unit == "mg":
			amount /= 1000.0
		else:
			measures = self.reportJson["foods"][0]["food"]["nutrients"][0]["measures"]
			converted = False
			for measure in measures:
				label = measure["label"]
				if label.lower() in unit.lower(): # if tortilla in tortillas, e.g.
					if measure["eunit"] == "g":
						amount *= measure["eqv"]
					elif measure["eunit"] == "ml":
						amount *= measure["eqv"] # Assumes water, where 1g/ml
					else:
						assert False, "Don't know the unit label"
					converted = True
					break
			if not converted:
				assert False, "Don't know the unit label"
		return amount


###############################################################################
# myIngredient = Ingredient("Ready-to-bake corn tortillas")

# print myIngredient.convertQuantity("1 Tortilla")
# print myIngredient.getNutrientValue("protein", 50)
# print(myIngredient.reportJson)

# measures = myIngredient.reportJson["foods"][0]["food"]["nutrients"][0]["measures"]

# for measure in measures:
# 	print(measure["label"])

from USDA import Ingredient

def parseRecipes():
	with open("Recipe List.txt", "r") as ins:
		allRecipes = {}
		ingrDict = {}
		recipeName = "[None]"
		for line in ins:
			if line[0] is '~':		# Current recipe done, begin on the next
				temp = ingrDict.copy()
				allRecipes[recipeName] = temp
				ingrDict = {}
				recipeName = "[None]"
				continue
			elif line[0] is chr(9):	# If line begins with a tab
				ingrMeasure = [s for s in line[1:-1].split(chr(9)) if s] # Delimits tabs
				ingrDict[ingrMeasure[0]] = ingrMeasure[1]
				continue
			else:	# Is recipe name
				recipeName = line[:-2]
			# print allRecipes
		print allRecipes

class Recipe:
	vegetarian = False
	ingredients = {}

	def __init__(self, ingredientDict):
		ingredients = ingredientDict.copy()

	"""
	Adds ingredient and subsequent quantity to ingredients list
	"""
	def addIngredient(self, ingredient, quantity):
		ingredients[ingredient] = quantity # ingredient should be of Ingredient type
	"""
	Converts an ingredient's quantity to grams
	"""
	def convertQuantity(self, quantity):
		amount = quantity.split(" ", 1)[0]
		unit = quantity.split(" ", 1)[1]

		if unit is "oz":
			amount *= 28.34952	# 1 oz is ~28.34952 grams
		# Check is tsp is a measurement option first, then fall back to these
		elif unit is "teaspoons":
			amount *= 4.93	# 1 tsp of WATER is ~4.93, so possible density issues
		elif unit is "cups":
			amount *= 236.6 # 1 cup of WATER is ~236.6, so possible density issues
		else:
			measures = myIngredient.reportJson["foods"][0]["food"]["nutrients"][0]["measures"]
			converted = False
			for measure in measures:
				label = measure["label"]
				if label in unit: # if tortilla in tortillas, e.g.
					if measure["eunit"] is "g":
						amount *= measure["eqv"]
					elif measure["eunit"] is "ml":
						amount *= measure["eqv"] # Assumes water, where 1g/ml
					else:
						assert False, "Don't know the unit label"
					converted = True
					break
			if not converted:
				assert False, "Don't know the unit label"
		return amount


	# TODO: Types of flags on food
	# [vegetarian, cuisine, palette, heaviness]

parseRecipes()
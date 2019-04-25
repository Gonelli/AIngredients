from USDA import Ingredient

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
	def.convertQuantity(self, quantity):
		amount = quantity.split(" ", 1)[0]
		unit = quantity.split(" ", 1)[1]

		if unit is "oz":
			amount *= 28.34952	# 1 oz is ~28.34952 grams
		# Check is tsp is a measurement option first, then fall back to these
		else if unit is "teaspoons":
			amount *= 4.93	# 1 tsp of WATER is ~4.93, so possible density issues
		else if unit is "cups":
			amount *= 236.6 # 1 cup of WATER is ~236.6, so possible density issues
		else:
			measures = myIngredient.reportJson["foods"][0]["food"]["nutrients"][0]["measures"]
			converted = False
			for measure in measures:
				label = measure["label"]
				if label in unit: # if tortilla in tortillas, e.g.
					if measure["eunit"] is "g":
						amount *= measure["eqv"]
					else if measure["eunit"] is "ml":
						amount *= measure["eqv"] # Assumes water, where 1g/ml
					else:
						assert False, "Don't know the unit label"
					converted = True
					break
			if not converted
				assert False, "Don't know the unit label"
		return amount


	# TODO: Types of flags on food
	# [vegetarian, cuisine, palette, heaviness]
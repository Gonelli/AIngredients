from USDA import Ingredient

"""
Goes through 'Recipe List.txt' and parses all of the recipe information.
Returns a dictionary of many recipes, structured as follows:
{recipeName: ({ingredientName: measurement, ingredientName: measurement}, [flag, flag])}

Use Recipe() on a recipe to get detailed nutritional information. This avoids requesting USDA info for each unused recipe.
"""
def parseRecipes():
	with open("Recipe List.txt", "r") as ins:
		allRecipes = {}
		ingrDict = {}
		recipeName = "[None]"
		flags = []
		for line in ins:
			if line[0] is '~':		# Current recipe done, begin on the next
				if line[1] is not ' ':
					assert False, "Need a space by the flags"
				flags = line[2:-1].lower().split(", ")
				ingrDictCopy = ingrDict.copy()
				allRecipes[recipeName] = (ingrDictCopy, flags)
				ingrDict = {}
				recipeName = "[None]"
				continue
			elif line[0] is chr(9):	# If line begins with a tab
				ingrAndMeasure = [s for s in line[1:-1].split(chr(9)) if s] # Delimits tabs
				ingrDict[ingrAndMeasure[0]] = ingrAndMeasure[1]
				continue
			else:	# Is recipe name
				recipeName = line[:-2]
		return allRecipes

class Recipe:
	#ingredients = {} # {Ingredient: measurement, Ingredient: measurement...}
	#flags = [] # [Vegetarian/meat, cuisine, palette, meal]

	def __init__(self, recipeName, hollowRecipe, hollowFlags):
		self.ingredients = {} # {Ingredient: measurement, Ingredient: measurement...}
		self.flags = [] # [Vegetarian/meat, cuisine, palette, meal]
		self.flags = hollowFlags
		for ingredientName in hollowRecipe.keys():
			fullIngredient = Ingredient(ingredientName)
			self.ingredients[fullIngredient] = hollowRecipe[ingredientName]

	"""
	Adds ingredient and subsequent quantity to ingredients list
	"""
	def addIngredient(self, ingredient, quantity):
		self.ingredients[ingredient] = quantity # ingredient should be of Ingredient type


###############################################################################
'''
# Demonstrate getting a Recipe
allRecipes = parseRecipes()
for recipeName in allRecipes.keys():
	if "Chicken Noodle Soup".lower() in recipeName.lower():	# Find recipe you want
		myRecipe = Recipe(recipeName, allRecipes[recipeName][0], allRecipes[recipeName][1]) # Create Recipe object
		for ingredient in myRecipe.ingredients:
			print ingredient
			# for nutrientSection in self.reportJson["foods"][0]["food"]["nutrients"]:

# 		print myRecipe.ingredients
# 		print myRecipe.flags
'''
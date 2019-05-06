from Recipes import *
from USDA import *
from recommender import *
from qLearning import *


def main():
	myUser = User(.5)
	userGender = "female"
	userHeight = 0
	userWeight = 0
	userAge = 0
	userMeal = "dinner"

	hungry = True
	loop = 0
	TEST = True

	allRecipes = parseRecipes()
	recipeList = []
	if not TEST:
		for recipeName in allRecipes.keys():
			recipeList.append(Recipe(recipeName, allRecipes[recipeName][0],allRecipes[recipeName][1]))

	print "\n\n> Greetings. Welcome to AIngredients! Here to spice up your recipes."
	print "> Would you prefer to go by Male or Female nutritional recomendations?"


	# Gender
	while True:
		userInput = raw_input("")
		if 'm' is userInput.lower()[0]:
			userGender = "male"
			break
		elif 'f' is userInput.lower()[0]:
			userGender = "female"
			break

		print "\n> Sorry, please try again. Use 'M' for Male or 'F' for Female."
		print "> Would you prefer to go by Male or Female nutritional recomendations?"

	print "\n> Good! Now, how tall are you in centimeters?"

	# Height
	while True:
		userInput = raw_input("")
		if str.isdigit(userInput):
			userHeight = float(userInput)
			break

		print "\n> Sorry, please try again. Enter your height as an integer."
		print "> How tall are you in centimeters?"

	print "\n> Right-o! Now, how much do you weigh in kgs or lbs? (We won't tell!)"
	print "> Enter as X lbs or X kgs"

	# Weight
	while True:
		userInput = raw_input("")
		if str.isdigit(userInput[:-4]) and userInput[-3:].lower() == "kgs":
			userWeight = float(userInput[:-4])
			break
		elif str.isdigit(userInput[:-4]) and userInput[-3:].lower() == "lbs":
			userWeight = float(userInput[:-4]) * 0.453592
			break

		print "\n> Sorry, please try again. How much do you weigh?"
		print "> Enter as X lbs or X kgs"

	print "\n> Cool, almost done! How old are you? (This program is rated PG-13 (I kid))"

	# Age
	while True:
		userInput = raw_input("")
		if str.isdigit(userInput):
			userAge = float(userInput)
			break

		print "\n> Sorry, please try again. Enter your age as an integer."
		print "> How old are you?"

##########################################################################
##                             BEGIN LOOP                               ##
##########################################################################

	while hungry:
		loop += 1

		# Meal
		print "\n> Sooooo.... Is this breakfast, lunch, or dinner?"

		while True:
			userInput = raw_input("")
			if userInput.lower()[0] is 'b':
				userMeal = "breakfast"
				break
			elif userInput.lower()[0] is 'l':
				userMeal = "lunch"
				break
			elif userInput.lower()[0] is 'd':
				userMeal = "dinner"
				break

			print "\n> Sorry, please try again."
			print "> Is this breakfast, lunch, or dinner?"

		# Vegetarian
		print "\n> Nice. Now, are you looking for a vegetarian option?"

		isVege = True
		while True:
			userInput = raw_input("")
			if 'y' is userInput.lower()[0]:
				break
			elif 'n' is userInput.lower()[0]:
				isVege = False
				break

			print "\n> Sorry, please try again."
			print "> Are you looking for a vegetarian option?"

		# Cuisine
		print "\n> Okay. What kind of cuisine are you looking for?"

		preferredCuisine = None
		while True:
			userInput = raw_input("")
			if userInput.lower() == "none":
				preferredCuisine = None
				break
			elif not str.isdigit(userInput):
				preferredCuisine = userInput
				break

			print "\n> Sorry, please try again."
			print "> What kind of cuisine are you looking for?"

		# Flavor
		print "\n> And what kind of flavor do you want?"

		preferredCuisine = None
		while True:
			userInput = raw_input("")
			if userInput.lower() == "none":
				preferredFlavor = None
				break
			elif not str.isdigit(userInput):
				preferredFlavor = userInput
				break

			print "\n> Sorry, please try again."
			print "> What kind of flavor do you want?"

		# Find a recipe
		print "> Finding a recipe, please wait..."
		myRecipe = ""
		if not TEST:
			myRecipe = recommend(recipeList, [userMeal, userGender, userHeight, userWeight, userAge], [isVege, preferredFlavor, preferredCuisine])
		else:
			for recipeName in allRecipes.keys():
				if "Beef and Broccoli Stir Fry".lower() in recipeName.lower():	# Find recipe you want
					myRecipe = Recipe(recipeName, allRecipes[recipeName][0], allRecipes[recipeName][1]) # Create Recipe object

		# Modify recipe after a couple go arounds
		if loop > 3:
			myRecipe = recommendModifiedRecipe(myUser, myRecipe, flagGrades)
		
		# Print recipe
		for ingredient in myRecipe.ingredients.keys():
			print "{0:22} {1}".format(ingredient.easyName+":",myRecipe.ingredients[ingredient])
			# print ingredient.easyName + " " + myRecipe.ingredients[ingredient]

		print "> Did you like that recipe?"
		print "> Please grade the following aspects from -5 to 5"

		# Ask user to grade the recipe based on flags
		flagGrades = {}
		for flag in myRecipe.flags:
			print "> Flag: ", flag.title()

			while True:
				userInput = raw_input("")
				try:

					if int(userInput) >= -5 and int(userInput) <= 5:
						flagGrades[flag] = int(userInput)
						break
				except:
					userInput = ""
				print "\n> Sorry, please try again. Enter your grade between -5 and 5."
				print "> Flag: ", flag.title()

		# Update Q-values
		updateWeights(myUser, myRecipe, flagGrades)

		print "\n> Wasn't that fun? How about another meal, whenever you're ready?"
		while True:
			userInput = raw_input("")
			if 'y' is userInput.lower()[0] or userInput.lower() == "sure":
				break
			elif 'n' in userInput.lower()[0]:
				hungry = False
				break

			print "\n> Sorry, please try again. Use 'Y' for Yes or 'N' for No."
			print "> Would you like another meal, whenever you're ready?"

if __name__ == "__main__":
	# execute only if run as a script
	main()
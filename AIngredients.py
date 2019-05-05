from Recipes import *
from USDA import *
from recommender import *
from qLearning import *


def main():
	userGender = ""
	userHeight = 0
	userWeight = 0
	userAge = 0
	userMeal = "dinner"
	allRecipes = parseRecipes()

	print "\n\n> Greetings. Welcome to AIngredients! Here to spice up your recipes."
	print "> Would you prefer to go by Male or Female nutritional recomendations?"


	# # Gender
	# while True:
	# 	userInput = raw_input("")
	# 	if 'm' is userInput.lower()[0]:
	# 		userGender = "male"
	# 		break
	# 	elif 'f' in userInput.lower()[0]:
	# 		userGender = "female"
	# 		break

	# 	print "\n> Sorry, please try again. Use 'M' for Male or 'F' for Female."
	# 	print "> Would you prefer to go by Male or Female nutritional recomendations?"

	# print "\n> Good! Now, how tall are you in centimeters?"

	# # Height
	# while True:
	# 	userInput = raw_input("")
	# 	if str.isdigit(userInput):
	# 		userHeight = float(userInput)
	# 		break

	# 	print "\n> Sorry, please try again. Enter your height as an integer."
	# 	print "> How tall are you in centimeters?"

	# print "\n> Right-o! Now, how much do you weigh in kgs or lbs? (We won't tell!)"
	# print "\n> Enter as X lbs or X kgs."

	# # Weight
	# while True:
	# 	userInput = raw_input("")
	# 	if str.isdigit(userInput[:-4]):
	# 		print userInput[-3:]
	# 		userWeight = float(userInput[:-4])
	# 		break

	# 	print "\n> Sorry, please try again. Enter as X lbs or X kgs."
	# 	print "> How much do you weigh in kilograms?"

	# print "\n> Cool, almost done! How old are you? (This program is rated PG-13 (I kid))"

	# # Age
	# while True:
	# 	userInput = raw_input("")
	# 	if str.isdigit(userInput):
	# 		userAge = float(userInput)
	# 		break

	# 	print "\n> Sorry, please try again. Enter your age as an integer."
	# 	print "> How old are you?"

	print "Finding a recipe, please wait..."
	# myRecipe = recommend(allRecipes, [userMeal, userGender, userHeight, userWeight, userAge], [False, None])
	myRecipe = ""

	for recipeName in allRecipes.keys():
		if "Chicken Noodle Soup".lower() in recipeName.lower():	# Find recipe you want
			myRecipe = Recipe(recipeName, allRecipes[recipeName][0], allRecipes[recipeName][1]) # Create Recipe object



	print API_requests
	print "Did you like that recipe?"
	print "Please grade the following aspects from -5 to 5"

	flagGrades = {}
	for flag in myRecipe.flags:
		print "Flag: ", flag.title()

		while True:
			userInput = raw_input("")
			try:

				if int(userInput) >= -5 and int(userInput) <= 5:
					flagGrades[flag] = int(userInput)
					break
			except:
				userInput = ""
			print "\n> Sorry, please try again. Enter your grade between -5 and 5."
			print "Flag: ", flag.title()

	print flagGrades
	myUser = User(.5)
	updateWeights(myUser, myRecipe, flagGrades)
	myRecipe.ingredients


if __name__ == "__main__":
	# execute only if run as a script
	main()
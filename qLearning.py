# for a recipe, get the flags, and the rating that the user gave
# if the rating is good, increase the rating for each ingredient towards the flag category
# if bad, decrease it
import sys

#and then eventually, we can dynamically generate new recipes based on ingredients that are towards

class User:
    # dictionary of weights for each possible flag
    ingredient_weights = {}
    #possibly add constraints for users
    #how fast the user wants to tweak recipes
    alpha = 0.5
    constraints = {}

    def __init__(self, alpha, **constraints):
        self.alpha = alpha
        self.constraints = constraints 

"""
user: User object with defined ingredient weights
recipe: Recipe object with defined ingredients and flags
grades: passed in user ratings for each category the recipe is associated with
"""
def updateWeights(user, recipe, grades):
    # get recipe flags and iterate over each
    for (category, grade) in grades:
        # grades should be on a scale from -5 to 5 so that updating weights is easy
        for ingredient in recipe:
            user.ingredient_weights[category][ingredient.name] = sqrt(user.ingredient_weights[category] + (alpha * grade * ingredient.convertQuantity(recipe[ingredient])))

def recommendModifiedRecipe(user, recipe, flags):
    #swap out the minimum ingredient with something new
    min_ingredient = (None, sys.maxint)
    for flag in flags:
        weights = user.ingredient_weights[flag]
        for ingredient in recipe.ingredients:
            if weights[ingredient] < min_ingredient[1]:
                #this is new minimum
                min_ingredient = (ingredient, weights[ingredient])
    # create a copy of the original recipe, swap the old ingredient with a new one, and return
    sorted_ingredients = sorted(user.ingredient_weights.items(), key=lambda x: x[1], reverse=True)
    ingredient_names = [ingredient.name for ingredient in recipe.weights]
    new_recipe = recipe.copy()
    for ingredient in sorted_ingredients:
        if ingredient.name not in ingredient_names:
            # find the equivalent value of the new ingredient for the old ingredient
            original_grams = min_ingredient[0].convertQuantity(recipe.ingredients[min_ingredient])
            # amount of grams in one cup of the new ingredient
            new_grams = ingredient.convertQuantity('1.0 cups') 
            new_cups = (original_grams / new_grams) 
            new_value = str(round(new_cups, 2)) + ' cups'
            del new_recipe[min_ingredient]
            new_recipe[ingredient] = new_value
            return
    #should not reach here

#FEATURE FUNCTIONS FOR VARIOUS NUTRIENT TYPES

            




# food_weights = [4.0, 3.0, 9.0] #weights for cheese, paprika, horseradish
# alpha = 0.5

# def cheese_function(amount):
#     #cheese is fattening, so more will decrease q value
#     return 1.0 / (amount ** 0.5)

# def paprika_function(amount):
#     #paprika is relatively healthy, but still not our healthiest ingredient
#     return 0.5 * amount

# def horseradish_function(amount):
#     #horseradish is very healthy, increasing should directly increase q value
#     return amount


# def qLearning(reward, volumes):
#     feature_functions =  [cheese_function, paprika_function, horseradish_function]
#     #carries out an approximate q learning algorithm that uses features with
#     #weights
#     for index in range(len(food_weights)):
#         food_weights[index] = food_weights[index] + (alpha * reward * feature_functions[index](volumes[index]))
#     print("Updated weights")
#     print(food_weights)
# if __name__ == '__main__':

#     print("Welcome to your AI Cook Assistant!")
#     while True:
#         advanceKey = input("Press anything to continue or type 'q' to quit: ")
#         if advanceKey == 'q':
#             break
#         cheese = float(input("Enter cheese volume: "))
#         paprika = float(input("Enter paprika volume: "))
#         horseradish = float(input("Enter horseradish volume: "))
#         reward = float(input("Your rating from 1 (worst) to 10 (best): "))
#         qLearning(reward, [cheese, paprika, horseradish])

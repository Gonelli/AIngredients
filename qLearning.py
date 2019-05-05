# for a recipe, get the flags, and the rating that the user gave
# if the rating is good, increase the rating for each ingredient towards the flag category
# if bad, decrease it
import sys
from math import sqrt
import copy

#and then eventually, we can dynamically generate new recipes based on ingredients that are towards

WEIGHT_INDEX = 0
OBJ_INDEX = 1

class WeightsDictionary:
    def __init__(self):
       self.dict = {}

    def __getitem__(self, key):
        if key not in self.dict:
            self.dict[key] = {}
        return self.dict[key]

    def __str__(self):
        result = ''
        for (key, dictionary) in self.dict.items():
            result += key + ': {'
            for (name, tup) in dictionary.items():
                result += '{' + name + ': ' + str(tup[WEIGHT_INDEX]) + '}, '
            result = result[0: len(result) - 2]
            result += '}, '
        result = result[0: len(result) - 2]
        result += '}'
        return result

class User:
    # dictionary of weights for each possible flag
    ingredient_weights = WeightsDictionary()
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
    for (category, grade) in grades.items():
        # grades should be on a scale from -5 to 5 so that updating weights is easy
        for (ingredient, quantity) in recipe.ingredients.items():
            raw_quantity = user.ingredient_weights[category].get(ingredient.name, (0.0, None))[WEIGHT_INDEX] + (user.alpha * grade * ingredient_feature_function(ingredient, quantity))
            user.ingredient_weights[category][ingredient.name] = (sqrt(abs(raw_quantity)) * ((raw_quantity / raw_quantity) if raw_quantity > 0 else 0), ingredient)
    print(user.ingredient_weights)


def recommendModifiedRecipe(user, recipe, flags):
    #swap out the minimum ingredient with something new in same category
    min_ingredient = (None, sys.maxint, None)
    for flag in flags:
        weights = user.ingredient_weights[flag]
        for (ingredient, quantity) in recipe.ingredients.items():
            if ingredient.name not in weights:
                continue
            if weights[ingredient.name][WEIGHT_INDEX] < min_ingredient[1]:
                #this is new minimum
                min_ingredient = (ingredient, weights[ingredient.name][WEIGHT_INDEX], flag)
    # create a copy of the original recipe, swap the old ingredient with a new one, and return
    if min_ingredient[0] is None:
        # we have never seen any of these ingredients before, return the original recipe, unmodified
        return recipe
    sorted_ingredients = sorted(user.ingredient_weights[flag].items(), key=lambda x: x[1][WEIGHT_INDEX], reverse=True)
    ingredient_names = {ingredient.name for (ingredient, quantity) in recipe.ingredients.items()}
    new_recipe = copy.copy(recipe)
    for (ingredient, tup) in sorted_ingredients:
        if ingredient not in ingredient_names:
            # find the equivalent value of the new ingredient for the old ingredient
            original_grams = min_ingredient[0].convertQuantity(recipe.ingredients[min_ingredient[0]])
            # amount of grams in one cup of the new ingredient
            new_grams = tup[OBJ_INDEX].convertQuantity('1.0 cups') 
            new_cups = (original_grams / new_grams) 
            new_value = str(round(new_cups, 2)) + ' cups'
            # delete the old ingredient
            new_recipe.ingredients.pop(min_ingredient[0], None)
            new_recipe.ingredients[tup[OBJ_INDEX]] = new_value
            return new_recipe
    #should not reach here

"""
gives a score to each ingredient based on amount of carbs, lipids, protein, and fiber
"""
def ingredient_feature_function(ingredient, quantity_raw):
    score = 0.0
    amount = ingredient.convertQuantity(quantity_raw)
    carbs = ingredient.getNutrientValue("Carbohydrate, by difference", amount)
    if carbs is not None:
        # 50 grams of carbs per meal is ideal
        score += (-0.04 * ((carbs - 50) ** 2)) + 100
    lipids = ingredient.getNutrientValue("Total lipid (fat)", amount)
    if lipids is not None:
        # 15 grams of fat per meal is ideal
        score += ((-2.0 / 15.0) * ((lipids - 15.0) ** 2)) + 30
    protein = ingredient.getNutrientValue("Protein", amount)
    if protein is not None:
        score += ((-1.0 / 9.0) * ((protein - 18.0) ** 2)) + 36
    fiber = ingredient.getNutrientValue("Fiber, total dietary", amount)
    if fiber is not None:
        score += ((-1.0 / 5.0) * ((fiber - 10.0) ** 2)) + 20
    return score
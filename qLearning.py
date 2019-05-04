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
        for (ingredient, quantity) in recipe.ingredients:
            user.ingredient_weights[category][ingredient.name] = sqrt(user.ingredient_weights[category] + (user.alpha * grade * ingredient_feature_function(ingredient, quantity)))

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

"""
gives a score to each ingredient based on amount of carbs, lipids, protein, and fiber
"""
def ingredient_feature_function(ingredient, quantity_raw):
    score = 0.0
    amount = ingredient.convertQuantity(quantity_raw)
    carbs = ingredient.getNutrientValue("Carbohydrate, by difference", amount)
    if carbs is not None:
        # 50 grams of carbs per meal is ideal
        score += (-0.04 * ((carbs[0] - 50) ** 2)) + 100
    lipids = ingredient.getNutrientValue("Total lipid (fat)", amount)
    if lipids is not None:
        # 15 grams of fat per meal is ideal
        score += ((-2.0 / 15.0) * ((lipids[0] - 15.0) ** 2)) + 30
    protein = ingredient.getNutrientValue("Protein", amount)
    if protein is not None:
        score += ((-1.0 / 9.0) * ((protein[0] - 18.0) ** 2)) + 36
    fiber = ingredient.getNutrientValue("Fiber, total dietary", amount)
    if fiber is not None:
        score += ((-1.0 / 5.0) * ((fiber[0] - 10.0) ** 2)) + 20
    return score
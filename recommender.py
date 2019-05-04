#for every recipe given, specify which constraints it satisfy and total amount of "importance"
#output the recipes with top "importance"

#user input: "breakfast", "Italian"
from Constraint import *

import getopt
import sys

def recommend(recipes, constraints):
    rec = []
    for recipeName in recipes.keys():
        #print recipeName
        myRecipe = Recipe(recipeName, recipes[recipeName])
        rec.append(myRecipe)
        rank = 0
        for c in constraints:
            if c.satisfy(myRecipe) == True:
                rank += c.get_importance()
            else:
                rank -= c.get_importance()
        ranks.append(rank)
    return rec[rank.index(min(rank))]
    

if __name__ == "__main__":
    height = 180
    weight = 90
    age = 30
    meal = "lunch"
    gender = 'male'
    flavour = None
    vege = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"a:g:h:w:m:f:v")
    except getopt.GetoptError:
        print 'recommender.py -a age -g gender -h height -w weight -m meal -f flavour -v vegetarian'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-a':
            age = int(arg)
            #print "age:",age
        elif opt == '-g':
            gender = arg
            #print "gender:",gender
        elif opt == '-h':
            height = float(arg)
            #print 'height',height
        elif opt == '-w':
            weight = float(arg)
            #print "weight:",weight
        elif opt == '-m':
            meal = arg
            #print "meal:",meal
        elif opt == '-f':
            flavour = arg.lower()
            #print "flavour:",flavour
        elif opt == '-v':
            vege = True
            #print "vege:",vege

    constraints = []
    if vege == True:
        constraints.append(Vege_Constraint())
    if flavour is not None:
        constraints.append(Flavour_Constraint(flavour))
    constraints.append(Calories_Constraint(meal, gender, height, weight, age))
    constraints.append(Balance_Constraint())

    '''
    recipe1 = {"carbonhydrate":50.01,"fat":13.3,"protein":20.01,"fibre":5.6,"vegetarian":False}
    recipe1["flags"] = ["Italian"]
    recipe2 = {"carbonhydrate":50.01,"fat":50,"protein":20.01,"fibre":5.6,"vegetarian":True}
    recipe2["flags"] = ["Chinese"]
    recipes = [recipe1,recipe2]
    print constraint2.satisfy(recipe2)
    '''
    
    ranks = []
    allRecipes = parseRecipes()

    for recipeName in allRecipes.keys():
        print recipeName
        myRecipe = Recipe(recipeName, allRecipes[recipeName])
        rank = 0
        for c in constraints:
            if c.satisfy(myRecipe) == True:
                rank += c.get_importance()
            else:
                rank -= c.get_importance()
        ranks.append(rank)
    print ranks
    
    
    
    

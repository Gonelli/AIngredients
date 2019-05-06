#for every recipe given, specify which constraints it satisfy and total amount of "importance"
#output the recipes with top "importance"

#user input: "breakfast", "Italian"
from Constraint import *

import getopt
import sys
import numpy as np

def recommend(recipeList, userStats, userPrefs):

    constraints = []
    ranks = []
    if userPrefs[0] == True:
        constraints.append(Vege_Constraint())
    if userPrefs[1] is not None:
        constraints.append(Flavour_Constraint(userPrefs[1]))
    constraints.append(Calories_Constraint(userStats[0], userStats[1], userStats[2], userStats[3], userStats[4]))
    constraints.append(Balance_Constraint())
    
    rec = []
    for myRecipe in recipeList:
        #print recipeName
        #rec.append(myRecipe)
        rank = 0
        deleted = False
        for c in constraints:
            if c.satisfy(myRecipe) == True:
                rank += c.get_importance()
            else:
                if c.get_type() == 1:   #not satisfying the hard constraint
                    deleted = True
                    break
                #rank -= c.get_importance()
        if deleted == False:
            ranks.append(rank)
            rec.append(myRecipe)
    #print ranks
    '''
    #softmax selection of recipe
    softmax = np.exp(ranks - np.max(ranks))/\
        np.exp(ranks - np.max(ranks)).sum(axis=0)
    index = int(np.random.choice(len(softmax),p=softmax))
    print softmax
    print ranks[index]
    '''
    print ranks
    prob = []
    for r in ranks:
        prob.append(float(r+0.1)/(sum(ranks)+0.1*len(ranks))) #Laplace smoothing
    index = int(np.random.choice(len(prob),p=prob))
    #print prob
    return rec[index]#rec[ranks.index(max(ranks))]
    

# if __name__ == "__main__":
#     height = 180
#     weight = 90
#     age = 30
#     meal = "lunch"
#     gender = 'male'
#     flavour = None
#     vege = False
#     try:
#         opts, args = getopt.getopt(sys.argv[1:],"a:g:h:w:m:f:v")
#     except getopt.GetoptError:
#         print 'recommender.py -a age -g gender -h height -w weight -m meal -f flavour -v vegetarian'
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-a':
#             age = int(arg)
#             #print "age:",age
#         elif opt == '-g':
#             gender = arg
#             #print "gender:",gender
#         elif opt == '-h':
#             height = float(arg)
#             #print 'height',height
#         elif opt == '-w':
#             weight = float(arg)
#             #print "weight:",weight
#         elif opt == '-m':
#             meal = arg
#             #print "meal:",meal
#         elif opt == '-f':
#             flavour = arg.lower()
#             #print "flavour:",flavour
#         elif opt == '-v':
#             vege = True
#             #print "vege:",vege

#     constraints = []
#     if vege == True:
#         constraints.append(Vege_Constraint())
#     if flavour is not None:
#         constraints.append(Flavour_Constraint(flavour))
#     constraints.append(Calories_Constraint(meal, gender, height, weight, age))
#     constraints.append(Balance_Constraint())

#     '''
#     recipe1 = {"carbonhydrate":50.01,"fat":13.3,"protein":20.01,"fibre":5.6,"vegetarian":False}
#     recipe1["flags"] = ["Italian"]
#     recipe2 = {"carbonhydrate":50.01,"fat":50,"protein":20.01,"fibre":5.6,"vegetarian":True}
#     recipe2["flags"] = ["Chinese"]
#     recipes = [recipe1,recipe2]
#     print constraint2.satisfy(recipe2)
#     '''
    
#     ranks = []
#     allRecipes = parseRecipes()
#     recipeList = []
#     for recipeName in allRecipes.keys():
#         recipeList.append(Recipe(recipeName, allRecipes[recipeName][0],allRecipes[recipeName][1]))
#     stat = [meal,gender, height, weight, age]
#     pref = [vege,flavour]
#     '''
#     for recipeName in allRecipes.keys():
#         print recipeName
#         myRecipe = Recipe(recipeName, allRecipes[recipeName][0],allRecipes[recipeName][1])
#         rank = 0
#         for c in constraints:
#             if c.satisfy(myRecipe) == True:
#                 rank += c.get_importance()
#             else:
#                 rank -= c.get_importance()
#         ranks.append(rank)
#     print ranks
#     '''
#     #print recommend(allRecipes,stat,pref)
#     print recommend(recipeList,stat,pref)
    
#     for r in recipeList:
#         r.divideRecipe(adjust_factor(r,meal,gender, height, weight, age))

#     print recommend(recipeList,stat,pref)
    
    
    

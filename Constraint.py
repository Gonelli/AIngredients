class Constraint:
    def satisfy():
        pass
    def get_importance():
        pass

class Vege_Constraint(Constraint):
    def satisfy(self,recipe):
        #return recipe.vegetarian
        return recipe["vegetarian"]
    def get_importance(self):
        return 5

#from https://www.livestrong.com/article/84673-calculate-nutrition-goals-weight-loss/
#and https://healthyeating.sfgate.com/recommended-grams-nutrients-per-day-healthy-weight-loss-6294.html
#https://health.gov/dietaryguidelines/dga2005/document/pdf/DGA2005.pdf
class Calories_Constraint(Constraint):
    def __init__(self,meal):
        self.meal = meal
    def satisfy(self,recipe):
        #15%-30, 35-50%, 35-45% calories for breakfast, lunch and dinner
        #Calculator: https://www.freedieting.com/calorie-calculator
        # amount of calories to keep weight: 1600-2000 for women and 2000-3000 for men per day
        # subtract 250-1000 calories 250=0.5lb weight loss a week
        # carbonhydrate -> 45%-65% calories -> divided by 4 -> grams
        # fat -> 20%-35% -> divided by 9 -> grams
        # protein -> 10-35% -> divided by 4 -> grams
        # fibre -> 25g-38g per day or 14g for 1000 calories consumed
        # no more than 2lb per week
        maintenance = 2500 - 500 #maintenance - weight_reduce per day
        if self.meal == "breakfast":
            max_cal = maintenance*0.3
            min_cal = maintenance*0.15
        elif self.meal == "lunch":
            max_cal = maintenance*0.50
            min_cal = maintenance*0.35
        elif self.meal == "dinner":
            max_cal = maintenance*0.45
            min_cal = maintenance*0.35
        #nutrients = recipe.get_nutrients()
        nutrients = recipe #for test
        ch_calories = 4 * nutrients["carbonhydrate"]
        fat_calories = 9 * nutrients["fat"]
        protein_calories = 4 * nutrients["protein"]
        total_calories = ch_calories + fat_calories + protein_calories
        ch_percent = float(ch_calories)/total_calories
        fat_percent = float(fat_calories)/total_calories
        protein_percent = float(protein_calories)/total_calories

        weight_reduced = (maintenance - total_calories)/250*0.5 #lb
        #check total in []
        #check ch_percent in [45%-65%], fat_percent in [20%-35%], protein_percent in [10%-35%]
        if ch_calories >= 0.45*total_calories and ch_calories <= 0.65*total_calories and \
        fat_calories >= 0.2*total_calories and fat_calories <= 0.35*total_calories and \
        protein_calories >= 0.1*total_calories and protein_calories <= 0.35*total_calories and\
        total_calories >= min_cal and total_calories <= max_cal:
            return True
        else:
            return False


    def get_importance(self):
        return 4

class Flavour_Constraint(Constraint):
    def __init__(self,flavour):
        self.flavour = flavour
    def satisfy(self,recipe):
        #return self.flavour in recipe.flags
        return self.flavour in recipe["flags"]
    def get_importance(self):
        return 2

class Balance_Constraint(Constraint):
    def satisfy(self,recipe):
        #check vitamins?
        #check fibre
        #nutrients = recipe.get_nutrients()
        nutrients=recipe #for test only
        fibre = nutrients["fibre"]
        #fibre in 25-38g per day
        ch_calories = 4 * nutrients["carbonhydrate"]
        fat_calories = 9 * nutrients["fat"]
        protein_calories = 4 * nutrients["protein"]
        total_calories = ch_calories + fat_calories + protein_calories
        recommended_fibre = total_calories/1000*14
        #check fibre in recommend+-2
        if fibre >= recommended_fibre-2 and fibre <= recommended_fibre+2:
            return True
        else:
            return False
    def get_importance(self):
        return 3

#testing code
recipe1 = {"carbonhydrate":50.01,"fat":13.3,"protein":20.01,"fibre":5.6,"vegetarian":False}
recipe1["flags"] = ["Italian"]

constraint1 = Vege_Constraint()
print constraint1.satisfy(recipe1)
constraint2 = Calories_Constraint("breakfast")
print constraint2.satisfy(recipe1)
constraint3 = Flavour_Constraint("Chinese")
print constraint3.satisfy(recipe1)
constraint4 = Balance_Constraint()
print constraint4.satisfy(recipe1)

food_weights = [4.0, 3.0, 9.0] #weights for cheese, paprika, horseradish
alpha = 0.5

def cheese_function(amount):
    #cheese is fattening, so more will decrease q value
    return 1.0 / (amount ** 0.5)

def paprika_function(amount):
    #paprika is relatively healthy, but still not our healthiest ingredient
    return 0.5 * amount

def horseradish_function(amount):
    #horseradish is very healthy, increasing should directly increase q value
    return amount


def qLearning(reward, volumes):
    feature_functions =  [cheese_function, paprika_function, horseradish_function]
    #carries out an approximate q learning algorithm that uses features with
    #weights
    for index in range(len(food_weights)):
        food_weights[index] = food_weights[index] + (alpha * reward * feature_functions[index](volumes[index]))
    print("Updated weights")
    print(food_weights)
if __name__ == '__main__':
    print("Welcome to your AI Cook Assistant!")
    while True:
        advanceKey = input("Press anything to continue or type 'q' to quit: ")
        if advanceKey == 'q':
            break
        cheese = float(input("Enter cheese volume: "))
        paprika = float(input("Enter paprika volume: "))
        horseradish = float(input("Enter horseradish volume: "))
        reward = float(input("Your rating from 1 (worst) to 10 (best): "))
        qLearning(reward, [cheese, paprika, horseradish])

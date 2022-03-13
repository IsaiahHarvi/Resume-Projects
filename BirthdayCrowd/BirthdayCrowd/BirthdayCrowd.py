from matplotlib import pyplot as plt
from random import randint

# Function to check for repeats in the list.
def repeats(list1):
    for i in range(len(list1)):
        for j in range(i + 1, len(list1)):
            if list1[i] == list1[j]:
                return True
    return False

# Turns the amount of repeats into a percentage.
def percent(list1):
    trues = sum(list1)
    return trues / len(list1) * 100

# Lists.
crowd = []
percentages = []
trials = []

for i in range(100): # Makes 100 Crowds
    trials = []
    for f in range(1000): # Tests each crowd 1,000 times
        crowd = []
        for j in range(i): # Adds i num random birthdays
            crowd.append(randint(1,365))
    
        trials.append(repeats(crowd))
    percentages.append(percent(trials))


#GRAPHING
plt.title("The Birthday Problem") 
plt.xlabel("Number of People") 
plt.ylabel("Percentage of people with same birthdays")
plt.plot(range(0,100), percentages) 
plt.show()

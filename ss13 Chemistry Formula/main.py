import sqlite3
import os
from thefuzz import process
from color_source import TextColor, color

# Enable color in CMD.
os.system('color')

# Connect to DB.
db = sqlite3.connect('chem.db')
branchEnds = {}

# Get list of Chemicals
chemicalsList = db.execute('SELECT name FROM Chemical').fetchall() # Get list of tuples.
chemicalsList = [x[0] for x in chemicalsList] # Convert to list of strings.


# Print Colored messages.
def ColorPrint(string, inputColor = TextColor.white, newLine = True):
    print(color(string, inputColor), end = '')
    if newLine: print()


# Validate input.
def ValidInput(string, params, printError = False):
    inp = str(input(string).lower().strip())
    while 1:
        if inp in params:
            return inp
        elif printError:
            ColorPrint("\nInvalid input, please pick from the following: %s.\n"%(', '.join(params)), TextColor.yellow)
        inp = str(input(string))


# Which chemical formula to print.
def inputFormula():
    inputChemical = input('\nEnter chemical name: ').lower().strip()

    if inputChemical not in chemicalsList: # Find closest match.
        print("\nCould not find a recipe for '%s'\n\nDid you mean: \n"%inputChemical, end = '')
        possibleMatches = process.extract(inputChemical, chemicalsList, limit = 3)
        for i in range(3): # print top 3 matches
            print('%g. %s'%(i+1, possibleMatches[i][0]))

        listChoice = ValidInput("> ", ["1","2","3"], printError = True)
        inputChemical = possibleMatches[int(listChoice) - 1][0]
    
    # Get chemical ID for formula table.
    chemicalID = db.execute('SELECT id FROM Chemical WHERE name = ?', (inputChemical,)).fetchone()[0]

    # Print the formula.
    print() # New line for appearance.
    printFormula(chemicalID)


def printBranches(depth):
    print('       ', end = '') # Indent from the side overall.

    if depth > 0:
        for i in range(0, depth - 1):
            if branchEnds[i]: # If the branch ends, print a space.
                print('    ', end = '')
            else: # If the branch continues, print a vertical line.
                ColorPrint('│   ', TextColor.colorsList[i], newLine=False)
        
        if branchEnds[depth - 1]: 
            ColorPrint('└── ', TextColor.colorsList[depth - 1], newLine=False) # If the branch ends, print a horizontal line for an ingredient.
        else:
            ColorPrint('├── ', TextColor.colorsList[depth - 1], newLine=False) # If the branch continues, print a horizontal line for a recipe with a continuing character.
            

def printFormula(chemicalID, quantity = 0, depth = 0):
    # Get list of chemicals in formula.
    formulaList = db.execute('SELECT substance_id, quantity FROM Formula WHERE solution_id = ?', (chemicalID,)).fetchall()
    temperature = db.execute('SELECT temperature FROM Temperature WHERE solution_id = ?', (chemicalID,)).fetchone()
    if temperature != None: temperature = temperature[0] # Get the temperature.

    # Get the chemical name
    chemicalName = db.execute('SELECT name FROM Chemical WHERE id = ?', (chemicalID,)).fetchone()[0]

    # Print the branches
    branchEnds[depth] = False # indicates whether or not this branch is the last one at the specified depth.
    printBranches(depth)

    # Print the chemical
    if quantity > 1: # If there is a quantity > 1
        #ColorPrint("   %s%s (%g)"%('   '*depth, chemicalName, quantity), TextColor.colorsList[depth])
        ColorPrint("%s(%g)"%(chemicalName, quantity), TextColor.colorsList[depth])
    else:
        #ColorPrint("   %s%s"%('   '*depth, chemicalName), TextColor.colorsList[depth])
        ColorPrint("%s"%chemicalName, TextColor.colorsList[depth])

    # Print the recipes
    for i in formulaList:
        if i == formulaList[-1] and not temperature: branchEnds[depth] = True # If this is the last item in the list, set the branchEnds to true.
        printFormula(i[0], i[1], depth + 1)

    if temperature:
        branchEnds[depth] = True
        printBranches(depth + 1)
        #ColorPrint("   %sheat (%gk)"%('   '*depth, temperature), TextColor.colorsList[depth])
        ColorPrint("heat (%gk)"%temperature, TextColor.colorsList[depth])
    

# Start
print("SS13 Chemistry Tool")
while True:
    inputFormula()
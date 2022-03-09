import math
import os
import string
import subprocess
import sys

try:
    from mendeleev import element, get_all_elements
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'mendeleev'])
finally:
    from mendeleev import element, get_all_elements
    

class ChemCalculator:
    def __init__(self):
        while 1: 
            os.system('cls')

            # Menu
            print("\tChemistry Helper\n1. Calculate molar mass\n2. Calculate Moles\n3. Element Properties\n4. Element Isotopes")
            calculateOption = input("\n-> ")

            if calculateOption not in ["1","2","3","4"]:
                raise ValueError("Not a valid option.")
            
            # Call the Functions
            callFunc = {
                "1" : self.molarMass,
                "2" : self.moles,
                "3" : self.elementInfo,
                "4" : self.isotopes
            }
            print(callFunc[calculateOption]())

            # Pause before printing menu again
            input("\n")

    
    def molarMass(self, formula=None):
        # If it is not going to return a float for other calculations instead of display
        if not formula:
            os.system('cls')
            print("\tCalculate Molar Mass")
            print("Example Formula: H2 O (seperate each element with a space)")

            chemEquation = input("Enter your chemical formula: ")
        else: chemEquation = formula

        atomicMasses = []

        # Check the string and find the amount of each element and which elements
        for i in range(len(chemEquation)):
            if chemEquation[i] != ' ' and chemEquation[i] not in string.ascii_lowercase:
                if i != len(chemEquation)-1 and chemEquation[i] in string.ascii_uppercase and chemEquation[i+1] in string.ascii_lowercase:
                    atomicMasses.append(element(chemEquation[i:i+2]).mass)

                elif chemEquation[i] in string.digits:
                    atomicMasses[-1] = atomicMasses[-1] * int(chemEquation[i])

                else:
                    atomicMasses.append(element(chemEquation[i]).mass)
        
        # Make return string
        returnStr = ""
        for i in range(len(atomicMasses)):
            if i == len(atomicMasses)-1:
                returnStr += "%g"%atomicMasses[i]

            else:
                returnStr += "%g + "%atomicMasses[i]
    
        if not formula: return "\n%s"%returnStr + " = %s g/mol"%round(sum(atomicMasses), 3)
        else: return round(sum(atomicMasses), 3) # If another function needs the calculation only return that
    

    def moles(self):
        os.system('cls')
        print("\tMoles")
        print("Example Formula: H2 O (seperate each element with a space)")
        chemEquation = input("Enter your chemical formula: ")
        gramsCompound = float(input("Enter the amount of your compound in grams: "))
        molarMass = self.molarMass(chemEquation) # Call molar mass function for this calculation
        return "\n%gg %s / %g g/mol = %g Mol"%(gramsCompound, ''.join(chemEquation.split()), molarMass, round(gramsCompound / molarMass, 5))
        
        
    def elementInfo(self):
        while 1:
            os.system('cls')
            print("\tElements")
            atomicSymbol = input("Atomic Symbol: ")

            el = element(atomicSymbol)

            try: 
                print(
                    "Element Name: %s\nAtomic Number: %g\nAtomic Weight: %g\nProtons: %g\nNeutrons: %g\nMelting Point: %g\nPeriodic Table Period: %g\n"
                    %(el.name, el.atomic_number, el.mass,el.protons, el.neutrons, el.melting_point,el.period)
                    )

                if input("\nPress any key to continue or type to exit."): 
                    return

            except Exception:
                os.system('cls')
                print("Couldn't find an element with the Atomic Symbol: %s\n\n\n"%atomicSymbol)


    def isotopes(self):
        while 1:
            os.system('cls')
            print("\tIsotopes")
            atomicSymbol = input("Atomic Symbol: ")

            for i in element(atomicSymbol).isotopes:
                print(i)
                
            print("\nThe columns represent the attributes atomic_number, mass, abundance and mass_number respectively.\n")

            if input("\nPress any key to continue or type to exit."): 
                return


ChemCalculator()

import random, os, time
from color_source import *


# List of all the Wordle Words
with open("wordleWords.txt") as r:
    words = r.read().split()

# List of all the English Words
with open("words_alpha.txt") as r:
    eng_words = r.read().split()


def main():
    global startTime; global board

    correctAnswer = random.choice(words)  # Worlde word

    startTime = time.time() # Timer

    board = [] # Screen


    while True:
        printBoard()
        #print(correctAnswer)

        if len(board) < 6:  # If there aren't 6 guesses in the board list
            guess = input("\n\n->").lower() # Users guess

            if verified(guess):
                searchedString = "|"

                for i in range(5):
                    if guess[i] in correctAnswer: # If the letter is in the word
                        r,g,b = 0,200,200
                        if guess[i] == correctAnswer[i]: # If the letter is in the same index
                            r,g,b = 0,230,0
                        
                    else: # If it is not in the word
                        r,g,b = 100,100,100

                    searchedString += "%s|"%color(guess[i].upper(), (r,g,b))

                board.append(searchedString) # Add the guess to the board

                clearConsole()

                if guess == correctAnswer: # Win
                    printBoard()
                    print("\nGood Job!")
                    finish()
                    break
    
            else: # Invalid input
                clearConsole()



        else: # Lose (All 6 guesses have been made)
            print("\nThe word was: %s"%correctAnswer.upper())
            finish()
            break
    

    main() if input("\n\nPlay again?  ") else quit()
                    


def verified(word): # Function to determine if the word is in english words
    if len(word) >= 5 and word in eng_words:
        return True
    return False
        

def finish(): # End the game
    print("Time (Min): %g"%round((time.time()-startTime)/60, 2))


def clearConsole():
    os.system('cls')


def printBoard():
    print("  ___________")
    for i in range(6):
        try:
            print("  %s"%board[i])
        except:
            print("  └─┴─┴─┴─┴─┘") if i == 5 else print( "  ├─┼─┼─┼─┼─┤")



main()


import random


def guessnumber():
    # To gererate the random number from 1 to 20
    randomNumber = random.randrange(1, 20)

    guessedByUser = False
    userNr = int(input("Please, try to guess the number: "))

    while guessedByUser == False:

        if userNr == randomNumber:
            guessedByUser = True
            print("Yes! The number is {}. You found it!".format(randomNumber))
        elif userNr > randomNumber:
            userNr = int(input("The number is too high. Try another number: "))
        else:
            userNr = int(input("The number is too low. Try another number: "))

guessnumber()

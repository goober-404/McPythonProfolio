import random
import time
play = "Y"
print("Hello! I'm your computer. Whats your name?")
username = input().title() # I'm use to typing "username" as one word so im gonna type ir like that for the variable
print("Well, ", (username),", I would like to play a number guessing game.")
while play == "Y":
    NumOfTry = 10
    LimitLow = 1
    LimitHigh = 100
    print("Please think of a whole number between ", LimitLow, " and " ,LimitHigh, ". I am about to try and guess it in ", NumOfTry, " tries.")
    randomGuess = random.randint(LimitLow, LimitHigh)
    while NumOfTry != 0:
        print(NumOfTry,"\n attempts left")
        print(f"I guess: ", randomGuess)
        print("H = too high")
        print("L = too low")
        print("C = correct")
        HumanAnswer = str(input ("\nSo did I guess right?").upper())
        if HumanAnswer == "C":
            print("\nWOO HOO! I won!")
            NumOfTry = 0
        elif HumanAnswer == "H":
            LimitHigh = randomGuess
            print (f"\nHmm, so your number is between ", (LimitLow), " and ", (LimitHigh))
            NumOfTry -=1
            randomGuess = random.randint(LimitLow, LimitHigh)
        elif HumanAnswer == "L":
            LimitLow = randomGuess
            print(f"\nHmm, so your number is between ", (LimitLow), " and ", (LimitHigh))
            NumOfTry -= 1
            randomGuess = random.randint(LimitLow, LimitHigh)
        else:
            print("\nPlease enter a valid answer. H, L, abd C are the valid choices.")
    else:
        if HumanAnswer != "C":
            print("\nLooks like you win this time!")
            print("\nWhat number did you choose?")
            LimitHigh = 100
            LimitLow = 1
            NumAnswer = int(input())
            #You weren't really specific on how the player was cheating, so I just assumed the player was thinking of a number above 100 or below 1
            if NumAnswer <LimitLow:
                print("\nHey! Thats less than ", LimitLow, ", you cheated! I don't like cheaters!")
                time.sleep(5)
                exit()
            if NumAnswer >LimitHigh:
                print("\nHey! Thats more than ", LimitHigh, ", you cheated! I don't like cheaters!")
                time.sleep(5)
                exit()
            else:
                print(NumAnswer, "huh? (I was thinking about that number darn it...)")

        print ("\nType Y if you want to play again.")
        play = input().upper()
else:
    print (f"\nThank you for playing with me,", (username), ".")

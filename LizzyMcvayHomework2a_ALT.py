import random
import time

print ("Hello! I'm your computer. What is your name?")
user_name = input().title()

print ("Well, " + user_name + ", I would like to play a number guessing game.")


tries = 6
computer_number = random.randint (1, 20)

print ("I am thinking of a number between 1 and 20")

while tries > 0:
    while True:
        try:
            print ("What is your guess of my number? You have", (tries), "guesses left")
            guess_value = int(input())
            break
        except ValueError:
            print("Invalid input. Please eter a valid integer.")

    if guess_value < computer_number:
        print ("Your guess is too low.")
        tries -= 1

    if guess_value > computer_number:
        print ("Your guess is too high.")
        tries -= 1
        
    if guess_value == computer_number:
        print("Congratulations, "+ user_name +"! You have guessed my number with only " + str(tries-1) + " guesses remaining!")
    


    if tries <=0 and guess_value != computer_number:
       computer_number = str(computer_number)
       print ("YAY! I win! The number I was thinking of was " + computer_number)
    
    
    if guess_value == computer_number or tries <=0 and guess_value != computer_number:
        print("Thank you for playing with me.", user_name + ".")
        print("")
        print("Do you wish to play again", user_name + "? (Y/N)")

        playerResponse = str(input())

        if playerResponse == "y":
            print("Very well, we shall play again.")
            print("")
            
            tries = 0
            tries = 6
            
            time.sleep(1)
            computer_number = random.randint (1, 20)
            continue

        elif playerResponse == "Y":
            print("Very well, we shall play again.")
            print("")
            
            tries = 0
            tries = 6
            
            time.sleep(1)
            computer_number = random.randint (1, 20)
            continue
    

        else:
            print("")
            print("Until we meet again", user_name+".")
            time.sleep(3)
            exit()

    
    
    


import time
import random


def countdown():
    countdownRate = int(input("Enter your countdown duration in seconds:"))
        
    for number in reversed(range(1, countdownRate+1, 1)):
        print(str(number))
        time.sleep(1)
    randomJoke = random.randint(1, 5)
    
    if randomJoke == 1:
        print("HAPPY NEW... kia soul?.. GRAB THE ALL NE-")
    if randomJoke == 2:
        print("HAPPY NEW... day... you should go to bed")
    if randomJoke == 3:
        print("HAPPY NEW YEAR!! did you think I wasn't gonna do that? c'mon.")
    if randomJoke == 4:
        print("happy new- wait a second that was meant to be in all caps oops lol")
    if randomJoke == 5:
        print("HAPPY NEW... PERSONA (persona 5 music starts playing)")
        
    time.sleep(2)
    print("")
    restartResponse = print("Press Enter to restart countdown (insert song refrence here)")
    countdown()

countdown()

# Yes this is my humor, yes im maybe not ashamed, yes i just got back from camping and I was kind home sick for most of it ||
#                                                                                                                          \/


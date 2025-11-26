import time

class USNationalParks:
    def __init__(self, name, location, time):
        self.name = name
        self.location = location
        self.time = time

    def visit(self):
        print(f'You visited', self.name)
    def curTime(self):
        print(f'The current time in', self.name, 'is', self.time+'.')
    def curLoc(self):
        print(f"You're currently in the beatuiful* state of", self.location+'.')
    def leave(self):
        print('you took in the sights but you decided to move on to the next park.')
        
YE = USNationalParks(f"Yellowstone", "Idaho", "3:31 P.M")
SM = USNationalParks(f'the Smokey Mountains', 'Tenessee', '6:47 A.M')
YO = USNationalParks(f'Yosemite', 'California', '5:56 P.M')
DV = USNationalParks(f'Death Valley', 'Calidornia (the 51st state)', '11:28 A.M')

print("You're feeling adventurous and you have magical teleportation abilites to take you anywhere you wish.")
time.sleep(3)
print("You decided to visit some US National parks because thats how you decided to spend your precious seconds here on this microscopic earth.")
time.sleep(4)

def visitor():
    print("Where would you like to go?")
    print("")
    time.sleep(2)
    print('type in all caps, YE for Yellowstone, SM for Smokey Mountains, YO for Yosemite, DV for DEATH VALLEY (duh nuh nuh nuuuuuh)')
    print('You can check what state your in by typing "LOC"')
    print('You can check what time is it by typing "TIM"')
    print('You can leave by typing "BYE"')
    print('type literally anything else to stop your adventure')

    teleTo = input('Go to:')

    def visitingYE():
        whatDo = input('Do what?')
        print("")
        if whatDo == 'LOC':
            YE.curLoc()
            time.sleep(1)
            visitingYE()
        if whatDo == 'TIM':
            YE.curTime()
            time.sleep(1)
            visitingYE()
        if whatDo == 'BYE':
            YE.leave()
            time.sleep(2)
            visitor()

    def visitingSM():
        whatDo = input('Do what?')
        print("")
        if whatDo == 'LOC':
            SM.curLoc()
            time.sleep(1)
            visitingSM()
        if whatDo == 'TIM':
            SM.curTime()
            time.sleep(1)
            visitingSM()
        if whatDo == 'BYE':
            SM.leave()
            time.sleep(2)
            visitor()

    def visitingYO():
        whatDo = input('Do what?')
        print("")
        if whatDo == 'LOC':
            YO.curLoc()
            time.sleep(1)
            visitingYO()
        if whatDo == 'TIM':
            YO.curTime()
            time.sleep(1)
            visitingYO()
        if whatDo == 'BYE':
            YO.leave()
            time.sleep(2)
            visitor()

    def visitingDV():
        whatDo = input('Do what?')
        print("")
        if whatDo == 'LOC':
            DV.curLoc()
            time.sleep(1)
            visitingDV()
        if whatDo == 'TIM':
            DV.curTime()
            time.sleep(1)
            visitingDV()
        if whatDo == 'BYE':
            DV.leave()
            time.sleep(2)
            visitor()
    
    if teleTo == 'YE':
        YE.visit()
        visitingYE()

    if teleTo == 'SM':
        SM.visit()
        visitingSM()
        
    if teleTo == 'YO':
        YO.visit()
        visitingYO()

    if teleTo == 'DV':
        DV.visit()
        visitingDV()
    else:
        print('You wanna quit? Alright')
        time.sleep(2)
        exit()
visitor()

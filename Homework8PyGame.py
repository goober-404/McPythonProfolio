from bs4 import BeautifulSoup
import requests
import pygame
screenWidth = 800
screenHeight = 600
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
FPS = 60
pygame.init()
screen = pygame.display.set_mode([screenWidth, screenHeight],pygame.RESIZABLE)

pygame.display.set_caption("Quiz Game")
font = pygame.font.SysFont(None, 40)

slide = 0

url = 'https://sites.google.com/view/pyhomework-emv/home'
result = requests.get(url)

soup = BeautifulSoup(result.text, "html.parser")
soupText = soup.get_text(separator="\n")


incorrectAnswers = soup.find_all('small')#small text

correctAnswers = soup.find_all('p')#paragraph

questions = soup.find_all('h1')#Header





##for q in questions:
##    print(q.get_text(strip=True))
##for q in incorrectAnswers:
##    print(q.get_text(strip=True))
##for q in correctAnswers:
##    print(q.get_text(strip=True))

def handleInputs():
    global running,slide
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                slide -= 1

            if event.key == pygame.K_RIGHT:
                slide += 1
            if event.key == pygame.K_ESCAPE:
                print("Escape key up, exiting.")
                running = False
            if slide<0:
                slide=3
            if slide>3:
                slide=0
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
            
        if event.type == pygame.QUIT:
            running = False
def drawSlides():
    global slide
    screen.fill(BLACK)

    question = font.render(questions[slide].get_text(), True,BLUE)
    correctAnswer = font.render(correctAnswers[slide].get_text(), True,GREEN)
    screen.blit(question, (100,100))
    screen.blit(correctAnswer, (100,200))
    if slide == 0:
            incorrectAnswer1 = font.render(incorrectAnswers[slide].get_text(), True,RED)
            incorrectAnswer2 = font.render(incorrectAnswers[slide+1].get_text(), True,RED)
            incorrectAnswer3 = font.render(incorrectAnswers[slide+2].get_text(), True,RED)
    if slide == 1:
            incorrectAnswer1 = font.render(incorrectAnswers[slide+2].get_text(), True,RED)
            incorrectAnswer2 = font.render(incorrectAnswers[slide+3].get_text(), True,RED)
            incorrectAnswer3 = font.render(incorrectAnswers[slide+4].get_text(), True,RED)
    if slide == 2:
            incorrectAnswer1 = font.render(incorrectAnswers[slide+4].get_text(), True,RED)
            incorrectAnswer2 = font.render(incorrectAnswers[slide+5].get_text(), True,RED)
            incorrectAnswer3 = font.render(incorrectAnswers[slide+6].get_text(), True,RED)
    if slide == 3:
            incorrectAnswer1 = font.render(incorrectAnswers[slide+6].get_text(), True,RED)
            incorrectAnswer2 = font.render(incorrectAnswers[slide+7].get_text(), True,RED)
            incorrectAnswer3 = font.render(incorrectAnswers[slide+8].get_text(), True,RED)
    screen.blit(incorrectAnswer1, (100, 300))
    screen.blit(incorrectAnswer2, (100, 400))
    screen.blit(incorrectAnswer3, (100, 500))
    pygame.display.flip()
        
running = True
while running:
    handleInputs()
    drawSlides()
    

    




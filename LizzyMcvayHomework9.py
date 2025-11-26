
import turtle
import time
pen = turtle.Turtle()
length = 1
pen.color("orange")
pen.speed(0)


while length<200:
    pen.forward(length)
    pen.left(69)
    length += 1

while length>=200 and length<400:
    pen.color("blue")
    pen.forward(length)
    pen.left(69)
    length += 1
    
while length>=400 and length<600:
    pen.color("green")
    pen.forward(length)
    pen.left(69)
    length += 1

while length>=600 and length<800:
    pen.color("black")
    pen.forward(length)
    pen.left(69)
    length += 1

while length>=800:
    print("i got tired, i mean, thats a lot of hexagons you wated me to draw. One computer can't possibly do that mauch!!")
    time.sleep(5)
    print("oh they can? Well... im not like other computers.. ¯|_(ツ)_|¯")
    break
turtle.done

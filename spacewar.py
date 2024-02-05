import os
import random
import pygame as pg
import time

import turtle
turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("background.gif")
turtle.title("SpaceWar")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def go(self):
        self.fd(self.speed)

        # Right Border
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        # Left Border
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        # Upper Border
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        # Down Border
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
    
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False
        

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.lives = 3

    # Player Movement
    def turn_left(self):
        self.lt(45)
    
    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1
    
    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))
    
    def go(self):
        self.fd(self.speed)

        # Right Border
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        # Left Border
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        # Upper Border
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        # Down Border
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.02, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)
        pg.mixer.init()
    
    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "shoot"
            pg.mixer.music.load('Laser.wav')
            pg.mixer.music.play()
        
    def go(self):

        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "shoot":
            self.fd(self.speed)

        #Border Check
        if self.xcor() < -290 or self.xcor() > 290 or\
        self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.01, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0
    
    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def go(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1
        
        if self.frame > 15:
            self.frame = 0
            self.goto(-1000, -1000)

# Game Stat
class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()

        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

game = Game()

game.border()

game.show_status()

# Visualization
player = Player("triangle", "white", 0, 0)
missile = Missile("square", "yellow", 0, 0)
enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))
allies = []
for i in range(3):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))

# Keyboard Bind 
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

# Movement Trigger
while True:
    turtle.update()
    time.sleep(0.03)

    player.go()
    missile.go()

    for enemy in enemies:
        enemy.go()

         # Collision Check
        if player.is_collision(enemy):
            pg.mixer.Sound('explosion.wav').play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            # Score Decrease
            game.score -= 100
            game.show_status()
            

        # Kill Enemy
        if missile.is_collision(enemy):
            pg.mixer.Sound('explosion.wav').play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            # Score Increase
            game.score += 100
            game.show_status()
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())
                particle.setheading(random.randint(0, 360))
            
    for ally in allies:
        ally.go()

        if missile.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            # Score Decrease
            game.score -= 50
            game.show_status()
            pg.mixer.Sound('explosion.wav').play()

    for particle in particles:
        particle.go()
   

    
    
    

delay = input("Press enter to finish. > ")
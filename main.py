#import all functions built in pygame
from math import *
from random import *
from pygame import * 
from colours import *
init() #initialize the screen
size = width, height = 1000, 700    #dimensions of the screen
screen = display.set_mode(size)     #set the screen
myClock = time.Clock()
button = 0
screen.fill(WHITE)
fontLoadingScreen = font.SysFont("Times New Roman",40)  #initialize font size for loading screen, and bigger text
fontRegister = font.SysFont("Times New Roman",20) #font size for smaller text

bossesPic = image.load("enemyBoss1.png")    #picture of my first avatar boss
virusEnemyPic = image.load("virusEnemy.png")    #picture of my small virus tower enemy
bulletFiringPic = transform.scale(image.load("bullets.png"),(30,30))    #bullet images for my player 
enemyBulletFiringPic = transform.scale(image.load("enemyBullets.png"),(30,30))  #enemy bullet pictures (for the virus towers)
bossBulletFiringPic = image.load("fireSpinner.png") #enemy bullet pictures (for the main boss enemy)

#defining a class for my bullets
class playerBullet():
    def __init__(self, mouseX, mouseY): #initialize the class
        self.PosX = xMoving[i]  #position of character variable (x value)
        self.PosY = yMoving[i] + 70 #position of character variable (y value)
        self.MovementX = (cos(-atan2(-(mouseY - self.PosY), mouseX - self.PosX))) #motion of my bullets (x value)
        self.MovementY = (sin(-atan2(-(mouseY - self.PosY), mouseX - self.PosX))) #motion of my bullets (y value)
    def movement(self): #initialize the movement of bullets
        self.PosX += self.MovementX*6  #move the x position based on this motion calculation
        self.PosY += self.MovementY*6  #move the y position based on this motion calculation
        
    def draw(self):#initialize the drawing of the bullets
        screen.blit(bulletFiringPic, Rect(round(self.PosX), round(self.PosY)-15, 0,0)) #draw on the screen the bullets

class mainEnemies(): #enemy class
    def __init__(self, health, initialPosX, initialPosY, picture, radius): #initialize the health, position of monster, the image itself, and the hitbox radius
        self.Health = health    #health variable of monster
        self.PosX = initialPosX  #initial position of the monster (x value)
        self.PosY = initialPosY  #initial position of the monster (y value)
        self.image = picture  #image variable
        self.radius = radius #radius variable
        

class enemies(mainEnemies): #minion SUBclass 
    def __init__(self): #initialize self
        global xRandom #globalize random x coordinate of the monster
        global yRandom #globalize random y coordinate of the monster  
        xRandom = randint(500,900) #random x coordiante
        yRandom =  randint(200,600) #random y coordinate
        mainEnemies.__init__(self, 110, xRandom, yRandom, virusEnemyPic, 35) #create the subclass from the main class parameters
        self.initialHealthDisplay = 88 #initial display of each minion
        self.magic = 0 #magic potion of the player
    
    def draw(self):
        global healthX
        screen.blit(self.image,Rect(self.PosX-50,self.PosY - 50,0,0))  
        #screen.blit(self.Image2, Rect(700,300,0,0))
        draw.rect(screen, BLACK, (self.PosX-50,self.PosY + 35,90,15),2)
        draw.rect(screen, GREEN, (self.PosX-49,self.PosY+37,self.initialHealthDisplay,12))

    def update(self): #updating the hitbox of the monster, and score
        global scoreCounting #globalize the score counting of the game
        for bullet in playerBulletList: #for each bullet in the list; 
            if sqrt((self.PosX - bullet.PosX)**2+(self.PosY - bullet.PosY)**2) < self.radius: #if the bullet hits the minion, 
                self.Health -= 5 #lose 5 health on the minion
                self.initialHealthDisplay -= 4 #lose 4 health on the screen display
                playerBulletList.remove(bullet) #remove the bullet, to make it look like it hit the object
        if self.Health <= 0: #if the health of the minion is less than or equal to 0:
            enemyList.remove(self)   #remove the enemy
            enemyList.append(enemies()) #add a new enemy
            scoreCounting += 20 #add to the score counting
        

class bosses(mainEnemies): #boss SUBclass
    def __init__(self): #initialize self
        mainEnemies.__init__(self, 270, 700, 400, bossesPic, 70) #create the subclass using the parameters from the main class
        self.initialHealthDisplay = 88 #initial display of health as 88
        
    def draw(self):
        screen.blit(self.image,(self.PosX - 48, self.PosY - 48)) #draw the actual boss on the screen
    
    def update(self):
        global scoreCounting    #globalize variables
        global enemyHealthX
        for bullet in playerBulletList: #check each bullet in the bullet list
            if sqrt((self.PosX - bullet.PosX)**2+(self.PosY - bullet.PosY)**2) < self.radius: #if the bullet hits the boss:
                self.Health -= 15
                self.initialHealthDisplay -= 4         #minus its health
                enemyHealthX -= 15
                playerBulletList.remove(bullet)    #remove the bullet, to make it look as if it hit the boss  
                scoreCounting += 7 #add to the score counting every time you hit the boss
                if self.Health <= 0: #if the health of the boss is less than or equal to 0:
                    enemyList.remove(self)   #remove the boss
                    scoreCounting += 200     #add to the score counting

class enemyBullet(): #create a class for enemy bullets
    def __init__(self, playerX, playerY): #define parameters of the bullet
        self.PosX = xRandom #xRandom is the random x coordinate at which the monster starts
        self.PosY = yRandom #yRandom is the random x coordinate at which the monster starts
        self.MovementX = (cos(-atan2(-(playerY - self.PosY), playerX - self.PosX))) #motion of the enemy bullets (x value)
        self.MovementY = (sin(-atan2(-(playerY - self.PosY+100), playerX - self.PosX))) #motion of the enemy bullets (y value)
        
    def movement(self): #initialize the movement of the bullets
        self.PosX += self.MovementX *6 #movement calculation based on the motion (x value)
        self.PosY += self.MovementY *6 #movement calculation based on the motion (y value)
        
    def draw(self): #initialize the drawing of the bullets
        screen.blit(enemyBulletFiringPic, Rect(round(self.PosX)-10,round(self.PosY)-30,0,0))   #draw the enemy bullets on the screen

class bossBullet(): #create a class for boss bullets
    def __init__(self, playerX, playerY): #define parameters of the bullets
        self.PosX = 700 #initial position of bullets (x value)
        self.PosY = 400 #initial position of the bullets (y value)
        self.MovementX = (cos(-atan2(-(playerY - self.PosY), playerX - self.PosX))) #motion of the boss bullets(x value)
        self.MovementY = (sin(-atan2(-(playerY - self.PosY+30), playerX - self.PosX))) #motion of the boss bullets (y value)
    
    def movement(self): #initialize the movement of the bullets
        self.PosX += self.MovementX *6 #movement calculation based on motion (x value)
        self.PosY += self.MovementY *6 #movement calculation based on motion (y value)
    
    def draw(self): #initialize the drawing of the bullets
        screen.blit(bossBulletFiringPic, Rect(round(self.PosX),round(self.PosY),0,0)) #draw the enemy bullets on the screen

magicPotionImage = transform.scale(image.load("manaPotion.png"),(80,70)) #image for each potion
def instructions(): #instruction page
    draw.rect(screen, WHITE, (280,150,500,500))
    draw.rect(screen, BLACK, (280,150,500,500),7)
    draw.rect(screen,BLACK,(740,150,40,40),2)           #draw dimensions of the box
    draw.line(screen, RED, (740,150),(780,190),3)
    draw.line(screen, RED, (780,150), (740,190),3)
    wasdKeyboard = transform.scale(image.load("keyboard.png"),(100,70)) #image for keyboard --> this is where the image error in python shell shows up
    screen.blit(wasdKeyboard, Rect(310,180,10,10)) #display the keyboard image
    instructionText1 = fontLoadingScreen.render("Use WASD to move",5,BLACK) #instructions
    screen.blit(instructionText1,Rect(400,170,10,10))
    draw.circle(screen,BLACK,(330, 310),5,0)
    draw.circle(screen,BLACK,(350, 310),5,0)
    draw.circle(screen,BLACK,(370, 310),5,0)
    instructionText2 = fontLoadingScreen.render("Press SPACE to shoot",5,BLACK) #shooting bullets instructions
    screen.blit(instructionText2, Rect(400,290,10,10))  #display the images and texts
    screen.blit(magicPotionImage, Rect(310,370,0,0))
    instructionText3 = fontLoadingScreen.render("Collect Potions;",5,BLACK)
    instructionText4 = fontLoadingScreen.render("Press f to use special ability;",5,BLACK)
    instructionText5 = fontLoadingScreen.render("Get shielded for 7 seconds",5,BLACK)   #more instructiosn for the user
    instructionText6 = fontLoadingScreen.render("Aim for the avatars head!",5,BLACK)
    screen.blit(instructionText3,Rect(400,390,0,0))
    screen.blit(instructionText4, Rect(310,450,0,0))    #display the text of the instructions
    screen.blit(instructionText5, Rect(310,510,0,0))
    screen.blit(instructionText6, Rect(310,570,0,0))
    
scoreCounting = 0
turretCount = 0     #variables for score, turret counts, and magic potion
magic = 0
def gameMenuScreen1(xCor,yCor,health): #initialize screen for the display of the game 
    colourX,colourY = mouse.get_pos()   #mouse position for the colours of the text
    draw.rect(screen, GREEN, (20,10,health,30))     #draw the health bars
    draw.rect(screen, BLACK, (20,10,270,30),2)
    
    draw.rect(screen, BLACK, (30,50,245,15),2)      #draw the magic bar of the character
    draw.rect(screen,DEEPSKYBLUE,(32,52,magic,12))
    
    draw.rect(screen, RED, (700,10,enemyHealthX,30))    #draw the health bar of the enemy characters
    draw.rect(screen, BLACK, (700,10,270,30),2) 

    currentScore = fontLoadingScreen.render("Score: " + str(scoreCounting),5,BLACK) #display score counting of the game
    screen.blit(currentScore, Rect(330,0,0,0))
    
    if colourX > 530 and colourX < 600 and colourY > 0 and colourY < 40:
        startButton = fontLoadingScreen.render("Start",5,RED)       #display the start button (red)
        screen.blit(startButton, Rect(530,0,0,0))
    else:
        startButton = fontLoadingScreen.render("Start",5,BLACK)
        screen.blit(startButton, Rect(530,0,0,0))   #display the start button (black)
        
def scorePage():    #final score page
    mx,my = mouse.get_pos()
    screen.fill(WHITE) #fill the screen with white
    finalScoreText = fontLoadingScreen.render("Game Lost",5,BLACK)
    finalScoreText2 = fontLoadingScreen.render("Final Score: "+ str(scoreCounting),5,BLACK)    #det the text of the ending screen
    screen.blit(finalScoreText, Rect(400,200,0,0))  #display the final screen text
    screen.blit(finalScoreText2, Rect(400,300,0,0))
    if mx > 400 and mx < 500 and my > 400 and my < 450:     #if the mouse positions hover over these coordinates:
        restartText = fontLoadingScreen.render("Quit",5,RED) #change the text to a red colour
        screen.blit(restartText, Rect(400,400,0,0)) #blit the text
    else:
        restartText = fontLoadingScreen.render("Quit",5,BLACK) #default text to black colour
        screen.blit(restartText, Rect(400,400,0,0)) #blit the text

def winningPage(): #defining a winning page
    mx,my = mouse.get_pos() #coordiantes of the mouse
    screen.fill(WHITE) #fill the screen with white
    finalScoreText = fontLoadingScreen.render("You Win!",5,BLACK) #text of the winning screen
    finalScoreText2 = fontLoadingScreen.render("Final Score: "+ str(scoreCounting),5,BLACK) #text of the winning screen
    screen.blit(finalScoreText, Rect(400,200,0,0))      #display the text of the winning screen
    screen.blit(finalScoreText2, Rect(400,300,0,0))
    if mx > 400 and mx < 500 and my > 400 and my < 450: #check the mouse position of the mouse
        restartText = fontLoadingScreen.render("Quit",5,RED) #switch the text colour to red
        screen.blit(restartText, Rect(400,400,0,0))
    else:
        restartText = fontLoadingScreen.render("Quit",5,BLACK) #default text colour of black
        screen.blit(restartText, Rect(400,400,0,0))    

def objective(): #define objective function
    permaFrostObjective = fontLoadingScreen.render("Don't let the virus' reach the permafrost lord!",5,BLACK) #set an objective text
    screen.blit(permaFrostObjective, Rect(150,550,0,0)) #display the text
    
#all the list variables
xMoving = [300]
yMoving = [300] 
playerBulletList = []
enemyList = []
enemyBulletList = []
bossBulletList = []
magicPotionX = []
magicPotionY = []
xFlyingList = []
yFlyingList = []
countingFire = xMoving[0]-140

#all of the boolean values (set to true)
homePageCheck = True
dataCheck = True
turretSpawning = True
running = True

#all of the other boolean values (set to false)
register = False
usernameChecking = False
passwordChecking = False
gameMenu = False
gameMenu2 = False
inputCheck = False
passwordCheck = False
changingColour = False
changingColour2 = False
bulletFire = False
enemySpawningLevel1 = False
enemySpawningLevel2 = False
instructionCheck = False
shieldActivation = False
endingScoreScreen = False
nextLevelScreen = False
finalScreen = False

#counter variables (all set to 0)
counterBullet = 0
counterBullet2 = 0
counterBullet3 = 0
bulletLevel = 0
countingPotion = 0
countingMagicSeconds = 0
craigMovement = 0
game2Counting = 0

#counter variables with set values 
turtleSpeed = 4
brainSpeed = 2
initialFiringSpeed = 13
initialFiringSpeed3 = 15
initialFiringSpeed2 = 25
enemyCounting = 25
healthX = 270
enemyHealthX = 270
flyingBrainHealth = 140

enemyList.append(enemies()) #append enemies to the list
enemyList.append(bosses()) #append bosses to the list
shieldImage = transform.scale(image.load("shieldActivate.png"),(30,30))
backgroundImage = transform.scale(image.load("backgroundGame.png"),(1000,1000))
backgroundImage2 = transform.scale(image.load("introScreen.png"),(1000,1000))
enemyBulletFiringPic = transform.scale(image.load("enemyBullets.png"),(30,30))
turtle = transform.scale(image.load("turtle.png"), (120,120))
portalEntry = transform.scale(image.load("portal.png"),(100,100))                   #most of my pixelated images
entryText = fontLoadingScreen.render("Enter",5,BLACK)                               #some of the iamges are transformed/scaled
craigTheHelper = image.load("helper.png")
portalEntry2 = transform.scale(image.load("portal2.png"),(100,100))
permafrostProtector = image.load("permafrost.png")
flyingBrain = image.load("flyingBrain.png")
rainClouds = image.load("rainClouds.png")

textBox = transform.scale(image.load("pixelTextBox.png"),(200,200))
craigWarning1 = fontRegister.render("Stay away",5,BLACK)            
craigWarning2 = fontRegister.render("from the",5,BLACK)             #text of craigs warning
craigWarning3 = fontRegister.render("portal",5,BLACK)

craigWarning4 = fontRegister.render("no",5,BLACK)
craigWarning5 = fontRegister.render("NO",5,BLACK)               #text of craigs warning pt.2
craigWarning6 = fontRegister.render("NOOO!!",5,BLACK)

craigWarning7 = fontRegister.render("Prepare",5,BLACK)
craigWarning8 = fontRegister.render("for the ",5,BLACK)         #text of craigs warning pt.3
craigWarning9 = fontRegister.render("viruses",5,BLACK)


while running:      #check to see if running is true; if so, 
    if homePageCheck == True:   #check if home page is true; if so, 
        mouse1, mouse2 = mouse.get_pos()
        screen.fill(WHITE)
        screen.blit(portalEntry, Rect(600,300,0,0))     #blit the intro screens (white, portal, etc)
        keys = key.get_pressed() #get the keys pressed
        for i in range(len(xMoving)): #check the movement of turtles (list of the coordinates)
            turtleRect = Rect(xMoving[i]-85,yMoving[i]+12,0,0) #turtle image set
            screen.blit(turtle, turtleRect) #display the turtle image
            if keys[K_d]:
                xMoving[i] += turtleSpeed
            if keys[K_a]:
                xMoving[i] -= turtleSpeed       #check the movement of the turtle; if so, move the turtle positions by turtleSpeed
            if keys[K_s]:
                yMoving[i] += turtleSpeed
            if keys[K_w] and yMoving[i] > 130:
                yMoving[i] -= turtleSpeed  
        if xMoving[i] > 580 and xMoving[i] < 700 and yMoving[i] > 270 and yMoving[i] < 350:     #check the coordinages of the turtles
            if mouse1 > 600 and mouse1 < 700 and mouse2 > 400 and mouse2 < 450: #if the mouse hovers over the coordinates
                entryText = fontLoadingScreen.render("Enter",5,RED)     #text display is red
                screen.blit(entryText, Rect(600,400,0,0))   #display the text
            else:
                entryText = fontLoadingScreen.render("Enter",5,BLACK) #default text display is black
                screen.blit(entryText, Rect(600,400,0,0)) #display the text
                
        screen.blit(craigTheHelper, Rect(830,350,0,0)) #display craig
        screen.blit(textBox, Rect(700,200,0,0)) #display the textbox image
        
        if xMoving[i] <= 300: #if the x value of the image is below 300:
            screen.blit(craigWarning1, Rect(740,245,0,0))
            screen.blit(craigWarning2, Rect(740,265,0,0))       #display this certain text
            screen.blit(craigWarning3, Rect(740,285,0,0))
            
        elif xMoving[i] > 300 and xMoving[i] < 550:     #if the x value of the image is between 300 and 550
            screen.blit(craigWarning4, Rect(740,245,0,0))
            screen.blit(craigWarning5, Rect(740,265,0,0))       #display this certain text
            screen.blit(craigWarning6, Rect(740,285,0,0))    
        
        else:      #for an other x value:
            screen.blit(craigWarning7, Rect(740,245,0,0))
            screen.blit(craigWarning8, Rect(740,265,0,0))       #display this certain text
            screen.blit(craigWarning9, Rect(740,285,0,0))               
            
#------------------------------------------------------------------------------------------------------------

    elif gameMenu == True: #check if the game menu screen is true; if it is
        homePageCheck = False
        screen.fill(WHITE)   
        screen.blit(backgroundImage, Rect(0,100,0,0))           #set the default home screen (White, background image, etc
        keys = key.get_pressed()    #get the keys pressed
        for i in range(len(xMoving)): #check for each coordinate in the list
            turtleRect = Rect(xMoving[i]-85,yMoving[i]+12,0,0)      #turtle image set coordinates
            screen.blit(turtle, turtleRect) #display the turtle picture
            if keys[K_d]:
                xMoving[i] += turtleSpeed
            if keys[K_a]:
                xMoving[i] -= turtleSpeed       #check the movement of the turtle; move it based on the keyboard input and turtleSpeed
            if keys[K_s]:
                yMoving[i] += turtleSpeed
            if keys[K_w] and yMoving[i] > 130:
                yMoving[i] -= turtleSpeed   
        for bullet in playerBulletList:     #check each bullet in the bullet list; 
            bullet.movement()   #calculate the movement
            bullet.draw()    #display the drawing of the bullet 
        mouseX,mouseY = mouse.get_pos()    #mouse x and y coordinates recieved
        gameMenuScreen1(xMoving,yMoving,healthX) #display the game menu screen
        counter = 0     #set a counter variable    
        if keys[K_f] and magic == 242: #if the user presses the key "f" and the magic value is 242: 
            print ("Special ability")      
            shieldActivation = True #activate the shield
            magic = 0  #set the magic values back to 0
        if keys[K_SPACE] and mouseX > xMoving[i]: #check if the user inputs space, and the mouse is pointing in front of the space button
            if counterBullet % initialFiringSpeed == 0 and xMoving[i] > 200 and xMoving[i] < 700:  #check the speed of the bullet
                playerBulletList.append(playerBullet(mouseX,mouseY))  #append bullets in the list
            counterBullet += 1  #add to the counter bullet
        if enemySpawningLevel1 == True:  #check if the enemies are spawning; if so,
            for enemyBulletCount in enemyBulletList: #check the enemies bullets in the list; for each bullet,
                enemyBulletCount.movement() #calculate the movement of the bullets
                enemyBulletCount.draw() #draw the bullets on to the screen
                if sqrt((xMoving[i] - enemyBulletCount.PosX)**2+(xMoving[i] - enemyBulletCount.PosY)**2) < 35: #if the enemy bullets collide with the player:
                    enemyBulletList.remove(enemyBulletCount) #remove the bullet, to make it look like it hit the player
                    if shieldActivation == True: #if the shield actiavtion is true:
                        healthX -= 1 #lose only 1 health; take less damage
                    else: #if the shield activation is not true
                        healthX -= 5 #lose 5 health; no shield
            for bulletCount in bossBulletList: #for each bullet in the BOSS bullet count:
                bulletCount.movement() #calculate the movement of the bullets
                bulletCount.draw() #draw the bullets onto the screen
                if sqrt(((xMoving[i] - bulletCount.PosX)-10)**2+((xMoving[i] - bulletCount.PosY)+60)**2) < 35: #if the boss bullets collide with the player:
                    bossBulletList.remove(bulletCount) #remove the bullet, to make it look like it hit the player
                    if shieldActivation == True: #if the shield activation is true:
                        healthX -= 5 #lose only 5 health; take less damage
                    else: #if the shield activation is not true:
                        healthX -= 15  #lose 15 health; no shield       
            if counterBullet2 % initialFiringSpeed2 == 0: #check the firing speed of the bullets; if the counter is divisible with the firing speed:
                enemyBulletList.append(enemyBullet(xMoving[i],yMoving[i])) #add to the bullet list
            if counterBullet3 % initialFiringSpeed3 == 0:
                if enemyHealthX > 0:                #if the enemy is still alive:
                    bossBulletList.append(bossBullet(xMoving[i],yMoving[i]))    #add the bullet to the bosses bullet list; this will display it
            counterBullet2 += 1 #add to the counter variable
            counterBullet3 += 1 #add to the counter variable
            if turretSpawning == True: #check if the turrets are spawning; if they are, 
                magicX = randint(1,500)
                magicY = randint(200,500)
                magicPotionX.append(magicX)         #spawn in random potions on the screen
                magicPotionY.append(magicY)
                screen.blit(magicPotionImage, Rect(magicPotionX[countingPotion],magicPotionY[countingPotion],10,10)) #display the potions
                if sqrt(((magicPotionX[countingPotion]+30)-xMoving[i])**2 + ((magicPotionY[countingPotion]+30)-(yMoving[i]+40))**2) < 35: #if the player collides with the potion: (hitbox)
                    countingPotion += 1 #add to the counting potion
                    magic += 30 #add to the potion box
                    scoreCounting += randint(5,10) #add to the score
                    if healthX <= 265:
                        healthX += 5
                    if magic > 242: #check if the magic goes above 242; if it does,
                        magic = 242 #it reaches its maximum of 242 pixels
            for enemy in enemyList: #for each enemy in the enemy list
                enemy.draw() #draw the enemies 
                enemy.update()  #update each enemy in the enemy list

        if shieldActivation == True: #check if the shield is activated; if it is, 
            screen.blit(shieldImage, Rect(xMoving[i]+5,yMoving[i]+20,10,10)) #display the shield of the character
            countingMagicSeconds += 1 #add to the counter variable that is the timer for the magic potion 
            print (countingMagicSeconds)
            if countingMagicSeconds == 300: #if the timer reaches 300:
                shieldActivation = False    #get rid of the shield
                countingMagicSeconds = 0    #set the timer back to 0
            
        if mouseX > 920 and mouseX < 970 and mouseY > 630 and mouseY < 700: #check if the mouse is in these coordinates; if it is,
            craigTheHelper = image.load("helper2.png")  #set the image for craig the helper (red eyes)
            screen.blit(craigTheHelper, Rect(920,630,10,10))    #display the image of the helper
        else:
            craigTheHelper = image.load("helper.png") #set the image for craig the helper (black eyes)
            screen.blit(craigTheHelper, Rect(920,630,10,10))    #display the image of the helper
        if instructionCheck == True:    #check if the instruction manual is true; if it is, 
            instructions() #call instructions for the user
      
        if enemyHealthX <= 0:  #if the enemy has a health less than 0
            gameMenu = False   #set the game menu screen to false
            nextLevelScreen = True   #move on to the next level screen
        if healthX <= 0: #check if the health is less than 0; if it is,
            gameMenu = False #set gameMenu to false
            endingScoreScreen = True #set the endingScoreScreen to True
#------------------------------------------------------------------------------------------------------------
    elif nextLevelScreen == True: #if the next level screen is set to true:
        screen.fill(WHITE)
        mouse1, mouse2 = mouse.get_pos()                            
        screen.blit(portalEntry2, Rect(600,300,0,0))        #set the display and background
        keys = key.get_pressed() #check if the keys are pressed
        for i in range(len(xMoving)): #check the movement of the character;
            turtleRect = Rect(xMoving[i]-85,yMoving[i]+12,0,0) #set a turtle image 
            screen.blit(turtle, turtleRect) #display the turtle image
            if keys[K_d]:
                xMoving[i] += turtleSpeed
            if keys[K_a]:
                xMoving[i] -= turtleSpeed           #check for movement of turtle based on user input; move based on turtle speed
            if keys[K_s]:
                yMoving[i] += turtleSpeed
            if keys[K_w] and yMoving[i] > 130:
                yMoving[i] -= turtleSpeed  
            if xMoving[i] > 580 and xMoving[i] < 700 and yMoving[i] > 270 and yMoving[i] < 350: #if the user is in these coordinates:
                if mouse1 > 600 and mouse1 < 700 and mouse2 > 400 and mouse2 < 450: #if the mouse hovers over these coordinates:
                    entryText = fontLoadingScreen.render("Enter",5,RED) #set the text colour to red
                    screen.blit(entryText, Rect(600,400,0,0))
                else:
                    entryText = fontLoadingScreen.render("Enter",5,BLACK) #set the text colour to default black
                    screen.blit(entryText, Rect(600,400,0,0)) #display the text
            screen.blit(rainClouds, Rect(xMoving[i]-80,130,0,0))
            screen.blit(rainClouds, Rect(xMoving[i],180,0,0))           #display the rain clouds 
            screen.blit(rainClouds, Rect(xMoving[i]-150,190,0,0))
        while len(playerBulletList) > 0: #while the bullet list is still full:
            playerBulletList.pop()  #remove the 
        objective() #calling the objective screen
#------------------------------------------------------------------------------------------------------------
    elif endingScoreScreen == True: #check if the ending score page is true; if it is,
        scorePage() #display the score page
#------------------------------------------------------------------------------------------------------------
    elif gameMenu2 == True:
        screen.fill(WHITE)   
        screen.blit(backgroundImage2, Rect(0,100,0,0))
        keys = key.get_pressed()                        #initial display of the screen
        for i in range(len(xMoving)):
            turtleRect = Rect(xMoving[i]-85,yMoving[i]+12,0,0)
            screen.blit(turtle, turtleRect)
            if keys[K_d]:
                xMoving[i] += turtleSpeed
            if keys[K_a]:                               #check for the movement of the turtle based on user input; moves based on turtle sped
                xMoving[i] -= turtleSpeed
            if keys[K_s]:
                yMoving[i] += turtleSpeed
            if keys[K_w] and yMoving[i] > 130:
                yMoving[i] -= turtleSpeed 
        xFlying = randint(1100,1150)
        yFlying = randint(200,600)              #random coordinates for the flying brain
        xFlyingList.append(xFlying)
        yFlyingList.append(yFlying)    
        for bullet in playerBulletList:     #for each bullet in the player bullet list:
            bullet.movement()           #calculate the movement of the bullets
            bullet.draw()               #draw the bullets
            if sqrt((xFlyingList[game2Counting]-bullet.PosX)**2 + (yFlyingList[game2Counting]-(bullet.PosY-50))**2) < 35: #if the bullets collide with the flying brain:
                playerBulletList.remove(bullet) #remove the bullet, to make it look like it hit the flying brain image
                flyingBrainHealth -= 15    #if the bullet hits the flying brain, get rid of the flying brains health
                if flyingBrainHealth <= 0: #if the health of the flying brain is less than 0:
                    game2Counting += 1  #increase the game2 counting counter variable
                    enemyCounting -= 1  #decrease the enemies counting
                    flyingBrainHealth = 140 #flying brain health is set back to 140
                    brainSpeed += 0.25 #speed of the flying brain is increased
                    scoreCounting += randint(5,50) #add a random number to the score
        mouseX,mouseY = mouse.get_pos()   #check the mouse position (x and y coordinates) of the mouse
        gameMenuScreen1(xMoving,yMoving,healthX) #display the game menu screen
        counter = 0     #counter back to 0     
        if keys[K_f] and magic == 242:      #if the user presses the key f, and the magic bar is full:
            print ("Special ability")
            shieldActivation = True     #activate the shield
            magic = 0         #set magic variable back to 0
        if keys[K_SPACE] and mouseX > xMoving[i]:   #if the user pressed space
            if counterBullet % initialFiringSpeed == 0:
                playerBulletList.append(playerBullet(mouseX,mouseY))   #add a bullet to the list
            counterBullet += 1 #add to the counter bullet variable
        if enemySpawningLevel2 == True: #check if the enemyspawning level 2 is true; if it is,
            screen.blit(flyingBrain, Rect(xFlyingList[game2Counting],yFlyingList[game2Counting],0,0))   #display the flying brain
            draw.rect(screen,RED,(xFlyingList[game2Counting]-20,yFlyingList[game2Counting]+100,flyingBrainHealth,20)) #draw the flying brains health
            draw.rect(screen,BLACK,(xFlyingList[game2Counting]-20,yFlyingList[game2Counting]+100,140,20),3)
            if xFlyingList[game2Counting] > 40: #if the brains list position is greater than 40:
                xFlyingList[game2Counting] -= brainSpeed #subtract from speed
            if xFlyingList[game2Counting] <= 40: #if the brains list position is less than 40:
                healthX -= 1    #subtract the health by 1
            if healthX <= 0:    #if your health is less than 0:
                endingScoreScreen = True #show the losing screen
            magicX = randint(1,500)
            magicY = randint(200,500)       #randomly spawn in potions
            magicPotionX.append(magicX)
            magicPotionY.append(magicY)
            screen.blit(magicPotionImage, Rect(magicPotionX[countingPotion],magicPotionY[countingPotion],10,10)) #display the image of the potion
            if sqrt(((magicPotionX[countingPotion]+30)-xMoving[i])**2 + ((magicPotionY[countingPotion]+30)-(yMoving[i]+40))**2) < 35:   #if the player collides with the potion:
                countingPotion += 1 #add to the counting potion
                magic += 20 #add to the magic bar value
                scoreCounting += 5 #add to the score value
                healthX += 5
                if magic > 242: #if the magic value is greater than 242:
                    magic = 242     #set the magic value to the maximum at 242 pixels display
            if shieldActivation == True: #If the shield is activated, 
                screen.blit(shieldImage, Rect(xMoving[i]+5,yMoving[i]+20,10,10)) #display the image of the shield
                countingMagicSeconds += 1 #add to counting magic (the timer for the shield)
                print (countingMagicSeconds)
                if countingMagicSeconds == 300: #if the timer hits 300 (roughly 7 seconds): 
                    shieldActivation = False #deactivate the shield
                    countingMagicSeconds = 0  #set the timer back to 0     
        enemyCountingText = fontLoadingScreen.render("Kills Left:" + str(enemyCounting),5,BLACK) #showcase the kills left to beat the level
        screen.blit(enemyCountingText, Rect(380,50,0,0))
        screen.blit(permafrostProtector, Rect(40,330,0,0)) #display the images of the permafrost and enemy counting text
        if enemyCounting == 0: #if the enemyCounting value is 0:
            gameMenu2 = False
            finalScreen = True #showcase the winning screen
#------------------------------------------------------------------------------------------------------------
    elif finalScreen == True: #if the final screen is true:
        screen.fill(WHITE) #fill the screen with white
        winningPage() #call the winning page background
  
#------------------------------------------------------------------------------------------------------------
    for evnt in event.get():    #for each event in pygame         
        if evnt.type == QUIT: #if the user exits:
            running = False #quit the program
        if evnt.type == MOUSEBUTTONDOWN: #if the user clicks
            mx, my = evnt.pos   #get the x and y coordinates of the click
            button = evnt.button 
            if mx > 530 and mx < 600 and my > 0 and my < 40 and gameMenu == True: #if the mx and my coordinates are inbetween these parameters, and the gameMenu is true: (start button)
                enemySpawningLevel1 = True #enemies now spawn
            if mx > 920 and mx < 970 and my > 630 and my < 700 and gameMenu == True: #if the mx and my coordinates are inbetween these parameters, and the gameMenu is true: 
                instructionCheck = True   #instruction check is true; shows the instruction page
                magic = 242 #magic value is 242
            if mx > 740 and mx < 780 and my > 150 and my < 190 and instructionCheck == True: #if the mx and my coordinates are inbetween these parameters, and the instruction check:
                instructionCheck = False #instruction check is false
                magic = 0 #magic back to false
            if mx > 400 and mx < 500 and my > 400 and my < 450 and endingScoreScreen == True: #if the mx and my coordinates are inbetween these parameters, and the endingScoreScreen is true: 
                running = False #running is false
            if mx > 600 and mx < 700 and my > 400 and my < 450 and homePageCheck == True: #if the mx and my coordinates are inbetween these parameters, and the homePageCheck is true:
                homePageCheck = False #homepage is now false
                gameMenu = True     #switch to the game menu screen 
            if mx > 600 and mx < 700 and my > 400 and my < 450 and nextLevelScreen == True: #if the mx and my coordinates are inbetween these parameters, and the nextLevelScreen is true:
                nextLevelScreen = False #nextlevelscreen is now false
                gameMenu2 = True   #switch to gamemenu2 screen
            if mx > 530 and mx < 600 and my > 0 and my < 40 and gameMenu2 == True:#if the mx and my coordinates are inbetween these parameters, and the gameMenu2 is true:
                enemySpawningLevel2 = True #enemySpawningLevel2 is now true
            if mx > 400 and mx < 500 and my > 400 and my < 450 and finalScreen == True: #if the mx and my coordinates are inbetween these parameters, and the endingScoreScreen is true: 
                running = False #running is false        
#------------------------------------------------------------------------------------------------------------             
            
    myClock.tick(60) #frames of 60
    display.flip() #flip every image
    
quit() #quit the program

### My attempt at using files with my work; didn't have enough time to do leaderboards, etc

#def homePage():
    #mx,my = mouse.get_pos()
    #infoText = fontLoadingScreen.render("Username:",5,(BLACK))
    #screen.blit(infoText, Rect(300,200,0,0))
    #if changingColour == True:
        #draw.rect(screen,RED,(475,200,300,50),2)
    #else:
        #draw.rect(screen,BLACK,(475,200,300,50),2)
    #passwordText = fontLoadingScreen.render("Password:",5,(BLACK))
    #screen.blit(passwordText, Rect(300,280,0,0))
    #if changingColour2 == True:
        #draw.rect(screen,RED,(475,280,300,50),2)
    #else:
        #draw.rect(screen,BLACK,(475,280,300,50),2)
    #if mx > 430 and mx < 700 and my > 375 and my < 395:
        #register = fontRegister.render("New to this game? Register now!",5,(RED))
        #screen.blit(register, Rect(430,375,10,10))
    #else:
        #register = fontRegister.render("New to this game? Register now!",5,(BLACK))
        #screen.blit(register, Rect(430,375,10,10))        

#username = ""
#def usernameInput():
    #usernameInputText = fontLoadingScreen.render(username,5,BLACK)
    #screen.blit(usernameInputText, Rect(480,200,0,0))
    
#password = ""
#def passwordInput():
    #passwordInputText = fontLoadingScreen.render(password,5,BLACK)
    #screen.blit(passwordInputText, Rect(480,280,0,0))  

#def enterButton():
    #mx, my = mouse.get_pos()
    #if mx > 300 and mx < 380 and my > 360 and my < 410:
        #enterText = fontLoadingScreen.render("Enter",5,RED)
        #screen.blit(enterText, Rect(300,360,0,0))
    #else:
        #enterText = fontLoadingScreen.render("Enter",5,BLACK)
        #screen.blit(enterText, Rect(300,360,0,0)) 

#if mx > 470 and mx < 770 and my > 200 and my < 250:
    #inputCheck = True
    #passwordCheck = False
    #changingColour = True
    #changingColour2 = False
    #usernameChecking = True     
    #passwordChecking = False
#elif mx > 470 and mx < 770 and my > 280 and my < 330:
    #passwordCheck = True
    #changingColour2 = True
    #changingColour = False
    #inputCheck = False
    #usernameChecking = False
    #passwordChecking = True
#elif mx > 430 and mx < 700 and my > 375 and my < 395:
    #register = True
    #homePageCheck = False
    #passwordCheck = False
    #inputCheck = False
    #usernameChecking = False
    #passwordChecking = False
    #changingColour = False
    #changingColour2 = False
    #dataCheck = False  
#else:
    #inputCheck = False
    #passwordCheck = False
    #changingColour = False
    #changingColour2 = False            
#if mx > 300 and mx < 380 and my > 360 and my < 410 and dataCheck == True:
    #numFile = open("in.dat","a")
    #num = username
    #num2 = password
    #numFile.write(str(num) + " " + str(num2) + "\n")
    #numFile.close()
    #homePageCheck = False
    #gameMenu = True
    
#if evnt.type == KEYDOWN and inputCheck == True and usernameChecking == True:
    #if evnt.unicode.isalpha() and len(username) < 10:
        #username += evnt.unicode
    #elif evnt.unicode.isdigit() and len(username) < 10:
        #username += evnt.unicode
    #elif evnt.key == K_BACKSPACE:
        #username = username[:-1]
    #elif evnt.key == K_SPACE:
        #username += " "
    #elif evnt.key == K_DOWN or evnt.key == K_RETURN:
        #passwordCheck = True
        #changingColour2 = True
        #changingColour = False
        #inputCheck = False
        #usernameChecking = False
        #passwordChecking = True
#if evnt.type == KEYDOWN and passwordCheck == True and passwordChecking == True:
    #if evnt.unicode.isalpha() and len(password) < 10:
        #password += evnt.unicode
    #elif evnt.unicode.isdigit() and len(password) < 10:
        #password += evnt.unicode
    #elif evnt.key == K_BACKSPACE:
        #password = password[:-1]
    #elif evnt.key == K_SPACE:
        #password += " " 
    #elif evnt.key == K_UP:
        #inputCheck = True
        #passwordCheck = False
        #changingColour = True
        #changingColour2 = False
        #usernameChecking = True
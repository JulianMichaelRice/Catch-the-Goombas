"""
Julian Michael Rice: SuperCoding 2019
Welcome to Python: Advanced Projects!

Week 4 - PyGame: Catch the Goombas
"""
import pygame, time, random

#Some colors and other constants for us to use (RGB)
WHITE = (255, 255, 255)     #Alpha is another possible parameter to use
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

#Grade Constants
SS = 100 ; S = 70 ; A = 50 ; B = 35 ; C = 25 ; D = 15 ; F = 0

#We are going to initialize pygame
pygame.init()

#Setting up a song to play during the game
song = 'C:/Users/Julian Michael Rice/Documents/w4.ogg'
pygame.mixer.music.load(song)
pygame.mixer.music.play(1)

#Setting up some system variables and timing
clock = pygame.time.Clock()
FPS = 60
DISPLAY_W = 1280
DISPLAY_H = 720

#Setting up a font for the game
font = pygame.font.SysFont(None, 40)

#Set up the game display and window text
gameDisplay = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('Practical Coding 2019 - Julian!')

#The game can be restarted until the user inputs Q after a game over
gameContinue = True

##---- CLASS DEFINITION ----##
class Player():
    "Class definition for the player of the game"
    def __init__(self):
        "Define all of the player's stats and parameters"
        #Setting up the player's sprite and loading the image
        pygame.sprite.Sprite.__init__(self)
        
        #Note, you will have to modify this path on your own!
        self.image = pygame.image.load('C:/Users/Julian Michael Rice/Documents/player.png')

        #General private variables
        self.lead_x = DISPLAY_W/2   #Current x position
        self.lead_y = DISPLAY_H/2   #Current y position
        self.lead_x_change = 0      #Movement in x direction
        self.lead_y_change = 0      #Movement in y direction
        self.block_velocity = 5     #Player's velocity
        self.block_width = 30       #Player's body's width
        self.block_height = 30      #Player's body's height
        self.sprint_constant = 2    #Sprint speed
        self.score = 0              #Final score

        #This takes the dimensions and position of the player as a rectangle
        self.form = self.image.get_rect()
        
        #You must use .x and .y member variables (of rect) to change coordinates
        self.form.x, self.form.y = self.lead_x, self.lead_y

    def getCoord(self, coord):
        "Return member variables relating to current movement coordinates"
        if coord == "x":
            return self.lead_x
        elif coord == "y":
            return self.lead_y
        else:
            print("ERROR: Coordinate Processing")
            quit()
    
    def setCoord(self, coord, new):
        "Set a new coordinate to the x/y position of the player"
        if coord == "x":
            self.lead_x = new
        elif coord == "y":
            self.lead_y = new
        else:
            print("ERROR: Coordinate Setting")
            quit()
    
    def setNewCoord(self, coord, new):
        "Set a new coordinate to the to update x/y position of the player"
        if coord == "x":
            self.lead_x_change = new
        elif coord == "y":
            self.lead_y_change = new
        else:
            print("ERROR: New Coordinate Setting") 
            quit()
    
    def getNewCoord(self, coord):
        "Return member variables relating to updated movement coordinates"
        if coord == "x":
            return self.lead_x_change
        elif coord == "y":
            return self.lead_y_change
        else:
            print("ERROR: New Coordinate Processing")
            quit()
    
    def getBlockParameters(self, parameter):
        "Return member variables relating to the player's character details"
        if parameter == "velocity":
            return self.block_velocity
        elif parameter == "width":
            return self.block_width
        elif parameter == "height":
            return self.block_height
        elif parameter == "sprint":
            return self.sprint_constant
        else:
            print("ERROR: Block Parameter Processing")
            quit()
    
    def getScore(self):
        "Return player's current score"
        return self.score
    
    def setScore(self, new_score):
        "Update the player's current score"
        self.score += new_score

    def getImage(self):
        "Return the sprite, greenba."
        return self.image

    def getForm(self):
        "Return the player's body (form)"
        return self.form

    def setForm(self):
        "Generate the player's body (form) for a single frame"
        self.form.x, self.form.y = self.lead_x, self.lead_y
        #First part of the tutorial (below)
        #self.form = pygame.Rect(self.lead_x, self.lead_y, self.block_width, self.block_height)

##---- General Functions ----##
def text_objects(text, color):
    "Return details for the text surface and the rectangle encompassing it"
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(message, color, width=DISPLAY_W/2, height=DISPLAY_H/2):
    "Output a text message to the screen"
    textSurf, textRect = text_objects(message, color)
    
    #Mark where the center of the rectangle is (coordinates and tuples)
    textRect.center = (width, height)
    
    #Put the font onto the screen
    gameDisplay.blit(textSurf, textRect)

def calculateGrade(score):
    "Calculate the player's grade from the number of points scored"
    grade = ""
    if (player.getScore() > SS):
        grade = "SS"
        difference = 0
    elif (player.getScore() > S):
        grade = "S"
        difference = SS - player.getScore()
    elif (player.getScore() > A):
        grade = "A"
        difference = S - player.getScore()
    elif (player.getScore() > B):
        grade = "B"
        difference = A - player.getScore()
    elif (player.getScore() > C):
        grade = "C"
        difference = B - player.getScore()
    elif (player.getScore() > D):
        grade = "D"
        difference = C - player.getScore()
    else:
        grade = "F"
        difference = D - player.getScore()
    return difference, grade

def gameLoop():
    "Overall game flow function"
    gameExit = False                #Did the game end?
    gameOver = False                #Did the player lose by hitting a Mario bot?
    global gameContinue             #Restart this function or quit the program
    
    player = Player()               #Define our player here    
    enemyCooldown = 3000            #Enemy cooldown before spawning more bots
    
    now = pygame.time.get_ticks()   #Get current time
    intensity = 1                   #Set the intensity to 1 (spawn rate per cooldown)

    goomba_width = 30               #Width of the green goal object
    goomba_height = 30              #Height of the green goal object
    goomba_image = pygame.image.load("C:/Users/Julian Michael Rice/Documents/greenba.png")
    goomba_form = goomba_image.get_rect()

    mario_bots = []                 #List of all current mario bots (to draw out later)
    mario_width = 30                #Width of one mario bot
    mario_height = 30               #Height of one mario bot
    mario_image = pygame.image.load("C:/Users/Julian Michael Rice/Documents/enemy.png")
    mario_form = mario_image.get_rect()

    #Random location placement for goombas
    randGoombaX = round(random.randrange(0, DISPLAY_W - goomba_width) / 5.0) * 5.0
    randGoombaY = round(random.randrange(0, DISPLAY_H - goomba_height) / 5.0) * 5.0
    goomba_form.x, goomba_form.y = randGoombaX, randGoombaY

    #Random location placement for a mario bot
    randMarioX = round(random.randrange(0, DISPLAY_W - mario_width) / 5.0) * 5.0
    randMarioY = round(random.randrange(0, DISPLAY_H - mario_height) / 5.0) * 5.0
    mario_form.x = randMarioX
    mario_form.y = randMarioY

    while not gameExit:
        while gameOver:
            #Game Over!
            gameDisplay.fill(RED)
            message_to_screen("Game Over! Press C to Retry | Press Q to Quit", WHITE)
            
            #Finding out what grade the player achieved
            difference, grade = calculateGrade(player.getScore()) #Returns two values
            
            #Output all results to the game over screen
            message_to_screen("Final Grade: " + grade, WHITE, DISPLAY_W/2, DISPLAY_H/2 - 100)
            message_to_screen("Score: " + str(player.getScore()), WHITE, DISPLAY_W/2, DISPLAY_H/2 - 150)
            message_to_screen("Next Rank: " + str(difference) + " more points needed...", WHITE, DISPLAY_W/2, DISPLAY_H/2 - 50)
            pygame.display.update()

            #Game Over screen's event handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #If Q is pressed, quit this game and do not continue
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                        gameContinue = False
                        return
                    #If C is pressed, quit this game but do continue playing
                    elif event.key == pygame.K_c:
                        gameExit = True
                        gameOver = False
                        gameContinue = True
                        return

        #Note that an event is only a change in status
        for event in pygame.event.get():
            #Use pygame.QUIT because we are refering to pygame's QUIT.
            if event.type == pygame.QUIT: #If we exit out the window
                gameExit = True
                
            #Check for a key pressing event
            if event.type == pygame.KEYDOWN:
                #Note that the origin of the window is at the top left-most spot.
                #Check for general movement (arrow keys)
                if event.key == pygame.K_LEFT:
                    player.setNewCoord("x", -player.getBlockParameters("velocity"))
                elif event.key == pygame.K_RIGHT:
                    player.setNewCoord("x", player.getBlockParameters("velocity"))
                if event.key == pygame.K_UP:
                    player.setNewCoord("y", -player.getBlockParameters("velocity"))
                elif event.key == pygame.K_DOWN:
                    player.setNewCoord("y", player.getBlockParameters("velocity"))

                #Check for sprinting (left shift)
                if event.key == pygame.K_LSHIFT:
                    player.setNewCoord("x", player.getNewCoord("x") * player.getBlockParameters("sprint"))
                    player.setNewCoord("y", player.getNewCoord("y") * player.getBlockParameters("sprint"))
            
            #Stop moving when the key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.setNewCoord("x", 0)
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.setNewCoord("y", 0)
                
                if event.key == pygame.K_LSHIFT:
                    player.setNewCoord("x", player.getNewCoord("x") / player.getBlockParameters("sprint"))
                    player.setNewCoord("y", player.getNewCoord("y") / player.getBlockParameters("sprint"))
        
        #Boundary checking - game over if the player touches the boundaries
        if player.getCoord("x") + player.getNewCoord("x") >= DISPLAY_W - player.getBlockParameters("width") or player.getCoord("x") + player.getNewCoord("x") <= 0:
            player.setNewCoord("x", 0)
            gameOver = True
        if player.getCoord("y") + player.getNewCoord("y") >= DISPLAY_H - player.getBlockParameters("height") or player.getCoord("y") + player.getNewCoord("y") <= 0:
            player.setNewCoord("y", 0)
            gameOver = True
        
        #Update the position of the player
        new_pos_x = player.getCoord("x") + player.getNewCoord("x")
        new_pos_y = player.getCoord("y") + player.getNewCoord("y")
        player.setCoord("x", new_pos_x)
        player.setCoord("y", new_pos_y)
        
        #Fill the screen with a black background
        gameDisplay.fill(BLACK)
        
        #Check the enemy cooldown - is it time to generate more enemies?
        ticks = pygame.time.get_ticks()
        if ticks - now >= enemyCooldown:
            now = ticks
            
            #Increase the number of red squares placed in a frame
            intensity += 1
            
            count = 1
            while count != intensity:
                #Generate random coordinates for every new mario bot
                randMarioX = round(random.randrange(0, DISPLAY_W - mario_width) / 5.0) * 5.0
                randMarioY = round(random.randrange(0, DISPLAY_H - mario_height) / 5.0) * 5.0
                
                #Create a new mario rectangle with previously generated random coordinates
                mario_form = mario_image.get_rect()
                mario_form.x = randMarioX
                mario_form.y = randMarioY
                
                #Add this newly made mario bot to the list of all mario bots to draw out
                mario_bots.append(mario_form)
                count += 1
                
        #Draw out every mario bot onto the screen
        for bot_form in mario_bots:
            gameDisplay.blit(mario_image, bot_form)
        
        #Update the location of the goomba goal
        goomba_form.x, goomba_form.y = randGoombaX, randGoombaY
        
        #Setup the player for drawing 
        player.setForm()
        mainBox = player.getForm()

        #Draw out the goomba goal and the player's location
        gameDisplay.blit(goomba_image, goomba_form)
        gameDisplay.blit(player.getImage(), player.getForm())
        
        #Draw out the score layered above everything else (like a real UI system)
        message_to_screen("Score: " + str(player.getScore()), BLUE, 60, 20)
        
        #Update the game display
        pygame.display.update() 

        #Check if the player collided into the goal goomba or not
        if mainBox.colliderect(goomba_form):
            #Generate new coordinates for the next goal goomba
            randGoombaX = round(random.randrange(0, DISPLAY_W - goomba_width) / 10.0) * 10.0
            randGoombaY = round(random.randrange(0, DISPLAY_H - goomba_height) / 10.0) * 10.0
            
            #Depending on the number of mario bots on the screen, how many points are earned?
            if len(mario_bots) < 10:
                player.setScore(1)
            elif len(mario_bots) >= 10 and len(mario_bots) < 30:
                player.setScore(2)
            elif len(mario_bots) >= 30 and len(mario_bots) < 50:
                player.setScore(3)
            elif len(mario_bots) >= 50 and len(mario_bots) < 80:
                player.setScore(4)
            else:
                player.setScore(5)
        
        #If the player collided with any mario bots, then it's a game over!
        for bot in mario_bots:
            if mainBox.colliderect(bot):
                gameOver = True
                break
        
        #Tick and process everything at the FPS set earlier
        clock.tick(FPS)

    #Player quit the game - shutdown process
    message_to_screen("You quit the game!", RED)
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    quit()

def main():
    while gameContinue:
        gameLoop()
        
##---- START HERE ----##
if __name__ == '__main__':
    main()
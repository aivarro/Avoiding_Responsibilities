import pygame
import time
import random

pygame.init()

# sounds and volumes
crash_sound = pygame.mixer.Sound('scream.wav')
pygame.mixer.music.load('funny.mp3')
crash_sound.set_volume(0.4)
pygame.mixer.music.set_volume(0.2)

display_width = 800
display_height = 600

black = (0,0,0)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

player_width = 140

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Avoiding Responsibilities')
clock = pygame.time.Clock()

playerImg = pygame.image.load('player.png')

pygame.display.set_icon(pygame.image.load('icon.png'))

pause = True

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Procrastination Points: ' + str(count), True, black)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def player(x,y):
    gameDisplay.blit(playerImg,(x,y))
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()   
    
def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)    
    
    largeText = pygame.font.Font('freesansbold.ttf',24)
    TextSurf, TextRect = text_objects('Responsibilities will always find a way to get you!', largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        mouse = pygame.mouse.get_pos()
        button('PLAY AGAIN',150,450,150,50,green,bright_green,game_loop)
        button('QUIT',550,450,100,50,red,bright_red,quitgame)
            
        pygame.display.update()
        clock.tick(15)

# button mechanics
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    
def quitgame():
    pygame.quit()
    quit()
    
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    
def paused():

    pygame.mixer.music.pause()

    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects('PAUSED', largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        mouse = pygame.mouse.get_pos()
        button('UNPAUSE',150,450,150,50,green,bright_green,unpause)
        button('QUIT',550,450,100,50,red,bright_red,quitgame)
            
        pygame.display.update()
        clock.tick(60)
    
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill((random.randrange(1, 255),random.randrange(1, 255),random.randrange(1, 255)))
        largeText = pygame.font.Font('freesansbold.ttf',60)
        TextSurf, TextRect = text_objects('Avoiding Responsibilities', largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        mouse = pygame.mouse.get_pos()
        
        button('START',150,450,100,50,green,bright_green,game_loop)
        button('QUIT',550,450,100,50,red,bright_red,quitgame)
            
        pygame.display.update()
        clock.tick(60)
    
def game_loop():
    global pause
    
    pygame.mixer.music.play(-1)
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    
    thing_startx = random.randrange(0, display_width-100)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        # initiates the player movement          
        x += x_change
        # background color
        gameDisplay.fill((random.randrange(1, 255),random.randrange(1, 255),random.randrange(1, 255)))
        # block color
        block_color = (random.randrange(1, 255),random.randrange(1, 255),random.randrange(1, 255))
        gameDisplay.blit(playerImg,(x,y))
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        player(x,y)
        things_dodged(dodged)
        
        # wall collisions
        if x < 0:
            x = 0
        elif x > display_width - player_width:
            x = display_width - player_width
        
        # what happens when a block goes out of the bottom border
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width-100)
            dodged += 1
            thing_speed *= 1.01
            if dodged > 20:
                thing_speed *= 1.04
            elif dodged > 10:
                thing_speed *= 1.02
        
        # player collisions
        if y < thing_starty+thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + player_width > thing_startx and x + player_width < thing_startx + thing_width or x < thing_startx and x + player_width > thing_startx + thing_width:
                crash()
                
        # sets everything running at 60fps        
        pygame.display.update()
        clock.tick(60)

game_intro()    
game_loop()
pygame.quit()
quit()

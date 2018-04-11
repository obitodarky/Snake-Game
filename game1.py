import pygame
import time
import random
import cx_Freeze

pygame.init() #necessary to call the method

white=(255,255,255) #RedGreenBlue value of the color white in a tuple, can also be a list
black=(0,0,0) #RGB vlue for the color black
red=(255,0,0)
green=(0,155,0)
blue=(0,0,225)

display_width=800
display_height=600
gameExit = False
gameOver = False  # when the game is over what to do , exit the game or start again

lead_x = display_width / 2
lead_y = display_height / 2

lead_x_change = 0  # 0 beacuse we will not be changing the position in the beginning
lead_y_change = 0

gameDisplay=pygame.display.set_mode((display_width,display_height)) #parameter must  a tuple or a list describing the pixels i.e 800x600 pixels

pygame.display.set_caption('PEN APPLE PEN') #game title : snake game

#pygame.display.flip() #works like a flip book, animates the entire surface

#pygame.display.update() #works like a flip book, animates surfaces and updates when called


'''lead will be the leader of the group of blocks in the snake
   the snake will be made up of multiple blocks and lead will be the
   1st main block of the snake(head of the snake)
'''

clock=pygame.time.Clock() #the frames per second BIF in pygame

FPS=15

direction='right'

AppleThickness=30

block_size=20

score=0

img=pygame.image.load('pen.jpg  ')

apple=pygame.image.load('apple.png')

icon=pygame.image.load('apple.png')

pygame.display.set_icon(icon)

font=pygame.font.SysFont(None,25) #25 is the size of the font

smallfont=pygame.font.SysFont('comicsansms',25)
medfont=pygame.font.SysFont('comicsansms',50)
largefont=pygame.font.SysFont('comicsansms',60)

def pause():
    paused=True
    #gameDisplay.fill(white)
    message_to_screen("Paused", black, -100, size="medium")
    message_to_screen("Press C to continue or Q to quit", black, 25)

    pygame.display.update()

    clock.tick(5)
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    paused=False
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()


def score(score):
    text=smallfont.render('Score : ' + str(score),True,black)
    gameDisplay.blit(text,[0,0])


def randAppleGen():
    randAppleX = round(random.randrange(0,
                                        display_width - AppleThickness))  # /10.0)*10.0 # it is possible that it just displays the apple at 800 and then the size of the apple will go out of range
    randAppleY = round(random.randrange(0,
                                        display_height - AppleThickness))  # /10.0)*10.0 #rounds the position of apple to a multiple fo 10 so it matches with the snake block
    return randAppleX,randAppleY

def game_intro():
    intro=True

    while intro:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


        gameDisplay.fill(white)
        message_to_screen("Welcome to the Snake Game",green,-100,'large')
        message_to_screen('The objective of the game is to eat red apples',black,-30)
        message_to_screen('The more appples you eat,the longer you get', black, 10)
        message_to_screen('If you run into yourself or the edges , you die and game is over ', black, 50)
        message_to_screen('Press C to play , Q to quit and P to pause ', black, 150)

        pygame.display.update()
        clock.tick(15)

def snake(block_size,snakelist):

    if direction=='right':
        head=pygame.transform.rotate(img,270)
    if direction=='left':
        head=pygame.transform.rotate(img,90)
    if direction=='up':
        head=img
    if direction=='down':
        head=pygame.transform.rotate(img,180)

    gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))

    for XnY in snakelist[:-1]: #for each item in snake list
        pygame.draw.rect(gameDisplay,blue,[XnY[0],XnY[1],block_size,block_size]) # lead_x=XnY[0] and lead_y=XnY[1]

def text_objects(text,color,size):
    if size=='small':
        textSurface=smallfont.render(text,True,color)
    elif size=='medium':
        textSurface = medfont.render(text, True, color)
    elif size=='large':
        textSurface=largefont.render(text,True,color)

    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size='small'): #the message and the color of the message
    textSurf,textRect = text_objects(msg,color,size)
    #screen_text=font.render(msg,True,color)
    #gameDisplay.blit(screen_text,[display_width/2,display_height/2]) #updates the screen
    textRect.center=(display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)


def gameLoop():

    global direction
    direction="right"
    gameExit = False
    gameOver=False #when the game is over what to do , exit the game or start again

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10  # 0 beacuse we will not be changing the position in the beginning
    lead_y_change = 0

    snakeList = []
    snakeLength=1 #at the begining of the loop, the lenght of the snake is 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit: #game loop

        if gameOver==True:
            message_to_screen('Game Over', red, -50, size='large')
            message_to_screen("Press C to play again or Q to quit ", black, 50, size='medium')
            pygame.display.update()

        while gameOver == True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameExit=True
                    gameOver=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #if user presses 'Q' , it will quit the game
                        gameExit = True
                        gameOver = False
                    if event.key==pygame.K_c: #if user presses 'C' it will continue to loop
                        gameLoop()  #calling gameLoop withign game loop so that the functions starts over from scratch

        for event in pygame.event.get():  #event handling BIF in pygame EVENT LOOP
            #print(event) # prints out the position of the mouse and the buttons pressed when in game window
            if event.type== pygame.QUIT: #if the user presses the [x] in game window, it quits the window
                gameExit=True

            if event.type==pygame.KEYDOWN:#event.type refers to the assigned functions(BIF) if pygame
                #Keydown means while any key is pressed
                if event.key==pygame.K_LEFT:
                    '''lead_x-=10
                    if the user presses the left arrow key
                       lead_x-=10 will be implemented since , and -= refers to
                       the co-ordinates will be shifted to the left i.e left side of the X-axis
                        thus, - = 10(because the block is 10 wide and tall)
                if event.key==pygame.K_RIGHT:
                    lead_x+=10'''

                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size #10 is the number of pixels moved in one loop
                    lead_y_change=0
                    direction='left'

                elif event.key==pygame.K_RIGHT:
                    lead_x_change=  block_size
                    lead_y_change=0
                    direction='right'

                elif event.key==pygame.K_UP:
                    lead_y_change= -block_size
                    lead_x_change=0
                    direction='up'


                elif event.key==pygame.K_DOWN:
                    lead_y_change= block_size
                    lead_x_change=0
                    direction='down'


                elif event.key==pygame.K_p:
                    pause()

                '''if event.type==pygame.KEYUP: #when user releases the key
                           if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                               lead_x_change=0'''


        if lead_x>=display_width or lead_x<0 or lead_y>display_height or lead_y<0:
            gameOver=True #once gameOver==True , the while gameOver==True: loop will start running



        lead_y+=lead_y_change
        lead_x+=lead_x_change #will add lead_x_change to lead_x LOGIC LOOP
        '''SINCE THE WHILE LOOP RUNS LIKE, 1000 times a second,
                the lead_x will add the lead_x_change a 1000 times
                i.e 10 will be added 1000 times in one second thus,'''



        gameDisplay.fill(white) #fills the display surface object, backgroud color is the parameter filled in
        #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(apple,[randAppleX,randAppleY])

        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead) #List inside a list

        if len(snakeList)>snakeLength:
            del snakeList[0] #get rid of the first element in the list if lenghth of snake list is greater than 1

        for eachSegment in snakeList[:-1]: #the last segment is the head so we want to exclude that out
            if eachSegment==snakeHead: #if the segment is identical to the cordinates of the snakehead
                gameOver=True


        snake(block_size,snakeList)
        '''draws a rectangle on the screen ,with parameters of
                           #where to draw on the screen
                           #color of the rectangle is second parameter
                           #and co-ordinates of the rectangle(where to daw on display screen), and with,height of the rectangle'''

        #pygame.draw.rect(gameDisplay, red, [400, 300, 10, 10])
        #overlaps the position of anything present in the same co-ordinate

        #gameDisplay.fill(red,rect=[200,200,50,50])
        ''' you can make a rectangle also by using the .fill function
            with the cordinates of 1)where to display in the screeen(co-ordinates)
                                   2)width,height of the rectangle
            .fill can be graphics accelerated and can be used to make processing quicker as compared
                    to .draw function'''

        score(snakeLength-1)

        pygame.display.update() #after done with all the action,update the surface


    #To make sure even if we change the thickness of the apple , we can still eat it when within
    #the boundary of the apple


        # if lead_x>=randAppleX and lead_x<=randAppleX+AppleThickness:
        #       if lead_y>=randAppleY and lead_y<=randAppleY+AppleThickness:
        #           randAppleX = round(random.randrange(0, display_width - block_size))# / 10.0) * 10.0 #does not always spawn in a location as a multiple of 10
        #           randAppleY = round(random.randrange(0, display_height - block_size) )#/ 10.0) * 10.0
        #           snakeLength+=1 #increases the length of the snake everytime it eats an apple

        if lead_x >randAppleX and lead_x<randAppleX+AppleThickness or lead_x +block_size>randAppleX and lead_x+block_size<randAppleX+AppleThickness:
            if lead_y>randAppleY and lead_y<randAppleY+AppleThickness or lead_y+block_size>randAppleY and lead_y+block_size<randAppleY+AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength+=1 #increases the length of the snake everytime it eats an apple




        clock.tick(FPS) #runs the game at 30FPS

    pygame.quit()
    quit()

game_intro()
gameLoop()

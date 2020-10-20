import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/player.png'
BACKGROUND = 'gallery/sprites/background-day.png'
PIPE = 'gallery/sprites/pipe.png'
MESSAGE = 'gallery/sprites/message.png'


def welcomeScreen():
    #Shows welcome image on the screen

    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get(
        ):  #tells us that the user has entered or clicked somethng on the screen

            #if user has clicked on cross button then close the game
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                #if the user presses space or up key then start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE
                                            or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                #SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def mainGame():

    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    #Create two pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [{
        'x': SCREENWIDTH + 200,
        'y': newPipe1[0]['y']
    }, {
        'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2),
        'y': newPipe2[1]['y']
    }]

    #list of lower pipes
    lowerPipes = [{
        'x': SCREENWIDTH + 200,
        'y': newPipe1[0]['y']
    }, {
        'x': SCREENWIDTH + 200 + SCREENWIDTH / 2,
        'y': newPipe2[1]['y']
    }]

    pipeVelX = -4  #negative as pipes will move in the backward direction
    playerVelY = -9  #player will fall down with velocity
    playerMaxVelY = -10  #player max velocity
    playerMinVelY = -8  #player min velocity
    playerAccY = -1

    playerFlapVel = -8  #velocity while flapping
    playerFlapped = False  #It is true when the bird is flapping

    while True:
        for event in pygame.event.get():
            print(f"event Type : {event.type} = {pygame.KEYDOWN}")
            print(f"event Key : {event.key} = {pygame.K_UP}")
            if event.type == QUIT or (event.type == pygame.KEYDOWN
                                      and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP):
                print(f"playery : {playery}")
                if playery > 0:
                    playerVelY = playerFlapVel
                    print(f"will fall down with : {playerVelY}")
                    playerFlapped = True

        print(f"flapped : {playerFlapped}")
        crashTest = isCollide(
            playerx, playery, upperPipes,
            lowerPipes)  #This function will return true if player has crashed
        # if crashTest:
        #     return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMiddlePosition = pipe['x'] + GAME_SPRITES['pipe'][0].get_width(
            ) / 2
            if pipeMiddlePosition <= playerMidPos < pipeMiddlePosition + 4:
                score += 1
                print(f"Your Score is {score}")

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #add a new pipe when the first is about to cross the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #if pipe is out of the screen then remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():

            upperPipes.pop(0)
            lowerPipes.pop(0)

        #blit the sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))

        #blit the upper and lower pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]

        width = 0

        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (xoffset, SCREENHEIGHT * 0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY or playery < 0:
        return True
    return False


def getRandomPipe():

    #Generate positions of two pipes(one straight and the other top rotated) for blitting on the screen
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(
        0,
        int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {
            'x': pipeX,
            'y': -y1
        },  #upper pipe
        {
            'x': pipeX,
            'y': y2
        }  #lower pipe
    ]

    return pipe


if __name__ == "__main__":
    #this will be the main function from where our game will start
    pygame.init()  #initialize pygame modules
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('FLAPPY BIRD')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['base'] = pygame.image.load(
        'gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(
        pygame.image.load(PIPE).convert_alpha(),
        180), pygame.image.load(PIPE).convert_alpha())

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['message'] = pygame.image.load(MESSAGE).convert_alpha()

    while True:
        welcomeScreen(
        )  #Shows welcome screen to the user until he/she presses a button
        mainGame()  #Main Game Function

import pygame
import logging
import os
from snake import Snake
from food import Food
from level import BackgroundLevel
from music import BackgroundMusic
from text import Text
from transition import Transition

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (196, 13, 13)
SLIVER = (192, 192, 192)

class Game(object):

    def __init__(self, screen):
        self.__currentLevel = 0
        self.__gameOver = False
        self.__exitGame = False
        self.__FPS = 30
        
        self.__backgroundMusic = BackgroundMusic("../Data/Music/")
        self.__backgroundMusic.playMusic("../Data/Music/")
        
        self.__gameOverMusicFile = os.path.abspath("../Data/Music/GameOverMusic/MetalGearGameOver.wav")
        
        self.__backgroundLevel = BackgroundLevel("../Data/Images/Levels/")
        self.__backgroundLevel.loadLevel("../Data/Images/Levels/", self.__currentLevel)

        self.__snake = Snake(screen.get_size())
        
        self.__apple = Food("../Data/Images/Sprites/", "RedApple.png")
        self.__apple.genRandomPosition(screen, self.__snake)
    
        self.__backgroundLevel.image = pygame.transform.scale(self.__backgroundLevel.image, screen.get_size())

        self.__gameOverText = Text("Game Over", "../Data/Fonts/", "Halo3.ttf", 100, DARK_RED)
        self.__gameOverText.renderText()
        textX = (screen.get_width() / 2) - (self.__gameOverText.textSize[0] / 2)
        textY = (screen.get_height() / 2) - (self.__gameOverText.textSize[1] / 2)
        self.__gameOverText.setPosition(textX, textY)

        self.__scoreText = Text("Score: " + str(self.__snake.getScore), "../Data/Fonts/", "neuropol x rg.ttf", 30, SLIVER)
        self.__scoreText.renderText()
        textX = screen.get_width() - self.__scoreText.textSize[0]
        self.__scoreText.setPosition(textX, 0)

        self.__transition = Transition(screen, "Fade Out", 255, BLACK)

    def __handleEvents(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT or (keys[pygame.K_F4] and keys[pygame.K_LALT]):
                self.__exitGame = True

            if event.type == pygame.KEYDOWN and self.__transition.isTransitionDone:
                self.__snake.changeDirection(keys)
            
            if event.type == BackgroundMusic.TRACK_END:
                self.__backgroundMusic.playNextMusic("../Data/Music/")

    def __update(self, screen, screenDimensions):
        if self.__snake.getSnakeSpeed != (0, 0) and self.__transition.isTransitionDone:
            self.__snake.move()

        if  self.__snake.snakeHead.rect.colliderect(self.__apple.rect):
            self.__snake.extend()
            self.__updateScore(screenDimensions)
            self.__apple.genRandomPosition(screen, self.__snake)

        if self.__snake.isSnakeShorter():
            self.__updateScore(screenDimensions)

        if  not self.__snake.isSnakeDead:
            self.__snake.checkBoundaries(screen, screenDimensions)

        if self.__snake.isSnakeDead:
            self.__snake.initiateDeathScene()
            self.__gameOver = True
            
    def __draw(self, screen):
        screen.fill(WHITE)
        
        screen.blit(self.__backgroundLevel.image, self.__backgroundLevel.rect)
        screen.blit(self.__apple.image, self.__apple.rect)

        screen.blit(self.__snake.snakeHead.image, self.__snake.snakeHead.rect)

        for segment in self.__snake.bodySegments:
            screen.blit(segment.image, segment.rect)

        screen.blit(self.__scoreText.label, self.__scoreText.labelRect)

        if self.__snake.isSnakeDead:
            screen.blit(self.__gameOverText.label, self.__gameOverText.labelRect)
        
        if not self.__transition.isTransitionDone:
            self.__transition.performTransition(screen)
        
        pygame.display.update()

    def __playGameOverScene(self, screen):      
        try:
            pygame.mixer.music.load(self.__gameOverMusicFile)
        except pygame.error as errorMessage:
            logging.exception(errorMessage)
            raise

        pygame.mixer.music.play()

        musicPlaying = True

        while musicPlaying and not self.__exitGame:
            musicPlaying = pygame.mixer.music.get_busy()

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT or (keys[pygame.K_F4] and keys[pygame.K_LALT]):
                    self.__exitGame = True

        self.__transition.setNewTransition("Fade In", 0, BLACK)

        while not self.__transition.isTransitionDone and not self.__exitGame:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
            
                if event.type == pygame.QUIT or (keys[pygame.K_F4] and keys[pygame.K_LALT]):
                    self.__exitGame = True
                
            self.__draw(screen)

    def __updateScore(self, screenDimensions):
        self.__snake.setScore = 1
        self.__scoreText.setText = "Score: " + str(self.__snake.getScore)
        self.__scoreText.renderText()
        textX = screenDimensions[0] - self.__scoreText.textSize[0]
        self.__scoreText.setPosition(textX, 0)
    
    def playGame(self, screen):
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()

        if pygame.event.get_blocked(self.__backgroundMusic.TRACK_END):
            pygame.event.set_allowed([self.__backgroundMusic.TRACK_END])

        screenDimensions = screen.get_size()
        
        while not self.__gameOver and not self.__exitGame:
            self.__handleEvents()
            self.__update(screen, screenDimensions)
            self.__draw(screen)
            clock.tick(self.__FPS)

        self.__backgroundMusic.stopMusic()

        if self.__gameOver:
            self.__playGameOverScene(screen)

        return self.__exitGame

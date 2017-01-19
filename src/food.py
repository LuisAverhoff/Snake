import pygame
import random
import logging
import os

class Food(pygame.sprite.Sprite):

    def __init__(self, path, file):
        super().__init__()

        imageFile = os.path.abspath(path + file)

        try:
            self.image = pygame.image.load(imageFile).convert_alpha()
        except pygame.error as errorMessage:
            logging.exception(errorMessage)
            raise

        self.rect = self.image.get_rect()

    def genRandomPosition(self, screen, snake):
        screenSize= screen.get_size()
        imageSize = self.image.get_size()
        
        positionOccupied = True

        while positionOccupied:
            randPosX = random.randrange(0, screenSize[0] - imageSize[0], imageSize[0])
            randPosY = random.randrange(0, screenSize[1] - imageSize[1], imageSize[1])

            self.rect.topleft = [randPosX, randPosY]

            if not snake.occupiesPosition(self.rect):
                positionOccupied = False

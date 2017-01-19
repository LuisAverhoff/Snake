import pygame
import random
import imghdr
import logging
import os

class BackgroundLevel(pygame.sprite.Sprite):

    def __init__(self, path):
        super().__init__()

        self.__levels = []

        levelDir = os.listdir(path)

        for file in levelDir:
            isImageFile = self.__checkIfImageFile(path + file)

            if isImageFile:
                self.__levels.append(file)

        self.__totalLevels = len(self.__levels)
        random.shuffle(self.__levels)

    def __checkIfImageFile(self, imageFile):
        isFile = os.path.isfile(imageFile)
        
        if isFile:
            isImageFile = imghdr.what(imageFile)
            if isImageFile is not None:
                return True

        return False

    def loadLevel(self, path, level):
        file = os.path.abspath(path + self.__levels[level])
        
        try:
            self.image = pygame.image.load(file).convert()
        except pygame.error as errorMessage:
            logging.exception(errorMessage)
            raise

        self.rect = self.image.get_rect()

    def finishedAllLevels(self, currentLevel):
        if currentLevel == self.__totalLevels - 1:
            return True
        
        return False

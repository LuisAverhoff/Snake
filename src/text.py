import pygame
import os

class Text(object):
    __cachedFonts = {}
    __cachedText = {}
    
    def __init__(self, text, path, fontName, fontSize, fontColor):
        self.__setFont(path, fontName, fontSize)    
        self.__text = text
        self.textSize = self.font.size(self.__text)
        self.__fontName = fontName
        self.__fontSize = fontSize
        self.__fontColor = fontColor

    def __setFont(self, path, fontName, fontSize):
        key = fontName + "|" + str(fontSize)
        self.font = Text.__cachedFonts.get(key, None)
        
        if self.font is None:
            try:
                self.font = pygame.font.Font(os.path.abspath(path + fontName), fontSize)
            except pygame.error as errorMessage:
                logging.exception(errorMessage)
                raise
            
            Text.__cachedFonts[key] = self.font

    def renderText(self):
        key = "|".join(map(str, (self.__fontName, self.__fontSize, self.__fontColor, self.__text)))
        self.label = Text.__cachedText.get(key, None)

        if self.label is None:
            self.label = self.font.render(self.__text, True, self.__fontColor)
            Text.__cachedText[key] = self.label
            
    def setPosition(self, x, y):
        self.labelRect = self.label.get_rect()
        self.labelRect[0] = x
        self.labelRect[1] = y

    @property
    def getText(self):
        return self.__text

    @getText.setter
    def setText(self, text):
        self.__text = text
        self.textSize = self.font.size(self.__text)

    def setFontColor(self, rgbTuple):
        self.__fontColor = rgbTuple
        self.renderText()

    def isMouseOverText(self, position):
        if(position[0] >= self.labelRect[0] and position[0] <= self.labelRect[0] + self.labelRect[2]) and \
          (position[1] >= self.labelRect[1] and position[1] <= self.labelRect[1] + self.labelRect[3]):
           return True

        return False

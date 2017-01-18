import pygame

class Transition(object):

    FADE_OUT = "Fade Out"
    FADE_IN = "Fade In"

    def __init__(self, screen, fadeType, alpha, color):
        self.__alphaSurface = pygame.Surface(screen.get_size())
        self.__fadeType = fadeType
        self.__alpha = alpha
        self.__alphaSurface.set_alpha(self.__alpha)
        self.__alphaSurface.fill(color)
        self.__isTransitionFinished = False

    def setNewTransition(self, fadeType, alpha, color):
        self.__fadeType = fadeType
        self.__alpha = alpha
        self.__alphaSurface.set_alpha(self.__alpha)
        self.__alphaSurface.fill(color)
        self.__isTransitionFinished = False

    def performTransition(self, screen):
        if self.__alpha != 0 and self.__fadeType == Transition.FADE_OUT:
            self.__alpha -= 5
            self.__alphaSurface.set_alpha(self.__alpha)
            screen.blit(self.__alphaSurface, (0,0))

            if self.__alpha == 0:
                self.__isTransitionFinished = True
                
        elif self.__alpha != 255 and self.__fadeType == Transition.FADE_IN:
            self.__alpha += 5
            self.__alphaSurface.set_alpha(self.__alpha)
            screen.blit(self.__alphaSurface, (0,0))

            if self.__alpha == 255:
                self.__isTransitionFinished = True

    @property
    def isTransitionDone(self):
        return self.__isTransitionFinished

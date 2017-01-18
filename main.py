import pygame
import logging
import os
from game import Game
from transition import Transition
from text import Text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIMEGREEN = (50, 205, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SLIVER = (192, 192, 192)

FLAGS = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

class GameMenu(object):

    colorButtonList = [LIMEGREEN, YELLOW, RED, SLIVER]

    def __init__(self, screen, items):
        self.screenSize = screen.get_size()
        self.__FPS = 30
        self.__exit = False
        self.__action = ""

        backgroundImageFile = os.path.join("Data/Images/MainMenuBackground.png")
        self.mainMenuMusicFile = os.path.join("Data/Music/MainMenuMusic/SuperMonkeyBall2SelectMode.wav")
        movementEffectFile = os.path.join("Data/Music/SoundEffects/MenuMovement.wav")
        selectionEffectFile = os.path.join("Data/Music/SoundEffects/MenuSelection.wav")
        
        try:
            self.__backgroundImage = pygame.image.load(backgroundImageFile).convert()
            pygame.mixer.music.load(self.mainMenuMusicFile)
            self.__movementSoundEffect = pygame.mixer.Sound(movementEffectFile)
            self.__selectionSoundEffect = pygame.mixer.Sound(selectionEffectFile)
        except pygame.error as errorMessage:
            logging.exception(errorMessage)
            raise

        self.__backgroundImage = pygame.transform.scale(self.__backgroundImage, screen.get_size())
        self.__backgroundRect = self.__backgroundImage.get_rect()

        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1, 0.0)
 
        self.__items = []
        self.__addMainMenuItems(items)
        self.__totalItems = len(self.__items)

        self.__BackToMenuText = Text("Back", "Data/Fonts/", "SpicyRice-Regular.otf", 35, BLACK)
        self.__BackToMenuText.renderText()
        posY = self.screenSize[1] - self.__BackToMenuText.textSize[1]
        self.__BackToMenuText.setPosition(0, posY)

        self.__mouseVisible = True
        self.__currentMenuItem = None

        self.__transition = Transition(screen, "Fade Out", 255, BLACK)

    def __addMainMenuItems(self, items):
        self.__titleMenuItem = Text("Welcome to Snake", "Data/Fonts/", "SpicyRice-Regular.otf", 50, BLACK)
        self.__titleMenuItem.renderText()
        posX = (self.screenSize[0] / 2) - (self.__titleMenuItem.textSize[0] / 2)
        posY = (self.screenSize[1] / 4) - (self.__titleMenuItem.textSize[1] / 4)
        self.__titleMenuItem.setPosition(posX, posY)        
        
        for index, item in enumerate(items):
           menuItem = Text(item, "Data/Fonts/", "SpicyRice-Regular.otf", 25, BLACK)
           menuItem.renderText()

           posX = (self.screenSize[0] / 2) - (menuItem.textSize[0] / 2)
           posY = (self.screenSize[1] / 2) - (menuItem.textSize[1] / 2) + ((index * 15) + (index * menuItem.textSize[1]))
           
           menuItem.setPosition(posX, posY)     
           self.__items.append(menuItem)

    def __setItemSelection(self, keys):

        for item in self.__items:
            item.font.set_italic(False)
            item.setFontColor(BLACK)

        if self.__currentMenuItem is None:
            self.__currentMenuItem = 0
        else:
            if keys[pygame.K_UP] and self.__currentMenuItem > 0:
                self.__currentMenuItem -= 1
            elif keys[pygame.K_UP] and self.__currentMenuItem == 0:
                self.__currentMenuItem = self.__totalItems - 1
            elif keys[pygame.K_DOWN] and self.__currentMenuItem < self.__totalItems - 1:
                self.__currentMenuItem += 1
            elif keys[pygame.K_DOWN]  and self.__currentMenuItem == self.__totalItems - 1:
                self.__currentMenuItem = 0

        self.__items[self.__currentMenuItem].font.set_italic(True)
        self.__items[self.__currentMenuItem].setFontColor(WHITE)
        self.__movementSoundEffect.play()

    def __setMouseSelection(self, item, mousePosition):
        if item.isMouseOverText(mousePosition):
            item.font.set_italic(True)
            item.setFontColor(WHITE)
        else:
            item.font.set_italic(False)
            item.setFontColor(BLACK)

    def __handleEvents(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT or (keys[pygame.K_F4] and keys[pygame.K_LALT]):
                self.__exit = True
            
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.__mouseVisible = False
                self.__setItemSelection(keys)

            if keys[pygame.K_RETURN] and self.__currentMenuItem is not None:
                 self.__action = self.__items[self.__currentMenuItem].getText
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                for item in self.__items:
                    if item.isMouseOverText(mousePosition):
                        self.__action = item.getText
            
        if pygame.mouse.get_rel() > (0, 0):
            self.__mouseVisible = True
            self.__currentMenuItem = None

        if self.__mouseVisible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
    
    def __draw(self, screen):
        screen.fill(WHITE)

        screen.blit(self.__backgroundImage, self.__backgroundRect)
        screen.blit(self.__titleMenuItem.label, self.__titleMenuItem.labelRect)

        for index, item in enumerate(self.__items):
            if self.__mouseVisible:
                mousePosition = pygame.mouse.get_pos()
                self.__setMouseSelection(item, mousePosition)
                
            pygame.draw.rect(screen, GameMenu.colorButtonList[index], item.labelRect)
            screen.blit(item.label, item.labelRect)

        if not self.__transition.isTransitionDone:
            self.__transition.performTransition(screen)
        
        pygame.display.update()

    def __executeAction(self, screen):
        if self.__action:
            if self.__action == 'Start':
                self.__selectionSoundEffect.play()
                self.__startGame(screen)
            elif self.__action == 'How to Play':
                self.__selectionSoundEffect.play()
                self.__showInstructions(screen)
            elif self.__action == 'Quit':
                self.__selectionSoundEffect.play()
                self.__exit = True

            self.__action = ""

    def __startGame(self, screen):
        pygame.mixer.music.stop()

        self.__transition.setNewTransition("Fade In", 0, BLACK)

        while not self.__transition.isTransitionDone and not self.__exit:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
            
                if event.type == pygame.QUIT or (keys[pygame.K_F4] and keys[pygame.K_LALT]):
                    self.__exit = True
                
            self.__draw(screen)

        if not self.__exit:
            game = Game(screen)
            self.__exit = game.playGame(screen)

        if not self.__exit:
            pygame.mixer.music.load(self.mainMenuMusicFile)
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play(-1, 0.0)
            self.__transition.setNewTransition("Fade Out", 255, BLACK)

    def __showInstructions(self, screen):
        if not self.__mouseVisible:
            pygame.mouse.set_visible(True)
            self.__mouseVisible = True

        while self.__action != "Back" and not self.__exit:
            mousePosition = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
            
                if event.type == pygame.QUIT or (keys[pygame.K_F4] and keys[pygame.K_LALT]):
                    self.__exit = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__BackToMenuText.isMouseOverText(mousePosition):
                        self.__action = self.__BackToMenuText.getText
            
            screen.fill(WHITE)
            screen.blit(self.__backgroundImage, self.__backgroundRect)
        
            pygame.draw.rect(screen, GameMenu.colorButtonList[3], self.__BackToMenuText.labelRect)
            screen.blit(self.__BackToMenuText.label, self.__BackToMenuText.labelRect)

            self.__setMouseSelection(self.__BackToMenuText, mousePosition)

            if not self.__transition.isTransitionDone:
                self.__transition.performTransition(screen)

            pygame.display.update()

    def run(self, screen):
        clock = pygame.time.Clock()

        pygame.event.set_allowed(None) # initially blocked all the events.
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]) # initialize the events that we are looking for
        
        while not self.__exit:
            self.__handleEvents()
            self.__draw(screen)
            self.__executeAction(screen)
            clock.tick(self.__FPS)

def initPygame():
    pygame.display.init()
    pygame.mixer.pre_init(22050, -16, 2, 4096)
    pygame.mixer.init()
    pygame.font.init()

def quitPygame():
    pygame.mixer.quit()
    pygame.display.quit()
    pygame.font.quit()
            
def main():
    initPygame()
    
    screen = pygame.display.set_mode((0, 0), FLAGS)

    menuItems = ('Start', 'How to Play', 'Quit')
    
    pygame.display.set_caption('Snake')

    gameMenu = GameMenu(screen, menuItems)
    gameMenu.run(screen)

    quitPygame()

if __name__ == "__main__":
    main()

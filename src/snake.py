import pygame
import logging
import os

class Snake(pygame.sprite.Sprite):
    # This dictionary contains all the possible combinations that the snake can move in degrees of 90 and 180.
    # For example, LeftUp means that the current direction of the snake is left and the new direction that the snake wants to move
    # in is Up hence LeftUp. The creation of this direction is through the concatenation of self.__currentDirection + self.__newDirection
    __angles = {
        "LeftUp": -90,
        "LeftDown": 90,
        "LeftRight": 180,
        "RightUp": 90,
        "RightDown": -90,
        "RightLeft": 180,
        "UpLeft": 90,
        "UpRight": -90,
        "UpDown": 180,
        "DownLeft": -90,
        "DownRight": 90,
        "DownUp": 180
        }

    __SEGMENT_DIMENSIONS = (32, 32)
    
    def __init__(self, screenDimensions):
        super().__init__()
        
        self.bodySegments = []
        self.__speed = (0, 0)
        self.__isSnakeDead = False
        self.__currentDirection = "Up" # Has to be up because the image in the directory Data/Images/Sprite/SnakeHead.png is pointing up initally.
        self.__newDirection = ""
        self.__lives = 3
        self.__score = 0
        # A private variable to keep track of the final rotation that needs to be performed when the snake dies and his head becomes red.
        # We need this because the red snake head image is initially rotated 90 degrees and when the green snake dies and the red snake image needs to be loaded,
        # it may not necessarily be pointing 90 degrees.
        self.__totalRotation = 0

        try:
            self.__gulpSoundEffect = pygame.mixer.Sound(os.path.abspath("../Data/Music/SoundEffects/Gulp.wav"))
            self.__cartoonSwipeSoundEffect = pygame.mixer.Sound(os.path.abspath("../Data/Music/SoundEffects/CartoonSwipe.wav"))
        except pygame.error as errorMessage:
            logging.exception(errorMessage)
            raise

        headPosition = (screenDimensions[0] / 2, screenDimensions[1] / 2)
        self.snakeHead = Snake._SnakeSegment(headPosition, "../Data/Images/Sprites/", "SnakeHead.png")
        
        for i in range(0, 4):
            segmentPosition = (headPosition[0], headPosition[1] + (Snake.__SEGMENT_DIMENSIONS[1] * (i + 1)))
            segment = Snake._SnakeSegment(segmentPosition, "../Data/Images/Sprites/", "SnakeBody.png")
            self.bodySegments.append(segment)

        self.__bodyLength = len(self.bodySegments)

    def occupiesPosition(self, objectRect):
        if self.snakeHead.rect.colliderect(objectRect):
            return True
        
        for segment in self.bodySegments:
           if segment.rect.colliderect(objectRect):
               return True

        return False

    def __getHeadDirection(self):
        head = self.bodySegments[0].rect
        neck = self.bodySegments[1].rect

        if head.x == neck.x:
            if head.y > neck.y:
                return "Down"
            else:
                return "Up"
        else:
            if head.x > neck.x:
                return "Right"
            else:
                return "Left"

    def changeDirection(self, keys):
        headDirection = ""
        
        if self.__bodyLength > 1:
            headDirection = self.__getHeadDirection()
        
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and headDirection != "Right":
            self.__speed = (Snake.__SEGMENT_DIMENSIONS[0] * -1, 0)
            self.__newDirection = "Left"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and headDirection != "Left":
            self.__speed = (Snake.__SEGMENT_DIMENSIONS[0], 0)
            self.__newDirection = "Right"
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and headDirection != "Down":
            self.__speed = (0, Snake.__SEGMENT_DIMENSIONS[1] * -1)
            self.__newDirection = "Up"
        elif (keys[pygame.K_DOWN] or keys[pygame.K_d]) and headDirection != "Up":
            self.__speed = (0, Snake.__SEGMENT_DIMENSIONS[1])
            self.__newDirection = "Down"

    def __rotateSnakeHead(self):
         rotation = Snake.__angles[self.__currentDirection + self.__newDirection]
         self.__totalRotation += rotation
         self.snakeHead.image = pygame.transform.rotate(self.snakeHead.image, float(rotation))
         self.__currentDirection = self.__newDirection

    def move(self):
        if self.__currentDirection != self.__newDirection:
            self.__rotateSnakeHead()
            
        if self.__bodyLength > 0:
            segment = self.bodySegments.pop()
            segment.rect.topleft = self.snakeHead.rect.topleft
            self.bodySegments.insert(0, segment)
            
        self.snakeHead.update(self.__speed)

    def extend(self):
        if not self.bodySegments:
            return

        self.__gulpSoundEffect.play()

        tailHead = self.bodySegments[self.__bodyLength - 1]

        if self.__bodyLength > 1:
            tailBone = self.bodySegments[self.__bodyLength - 2]

            if tailHead.rect.x == tailBone.rect.x:
                displacement = (self.__speed[0], self.__speed[1] * -1)
            else:
                displacement = (self.__speed[0] * -1, self.__speed[1])
        else:
            if self.__currentDirection == "Up" or self.__currentDirection == "Down":
                displacement = (self.__speed[0], self.__speed[1] * -1)
            else:
                displacement = (self.__speed[0] * -1, self.__speed[1])

        tailHead.update(displacement)
        self.bodySegments.append(Snake._SnakeSegment(tailHead.rect.topleft,"../Data/Images/Sprites/",  "SnakeBody.png"))
        self.__bodyLength += 1

    def __changeSnakeSkin(self):
        for index, segment in enumerate(self.bodySegments):
            segment = self.bodySegments.pop(index)
            newSegment = Snake._SnakeSegment(segment.rect.topleft, "../Data/Images/Sprites/", "SnakeRedBody.png")
            self.bodySegments.insert(index, newSegment)

        self.snakeHead = Snake._SnakeSegment(self.snakeHead.rect.topleft, "../Data/Images/Sprites/", "SnakeRedHead.png")
        self.snakeHead.image = pygame.transform.rotate(self.snakeHead.image, float(self.__totalRotation))

    def __cutSnake(self, segmentsToCut):
        for i in range(segmentsToCut):
            self.bodySegments.pop()
        
        self.__bodyLength -= segmentsToCut

        self.__score -= segmentsToCut
        
        if self.__score < 0:
            self.__score = 0
        
        self.__cartoonSwipeSoundEffect.play()
        
        self.__lives -= 1

        if not self.__lives:
            self.__isSnakeDead = True

    def isSnakeShorter(self):
        if self.__bodyLength > 8:
            for index, segment in enumerate(self.bodySegments):
                if self.snakeHead.rect.colliderect(segment.rect):
                    segmentsToCut = self.__bodyLength - index
                    self.__cutSnake(segmentsToCut)
                    return True
                
        return False
            
    def checkBoundaries(self, screen, screenDimensions):    
        position = (self.snakeHead.rect.x, self.snakeHead.rect.y)
        width = self.snakeHead.rect.width
        height = self.snakeHead.rect.height
                    
        if position[0] <= 0 or position[0] + width >= screenDimensions[0] or \
           position[1] <= 0 or position[1] + height >= screenDimensions[1]:
            self.__isSnakeDead = True

    def initiateDeathScene(self):
        self.__speed = (0, 0)
        self.__changeSnakeSkin()
            
    @property
    def isSnakeDead(self):
        return self.__isSnakeDead

    @property
    def getSnakeSpeed(self):
        return self.__speed

    @property
    def getScore(self):
        return self.__score

    @getScore.setter
    def setScore(self, score):
        self.__score += score

    class _SnakeSegment(pygame.sprite.Sprite):
        __SnakeImages = {}
        
        def __init__(self, position, path, file):
            super().__init__()

            if file not in Snake._SnakeSegment.__SnakeImages:
                snakeBodyFile = os.path.abspath(path + file)
         
                try:
                    Snake._SnakeSegment.__SnakeImages[file] = pygame.image.load(snakeBodyFile).convert_alpha()
                except pygame.error as errorMessage:
                    logging.exception(errorMessage)
                    raise
            
            self.image = Snake._SnakeSegment.__SnakeImages[file]
            self.rect = self.image.get_rect()
            self.rect.topleft = position

        def update(self, speed):
            self.rect.x += speed[0]
            self.rect.y += speed[1]

import pygame
import random
import sndhdr
import logging
import os

class BackgroundMusic(object):

    TRACK_END = pygame.USEREVENT + 1

    def __init__(self, path):
        self.__tracks = []
        self.__currentTrack = 0

        musicDir = os.listdir(path)

        for file in musicDir:
            isMusicFile = self.__checkIfMusicFile(path + file)

            if isMusicFile:
                    self.__tracks.append(file)

        self.__totalTracks = len(self.__tracks)
        
        random.shuffle(self.__tracks)
        pygame.mixer.music.set_endevent(BackgroundMusic.TRACK_END)

    def __checkIfMusicFile(self, musicFile):
        isFile = os.path.isfile(musicFile)
        
        if isFile:
            isMusicFile = sndhdr.what(musicFile)
            if isMusicFile is not None:
                return True

        return False

    def __loadMusic(self, path): 
        file = os.path.abspath(path + self.__tracks[self.__currentTrack])
            
        try:
            pygame.mixer.music.load(file)
        except pygame.error as errorMessage:
            logging.exception(errorMessage)
            raise

    def isMusicPlaying(self):
        return pygame.mixer.music.get_busy()

    def playMusic(self, path):
        if self.__totalTracks == 0 or self.isMusicPlaying():
            return

        self.__loadMusic(path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        self.__currentTrack += 1

    def playNextMusic(self, path):
        if self.__currentTrack == self.__totalTracks:
            self.__currentTrack = 0

        self.playMusic(path)

    def stopMusic(self):
        if self.isMusicPlaying():
            pygame.mixer.music.stop()
            
            

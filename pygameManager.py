from pygame import *
import pygame
#Pygame Screen
WIDTH_, HEIGHT_ = (1920/2).__round__(), (1920/2).__round__()
SCREEN_ = pygame.display.set_mode((WIDTH_, HEIGHT_))
pygame.display.set_caption("3D Render Engine")

#Pygame Clock
CLOCK_ = pygame.time.Clock()
WIDTH, HEIGHT, SCREEN, CLOCK = WIDTH_, HEIGHT_, SCREEN_, CLOCK_

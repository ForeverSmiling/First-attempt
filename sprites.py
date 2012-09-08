__author__ = 'fs'

import os,sys
import pygame
from pygame.locals import *
from helpers import *

class MainCloud(pygame.sprite.Sprite):
  def __init__(self,rect=None):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_image('cloud10x10.gif',-1)
    self.x_dist = 10
    self.y_dist = 10
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    if rect:
      self.rect = rect
  def update(self, w,h):
    """
    reacts on mouse moving
    """
    if pygame.mouse.get_focused():
      mouse_pos = pygame.mouse.get_pos()
      real_pos = (int(mouse_pos[0] - mouse_pos[0] % 10), int(mouse_pos[1]- mouse_pos[1] % 10))
      self.rect.topleft = real_pos
  def move(self, keys):
    """
    reacts on arrows press
    """
    xMove = 0;
    yMove = 0;
    if (keys[K_RIGHT]):
      xMove = self.x_dist
    elif (keys[K_LEFT]):
      xMove = -self.x_dist
    if (keys[K_UP]):
      yMove = -self.y_dist
    elif (keys[K_DOWN]):
      yMove = self.y_dist
    newpos = self.rect.move((xMove,yMove))
    if self.area.contains(newpos):
      self.rect = newpos

class SubCloud(MainCloud):
  def __init__(self, rect=None):
    MainCloud.__init__(self)
    self.image, self.rect = load_image('cloud_black.gif',-1)
    if rect:
      self.rect = rect
    self.isAlive = False
  def move(self):
    return

class Grass(pygame.sprite.Sprite):
  def __init__(self,rect=None):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_image('grass.gif')
    if rect:
      self.rect = rect
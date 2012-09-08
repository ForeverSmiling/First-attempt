__author__ = 'fs'

import os,sys
import pygame
from pygame.locals import *
from sprites import *

class MainGame:
  def __init__(self, width=640, height=480):
    pygame.init();
    pygame.key.set_repeat(1*1, 1*125)
    pygame.display.set_caption('The Game of Life')
    self.width = width
    self.height = height
    self.numOfCloudsHorizontal = int(self.width//10)
    self.numOfCloudsVertical = int(self.height//10)
    self.screen = pygame.display.set_mode((self.width, self.height))
    #pygame.mouse.set_visible(0)
    self.array_of_black_clouds = {}
    for line in xrange(self.numOfCloudsHorizontal):
      for index in xrange(self.numOfCloudsVertical):
        pos = pygame.Rect(line*10,index*10,10,10)
        self.array_of_black_clouds[self._rect_to_string(pos)] = SubCloud(pos)
    self.isPlayMode = False
    self.population = 0
    self.maxAlive = 0
    self.round = 1

  def _changePlayMode(self):
    self.isPlayMode = not self.isPlayMode
    self.population = 0
    if not self.isPlayMode:
      print 'Max alive clouds in round {0}: {1}'.format(self.round,self.maxAlive)
      self.round += 1
    self.maxAlive = 0
  def _rect_to_string(self,rect):
    return str((rect.left,rect.top))
  def _get_black_clouds_in_rect(self, rect):
    return filter(lambda x: x.rect == rect,self.black_clouds_sprites)
  def _get_possible_neighbors(self,rect):
    """
    return all possible neighbors keys as a list
    """
    rl,rt = rect.left,rect.top
    all_left_n = [str((rl-10,rt-10)),str((rl-10,rt)),str((rl-10,rt+10))]
    all_right_n = [str((rl+10,rt-10)),str((rl+10,rt)),str((rl+10,rt+10))]
    top_n = [str((rl,rt-10))]
    bottom_n = [str((rl,rt+10))]
    return all_left_n+all_right_n+top_n+bottom_n
  def _recalc_sub_clouds(self):
    """
    recalculate all black clouds states
    """
    clouds_must_die = []
    clouds_alive = []
    dead_clouds_checked = []
    all_alive_clouds = filter(lambda x: x[1].isAlive, self.array_of_black_clouds.items())
    all_dead_clouds = filter(lambda x: not x[1].isAlive, self.array_of_black_clouds.items())
    alive_count = len(all_alive_clouds)
    if alive_count > self.maxAlive: self.maxAlive = alive_count
    print 'Population:', self.population, 'Alive:',alive_count, 'Dead:', len(all_dead_clouds)
    for cloud in all_alive_clouds:
      possible_neighbors = self._get_possible_neighbors(cloud[1].rect)
      neighbors = filter(lambda x: x[0] in possible_neighbors,all_alive_clouds + all_dead_clouds)
      if neighbors:
        alive_num = len([n for n in neighbors if n[1].isAlive])
        if alive_num < 2 or alive_num> 3:
          if cloud not in clouds_must_die:
            clouds_must_die += [cloud[1]]
        dead_neighbors = filter(lambda x: x[0] not in dead_clouds_checked and not x[1].isAlive,neighbors)
        for neighbor in dead_neighbors:
          possible_neighbors = self._get_possible_neighbors(neighbor[1].rect)
          alive_neighbors = filter(lambda x: x[0] in possible_neighbors,all_alive_clouds)
          if len(alive_neighbors) == 3:
            if neighbor[1] not in clouds_alive:
              clouds_alive += [neighbor[1]]
          dead_clouds_checked += [neighbor[0]]
    if not clouds_alive and not clouds_must_die:
      self._changePlayMode()
      return
    for cloud in clouds_must_die:
      cloud.isAlive = False
    for cloud in clouds_alive:
      cloud.isAlive = True

  def _draw_sprites(self):
    """
    redraw all sprites and flip pygame.display
    """
    self.grass_sprites.draw(self.screen)
    self.black_clouds_sprites.draw(self.screen)
    if not self.isPlayMode:
      self.cloud_sprites.update(self.width, self.height)
      self.cloud_sprites.draw(self.screen)
    pygame.display.flip()

  def _add_black_cloud(self):
    """
    add black cloud to white cloud position
    """
    current_SubCloud = self.array_of_black_clouds[self._rect_to_string(self.mainCloud.rect)]
    current_SubCloud.isAlive = not current_SubCloud.isAlive
    black_clouds_in_rect = self._get_black_clouds_in_rect(current_SubCloud.rect)
    if black_clouds_in_rect:
      self.black_clouds_sprites.remove(black_clouds_in_rect)
    else:
      self.black_clouds_sprites.add(current_SubCloud)

  def MainLoop(self):
    """
    all main work is doing here
    """
    self.LoadSprites()
    self.clock = pygame.time.Clock()
    while True:
      if self.isPlayMode:
        self.clock.tick(8)
      else:
        self.clock.tick(60)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        elif event.type == pygame.KEYDOWN or (pygame.mouse.get_focused() and event.type == pygame.MOUSEBUTTONDOWN):
          if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            self._changePlayMode()
            if self.isPlayMode:
              self._draw_sprites()
          elif not self.isPlayMode:
            pressed_buttons = pygame.key.get_pressed()
            if (event.type == pygame.KEYDOWN and pressed_buttons[K_SPACE]) or event.type == pygame.MOUSEBUTTONDOWN:
              self._add_black_cloud()
            self.mainCloud.move(pressed_buttons)
      if self.isPlayMode:
        self.population += 1
        self._recalc_sub_clouds()
        self.black_clouds_sprites.remove(self.array_of_black_clouds.values())
        self.black_clouds_sprites.add(filter(lambda x: x.isAlive,self.array_of_black_clouds.values()))
      self._draw_sprites()

  def LoadSprites(self):
    """
    fill screen with grass, add white cloud and prepares group for black cloud sprites
    """
    self.mainCloud = MainCloud()
    self.cloud_sprites = pygame.sprite.GroupSingle(self.mainCloud)
    self.grass_sprites = pygame.sprite.Group()
    for x in range(self.numOfCloudsHorizontal):
      for y in range(self.numOfCloudsVertical):
        self.grass_sprites.add(Grass(pygame.Rect(x*10,y*10,10,10))) # rect(left,top,w,h)
    self.black_clouds_sprites = pygame.sprite.Group()

if __name__ == "__main__":
  MainWindow = MainGame()
  MainWindow.MainLoop()
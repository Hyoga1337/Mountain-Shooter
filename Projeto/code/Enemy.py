import random
import pygame.key

from Const import ENTITY_SHOT_DELAY, ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH
from EnemyShot import EnemyShot
from Entity import Entity

class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.goingDown = True

    def move(self, ):
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.name == "Enemy3":
            if self.goingDown:
                self.rect.centery += ENTITY_SPEED[self.name] * 2
                if self.rect.bottom >= WIN_HEIGHT:
                    self.goingDown = False 
            if not self.goingDown:
                self.rect.centery -= ENTITY_SPEED[self.name]
                if self.rect.top <= 0:
                    self.goingDown = True

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        

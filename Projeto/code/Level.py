import sys
import random

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Const import (C_CYAN, C_GREEN, C_WHITE, 
                    EVENT_ENEMY, EVENT_TIMEOUT, 
                    MENU_OPTION, 
                    SPAWN_TIME, 
                    TIMEOUT_LEVEL, TIMEOUT_STEP, 
                    WIN_HEIGHT)

from Enemy import Enemy
from Entity import Entity
from EntityFactory import EntityFactory
from EntityMediator import EntityMediator
from Player import Player

class Level:
    current_level = 1
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL # 20 segundos
        self.window = window
        self.name = name
        if self.name == 'Level3':
            self.timeout = TIMEOUT_LEVEL * 2 # 40 segundos
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        player1 = EntityFactory.get_entity('Player1')
        player1.score = player_score[0]
        self.entity_list.append(player1)
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player2 = EntityFactory.get_entity('Player2')
            player2.score = player_score[1]
            self.entity_list.append(player2)
            player1.rect.centery -= 20 # Inicia o Jogador1 para cima do Jogador2 nos modos 2P
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)     # 4s
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP) # 100 ms

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)
                if ent.name == 'Player1':
                    self.level_text(14, f'Player1 - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
                if ent.name == 'Player2':
                    self.level_text(14, f'Player2 - Health: {ent.health} | Score: {ent.score}', C_CYAN, (10, 45))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    if self.name != "Level3":
                        choice = random.choice(('Enemy1', 'Enemy2'))
                        self.entity_list.append(EntityFactory.get_entity(choice))
                    else:
                        self.entity_list.append(EntityFactory.get_entity('Enemy3'))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] += ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] += ent.score
                        return True

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True
                    
                if not found_player:
                    Level.current_level = 4
                    return False
                    
            # Texto impresso
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s', C_WHITE, (10, 5)) # Tempo da fase
            self.level_text(14, f'fps: {clock.get_fps() :.0f}', C_WHITE, (10, WIN_HEIGHT - 35))          # FPS
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))   # Contador de entidades
            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucidasans", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)


    



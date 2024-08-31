from Entity import Entity
from Const import ENTITY_SPEED, WIN_WIDTH

class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        pass

    def move(self, ):
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH

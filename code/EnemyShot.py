from code.Const import ENTITY_SPEED, WIN_HEIGHT
from code.Entity import Entity


class EnemyShot(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # O tiro inimigo nasce indo apenas para a esquerda
        self.speed_x = -ENTITY_SPEED[self.name]
        self.speed_y = 0

    def move(self):
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y

        # Recochetear nas bordas superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= WIN_HEIGHT:
            self.speed_y *= -1
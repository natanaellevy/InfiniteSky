from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH
from code.Entity import Entity


class PlayerShot(Entity):

    def __init__(self, name: str, position: tuple, speed_x: float, speed_y: float):
        super().__init__(name, position)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y

        # Quicar no teto e no chão
        if self.rect.top <= 0 or self.rect.bottom >= WIN_HEIGHT:
            self.speed_y *= -1

        # Quicar na parede direita (volta para a esquerda)
        if self.rect.right >= WIN_WIDTH:
            self.speed_x *= -1
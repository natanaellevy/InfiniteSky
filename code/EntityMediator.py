from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot
from code.Const import WIN_WIDTH, ENTITY_SPEED


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity, entity_list: list[Entity]):  # <-- Adicionamos a lista aqui
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0

        # Se QUALQUER tiro sair pela esquerda da tela, o jogador toma dano
        if isinstance(ent, (EnemyShot, PlayerShot)):
            if ent.rect.right <= 0:
                ent.health = 0
                # Procura os players na tela e aplica o dano da bala neles
                for entity in entity_list:
                    if isinstance(entity, Player):
                        entity.health -= ent.damage

    @staticmethod
    def __verify_collision_entity(ent1, ent2, entity_list):  # <-- Atenção ao novo parâmetro
        valid_interaction = False
        is_deflection = False

        # Interações de dano normal (Inimigo vs Tiro rebatido)
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True

        # Nova mecânica: Colisão para rebater
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            is_deflection = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            is_deflection = True

        if valid_interaction or is_deflection:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):

                if is_deflection:
                    player = ent1 if isinstance(ent1, Player) else ent2
                    shot = ent2 if isinstance(ent2, EnemyShot) else ent1

                    # 1. Mata o tiro inimigo original
                    shot.health = 0

                    # 2. Calcula o ângulo do rebote (Pong) baseado em onde pegou na nave
                    offset_y = shot.rect.centery - player.rect.centery
                    speed_y = offset_y // 4  # Ajuste esse divisor para aumentar/diminuir o ângulo
                    speed_x = ENTITY_SPEED[f'{player.name}Shot']

                    # 3. Cria o tiro aliado rebatido na mesma posição
                    deflected_shot = PlayerShot(f'{player.name}Shot', (shot.rect.centerx, shot.rect.centery), speed_x,
                                                speed_y)
                    entity_list.append(deflected_shot)

                else:
                    # Lógica de dano original (Aplica o dano no inimigo e destrói o tiro rebatido)
                    ent1.health -= ent2.damage
                    ent2.health -= ent1.damage
                    ent1.last_dmg = ent2.name
                    ent2.last_dmg = ent1.name

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            # Passamos a entity_list para a verificação da janela
            EntityMediator.__verify_collision_window(entity1, entity_list)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2, entity_list)

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)
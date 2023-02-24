import pygame as pg
from random import randrange
import time
import datetime

pg.font.init()
WINDOW = 400
TILE_SIZE = 20
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE //2, TILE_SIZE)

pg.display.set_caption('oskour') 
clock = pg.time.Clock()
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 0, TILE_SIZE - 0])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
now = datetime.datetime.now()
date_str = now.strftime("%Y-%m-%d %H:%M:%S")


# Ouverture du fichier scores.txt en mode "append"
with open("scores.txt", "a") as f:
    f.write("\n")  # Écriture d'une nouvelle ligne vide pour séparer les scores

score = 0

# Afficher le menu
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            if event.key == pg.K_SPACE:
                # Réinitialiser le jeu et commencer une nouvelle partie
                snake.center, food.center = get_random_position(), get_random_position()
                length, snake_dir, score = 1, (0, 0), 0
                segments = [snake.copy()]
                # Sortir de la boucle de menu et commencer le jeu
                break
    else:
        # Afficher le message "Press space to play"
        screen.fill('white')
        font = pg.font.SysFont('arial', 20)
        message_surface = font.render('appuyer espace pour jouer', True, 'black')
        screen.blit(message_surface, (WINDOW // 2 - message_surface.get_width() // 2, WINDOW // 2))
        message_surface = font.render('appuyer up pour afficher les scores une fois mort', True, 'black')
        screen.blit(message_surface, (WINDOW // 2 - message_surface.get_width() // 2, WINDOW // 1.8))
        pg.display.flip()
        clock.tick(60)
        continue
    break


game_over = False
while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirs[pg.K_UP]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
            if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
    screen.fill('white')
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            snake.center, food.center = get_random_position(), get_random_position()
            length, snake_dir = 1, (0, 0)
            segments = [snake.copy()]
            with open("scores.txt", "a") as f:
                f.write(f"{date_str} - Score: {score}\n")
            
            # Reinitialisation du jeu
            snake.center, food.center = get_random_position(), get_random_position()
            length, snake_dir, score = 1, (0, 0), 0
            segments = [snake.copy()]

            # Attendre que le joueur appuie sur la touche Espace pour recommencer le jeu
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            exit()
                        if event.key == pg.K_SPACE:
                            # Réinitialiser le jeu et commencer une nouvelle partie
                            snake.center, food.center = get_random_position(), get_random_position()
                            length, snake_dir, score = 1, (0, 0), 0
                            segments = [snake.copy()]
                            # Sortir de la boucle de menu et commencer le jeu
                            break
                        # Lire le contenu du fichier scores.txt
                    with open("scores.txt", "r") as f:
                        scores = f.readlines()
                    # Afficher les scores à l'écran
                    screen.fill('white')
                    font = pg.font.SysFont('arial', 20)
                    for i, score in enumerate(scores):
                        score_surface = font.render(score.strip(), True, 'black')
                        screen.blit(score_surface, (WINDOW // 2 - score_surface.get_width() // 2, WINDOW // 2 + i*25))
                    message_surface = font.render('appuyer espace pour rejouer', True, 'black')
                    screen.blit(message_surface, (WINDOW // 2 - message_surface.get_width() // 2, WINDOW // 2 - 50))
                    pg.display.update

                else:
                    pg.display.flip()
                    clock.tick(60)
                    continue
                break
        
    if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            score += 1

    pg.draw.rect(screen, 'red', food)

    [pg.draw.rect(screen, 'black', segment) for segment in segments]

    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]
        
    pg.display.flip()
    clock.tick(60)

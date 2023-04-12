import pygame
import random
import math
import sys
import os

# inicializar juego
pygame.init()

# Establece tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Funcion para obtener ruta de los recursos

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


# Cargar imagenes
asset_background = resource_path('assets/imagenes/background.jpeg')
background = pygame.image.load(asset_background)
asset_icon = resource_path('assets/imagenes/icono.png')
icon = pygame.image.load(asset_icon)
asset_player = resource_path('assets/imagenes/jugador.png')
player = pygame.image.load(asset_player)
asset_bullet = resource_path('assets/imagenes/bala.png')
bullet = pygame.image.load(asset_bullet)
asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

asset_mode=resource_path('assets/imagenes/engranaje.png')
# Cargar imagen de engranaje
engranaje_img = pygame.image.load(asset_mode).convert_alpha()
BLANCO = (255, 255, 255)

# Definimos las dimensiones del botón y su posición
button_width = 50
button_height = 50
button_x = 750
button_y = 10

# Creamos el rectángulo que define el área del botón
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
pygame.draw.rect(screen, BLANCO, [button_x, button_y, button_width, button_width])


# Actualizar pantalla
pygame.display.flip()

#########
asset_bullet_enemy = resource_path('assets/imagenes/bala_enemigo.png')
bullet_enemy = pygame.image.load(asset_bullet_enemy)

asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

# titulo de la ventana
pygame.display.set_caption("Space HERO")
pygame.display.set_icon(icon)

pygame.mixer.music.play(-1)
# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock

# Posicion inicial jugador
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

# lista almacenamiento posicion enemigos
enem_img = []
enemX = []
enemY = []
enemX_change = []
enemY_change = []

n_of_enem = 5

# inicializacion de variable
for i in range(n_of_enem):
    # carga de enemigos
    enem_normal = resource_path('assets/imagenes/enemigo.png')
    enem_img.append(pygame.image.load(enem_normal))

    # se les asigan posicion aleatoria
    enemX.append(random.randint(0, 736))
    enemY.append(random.randint(0, 150))
    # velocidad del movimiento en X y Y

    enemX_change.append(5)
    enemY_change.append(20)

    # inicializacion de variables para la bala
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "Ready"


    #inicializavion variables para la bala del enemigo
    bulletX_enemy=[]
    bulletY_enemy=[]
    bulletenemX_change = 0
    bulletenemY_change = 10
    bullet_enemy_state = "Ready"

    for enX in enemX_change:
        bulletX_enemy.append(enX)
    for enY in enemY_change:
        bulletY_enemy.append(enY)


    # inicializacion de puntuacion
    score = 0


    # mostrar puntuacion en pantalla
    def show_score():
        score_value = font.render("SCORE" +" " + str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))


    # dibujar player en pantalla
    def show_player(x, y):
        screen.blit(player, (x, y))


    # dibujar enemigo en la pantalla
    def show_enemy(x, y, i):
        screen.blit(enem_img[i], (x, y))

    def show_button(x,y,imagen):
        screen.blit(imagen, (x, y))
    def fire_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bullet, (x + 16, y + 10))

    def fire_bullet_enemy(x, y):
        global bullet_enemy_state
        bullet_enemy_state = "fire"
        screen.blit(bullet_enemy, (x - 16, y - 10))

    def check_button_clicked(button_rect):
        #Detecta si el botón fue presionado y retorna un booleano
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
            return True
        else:
            return False

    # comparar si hay colision entre enemigo y la bala

    def isCollision(enemX, enemY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemX - bulletX, 2)) + (math.pow(enemY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False
    def isCollisionPlayer(playerX, playerY, bulletX_enemy, bulletY_enemy):
        distance = math.sqrt((math.pow(playerX - bulletX_enemy, 2)) + (math.pow(playerY - bulletY_enemy, 2)))
        if distance < 27:
            return True
        else:
            return False

    # Mostrar game over en pantalla

    def show_game_over():
        over_text = over_font.render('GAME OVER', True, (255, 255, 255))
        text_rect = over_text.get_rect(
            center=(int(screen_width / 2), int(screen_height / 2))
        )
        screen.blit(over_text, text_rect)


    # funcion principal

    def gameloop():
        global score
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global Collision
        global bullet_state
        global bulletY_enemy
        global bulletX_enemy
        global bullet_enemy_state


        in_game = True
        level_mode_easy=True
        while in_game:
            if level_mode_easy:
                # Manejo eventos, actualiza y renderiza
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))
                show_button(button_x, button_y, engranaje_img)
                #screen.blit(engranaje_img, (button_x, button_y))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        in_game = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        # manejo movimiento del jugador
                        if event.key == pygame.K_LEFT:
                            playerX_change = -5
                        if event.key == pygame.K_RIGHT:
                            playerX_change = 5
                        if event.key == pygame.K_SPACE:
                            if bullet_state == "Ready":
                                bulletX = playerX
                                fire_bullet(bulletX, bulletY)
                        if event.type == pygame.KEYUP:
                            playerX_change = 0
                # Actualizando la posicion del jugador
                playerX += playerX_change
                if playerX <= 0:
                    playerX = 0
                elif playerX >= 736:
                    playerX = 736

                # Bucle para cada enemigo

                for i in range(n_of_enem):
                    if enemY[i] > 440:
                        for j in range(n_of_enem):
                            enemY[j] = 2000
                        show_game_over()
                    enemX[i] += enemX_change[i]
                    if enemX[i] <= 0:
                        enemX_change[i] = 5
                        enemY[i] += enemY_change[i]
                    elif enemX[i] >= 736:
                        enemX_change[i] = -5
                        enemY[i] += enemY_change[i]

                    # Comprobacion de colision entre enemigo y bala
                    collision = isCollision(enemX[i], enemY[i], bulletX, bulletY)

                    if collision:
                        bulletY = 454
                        bullet_state = "Ready"
                        score += 1
                        enemX[i] = random.randint(0, 736)
                        enemY[i] = random.randint(0, 150)


                    show_enemy(enemX[i], enemY[i], i)
                if bulletY <= 0:
                    bulletY = 454
                    bullet_state = "Ready"
                if bullet_state == "fire":
                    fire_bullet(bulletX, bulletY)
                    bulletY -= bulletY_change
                show_player(playerX, playerY)
                show_score()
                pygame.display.update()
                #clock.tick(60)

                if check_button_clicked(button_rect):
                    level_mode_easy=False

            elif level_mode_easy==False:
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))
                show_button(button_x, button_y, engranaje_img)
                # screen.blit(engranaje_img, (button_x, button_y))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        in_game = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        # manejo movimiento del jugador
                        if event.key == pygame.K_LEFT:
                            playerX_change = -5
                        if event.key == pygame.K_RIGHT:
                            playerX_change = 5
                        if event.key == pygame.K_SPACE:
                            if bullet_state == "Ready":
                                bulletX = playerX
                                fire_bullet(bulletX, bulletY)
                        if event.type == pygame.KEYUP:
                            playerX_change = 0
                # Actualizando la posicion del jugador
                playerX += playerX_change
                if playerX <= 0:
                    playerX = 0
                elif playerX >= 736:
                    playerX = 736

                # Bucle para cada enemigo

                for i in range(n_of_enem):
                    if enemY[i] > 440:
                        for j in range(n_of_enem):
                            enemY[j] = 2000
                        show_game_over()
                    enemX[i] += enemX_change[i]
                    if enemX[i] <= 0:
                        enemX_change[i] = 5
                        enemY[i] += enemY_change[i]
                    elif enemX[i] >= 736:
                        enemX_change[i] = -5
                        enemY[i] += enemY_change[i]

                    # Comprobacion de colision entre enemigo y bala
                    collision = isCollision(enemX[i], enemY[i], bulletX, bulletY)
                    if collision:
                        bulletY = 454
                        bullet_state = "Ready"
                        score += 1
                        enemX[i] = random.randint(0, 736)
                        enemY[i] = random.randint(0, 150)

                    if bulletY_enemy[i] <= 454:
                        bulletY = 0
                        bullet_enemy_state = "Ready"
                    if bullet_enemy_state == "fire":
                        fire_bullet_enemy(enemX[i],enemY[i])
                        bulletY_enemy -= bulletenemY_change
                    show_enemy(enemX[i], enemY[i], i)

                if bulletY <= 0:
                    bulletY = 454
                    bullet_state = "Ready"
                if bullet_state == "fire":
                    fire_bullet(bulletX, bulletY)
                    bulletY -= bulletY_change
                show_player(playerX, playerY)
                #collision_player = isCollisionPlayer(playerX,playerY)
                show_score()
                pygame.display.update()
                # clock.tick(60)

                if check_button_clicked(button_rect):
                    level_mode_easy = True

gameloop()

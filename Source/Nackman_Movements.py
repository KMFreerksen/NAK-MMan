import pygame

pygame.init()

WIDTH=800
HEIGHT=800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps=30

"""Player Image"""
player_img=[]
for i in range(1,4):
    player_img.append(pygame.transform.scale(pygame.image.load(f'packman_imgaes/{i}.png'), (50, 50)))

player_x = 250
player_y = 250

direction = 0
packman_img_cycle = 0
player_speed = 2

def draw_player():
    #direction definition: 0: right, 1: up, 2: left, 3: down
    if direction == 0:
        screen.blit(player_img[packman_img_cycle // 4], [player_x, player_y])
    if direction == 1:
        screen.blit(pygame.transform.rotate(player_img[packman_img_cycle // 4], 90), [player_x, player_y])
    if direction == 2:
        screen.blit(pygame.transform.flip(player_img[packman_img_cycle // 4], True, False), [player_x, player_y])
    if direction == 3:
        screen.blit(pygame.transform.rotate(player_img[packman_img_cycle // 4], -90), [player_x, player_y])


def move_player(play_x, play_y):
# moving plyer to right, up, left and down
    if direction == 0:
        play_x += player_speed
    elif direction == 1:
        play_y -= player_speed
    if direction == 2:
        play_x -= player_speed
    elif direction == 3 :
        play_y += player_speed
    return play_x, play_y

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    if packman_img_cycle < 11:
        packman_img_cycle += 1
    else:
        packman_img_cycle = 0
    draw_player()
    player_x, player_y = move_player(player_x, player_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_UP:
                direction = 1
            if event.key == pygame.K_LEFT:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3

    pygame.display.flip()
pygame.quit()

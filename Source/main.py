import pygame
import sys
import random
import math
import os
from enum import Enum
from board import boards, boards3
from sprite import *
from sounds import *

pygame.init()
vec = pygame.math.Vector2
TILE_SIZE = 25
SCREEN_WIDTH, SCREEN_HEIGHT = (TILE_SIZE * 30), (TILE_SIZE * 34 + 80)
PACMAN_SIZE = 30
DOT_SIZE = 4
TILE_HEIGHT = TILE_SIZE
TILE_WIDTH = TILE_SIZE
POWER_DOT_SIZE = 8
BLACK = (0, 0, 0)
BLUE = (25, 25, 166)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PI = math.pi
FRAME_RATE = 30
#PACKMAN_IMG_CYCLE = 0
PLAYER_SPEED = 10 * TILE_SIZE
GHOST_IMGS = ['Nick.jpg', 'Felipe.jpg', 'jason.jpg', 'dawn.jpg']
MAX_LEVEL = 2

CHANGE_DIRECTION_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_DIRECTION_EVENT, 1000)

HIGH_SCORE_FILE = "high_score.txt"
SCORE_FONT = pygame.font.Font(None, 36)


class State(Enum):
    START = 1
    GAME = 2
    GAMEOVER = 3
    PREGAME = 4
    WIN = 5


class Ghost(pygame.sprite.Sprite):

    def __init__(self, x, y, color):
        super().__init__()
        self.image =pygame.transform.scale(pygame.image.load(f'images/ghost_{color}'),(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.new_rect = self.rect
        self.dead_timer = 0
        self.previous_move=['ss','ss']
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, tiles, ghosts):
        flag = 1
        while flag:
            self.new_rect = self.rect.copy()
            if self.direction == 'up':
                self.new_rect.move_ip(0, -5)
            elif self.direction == 'down':
                self.new_rect.move_ip(0, 5)
            elif self.direction == 'left':
                self.new_rect.move_ip(-5, 0)
            elif self.direction == 'right':
                self.new_rect.move_ip(5, 0)
            if (not any(tile.rect.colliderect(self.new_rect) for tile in tiles)) and self.direction != self.previous_move[0]:
                self.rect = self.new_rect

                flag=0
                if self.direction != self.previous_move[1]:
                    self.previous_move[0]=self.previous_move[1]
                    self.previous_move[1]=self.direction
            else:
                self.direction = random.choice(['up', 'down', 'left', 'right'])

    def out(self, screen):
        self.clock=pygame.time.Clock()
        
    def die (self):
        self.x=330
        self.y=270
        self.dead_timer=5*FRAME_RATE
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y) * TILE_SIZE
        self.player_img = []
        self.packman_img_cycle = 0
        for i in range(1, 4):
            self.player_img.append(pygame.transform.scale(pygame.image.load(f'images/{i}.png'), (25, 25)))
        self.image = self.player_img[0]
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.score = 0
        self.lives = 3
        # added for movement
        self.move_buffer = 20
        self.vel = vec(0, 0)
        self.dirvec = vec(0, 0)
        self.last_pos = self.pos
        self.next_pos = self.pos
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.between_tiles = False
        self.starting_pos = vec(x, y) * TILE_SIZE

    def update(self, dt, walls):
        self.handle_keys()
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

        if self.pos != self.next_pos:
            delta = self.next_pos - self.pos
            if delta.length() > (self.dirvec * PLAYER_SPEED * dt).length():
                self.pos += self.dirvec * PLAYER_SPEED * dt
            else:
                self.pos = self.next_pos
                self.dirvec = vec(0, 0)
                self.between_tiles = False
        self.rect.topleft = self.pos
        if pygame.sprite.spritecollide(self, walls, False):
            self.pos = self.last_pos
            self.next_pos = self.last_pos
            self.dirvec = vec(0, 0)
            self.between_tiles = False
        if self.rect.topleft[0] <= 0:
            self.pos = vec(30, self.rect.centery // TILE_SIZE) * TILE_SIZE
            self.dirvec = vec(0, 0)
            self.between_tiles = False
        if self.rect.topleft[0] >= SCREEN_WIDTH:
            self.pos = vec(1, self.rect.centery // TILE_SIZE) * TILE_SIZE
            self.dirvec = vec(0, 0)
            self.between_tiles = False
        self.rect.topleft = self.pos

    def handle_keys(self):
        key = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if now - self.last_update > self.move_buffer:
            self.last_update = now

            new_dir_vec = vec(0, 0)
            if self.dirvec.y == 0:
                if key[pygame.K_LEFT]:  # left key
                    new_dir_vec = vec(-1, 0)
                    self.image = pygame.transform.flip(self.player_img[self.packman_img_cycle // 4], True, False)
                elif key[pygame.K_RIGHT]:  # right key
                    new_dir_vec = vec(1, 0)
                    self.image = self.player_img[self.packman_img_cycle // 4]
            if self.dirvec.x == 0:
                if key[pygame.K_DOWN]:  # down key
                    new_dir_vec = vec(0, 1)
                    self.image = pygame.transform.rotate(self.player_img[self.packman_img_cycle // 4], -90)
                elif key[pygame.K_UP]:  # up key
                    new_dir_vec = vec(0, -1)
                    self.image = pygame.transform.rotate(self.player_img[self.packman_img_cycle // 4], 90)

            if new_dir_vec != vec(0, 0):
                self.dirvec = new_dir_vec
                self.between_tiles = True
                current_index = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
                self.last_pos = vec(current_index) * TILE_SIZE
                self.next_pos = self.last_pos + self.dirvec * TILE_SIZE

            if self.packman_img_cycle < 11:
                self.packman_img_cycle += 1
            else:
                self.packman_img_cycle = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))


class Dot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, DOT_SIZE, DOT_SIZE)
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, ((self.x + DOT_SIZE/2), (self.y + DOT_SIZE/2)), DOT_SIZE)

class Power_Dot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, POWER_DOT_SIZE, POWER_DOT_SIZE)
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, ((self.x + POWER_DOT_SIZE/2), (self.y + POWER_DOT_SIZE/2)), POWER_DOT_SIZE)

class Tile:
    def __init__(self, x, y, w, h, is_wall=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_wall = is_wall

    def draw(self, screen):
        color = (50, 150, 50) if self.is_wall else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect)


class GameController:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.clock = pygame.time.Clock()
        self.running = True
        self.start_level = True
        self.state = State.START
        self.board = boards
        self.level = 1
        self.player = Player(100, 120)
        self.dots = []
        self.power_dots = []
        self.ghosts = pygame.sprite.Group()
        self.walls = []
        self.sounds = Sounds()
        self.ghost_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.start_pos = [0, 0]
        self.score = 0
        self.lives = 3

    def draw_start_menu(self):
        if self.state == State.START:
            self.screen.fill(BLACK)
            title_font = pygame.font.Font('CrackMan.TTF', 75)
            title = title_font.render('Nak-Man', True, YELLOW)
            button_font = pygame.font.SysFont('impact', 32)
            start_button = button_font.render('Press Space to Start', True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/4))
            self.screen.blit(start_button, (
                SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))
            pygame.display.flip()

    def draw_game_over_screen(self):
        if self.state == State.GAMEOVER:
            title_font = pygame.font.SysFont('impact', 48)
            title = title_font.render('Game Over', True, YELLOW, BLACK)
            button_font = pygame.font.SysFont('impact', 32)
            restart = button_font.render('P - Play Again', True, YELLOW, BLACK)
            quit_button = button_font.render('Q - Quit', True, YELLOW, BLACK)
            self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
            self.screen.blit(restart, (
                SCREEN_WIDTH / 2 - restart.get_width() / 2, SCREEN_HEIGHT / 2 + restart.get_height()))
            self.screen.blit(quit_button, (
                SCREEN_WIDTH / 2 - quit_button.get_width() / 2, SCREEN_HEIGHT / 2 + restart.get_height() +
                quit_button.get_height()))
            pygame.display.flip()

    def draw_win_screen(self):
        title_font = pygame.font.SysFont('impact', 48)
        title = title_font.render('You Win!', True, YELLOW, BLACK)
        button_font = pygame.font.SysFont('impact', 32)
        restart = button_font.render('P - Play Again', True, YELLOW, BLACK)
        quit_button = button_font.render('Q - Quit', True, YELLOW, BLACK)
        self.screen.blit(title,
                         (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height() / 2))
        self.screen.blit(restart, (
            SCREEN_WIDTH / 2 - restart.get_width() / 2, SCREEN_HEIGHT / 2 + restart.get_height()))
        self.screen.blit(quit_button, (
            SCREEN_WIDTH / 2 - quit_button.get_width() / 2, SCREEN_HEIGHT / 2 + restart.get_height() +
            quit_button.get_height()))
        pygame.display.flip()

    def add_dot(self, dot):
        self.dots.append(dot)

    def add_power_dot(self, dot):
        self.power_dots.append(dot)

    def add_wall(self, wall):
        self.walls.append(wall)

    def create_map_objects(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 3:
                    self.add_wall(Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT), 3, TILE_HEIGHT))
                if self.board[i][j] == 4:
                    self.add_wall(Tile((j * TILE_WIDTH), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5), TILE_WIDTH, 3))
                if self.board[i][j] == 5:
                    self.add_wall(
                        Tile((j * TILE_WIDTH - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5), TILE_WIDTH * 0.6,
                             3))
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3,
                             TILE_HEIGHT * 0.7))
                if self.board[i][j] == 6:
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3,
                             TILE_HEIGHT * 0.5))
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5),
                             TILE_HEIGHT * 0.7, 3))
                if self.board[i][j] == 7:
                    pygame.draw.arc(self.screen, BLUE,
                                    [(j * TILE_HEIGHT + (TILE_HEIGHT * 0.5)), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)),
                                     TILE_WIDTH, TILE_HEIGHT], PI, 3 * PI / 2, 3)
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT), 3, TILE_HEIGHT * 0.6))
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5),
                             TILE_WIDTH * 0.6, 3))
                if self.board[i][j] == 8:
                    self.add_wall(
                        Tile((j * TILE_WIDTH - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5), TILE_WIDTH * 0.6,
                             3))
                    self.add_wall(Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT), 3, TILE_HEIGHT *
                                       0.6))
                if self.board[i][j] == 9:
                    pass


    def draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 3:
                    pygame.draw.line(self.screen, RED, (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT),
                                     (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT + TILE_HEIGHT), 3)
                if self.board[i][j] == 4:
                    pygame.draw.line(self.screen, RED, (j * TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)),
                                     (j * TILE_WIDTH + TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3)
                if self.board[i][j] == 5:
                    pygame.draw.arc(self.screen, RED, [(j * TILE_WIDTH - (TILE_WIDTH * 0.4) - 2), (i * TILE_HEIGHT +
                                                        (0.5 * TILE_HEIGHT)), TILE_WIDTH, TILE_HEIGHT], 0, PI / 2, 3)
                if self.board[i][j] == 6:
                    pygame.draw.arc(self.screen, RED, [(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), (i * TILE_HEIGHT +
                                                        (0.5 * TILE_HEIGHT)), TILE_WIDTH, TILE_HEIGHT], PI / 2, PI, 3)
                if self.board[i][j] == 7:
                    pygame.draw.arc(self.screen, RED,
                                    [(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)),
                                     TILE_WIDTH, TILE_HEIGHT], PI, 3 * PI / 2, 3)
                if self.board[i][j] == 8:
                    pygame.draw.arc(self.screen, RED,
                                    [(j * TILE_WIDTH - (TILE_WIDTH * 0.4) - 2), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)),
                                     TILE_WIDTH, TILE_HEIGHT], 3 * PI / 2, 2 * PI, 3)
                if self.board[i][j] == 9:
                    pygame.draw.line(self.screen, WHITE, (j * TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)),
                                     (j * TILE_WIDTH + TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3)
                # So the 'COHORT' is a different color (BLUE)
                if self.board[i][j] == 10:
                    pygame.draw.line(self.screen, BLUE, (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT),
                                 (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT + TILE_HEIGHT), 5)
                if self.board[i][j] == 11:
                    pygame.draw.line(self.screen, BLUE, (j * TILE_HEIGHT, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)),
                                 (j * TILE_WIDTH + TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 5)
                if self.board[i][j] == 12:
                    pygame.draw.arc(self.screen, BLUE, [(j * TILE_WIDTH - (TILE_WIDTH * 0.4) - 2), (i * TILE_HEIGHT +
                                                                                                (0.5 * TILE_HEIGHT)),
                                                    TILE_WIDTH, TILE_HEIGHT], 0, PI / 2, 5)
                if self.board[i][j] == 13:
                    pygame.draw.arc(self.screen, BLUE, [(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), (i * TILE_HEIGHT +
                                                                                            (0.5 * TILE_HEIGHT)),
                                                    TILE_WIDTH, TILE_HEIGHT], PI / 2, PI, 5)
                if self.board[i][j] == 14:
                    pygame.draw.arc(self.screen, BLUE,
                                [(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)),
                                 TILE_WIDTH, TILE_HEIGHT], PI, 3 * PI / 2, 5)
                if self.board[i][j] == 15:
                    pygame.draw.arc(self.screen, BLUE,
                                [(j * TILE_WIDTH - (TILE_WIDTH * 0.4) - 2), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)),
                                 TILE_WIDTH, TILE_HEIGHT], 3 * PI / 2, 2 * PI, 5)

    def restart_level(self):
        self.player.kill()
        self.player = Player(self.start_pos[0], self.start_pos[1])
        self.all_sprites.add(self.player)

    def lose_life(self):
        if self.lives == 1:
            self.state = State.GAMEOVER
        else:
            self.lives -= 1
            self.restart_level()

    def draw_lives(self):
        i = PACMAN_SIZE / 2
        for _ in range(self.lives):
            self.screen.blit(pygame.transform.scale(pygame.image.load('images/1.png'), (PACMAN_SIZE, PACMAN_SIZE)),
                             (i + PACMAN_SIZE // 2, SCREEN_HEIGHT - 1.5 * PACMAN_SIZE))
            i += PACMAN_SIZE * 2

    def create_sprite_objects(self):
        ghost_loc = []
        for row, tiles in enumerate(self.board):
            for col, tile in enumerate(tiles):
                if tile in [3, 4, 5, 6, 7, 8, 9]:
                    obstacle = Obstacle(col, row)
                    self.obstacles.add(obstacle)
                    self.all_sprites.add(obstacle)
                elif tile == 'P':
                    self.player = Player(col, row)
                    self.all_sprites.add(self.player)
                    self.start_pos[0] = col
                    self.start_pos[1] = row
                elif tile == 'G':
                    ghost_loc.append((col * TILE_SIZE, row * TILE_SIZE))
        i = 0
        for loc in ghost_loc:
            ghost = Ghost(loc[0], loc[1], GHOST_IMGS[i])
            self.ghosts.add(ghost)
            # self.all_sprites.add(ghost)
            i += 1

    def create_dots(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    self.add_dot(
                        Dot((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 2), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 2)))
                if self.board[i][j] == 2:
                    self.add_power_dot(
                        Power_Dot((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 5)))
    def main(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                high_score = int(f.read())
        else:
            high_score = 0
        pygame.mixer.init()

        flag=1
        frightened_mode=False
        
        frightened_mode_timer=0

        while self.running:

            self.player.packman_img_cycle = self.player.packman_img_cycle + 1 if self.player.packman_img_cycle < 11 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == CHANGE_DIRECTION_EVENT:
                    for ghost in self.ghosts:
                        ghost.direction = random.choice(['up', 'down', 'left', 'right'])
            
            if game.state == State.START:
                game.draw_start_menu()
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    game.state = State.PREGAME
                    play_pacman_intro()  # self.sounds.play_intro()

            if game.state == State.PREGAME:
                self.screen.blit(self.surface, (0, 0))

                if self.start_level:
                    self.create_sprite_objects()
                    #self.create_map_objects()
                    self.create_dots()
                    self.start_level = False
                self.draw_board()
                for ghoste in self.ghosts:
                    ghoste.draw(self.screen)

                for dot in self.dots:
                    dot.draw(self.screen)
                for power_dot in self.power_dots:
                    power_dot.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(FRAME_RATE)
                game.draw_lives()
                for ghost in self.ghosts:
                    for i in range(11):
                        self.screen.blit(self.surface, (0, 0))
                        self.draw_board()
                        for ghoste in self.ghosts:
                            ghoste.draw(self.screen)
                        for dot in self.dots:
                            dot.draw(self.screen)
                        for power_dot in self.power_dots:
                            power_dot.draw(self.screen)
                        ghost.rect.move_ip(0,-5)
                        pygame.display.flip()
                        self.clock.tick(FRAME_RATE)
                game.state = State.GAME

            if game.state == State.GAME:
                dt = self.clock.tick(FRAME_RATE) / 1000
                self.screen.blit(self.surface, (0, 0))

                if self.start_level:
                    if self.level == 2:
                        self.board = boards3
                    self.create_sprite_objects()
                    self.create_dots()
                    self.start_level = False

                for dot in self.dots:
                    dot.draw(self.screen)
                for power_dot in self.power_dots:
                    power_dot.draw(self.screen)

                self.player.update(dt, self.obstacles)
                for sprite in self.all_sprites:
                    self.screen.blit(sprite.image, sprite.rect)
                self.draw_board()

                for ghost in self.ghosts:
                    if ghost.dead_timer == 0:
                        ghost.update(self.obstacles, self.ghosts)

                for power_dot in self.power_dots:
                    if self.player.rect.colliderect(power_dot.rect):   
                        self.power_dots.remove(power_dot) 
                        frightened_mode_timer= 20 * FRAME_RATE
                if frightened_mode_timer > 0:
                    frightened_mode = True
                else:
                    frightened_mode = False

                for dot in self.dots:
                    if self.player.rect.colliderect(dot.rect):
                        self.dots.remove(dot)
                        self.sounds.play_pacman_eating()  # Play eating sound
                        self.score += 1  # Increase the score when a dot is eaten
                        if self.score > high_score:
                            high_score = self.score
                        if self.score >= 20 and self.score % 20 == 0:
                            self.lives += 1
                            self.sounds.play_extra_life()

                for ghost in self.ghosts:
                    if ghost.dead_timer>0:
                        ghost.dead_timer-=1
                    if self.player.rect.colliderect(ghost.rect):
                        if frightened_mode==False:
                            self.lose_life()
                            play_pacman_dies()  # self.sounds.play_pacman_dies()  # Play pacman dies sound
                        else:
                            ghost.die()

                #for tile in self.walls:
                    #tile.draw(self.screen)
                for ghost in self.ghosts:
                    if ghost.dead_timer==0:
                        ghost.draw(self.screen)

                game.draw_lives()

                if not self.dots:
                    if self.level == 2:
                        self.state = State.WIN
                    elif self.level == 1:
                        for sprite in self.all_sprites:
                            sprite.kill()
                        self.dots.clear()
                        self.power_dots.clear()
                        self.level += 1
                        self.start_level = True

                    
                score_text = SCORE_FONT.render("Score: %d" % self.player.score, True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))
                high_score_text = SCORE_FONT.render("High Score: %d" % high_score, True, (255, 255, 255))
                self.screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))

                frightened_mode_timer-=1
                pygame.display.flip()
                self.clock.tick(FRAME_RATE)

            if game.state == State.WIN:
                game.draw_win_screen()
                key = pygame.key.get_pressed()
                if key[pygame.K_p]:
                    self.player.kill()
                    for ghost in self.ghosts:
                        ghost.kill()
                    for sprite in self.all_sprites:
                        sprite.kill()
                    self.walls.clear()
                    self.dots.clear()
                    self.power_dots.clear()
                    self.start_level = True
                    self.state = State.START
                if key[pygame.K_q]:
                    self.running = False

            if game.state == State.GAMEOVER:
                game.draw_game_over_screen()
                key = pygame.key.get_pressed()
                if key[pygame.K_p]:
                    self.player.kill()
                    for ghost in self.ghosts:
                        ghost.kill()
                    for sprite in self.all_sprites:
                        sprite.kill()
                    self.walls.clear()
                    self.dots.clear()
                    self.power_dots.clear()
                    self.start_level = True
                    self.lives = 3
                    self.level = 1
                    self.score = 0
                    self.state = State.START
                if key[pygame.K_q]:
                    self.running = False

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameController()
    game.main()

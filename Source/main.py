import pygame
import sys
import random
import math
import os
from enum import Enum
from board import boards
from sprite import *
from sounds import *

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 750
PACMAN_SIZE = 30
DOT_SIZE = 20
TILE_SIZE = 50
TILE_HEIGHT = ((SCREEN_HEIGHT - 50) // 32)
TILE_WIDTH = (SCREEN_WIDTH // 30)
GHOST_SIZE = 25
GHOST_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (25, 25, 166)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PI = math.pi
FRAME_RATE = 30

CHANGE_DIRECTION_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_DIRECTION_EVENT, 1000)

HIGH_SCORE_FILE = "high_score.txt"
SCORE_FONT = pygame.font.Font(None, 36)

class State(Enum):
    START = 1
    GAME = 2
    GAMEOVER = 3


class Ghost:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/image.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.new_rect = self.rect

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, tiles, ghosts):
        self.new_rect = self.rect.copy()
        if self.direction == 'up':
            self.new_rect.move_ip(0, -5)
        elif self.direction == 'down':
            self.new_rect.move_ip(0, 5)
        elif self.direction == 'left':
            self.new_rect.move_ip(-5, 0)
        elif self.direction == 'right':
            self.new_rect.move_ip(5, 0)
        if not any(tile.rect.colliderect(self.new_rect) for tile in tiles if tile.is_wall) and \
                not any(ghost.rect.colliderect(self.new_rect) for ghost in ghosts if ghost is not self):
            self.rect = self.new_rect


class Player:
    def __init__(self, x, y, starting_lives):
        self.rect = pygame.Rect(x, y, PACMAN_SIZE, PACMAN_SIZE)
        self.new_rect = self.rect
        self.radius = PACMAN_SIZE / 2
        self.starting_pos = (x, y)
        self.score = 0
        self.lives = starting_lives

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, ((self.rect.x + self.radius), (self.rect.y + self.radius)), self.radius)

    def handle_keys(self, tiles):
        key = pygame.key.get_pressed()
        dist = 3
        self.new_rect = self.rect.copy()
        if key[pygame.K_DOWN]:  # down key
            self.new_rect.move_ip(0, dist)
        elif key[pygame.K_UP]:  # up key
            self.new_rect.move_ip(0, -dist)
        elif key[pygame.K_LEFT]:  # left key
            self.new_rect.move_ip(-dist, 0)
        elif key[pygame.K_RIGHT]:  # right key
            self.new_rect.move_ip(dist, 0)

        if not any(tile.rect.colliderect(self.new_rect) for tile in tiles if tile.is_wall):
            if self.new_rect.x <= 0:
                self.new_rect.move_ip(SCREEN_WIDTH, 0)
            if self.new_rect.x >= SCREEN_WIDTH:
                self.new_rect.move_ip(-SCREEN_WIDTH, 0)
            self.rect = self.new_rect


class Dot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, DOT_SIZE, DOT_SIZE)
        self.x = x
        self.y = y

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.circle(screen, WHITE, ((self.x + 2), (self.y + 2)), 4)


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
        self.level = boards
        self.player = Player(100, 120, 3)  # Pass the starting number of lives (3 in this case)
        #self.player = Player(100, 120)
        self.dots = []
        self.ghosts = [Ghost(290, 290)]
        self.walls = []
        self.lives = 3
        self.sounds = Sounds()

        self.player_lives = 3



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
            title = title_font.render('Game Over', True, YELLOW)
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

    def add_dot(self, dot):
        self.dots.append(dot)

    def add_wall(self, wall):
        self.walls.append(wall)

    def create_dots(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 1:
                    self.add_dot(
                        Dot((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 2), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 2)))
                if self.level[i][j] == 2:
                    pygame.draw.circle(self.screen, WHITE, (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT +
                                                            (0.5 * TILE_HEIGHT)), 10)

    def create_walls(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 3:
                    self.add_wall(Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT), 3, TILE_HEIGHT))
                if self.level[i][j] == 4:
                    self.add_wall(Tile((j * TILE_WIDTH), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5), TILE_WIDTH, 3))
                if self.level[i][j] == 5:
                    self.add_wall(
                        Tile((j * TILE_WIDTH - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5), TILE_WIDTH * 0.6,
                             3))
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3,
                             TILE_HEIGHT * 0.7))
                if self.level[i][j] == 6:
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3,
                             TILE_HEIGHT * 0.5))
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5),
                             TILE_HEIGHT * 0.7, 3))
                if self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, BLUE,
                                    [(j * TILE_HEIGHT + (TILE_HEIGHT * 0.5)), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)),
                                     TILE_WIDTH, TILE_HEIGHT], PI, 3 * PI / 2, 3)
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT), 3, TILE_HEIGHT * 0.6))
                    self.add_wall(
                        Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5),
                             TILE_WIDTH * 0.6, 3))
                if self.level[i][j] == 8:
                    self.add_wall(
                        Tile((j * TILE_WIDTH - 1.5), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT) - 1.5), TILE_WIDTH * 0.6,
                             3))
                    self.add_wall(Tile((j * TILE_WIDTH + (0.5 * TILE_WIDTH) - 1.5), (i * TILE_HEIGHT), 3, TILE_HEIGHT *
                                       0.6))
                if self.level[i][j] == 9:
                    pass
                if self.level[i][j] == 10:
                    self.player = Player(j * TILE_WIDTH + (TILE_WIDTH * 0.3), i * TILE_HEIGHT - 6)

    def draw_board(self):
        tile_height = ((SCREEN_HEIGHT - 50) // 32)
        tile_width = (SCREEN_WIDTH // 30)
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 2:
                    pygame.draw.circle(self.screen, WHITE, (j * tile_width + (0.5 * tile_width), i * tile_height +
                                                            (0.5 * tile_height)), 10)
                if self.level[i][j] == 3:
                    pygame.draw.line(self.screen, BLUE, (j * tile_width + (0.5 * tile_width), i * tile_height),
                                     (j * tile_width + (0.5 * tile_width), i * tile_height + tile_height), 3)
                if self.level[i][j] == 4:
                    pygame.draw.line(self.screen, BLUE, (j * tile_width, i * tile_height + (0.5 * tile_height)),
                                     (j * tile_width + tile_width, i * tile_height + (0.5 * tile_height)), 3)
                if self.level[i][j] == 5:
                    pygame.draw.arc(self.screen, BLUE, [(j * tile_width - (tile_width * 0.4) - 2), (i * tile_height +
                                                        (0.5 * tile_height)), tile_width, tile_height], 0, PI / 2, 3)
                if self.level[i][j] == 6:
                    pygame.draw.arc(self.screen, BLUE, [(j * tile_width + (tile_width * 0.5)), (i * tile_height +
                                                        (0.5 * tile_height)), tile_width, tile_height], PI / 2, PI, 3)
                if self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, BLUE,
                                    [(j * tile_width + (tile_width * 0.5)), (i * tile_height - (0.4 * tile_height)),
                                     tile_width, tile_height], PI, 3 * PI / 2, 3)
                if self.level[i][j] == 8:
                    pygame.draw.arc(self.screen, BLUE,
                                    [(j * tile_width - (tile_width * 0.4) - 2), (i * tile_height - (0.4 * tile_height)),
                                     tile_width, tile_height], 3 * PI / 2, 2 * PI, 3)
                if self.level[i][j] == 9:
                    pygame.draw.line(self.screen, WHITE, (j * tile_width, i * tile_height + (0.5 * tile_height)),
                                     (j * tile_width + tile_width, i * tile_height + (0.5 * tile_height)), 3)

    def restart_level(self):
        self.player.rect = pygame.Rect(self.player.starting_pos[0], self.player.starting_pos[1], PACMAN_SIZE, PACMAN_SIZE)

   #def lose_life(self):
   #     if self.lives == 1:
   #         self.lives = 0
   #         self.state = State.GAMEOVER
   #     else:
   #         self.lives -= 1
   #         self.restart_level()
    def lose_life(self):
        if self.player.lives == 1:
            self.state = State.GAMEOVER
        else:
            self.player.lives -= 1
            self.restart_level()

    def draw_lives(self):
        i = PACMAN_SIZE/2
        for life in range(self.lives):
            pygame.draw.circle(self.screen, YELLOW, (i + PACMAN_SIZE, SCREEN_HEIGHT - PACMAN_SIZE), PACMAN_SIZE/2)
            i += PACMAN_SIZE * 2

    def draw_lives(self):
        i = PACMAN_SIZE / 2
        for _ in range(self.player.lives):
            pygame.draw.circle(self.screen, YELLOW, (i + PACMAN_SIZE, SCREEN_HEIGHT - PACMAN_SIZE), PACMAN_SIZE / 2)
            i += PACMAN_SIZE * 2

    def main(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                high_score = int(f.read())
        else:
                high_score = 0 
        pygame.mixer.init()

        while self.running:
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
                    game.state = State.GAME
                    play_pacman_intro()  # self.sounds.play_intro()

            if game.state == State.GAME:

                self.screen.blit(self.surface, (0, 0))
                self.draw_board()

                self.player.handle_keys(self.walls)
                for ghost in self.ghosts:
                    ghost.update(self.walls, self.ghosts)

                for dot in self.dots:
                    if self.player.rect.colliderect(dot.rect):
                        self.dots.remove(dot)
                        self.sounds.play_pacman_eating()  # Play eating sound
                        self.player.score += 1  # Increase the score when a dot is eaten
                        if self.player.score > high_score:
                            high_score = self.player.score
                        if self.player.score >= 20:
                            self.player.lives += 1
                            self.player_lives += 1
                            self.player.score = 0
                            self.sounds.play_extra_life()
                for ghost in self.ghosts:
                    if self.player.rect.colliderect(ghost.rect):
                        self.lose_life()
                        play_pacman_dies()  # self.sounds.play_pacman_dies()  # Play pacman dies sound

                if self.start_level:
                    self.create_dots()
                    self.create_walls()
                    self.start_level = False

                #for tile in self.walls:
                    #tile.draw(self.screen)
                for ghost in self.ghosts:
                    ghost.draw(self.screen)
                self.player.draw(self.screen)
                for dot in self.dots:
                    dot.draw(self.screen)
                game.draw_lives()

                if not self.dots:
                    print("You win!")
                    self.running = False
                    
                score_text = SCORE_FONT.render("Score: %d" % self.player.score, True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))
                high_score_text = SCORE_FONT.render("High Score: %d" % high_score, True, (255, 255, 255))
                self.screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))

                pygame.display.flip()
                self.clock.tick(FRAME_RATE)

            if game.state == State.GAMEOVER:
                game.draw_game_over_screen()
                key = pygame.key.get_pressed()
                if key[pygame.K_p]:
                    self.start_level = True
                    self.dots.clear()
                    self.walls.clear()
                    self.state = State.START
                if key[pygame.K_q]:
                    self.running = False

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameController()
    game.main()

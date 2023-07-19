"""
Game Board for pac-man game
"""

import pygame
from board import boards
import math

pygame.init()

pygame.display.set_caption("NAK-MAN Pac-Man")
width = 700
height = 750
screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0)
blue = (25, 25, 166)
white = (255, 255, 255)
level = boards
pi = math.pi


def draw_board():
    tile_height = ((height - 50) // 32)
    tile_width = (width // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, white, (j * tile_width + (0.5 * tile_width), i * tile_height +
                                                   (0.5 * tile_height)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, white, (j * tile_width + (0.5 * tile_width), i * tile_height +
                                                   (0.5 * tile_height)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, blue, (j * tile_width + (0.5 * tile_width), i * tile_height),
                                 (j * tile_width + (0.5 * tile_width), i * tile_height + tile_height), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, blue, (j * tile_width, i * tile_height + (0.5 * tile_height)),
                                 (j * tile_width + tile_width, i * tile_height + (0.5 * tile_height)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, blue, [(j * tile_width - (tile_width * 0.4) - 2), (i * tile_height +
                                                                                           (0.5 * tile_height)),
                                               tile_width, tile_height], 0, pi / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, blue, [(j * tile_width + (tile_width * 0.5)), (i * tile_height +
                                                                                       (0.5 * tile_height)), tile_width,
                                               tile_height], pi / 2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, blue, [(j * tile_width + (tile_width * 0.5)), (i * tile_height -
                                                                                       (0.4 * tile_height)), tile_width,
                                               tile_height], pi, 3 * pi / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, blue, [(j * tile_width - (tile_width * 0.4) - 2), (i * tile_height -
                                                                                           (0.4 * tile_height)),
                                               tile_width, tile_height], 3 * pi / 2, 2 * pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, white, (j * tile_width, i * tile_height + (0.5 * tile_height)),
                                 (j * tile_width + tile_width, i * tile_height + (0.5 * tile_height)), 3)


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

if __name__ == "__main__":

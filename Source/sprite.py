import pygame
import pygame.sprite

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)


class Characters(pygame.sprite.Sprite):
    def __init__(self, node):
        super().__init__()
        self.node = node

    def update(self):
        pass


class Pacman(Characters):
    def __init__(self, name, color, node):
        super().__init__(node)
        self.name = name
        self.color = color
        self.images = [
            pygame.transform.scale(pygame.image.load("source/images/paku.png"), (35, 35)),
            pygame.transform.scale(pygame.image.load("source/images/man.png"), (35, 35)),
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()

    def update(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        super().update()


class Blinky(Characters):
    def __init__(self, name, color, node):
        super().__init__(node)
        self.name = name
        self.color = color
        self.images = [
            pygame.transform.scale(pygame.image.load("source/images/ghost_red.png"), (35, 35)),
            # pygame.transform.scale(pygame.image.load("images/ghost.png"), (20, 20))
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        print("test veriftied")

    def update(self, ghosts):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        super().update()


class Pinky(Characters):
    def __init__(self, name, color, node):
        super().__init__(node)
        self.name = name
        self.color = color
        self.images = [
            pygame.transform.scale(pygame.image.load("source/images/ghost_pink.png"), (35, 35)),
            # pygame.transform.scale(pygame.image.load("images/ghost.png"), (20, 20))
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()

    def update(self, ghosts):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        super().update()


class Inky(Characters):
    def __init__(self, name, color, node):
        super().__init__(node)
        self.name = name
        self.color = color
        self.images = [
            pygame.transform.scale(pygame.image.load("source/images/ghost_blue.png"), (35, 35)),
            # pygame.transform.scale(pygame.image.load("images/ghost.png"), (20, 20))
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()

    def update(self, ghosts):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        super().update()


class Clyde(Characters):
    def __init__(self, name, color, node):
        super().__init__(node)
        self.name = name
        self.color = color
        self.images = [
            pygame.transform.scale(pygame.image.load("source/images/ghost_orange.png"), (35, 35)),
            # pygame.transform.scale(pygame.image.load("images/ghost.png"), (20, 20))
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()

    def update(self, ghosts):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        super().update()

 #   def draw(self, screen):
 #       screen.blit(self.image, self.rect)


pacman = Pacman("Pac-Man", YELLOW, node=None)
ghost1 = Blinky("Ghost 1", RED, node=None)
ghost2 = Pinky("Ghost 2", BLUE, node=None)
ghost3 = Inky("Ghost 3", YELLOW, node=None)
ghost4 = Clyde("Ghost 4", ORANGE, node=None)



